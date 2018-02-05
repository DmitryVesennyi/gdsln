import os
import asyncio

import aiohttp

from client.report import Report
from client.asyncClient import  DownloadTask
from config import COUNT_BYTES, COUNT_TASKS, DOWNLOAD_PATH, URLS

def main():
    "Тестируем только клиент"
    os.chdir(DOWNLOAD_PATH)
    clientObj = aiohttp.ClientSession()
    loop = asyncio.get_event_loop()
    tasks = [loop.create_task(DownloadTask(Report, DOWNLOAD_PATH, url, clientObj, concurrency=COUNT_TASKS, countBytes=COUNT_BYTES).download()) for url in URLS]
    wait_tasks = asyncio.wait(tasks)
    loop.run_until_complete(wait_tasks)
    for task in tasks:
        print(task.result())
        task.cancel()
    clientObj.close()
    loop.close()


if __name__ == "__main__":
    main()
    """
        Тестировал на локалхосте, в качестве range-сервера был nginx.
        Тест прошел успешно.
    """