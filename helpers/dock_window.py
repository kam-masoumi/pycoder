import os

from PyQt5.QtCore import Qt, QProcess
from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import QFileSystemModel, QTreeView, QApplication, \
    QDockWidget, QTextEdit, QWidget, QPushButton, QGridLayout, QFileIconProvider, QVBoxLayout

from git.git_commands import Git
from models.color import ColorScheme


class IconProvider(QFileIconProvider):
    def icon(self, fileInfo):
        if fileInfo.isDir():
            return QIcon("images/directory.png")
        elif fileInfo.fileName()[-2:] == 'py':
            return QIcon('images/pythonfile.png')
        return QFileIconProvider.icon(self, fileInfo)


class Embterminal(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.process = QProcess(self)
        availableSize = QApplication.desktop().availableGeometry(self).size()

        status = ColorScheme().get(id=1).dark_theme
        if status is True:
            with open('.Xdefaults', 'w') as f:
                f.write('xterm*background:   #313131\n'
                        'xterm*foreground:   white\n'
                        'xterm*font:     *-fixed-*-*-*-20-*\n'
                        'xterm*BorderWidth: 0')
        else:
            with open('.Xdefaults', 'w') as f:
                f.write('xterm*background:   #FFFFFF\n'
                        'xterm*foreground:   black\n'
                        'xterm*font:     *-fixed-*-*-*-20-*\n'
                        'xterm*BorderWidth: 0\n')

        os.system('xrdb .Xdefaults')
        self.process.start('xterm', ['-into', str(int(self.winId()))])
        self.setFixedSize(availableSize/3)
        self.setMaximumWidth(availableSize.width())


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
        self.console = Embterminal()
        dock = QDockWidget("Console", self)
        # dock.setMinimumHeight(300)
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
