from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLineEdit,
                            QPushButton, QLabel, QFrame, QGraphicsBlurEffect)
from PyQt6.QtGui import QFont, QShortcut,QFontDatabase, QPixmap, QColor
from PyQt6.QtCore import Qt, QSize
from pathlib import Path
import json
from src.utils.constants import ICON_PATH, FONT_PATH, IMAGE_PATH


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GeoGrapy - Login")

        # Size ventana
        screen = self.screen().availableGeometry()
        self.setFixedSize(1080, 600)
        self.move((screen.width() - self.width()) // 2,
                  (screen.height() - self.height()) // 2)

        font_path = FONT_PATH / "MADE TOMMY Bold_PERSONAL USE.otf"
        font_id = QFontDatabase.addApplicationFont(str(font_path))
        if font_id != -1:
            self.tommy_font = QFontDatabase.applicationFontFamilies(font_id)[0]
        else:
            self.tommy_font = "Arial"

        self.setup_ui()
        self.setup_styles()

    def setup_ui(self):
        # Widget central con fondo
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Contenedor para el fondo
        background_container = QWidget(central_widget)
        background_container.setFixedSize(self.size())

        # Fondo con imagen
        background = QLabel(background_container)
        background_pixmap = QPixmap(str(IMAGE_PATH / 'login.png'))
        background_pixmap = background_pixmap.scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
        background.setPixmap(background_pixmap)
        background.setFixedSize(self.size())

        # Aplicar blur
        blur_effect = QGraphicsBlurEffect()
        blur_effect.setBlurRadius(10) # Blur para el fondo
        background.setGraphicsEffect(blur_effect)

        # Panel de login
        login_panel = QFrame(central_widget)
        login_panel.setFixedSize(300, 400)
        login_panel.move((self.width() - login_panel.width()) // 2,
                        (self.height() - login_panel.height()) // 2)

        login_layout = QVBoxLayout(login_panel)
        login_layout.setSpacing(20)
        login_layout.setContentsMargins(30, 30, 30, 30)

        # Logo
        logo_label = QLabel()
        logo_pixmap = QPixmap(str(ICON_PATH / "logo2_preview.png"))
        logo_pixmap = logo_pixmap.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio)
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setStyleSheet("background-color: rgba(255, 255, 255, 0);")

        # Título
        title_label = QLabel("GeoGrapy")
        title_label.setFont(QFont(self.tommy_font, 24))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("background-color: rgba(255, 255, 255, 0);")

        # Campo de usuario
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Ingresa tu nombre de usuario")
        self.username_input.setMinimumHeight(40)

        # Botón de inicio
        self.login_button = QPushButton("Comenzar")
        self.login_button.setMinimumHeight(40)
        self.login_button.clicked.connect(self.handle_login)
        shortcut = QShortcut(Qt.Key.Key_Return, self)
        shortcut.activated.connect(self.handle_login)


        # Añadir widgets al layout
        login_layout.addWidget(logo_label)
        login_layout.addWidget(title_label)
        login_layout.addStretch()
        login_layout.addWidget(self.username_input)
        login_layout.addWidget(self.login_button)
        login_layout.addStretch()

    def setup_styles(self):
        # Estilo para el panel de login
        self.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.95);
                border-radius: 20px;
            }

            QLineEdit {
                border: 2px solid #3498db;
                border-radius: 20px;
                padding: 5px 15px;
                background: white;
                selection-background-color: #3498db;
                font-size: 14px;
                color: #2c3e50;  /* Color del texto */
            }

            QLineEdit:focus {
                border-color: #2980b9;
            }

            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 14px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #2980b9;
            }

            QLabel {
                color: #2c3e50;
            }
        """)

    def handle_login(self):
        username = self.username_input.text().strip()
        if not username:
            return

        # Crear directorio para datos de usuario si no existe
        save_dir = Path.home() / '.geograpy' / 'progress'
        save_dir.mkdir(parents=True, exist_ok=True)

        # Guardar datos del usuario
        user_data_file = save_dir / 'user_data.json'
        user_data = {
            'username': username,
            'settings': {
                'theme': 'default',
                'notifications': True
            }
        }

        try:
            with open(user_data_file, 'w', encoding='utf-8') as f:
                json.dump(user_data, f, indent=4)

            # Cerrar la ventana de login y abrir la ventana principal
            self.close()
            from src.main import MainWindow
            self.main_window = MainWindow()
            self.main_window.show()

        except Exception as e:
            print(f"Error al guardar los datos del usuario: {e}")