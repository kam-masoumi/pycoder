import webbrowser

from PyQt5.QtCore import Qt, QFile, QStringListModel
from PyQt5.QtGui import QPixmap, QCursor, QIcon
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QLabel, QCompleter, QApplication, QTextEdit

from helpers.menubar import MenuBar
from helpers.themes import ThemeEdit
from helpers.tabs import Tabs
from helpers.dock_window import DockWindows


class MainWindow(QMainWindow, MenuBar, ThemeEdit, Tabs, DockWindows):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initTabUI()
        self.initThemeUI()
        self.initMenuUI()
        self.setWindowTitle("PyCoder")
        self.setWindowIcon(QIcon('images/pycoder.png'))

        self.completer = QCompleter(self)
        self.completer.setModel(self.modelFromFile('wordlist.txt'))
        self.completer.setModelSorting(QCompleter.CaseInsensitivelySortedModel)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setWrapAround(False)
        self.completer.popup().setStyleSheet("background-color: rgb(49,49,49);"
                                             "color: silver;"
                                             "font-size: 18px;"
                                             "width: 20px;")
        backGround = QLabel()
        backGround.setAlignment(Qt.AlignCenter)
        backGround.setPixmap(QPixmap("images/python.png"))

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

    def newFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        directory, _ = QFileDialog.getSaveFileName(self,
                                                  "New file",
                                                  "Pyhton file (*.py)", options=options)

        fileName = directory.split('/')[-1]
        if fileName[-2:] == 'py':
            try:
                with open(directory, 'w') as f:
                    f.write('')
                    self.createTab('', fileName, directory)
            except FileNotFoundError:
                pass
        else:
            QMessageBox.warning(self, 'Error',
                                "This is not python file!")

    def openFile(self):
        self.statusBar().showMessage('Open Text Files ')
        fileDirectory = QFileDialog.getOpenFileName(self, 'Open file', '/home', "Python Files (*.py *.h)")
        fileName = fileDirectory[0].split('/')[-1]
        self.statusBar().showMessage(f'{fileDirectory[0]}')
        if fileDirectory[0]:
            with open(fileDirectory[0], 'r') as f:
                data = f.read()
                self.createTab(data, fileName, fileDirectory[0])

    def openProject(self):
        directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        directoryDock = DockWindows.directoryDockWindow(self, directory)
        self.fileMenu3.addAction(directoryDock.toggleViewAction())

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

    def modelFromFile(self, fileName):
        f = QFile(fileName)
        if not f.open(QFile.ReadOnly):
            return QStringListModel(self.completer)

        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

        words = []
        while not f.atEnd():
            line = f.readLine().trimmed()
            if line.length() != 0:
                try:
                    line = str(line, encoding='ascii')
                except TypeError:
                    line = str(line)

                words.append(line)

        QApplication.restoreOverrideCursor()

        return QStringListModel(words, self.completer)
