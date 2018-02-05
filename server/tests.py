# -*- coding: utf-8 -*-
import asyncio

from server.asyncServer import Server
from client.report import Report


def main(address = '127.0.0.1', port = 8080):
    "Тестируем только сервер"
    REPORTS = {i:Report(str(i), i*2, i*100) for i in range(5)}#Создаем словарь с мнимым отчетом, для тестирования
    serverObj = Server(REPORTS)
    loop = asyncio.get_event_loop()
    server_coro = asyncio.start_server(serverObj.run, address, port, loop = loop)
    server = loop.run_until_complete(server_coro)
    host = server.sockets
    print(host)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    print('Server stoped')
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

if __name__ == '__main__':
    main()
