from PyQt5.QtWidgets import QDialog, QLabel, QTextEdit, QPushButton, QCheckBox

from models import Search


class Find(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)

        self.initUI()

    def initUI(self):
        self.oldSearch = Search().get(id=1)

        self.searchLabel = QLabel("Search for: ", self)
        self.searchLabel.setStyleSheet("font-size: 15px; ")
        self.searchLabel.move(10, 10)

        self.searchText = QTextEdit(self)
        self.searchText.move(10, 40)
        self.searchText.resize(250, 25)

        self.findButton = QPushButton("Find", self)
        self.findButton.move(270, 40)

        self.replaceLabel = QLabel("Replace all by: ", self)
        self.replaceLabel.setStyleSheet("font-size: 15px; ")
        self.replaceLabel.move(10, 80)

        self.replaceText = QTextEdit(self)
        self.replaceText.move(10, 110)
        self.replaceText.resize(250, 25)

        self.replaceButton = QPushButton("Replace", self)
        self.replaceButton.move(270, 110)

        self.caseCheck = QCheckBox("Case sensitive", self, checked=self.oldSearch.case_sensitively)
        self.caseCheck.move(10, 160)
        self.caseCheck.stateChanged.connect(self.caseSensitively)

        self.wordCheck = QCheckBox("Whole words only", self, checked=self.oldSearch.whole_words)
        self.wordCheck.move(10, 190)
        self.wordCheck.stateChanged.connect(self.wholeWords)

        self.close = QPushButton("Close", self)
        self.close.move(270, 220)
        self.close.clicked.connect(self.closeFind)

        self.setGeometry(300, 300, 360, 250)

    def caseSensitively(self, state):
        self.oldSearch.changeStateCaseSensitively()

    def wholeWords(self, state):
        self.oldSearch.changeStateWholeWord()

    def closeFind(self):
        self.hide()
