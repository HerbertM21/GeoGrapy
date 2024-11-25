from PyQt6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit,
                             QPushButton, QWidget, QLabel, QMessageBox)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import pyqtSignal
from datetime import datetime
from src.services.notes_persistence import NotesSystem


class NotesManager:
    """Componente para manejar las notas"""

    def __init__(self, editor):
        self.editor = editor
        self.notes_system = NotesSystem()

    def save_note(self, note_data: dict, category: str) -> bool:
        """Maneja la lógica de guardado de notas"""
        try:
            if category not in self.get_notes():
                self.create_category(category)
            return self.notes_system.add_note(category, "default", note_data)
        except Exception as e:
            self.editor.show_error_message("Error", f"Error al guardar: {str(e)}")
            return False

    def update_note(self, note_data: dict, category: str) -> bool:
        """Maneja la lógica de actualización de notas"""
        try:
            notes = self.get_notes()

            if category not in notes:
                notes[category] = {'default': []}

            category_notes = notes[category]['default']
            found = False

            for i, note in enumerate(category_notes):
                if note['created_at'] == self.editor.note_data['created_at']:
                    category_notes[i] = note_data
                    found = True
                    break

            if not found:
                category_notes.append(note_data)

            return self.notes_system.save_notes(notes)
        except Exception as e:
            self.editor.show_error_message("Error", f"Error al actualizar: {str(e)}")
            return False

    def get_notes(self) -> dict:
        """Obtiene todas las notas"""
        return self.notes_system.load_notes()

    def create_category(self, category: str) -> None:
        """Crea una nueva categoría"""
        notes = self.get_notes()
        notes[category] = {'default': []}
        self.notes_system.save_notes(notes)


