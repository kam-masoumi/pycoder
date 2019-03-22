from PyQt5.QtWidgets import QAction, QMenu
from PyQt5.QtGui import QIcon, QCursor

from helpers.text_editor import TextEditor
from helpers.dock_window import DockWindows


class MenuBar:

    def initMenuUI(self):
        directoryDock = DockWindows.directoryDockWindow(self)
        terminalDock = DockWindows.terminalDockWindow(self)

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
        fileMenu3.addAction(terminalDock.toggleViewAction())
        fileMenu4 = menubar.addMenu('&Tools')
        fileMenu4.addAction(runAction)
        fileMenu5 = menubar.addMenu('&Help')
        fileMenu5.addAction(aboutAction)

        self.setWindowIcon(QIcon('text.png'))
        self.show()

    def contextMenuEvent(self, event):
        self.menu = QMenu(self)
        runAction = QAction(QIcon('run.png'), 'Run', self)
        runAction.triggered.connect(lambda: self.runCommand())
        self.menu.addAction(runAction)
        self.menu.popup(QCursor.pos())
