# -*- coding: utf-8 -*-
import abc
import json

class ServerAbstract:
    def __init__(self, REPORTS):
        "Получаем глобальный список объектов отчета задач"
        self.reports = REPORTS
    def form_report(self):
        "метод формирования отчета"
        report = {}
        for url_report in self.reports:
           report[url_report] = self.reports[url_report].create_report()
        return json.dumps(report).encode()
    @abc.abstractmethod
    async def run(self, reader, writer):
        """
        Метод запуска сервера,
        coro = asyncio.start_server(ServerInstance.run, address, port, loop = loop)
        :param reader: async transport reader
        :param writer: async transport writer
        """