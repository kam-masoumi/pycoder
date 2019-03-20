from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont


class Highlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(Highlighter, self).__init__(parent)

        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(QColor(215, 58, 73))
        keywordFormat.setFontWeight(QFont.Bold)

        keywordPatterns = ["\\bclass\\b", "\\bdef\\b", "\\bfor\\b",
                           "\\bif\\b", "\\bin\\b", "\\bis\\b", "\\bnot\\b",
                           "\\bNone\\b", "\\bTrue\\b", "\\bFalse\\b","\\bas\\b",
                           "\\bfrom\\b", "\\bimport\\b", "\\bwith\\b", "\\breturn\\b",
                           "\\bbreak\\b", "\\belif\\b", "\\belse\\b", "\\bcontinue\\b",
                           "\\byield\\b", "\\bwhile\\b", "\\btry\\b", "\\bexcept\\b",
                           "\\bfinally\\b", "\\braise\\b", "\\bassert\\b", "\\bpass\\b"]

        self.highlightingRules = [(QRegExp(pattern), keywordFormat)
                                  for pattern in keywordPatterns]

        functionFormat = QTextCharFormat()
        functionFormat.setFontWeight(QFont.Bold)
        functionFormat.setForeground(Qt.white)
        self.highlightingRules.append((QRegExp("\\b [A-Za-z0-9_]+(?=\\()"), functionFormat))
        self.highlightingRules.append((QRegExp("[0-9]"), functionFormat))

        builtinFormat = QTextCharFormat()
        builtinFormat.setForeground(QColor(136, 136, 198))
        builtinFunctionPatterns = ["\\babs\\b", "\\ball\\b", "\\bany\\b", "\\bascii\\b",
                                    "\\bbin\\b", "\\bbool\\b", "\\bbreakpoint\\b", "\\bbytearray\\b",
                                    "\\bbytes\\b", "\\bcallable\\b", "\\bchr\\b", "\\bcompile\\b",
                                    "\\bcomplex\\b", "\\bdelattr\\b", "\\bdict\\b", "\\bdir\\b",
                                    "\\bdivmod\\b", "\\benumerate\\b", "\\beval\\b", "\\bexec\\b",
                                    "\\bfilter\\b", "\\bfloat\\b", "\\bformat\\b", "\\bfrozenset\\b",
                                    "\\bgetattr\\b", "\\bglobals\\b", "\\bhasattr\\b", "\\bhash\\b",
                                    "\\bhelp\\b", "\\bhex\\b", "\\bid\\b", "\\binput\\b", "\\bint\\b",
                                    "\\bisinstance\\b", "\\bissubclass\\b", "\\biter\\b", "\\blen\\b",
                                    "\\blist\\b", "\\blocals\\b", "\\bmap\\b", "\\bmax\\b", "\\bmax\\b",
                                    "\\bmemoryview\\b", "\\bmin\\b", "\\bnext\\b", "\\bobject\\b", "\\boct\\b",
                                    "\\bopen\\b", "\\bord\\b", "\\bpow\\b", "\\bprint\\b", "\\bproperty\\b",
                                    "\\brange\\b", "\\brepr\\b", "\\breversed\\b", "\\bround\\b", "\\bset\\b",
                                    "\\bsetattr\\b", "\\bslice\\b", "\\bsorted\\b", "\\bstr\\b", "\\bsum\\b",
                                    "\\bsuper\\b", "\\btuple\\b", "\\btype\\b", "\\bvars\\b", "\\bzip\\b",
                                    "\\b__import__\\b"]

        for pattern in builtinFunctionPatterns:
            self.highlightingRules.append((QRegExp(pattern), builtinFormat))

        singleLineCommentFormat = QTextCharFormat()
        singleLineCommentFormat.setForeground(QColor(128, 128, 128))
        self.highlightingRules.append((QRegExp("#[^\"\n]*"), singleLineCommentFormat))

        self.multiLineCommentFormat = QTextCharFormat()
        self.multiLineCommentFormat.setForeground(Qt.red)

        psFormat = QTextCharFormat()
        psFormat.setForeground(QColor(148, 85, 141))
        self.highlightingRules.append((QRegExp("\\bself\\b"), psFormat))

        quotationFormat = QTextCharFormat()
        quotationFormat.setForeground(QColor(98, 151, 85))
        self.highlightingRules.append((QRegExp("'''.*[.*]*'''"), quotationFormat))
        self.highlightingRules.append((QRegExp('".*[.*]*"'), quotationFormat))
        self.highlightingRules.append((QRegExp("'.*[^'.*]*'"), quotationFormat))
        self.highlightingRules.append((QRegExp("[rf]'\{"), quotationFormat))

        decoratorFormat = QTextCharFormat()
        decoratorFormat.setFontWeight(QFont.Bold)
        decoratorFormat.setForeground(QColor(227, 98, 9))
        self.highlightingRules.append((QRegExp("@[\w()]*"), decoratorFormat))

        self.commentStartExpression = QRegExp("/\\*")
        self.commentEndExpression = QRegExp("\\*/")

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
