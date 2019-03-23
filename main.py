import webbrowser

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QLabel

from helpers.menubar import MenuBar
from helpers.themes import ThemeEdit
from helpers.tabs import Tabs
from helpers.text_editor import TextEditor
from helpers.dock_window import DockWindows


class MainWindow(QMainWindow, TextEditor, MenuBar, ThemeEdit, Tabs, DockWindows):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initTabUI()
        self.initThemeUI()
        self.initMenuUI()
        self.setWindowTitle("PyCoder")

        backGround = QLabel()
        backGround.setAlignment(Qt.AlignCenter)
        backGround.setPixmap(QPixmap("python.png"))

        self.setCentralWidget(backGround)

        self.resize(500, 500)
        self.lastDirectory = []

    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.statusBar().showMessage('Quiting...')
            event.accept()

        else:
            event.ignore()

    def openFile(self):
        self.statusBar().showMessage('Open Text Files ')
        fileDirectory = QFileDialog.getOpenFileName(self, 'Open file', '/home', "Python Files (*.py *.h)")
        fileName = fileDirectory[0].split('/')[-1]
        self.statusBar().showMessage(f'{fileDirectory[0]}')
        if fileDirectory[0]:
            f = open(fileDirectory[0], 'r')
            with f:
                data = f.read()
                self.createTab(data, fileName, fileDirectory[0])

    def save(self):
        currentTabWidget = self.tabs.currentWidget()
        self.statusBar().showMessage('Add extension to file name')
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,
                                                  "Save file",
                                                  "Pyhton file (*.py)", options=options)
        if fileName and currentTabWidget is not None:
            try:
                data = currentTabWidget.toPlainText()
                with open(fileName, 'w') as f:
                    f.write(data)
            except FileNotFoundError:
                pass

    def copy(self):
        cursor = self.textEdit.textCursor()
        textSelected = cursor.selectedText()
        self.copiedtext = textSelected

    def paste(self):
        self.textEdit.append(self.copiedtext)

    def cut(self):
        cursor = self.textEdit.textCursor()
        textSelected = cursor.selectedText()
        self.copiedtext = textSelected
        self.textEdit.cut()

    def about(self):
        url = "https://github.com/kam-masoumi/pycoder"
        self.statusBar().showMessage('Loading url...')
        webbrowser.open(url)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('text/plain'):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        fileDirectory = event.mimeData().text()[7:-2]
        fileName = fileDirectory.split('/')[-1]
        if fileName[-2:] != 'py':
            return event.ignore()
        f = open(fileDirectory, 'r')
        with f:
            data = f.read()
            self.createTab(data, fileName, fileDirectory)
