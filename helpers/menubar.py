import subprocess

from PyQt5.QtWidgets import QAction, QMenu, QMessageBox
from PyQt5.QtGui import QIcon, QCursor, QColor, QFont

from helpers.dock_window import DockWindows
from models.color import ColorScheme


class MenuBar:

    def initMenuUI(self):
        self.terminalDock = DockWindows.terminalDockWindow(self)

        exitAction = QAction(QIcon('images/exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        newAction = QAction(QIcon('images/pythonfile.png'), 'New', self)
        newAction.setShortcut('Ctrl+N')
        newAction.setStatusTip('New File')
        newAction.triggered.connect(self.newFile)

        openAction = QAction(QIcon('images/open.png'), 'Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open File')
        openAction.triggered.connect(self.openFile)

        openProjectAction = QAction(QIcon('images/open.png'), 'Open project', self)
        openProjectAction.setShortcut('Ctrl+Shift+O')
        openProjectAction.setStatusTip('Open Project')
        openProjectAction.triggered.connect(self.openProject)

        saveAction = QAction(QIcon('images/save.png'), 'Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.setStatusTip('Save File')
        saveAction.triggered.connect(self.save)

        colorAction = QAction('Color Scheme', self)
        colorAction.setShortcut('Ctrl+Shift+C')
        colorAction.setStatusTip('Color Scheme')
        colorAction.triggered.connect(self.colorScheme)

        status = ColorScheme().get(id=1).dark_theme
        themeAction = QAction('Dark Theme', self, checkable=True, checked=status)
        themeAction.setShortcut('Ctrl+Shift+C')
        themeAction.setStatusTip('Color Scheme')
        themeAction.triggered.connect(lambda: self.changeTheme())

        defaultthemeAction = QAction('Default Theme', self)
        defaultthemeAction.setShortcut('Ctrl+Shift+R')
        defaultthemeAction.setStatusTip('Default Theme')
        defaultthemeAction.triggered.connect(lambda: self.setDefaultTheme())

        aboutAction = QAction('About', self)
        aboutAction.setStatusTip('About')
        aboutAction.triggered.connect(self.about)

        runAction = QAction(QIcon('images/run.png'), 'Run', self)
        runAction.setStatusTip('Run selected configuration')
        runAction.setShortcut('Ctrl+Shift+R')
        runAction.triggered.connect(lambda: self.runCommand())

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(openProjectAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(exitAction)

        self.fileMenu3 = menubar.addMenu("&View")
        self.fileMenu3.addAction(self.terminalDock.toggleViewAction())
        self.fileMenu3.addAction(colorAction)
        self.fileMenu3.addAction(themeAction)
        self.fileMenu3.addAction(defaultthemeAction)
        fileMenu4 = menubar.addMenu('&Tools')
        fileMenu4.addAction(runAction)
        fileMenu5 = menubar.addMenu('&Help')
        fileMenu5.addAction(aboutAction)

    def contextMenuEvent(self, event):
        self.menu = QMenu(self)
        runAction = QAction(QIcon('images/run.png'), 'Run', self)
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

        status = ColorScheme().get(id=1)
        redColor = QColor(220, 20, 60)

        resultColor = QColor(0, 0, 0)
        if status.dark_theme is True:
            resultColor = QColor(255, 255, 255)

        font = QFont()
        font.setFamily('Courier')
        font.setBold(True)
        font.setPointSize(12.5)
        self.terminalShow.setFont(font)

        if len(out.decode()) >= 1:
            self.terminalShow.setTextColor(resultColor)
            self.terminalShow.append(out.decode())
        self.terminalShow.setTextColor(redColor)
        self.terminalShow.append(err.decode())

        self.terminalShow.setTextColor(resultColor)
        self.terminalShow.append('Process finished with exit code 0')
