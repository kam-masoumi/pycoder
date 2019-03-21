from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon

from helpers.text_editor import TextEditor
from helpers.dock_window import DockWindows

class MenuBar:

    def initMenuUI(self):
        directoryDock = DockWindows.directoryDockWindow(self)
        terminalDock = DockWindows.terminalDockWindow(self)
        c = TextEditor.createTextEditor()
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

        undoAction = QAction(QIcon('undo.png'), 'Undo', self)
        undoAction.setShortcut('Ctrl+Z')
        undoAction.setStatusTip('Undo')
        undoAction.triggered.connect(c.undo)

        redoAction = QAction(QIcon('redo.png'), 'Redo', self)
        redoAction.setShortcut('Ctrl+Y')
        redoAction.setStatusTip('Redo')
        redoAction.triggered.connect(c.redo)

        copyAction = QAction(QIcon('copy.png'), 'Copy', self)
        copyAction.setShortcut('Ctrl+C')
        copyAction.setStatusTip('Copy')
        copyAction.triggered.connect(self.copy)

        pasteAction = QAction(QIcon('paste.png'), 'Paste', self)
        pasteAction.setShortcut('Ctrl+V')
        pasteAction.setStatusTip('Paste')
        pasteAction.triggered.connect(self.paste)

        cutAction = QAction(QIcon('cut.png'), 'Cut', self)
        cutAction.setShortcut('Ctrl+X')
        cutAction.setStatusTip('Cut')
        cutAction.triggered.connect(self.cut)

        aboutAction = QAction('About', self)
        aboutAction.setStatusTip('About')
        aboutAction.triggered.connect(self.about)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(exitAction)
        fileMenu2 = menubar.addMenu('&Edit')
        fileMenu2.addAction(undoAction)
        fileMenu2.addAction(redoAction)
        fileMenu2.addAction(cutAction)
        fileMenu2.addAction(copyAction)
        fileMenu2.addAction(pasteAction)
        fileMenu3 = menubar.addMenu('&Help')
        fileMenu3.addAction(aboutAction)
        fileMenu4 = menubar.addMenu("&View")
        fileMenu4.addAction(directoryDock.toggleViewAction())
        fileMenu4.addAction(terminalDock.toggleViewAction())

        self.setWindowIcon(QIcon('text.png'))
        self.show()
