from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QFrame, QPushButton, QScrollArea,
                             QDialog, QTextEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon
from src.services.notes_persistence import NotesSystem
from src.services.note_editor_system import CreateNoteEditor, EditNoteEditor
from src.utils.constants import ICON_PATH


class NoteViewerDialog(QDialog):
    """Ventana modal para visualizar una nota completa"""
    def __init__(self, note_data, notes_page, parent=None):
        super().__init__(parent)
        self.note_data = note_data
        self.notes_page = notes_page
        self.editor = None

        # hacer la ventana frameless pero sin modalidad
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Desactivar la interacción con otras ventanas
        self.setModal(False)

        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle(self.note_data.get('title', 'Nota'))

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        card = QWidget(self)
        card.setObjectName("modalCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(0, 0, 0, 0)
        card_layout.setSpacing(0)

        header = QWidget()
        header.setObjectName("modalHeader")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(16, 16, 16, 16)

        title = QLabel(self.note_data.get('title', 'Sin título'))
        title.setObjectName("modalTitle")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50;")

        close_button = QPushButton("✕")
        close_button.setObjectName("closeButton")
        close_button.clicked.connect(self.close)
        close_button.setFixedSize(30, 30)

        header_layout.addWidget(title)
        header_layout.addWidget(close_button)
        card_layout.addWidget(header)

        content = QTextEdit()
        content.setObjectName("modalContent")
        content.setPlainText(self.note_data.get('content', ''))
        content.setReadOnly(True)
        card_layout.addWidget(content)

        footer = QWidget()
        footer.setObjectName("modalFooter")
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(16, 16, 16, 16)

        edit_button = QPushButton("Editar")
        edit_button.setObjectName("footerButton")
        edit_button.clicked.connect(self.edit_note)

        close_button_footer = QPushButton("Cerrar")
        close_button_footer.setObjectName("footerButton")
        close_button_footer.clicked.connect(self.close)

        footer_layout.addStretch()
        footer_layout.addWidget(edit_button)
        footer_layout.addWidget(close_button_footer)
        card_layout.addWidget(footer)

        layout.addWidget(card)

        self.setMinimumSize(600, 400)

        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }

            #modalCard {
                background-color: #fff9e6;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
            }

            #modalHeader {
                background-color: #fff9e6;
                border-bottom: 1px solid #e5e7eb;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }

            #modalTitle {
                color: #111827;
                font-size: 1.25rem;
                margin: 0;
            }

            #closeButton {
                background: none;
                border: none;
                color: #6b7280;
                font-size: 16px;
                padding: 4px 8px;
                border-radius: 4px;
            }

            #closeButton:hover {
                color: #374151;
                background-color: #f3f4f6;
            }

            #modalContent {
                background-color: #fff9e6;
                border: none;
                padding: 16px;
                color: #374151;
            }

            #modalContent:focus {
                outline: none;
            }

            #modalFooter {
                background-color: #fff9e6;
                border-top: 1px solid #e5e7eb;
                border-bottom-left-radius: 8px;
                border-bottom-right-radius: 8px;
            }

            #footerButton {
                background-color: transparent;
                color: #374151;
                border: none;
                padding: 8px 16px;
                font-size: 0.875rem;
                font-weight: 500;
                border-radius: 4px;
                min-width: 80px;
            }

            #footerButton:hover {
                background-color: #e5e7eb;
            }
        """)

    def edit_note(self):
        self.editor = EditNoteEditor(
            category=self.note_data.get('category', ''),
            note_data=self.note_data,
            parent=self.notes_page
        )
        self.editor.note_saved.connect(self.notes_page.load_notes)
        self.editor.close_signal.connect(self.close)
        self.editor.show()
        # Ocultamos la ventana mientras se edita
        self.hide()

    def get_editor(self):
        return self.editor


class NoteCard(QFrame):
    """Tarjeta para mostrar una nota"""
    def __init__(self, note_data, notes_page, parent=None):
        super().__init__(parent)
        self.note_data = note_data
        self.notes_page = notes_page
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

        # Hacer que el cursor cambie al pasar sobre la tarjeta
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(8)

        # Título
        title = QLabel(self.note_data.get('title', 'Sin título'))
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50; border: none;")
        layout.addWidget(title)

        # Preview del contenido
        content = str(self.note_data.get('content', ''))
        # Limitar la vista previa a 50 caracteres
        preview_text = content[:50] + "..." if len(content) > 50 else content
        preview = QLabel(preview_text)
        preview.setWordWrap(True)
        preview.setStyleSheet("color: #4a4a4a; border: none;")
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
        """Manejar el evento de clic en la tarjeta"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.show_note_viewer()

    def show_note_viewer(self):
        viewer = NoteViewerDialog(self.note_data, self.notes_page, self)
        viewer.exec()


