# -*- coding: utf-8 -*-
import asyncio
import concurrent.futures

from interfaces.abs_server import ServerAbstract

class Server(ServerAbstract):
    async def run(self, reader, writer):
        peername = writer.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        while True:
            try:
                #отлавливаем неблокирующие сообщения
                data = await asyncio.wait_for(reader.readline(), timeout=1.0)
                print(peername, ' >> ', data)
                if not data:
                    print('close connection from {}'.format(peername))
                    break
                elif data == b'get_report\n':
                    report_json = self.form_report()
                    writer.write(report_json)
                    await writer.drain()
                else:
                    print(data)
                    writer.write(b'error send data')
                    await writer.drain()
            except concurrent.futures.TimeoutError:
                #print('close connection from {}'.format(peername))
                #break
                pass
            #срабатывает при закрытии сокета со стороны клиента
            except ConnectionResetError:
                print('close connection from {}'.format(peername))
                break
            try:
                await asyncio.sleep(.1)
            except asyncio.CancelledError:
                print('Server stop ...')
                break
            #writer.write(b'plise send command')
            #await writer.drain()
        writer.close()