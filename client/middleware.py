# -*- coding: utf-8 -*-
from io import BytesIO
import pycurl
import re

#Функция которая определяет поддерживает ли сервер Ranges
#После некоторых раздумий решил её не использовать, т.к. она будет блокировать поток
def accepts_byte_ranges(self, url):
    connect = pycurl.Curl()
    header = BytesIO()
    connect.setopt(connect.URL, url)
    connect.setopt(c.NOBODY, 1)
    connect.setopt(connect.HEADERFUNCTION, header.write)
    connect.perform()
    connect.close()
    header_text = header.getvalue()
    header.close()
    match = re.search('Accept-Ranges:\s+bytes', header_text)
    if match:
        return True
    else:
        # If server explicitly specifies "Accept-Ranges: none" in the header, we do not attempt partial download.
        match = re.search('Accept-Ranges:\s+none', header_text)
        if match:
            return False
        else:
            connect = pycurl.Curl()

            # There is still hope, try a simple byte range query
            connect.setopt(connect.RANGE, '0-0') # First byte
            connect.setopt(connect.URL, url)
            connect.setopt(connect.NOBODY, 1)
            connect.perform()

            http_code = connect.getinfo(connect.HTTP_CODE)
            connect.close()

            if http_code == 206:
                return True
            else:
                return False