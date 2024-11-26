class ExamScore:
    """Clase para manejar puntajes de exámenes."""

    def __init__(self, correct_answers: int, total_questions: int, xp_earned: int):
        self.correct_answers = correct_answers
        self.total_questions = total_questions
        self.xp_earned = xp_earned

    def get_accuracy(self) -> float:
        """Calcula y retorna el porcentaje de precisión"""
        if self.total_questions == 0:
            return 0.0
        return (self.correct_answers / self.total_questions) * 100


    """Sobrecarga de operadores
    
    - Controlamos los tipos de datos de la instancia y el otro objeto con isinstance y devolvemos NotImplemented si no son compatibles.
    """

    def __iadd__(self, value: int):
        """Incrementa el numero de respuestas correctas"""
        if isinstance(value, int):
            self.correct_answers += value
            return self
        return NotImplemented

    def __mul__(self, multiplier: float):
        """Multiplica la XP ganada por un factor"""
        if isinstance(multiplier, (int, float)):
            return ExamScore(
                correct_answers=self.correct_answers,
                total_questions=self.total_questions,
                xp_earned=int(self.xp_earned * multiplier)
            )
        return NotImplemented

    def __gt__(self, other):
        """Mayor que - compara la precisión"""
        if isinstance(other, ExamScore):
            return (self.correct_answers / self.total_questions) > (other.correct_answers / other.total_questions)
        return NotImplemented

    def __eq__(self, other) -> bool:
        """Compara dos puntajes de exámenes"""
        if not isinstance(other, ExamScore):
            return NotImplemented
        return (self.correct_answers / self.total_questions) == (other.correct_answers / other.total_questions)

    def __lt__(self, other) -> bool:
        """Compara dos puntajes de exámenes"""
        if not isinstance(other, ExamScore):
            return NotImplemented
        return (self.correct_answers / self.total_questions) < (other.correct_answers / other.total_questions)

    def __str__(self) -> str:
        accuracy = self.get_accuracy()
        return f"Puntuación: {self.correct_answers}/{self.total_questions} ({accuracy:.1f}%) - XP: {self.xp_earned}"
