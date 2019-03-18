import sys
from PyQt5.QtWidgets import QTextEdit, QAction, QApplication, QMessageBox, QFileDialog
from PyQt5.QtGui import QIcon
import webbrowser


class TextEditor:

    def initUI(self):

        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.textEdit.setText("")

        exit_action = QAction(QIcon('exit.png'), 'Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(self.close)

        new_action = QAction(QIcon('new.png'), 'New', self)
        new_action.setShortcut('Ctrl+N')
        new_action.setStatusTip('New Application')
        new_action.triggered.connect(self.__init__)

        open_action = QAction(QIcon('open.png'), 'Open', self)
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip('Open Application')
        open_action.triggered.connect(self.openo)

        save_action = QAction(QIcon('save.png'), 'Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.setStatusTip('Save Application')
        save_action.triggered.connect(self.save)

        undo_action = QAction(QIcon('undo.png'), 'Undo', self)
        undo_action.setShortcut('Ctrl+Z')
        undo_action.setStatusTip('Undo')
        undo_action.triggered.connect(self.textEdit.undo)

        redo_action = QAction(QIcon('redo.png'), 'Redo', self)
        redo_action.setShortcut('Ctrl+Y')
        redo_action.setStatusTip('Undo')
        redo_action.triggered.connect(self.textEdit.redo)

        copy_action = QAction(QIcon('copy.png'), 'Copy', self)
        copy_action.setShortcut('Ctrl+C')
        copy_action.setStatusTip('Copy')
        copy_action.triggered.connect(self.copy)

        paste_action = QAction(QIcon('paste.png'), 'Paste', self)
        paste_action.setShortcut('Ctrl+V')
        paste_action.setStatusTip('Paste')
        paste_action.triggered.connect(self.paste)

        cut_action = QAction(QIcon('cut.png'), 'Cut', self)
        cut_action.setShortcut('Ctrl+X')
        cut_action.setStatusTip('Cut')
        cut_action.triggered.connect(self.cut)

        about_action = QAction('About', self)
        about_action.setStatusTip('About')
        about_action.triggered.connect(self.about)

        self.statusBar()

        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(exit_action)
        file_menu2 = menubar.addMenu('&Edit')
        file_menu2.addAction(undo_action)
        file_menu2.addAction(redo_action)
        file_menu2.addAction(cut_action)
        file_menu2.addAction(copy_action)
        file_menu2.addAction(paste_action)
        file_menu3 = menubar.addMenu('&Help')
        file_menu3.addAction(about_action)

        self.setWindowIcon(QIcon('text.png'))
        self.show()

    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit without Saving?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.statusBar().showMessage('Quiting...')
            event.accept()

        else:
            event.ignore()
            self.save()
            event.accept()

    def openo(self):
        self.statusBar().showMessage('Open Text Files ')
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        self.statusBar().showMessage('Open File')
        if fname[0]:
            f = open(fname[0], 'r')

            with f:
                data = f.read()
                self.textEdit.setText(data)

    def save(self):
        self.statusBar().showMessage('Add extension to file name')
        fname = QFileDialog.getSaveFileName(self, 'Save File')
        data = self.textEdit.toPlainText()

        try:
            file = open(fname[0], 'w')
            file.write(data)
            file.close()
        except FileNotFoundError:
            pass

    def copy(self):
        cursor = self.textEdit.textCursor()
        textSelected = cursor.selectedText()
        self.copiedtext = textSelected

    def paste(self):
        self.textEdit.append(self.copiedtext)

    def cut(self):
        cursor = self.textEdit.textCursor()
        textSelected = cursor.selectedText()
        self.copiedtext = textSelected
        self.textEdit.cut()

    def about(self):
        url = "https://github.com/kam-masoumi/pycoder"
        self.statusBar().showMessage('Loading url...')
        webbrowser.open(url)
