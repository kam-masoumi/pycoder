from PyQt5.QtWidgets import QMainWindow

from helpers.text_editor import TextEditor


class MainWindow(QMainWindow, TextEditor):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()
        self.setWindowTitle("PyCoder")
        self.resize(500, 400)
