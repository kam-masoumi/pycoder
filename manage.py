import inspect
import sys

import time
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QSplashScreen, QProgressBar

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

    splash_pix = QPixmap('images/loading.jpg')

    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
    splash.setEnabled(False)

    progressBar = QProgressBar(splash)
    progressBar.setStyleSheet("""
    QProgressBar {
    text-align: center;
    }
    QProgressBar::chunk {
    background-color: rgb(49,49,49);
    width: 10px;
    }
    """)
    progressBar.setMaximum(10)
    progressBar.setGeometry(0, splash_pix.height() - 17, splash_pix.width(), 20)

    splash.show()
    splash.showMessage("<h1><font color='white'>Enjoy from this editor</font></h1>", Qt.AlignBottom | Qt.AlignCenter)

    for i in range(1, 10):
        progressBar.setValue(i)
        t = time.time()
        while time.time() < t + 0.1:
            app.processEvents()

    gui = MainWindow()
    gui.show()
    splash.finish(gui)
    sys.exit(app.exec_())
