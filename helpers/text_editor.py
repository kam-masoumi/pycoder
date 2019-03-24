from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor, QFont, QColor, QTextFormat
from PyQt5.QtWidgets import QTextEdit, QCompleter


class TextEditor(QTextEdit):

    def __init__(self, parent=None):
        super(TextEditor, self).__init__(parent)

        self._completer = None
        font = QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(16)
        self.setFont(font)
        self.mouseReleaseEvent = self.highlightCurrentLineByMouse
        self.keyReleaseEvent = self.highlightCurrentLineByKey
        self.textChanged.connect(lambda: self.autoSave(parent))

    def setCompleter(self, c):
        if self._completer is not None:
            self._completer.activated.disconnect()

        self._completer = c

        c.setWidget(self)
        c.setCompletionMode(QCompleter.PopupCompletion)
        c.setCaseSensitivity(Qt.CaseInsensitive)
        c.activated.connect(self.insertCompletion)

    def completer(self):
        return self._completer

    def insertCompletion(self, completion):
        if self._completer.widget() is not self:
            return

        tc = self.textCursor()
        extra = len(completion) - len(self._completer.completionPrefix())
        tc.movePosition(QTextCursor.Left)
        tc.movePosition(QTextCursor.EndOfWord)
        tc.insertText(completion[-extra:])
        self.setTextCursor(tc)

    def textUnderCursor(self):
        tc = self.textCursor()
        tc.select(QTextCursor.WordUnderCursor)

        return tc.selectedText()

    def focusInEvent(self, e):
        if self._completer is not None:
            self._completer.setWidget(self)

        super(TextEditor, self).focusInEvent(e)

    def keyPressEvent(self, e):
        if self._completer is not None and self._completer.popup().isVisible():
            # The following keys are forwarded by the completer to the widget.
            if e.key() in (Qt.Key_Enter, Qt.Key_Return, Qt.Key_Escape, Qt.Key_Tab, Qt.Key_Backtab):
                e.ignore()
                # Let the completer do default behavior.
                return

        isShortcut = ((e.modifiers() & Qt.ControlModifier) != 0 and e.key() == Qt.Key_F10)
        if self._completer is None or not isShortcut:
            # Do not process the shortcut when we have a completer.
            super(TextEditor, self).keyPressEvent(e)

        ctrlOrShift = e.modifiers() & (Qt.ControlModifier | Qt.ShiftModifier)
        if self._completer is None or (ctrlOrShift and len(e.text()) == 0):
            return

        eow = "~!@#$%^&*()_+{}|:\"<>?,./;'[]\\-="
        hasModifier = (e.modifiers() != Qt.NoModifier) and not ctrlOrShift
        completionPrefix = self.textUnderCursor()

        if not isShortcut and (
                hasModifier or len(e.text()) == 0 or len(completionPrefix) < 1 or e.text()[-1] in eow):
            self._completer.popup().hide()
            return

        if completionPrefix != self._completer.completionPrefix():
            self._completer.setCompletionPrefix(completionPrefix)
            self._completer.popup().setCurrentIndex(
                self._completer.completionModel().index(0, 0))

        cr = self.cursorRect()
        cr.setWidth(self._completer.popup().sizeHintForColumn(
            0) + self._completer.popup().verticalScrollBar().sizeHint().width())
        self._completer.complete(cr)

    def highlightCurrentLineByKey(self, event):
        extraSelectionsKey = []
        selection = QTextEdit.ExtraSelection()
        lineColor = QColor(174, 182, 191, 60)
        selection.format.setBackground(lineColor)
        selection.format.setProperty(QTextFormat.FullWidthSelection, True)
        selection.cursor = self.textCursor()
        selection.cursor.clearSelection()
        extraSelectionsKey.append(selection)
        self.setExtraSelections(extraSelectionsKey)

    def highlightCurrentLineByMouse(self, event):
        extraSelectionsMouse = []
        selection = QTextEdit.ExtraSelection()
        lineColor = QColor(174, 182, 191, 60)
        selection.format.setBackground(lineColor)
        selection.format.setProperty(QTextFormat.FullWidthSelection, True)
        selection.cursor = self.textCursor()
        selection.cursor.clearSelection()
        extraSelectionsMouse.append(selection)
        self.setExtraSelections(extraSelectionsMouse)

    def autoSave(self, directory=None):
        if directory is not None:
            text = self.toPlainText()
            with open(f'{directory}', 'w') as f:
                f.write(text)

            with open(f'{directory}', 'r') as f:
                file = f.readlines()
                if len(file) != 0:
                    lines = len(file) if '\n' not in file[-1] else len(file) + 1
                    return lines
