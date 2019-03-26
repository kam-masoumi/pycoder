import inspect
import resource
import sys

from PyQt5.QtWidgets import QApplication

import models
from main import MainWindow

from models.model_manager import ModelManager


def memory_limit():
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    resource.setrlimit(resource.RLIMIT_AS, (get_memory() * 1024 / 2, hard))


def get_memory():
    with open('/proc/meminfo', 'r') as mem:
        free_memory = 0
        for i in mem:
            sline = i.split()
            if str(sline[0]) in ('MemFree:', 'Buffers:', 'Cached:'):
                free_memory += int(sline[1])
    return free_memory


def create_all_database():
    classes = inspect.getmembers(sys.modules[models.__name__], inspect.isclass)
    for model in classes:
        ModelManager.create_model(model[1])
    return True


if __name__ == '__main__':
    memory_limit()
    create_all_database()
    app = QApplication(sys.argv)
    gui = MainWindow()
    gui.show()
    sys.exit(app.exec_())
