import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton
from PyQt6 import QtCore
from src.ui.sidebar_ui import Ui_MainWindow
from src.ui.exams_page import ExamsPage
from src.ui.chat_page import ChatPage

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Maximizar la ventana al inicio
        self.showMaximized()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Inicializar páginas
        self.exams_page = ExamsPage()
        self.chat_page = ChatPage()

        # Agregar paginas a sus respectivos layouts
        self.ui.page_3_layout.addWidget(self.exams_page)
        self.ui.page_4_layout.addWidget(self.chat_page)

        # Configuracion inicial
        self.ui.icon_only_widget.hide()
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.home_btn_2.setChecked(True)

        # Conectar navegacion del sidebar
        self.setup_navigation()

        # Conectar boton de búsqueda
        self.ui.search_btn.clicked.connect(self.on_search_btn_clicked)
        self.ui.stackedWidget.currentChanged.connect(self.on_stackWidget_currentChanged)

    def setup_navigation(self):
        """Configura las conexiones de navegación"""

        # Navegacion del sidebar principal
        navigation_connections = [
            (self.ui.home_btn_2, 0),
            (self.ui.dashboard_btn_2, 1),
            (self.ui.questions_btn_2, 2),
            (self.ui.chat_btn_2, 3),
            (self.ui.credits_btn_2, 5)
        ]

        # Navegacion del menu reducido
        compact_navigation_connections = [
            (self.ui.home_btn_1, 0),
            (self.ui.dashboard_btn_1, 1),
            (self.ui.questions_btn_1, 2),
            (self.ui.chat_btn_1, 3),
            (self.ui.credits_btn_1, 5)
        ]

        # Configurar todas las conexiones
        for button, index in navigation_connections + compact_navigation_connections:
            button.clicked.connect(lambda checked, idx=index: self.ui.stackedWidget.setCurrentIndex(idx))

    def on_search_btn_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(5)
        search_text = self.ui.search_input.text().strip()
        if search_text:
            self.ui.label_9.setText(search_text)

    def on_stackWidget_currentChanged(self, index):
        btn_list = self.ui.icon_only_widget.findChildren(QPushButton) \
                   + self.ui.full_menu_widget.findChildren(QPushButton)
        for btn in btn_list:
            if index in [5, 6]:
                btn.setAutoExclusive(False)
                btn.setCheckable(False)
            else:
                btn.setAutoExclusive(True)


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()