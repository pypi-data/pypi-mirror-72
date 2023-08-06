# coding=utf-8

import json
import uuid
import logging

chunk_size = 2048


def uuid_str():
    return str(uuid.uuid4()).replace('-', '')


def parse_address(addr, server_name='server'):
    bb = addr.split(':')
    if len(bb) != 2:
        raise Exception(f"{server_name}({addr}) format error, should be <host>:<port>")
    return bb[0], int(bb[1])


async def pipe_stream(reader, writer):
    try:
        while not reader.at_eof():
            data = await reader.read(chunk_size)
            writer.write(data)
    finally:
        try:
            writer.close()
        except Exception as e:
            logging.error(e, exc_info=True)


async def send_cmd(writer, cmd):
    content = json.dumps(cmd)
    buff = len(content).to_bytes(4, byteorder='big')
    buff += content.encode('utf-8')
    writer.write(buff)
    await writer.drain()


async def recv_cmd(reader, cmd_handler_table):
    buffer = b''
    body_len = 0
    while not reader.at_eof():
        data = await reader.read(chunk_size)
        buffer += data
        if not body_len:
            if len(buffer) < 4:
                continue
            body_len = int.from_bytes(buffer[0:4], byteorder='big')
            buffer = buffer[4:]
        if len(buffer) < body_len:  # body not ready
            continue

        body = buffer[0: body_len]
        buffer = buffer[body_len:]
        body_len = 0
        try:
            body = json.loads(body, encoding='utf-8')
            logging.debug(f"Command: {body}")
            cmd = body.get('cmd')
            param = body.get('param')
            if not cmd:
                logging.warning("cmd missing")
                continue
            handler = cmd_handler_table.get(cmd)
            if not handler:
                logging.warning(f"cmd({cmd}) missing handler")
                continue
            try:
                handler(param)
            except Exception as e:
                logging.error(e, exc_info=True)

        except Exception as e:
            logging.error(e, exc_info=True)
            return False

HTTP_METHODS = [
    'GET',
    'HEAD',
    'POST',
    'PUT',
    'DELETE',
    'CONNECT',
    'OPTIONS',
    'TRACE',
    'PATCH'
]


def find_header_end(buf, start=0):
    i = start
    end = len(buf)
    while i + 3 < end:
        if buf[i] == 13 and buf[i + 1] == 10 and buf[i + 2] == 13 and buf[i + 3] == 10:
            return i + 3
        i += 1
    return -1


def find_access_id(buf):
    buf = buf.decode('utf-8')
    lines = buf.splitlines()
    for i in range(1, len(lines)):
        line = lines[i]
        if len(line) == 0:
            continue
        try:
            p = line.index(':')
            key = str(line[0:p]).strip()
            val = str(line[p + 1:]).strip()
            if key == 'access_id':
                return val
        except Exception as e:
            logging.error(e)


def http_type_quick_fail(buffer):
    s = buffer.decode('utf-8')
    s = s.upper()
    for m in HTTP_METHODS:
        if s.startswith(m):
            return False

    return True


async def detect_access_id_in_http_header(reader):
    max_header = 64*1024
    buffer = b''
    while not reader.at_eof():
        data = await reader.read(1024)
        buffer += data
        if len(buffer) > 10:    # http methods length
            if http_type_quick_fail(buffer):    # 快速判断不是HTTP请求第一行的开头方法
                return buffer, -1

        p = find_header_end(buffer, 0)
        if p < 0:
            if len(buffer) > max_header:
                return buffer, -1
            continue
        head = buffer[0: p]
        access_id = find_access_id(head)
        return buffer, access_id


async def http_reply(writer, msg):
    size = len(msg)
    data = f"""HTTP/1.1 400 Bad Request\r\nContent-Length: {size}\r\n\r\n{msg}"""
    writer.write(data.encode('utf-8'))
    await writer.drain()
