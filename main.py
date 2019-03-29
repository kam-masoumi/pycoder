import webbrowser

from PyQt5.QtCore import Qt, QFile, QStringListModel
from PyQt5.QtGui import QPixmap, QCursor, QIcon, QTextDocument
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QLabel, QCompleter, QApplication, QInputDialog, \
    QLineEdit

from helpers.menubar import MenuBar
from helpers.search import Find
from helpers.themes import ThemeEdit, codeColorScheme
from helpers.tabs import Tabs
from helpers.dock_window import DockWindows
from models.color import ColorScheme
from models.search import Search


class MainWindow(QMainWindow, MenuBar, ThemeEdit, Tabs, DockWindows):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initTabUI()
        self.initThemeUI()
        self.initMenuUI()
        self.setWindowTitle("PyCoder")
        self.setWindowIcon(QIcon('images/pycoder.png'))

        self.completer = QCompleter(self)
        self.completer.setModel(self.modelFromFile('wordlist.txt'))
        self.completer.setModelSorting(QCompleter.CaseInsensitivelySortedModel)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setWrapAround(False)
        self.completer.popup().setStyleSheet("background-color: rgb(49,49,49);"
                                             "color: silver;"
                                             "font-size: 18px;"
                                             "width: 20px;")
        backGround = QLabel()
        backGround.setAlignment(Qt.AlignCenter)
        backGround.setPixmap(QPixmap("images/pycoder.png"))

        self.setCentralWidget(backGround)

        self.showMaximized()
        self.lastDirectory = []
        self.lastDockDirectory = []
        self.lastGit = []

    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.statusBar().showMessage('Quiting...')
            event.accept()

        else:
            event.ignore()

    def newFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        directory, _ = QFileDialog.getSaveFileName(self,
                                                  "New file",
                                                  "Pyhton file (*.py)", options=options)

        fileName = directory.split('/')[-1]
        if fileName[-2:] == 'py':
            try:
                with open(directory, 'w') as f:
                    f.write('')
                    self.createTab('', fileName, directory)
            except FileNotFoundError:
                pass
        else:
            QMessageBox.warning(self, 'Error',
                                "This is not python file!")

    def openFile(self):
        self.statusBar().showMessage('Open Text Files ')
        fileDirectory = QFileDialog.getOpenFileName(self, 'Open file', '/home', "Python Files (*.py *.h)")
        fileName = fileDirectory[0].split('/')[-1]
        self.statusBar().showMessage(f'{fileDirectory[0]}')
        if fileDirectory[0]:
            with open(fileDirectory[0], 'r') as f:
                data = f.read()
                self.createTab(data, fileName, fileDirectory[0])

    def openProject(self):
        directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        directoryDock = DockWindows.directoryDockWindow(self, directory)
        self.fileMenu3.addAction(directoryDock.toggleViewAction())

    def save(self):
        currentTabWidget = self.tabs.currentWidget()
        self.statusBar().showMessage('Add extension to file name')
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,
                                                  "Save file",
                                                  "Pyhton file (*.py)", options=options)
        if fileName and currentTabWidget is not None:
            try:
                data = currentTabWidget.toPlainText()
                with open(fileName, 'w') as f:
                    f.write(data)
            except FileNotFoundError:
                pass

    def about(self):
        url = "https://github.com/kam-masoumi/pycoder"
        self.statusBar().showMessage('Loading url...')
        webbrowser.open(url)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('text/plain'):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        fileDirectory = event.mimeData().text()[7:-2]
        fileName = fileDirectory.split('/')[-1]
        if fileName[-2:] != 'py':
            return event.ignore()
        f = open(fileDirectory, 'r')
        with f:
            data = f.read()
            self.createTab(data, fileName, fileDirectory)

    def modelFromFile(self, fileName):
        f = QFile(fileName)
        if not f.open(QFile.ReadOnly):
            return QStringListModel(self.completer)

        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

        words = []
        while not f.atEnd():
            line = f.readLine().trimmed()
            if line.length() != 0:
                try:
                    line = str(line, encoding='ascii')
                except TypeError:
                    line = str(line)

                words.append(line)

        QApplication.restoreOverrideCursor()

        return QStringListModel(words, self.completer)

    def changeTheme(self):
        status = ColorScheme().get(id=1)
        status.changeTheme()
        return self.initThemeUI()

    def colorScheme(self):
        dialog = codeColorScheme(self)
        dialog.show()

    def setDefaultTheme(self):
        reply = QMessageBox.question(self, "Warning!!!", 'Are you sure to set default theme?',
                                     QMessageBox.Yes | QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            newTheme = ColorScheme().get(id=1)
            newTheme.setDefault()

    def gitStatus(self):

        try:
            git = self.lastGit[-1]
        except IndexError:
            QMessageBox.warning(self, 'Error',
                                "Does not exist any git repository!")
            return False

        result = git.status()
        QMessageBox.information(self, "Git Status", result)

    def gitDiff(self):
        try:
            git = self.lastGit[-1]
        except IndexError:
            QMessageBox.warning(self, 'Error',
                                "Does not exist any git repository!")
            return False

        result = git.diff()
        QMessageBox.information(self, "Git Diff", result)

    def gitCommit(self):
        try:
            git = self.lastGit[-1]
        except IndexError:
            QMessageBox.warning(self, 'Error',
                                "Does not exist any git repository!")
            return False

        message, ok = QInputDialog.getText(self, "Commit message",
                                              "Message:", QLineEdit.Normal)
        if ok and message != '':
            result = git.commit(message)
            QMessageBox.information(self, "Git Commit", result)

    def gitPush(self):
        try:
            git = self.lastGit[-1]
        except IndexError:
            QMessageBox.warning(self, 'Error',
                                "Does not exist any git repository!")
            return False

        allBranch = git.branchs()
        for branch in allBranch:
            if branch.isidentifier() is False:
                currentBranch = branch

        reply = QMessageBox.question(self, "Git Push",
                                     f'Are you sure want push in {currentBranch}?',
                                     QMessageBox.Yes | QMessageBox.Cancel)

        if reply == QMessageBox.Yes:
            result = git.push(currentBranch)
            QMessageBox.information(self, "Git Push", result)

    def gitPull(self):
        try:
            git = self.lastGit[-1]
        except IndexError:
            QMessageBox.warning(self, 'Error',
                                "Does not exist any git repository!")
            return False

        nameBranch, ok = QInputDialog.getText(self, "Git Pull",
                                              "Branch Name:", QLineEdit.Normal)
        if ok and nameBranch != '':
            result = git.pull(nameBranch)
            QMessageBox.information(self, "Git Pull", result)

    def gitCheckout(self):
        try:
            git = self.lastGit[-1]
        except IndexError:
            QMessageBox.warning(self, 'Error',
                                "Does not exist any git repository!")
            return False

        allBranch = git.branchs()
        for branch in allBranch:
            if branch.isidentifier() is False:
                index = allBranch.index(branch)

        branch, ok = QInputDialog.getItem(self, "Choice your branch",
                                        "Branchs:", allBranch, index, False)
        if ok and branch:
            if branch.isalnum():
                result = git.checkout(branch)
                QMessageBox.information(self, "Git Checkout", result)

    def gitCreateBranch(self):
        try:
            git = self.lastGit[-1]
        except IndexError:
            QMessageBox.warning(self, 'Error',
                                "Does not exist any git repository!")
            return False

        nameBranch, ok = QInputDialog.getText(self, "Create New Branch",
                                        "Branch Name:", QLineEdit.Normal)
        if ok and nameBranch != '':
            result = git.create(nameBranch)
            QMessageBox.information(self, f"Create New Branch {nameBranch} Successfully", result)

    def gitMerge(self):
        pass

    def findAndReplace(self):
        currentTextEditor = self.tabs.currentWidget()

        find = Find(self)
        find.show()

        def handleFind():
            oldSearch = Search().get(id=1)
            caseSensitively = oldSearch.case_sensitively
            wholeWords = oldSearch.whole_words

            f = find.searchText.toPlainText()
            if caseSensitively is True and wholeWords is False:
                flag = QTextDocument.FindBackward and QTextDocument.FindCaseSensitively

            elif caseSensitively is False and wholeWords is False:
                flag = QTextDocument.FindBackward

            elif caseSensitively is False and wholeWords is True:
                flag = QTextDocument.FindBackward and QTextDocument.FindWholeWords

            elif caseSensitively is True and wholeWords is True:
                flag = QTextDocument.FindBackward and QTextDocument.FindCaseSensitively and QTextDocument.FindWholeWords

            try:
                currentTextEditor.find(f, flag)
            except AttributeError:
                QMessageBox.warning(self, 'Error',
                                    "Does not exist any text editor!")

        def handleReplace():
            f = find.searchText.toPlainText()
            r = find.replaceText.toPlainText()

            try:
                text = currentTextEditor.toPlainText()
            except AttributeError:
                QMessageBox.warning(self, 'Error',
                                    "Does not exist any text editor!")
                return False

            newText = text.replace(f, r)

            currentTextEditor.clear()
            currentTextEditor.append(newText)

        find.findButton.clicked.connect(handleFind)
        find.replaceButton.clicked.connect(handleReplace)

