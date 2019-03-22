from PyQt5.QtGui import QFont, QColor, QTextFormat
from PyQt5.QtWidgets import QTextEdit


class TextEditor:

    def createTextEditor(self, directory=None):
        font = QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(16)

        self.textEdit = QTextEdit()

        self.textEdit.setAcceptDrops(False)
        self.textEdit.setFont(font)
        self.textEdit.textChanged.connect(lambda: self.autoSave(self.textEdit, directory))
        self.textEdit.setViewportMargins(50, 0, 0, 0)
        self.textEdit.mouseReleaseEvent = self.highlightCurrentLineByMouse
        self.textEdit.keyReleaseEvent = self.highlightCurrentLineByKey

        return self.textEdit

    def autoSave(self, text_edit=None, directory=None):
        if text_edit is not None and directory is not None:
            text = text_edit.toPlainText()
            with open(f'{directory}', 'w') as f:
                f.write(text)

            with open(f'{directory}', 'r') as f:
                file = f.readlines()
                if len(file) != 0:
                    lines = len(file) if '\n' not in file[-1] else len(file) + 1
                    return lines

    def highlightCurrentLineByKey(self, event):
        extraSelectionsKey = []
        if not self.textEdit.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            lineColor = QColor(52, 73, 94)
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textEdit.textCursor()
            selection.cursor.clearSelection()
            extraSelectionsKey.append(selection)
        self.textEdit.setExtraSelections(extraSelectionsKey)

    def highlightCurrentLineByMouse(self, event):
        extraSelectionsMouse = []
        selection = QTextEdit.ExtraSelection()
        lineColor = QColor(52, 73, 94)
        selection.format.setBackground(lineColor)
        selection.format.setProperty(QTextFormat.FullWidthSelection, True)
        selection.cursor = self.textEdit.textCursor()
        selection.cursor.clearSelection()
        extraSelectionsMouse.append(selection)
        self.textEdit.setExtraSelections(extraSelectionsMouse)
