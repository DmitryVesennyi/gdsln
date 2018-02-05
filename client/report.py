# -*- coding: utf-8 -*-
import os

class Report:
    def __init__(self, url, dir_path, path, report_dict = None, size_download_byte = 0, downloaded = None):
        self.url = url
        self.dir_path = dir_path
        self.path = path
        self.report_dict = report_dict
        self.size = size_download_byte
        self.downloaded = downloaded
    def update(self, size = None, downloaded = None):
        if size:
            self.size = size
        self.downloaded = downloaded
        if self.report_dict is not None:
            self.report_dict[self.url] = self
    def create_report(self):
        if not self.downloaded:
            return "<{0}>, download [{1}] bytes, of all threads [{2}]\n".format(self.url, self.size, len(self.report_dict) if self.report_dict else "no data")
        else:
            return "<{0}>, Downloaded, file:/{1}\n".format(self.url, os.path.join(self.dir_path, self.path))
