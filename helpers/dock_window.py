from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import QFileSystemModel, QTreeView, QApplication, \
    QDockWidget, QTextEdit, QWidget, QPushButton, QGridLayout, QFileIconProvider


class IconProvider(QFileIconProvider):
    def icon(self, fileInfo):
        if fileInfo.isDir():
            return QIcon("images/open.png")
        elif fileInfo.fileName()[-2:] == 'py':
            return QIcon('images/pythonfile.png')
        return QFileIconProvider.icon(self, fileInfo)


class DockWindows:

    def directoryDockWindow(self, directory=None):
        self.model = QFileSystemModel()
        self.model.setReadOnly(False)
        self.model.setRootPath('/home')
        self.model.setIconProvider(IconProvider())

        tree = QTreeView()
        tree.setModel(self.model)
        tree.setRootIndex(self.model.index(f'{directory}'))
        tree.doubleClicked.connect(self.test)

        tree.setAnimated(True)
        tree.setIndentation(20)

        availableSize = QApplication.desktop().availableGeometry(tree).size()
        tree.resize(availableSize / 2)
        tree.setColumnWidth(0, tree.width() / 3)

        dock = QDockWidget("Project", self)
        dock.setMinimumWidth(200)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea)
        dock.setWidget(tree)

        self.addDockWidget(Qt.LeftDockWidgetArea, dock)
        return dock

    def textEditorDockWindows(self):
        pass

    def terminalDockWindow(self):
        dockLayout = QGridLayout()

        self.terminalShow = QTextEdit()
        self.terminalShow.setReadOnly(True)

        runButton = QPushButton(QIcon('images/run.png'), '')
        runButton.clicked.connect(self.runCommand)

        dock = QDockWidget("Terminal", self)
        self.addDockWidget(Qt.BottomDockWidgetArea, dock)

        dockedWidget = QWidget(self)
        dock.setWidget(dockedWidget)
        dockedWidget.setLayout(dockLayout)
        dockedWidget.layout().addWidget(runButton, 0, 0, Qt.AlignTop)
        dockedWidget.layout().addWidget(self.terminalShow, 0, 1)

        dock.setAllowedAreas(Qt.BottomDockWidgetArea)
        dock.hide()
        return dock

    def test(self, signal):
        directory = self.model.filePath(signal)
        pythonFile = directory.split('/')[-1]
        try:
            if pythonFile[-2:] == 'py':
                with open(directory, 'r') as f:
                    self.createTab(f.read(), pythonFile, directory)
        except IndexError:
            pass
