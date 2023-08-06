# coding=utf-8
import asyncio
import logging
import logging.config
import os
import argparse
import sys
sys.path.append('./')

from dmz.common import parse_address, pipe_stream, send_cmd, recv_cmd

class NotifyAgent:
    def __init__(self, config, loop):
        self.loop = loop
        self.notify_server = config.get('notify_server')
        self.proxy_server = config.get('proxy_server')
        self.target_server = config.get('target_server')

        self.notify_host, self.notify_port = parse_address(self.notify_server, 'notify_server')
        self.proxy_host, self.proxy_port = parse_address(self.proxy_server, 'proxy_server')
        self.target_host, self.target_port = parse_address(self.target_server, 'target_server')

        self.connect_timeout = config.get('connect_timeout', 3.0)
        acl = config.get('acl', {})
        self.access_id = acl.get('access_id', '')
        self.register_token = acl.get('register_token', '')

    async def start(self):
        notify_reader, notify_writer = None, None
        try:
            # logging.info(f'Connecting to NotifyServer({self.notify_server})')
            notify_reader, notify_writer = await asyncio.open_connection(self.notify_host, self.notify_port)
            logging.info(f'Connected to NotifyServer({self.notify_server})')

            cmd = {
                'cmd': 'register',
                'param': {
                    'access_id': self.access_id,
                    'register_token': self.register_token
                }
            }
            # 注册通知
            await send_cmd(notify_writer, cmd)

            def bind_handler(param):
                stream_id = param['stream_id']
                logging.debug(f'Binding ({self.target_server}) <==> ({self.proxy_server})')
                self.loop.create_task(self.bind_proxy(stream_id))

            cmd_handler_table = {
                'bind': bind_handler
            }
            await recv_cmd(notify_reader, cmd_handler_table)

        except ConnectionRefusedError:
            logging.warning(f'Connection to server NotifyServer({self.notify_server}) failed!')
        except asyncio.TimeoutError:
            logging.warning(f'Connection to server NotifyServer({self.notify_server}) timed out!')
        except Exception as e:
            logging.error(e, exc_info=True)
        finally:
            if notify_writer:
                notify_writer.close()
            await asyncio.sleep(self.connect_timeout)
            await self.start()

    async def bind_proxy(self, stream_id):
        # logging.debug(f'Connecting to TargetServer({self.target_server})')
        target_reader, target_writer = await asyncio.open_connection(self.target_host, self.target_port)
        logging.info(f'Connected to TargetServer({self.target_server})')

        # logging.debug(f'Connecting to ProxyServer({self.proxy_server})')
        proxy_reader, proxy_writer = await asyncio.open_connection(self.proxy_host, self.proxy_port)
        logging.info(f'Connected to ProxyServer({self.proxy_server})')

        proxy_writer.write(stream_id.encode('utf-8'))   # 固定32个字节的uuid
        await proxy_writer.drain()

        upstream = pipe_stream(target_reader, proxy_writer)
        downstream = pipe_stream(proxy_reader, target_writer)
        await asyncio.gather(upstream, downstream)


async def main(config_file, loop):
    import json
    with open(config_file) as json_file:
        config = json.load(json_file)

    agent = NotifyAgent(config, loop)
    await agent.start()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='DMZ Server')
    parser.add_argument('--config', default='../dmz_agent.json', help='DMZ server config json file')
    parser.add_argument('--log', default='../log.conf', help='DMZ server config json file')
    args = parser.parse_args()
    config_file = args.config
    log_file = args.log

    logging_conf_path = os.path.join(os.getcwd(), log_file)
    logging.config.fileConfig(logging_conf_path)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(config_file, loop))
    loop.close()
