from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,
                             QPushButton, QScrollArea, QLabel, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QGraphicsDropShadowEffect
from src.utils.constants import ICON_PATH
from src.services.chat_service import ChatService
from PyQt6.QtGui import QPixmap, QPainter

# Clase para añadir la funcionalidad de enviar un mensaje al presionar Enter
class CustomTextEdit(QTextEdit):
    enter_pressed = pyqtSignal()

    def keyPressEvent(self, event):
        """Envía la señal enter_pressed cuando se presiona Enter
            Enviar el mensaje solamente con Enter

        Args:
            event (QKeyEvent): Evento de teclado

        Returns:
            None
        """
        if event.key() == Qt.Key.Key_Return and not event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
            self.enter_pressed.emit()
            event.accept()
        else:
            super().keyPressEvent(event)

class MessageWidget(QFrame):
    def __init__(self, text, is_user=True, parent=None):
        super().__init__(parent)
        self.is_user = is_user
        self.text = text
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(0)

        if not self.is_user:
            # IMAGEN BOT UVA
            profile_pic = QLabel()
            pixmap = QPixmap(str(ICON_PATH / "uva_fondo.png"))
            scaled_pixmap = pixmap.scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio,
                                        Qt.TransformationMode.SmoothTransformation)
            profile_pic.setPixmap(scaled_pixmap)
            profile_pic.setFixedSize(40, 40)
            profile_pic.setStyleSheet("""
                QLabel {
                    border-radius: 20px;
                    background-color: transparent;
                }
            """)
            # SE CREA CONTORNO CIRCULAR
            mask = QPixmap(40, 40)
            mask.fill(Qt.GlobalColor.transparent)
            painter = QPainter(mask)
            painter.setBrush(Qt.GlobalColor.white)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(0, 0, 40, 40)
            painter.end()
            scaled_pixmap.setMask(mask.mask())
            profile_pic.setPixmap(scaled_pixmap)
            layout.addWidget(profile_pic)

        # Contenedor de mensaje
        bubble = QFrame()
        bubble.setMaximumWidth(500)
        bubble.setStyleSheet(f"""
            QFrame {{
                background-color: {'#DCF8C6' if self.is_user else '#E8E8E8'};
                border-radius: 12px;
                border: 1px solid {'#c5e1a5' if self.is_user else '#d4d4d4'};
                margin: 2px 5px;
            }}
        """)

        # efecto sombra
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setXOffset(0)
        shadow.setYOffset(2)
        shadow.setColor(QColor(0, 0, 0, 40))
        bubble.setGraphicsEffect(shadow)

        bubble_layout = QVBoxLayout(bubble)
        bubble_layout.setContentsMargins(12, 10, 12, 10)
        bubble_layout.setSpacing(0)

        text_label = QLabel(self.text)
        text_label.setWordWrap(True)
        text_label.setTextFormat(Qt.TextFormat.PlainText)
        text_label.setStyleSheet("""
            QLabel {
                color: black;
                font-size: 14px;
                background: transparent;
                padding: 2px;
                border: none;
            }
        """)

        bubble_layout.addWidget(text_label)

        # ajustar alineación
        layout.addStretch() if self.is_user else None
        layout.addWidget(bubble)
        layout.addStretch() if not self.is_user else None


class ChatPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.chat_service = ChatService()
        self.setup_ui()
        self.messages_to_process = []
        self.is_processing = False

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.chat_area = QScrollArea()
        self.chat_area.setWidgetResizable(True)
        self.chat_area.setStyleSheet(self.get_chat_area_style())

        self.message_container = QWidget()
        self.message_layout = QVBoxLayout(self.message_container)
        self.message_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.message_layout.setSpacing(2)
        self.message_layout.setContentsMargins(0, 10, 0, 10)
        self.chat_area.setWidget(self.message_container)

        input_panel = QWidget()
        input_panel.setFixedHeight(80)
        input_panel.setStyleSheet(self.get_input_panel_style())

        input_layout = QHBoxLayout(input_panel)
        input_layout.setContentsMargins(10, 5, 10, 5)
        input_layout.setSpacing(10)

        self.input_area = CustomTextEdit()
        self.input_area.setPlaceholderText("Escribe tu mensaje aquí...")
        self.input_area.setFixedHeight(50)
        self.input_area.setStyleSheet(self.get_input_area_style())

        # Conectar la señal enter_pressed con send_message
        self.input_area.enter_pressed.connect(self.send_message)

        self.send_button = QPushButton("Enviar")
        self.send_button.setFixedSize(60, 35)
        self.send_button.setStyleSheet(self.get_send_button_style())
        self.send_button.clicked.connect(self.send_message)

        input_layout.addWidget(self.input_area)
        input_layout.addWidget(self.send_button)

        main_layout.addWidget(self.chat_area)
        main_layout.addWidget(input_panel)

        self.add_message("¡Hola! Soy Grapy, tu asistente de geografía. ¿En qué puedo ayudarte?", False)


    def send_message(self):
        """Envía el mensaje del usuario y obtiene la respuesta"""
        text = self.input_area.toPlainText().strip()
        if text:
            self.add_message(text, True)
            self.input_area.clear()
            response = self.chat_service.get_response(text)
            self.add_message(response, False)

    def add_message(self, text, is_user):
        """Añade un mensaje al chat"""
        message = MessageWidget(text, is_user)
        self.message_layout.addWidget(message)
        self.scroll_to_bottom()

    def scroll_to_bottom(self):
        """Desplaza el scroll al final del chat"""
        QTimer.singleShot(100, lambda: self.chat_area.verticalScrollBar().setValue(
            self.chat_area.verticalScrollBar().maximum()
        ))

    @staticmethod
    def get_chat_area_style():
        return """
            QScrollArea {
                border: none;
                background-color: #F5F6FA;
            }
            QScrollBar:vertical {
                border: none;
                width: 8px;
                background: #F5F6FA;
            }
            QScrollBar::handle:vertical {
                background-color: #B3B3B3;
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """

    @staticmethod
    def get_input_panel_style():
        return """
            QWidget {
                background-color: white;
                border-top: 1px solid #E0E0E0;
            }
        """

    @staticmethod
    def get_input_area_style():
        return """
            QTextEdit {
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                padding: 8px;
                font-size: 13px;
                background-color: white;
                color: black;
            }
        """

    @staticmethod
    def get_send_button_style():
        return """
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """