from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QProgressBar, QMessageBox, QScrollArea)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QSize
from PyQt6.QtGui import QPixmap, QFont
from src.utils.constants import IMAGE_PATH
from pathlib import Path
import random


class ExamWindow(QMainWindow):
    exam_completed = pyqtSignal(dict)

    def __init__(self, exam_data):
        super().__init__()
        self.exam_data = exam_data
        self.current_question = 0
        self.correct_answers = 0
        self.questions = exam_data['questions']
        random.shuffle(self.questions)

        self.setWindowTitle(exam_data['title'])

        # Calcular el tamaño de la ventana basado en la pantalla
        screen = QApplication.primaryScreen().availableGeometry()
        window_width = min(600, int(screen.width() * 0.8))
        window_height = min(800, int(screen.height() * 0.8))
        self.setMinimumSize(350, 500)  # Tamaño mínimo para asegurar usabilidad
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

        # Layout principal con scroll
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Scroll area para contenido
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

        # Contenedor scrolleable
        scroll_content = QWidget()
        scroll_content.setStyleSheet("background: transparent;")
        self.content_layout = QVBoxLayout(scroll_content)
        self.content_layout.setSpacing(15)

        # Barra de progreso
        self.progress = QProgressBar()
        self.progress.setRange(0, len(self.questions))
        self.progress.setValue(0)
        self.progress.setMinimumHeight(30)
        main_layout.addWidget(self.progress)

        # Área de la pregunta
        self.question_label = QLabel()
        self.question_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
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

        # Imagen
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.content_layout.addWidget(self.image_label)

        # Contenedor para botones de opciones
        self.options_widget = QWidget()
        self.options_widget.setStyleSheet("background: transparent;")
        self.options_layout = QVBoxLayout(self.options_widget)
        self.options_layout.setSpacing(10)
        self.content_layout.addWidget(self.options_widget)

        # Agregar el scroll area al layout principal
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)

        # Estilos generales
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
        """Obtener la ruta completa de la imagen"""
        possible_paths = [
            IMAGE_PATH / 'countries' / image_name,
            IMAGE_PATH / 'capitals' / image_name,
        ]

        for path in possible_paths:
            if path.exists():
                return str(path)

        # Si no se encuentra en las carpetas específicas, devolver la ruta original
        return image_name

    def show_question(self):
        if self.current_question < len(self.questions):
            question = self.questions[self.current_question]

            # Actualizar progreso
            self.progress.setValue(self.current_question + 1)

            # Mostrar pregunta
            self.question_label.setText(question['question'])

            # Mostrar imagen
            image_path = self.get_image_path(question['image'])
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                # Calcular tamaño máximo de imagen basado en el tamaño de la ventana
                max_img_size = min(self.width() * 0.6, 300)
                scaled_pixmap = pixmap.scaled(
                    int(max_img_size),
                    int(max_img_size),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.image_label.setPixmap(scaled_pixmap)

            # Limpiar opciones anteriores
            while self.options_layout.count():
                child = self.options_layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

            # Añadir nuevas opciones
            options = question['options'].copy()
            random.shuffle(options)

            for option in options:
                button = QPushButton(option)
                button.setMinimumHeight(50)
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

    def show_feedback(self, is_correct, explanation):
        # Cambiar color del botón seleccionado
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

        # Mostrar explicación
        feedback = QMessageBox(self)
        feedback.setWindowTitle("Resultado")
        if is_correct:
            feedback.setText("¡Correcto! 🎉\n\n" + explanation)
            feedback.setIcon(QMessageBox.Icon.Information)
        else:
            feedback.setText("Incorrecto 😔\n\n" + explanation)
            feedback.setIcon(QMessageBox.Icon.Warning)

        QTimer.singleShot(2000, feedback.close)
        feedback.show()
        QTimer.singleShot(2500, self.next_question)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Reescalar imagen si existe
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

    def next_question(self):
        self.current_question += 1
        if self.current_question < len(self.questions):
            self.show_question()
        else:
            self.show_results()

    def reset_exam(self):
        self.current_question = 0
        self.correct_answers = 0
        random.shuffle(self.questions)
        self.progress.setValue(0)
        self.show_question()

    def show_results(self):
        score = (self.correct_answers / len(self.questions)) * 100
        xp_earned = int((score / 100) * self.exam_data['xp'])

        result_message = f"""
        ¡Examen completado!

        Respuestas correctas: {self.correct_answers}/{len(self.questions)}
        Puntuación: {score:.1f}%
        XP ganada: {xp_earned}

        {'¡Excelente trabajo! 🌟' if score >= 80 else
        '¡Buen intento! 👍' if score >= 60 else
        'Sigue practicando 💪'}
        """

        results = QMessageBox(self)
        results.setWindowTitle("Resultados del Examen")
        results.setText(result_message)
        results.setIcon(QMessageBox.Icon.Information)

        menu_button = results.addButton("Volver al Menú", QMessageBox.ButtonRole.AcceptRole)
        retry_button = results.addButton("Reintentar", QMessageBox.ButtonRole.RejectRole)

        exam_results = {
            'category': self.exam_data.get('category', ''),
            'title': self.exam_data['title'],
            'score': score,
            'xp_earned': xp_earned,
            'correct_answers': self.correct_answers,
            'total_questions': len(self.questions)
        }

        result = results.exec()
        clicked_button = results.clickedButton()

        if clicked_button == menu_button:
            self.exam_completed.emit(exam_results)
            self.close()
        elif clicked_button == retry_button:
            self.reset_exam()

    def closeEvent(self, event):
        event.accept()