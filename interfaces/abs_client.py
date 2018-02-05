# -*- coding: utf-8 -*-
import abc
import os
import logging

class AsyncClientAbstract(abc.ABC):
    def __init__(self, urlDownload, asyncClient, concurrency=2, timeout=0, headers=None, countBytes = 512):
        self.urlDownload = urlDownload
        self.concurrency = concurrency
        self.timeout = timeout
        self.countBytes = countBytes
        if not headers:
            self.headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.5',
                            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0',
                            'Connection': 'keep-alive'}
        else:
            self.headers = headers
        self.client = asyncClient

        logging.basicConfig(level='INFO')
        self.log = logging.getLogger()
        #Получаем количество загруженных байт, если файл есть и он не пуст
        self.getBytes()
    def getBytes(self):
        self.path = os.path.split(self.urlDownload)[1]
        try:
            self.size = os.path.getsize(os.path.split(self.urlDownload)[1])
        except FileNotFoundError:
            self.size = 0
    @abc.abstractmethod
    def report(self, size_downloads):
        """
        Система отчетов.
        При каждом скачивании кусочка это событие будет заноситься в глобальный словарь
        :param size_downloads: сколько уже скачали байт int
        """
    @abc.abstractmethod
    def download(self):
        """
            Функцию скачивания нужно переопределить
        """

