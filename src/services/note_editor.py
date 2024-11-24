from PyQt6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit,
                             QPushButton, QWidget, QLabel, QMessageBox)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from datetime import datetime
from src.services.notes_persistence import NotesSystem


class NoteEditor(QMainWindow):
    def __init__(self, category=None, note_data=None, parent=None):
        super().__init__(parent)
        self.category = category
        self.note_data = note_data or {
            'title': '',
            'content': '',
            'created_at': datetime.now().isoformat(),
            'modified_at': datetime.now().isoformat()
        }
        self.notes_system = NotesSystem()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Crear una nueva nota")
        self.setFixedSize(450, 600)  # Tamaño fijo para mantener el diseño compacto

        # Widget y layout principal
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Aplicar estilo al fondo
        main_widget.setStyleSheet("""
            QWidget {
                background-color: white;
            }
        """)

        # Layout principal con márgenes
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        # Título de la ventana
        title = QLabel("Crear una nueva nota")
        title.setFont(QFont("Segoe UI", 24))
        title.setStyleSheet("""
            QLabel {
                color: #111;
                font-weight: 600;
                margin-bottom: 24px;
            }
        """)
        layout.addWidget(title)

        # Función helper para crear grupos de form
        def create_form_group(label_text, widget, placeholder_text):
            group = QWidget()
            group_layout = QVBoxLayout(group)
            group_layout.setSpacing(8)
            group_layout.setContentsMargins(0, 0, 0, 16)

            label = QLabel(label_text)
            label.setFont(QFont("Segoe UI", 14))
            label.setStyleSheet("color: #111;")

            widget.setPlaceholderText(placeholder_text)
            widget.setStyleSheet("""
                QLineEdit, QTextEdit {
                    padding: 8px 12px;
                    border: 1px solid #ddd;
                    border-radius: 6px;
                    font-size: 14px;
                    line-height: 1.5;
                    background-color: white;
                }
                QLineEdit:focus, QTextEdit:focus {
                    border: 1px solid #111;
                }
            """)

            group_layout.addWidget(label)
            group_layout.addWidget(widget)
            return group

        # Categoría
        self.category_input = QLineEdit(self.category or '')
        category_group = create_form_group("Categoria", self.category_input, "Ingrese una categoria")
        layout.addWidget(category_group)

        # Título
        self.title_input = QLineEdit(self.note_data.get('title', ''))
        title_group = create_form_group("Titulo", self.title_input, "Ingrese un titulo")
        layout.addWidget(title_group)

        # Contenido
        self.editor = QTextEdit(self.note_data.get('content', ''))
        self.editor.setMinimumHeight(120)
        content_group = create_form_group("Contenido", self.editor, "Ingrese nuevo contenido")
        layout.addWidget(content_group)

        # Botones
        button_layout = QHBoxLayout()

        save_button = QPushButton("Crear una nueva nota")
        save_button.setStyleSheet("""
            QPushButton {
                padding: 12px;
                background-color: #111;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #222;
            }
        """)
        save_button.clicked.connect(self.save_note)

        cancel_button = QPushButton("Cancelar")
        cancel_button.setStyleSheet("""
            QPushButton {
                padding: 12px;
                background-color: #e0e0e0;
                color: #111;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
        """)
        cancel_button.clicked.connect(self.close)

        button_layout.addWidget(cancel_button)
        button_layout.addWidget(save_button)

        layout.addLayout(button_layout)
        layout.addStretch()

    def save_note(self):
        category = self.category_input.text().strip()
        title = self.title_input.text().strip()
        content = self.editor.toPlainText().strip()

        if not all([category, title, content]):
            QMessageBox.warning(
                self,
                "Campos incompletos",
                "Por favor, completar todos los campos (Categoria, titulo y contenido)."
            )
            return

        # Actualizar datos de la nota
        note_data = {
            'title': title,
            'content': content,
            'modified_at': datetime.now().isoformat()
        }

        # Si es una nota existente, mantener la fecha de creación
        if self.note_data.get('created_at'):
            note_data['created_at'] = self.note_data['created_at']
        else:
            note_data['created_at'] = datetime.now().isoformat()

        # Guardar la nota
        self.notes_system.add_note(category, "default", note_data)
        self.close()