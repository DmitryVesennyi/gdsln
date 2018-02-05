# -*- coding: utf-8 -*-
import time
import asyncio
import os

import aiohttp

from client.asyncClient import  DownloadTask
from config import COUNT_BYTES, COUNT_TASKS, DOWNLOAD_PATH, URLS
from server.asyncServer import Server
from client.report import Report

"Собираем вместе клиент и сервер"

class Conductor:
    def __init__(self, event_loop, urls, download_path, countBytes = 1024, countTask = 4):
        self.countTask = countTask
        self.urls = urls
        self.download_path = download_path
        self.countBytes = countBytes
        self.queue = asyncio.Queue()
        self.client = aiohttp.ClientSession()
        self.REPORTS = {}

        self.loop = event_loop
        os.chdir(DOWNLOAD_PATH)
    def worker(self, urls_tasks):
        tasks = [asyncio.ensure_future(DownloadTask(Report, self.download_path, url, self.client, timeout = 0, concurrency=self.countTask, countBytes=self.countBytes, reports_dict=self.REPORTS).run()) for url in self.urls]
        return tasks
    async def downloads(self):
        print('Starting downloading ...')
        tasks = self.worker(self.urls)
        await asyncio.gather(*tasks)
        return tasks
    def run(self, address = '127.0.0.1', port = 8080):
        start = time.time()
        print('Starting server ...')
        serverObj = Server(self.REPORTS)
        server_coro = asyncio.start_server(serverObj.run, address, port, loop = self.loop)
        server = asyncio.async(server_coro)

        tasks = loop.run_until_complete(self.downloads())

        #Закрываем выполненные сопрограммы
        for task in tasks:
            task.cancel()

        server.cancel()
        self.client.close()
        self.loop.close()
        end = time.time()
        print('FINISHED CONDUCTOR AT {} secs'.format(end-start))

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    conductor = Conductor(loop, URLS, DOWNLOAD_PATH, COUNT_BYTES, 4)
    print("Start Conductor ...")
    conductor.run()
