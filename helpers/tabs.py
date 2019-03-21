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
        self.setAcceptDrops(True)

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
        newTab = TextEditor().createTextEditor()
        newTab.setText(data)

        tabLayout.addWidget(newTab)
        self.tabs.addTab(newTab, f'{file_name}')
        tabIndex = self.tabs.indexOf(newTab)
        self.tabs.setTabIcon(tabIndex, QIcon('python1.png'))
        self.tabs.tabBarClicked.connect(self.changeStatusBar)
        cache.setdefault(file_name, directory)

        self.tabs.setCurrentWidget(newTab)
        self.changeStatusBar(-1)
        self.setCentralWidget(self.tabs)
        self.statusBar().showMessage(directory)

        self.list.clear()
        self.list.append(directory)

    def closeTab(self, index):
        currentTabName = self.tabs.tabText(index)
        try:
            cache.pop(currentTabName)
            self.list.clear()
        except KeyError:
            pass
        self.tabs.removeTab(index)
        newCurrentTabName = self.tabs.tabText(0)
        currentDirectory = cache.get(newCurrentTabName)
        self.statusBar().showMessage(currentDirectory)
        return index

    def changeStatusBar(self, index):
        currentTabWidget = self.tabs.currentWidget()
        self.highlighter = Highlighter(currentTabWidget)
        currentTabName = self.tabs.tabText(index)
        currentDirectory = cache.get(currentTabName)
        self.list.clear()
        self.list.append(currentDirectory)
        self.statusBar().showMessage(currentDirectory)
