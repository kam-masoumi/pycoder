from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont


class Highlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(Highlighter, self).__init__(parent)

        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(QColor(255,119,0))
        keywordFormat.setFontWeight(QFont.Bold)

        keywordPatterns = ["\\bclass\\b", "\\bdef\\b", "\\bfor\\b",
                           "\\bif\\b", "\\bin\\b", "\\bis\\b", "\\bnot\\b",
                           "\\bNone\\b", "\\bTrue\\b", "\\bFalse\\b","\\bas\\b",
                           "\\bfrom\\b", "\\bimport\\b", "\\bwith\\b", "\\breturn\\b",
                           "\\bbreak\\b", "\\belif\\b", "\\belse\\b", "\\bcontinue\\b",
                           "\\byield\\b", "\\bwhile\\b", "\\btry\\b", "\\bexcept\\b",
                           "\\bfinally\\b", "\\braise\\b"]

        self.highlightingRules = [(QRegExp(pattern), keywordFormat)
                                  for pattern in keywordPatterns]

        singleLineCommentFormat = QTextCharFormat()
        singleLineCommentFormat.setForeground(Qt.red)
        self.highlightingRules.append((QRegExp("#[^\"\n]*"), singleLineCommentFormat))

        self.multiLineCommentFormat = QTextCharFormat()
        self.multiLineCommentFormat.setForeground(Qt.red)

        psFormat = QTextCharFormat()
        psFormat.setForeground(QColor(144,0,144))
        self.highlightingRules.append((QRegExp("\\bself\\b"), psFormat))
        self.highlightingRules.append((QRegExp("\\bprint\\b"), psFormat))


        functionFormat = QTextCharFormat()
        functionFormat.setFontItalic(True)
        functionFormat.setFontWeight(QFont.Bold)
        functionFormat.setForeground(Qt.blue)
        self.highlightingRules.append((QRegExp("\\b [A-Za-z0-9_]+(?=\\()"), functionFormat))
        self.highlightingRules.append((QRegExp("[0-9]"), functionFormat))

        self.highlightingRules.append((QRegExp("\\brange\\b"), psFormat))

        self.commentStartExpression = QRegExp("/\\*")
        self.commentEndExpression = QRegExp("\\*/")

        quotationFormat = QTextCharFormat()
        quotationFormat.setForeground(Qt.darkGreen)
        self.highlightingRules.append((QRegExp("\\'.[^']*\\'"), quotationFormat))
        self.highlightingRules.append((QRegExp('\\".[^"]*\\"'), quotationFormat))

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

        startIndex = 0
        if self.previousBlockState() != 1:
            startIndex = self.commentStartExpression.indexIn(text)

        while startIndex >= 0:
            endIndex = self.commentEndExpression.indexIn(text, startIndex)

            if endIndex == -1:
                self.setCurrentBlockState(1)
                commentLength = len(text) - startIndex
            else:
                commentLength = endIndex - startIndex + self.commentEndExpression.matchedLength()

            self.setFormat(startIndex, commentLength,
                    self.multiLineCommentFormat)
            startIndex = self.commentStartExpression.indexIn(text,
                    startIndex + commentLength);