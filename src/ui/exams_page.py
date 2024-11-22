from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QScrollArea, QProgressBar, QGridLayout,
                             QSizePolicy, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
from src.services.exam_data import get_exams_by_category
from src.ui.exam_window import ExamWindow
from src.utils.constants import ICON_PATH
from pathlib import Path


class ExamButton(QPushButton):
    def __init__(self, exam_data):
        super().__init__()
        self.exam_data = exam_data
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)
        self.setLayout(layout)

        # Contenedor para la imagen
        image_container = QWidget()
        image_container.setFixedHeight(120)
        image_layout = QVBoxLayout(image_container)
        image_layout.setContentsMargins(0, 0, 0, 0)

        image_label = QLabel()
        icon_path = str(ICON_PATH / self.exam_data['icon'].split('/')[-1])
        pixmap = QPixmap(icon_path)
        if not pixmap.isNull():
            pixmap = pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
            image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_layout.addWidget(image_label)

        title_label = QLabel(self.exam_data['title'])
        title_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #2c3e50;")
        title_label.setWordWrap(True)

        difficulty_label = QLabel(f"Dificultad: {self.exam_data['difficulty']}")
        difficulty_label.setStyleSheet("color: #7f8c8d;")

        xp_label = QLabel(f"XP: {self.exam_data['xp']}")
        xp_label.setStyleSheet("color: #27ae60;")

        layout.addWidget(image_container)
        for label in [title_label, difficulty_label, xp_label]:
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(label)

        self.setMinimumSize(180, 250)
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.setStyleSheet("""
            ExamButton {
                background-color: #f5f6fa;
                border: 2px solid #ddd;
                border-radius: 10px;
                padding: 10px;
            }
            ExamButton:hover {
                border-color: #3498db;
                background-color: #f0f8ff;
            }
        """)


class ExamsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.nivel = 1
        self.exp = 0
        self.exp_necesaria = 100
        self.categories = [
            ("PAÍSES", "paises", "#3498db", str(ICON_PATH / "paises-preview.png")),
            ("CAPITALES", "capitales", "#e74c3c", str(ICON_PATH / "capitals-preview.png")),
            ("FLORA", "flora", "#2ecc71", str(ICON_PATH / "flora-preview.png")),
            ("FAUNA", "fauna", "#f1c40f", str(ICON_PATH / "fauna.png"))
        ]
        self.setup_ui()

    def setup_ui(self):
        # Layout principal
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(20, 20, 20, 20)

        # ScrollArea principal que contendrá todo excepto la barra de progreso
        main_scroll = QScrollArea()
        main_scroll.setWidgetResizable(True)
        main_scroll.setFrameShape(QFrame.Shape.NoFrame)
        main_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        main_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
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
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)

        # Widget contenedor para el contenido scrolleable
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(20)
        scroll_layout.setContentsMargins(0, 0, 0, 0)

        # Crear secciones
        categories_section = self.create_categories_section()
        exams_section = self.create_exams_section()

        # Agregar secciones al layout scrolleable
        scroll_layout.addWidget(categories_section)
        scroll_layout.addWidget(exams_section)

        # Configurar el ScrollArea
        main_scroll.setWidget(scroll_content)

        # Layout principal: ScrollArea arriba, barra de progreso abajo
        self.layout.addWidget(main_scroll)

        # Crear y agregar la sección de nivel al final
        level_section = self.create_level_section()
        self.layout.addWidget(level_section)

        self.update_level_display()

    def create_categories_section(self):
        categories_widget = QWidget()
        categories_widget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        categories_layout = QVBoxLayout(categories_widget)
        categories_layout.setSpacing(15)

        # Container para íconos y botones
        icons_buttons_container = QWidget()
        icons_buttons_layout = QVBoxLayout(icons_buttons_container)
        icons_buttons_layout.setSpacing(10)

        # Layout para íconos
        icons_layout = QHBoxLayout()
        icons_layout.setSpacing(20)
        icons_layout.setContentsMargins(10, 0, 10, 0)

        # Layout para botones
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)
        buttons_layout.setContentsMargins(10, 0, 10, 0)

        for _, _, _, icon_path in self.categories:
            icon_container = QWidget()
            icon_container.setFixedWidth(150)
            icon_layout = QVBoxLayout(icon_container)
            icon_layout.setContentsMargins(0, 0, 0, 0)

            icon_label = QLabel()
            pixmap = QPixmap(icon_path)
            if not pixmap.isNull():
                pixmap = pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
                icon_label.setPixmap(pixmap)
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            icon_layout.addWidget(icon_label)
            icons_layout.addWidget(icon_container)

        for texto, categoria, color, _ in self.categories:
            btn = QPushButton(texto)
            btn.setFixedSize(150, 50)
            btn.clicked.connect(lambda c, cat=categoria: self.load_exams(cat))
            btn.setStyleSheet(self.get_category_button_style(color))
            buttons_layout.addWidget(btn)

        icons_buttons_layout.addLayout(icons_layout)
        icons_buttons_layout.addLayout(buttons_layout)
        categories_layout.addWidget(icons_buttons_container)

        return categories_widget

    def create_exams_section(self):
        exams_widget = QWidget()
        exams_widget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        exams_layout = QVBoxLayout(exams_widget)
        exams_layout.setContentsMargins(0, 0, 0, 0)

        self.exams_scroll = QScrollArea()
        self.exams_scroll.setWidgetResizable(True)
        self.exams_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.exams_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.exams_scroll.setMinimumHeight(300)
        self.exams_scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.exams_scroll.setStyleSheet("""
            QScrollArea {
                background-color: #f5f6fa;
                border: none;
            }
            QScrollBar:horizontal {
                border: none;
                height: 8px;
                background: #F5F6FA;
            }
            QScrollBar::handle:horizontal {
                background-color: #B3B3B3;
                border-radius: 4px;
                min-width: 20px;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                border: none;
                background: none;
            }
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: none;
            }
        """)

        self.exams_container = QWidget()
        self.exams_layout = QHBoxLayout(self.exams_container)
        self.exams_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.exams_layout.setSpacing(20)
        self.exams_layout.setContentsMargins(10, 10, 10, 10)

        self.exams_scroll.setWidget(self.exams_container)

        exams_layout.addWidget(self.exams_scroll)
        return exams_widget

    def create_level_section(self):
        level_widget = QWidget()
        level_widget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        level_widget.setMaximumHeight(100)  # Limitar altura máxima
        level_layout = QVBoxLayout(level_widget)
        level_layout.setContentsMargins(10, 10, 10, 10)

        level_info = QGridLayout()
        level_info.setColumnStretch(0, 1)
        level_info.setColumnStretch(1, 1)
        level_info.setColumnStretch(2, 1)

        self.level_label = QLabel(f"Nivel {self.nivel}")
        self.level_label.setStyleSheet("color: #2c3e50;")
        self.level_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))

        self.exp_label = QLabel(f"EXP: {self.exp}/{self.exp_necesaria}")
        self.exp_label.setStyleSheet("color: #27ae60;")
        self.exp_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))

        level_info.addWidget(self.level_label, 0, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        level_info.addWidget(self.exp_label, 0, 2, alignment=Qt.AlignmentFlag.AlignRight)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimumHeight(20)
        self.progress_bar.setRange(0, self.exp_necesaria)
        self.progress_bar.setValue(self.exp)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                border-radius: 10px;
                background-color: #ddd;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #3498db;
                border-radius: 10px;
            }
        """)

        level_layout.addLayout(level_info)
        level_layout.addWidget(self.progress_bar)

        return level_widget

    def load_exams(self, category):
        while self.exams_layout.count():
            item = self.exams_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        exams = get_exams_by_category(category)
        for exam_data in exams:
            exam_button = ExamButton(exam_data)
            exam_button.clicked.connect(lambda c, data=exam_data: self.start_exam(data))
            self.exams_layout.addWidget(exam_button)

    def start_exam(self, exam_data):
        self.exam_window = ExamWindow(exam_data)
        self.exam_window.exam_completed.connect(self.on_exam_completed)
        self.exam_window.show()

    def on_exam_completed(self, result):
        self.exp += result['xp_earned']
        while self.exp >= self.exp_necesaria:
            self.nivel += 1
            self.exp -= self.exp_necesaria
            self.exp_necesaria = int(self.exp_necesaria * 1.5)
        self.update_level_display()

    def update_level_display(self):
        self.level_label.setText(f"Nivel {self.nivel}")
        self.exp_label.setText(f"EXP: {self.exp}/{self.exp_necesaria}")
        self.progress_bar.setRange(0, self.exp_necesaria)
        self.progress_bar.setValue(self.exp)

    @staticmethod
    def get_category_button_style(color):
        return f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
                padding: 10px;
            }}
            QPushButton:hover {{
                background-color: {color}dd;
            }}
        """