class BaseNoteEditor(QMainWindow):
    note_saved = pyqtSignal()
    close_signal = pyqtSignal()

    def __init__(self, category=None, note_data=None, parent=None):
        super().__init__(parent)
        self.category = category
        self.note_data = note_data or {
            'title': '',
            'content': '',
            'created_at': datetime.now().isoformat(),
            'modified_at': datetime.now().isoformat()
        }
        self.notes_manager = NotesManager(self)
        self.setup_base_ui()

    def setup_base_ui(self):
        """Configura la interfaz base común para todos los editores"""
        self.setFixedSize(450, 600)

        # Widget y layout principal
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_widget.setStyleSheet("""
            QWidget {
                background-color: white;
            }
        """)

        # Layout principal con márgenes
        self.layout = QVBoxLayout(main_widget)
        self.layout.setSpacing(16)
        self.layout.setContentsMargins(24, 24, 24, 24)

        # Título de la ventana (será sobrescrito por las clases hijas)
        self.window_title = QLabel()
        self.window_title.setFont(QFont("Segoe UI", 24))
        self.window_title.setStyleSheet("""
            QLabel {
                color: #111;
                font-weight: 600;
                margin-bottom: 24px;
            }
        """)
        self.layout.addWidget(self.window_title)

        # Crear campos del formulario
        self.create_form_fields()

        # Crear botones
        self.create_buttons()

        self.layout.addStretch()

    def create_form_group(self, label_text, widget, placeholder_text):
        """Crea un grupo de formulario con etiqueta y widget"""
        group = QWidget()
        group_layout = QVBoxLayout(group)
        group_layout.setSpacing(8)
        group_layout.setContentsMargins(0, 0, 0, 16)

        label = QLabel(label_text)
        label.setFont(QFont("Segoe UI", 14))
        label.setStyleSheet("color: #111; font-weight: bold;")

        widget.setPlaceholderText(placeholder_text)
        widget.setStyleSheet("""
            QLineEdit, QTextEdit {
                padding: 8px 12px;
                border: 1px solid #ddd;
                border-radius: 6px;
                font-size: 14px;
                line-height: 1.5;
                background-color: white;
                color: #2c3e50;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 1px solid #111;
            }
        """)

        group_layout.addWidget(label)
        group_layout.addWidget(widget)
        return group

    def create_form_fields(self):
        """Crea los campos del formulario"""
        # Categoría
        self.category_input = QLineEdit(self.category or '')
        category_group = self.create_form_group("Categoría", self.category_input, "Ingrese una categoría")
        self.layout.addWidget(category_group)

        # Título
        self.title_input = QLineEdit(self.note_data.get('title', ''))
        title_group = self.create_form_group("Título", self.title_input, "Ingrese un título")
        self.layout.addWidget(title_group)

        # Contenido
        self.editor = QTextEdit(self.note_data.get('content', ''))
        self.editor.setMinimumHeight(120)
        content_group = self.create_form_group("Contenido", self.editor, "Ingrese contenido")
        self.layout.addWidget(content_group)

    def create_buttons(self):
        """Crea los botones de acción"""
        button_layout = QHBoxLayout()

        save_button = QPushButton()
        save_button.setStyleSheet("""
            QPushButton {
                padding: 12px;
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #2980b9;
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

        self.layout.addLayout(button_layout)

        # Guardar referencias a los botones para que las clases hijas puedan modificarlos
        self.save_button = save_button
        self.cancel_button = cancel_button

    def save_note(self):
        """Metodo que debe ser implementado por las clases hijas"""
        raise NotImplementedError("Las clases hijas deben implementar save_note")

    def show_error_message(self, title, message):
        msg = QMessageBox(self)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QMessageBox QLabel {
                color: #111;
                font-size: 14px;
            }
            QMessageBox QPushButton {
                padding: 6px 12px;
                border-radius: 4px;
                min-width: 70px;
                background-color: #3498db;
                color: white;
                border: none;
            }
            QMessageBox QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec()

    def closeEvent(self, event):
        """Evento de cierre"""
        self.close_signal.emit()
        super().closeEvent(event)


class CreateNoteEditor(BaseNoteEditor):
    def __init__(self, category=None, parent=None):
        super().__init__(category=category, parent=parent)
        self.setWindowTitle("Crear una nueva nota")
        self.window_title.setText("Crear una nueva nota")
        self.save_button.setText("Crear nota")

    def save_note(self):
        category = self.category_input.text().strip()
        title = self.title_input.text().strip()
        content = self.editor.toPlainText().strip()

        if not all([title, content]):
            self.show_error_message("Campos incompletos",
                                    "Por favor, complete al menos el título y el contenido de la nota.")
            return

        note_data = {
            'title': title,
            'content': content,
            'created_at': datetime.now().isoformat(),
            'modified_at': datetime.now().isoformat()
        }

        if self.notes_manager.save_note(note_data, category):
            self.note_saved.emit()
            self.close_signal.emit()
            self.close()
        else:
            self.show_error_message("Error", "No se pudo guardar la nota. Por favor, intente nuevamente.")


class EditNoteEditor(BaseNoteEditor):
    def __init__(self, category, note_data, parent=None):
        note_data['category'] = category
        super().__init__(category=category, note_data=note_data, parent=parent)
        self.setWindowTitle("Editar nota")
        self.window_title.setText("Editar nota")
        self.save_button.setText("Guardar cambios")
        self.category_input.setReadOnly(True)

    def save_note(self):
        category = self.category_input.text().strip()
        title = self.title_input.text().strip()
        content = self.editor.toPlainText().strip()

        if not all([title, content]):
            self.show_error_message("Campos incompletos",
                                    "Por favor, complete al menos el título y el contenido de la nota.")
            return

        note_data = {
            'title': title,
            'content': content,
            'category': category,
            'created_at': self.note_data['created_at'],
            'modified_at': datetime.now().isoformat()
        }

        if self.notes_manager.update_note(note_data, category):
            self.note_saved.emit()
            self.close_signal.emit()
            self.close()
        else:
            self.show_error_message("Error", "No se pudo actualizar la nota. Por favor, intente nuevamente.")