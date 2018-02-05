# -*- coding: utf-8 -*-
import asyncio
import logging

from interfaces.abs_client import AsyncClientAbstract

class DownloadTask(AsyncClientAbstract):
    def __init__(self, obj_report, dir_path, urlDownload, asyncClient, concurrency=2, timeout=0, headers=None, countBytes = 512, reports_dict = None):
        super().__init__(urlDownload, asyncClient, concurrency, timeout, headers, countBytes)
        self.obj_report = obj_report(self.urlDownload, dir_path, self.path, reports_dict)
    async def run(self):
        #Устанавливаем ограничение одновременных задач
        semaphore = asyncio.Semaphore(self.concurrency)
        with (await semaphore):
            await self.download()
    async def download(self):
        file = open(self.path, 'ab')
        while True:
            self.headers["Range"] = "bytes={0}-{1}".format(self.size, self.size + self.countBytes)
            async with self.client.get(self.urlDownload, headers=self.headers) as response:
                #Проверяем поддерживает ли сервер Range, если нет, то выходим из цикла
                #и начинаем качать кусочками обычным образом
                if response.status == 206:
                    content_bytes = await response.read()
                elif response.status == 200:
                    break
                elif response.status == 416:
                    # Закрываем канал файла и записываем все на диск.
                    file.close()
                    logging.info('Range File stored at {}'.format(self.path))
                    self.obj_report.update(downloaded = True)
                    await asyncio.sleep(self.timeout)
                    return self.report
                else:
                    #Видимо тут произошла какя-то ошибка - возвращаем None
                    self.log.error('BAD RESPONSE: {}'.format(response.status))
                    return None
            # Складываем в буфер файла полученные байты
            file.write(content_bytes)
            self.size += self.countBytes + 1
            self.obj_report.update(self.size)
        #Если сервер не поддерживает Range, просто кусками читаем файл
        async with self.client.get(self.urlDownload, headers=self.headers) as response:
            count_bytes = 0
            while True:
                # Читаем буфер и записываем полученные данные в файл.
                # Здесь всё синхронно.
                chunk = await response.read(self.size)
                if not chunk:
                    file.close()
                    break
                file.write(chunk)
                self.obj_report.update(count_bytes)
        logging.info('File stored at {}'.format(self.path))
        self.obj_report.update(downloaded = True)
        await asyncio.sleep(self.timeout)
        return self.report
    @property
    def report(self):
        return self.obj_report.create_report()


