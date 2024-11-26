from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QFrame, QScrollArea, QGridLayout, QSpacerItem, QSizePolicy, QPushButton)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor, QPainter, QPen, QPixmap
from PyQt6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from datetime import datetime, timedelta
import json
from pathlib import Path
from src.services.level_system import ImprovedLevelSystem, JsonProgressPersistence, LevelProgress
from src.utils.constants import ICON_PATH


class StatsPage(QWidget):
    """Página de estadísticas del usuario"""
    def __init__(self, parent=None):
        super().__init__(parent)

        # Inicializar sistema de niveles y persistencia
        save_dir = Path.home() / '.geograpy' / 'progress'
        self.progress_persistence = JsonProgressPersistence(save_dir)

        # Cargar progreso actual
        self.current_progress = self.progress_persistence.load_progress('current_user')

        # Inicializar sistema de niveles con la dificultad guardada
        difficulty = self.current_progress.get('difficulty', 'normal')
        self.level_system = ImprovedLevelSystem(difficulty=difficulty)

        self.setup_ui()
        self.load_user_stats()

    def setup_ui(self):
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # ScrollArea para todo el contenido
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
        """)

        # Widget contenedor para el contenido scrolleable
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(30)

        # Título y nivel
        title_section = self.create_title_section()
        content_layout.addWidget(title_section)

        # Grid para las tarjetas de estadisticas
        stats_grid = self.create_stats_grid()
        content_layout.addWidget(stats_grid)

        # Seccion de recompensas
        rewards_section = self.create_rewards_section()
        content_layout.addWidget(rewards_section)

        # Grafico de progreso
        progress_chart = self.create_progress_chart()
        content_layout.addWidget(progress_chart)

        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

    def create_title_section(self):
        title_widget = QWidget()
        title_layout = QHBoxLayout(title_widget)

        title = QLabel("Estadísticas del Usuario")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50;")

        self.difficulty_label = QLabel()
        self.difficulty_label.setFont(QFont("Arial", 14))
        self.difficulty_label.setStyleSheet("color: #7f8c8d;")

        self.level_label = QLabel()
        self.level_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.level_label.setStyleSheet("""
            color: #2c3e50;
            padding: 5px;
            background-color: rgba(52, 152, 219, 0.1);
            border-radius: 5px;
        """)

        title_layout.addWidget(title)
        title_layout.addStretch()
        title_layout.addWidget(self.difficulty_label)
        title_layout.addWidget(self.level_label)

        return title_widget

    def create_stats_grid(self):
        stats_widget = QWidget()
        stats_layout = QGridLayout(stats_widget)
        stats_layout.setSpacing(20)

        # Lista de estadísticas a mostrar
        self.stat_labels = {
            'total_xp': self.create_stat_card("XP Total",
                str(self.current_progress.get('total_xp', 0))),
            'exams_completed': self.create_stat_card("Exámenes Completados",
                str(self.current_progress.get('exams_completed', 0))),
            'accuracy': self.create_stat_card("Precisión Media",
                f"{self.current_progress.get('average_accuracy', 0):.1f}%"),
            'xp_to_next': self.create_stat_card("XP para siguiente nivel", "0")
        }

        # Organizar las tarjetas en un grid 2x2
        positions = [(i, j) for i in range(2) for j in range(2)]
        for (key, card), (row, col) in zip(self.stat_labels.items(), positions):
            stats_layout.addWidget(card, row, col)

        return stats_widget

    def create_stat_card(self, title, value):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 15px;
                border: 1px solid #e0e0e0;
            }
        """)

        layout = QVBoxLayout(card)

        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        title_label.setStyleSheet('''
            color: white;
            background-color: #232c38;
            padding: 15px 10px;
            border-radius: 10px;
        ''')
        layout.addWidget(title_label)

        value_label = QLabel(value)
        value_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        value_label.setStyleSheet("""
            color: #2c3e50;
            margin-top: 10px;
        """)
        value_label.setObjectName("value_label")

        layout.addWidget(value_label)

        return card

    def create_rewards_section(self):
        rewards_widget = QFrame()
        rewards_widget.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
                border: 1px solid #e0e0e0;
            }
        """)

        layout = QVBoxLayout(rewards_widget)

        title = QLabel("Reconocimientos")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setStyleSheet('''
            color: white;
            background-color: #232c38;
            padding: 15px 10px;
            border-radius: 10px;
            margin-bottom: 15px;
        ''')

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setMinimumHeight(180)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:horizontal {
                height: 8px;
                background: #F5F6FA;
            }
            QScrollBar::handle:horizontal {
                background-color: #B3B3B3;
                border-radius: 4px;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
            }
        """)

        rewards_container = QWidget()
        rewards_container.setMinimumHeight(130)  # altura
        rewards_container.setStyleSheet("background: transparent;")
        self.rewards_layout = QHBoxLayout(rewards_container)
        self.rewards_layout.setSpacing(15)
        self.rewards_layout.setContentsMargins(0, 0, 0, 0)
        self.rewards_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        scroll.setWidget(rewards_container)

        layout.addWidget(title)
        layout.addWidget(scroll)

        return rewards_widget

    def create_reward_card(self, text, reward_type):
        card = QFrame()
        card.setFixedSize(300, 130)

        if reward_type == 'title':
            style = """
                QFrame {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #3498db, stop:1 #2980b9);
                    border-radius: 10px;
                }
            """
            icon_path = "resources/images/levels/corona.png"
            category = "Título"
        elif reward_type == 'badge':
            style = """
                QFrame {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #11d6a2, stop:1 #1ed494);
                    border-radius: 10px;
                }
            """
            icon_path = "resources/images/levels/medalla-de-oro.png"
            category = "Insignia"
        else:  # features
            style = """
                QFrame {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #2ecc71, stop:1 #27ae60);
                    border-radius: 10px;
                }
            """
            icon_path = "resources/images/levels/llave_inglesa.png"
            category = "Característica"

        card.setStyleSheet(style)

        # Crear layout horizontal para el icono y contenido
        main_layout = QHBoxLayout(card)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(20)  # spaciado entre icono y contenido

        # Icono/Imagen
        icon_label = QLabel()
        pixmap = QPixmap(icon_path)
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(
                40, 40,  #  tamaño del icono
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            icon_label.setPixmap(scaled_pixmap)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setFixedSize(40, 40)  # contenedor del icono
        icon_label.setStyleSheet("background: transparent; border: none;")

        # Contenedor vertical para categoría y texto
        content_layout = QVBoxLayout()
        content_layout.setSpacing(8)  # espacio entre categoría y texto
        content_layout.setContentsMargins(0, 5, 0, 5)  #  márgenes verticales

        # Categoría
        category_label = QLabel(category)
        category_label.setFont(QFont("Arial", 10))
        category_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        category_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        category_label.setStyleSheet("""
            color: rgba(255, 255, 255, 0.8);
            background: transparent;
            padding: 2px 0px;
        """)
        category_label.setFixedHeight(20)

        # Texto principal
        text_label = QLabel(text)
        text_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        text_label.setWordWrap(True)
        text_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        text_label.setStyleSheet("color: white; background: transparent;")
        text_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        #  widgets al layout de contenido
        content_layout.addWidget(category_label)
        content_layout.addWidget(text_label)

        # layout principal
        main_layout.addWidget(icon_label)
        main_layout.addLayout(content_layout, 1)

        return card

    def create_progress_chart(self):
        chart_widget = QFrame()
        chart_widget.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
                border: 1px solid #e0e0e0;
            }
        """)
        chart_widget.setMinimumHeight(500)

        layout = QVBoxLayout(chart_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel("Progreso de XP")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setStyleSheet('''
            color: white;
            background-color: #232c38;
            padding: 15px 10px;
            border-radius: 10px;
            margin-bottom: 15px;
        ''')

        # Crear scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:horizontal {
                height: 8px;
                background: #F5F6FA;
            }
            QScrollBar::handle:horizontal {
                background-color: #B3B3B3;
                border-radius: 4px;
            }
        """)

        # Widget contenedor para el chart
        chart_container = QWidget()
        chart_container.setMinimumWidth(800)  # Ancho mínimo del gráfico
        chart_layout = QVBoxLayout(chart_container)
        chart_layout.setContentsMargins(20, 10, 20, 10)
        chart_container.setStyleSheet("background: transparent;")

        self.chart_view = QChartView()
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        chart_layout.addWidget(self.chart_view)

        scroll.setWidget(chart_container)

        layout.addWidget(title)
        layout.addWidget(scroll)

        return chart_widget

    def load_user_stats(self):
        if not self.current_progress:
            return

        # Obtener progreso de nivel
        level_progress = self.level_system.get_level_progress(
            self.current_progress.get('total_xp', 0)
        )

        # Actualizar UI
        self.level_label.setText(f"Nivel {level_progress.level}")
        difficulty_info = self.level_system.get_difficulty_info()
        self.difficulty_label.setText(f"Modo: {difficulty_info['name']}")

        self.update_stats(level_progress)
        self.update_rewards(level_progress.level)
        self.update_progress_chart()

    def update_stats(self, level_progress: LevelProgress):
        """Actualiza las estadísticas mostradas"""
        stats = {
            'total_xp': f"{self.current_progress.get('total_xp', 0):,} XP",
            'exams_completed': str(self.current_progress.get('exams_completed', 0)),
            'accuracy': (f"{self.current_progress.get('average_accuracy', 0):.1f}% "
                       f"(Último: {self.current_progress.get('last_accuracy', 0):.1f}%)"),
            'xp_to_next': f"{level_progress.xp_for_next - level_progress.current_xp:,} XP"
        }

        for key, value in stats.items():
            card = self.stat_labels[key]
            value_label = card.findChild(QLabel, "value_label")
            if value_label:
                value_label.setText(value)

    def update_rewards(self, level):
        # Ñimpiar recompensas actuales
        while self.rewards_layout.count():
            item = self.rewards_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Obtener recompensas del nivel actual
        rewards = self.level_system.get_level_rewards(level)

        # Mostrar títulos
        if rewards.titles:
            for title in rewards.titles:
                card = self.create_reward_card(title, 'title')
                self.rewards_layout.addWidget(card)

        # Mostrar insignias
        if rewards.badges:
            for badge in rewards.badges:
                card = self.create_reward_card(badge, 'badge')
                self.rewards_layout.addWidget(card)

        # Mostrar características
        if rewards.features:
            for feature in rewards.features:
                card = self.create_reward_card(feature, 'feature')
                self.rewards_layout.addWidget(card)

        # Agregar un spacer al final
        self.rewards_layout.addStretch()

    def update_progress_chart(self):
        series = QLineSeries()
        today = datetime.now()
        data_points = []
        max_xp = 0

        # Obtener datos de XP diaria
        for i in range(7):
            date = today - timedelta(days=i)
            date_str = date.strftime("%Y-%m-%d")
            xp = self.current_progress.get(f'daily_xp_{date_str}', 0)
            data_points.append((6 - i, xp))
            max_xp = max(max_xp, xp)

        for x, y in data_points:
            series.append(x, y)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("XP Ganada por Día")

        # Configurar eje X
        axis_x = QValueAxis()
        axis_x.setRange(0, 6)
        axis_x.setTickCount(7)
        axis_x.setLabelFormat("%d")
        axis_x.setTitleText("Últimos 7 días")
        axis_x.setLabelsAngle(-45)

        # Configurar eje Y
        axis_y = QValueAxis()
        max_y = max_xp if max_xp > 0 else 100
        axis_y.setRange(0, max_y * 1.1)
        axis_y.setLabelFormat("%d XP")
        axis_y.setTitleText("Experiencia")

        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_x)
        series.attachAxis(axis_y)

        chart.setBackgroundVisible(False)
        chart.setTheme(QChart.ChartTheme.ChartThemeLight)
        chart.legend().hide()

        self.chart_view.setChart(chart)

    def refresh_stats(self):
        """Refresca todas las estadísticas"""
        # Recargar el progreso actual
        self.current_progress = self.progress_persistence.load_progress('current_user')

        # Recargar dificultad por si cambió
        difficulty = self.current_progress.get('difficulty', 'normal')
        self.level_system = ImprovedLevelSystem(difficulty=difficulty)

        # Recargar todas las estadísticas
        self.load_user_stats()