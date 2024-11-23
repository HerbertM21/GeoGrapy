from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QFrame, QScrollArea, QGridLayout, QSpacerItem, QSizePolicy)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor, QPainter, QPen
from PyQt6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis  # Cambio aquí
from datetime import datetime, timedelta
import json
from pathlib import Path
from src.services.level_system import ImprovedLevelSystem, JsonProgressPersistence, LevelProgress
from src.utils.constants import ICON_PATH


class StatsPage(QWidget):
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
        self.level_label.setFont(QFont("Arial", 18))
        self.level_label.setStyleSheet("""
            color: #34495e;
            background-color: #e8f4f8;
            padding: 5px 15px;
            border-radius: 10px;
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

        # Lista de estadisticas a mostrar
        self.stat_labels = {
            'total_xp': self.create_stat_card("XP Total", "0"),
            'exams_completed': self.create_stat_card("Exámenes Completados", "0"),
            'accuracy': self.create_stat_card("Precisión Media", "0%"),
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
        title_label.setFont(QFont("Arial", 12))
        title_label.setStyleSheet("color: #7f8c8d;")

        value_label = QLabel(value)
        value_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        value_label.setStyleSheet("color: #2c3e50;")
        value_label.setObjectName("value_label")  # PARA poder actualizarlo después

        layout.addWidget(title_label)
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

        title = QLabel("Recompensas Desbloqueadas")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")

        self.rewards_layout = QVBoxLayout()
        self.rewards_layout.setSpacing(10)

        layout.addWidget(title)
        layout.addLayout(self.rewards_layout)

        return rewards_widget

    def create_reward_label(self, text, reward_type):
        label = QLabel(text)
        if reward_type == 'title':
            style = """
                background-color: #e8f6ff;
                color: #2980b9;
            """
            icon = "👑 "
        elif reward_type == 'badge':
            style = """
                background-color: #fff7e6;
                color: #f39c12;
            """
            icon = "🏅 "
        else:  # las features
            style = """
                background-color: #e8f8f5;
                color: #27ae60;
            """
            icon = "⭐ "

        label.setText(f"{icon}{text}")
        label.setStyleSheet(f"""
            QLabel {{
                {style}
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }}
        """)
        return label

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
        chart_widget.setMinimumHeight(300)

        layout = QVBoxLayout(chart_widget)

        title = QLabel("Progreso de XP")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50;")

        self.chart_view = QChartView()
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        layout.addWidget(title)
        layout.addWidget(self.chart_view)

        return chart_widget

    def load_user_stats(self):
        if not self.current_progress:
            return

        # Obtener nivel y progreso actual
        total_xp = self.current_progress.get('total_xp', 0)
        level_progress = self.level_system.get_level_progress(total_xp)

        # Actualizar etiquetas de nivel y dificultad
        self.level_label.setText(f"Nivel {level_progress.level}")
        difficulty_info = self.level_system.get_difficulty_info()
        self.difficulty_label.setText(f"Modo: {difficulty_info['name']}")

        # Actualizar estadisticas
        self.update_stats(level_progress)

        # Actualizar recompensas
        self.update_rewards(level_progress.level)

        # Actualizar gráfico de progreso
        self.update_progress_chart()

    def update_stats(self, level_progress: LevelProgress):
        stats = {
            'total_xp': f"{level_progress.total_xp:,} XP",
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
        # Limpiar recompensas actuales
        while self.rewards_layout.count():
            item = self.rewards_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Obtener recompensas del nivel actual
        rewards = self.level_system.get_level_rewards(level)

        # Mostrar títulos
        if rewards.titles:
            for title in rewards.titles:
                label = self.create_reward_label(title, 'title')
                self.rewards_layout.addWidget(label)

        # Mostrar insignias
        if rewards.badges:
            for badge in rewards.badges:
                label = self.create_reward_label(badge, 'badge')
                self.rewards_layout.addWidget(label)

        # Mostrar caracteristicas
        if rewards.features:
            for feature in rewards.features:
                label = self.create_reward_label(feature, 'feature')
                self.rewards_layout.addWidget(label)

    def update_progress_chart(self):
        # Crear serie de datos de XP
        series = QLineSeries()

        # Obtener historial de XP de los últimos 7 dias
        today = datetime.now()
        data_points = []
        max_xp = 0

        for i in range(7):
            date = today - timedelta(days=i)
            date_str = date.strftime("%Y-%m-%d")
            xp = self.current_progress.get(f'daily_xp_{date_str}', 0)
            data_points.append((6 - i, xp))  # 6-i para que los días vayan de izquierda a derecha
            max_xp = max(max_xp, xp)

        # Añadir puntos a la serie
        for x, y in data_points:
            series.append(x, y)

        # Crear y configurar el gráfico
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("XP Ganada por Día")

        # Configurar ejes
        axis_x = QValueAxis()
        axis_x.setRange(0, 6)
        axis_x.setTickCount(7)
        axis_x.setLabelFormat("%d")

        axis_y = QValueAxis()
        max_y = max_xp if max_xp > 0 else 100
        axis_y.setRange(0, max_y * 1.1)

        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_x)
        series.attachAxis(axis_y)

        # Aplicar estilos
        chart.setBackgroundVisible(False)
        chart.setTheme(QChart.ChartTheme.ChartThemeLight)

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