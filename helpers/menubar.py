import subprocess

from PyQt5.QtWidgets import QAction, QMenu, QMessageBox
from PyQt5.QtGui import QIcon, QCursor, QColor, QFont

from helpers.dock_window import DockWindows


class MenuBar:

    def initMenuUI(self):
        directoryDock = DockWindows.directoryDockWindow(self)
        self.terminalDock = DockWindows.terminalDockWindow(self)

        exitAction = QAction(QIcon('exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        newAction = QAction(QIcon('new.png'), 'New', self)
        newAction.setShortcut('Ctrl+N')
        newAction.setStatusTip('New Application')
        newAction.triggered.connect(self.__init__)

        openAction = QAction(QIcon('open.png'), 'Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open Application')
        openAction.triggered.connect(self.openFile)

        saveAction = QAction(QIcon('save.png'), 'Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.setStatusTip('Save Application')
        saveAction.triggered.connect(self.save)

        aboutAction = QAction('About', self)
        aboutAction.setStatusTip('About')
        aboutAction.triggered.connect(self.about)

        runAction = QAction(QIcon('run.png'), 'Run', self)
        runAction.setStatusTip('Run selected configuration')
        runAction.setShortcut('Ctrl+Shift+R')
        runAction.triggered.connect(lambda: self.runCommand())

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(exitAction)

        fileMenu3 = menubar.addMenu("&View")
        fileMenu3.addAction(directoryDock.toggleViewAction())
        fileMenu3.addAction(self.terminalDock.toggleViewAction())
        fileMenu4 = menubar.addMenu('&Tools')
        fileMenu4.addAction(runAction)
        fileMenu5 = menubar.addMenu('&Help')
        fileMenu5.addAction(aboutAction)

    def contextMenuEvent(self, event):
        self.menu = QMenu(self)
        runAction = QAction(QIcon('run.png'), 'Run', self)
        runAction.triggered.connect(lambda: self.runCommand())
        self.menu.addAction(runAction)
        self.menu.popup(QCursor.pos())

    def runCommand(self):
        self.terminalShow.clear()

        try:
            directory = self.lastDirectory[0]
        except IndexError:
            QMessageBox.warning(self, 'Error',
                                "Not found any file for run!")
            return False
        self.terminalDock.show()
        cmd = ['python', f'{directory}']
        runFile = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = runFile.communicate()

        redColor = QColor(220, 20, 60)
        whiteColor = QColor(255, 255, 255)
        font = QFont()
        font.setFamily('Courier')
        font.setBold(True)
        font.setPointSize(12.5)
        self.terminalShow.setFont(font)

        if len(out.decode()) >= 1:
            self.terminalShow.setTextColor(whiteColor)
            self.terminalShow.append(out.decode())
        self.terminalShow.setTextColor(redColor)
        self.terminalShow.append(err.decode())

        self.terminalShow.setTextColor(whiteColor)
        self.terminalShow.append('Process finished with exit code 0')
