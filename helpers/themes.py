from PyQt5.QtGui import QFont, QColor

from PyQt5.QtWidgets import QColorDialog, QMainWindow, QTextEdit

from helpers.highlighter import Highlighter
from models.color import ColorScheme


class ThemeEdit:

    def initThemeUI(self):
        status = ColorScheme().get(id=1)
        if status.dark_theme is True:
            self.setStyleSheet("""
                                 QWidget {
                                     background-color: rgb(49,49,49);
                                     color: rgb(255,255,255);
                                 }
    
                                 QTextEdit {
                                     background-color: rgb(49,49,49);
                                     color: rgb(255,255,255);
                                     border: 0px;
                                 }
    
                                 QMainWindow {
                                     background-color: rgb(49,49,49);
                                     color: rgb(255,255,255);
                                     border: 1px solid ;
                                 }
    
                                 QMenuBar {
                                     background-color: rgb(49,49,49);
                                     color: rgb(255,255,255);
                                     border: 1px solid ;
                                 }
    
                                 QMenuBar::item {
                                     background-color: rgb(49,49,49);
                                     color: rgb(255,255,255);
                                 }
    
                                 QMenuBar::item::selected {
                                     background-color: rgb(30,30,200);
                                 }
    
                                 QMenu {
                                     background-color: rgb(49,49,49);
                                     color: rgb(255,255,255);
                                     border: 1px solid ;
                                 }
    
                                 QMenu::item::selected {
                                     background-color: rgb(30,30,200);
    
                                 }
                                 
                                 QComboBox {
                                      font-size: 12px;
                                      padding: 3px;
                                      }
                                      
                                 QTabWidget {
                                      font-size: 16px;
                                      color: red;
                                      }
                                      
                                 QTabBar::tab {
                                       background-color: rgb(49,49,49);
                                       color: white;
                                 }
                                 
                                 QTabBar::tab:selected {
                                       background-color: white;
                                       color: rgb(49,49,49);
                                 }
                                 
                                 QDockWidget::title {
                                 text-align: left; /* align the text to the left */
                                 background:  #515a5a;
                                 padding-left: 5px;
                                 }
                                 
                                 QDockWidget::close-button, QDockWidget::float-button {
                                 background: white;
                                 padding: 0px;
                                 icon-size: 18px; /* maximum icon size */
                                 }
                                 
                                 QDockWidget::close-button:pressed, QDockWidget::float-button:pressed {
                                 padding: 1px -1px -1px 1px;
                                 }  
                                          
                                 QTreeView {
                                 show-decoration-selected: 1;
                                 }                                        
                            """)
        else:
            self.setStyleSheet("""
                                 QTabBar::tab {
                                       background-color: white;
                                       color: rgb(49,49,49);
                                 }
                                 
                                 QTabBar::tab:selected {
                                       background-color: rgb(49,49,49);
                                       color: white;
                                 }
                                 
                                 QTextEdit {
                                     background-color: #FFFFFF;
                                     color: #000000;
                                     border: 0px;
                                 }

                                 QMainWindow {
                                     background-color: #FFFFFF;
                                     color: rgb(255,255,255);
                                     border: 1px solid ;
                                 }
                                                                                  
                                        """)


class codeColorScheme(QMainWindow):
    def __init__(self, parent=None):
        super(codeColorScheme, self).__init__(parent)

        self.resize(500, 350)
        self.exampleText = QTextEdit()
        self.exampleText.mouseReleaseEvent = self.changeColor
        self.exampleText.setReadOnly(True)
        font = QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(12)
        self.exampleText.setFont(font)
        self.exampleText.setText('''
        # comment
        @decorator
        class Foo:
            def __init__(parent=None):
                self.parent = parent

            def test(self, value):
                if value == "pycoder":
                    return value

            def test_2(self):
                for i in range(10):
                    print(i)
            x = len('abc')
            print()''')
        self.highlighter = Highlighter(self.exampleText)
        self.setCentralWidget(self.exampleText)

    def changeColor(self, even):
        oldTheme = ColorScheme().get(id=1)
        selectedword = self.exampleText.textCursor().selectedText()

        if selectedword in ['class', 'def', 'if', 'return', 'for', 'None']:
            color = QColorDialog.getColor(QColor(oldTheme.keywords))
            if color.isValid():
                oldTheme.keywords = color.name()
                oldTheme.save()

        elif selectedword in ['print', 'len', 'range']:
            color = QColorDialog.getColor(QColor(oldTheme.builtin))
            if color.isValid():
                oldTheme.builtin = color.name()
                oldTheme.save()

        elif selectedword in ['comment']:
            color = QColorDialog.getColor(QColor(oldTheme.comment))
            if color.isValid():
                oldTheme.comment = color.name()
                oldTheme.save()

        elif selectedword in ['abc', 'pycoder']:
            color = QColorDialog.getColor(QColor(oldTheme.quotation))
            if color.isValid():
                oldTheme.quotation = color.name()
                oldTheme.save()

        elif selectedword in ['decorator']:
            color = QColorDialog.getColor(QColor(oldTheme.decorator))
            if color.isValid():
                oldTheme.decorator = color.name()
                oldTheme.save()

        elif selectedword in ['Foo', '__init__', 'test', 'test_2']:
            color = QColorDialog.getColor(QColor(oldTheme.function))
            if color.isValid():
                oldTheme.function = color.name()
                oldTheme.save()

        self.highlighter = Highlighter(self.exampleText)
