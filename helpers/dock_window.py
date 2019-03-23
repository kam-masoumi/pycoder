from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import QFileSystemModel, QTreeView, QApplication, \
    QDockWidget, QTextEdit, QWidget, QPushButton, QVBoxLayout, QGridLayout


class DockWindows:

    def directoryDockWindow(self):
        model = QFileSystemModel()
        model.setRootPath('/home/kamran/workspace')
        tree = QTreeView()
        tree.setModel(model)

        tree.setAnimated(True)
        tree.setIndentation(20)
        tree.setSortingEnabled(True)

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

        runButton = QPushButton(QIcon('run.png'), '')
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
