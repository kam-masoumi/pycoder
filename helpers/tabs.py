from linecache import cache

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTabWidget

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
        self.tabs.tabBarClicked.connect(self.changeStatusBar)

    def createTab(self, data, file_name, directory):
        oldFileDirectory = cache.get(file_name)
        allFile = cache.keys()
        if file_name in allFile and oldFileDirectory == directory:
            return False
        elif file_name in allFile and oldFileDirectory != directory:
            file_name += '-another'
        else:
            pass

        newTextEditor = TextEditor().createTextEditor(directory)
        newTextEditor.setText(data)

        self.tabs.addTab(newTextEditor, f'{file_name}')

        tabIndex = self.tabs.indexOf(newTextEditor)
        self.tabs.setTabIcon(tabIndex, QIcon('python1.png'))
        cache.setdefault(file_name, directory)

        self.tabs.setCurrentWidget(newTextEditor)
        self.changeStatusBar(-1)
        self.setCentralWidget(self.tabs)
        self.statusBar().showMessage(directory)

        self.lastDirectory.clear()
        self.lastDirectory.append(directory)

    def closeTab(self, index):
        currentTabName = self.tabs.tabText(index)
        try:
            cache.pop(currentTabName)
            self.lastDirectory.clear()
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
        self.lastDirectory.clear()
        self.lastDirectory.append(currentDirectory)
        self.statusBar().showMessage(currentDirectory)
