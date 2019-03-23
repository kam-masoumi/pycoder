from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QFileSystemModel, QTreeView, QApplication, QDockWidget, QTextEdit


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
        self.terminalShow = QTextEdit()
        self.terminalShow.setReadOnly(True)

        dock = QDockWidget("Terminal", self)
        dock.setMinimumHeight(150)
        dock.setAllowedAreas(Qt.BottomDockWidgetArea)
        self.addDockWidget(Qt.BottomDockWidgetArea, dock)
        dock.setWidget(self.terminalShow)
        dock.hide()
        return dock
