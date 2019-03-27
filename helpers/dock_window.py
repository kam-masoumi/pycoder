import subprocess

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QTextCursor
from code import InteractiveConsole

from PyQt5.QtWidgets import QFileSystemModel, QTreeView, QApplication, \
    QDockWidget, QTextEdit, QWidget, QPushButton, QGridLayout, QFileIconProvider, QPlainTextEdit

from git.git_commands import Git
from helpers.text_editor import TextEditor

class IconProvider(QFileIconProvider):
    def icon(self, fileInfo):
        if fileInfo.isDir():
            return QIcon("images/directory.png")
        elif fileInfo.fileName()[-2:] == 'py':
            return QIcon('images/pythonfile.png')
        return QFileIconProvider.icon(self, fileInfo)


class DockWindows:

    def directoryDockWindow(self, directory=None):

        try:
            oldDock = self.lastDockDirectory[0]
            self.removeDockWidget(oldDock)
            self.lastDockDirectory.clear()
            self.lastGit.clear()
        except IndexError:
            pass

        self.model = QFileSystemModel()
        self.model.setReadOnly(False)
        self.model.setRootPath('/home')
        self.model.setIconProvider(IconProvider())

        tree = QTreeView()
        tree.setModel(self.model)
        tree.setRootIndex(self.model.index(f'{directory}'))
        tree.doubleClicked.connect(self.openNewFile)

        tree.setAnimated(True)
        tree.setIndentation(20)

        availableSize = QApplication.desktop().availableGeometry(tree).size()
        tree.resize(availableSize / 2)
        tree.setColumnWidth(0, tree.width() / 3)

        dock = QDockWidget("Project", self)
        self.lastDockDirectory.append(dock)
        dock.setMinimumWidth(200)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea)
        dock.setWidget(tree)

        self.addDockWidget(Qt.LeftDockWidgetArea, dock)
        self.lastGit.append(Git(directory))
        return dock

    def consoleDockWindows(self):
        self.console = QTextEdit()
        self.console.setText('>>> ')
        self.console.keyReleaseEvent = self.consoleNewLine
        dock = QDockWidget("Console", self)
        dock.setMinimumHeight(300)
        dock.setWidget(self.console)
        dock.hide()
        self.addDockWidget(Qt.BottomDockWidgetArea, dock)


        return dock

    def terminalDockWindow(self):
        dockLayout = QGridLayout()

        self.terminalShow = QTextEdit()
        self.terminalShow.setReadOnly(True)

        runButton = QPushButton(QIcon('images/run.png'), '')
        runButton.clicked.connect(self.runCommand)

        dock = QDockWidget("Run", self)
        dock.setMinimumHeight(300)
        self.addDockWidget(Qt.BottomDockWidgetArea, dock)

        dockedWidget = QWidget(self)
        dock.setWidget(dockedWidget)
        dockedWidget.setLayout(dockLayout)
        dockedWidget.layout().addWidget(runButton, 0, 0, Qt.AlignTop)
        dockedWidget.layout().addWidget(self.terminalShow, 0, 1)

        dock.setAllowedAreas(Qt.BottomDockWidgetArea)
        dock.hide()
        return dock

    def openNewFile(self, signal):
        directory = self.model.filePath(signal)
        pythonFile = directory.split('/')[-1]
        try:
            if pythonFile[-2:] == 'py':
                with open(directory, 'r') as f:
                    self.createTab(f.read(), pythonFile, directory)
        except IndexError:
            pass

    def consoleNewLine(self, event):
        if event.key() == 16777220:

            cursor = self.console.textCursor()
            cursor.movePosition(QTextCursor.End)

            document = self.console.document()
            lineCount = document.lineCount()
            lastCode = document.findBlockByLineNumber(lineCount - 2).text()
            result = console.enter(lastCode[4:])
            self.console.append(result)
            self.console.append('>>> ')


from code import InteractiveConsole
from imp import new_module


class Console(InteractiveConsole):

    def __init__(self, names=None):
        names = names or {}
        names['console'] = self
        InteractiveConsole.__init__(self, names)
        self.superspace = new_module('superspace')

    def enter(self, source):
        import subprocess
        source = self.preprocess(source)

        with open('console.py', 'a') as f:
            f.write('\n')
            f.write(source)
        runFile = subprocess.Popen(['python', 'console.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = runFile.communicate()
        print(out, err)
        return out.decode()

    @staticmethod
    def preprocess(source):
        return source


console = Console()
