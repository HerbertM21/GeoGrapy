import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton
from PyQt6 import QtCore
from src.ui.sidebar_ui import Ui_MainWindow
from src.ui.exams_page import ExamsPage
from src.ui.chat_page import ChatPage
from src.services.level_system import ImprovedLevelSystem, JsonProgressPersistence
from pathlib import Path
from src.ui.exams_page import DifficultySelector
from datetime import datetime


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.showMaximized()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Configuración inicial
        self.ui.icon_only_widget.hide()

        # Inicializar sistema de niveles y persistencia
        save_dir = Path.home() / '.geograpy' / 'progress'
        self.progress_persistence = JsonProgressPersistence(save_dir)
        self.level_system = None  # Se inicializará cuando se elija la dificultad

        # Inicializar páginas
        self.exams_page = None  # Se inicializará cuando se visite por primera vez
        self.chat_page = ChatPage()

        # Agregar chat page a su layout
        self.ui.page_4_layout.addWidget(self.chat_page)

        # Configurar navegación con manejo especial para la página de exámenes
        self.setup_navigation()

        # Conectar el cambio de página
        self.ui.stackedWidget.currentChanged.connect(self.on_stackWidget_currentChanged)

        # Marcar el botón de inicio
        self.ui.home_btn_2.setChecked(True)
        self.ui.stackedWidget.setCurrentIndex(0)

    def setup_navigation(self):
        """Configura las conexiones de navegación"""
        for i, (menu_btn, icon_btn) in enumerate(zip(self.ui.menu_buttons, self.ui.icon_buttons)):
            page_index = i
            if page_index == 2:  # Índice de la página de exámenes
                menu_btn.clicked.connect(lambda checked, idx=page_index: self.handle_exams_page())
                icon_btn.clicked.connect(lambda checked, idx=page_index: self.handle_exams_page())
            else:
                menu_btn.clicked.connect(lambda checked, idx=page_index: self.ui.stackedWidget.setCurrentIndex(idx))
                icon_btn.clicked.connect(lambda checked, idx=page_index: self.ui.stackedWidget.setCurrentIndex(idx))

    def handle_exams_page(self):
        """Maneja la navegación a la página de exámenes"""
        if self.exams_page is None:
            # Primera visita a la página de exámenes
            difficulty = self.show_difficulty_selector()
            if difficulty:
                self.level_system = ImprovedLevelSystem(difficulty=difficulty)
                self.exams_page = ExamsPage(
                    level_system=self.level_system,
                    progress_persistence=self.progress_persistence
                )
                self.ui.page_3_layout.addWidget(self.exams_page)
            else:
                # Si el usuario cancela la selección de dificultad, volver a la página anterior
                return

        self.ui.stackedWidget.setCurrentIndex(2)

    def show_difficulty_selector(self) -> str:
        """Muestra el selector de dificultad al entrar por primera vez"""
        current_progress = self.progress_persistence.load_progress('current_user')

        # Si ya hay una dificultad guardada, usarla
        if current_progress and 'difficulty' in current_progress:
            return current_progress['difficulty']

        # Mostrar selector de dificultad
        selector = DifficultySelector(self)
        if selector.exec():
            difficulty = selector.get_selected_difficulty()
            # Guardar la preferencia
            self.progress_persistence.save_progress('current_user', {
                'difficulty': difficulty,
                'total_xp': 0,
                'level': 1,
                'last_update': str(datetime.now())
            })
            return difficulty

        return None  # Si el usuario cancela la selección

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