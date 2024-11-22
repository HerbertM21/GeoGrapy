# NO ESTA IMPLEMENTADO EN LA APP PRINCIPAL

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QLineEdit, QPushButton, QLabel, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
import sys
# main_app import GeografiaApp

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyGeo - Iniciar Sesión")
        self.setFixedSize(400, 500)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal
        layout = QVBoxLayout()
        layout.setSpacing(20)
        central_widget.setLayout(layout)

        # Añadir logo
        logo_label = QLabel()
        logo_pixmap = QPixmap("resources/icon/logo2_preview.png")
        if logo_pixmap.isNull():
            logo_label.setText("LOGO")
            logo_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
            logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        else:
            scaled_pixmap = logo_pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio)
            logo_label.setPixmap(scaled_pixmap)
            logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(logo_label)
        layout.addSpacing(20)

        # Campo de entrada para el nombre
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Ingrese su nombre")
        self.name_input.setMaxLength(100)  # Límite de 100 caracteres
        self.name_input.setFixedWidth(200)
        self.name_input.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Contenedor para centrar el input
        input_container = QWidget()
        input_layout = QVBoxLayout()
        input_layout.addWidget(self.name_input, alignment=Qt.AlignmentFlag.AlignCenter)
        input_container.setLayout(input_layout)
        layout.addWidget(input_container)

        # Botón de entrada
        self.enter_button = QPushButton("Entrar")
        self.enter_button.setFixedWidth(120)
        self.enter_button.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                border: none;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
            QPushButton:pressed {
                background-color: #219a52;
            }
        """)
        self.enter_button.clicked.connect(self.validate_and_enter)

        # Contenedor para centrar el botón
        button_container = QWidget()
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.enter_button, alignment=Qt.AlignmentFlag.AlignCenter)
        button_container.setLayout(button_layout)
        layout.addWidget(button_container)

        # Centrar la ventana en la pantalla
        screen_geometry = QApplication.primaryScreen().geometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

        # Estilo general
        self.setStyleSheet("""
            QMainWindow {
                background-color: white;
            }
            QLineEdit {
                padding: 8px;
                border: 2px solid #bdc3c7;
                border-radius: 4px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
        """)

    def validate_and_enter(self):
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Error", "Por favor ingrese un nombre")
        elif len(name) < 6:
            QMessageBox.warning(self, "Error", "El nombre no puede tener más de 6 caracteres")
        else:
            # Crear y mostrar la ventana principal
#            self.main_window = GeografiaApp(name)  # Pasamos el nombre a la ventana principal
            self.main_window.show()
            self.close()

def main():
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()