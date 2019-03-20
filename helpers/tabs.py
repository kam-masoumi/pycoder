from linecache import cache

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

    def createTab(self, data, file_name, directory):
        oldFileDirectory = cache.get(file_name)
        allFile = cache.keys()

        if file_name in allFile and oldFileDirectory == directory:
            return False
        elif file_name in allFile and oldFileDirectory != directory:
            file_name += '-another'
        else:
            pass

        tabLayout = QGridLayout()
        newTab = TextEditor.createTextEditor()
        self.highlighter = Highlighter(newTab.document())
        newTab.setText(data)

        tabLayout.addWidget(newTab)

        self.tabs.addTab(newTab, f'{file_name}')
        tabIndex = self.tabs.indexOf(newTab)
        self.tabs.setTabIcon(tabIndex, QIcon('python1.png'))
        self.tabs.tabBarClicked.connect(self.changeStatusBar)
        cache.setdefault(file_name, directory)

        self.setCentralWidget(self.tabs.currentWidget())

    def closeTab(self, index):
        self.tabs.removeTab(index)
        return index

    def changeStatusBar(self, index):
        currentTabWidget = self.tabs.currentWidget()
        self.highlighter = Highlighter(currentTabWidget)
        currentTabName = self.tabs.tabText(index)
        currentDirectory = cache.get(currentTabName)
        self.statusBar().showMessage(currentDirectory)
