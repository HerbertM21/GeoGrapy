from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                          QPushButton, QLabel, QProgressBar, QScrollArea, QFrame)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QPixmap, QFont
from src.utils.constants import IMAGE_PATH
from src.services.exam_score import ExamScore
from src.services.level_system import AbstractLevelSystem, ImprovedLevelSystem, JsonProgressPersistence
from pathlib import Path
import random
from datetime import datetime


class ExamWindow(QMainWindow):
    exam_completed = pyqtSignal(dict)

    def __init__(self, exam_data, level_system: AbstractLevelSystem = None,
                 progress_persistence=None):
        super().__init__()
        self.exam_data = exam_data
        self.current_question = 0
        self.correct_answers = 0
        self.questions = exam_data['questions']

        # Inicializar sistema de niveles y persistencia
        self.level_system = level_system or ImprovedLevelSystem()
        if progress_persistence is None:
            save_dir = Path.home() / '.geograpy' / 'progress'
            self.progress_persistence = JsonProgressPersistence(save_dir)
        else:
            self.progress_persistence = progress_persistence

        # Cargar último resultado del usuario para este examen
        self.current_progress = self.progress_persistence.load_progress('current_user')
        self.last_exam_score = None
        if self.current_progress:
            last_correct = self.current_progress.get('last_exam_score', 0)
            last_total = self.current_progress.get('last_exam_total', 1)
            last_xp = self.current_progress.get('last_exam_xp', 0)
            self.last_exam_score = ExamScore(last_correct, last_total, last_xp)

        random.shuffle(self.questions)
        self.setWindowTitle(exam_data['title'])

        # Calcular el tamaño de la ventana basado en la pantalla
        screen = QApplication.primaryScreen().availableGeometry()
        window_width = min(600, int(screen.width() * 0.8))
        window_height = min(800, int(screen.height() * 0.8))
        self.setMinimumSize(350, 500)
        self.resize(window_width, window_height)

        # Centrar la ventana
        x = (screen.width() - window_width) // 2
        y = (screen.height() - window_height) // 2
        self.move(x, y)

        self.setup_ui()
        self.show_question()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
                        QScrollArea {
                            border: none;
                            background: transparent;
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

        scroll_content = QWidget()
        scroll_content.setStyleSheet("background: transparent;")
        self.content_layout = QVBoxLayout(scroll_content)
        self.content_layout.setSpacing(15)

        self.progress = QProgressBar()
        self.progress.setRange(0, len(self.questions))
        self.progress.setValue(0)
        self.progress.setMinimumHeight(20)

        self.question_label = QLabel()
        self.question_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.question_label.setWordWrap(True)
        self.question_label.setStyleSheet("""
                        QLabel {
                            color: #2c3e50;
                            background-color: white;
                            padding: 15px;
                            border: 2px solid #3498db;
                            border-radius: 10px;
                            margin: 10px 0;
                        }
                    """)
        self.content_layout.addWidget(self.question_label)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.content_layout.addWidget(self.image_label)

        self.options_widget = QWidget()
        self.options_widget.setStyleSheet("background: transparent;")
        self.options_layout = QVBoxLayout(self.options_widget)
        self.options_layout.setSpacing(10)
        self.content_layout.addWidget(self.options_widget)

        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)

        central_widget.setStyleSheet("""
                        QWidget {
                            background-color: #f5f6fa;
                        }
                    """)

        self.setStyleSheet("""
                        QMainWindow {
                            background-color: #f5f6fa;
                        }
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

        main_layout.addWidget(self.progress)

    def get_image_path(self, image_name: str) -> str:
        possible_paths = [
            IMAGE_PATH / 'countries' / image_name,
            IMAGE_PATH / 'capitals' / image_name,
        ]

        for path in possible_paths:
            if path.exists():
                return str(path)

        return image_name

    def show_question(self):
        if self.current_question < len(self.questions):
            question = self.questions[self.current_question]
            self.progress.setValue(self.current_question)
            self.question_label.setText(question['question'])

            image_path = self.get_image_path(question['image'])
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                max_img_size = min(self.width() * 0.6, 300)
                scaled_pixmap = pixmap.scaled(
                    int(max_img_size),
                    int(max_img_size),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.image_label.setPixmap(scaled_pixmap)

            while self.options_layout.count():
                child = self.options_layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

            options = question['options'].copy()
            random.shuffle(options)

            for option in options:
                button = QPushButton(option)
                button.setMinimumHeight(50)
                button.setMinimumWidth(15)  # Ajusta el ancho minimo
                button.clicked.connect(lambda checked, opt=option: self.check_answer(opt))
                button.setStyleSheet("""
                                QPushButton {
                                    background-color: white;
                                    border: 2px solid #3498db;
                                    color: #3498db;
                                    border-radius: 25px;
                                    padding: 15px;
                                    font-size: 16px;
                                    font-weight: bold;
                                    margin: 5px;
                                }
                                QPushButton:hover {
                                    background-color: #3498db;
                                    color: white;
                                }
                                QPushButton:disabled {
                                    background-color: white;
                                    border: 2px solid #bdc3c7;
                                    color: #bdc3c7;
                                }
                            """)
                self.options_layout.addWidget(button)

    def show_results(self):
        # Crear objeto ExamScore para el intento actual
        current_score = ExamScore(
            correct_answers=self.correct_answers,
            total_questions=len(self.questions),
            xp_earned=self.exam_data['xp']
        )

        # Comparar con el último intento si existe
        comparison_message = ""
        if self.last_exam_score:
            if current_score > self.last_exam_score:
                comparison_message = "¡Has mejorado desde tu último intento! 🎉"
            elif current_score == self.last_exam_score:
                comparison_message = "Mantuviste el mismo nivel que tu último intento 🎯"
            else:
                comparison_message = "Sigue practicando para superar tu último intento 💪"

        # Calcular recompensas usando el sistema de niveles
        rewards = self.level_system.calculate_exam_rewards(
            exam_base_xp=current_score.xp_earned,
            correct_answers=current_score.correct_answers,
            total_questions=current_score.total_questions
        )

        # Cargar y actualizar progreso
        old_total_xp = self.current_progress.get('total_xp', 0)
        new_total_xp = old_total_xp + rewards.total_xp

        old_level_progress = self.level_system.get_level_progress(old_total_xp)
        new_level_progress = self.level_system.get_level_progress(new_total_xp)

        # Calcular nueva precisión media usando ExamScore
        total_exams = self.current_progress.get('exams_completed', 0)
        old_accuracy = self.current_progress.get('average_accuracy', 0)

        if total_exams == 0:
            new_accuracy = current_score.get_accuracy()
        else:
            new_accuracy = (old_accuracy * total_exams + current_score.get_accuracy()) / (total_exams + 1)

        # Verificar subida de nivel
        level_up_message = ""
        if new_level_progress.level > old_level_progress.level:
            new_rewards = self.level_system.get_level_rewards(new_level_progress.level)
            level_up_message = self._format_level_up_message(
                old_level_progress.level,
                new_level_progress.level,
                new_rewards
            )

        # Guardar progreso actualizado
        progress_data = {
            'total_xp': new_total_xp,
            'level': new_level_progress.level,
            'last_exam_date': str(datetime.now()),
            'exams_completed': total_exams + 1,
            'average_accuracy': new_accuracy,
            'last_accuracy': current_score.get_accuracy(),
            'last_exam_score': current_score.correct_answers,
            'last_exam_total': current_score.total_questions,
            'last_exam_xp': current_score.xp_earned,
            'difficulty': self.current_progress.get('difficulty', 'normal')
        }

        # Actualizar el progreso manteniendo datos existentes
        if self.current_progress:
            today_date = datetime.now().strftime("%Y-%m-%d")
            daily_xp_key = f'daily_xp_{today_date}'
            self.current_progress[daily_xp_key] = self.current_progress.get(daily_xp_key, 0) + rewards.total_xp
            self.current_progress.update(progress_data)
            progress_data = self.current_progress

        # Preparar datos para la ventana de resultados
        results_data = {
            'correct_answers': current_score.correct_answers,
            'total_questions': current_score.total_questions,
            'accuracy': current_score.get_accuracy(),
            'rewards': rewards,
            'new_level': new_level_progress.level,
            'progress': new_level_progress,
            'performance_message': self._get_performance_message(current_score.get_accuracy()),
            'comparison_message': comparison_message
        }

        # Guardar progreso
        self.progress_persistence.save_progress('current_user', progress_data)

        # Emitir resultados
        exam_results = {
            'category': self.exam_data.get('category', ''),
            'title': self.exam_data['title'],
            'xp_earned': rewards.total_xp,
            'correct_answers': current_score.correct_answers,
            'total_questions': current_score.total_questions,
            'accuracy': current_score.get_accuracy(),
            'new_level': new_level_progress.level,
            'old_level': old_level_progress.level
        }

        if level_up_message:
            results_data['level_up_message'] = level_up_message

        # Mostrar ventana de resultados
        results_window = ResultsWindow(results_data, self)
        results_window.closed.connect(lambda: self.handle_results_closed(exam_results))
        results_window.show()

    def handle_results_closed(self, exam_results):
        """Maneja el cierre de la ventana de resultados"""
        self.exam_completed.emit(exam_results)
        self.close()

    def _format_level_up_message(self, old_level: int, new_level: int, rewards) -> str:
        message = f"\n¡SUBISTE DE NIVEL!\n{old_level} → {new_level}\n"

        if rewards.titles:
            message += "\nNuevos títulos desbloqueados:"
            for title in rewards.titles:
                message += f"\n→ {title}"

        if rewards.badges:
            message += "\n\nNuevas insignias desbloqueadas:"
            for badge in rewards.badges:
                message += f"\n→ {badge}"

        if rewards.features:
            message += "\n\nNuevas características desbloqueadas:"
            for feature in rewards.features:
                message += f"\n→ {feature}"

        return message

    @staticmethod
    def _get_performance_message(accuracy: float) -> str:
        if accuracy >= 90:
            return "¡Excelente trabajo! 🌟\n¡Eres un verdadero maestro de la geografía!"
        elif accuracy >= 75:
            return "¡Muy buen trabajo! 🎉\nEstás en el camino correcto."
        elif accuracy >= 60:
            return "¡Buen intento! 👍\nSigue practicando para mejorar."
        else:
            return "No te desanimes 💪\nCada intento es una oportunidad para aprender."

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.image_label.pixmap():
            max_img_size = min(self.width() * 0.6, 300)
            current_pixmap = self.image_label.pixmap()
            scaled_pixmap = current_pixmap.scaled(
                int(max_img_size),
                int(max_img_size),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)

    def check_answer(self, selected_option):
        current_question = self.questions[self.current_question]
        correct_answer = current_question['correct']

        for i in range(self.options_layout.count()):
            self.options_layout.itemAt(i).widget().setEnabled(False)

        if selected_option == correct_answer:
            self.correct_answers += 1
            self.show_feedback(True, current_question['explanation'])
        else:
            self.show_feedback(False, current_question['explanation'])

    def show_feedback(self, is_correct, explanation):
        """Muestra el feedback para la respuesta seleccionada"""
        # Actualizar estilos de los botones
        for i in range(self.options_layout.count()):
            button = self.options_layout.itemAt(i).widget()
            if button.text() == self.questions[self.current_question]['correct']:
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #2ecc71;
                        color: white;
                        border: 2px solid #2ecc71;
                        border-radius: 25px;
                        padding: 15px;
                        font-size: 16px;
                        font-weight: bold;
                        margin: 5px;
                    }
                """)
            elif not is_correct and button.isEnabled() == False:
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #e74c3c;
                        color: white;
                        border: 2px solid #e74c3c;
                        border-radius: 25px;
                        padding: 15px;
                        font-size: 16px;
                        font-weight: bold;
                        margin: 5px;
                    }
                """)

        # Avanzar a la siguiente pregunta después de un breve delay
        QTimer.singleShot(1000, self.next_question)

    def next_question(self):
        """Avanza a la siguiente pregunta o muestra resultados si es la última"""
        self.current_question += 1
        if self.current_question < len(self.questions):
            self.show_question()
        else:
            self.show_results()

    def reset_exam(self):
        """Reinicia el examen mezclando las preguntas"""
        self.current_question = 0
        self.correct_answers = 0
        random.shuffle(self.questions)
        self.progress.setValue(0)
        self.show_question()

    def closeEvent(self, event):
        """Maneja el evento de cierre de la ventana"""

        # Guardar progreso actual antes de cerrar
        current_progress = self.progress_persistence.load_progress('current_user')
        current_progress['last_session'] = str(datetime.now())
        self.progress_persistence.save_progress('current_user', current_progress)

        event.accept()


class ResultsWindow(QMainWindow):
    closed = pyqtSignal()

    def __init__(self, results_data, parent=None):
        super().__init__(parent)
        self.setup_ui(results_data)

        # Centrar la ventana
        screen = QApplication.primaryScreen().availableGeometry()
        window_width = 400
        window_height = 600
        self.setMinimumSize(500, 700)
        self.resize(window_width, window_height)

        # Centrar en la pantalla
        x = (screen.width() - window_width) // 2
        y = (screen.height() - window_height) // 2
        self.move(x, y)

        self.setWindowTitle("Resultados")

    def setup_ui(self, results_data):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Título con emoji
        title = "¡Excelente! 🌟" if results_data['accuracy'] >= 75 else "¡Buen intento! 💪"
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #2c3e50;")
        layout.addWidget(title_label)

        # Mensaje de comparación
        if 'comparison_message' in results_data and results_data['comparison_message']:
            comparison_label = QLabel(results_data['comparison_message'])
            comparison_label.setFont(QFont("Arial", 14))
            comparison_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            comparison_label.setWordWrap(True)
            comparison_label.setStyleSheet("""
                QLabel {
                    color: #2c3e50;
                    background-color: rgba(52, 152, 219, 0.1);
                    padding: 15px;
                    border-radius: 10px;
                    margin: 10px 0;
                }
            """)
            layout.addWidget(comparison_label)

        # Contenedor principal
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)

        # Resultados del examen
        results_frame = self.create_section(
            "Resultados",
            [f"{results_data['correct_answers']}/{results_data['total_questions']} correctas",
             f"{results_data['accuracy']:.0f}% precisión"],
            "#3498db"
        )
        content_layout.addWidget(results_frame)

        # XP ganada
        xp_frame = self.create_section(
            "XP Ganada",
            [f"+{results_data['rewards'].total_xp} XP"],
            "#27ae60"
        )
        content_layout.addWidget(xp_frame)

        # Nivel (solo si subio de nivel)
        if results_data.get('level_up_message'):
            level_frame = self.create_section(
                "¡Subiste de nivel!",
                [f"Nivel {results_data['new_level']}"],
                "#8e44ad"
            )
            content_layout.addWidget(level_frame)

        layout.addWidget(content_widget)

        # Botones
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        retry_button = QPushButton("Reintentar")
        menu_button = QPushButton("Continuar")

        for button in [retry_button, menu_button]:
            button.setMinimumHeight(40)
            button.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border: none;
                    border-radius: 20px;
                    padding: 10px 20px;
                    font-weight: bold;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
            """)

        button_layout.addWidget(retry_button)
        button_layout.addWidget(menu_button)

        menu_button.clicked.connect(self.handle_menu)
        retry_button.clicked.connect(self.handle_retry)

        layout.addLayout(button_layout)

    def create_section(self, title, items, color):
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-radius: 10px;
                padding: 15px;
            }}
        """)

        layout = QVBoxLayout(frame)
        layout.setSpacing(5)

        # Título de la sección
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title_label.setStyleSheet(f"color: {color};")
        layout.addWidget(title_label)

        # Contenido
        for item in items:
            item_label = QLabel(item)
            item_label.setFont(QFont("Arial", 16))
            item_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            item_label.setStyleSheet("color: #2c3e50;")
            layout.addWidget(item_label)

        return frame

    def handle_menu(self):
        """Maneja el botón de continuar"""
        self.closed.emit()
        self.close()

    def handle_retry(self):
        """Maneja el botón de reintentar"""
        self.parent().reset_exam()
        self.close()