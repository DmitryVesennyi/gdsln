# gdsln
python 3.6.3

Файл запуска - conductor/conductor.py

В файле confog.py, вписываем переменные(URLS, COUNT_BYTES, COUNT_TASKS, DOWNLOAD_PATH).

Как это работает:
	-Запускается несколько асинхронных задач(несколько таск клиента и одна таска сервера)
	-Клиент асинхронно обходит urls и начинает скачивать COUNT_BYTES, сохраняя файлы в буфере
	-В это же время сервер отслеживает процесс работы и при обращении к нему выдает отчет в виде json
									(sock.send(b'get_report\n')
									 sock.recv(..))
