from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                          QPushButton, QLabel, QProgressBar, QMessageBox, QScrollArea)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QSize
from PyQt6.QtGui import QPixmap, QFont
from src.utils.constants import IMAGE_PATH
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
            # Usar directorio por defecto si no se proporciona
            # ~/.geograpy/progress
            save_dir = Path.home() / '.geograpy' / 'progress'
            self.progress_persistence = JsonProgressPersistence(save_dir)
        else:
            self.progress_persistence = progress_persistence

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
        self.progress.setMinimumHeight(30)
        main_layout.addWidget(self.progress)

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
                            background-color: #ddd;
                            text-align: center;
                            border-radius: 15px;
                        }
                        QProgressBar::chunk {
                            background-color: #3498db;
                            border-radius: 15px;
                        }
                    """)

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
            self.progress.setValue(self.current_question + 1)
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
        # Calcular resultados básicos
        total_questions = len(self.questions)

        # Obtener recompensas usando el sistema de niveles
        rewards = self.level_system.calculate_exam_rewards(
            exam_base_xp=self.exam_data['xp'],
            correct_answers=self.correct_answers,
            total_questions=total_questions
        )

        # Cargar progreso actual y calcular nuevo nivel
        current_progress = self.progress_persistence.load_progress('current_user')
        old_total_xp = current_progress.get('total_xp', 0)
        new_total_xp = old_total_xp + rewards.total_xp

        old_level_progress = self.level_system.get_level_progress(old_total_xp)
        new_level_progress = self.level_system.get_level_progress(new_total_xp)

        # Verificar si subió de nivel
        level_up_message = ""
        if new_level_progress.level > old_level_progress.level:
            new_rewards = self.level_system.get_level_rewards(new_level_progress.level)
            level_up_message = self._format_level_up_message(
                old_level_progress.level,
                new_level_progress.level,
                new_rewards
            )

        # Crear mensaje de resultados detallado
        result_message = f"""
                ¡Examen completado!

                Resultados:
                ✓ Respuestas correctas: {self.correct_answers}/{total_questions}
                ✓ Precisión: {rewards.accuracy:.1f}%

                Experiencia ganada:
                → XP Base: {rewards.base_xp}
                → Bonus por completar: +{rewards.completion_bonus}
                → Bonus por precisión: +{rewards.accuracy_bonus}
                ━━━━━━━━━━━━━━━━━━━━━━━━
                Total XP ganada: {rewards.total_xp}

                Nivel actual: {new_level_progress.level}
                Progreso: {new_level_progress.current_xp}/{new_level_progress.xp_for_next} XP
                ({new_level_progress.progress_percentage:.1f}%)

                {level_up_message}

                {self._get_performance_message(rewards.accuracy)}
                """

        # Guardar progreso
        progress_data = {
            'total_xp': new_total_xp,
            'level': new_level_progress.level,
            'last_exam_date': str(datetime.now()),
            'exams_completed': current_progress.get('exams_completed', 0) + 1
        }
        self.progress_persistence.save_progress('current_user', progress_data)

        # Mostrar resultados
        results = QMessageBox(self)
        results.setWindowTitle("Resultados del Examen")
        results.setText(result_message)
        results.setIcon(QMessageBox.Icon.Information)

        menu_button = results.addButton("Volver al Menú", QMessageBox.ButtonRole.AcceptRole)
        retry_button = results.addButton("Reintentar", QMessageBox.ButtonRole.RejectRole)

        exam_results = {
            'category': self.exam_data.get('category', ''),
            'title': self.exam_data['title'],
            'xp_earned': rewards.total_xp,
            'correct_answers': self.correct_answers,
            'total_questions': total_questions,
            'accuracy': rewards.accuracy,
            'new_level': new_level_progress.level,
            'old_level': old_level_progress.level
        }

        result = results.exec()
        clicked_button = results.clickedButton()

        if clicked_button == menu_button:
            self.exam_completed.emit(exam_results)
            self.close()
        elif clicked_button == retry_button:
            self.reset_exam()

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

        # Mostrar mensaje de feedback
        feedback = QMessageBox(self)
        feedback.setWindowTitle("Resultado")

        # Explicacion del resultadio
        if is_correct:
            feedback.setText(f"¡Correcto! 🎉\n\n{explanation}")
            feedback.setIcon(QMessageBox.Icon.Information)
        else:
            feedback.setText(f"Incorrecto 😔\n\n{explanation}")
            feedback.setIcon(QMessageBox.Icon.Warning)

        # Configurar tiempo de visualización y siguiente pregunta
        QTimer.singleShot(2000, feedback.close)
        feedback.show()
        QTimer.singleShot(2500, self.next_question)

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