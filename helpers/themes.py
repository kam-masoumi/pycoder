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
