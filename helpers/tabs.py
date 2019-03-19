from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTabWidget, QGridLayout

from helpers.highlighter import Highlighter
from helpers.text_editor import TextEditor


class Tabs:

    def initTabUI(self):
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.setStyleSheet("border: solid;")
        self.tabs.tabCloseRequested.connect(self.closeTab)

    def createTab(self, data, file_name):
        tabLayout = QGridLayout()
        newTab = TextEditor().createTextEditor()
        self.highlighter = Highlighter(newTab.document())
        newTab.setText(data)

        tabLayout.addWidget(newTab)

        self.tabs.addTab(newTab, f'{file_name}')
        tabIndex = self.tabs.indexOf(newTab)
        self.tabs.setTabIcon(tabIndex, QIcon('python1.png'))

        self.setCentralWidget(self.tabs)

    def closeTab(self, index):
        self.tabs.removeTab(index)
        return index
