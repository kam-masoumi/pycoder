from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QTextEdit


class TextEditor:

    @staticmethod
    def createTextEditor():
        font = QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(16)

        textEdit = QTextEdit()
        textEdit.setFont(font)

        return textEdit
