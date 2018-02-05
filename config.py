# -*- coding: utf-8 -*-
#Пути для скачивания файлов
URLS = ["http://localhost:9000/foto/temp.jpg", "http://localhost:9000/foto/IMG_20170712_142613.jpg",
        "http://localhost:9000/foto/IMG_20170712_142624.jpg", "http://localhost:9000/foto/Ayshirskaya-poroda-korov.jpg",
        "http://localhost:9000/foto/CHerno-pestraya-poroda-korov.jpg", "http://localhost:9000/foto/Dzheyserskaya-poroda-korov.jpg",
        "http://localhost:9000/foto/Golshtinskaya-poroda-korov.jpg",
        "http://localhost:9000/foto/Снимок экрана от 2017-09-18 16-36-37.png"]
#Порция скачивания
COUNT_BYTES = 512
#Количество одновременных задач
COUNT_TASKS = 4
#Папка куда будут складываться файлы
DOWNLOAD_PATH = '/home/jacksparrow/tests'