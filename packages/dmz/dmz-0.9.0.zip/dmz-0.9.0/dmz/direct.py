# coding=utf-8

import asyncio
chunk_size = 2048


async def tcp_proxy(destination, port):

    async def handle_client(local_reader, local_writer):
        try:
            remote_reader, remote_writer = await asyncio.open_connection(*destination)
            upstream = _pipe(local_reader, remote_writer)
            downstream = _pipe(remote_reader, local_writer)
            await asyncio.gather(upstream, downstream)
        finally:
            local_writer.close()

    return await asyncio.start_server(handle_client, '0.0.0.0', port)


async def _pipe(reader, writer):
    try:
        while not reader.at_eof():
            data = await reader.read(chunk_size)
            writer.write(data)
    finally:
        writer.close()


proxy = tcp_proxy(destination=('localhost', 3306), port=3307)


loop = asyncio.get_event_loop()
server = loop.run_until_complete(proxy)
server_socket = server.sockets[0]
# server_socket.setsockopt(socket.SOL_TCP, 23, 5)
print('Serving on {}'.format(server_socket.getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