class CategorySection(QWidget):
    """Sección para mostrar las notas de una categoría"""
    def __init__(self, category_name, notes_page, parent=None):
        super().__init__(parent)
        self.category_name = category_name
        self.notes_page = notes_page
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 20)

        # Contenedor principal con estilo de tarjeta
        card_container = QFrame()
        card_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
                border: 1px solid #e0e0e0;
            }
        """)
        card_layout = QVBoxLayout(card_container)
        card_layout.setSpacing(15)
        card_layout.setContentsMargins(20, 20, 20, 20)

        # Título de categoría s
        category_title = QLabel(f"{self.category_name}")
        category_title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        category_title.setStyleSheet('''
            QLabel {
                color: white;
                background-color: #232c38;
                padding: 15px 10px;
                border-radius: 10px;
                margin-bottom: 15px;
            }
        ''')
        card_layout.addWidget(category_title)

        # Contenedor para el scroll
        scroll_container = QWidget()
        scroll_container.setFixedHeight(250)
        scroll_container_layout = QVBoxLayout(scroll_container)
        scroll_container_layout.setContentsMargins(0, 0, 0, 0)
        scroll_container_layout.setSpacing(0)

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
        self.notes_container.setStyleSheet("background: transparent;")
        self.notes_layout = QHBoxLayout(self.notes_container)
        self.notes_layout.setSpacing(15)
        self.notes_layout.setContentsMargins(0, 0, 0, 0)
        self.notes_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        scroll.setWidget(self.notes_container)
        scroll_container_layout.addWidget(scroll)
        card_layout.addWidget(scroll_container)

        # Contenedor de la tarjeta al layout principal
        main_layout.addWidget(card_container)

        # Altura fija para el contenedor de las notas
        self.setFixedHeight(450)  # Contenedor que almacenan las cards (notas)

    def add_note(self, note_data):
        note_card = NoteCard(note_data, self.notes_page, self)
        self.notes_layout.addWidget(note_card)

class NotesPage(QWidget):
    """Página principal para mostrar las notas"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.notes_system = NotesSystem()
        self.category_sections = {}
        self.setup_ui()

    def setup_ui(self):
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Header
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header.setFixedHeight(60)  # Altura para el header

        title = QLabel("Mis Notas")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50;")

        new_note_btn = QPushButton("Nueva Nota")
        new_note_btn.setIcon(QIcon(str(ICON_PATH / "plus.ico")))
        new_note_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        new_note_btn.clicked.connect(self.create_new_note)

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(new_note_btn)

        main_layout.addWidget(header)

        # Scroll área principal
        main_scroll = QScrollArea()
        main_scroll.setWidgetResizable(True)
        main_scroll.setFrameShape(QFrame.Shape.NoFrame)
        main_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        main_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        main_scroll.setStyleSheet("""
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
            QScrollBar:horizontal {
                height: 0px;
            }
        """)

        # Contenedor para las categorías
        self.categories_container = QWidget()
        self.categories_layout = QVBoxLayout(self.categories_container)
        self.categories_layout.setSpacing(30)
        self.categories_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.categories_layout.setContentsMargins(0, 0, 0, 0)

        main_scroll.setWidget(self.categories_container)
        main_layout.addWidget(main_scroll)

        # Cargar las notas iniciales
        self.load_notes()

    def create_new_note(self):
        editor = CreateNoteEditor(parent=self)
        editor.note_saved.connect(self.load_notes)
        editor.show()

    # Manejar actualizacion de notas
    def show_note_viewer(self, note_data):
        viewer = NoteViewerDialog(note_data, self)
        editor = viewer.get_editor()
        if editor:
            editor.note_saved.connect(self.load_notes)
        viewer.exec()

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
        else:
            # Crear sección para cada categoría
            for category, notes_dict in notes.items():
                category_section = CategorySection(category, self)  #  self (NotesPage)
                for notes_list in notes_dict.values():
                    for note in notes_list:
                        note['category'] = category
                        category_section.add_note(note)
                self.categories_layout.addWidget(category_section)

        # Añadir espacio al final para evitar que el último elemento se corte
        self.categories_layout.addStretch()