class ThemeEdit:

    def initThemeUI(self):
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
                        """)
