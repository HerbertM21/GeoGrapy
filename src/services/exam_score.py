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

    def __add__(self, other):
        if isinstance(other, ExamScore):
            return ExamScore(
                correct_answers=self.correct_answers + other.correct_answers,
                total_questions=self.total_questions + other.total_questions,
                xp_earned=self.xp_earned + other.xp_earned
            )
        return NotImplemented

    def __eq__(self, other) -> bool:
        if not isinstance(other, ExamScore):
            return NotImplemented
        return (self.correct_answers / self.total_questions) == (other.correct_answers / other.total_questions)

    def __lt__(self, other) -> bool:
        if not isinstance(other, ExamScore):
            return NotImplemented
        return (self.correct_answers / self.total_questions) < (other.correct_answers / other.total_questions)

    def __str__(self) -> str:
        accuracy = self.get_accuracy()
        return f"Puntuación: {self.correct_answers}/{self.total_questions} ({accuracy:.1f}%) - XP: {self.xp_earned}"