from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QFrame, QPushButton, QScrollArea, QSizePolicy,
                             QDialog, QTextEdit, QLineEdit, QComboBox, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon
from pathlib import Path
from src.services.notes_persistence import NotesSystem
from src.services.note_editor import NoteEditor
from src.utils.constants import ICON_PATH


class NoteViewerDialog(QDialog):
    def __init__(self, note_data, parent=None):
        super().__init__(parent)
        self.note_data = note_data
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle(self.note_data.get('title', 'Nota'))
        self.setMinimumSize(600, 400)

        layout = QVBoxLayout(self)

        # Título
        title = QLabel(self.note_data.get('title', 'Sin título'))
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        layout.addWidget(title)

        # Contenido
        content = QTextEdit()
        content.setPlainText(self.note_data.get('content', ''))
        content.setReadOnly(True)
        content.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        layout.addWidget(content)

        # Botones
        button_layout = QHBoxLayout()

        edit_button = QPushButton("Editar")
        edit_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        edit_button.clicked.connect(self.edit_note)

        close_button = QPushButton("Cerrar")
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        close_button.clicked.connect(self.close)

        button_layout.addWidget(edit_button)
        button_layout.addWidget(close_button)
        layout.addLayout(button_layout)

    def edit_note(self):
        editor = NoteEditor(
            category=self.note_data.get('category', ''),
            note_data=self.note_data,
            parent=self
        )
        editor.show()
        self.close()


class NoteCard(QFrame):
    def __init__(self, note_data, parent=None):
        super().__init__(parent)
        self.note_data = note_data
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("""
            QFrame {
                background-color: #fff9e6;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
                margin: 10px;
                padding: 15px;
            }
            QFrame:hover {
                border: 1px solid #3498db;
                background-color: #fffdf5;
            }
        """)

        # Establecer el cursor de manera correcta
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(8)

        # Título
        title = QLabel(self.note_data.get('title', 'Sin título'))
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #1a1a1a; border: none;")
        layout.addWidget(title)

        # Preview del contenido
        content = str(self.note_data.get('content', ''))
        preview_text = content[:50] + "..." if len(content) > 50 else content
        preview = QLabel(preview_text)
        preview.setWordWrap(True)
        preview.setStyleSheet("color: #4a4a4a;")
        preview.setFont(QFont("Arial", 12))
        layout.addWidget(preview)

        # Fecha de modificación
        modified = QLabel(f"Modificado: {self.note_data.get('modified_at', 'Sin fecha')}")
        modified.setStyleSheet("color: #666; font-style: italic; border: none;")
        modified.setFont(QFont("Arial", 10))
        layout.addWidget(modified)

        self.setFixedSize(250, 200)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.show_note_viewer()

    def show_note_viewer(self):
        viewer = NoteViewerDialog(self.note_data, self)
        viewer.exec()


class CategorySection(QWidget):
    def __init__(self, category_name, parent=None):
        super().__init__(parent)
        self.category_name = category_name
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(0, 0, 0, 20)

        # Título de categoría
        category_title = QLabel(f"Etiquetas: {self.category_name}")
        category_title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        category_title.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                padding: 5px;
                background-color: rgba(52, 152, 219, 0.1);
                border-radius: 5px;
            }
        """)
        layout.addWidget(category_title)

        # Scroll área horizontal para las notas
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:horizontal {
                border: none;
                height: 8px;
                background: #F5F6FA;
            }
            QScrollBar::handle:horizontal {
                background-color: #B3B3B3;
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                border: none;
                background: none;
            }
        """)

        # Contenedor para las notas
        self.notes_container = QWidget()
        self.notes_layout = QHBoxLayout(self.notes_container)
        self.notes_layout.setSpacing(15)
        self.notes_layout.setContentsMargins(0, 10, 0, 0)
        self.notes_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        scroll.setWidget(self.notes_container)
        layout.addWidget(scroll)

    def add_note(self, note_data):
        note_card = NoteCard(note_data)
        self.notes_layout.addWidget(note_card)


class NotesPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.notes_system = NotesSystem()
        self.category_sections = {}
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Header
        header = QWidget()
        header_layout = QHBoxLayout(header)

        title = QLabel("Mis Notas")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50;")

        new_note_btn = QPushButton("Nueva Nota")
        new_note_btn.setIcon(QIcon(str(ICON_PATH / "plus.ico")))
        new_note_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        new_note_btn.clicked.connect(self.create_new_note)

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(new_note_btn)

        main_layout.addWidget(header)

        # Contenedor scrolleable para las categorías
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("""
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
        """)

        self.categories_container = QWidget()
        self.categories_layout = QVBoxLayout(self.categories_container)
        self.categories_layout.setSpacing(30)
        self.categories_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        scroll.setWidget(self.categories_container)

        main_layout.addWidget(scroll)
        self.load_notes()

    def create_new_note(self):
        editor = NoteEditor(parent=self)
        editor.show()
        editor.destroyed.connect(self.load_notes)

    def load_notes(self):
        # Limpiar categorías existentes
        while self.categories_layout.count():
            child = self.categories_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        notes = self.notes_system.load_notes()

        if not notes:
            empty_label = QLabel("No hay notas disponibles. Crea una nueva nota.")
            empty_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
            empty_label.setStyleSheet("color: #95a5a6; background-color: transparent;")
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.categories_layout.addWidget(empty_label)
            return

        # Crear sección para cada categoría
        for category, notes_dict in notes.items():
            category_section = CategorySection(category)
            for notes_list in notes_dict.values():
                for note in notes_list:
                    note['category'] = category
                    category_section.add_note(note)
            self.categories_layout.addWidget(category_section)

        # Añadir espacio al final
        self.categories_layout.addStretch()