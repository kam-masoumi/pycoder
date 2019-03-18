import inspect
import sys

from PyQt5.QtWidgets import QApplication

import models
from main import MainWindow

from models.model_manager import ModelManager


def create_all_database():
    classes = inspect.getmembers(sys.modules[models.__name__], inspect.isclass)
    for model in classes:
        ModelManager.create_model(model[1])
    return True


if __name__ == '__main__':
    create_all_database()
    app = QApplication(sys.argv)
    gui = MainWindow()
    gui.show()
    sys.exit(app.exec_())