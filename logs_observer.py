# region Imports

import threading
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

# endregion


# region Watchdog handler


class LogFileHandler(FileSystemEventHandler):
    """
    Обработчик событий для файла логов. Выводит новые строки по мере появления.
    """

    def __init__(self, logfile_path: str):
        self.logfile_path = logfile_path
        self.logfile = open(logfile_path, "r")
        self.logfile.seek(0, 2)  # Перемещаем указатель в конец файла

    def on_modified(self, event):
        if event.src_path == self.logfile_path:
            new_line = self.logfile.readline()
            while new_line:
                print(new_line.strip())
                new_line = self.logfile.readline()


# endregion

# region Запуск Watchdog в отдельном потоке


def start_watchdog(logfile_path: str):
    """
    Функция для запуска наблюдателя за файлом логов в отдельном потоке.
    Args:
        logfile_path (str): Путь к файлу логов.
    """
    event_handler = LogFileHandler(logfile_path)
    observer = Observer()
    observer.schedule(event_handler, path=logfile_path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


def run_watchdog_in_thread(logfile_path: str):
    """
    Запуск Watchdog в отдельном потоке, чтобы не блокировать основной цикл FastAPI.
    """
    watchdog_thread = threading.Thread(target=start_watchdog, args=(logfile_path,), daemon=True)
    watchdog_thread.start()


# endregion
