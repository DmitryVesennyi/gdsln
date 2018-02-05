# -*- coding: utf-8 -*-
import asyncio
import socket
from string import ascii_letters
import random


class BroadcastProtocol:

    def __init__(self, loop):
        self.loop = loop

    def connection_made(self, transport):
        print('started')
        self.transport = transport
        sock = transport.get_extra_info("socket")
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.broadcast()

    def datagram_received(self, data, addr):
        print('data received:', data, addr)

    def broadcast(self):
        string = ''.join([random.choice(ascii_letters) for _ in range(5)])
        print('sending:', string)
        self.transport.sendto(string.encode(), ('192.168.43.255', 9090))
        self.loop.call_later(5, self.broadcast)

loop = asyncio.get_event_loop()
coro = loop.create_datagram_endpoint(
    lambda: BroadcastProtocol(loop), local_addr=('0.0.0.0', 9090))
loop.run_until_complete(coro)
loop.run_forever()
loop.close()