# coding=utf-8

import asyncio
import logging
import logging.config
import os
import argparse
import sys
sys.path.append('./')

from dmz.common import parse_address, pipe_stream, send_cmd, recv_cmd, uuid_str
from dmz.common import detect_access_id_in_http_header, http_reply


class FrontServerInfo:
    def __init__(self):
        self.server = None      # ProxyFront服务器
        self.agent_table = {}   # access_id => agent writer
        self.listen = ''
        self.protocol = ''
        self.acl = []


class NotifyServer:
    def __init__(self, notify_server_address, front_server_table):
        self.notify_server_address = notify_server_address
        self.notify_host, self.notify_port = parse_address(self.notify_server_address, 'notify_server')

        self.front_server_table = front_server_table

    async def notify_downstream(self, server_addr, access_id, upstream_id):
        """
        通知下游内网代理主动创建链接上来
        :param server_addr: 服务器地址
        :param access_id: 访问标识
        :param upstream_id: 上游链接唯一标识，UUID
        :return:
        """
        front_server = self.front_server_table.get(server_addr)
        if not front_server:
            raise Exception(f"ProxyFront({server_addr}) not exists")

        if access_id is None:
            if front_server.protocol == 'http':
                logging.error(f"access_id is missing")
                return False
            else:   # TCP 默认到任意一个
                if len(front_server.agent_table) > 0:
                    for key in front_server.agent_table:
                        agent = front_server.agent_table[key]
                        break
        else:
            agent = front_server.agent_table.get(access_id)

        if agent is None:
            logging.error(f"{access_id} has no downstream agent")
            return False

        logging.debug(f"Notify agent: {upstream_id}")
        cmd = {
            'cmd': 'bind',
            'param': {
                'stream_id': upstream_id
            }
        }
        await send_cmd(agent, cmd)
        return True

    async def start(self):
        async def handle_client(reader, writer):

            def agent_register(param):
                access_id = param.get('access_id', '')  # access_id 是全局唯一的
                register_token = param.get('register_token', '')
                for listen in self.front_server_table:
                    info = self.front_server_table[listen]
                    found = False
                    for item in info.acl:
                        if access_id == item['access_id']:
                            found = True
                            if register_token != item['register_token']:
                                logging.warning(f"register_token denied for access_id({access_id})")
                                return
                    if found:
                        front_server = info
                        break
                if not front_server:
                    logging.warning(f"access_id({access_id}) not exists for any server")
                    return

                logging.info(f"Agent({access_id}) for {front_server.protocol}://{front_server.listen} joined")
                front_server.agent_table[access_id] = writer

            cmd_handler_table = {
                'register': agent_register
            }
            try:
                await recv_cmd(reader, cmd_handler_table)
            finally:
                writer.close()
        # logging.info(f"Starting NotifyServer({self.notify_server})")
        server = await asyncio.start_server(handle_client, self.notify_host, self.notify_port)
        logging.info(f"NotifyServer({self.notify_server_address}) started")
        return server


class DmzServer:
    def __init__(self, config):
        self.config = config
        self.front_streams = {}

        self.front_server_table = {} # listen => FrontServerInfo
        for front_config in self.config.get('proxy_front_list', []):
            info = FrontServerInfo()
            info.listen = front_config.get('listen')    # TODO check empty
            info.protocol = front_config.get('protocol', 'tcp').lower()
            info.acl = front_config.get('acl', [])

            self.front_server_table[info.listen] = info

        self.proxy_back_address = self.config.get('proxy_back')
        self.notify_server_address = self.config.get('notify_server')

        self.notify_server = NotifyServer(self.notify_server_address, self.front_server_table)

    async def start(self):
        for listen in self.front_server_table:
            info = self.front_server_table[listen]
            info.server = await self.start_proxy_front(info)

        await self.notify_server.start()

        await self.start_proxy_back()

    async def start_proxy_front(self, front_info: FrontServerInfo):
        """
        启动代理前端
        1）接收到链接请求
        2）做必要协议分析（如果使能）出访问目标
        3）根据访问目标发送通知到下游代理（代理主动链接到代理后端）
        :return:
        """
        host, port = parse_address(front_info.listen, 'proxy_front')

        async def handle_client(front_reader, front_writer):
            checked_buffer, access_id = None, None
            if front_info.protocol == 'http':
                checked_buffer, access_id = await detect_access_id_in_http_header(front_reader)

            stream_id = uuid_str()
            self.front_streams[stream_id] = (front_reader, front_writer, checked_buffer)
            logging.debug(f"ProxyFront connection>>>: {stream_id}")
            res = await self.notify_server.notify_downstream(front_info.listen, access_id, stream_id)
            if not res:
                try:
                    front_writer.close()
                except:
                    pass

        # logging.info(f"Starting ProxyFrontServer({proxy_front})")
        server = await asyncio.start_server(handle_client, host, port)
        logging.info(f"ProxyFrontServer({front_info.listen}) started")
        return server

    async def start_proxy_back(self):
        host, port = parse_address(self.proxy_back_address, 'proxy_back')

        async def handle_client(back_reader, back_writer):
            try:
                stream_id_size = 32
                data = await back_reader.read(stream_id_size)
                stream_id = data.decode('utf-8')
                logging.debug(f"ProxyBack connection<<<: {stream_id}")
                front = self.front_streams.get(stream_id)
                if front is None:
                    logging.error(f"Unknown/obsolete upstream: {stream_id}")
                    return
                front_reader, front_writer, checked_buffer = front
                if checked_buffer:  # 预先读了的数据
                    back_writer.write(checked_buffer)

                upstream = pipe_stream(back_reader, front_writer)
                downstream = pipe_stream(front_reader, back_writer)
                await asyncio.gather(upstream, downstream)
            finally:
                back_writer.close()

        # logging.info(f"Starting ProxyBackServer({proxy_back})")
        server = await asyncio.start_server(handle_client, host, port)
        logging.info(f"ProxyBackServer({self.proxy_back_address}) started")
        return server


async def main(config_file):
    import json
    with open(config_file) as json_file:
        config = json.load(json_file)
    server = DmzServer(config)
    await server.start()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='DMZ Server')
    parser.add_argument('--config', default='../dmz_server.json', help='DMZ server config json file')
    parser.add_argument('--log', default='../log.conf', help='DMZ server config json file')
    args = parser.parse_args()
    config_file = args.config
    log_file = args.log

    logging_conf_path = os.path.join(os.getcwd(), log_file)
    logging.config.fileConfig(logging_conf_path)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(config_file))
    loop.run_forever()
