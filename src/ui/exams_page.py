from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QScrollArea, QProgressBar, QGridLayout,
                             QSizePolicy, QFrame,  QRadioButton, QDialog, QButtonGroup)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
from src.services.exam_data import get_exams_by_category
from src.ui.exam_window import ExamWindow
from src.utils.constants import ICON_PATH
from src.services.level_system import AbstractLevelSystem, JsonProgressPersistence, ImprovedLevelSystem
from datetime import datetime

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
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter) # Centrar la imagen
        image_layout.addWidget(image_label) # Añadir la imagen al layout

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


class DifficultySelector(QDialog):
    """Diálogo para seleccionar la dificultad del sistema de niveles"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_difficulty = 'normal'  # Dificultad por defecto
        self.setStyleSheet("""
            QDialog {
                background-color: #232c38; /* Fondo gris claro */
            }
        """)
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Selecciona tu Dificultad")
        self.setMinimumWidth(400)
        layout = QVBoxLayout(self)

        # Obtener información de dificultades
        difficulties = ImprovedLevelSystem.get_available_difficulties()

        # Grupo de botones para la selección
        self.button_group = QButtonGroup(self)

        # Crear tarjeta para cada dificultad
        for diff_key, diff_info in difficulties.items():
            card = self.create_difficulty_card(diff_key, diff_info)
            layout.addWidget(card)

        # Botón de confirmación
        confirm_btn = QPushButton("Confirmar Selección")
        confirm_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        confirm_btn.clicked.connect(self.accept)
        layout.addWidget(confirm_btn)

    def create_difficulty_card(self, diff_key, diff_info) -> QFrame:
        """Crea una tarjeta visual para cada dificultad"""
        card = QFrame()
        card.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 10px;
                padding: 10px;
                margin: 5px;
            }
        """)

        card_layout = QVBoxLayout(card)

        # Radio button para selección -título de la dificultad-
        radio = QRadioButton(diff_info['name'])
        radio.setStyleSheet("""
            QRadioButton {
                color: #232c38  /* Texto en negro */
            }
            QRadioButton::indicator {
                width: 16px;
                height: 16px;
            }
            QRadioButton::indicator::unchecked {
                border: 1px solid #555;
                background-color: white;
                border-radius: 8px;
            }
            QRadioButton::indicator::checked {
                border: 1px solid #555;
                background-color: #3498db;
                border-radius: 8px;
            }
        """)
        if diff_key == 'normal':
            radio.setChecked(True)
        radio.setObjectName(diff_key)
        radio.toggled.connect(lambda: self.on_difficulty_selected(diff_key))
        self.button_group.addButton(radio)

        # Descripción
        desc = QLabel(diff_info['description'])
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #505357;")  # Texto negro para descripción

        # Bonificaciones
        rewards = QLabel(f"Multiplicador de recompensas: x{diff_info['reward_multiplier']}")
        rewards.setStyleSheet("color: #3498db; font-weight: Bold;")  # Texto negro para bonificaciones

        # Características exclusivas
        if diff_info['exclusive_rewards']:
            exclusive = QLabel("✨ ¡Incluye recompensas exclusivas!")
            exclusive.setStyleSheet("color: #e67e22; font-weight: bold;")
            card_layout.addWidget(exclusive)

        card_layout.addWidget(radio)
        card_layout.addWidget(desc)
        card_layout.addWidget(rewards)

        return card

    def on_difficulty_selected(self, difficulty):
        """Guarda la dificultad seleccionada"""
        self.selected_difficulty = difficulty

    def get_selected_difficulty(self) -> str:
        """Retorna la dificultad seleccionada"""
        return self.selected_difficulty




class ExamsPage(QWidget):
    def __init__(self, parent=None, level_system: AbstractLevelSystem = None,
                 progress_persistence=None):
        super().__init__(parent)

        # Inicializar sistemas
        self.level_system = level_system
        self.progress_persistence = progress_persistence

        if not self.level_system or not self.progress_persistence:
            raise ValueError("Se requiere level_system y progress_persistence")

        # Configuración inicial de categorías
        self.categories = [
            ("PAÍSES", "paises", "#3498db", str(ICON_PATH / "paises-preview.png")),
            ("CAPITALES", "capitales", "#e74c3c", str(ICON_PATH / "capitals-preview.png")),
            ("FLORA", "flora", "#2ecc71", str(ICON_PATH / "flora-preview.png")),
            ("FAUNA", "fauna", "#f1c40f", str(ICON_PATH / "fauna.png"))
        ]

        # Inicializar variables de nivel y progreso
        self.load_user_progress()

        # Configurar la interfaz
        self._setup_ui()

    def load_user_progress(self):
        """Carga el progreso del usuario desde el sistema de persistencia"""
        progress_data = self.progress_persistence.load_progress('current_user')
        total_xp = progress_data.get('total_xp', 0)

        # Obtener nivel actual y progreso
        level_progress = self.level_system.get_level_progress(total_xp)
        self.nivel = level_progress.level
        self.exp = level_progress.current_xp
        self.exp_necesaria = level_progress.xp_for_next

    def start_exam(self, exam_data):
        """Inicia un nuevo examen con el sistema de niveles configurado"""
        self.exam_window = ExamWindow(
            exam_data=exam_data,
            level_system=self.level_system,
            progress_persistence=self.progress_persistence
        )
        self.exam_window.exam_completed.connect(self.on_exam_completed)
        self.exam_window.show()

    def show_difficulty_selector(self) -> str:
        """Muestra el diálogo de selección de dificultad"""
        selector = DifficultySelector(self)
        if selector.exec():
            return selector.get_selected_difficulty()
        return 'normal'  # Dificultad por defecto si se cierra el diálogo

    def _setup_ui(self):
        """Configuración de la interfaz de usuario"""
        # Layout principal
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(20, 20, 20, 20)

        # ScrollArea principal que contendrá todo excepto la barra de progreso
        main_scroll = QScrollArea()
        main_scroll.setWidgetResizable(True) # El widget interno se ajusta al tamaño del ScrollArea
        main_scroll.setFrameShape(QFrame.Shape.NoFrame) # Sin borde
        main_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded) # Scroll vertical si es necesario
        main_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff) # Sin scroll horizontal
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
        scroll_layout.setSpacing(30)
        scroll_layout.setContentsMargins(0, 0, 0, 0)

        # Título para la sección de categorías
        categories_title = QLabel("Categorías")
        categories_title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        categories_title.setStyleSheet("color: #2c3e50;")
        scroll_layout.addWidget(categories_title)

        # Crear secciones
        categories_section = self.create_categories_section()
        scroll_layout.addWidget(categories_section)

        # Título para la sección de exámenes
        exams_title = QLabel("Exámenes disponibles")
        exams_title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        exams_title.setStyleSheet("color: #2c3e50;")
        scroll_layout.addWidget(exams_title)

        exams_section = self.create_exams_section()
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
        """Crea la sección de categorías con íconos y botones"""
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
        """Crea la sección de exámenes con scroll horizontal"""
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

    def load_exams(self, category: str):
        """Carga y muestra los exámenes de una categoría específica"""
        while self.exams_layout.count():
            item = self.exams_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        exams = get_exams_by_category(category)
        for exam_data in exams:
            exam_button = ExamButton(exam_data)
            exam_button.clicked.connect(lambda c, data=exam_data: self.start_exam(data))
            self.exams_layout.addWidget(exam_button)

    def save_user_progress(self):
        """Guarda el progreso actual del usuario"""
        current_progress = self.progress_persistence.load_progress('current_user')
        current_progress.update({
            'total_xp': self.calculate_total_xp(),
            'level': self.nivel,
            'last_update': str(datetime.now())
        })
        self.progress_persistence.save_progress('current_user', current_progress)

    def calculate_total_xp(self) -> int:
        """Calcula la XP total acumulada del usuario"""
        total = 0
        for level in range(1, self.nivel):
            total += self.level_system.calculate_xp_for_level(level)
        total += self.exp
        return total

    def on_exam_completed(self, result):
        """Maneja la finalización de un examen y actualiza el progreso"""
        self.load_user_progress()
        self.update_level_display()
        self.check_unlocked_features()

    def check_unlocked_features(self):
        """Verifica y actualiza las características desbloqueadas por nivel"""
        rewards = self.level_system.get_level_rewards(self.nivel)

        if 'create_custom_quizzes' in rewards.features:
            self.enable_custom_quiz_creation()

        if 'custom_profile' in rewards.features:
            self.enable_custom_profile()

    def enable_custom_quiz_creation(self):
        """Creación de cuestionarios personalizados desbloqueado"""
        # PRONTO NO ES PRIORIDAD
        pass

    def enable_custom_profile(self):
        """Personalización del perfil desbloqueado"""
        # NO ES PRIORIDAD
        pass

    def create_level_section(self):
        """Crea la sección de nivel con información detallada"""
        level_widget = QWidget()
        level_widget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        level_widget.setMaximumHeight(100)
        level_layout = QVBoxLayout(level_widget)
        level_layout.setContentsMargins(10, 10, 10, 10)

        # Información detallada del nivel
        level_info = QGridLayout()
        level_info.setColumnStretch(0, 1)
        level_info.setColumnStretch(1, 1)
        level_info.setColumnStretch(2, 1)

        # Etiqueta de nivel con título
        self.level_label = QLabel(f"Nivel {self.nivel}")
        self.level_label.setStyleSheet("""
            color: #2c3e50;
            padding: 5px;
            background-color: rgba(52, 152, 219, 0.1);
            border-radius: 5px;
        """)
        self.level_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))

        # Etiqueta de XP con más detalles
        self.exp_label = QLabel()
        self.exp_label.setStyleSheet("""
            color: #27ae60;
            padding: 5px;
            background-color: rgba(46, 204, 113, 0.1);
            border-radius: 5px;
        """)
        self.exp_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))

        level_info.addWidget(self.level_label, 0, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        level_info.addWidget(self.exp_label, 0, 2, alignment=Qt.AlignmentFlag.AlignRight)

        # Barra de progreso mejorada
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimumHeight(20)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                border-radius: 10px;
                background-color: #ddd;
                text-align: center;
                color: #2c3e50;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3498db,
                    stop:1 #2ecc71
                );
                border-radius: 10px;
            }
        """)

        level_layout.addLayout(level_info)
        level_layout.addWidget(self.progress_bar)

        return level_widget

    def update_level_display(self):
        """Actualiza la visualización del progreso del nivel con información detallada"""
        # Actualizar etiquetas
        self.level_label.setText(f"Nivel {self.nivel}")

        # Calcular porcentaje de progreso
        progress_percent = (self.exp / self.exp_necesaria) * 100 if self.exp_necesaria > 0 else 100

        # Actualizar etiqueta de XP con porcentaje
        self.exp_label.setText(
            f"EXP: {self.exp}/{self.exp_necesaria} ({progress_percent:.1f}%)"
        )

        # Actualizar barra de progreso
        self.progress_bar.setRange(0, self.exp_necesaria)
        self.progress_bar.setValue(self.exp)
        self.progress_bar.setFormat(f"{progress_percent:.1f}%")

        # Guardar progreso
        self.save_user_progress()

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