# src/services/level_system.py
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Any
import json
from pathlib import Path

"""
@dataclass lo usamos para definir una clase de datos simple, que solo tiene atributos y no métodos.
- Menos código para escribir
- Más fácil de leer
- Más fácil de mantener
"""


@dataclass
class LevelProgress:
    """Clase para almacenar el progreso del nivel"""
    level: int
    current_xp: int
    xp_for_next: int
    total_xp: int
    progress_percentage: float


@dataclass
class ExamRewards:
    """Clase para almacenar las recompensas del examen"""
    base_xp: int
    completion_bonus: int
    accuracy_bonus: int
    total_xp: int
    accuracy: float


@dataclass
class LevelRewards:
    """Clase para almacenar las recompensas por nivel"""
    titles: List[str]
    badges: List[str]
    features: List[str]


@dataclass
class Difficulty:
    """Configuración de dificultad"""
    name: str
    base_xp: int
    xp_multiplier: float
    max_level: int
    reward_multiplier: float
    exclusive_rewards: bool
    description: str


class AbstractLevelSystem(ABC):
    """Clase base para el sistema de niveles"""

    @property
    @abstractmethod
    def difficulty_name(self) -> str:
        """Retorna el nombre de la dificultad actual"""
        pass

    @abstractmethod
    def calculate_xp_for_level(self, level: int) -> int:
        """Calcula la XP necesaria para un nivel específico"""
        pass

    @abstractmethod
    def get_level_progress(self, total_xp: int) -> LevelProgress:
        """Obtiene el progreso actual del nivel"""
        pass

    @abstractmethod
    def calculate_exam_rewards(self, exam_base_xp: int,
                               correct_answers: int,
                               total_questions: int) -> ExamRewards:
        """Calcula las recompensas del examen"""
        pass

    @abstractmethod
    def get_level_rewards(self, level: int) -> LevelRewards:
        """Obtiene las recompensas por nivel"""
        pass


class AbstractProgressPersistence(ABC):
    """Clase base para la persistencia del progreso"""

    @abstractmethod
    def save_progress(self, user_id: str, progress_data: Dict[str, Any]) -> bool:
        """Guarda el progreso del usuario"""
        pass

    @abstractmethod
    def load_progress(self, user_id: str) -> Dict[str, Any]:
        """Carga el progreso del usuario"""
        pass


class ImprovedLevelSystem(AbstractLevelSystem):
    """Sistema de niveles mejorado con diferentes dificultades

    PROGRESION DE NIVELES:
    - FACIL: Progresa de nivel mucho más rapido, sin embargo:
        - NO SE PUEDE GANAR RECOMPENSAS EXCLUSIVAS
        - SU MULTIPLICADOR DE RECOMPENSAS ES BAJO (1.0)

    - NORMAL: Progresa de nivel de forma equilibrada, con:
        - MULTIPLICADOR DE RECOMPENSAS MEDIO (1.2)
        - NO TIENE RESTRICCIONES DE RECOMPENSAS


    """

    DIFFICULTIES = {
        'easy': Difficulty(
            name="Explorador",
            base_xp=80,
            xp_multiplier=1.3,
            max_level=120,
            reward_multiplier=1.0,
            exclusive_rewards=False,
            description="Progresión más rápida, ideal para explorar y aprender"
        ),
        'normal': Difficulty(
            name="Geógrafo",
            base_xp=100,
            xp_multiplier=1.5,
            max_level=100,
            reward_multiplier=1.2,
            exclusive_rewards=False,
            description="Progresión equilibrada, la experiencia clásica"
        ),
        'hard': Difficulty(
            name="Maestro",
            base_xp=150,
            xp_multiplier=1.8,
            max_level=80,
            reward_multiplier=1.5,
            exclusive_rewards=True,
            description="Progresión desafiante con recompensas exclusivas"
        )
    }

    def __init__(self, difficulty: str = 'normal'):
        if difficulty not in self.DIFFICULTIES:
            difficulty = 'normal'

        self.difficulty = self.DIFFICULTIES[difficulty]
        self._difficulty_name = difficulty  # Cambiado a _difficulty_name

        # Inicializar con los valores de la dificultad seleccionada
        self.base_xp = self.difficulty.base_xp
        self.xp_multiplier = self.difficulty.xp_multiplier
        self.max_level = self.difficulty.max_level

    @property
    def difficulty_name(self) -> str:
        """Retorna el nombre de la dificultad actual"""
        return self._difficulty_name

    def calculate_xp_for_level(self, level: int) -> int:
        if level <= 1:
            return 0
        return int(self.base_xp * (self.xp_multiplier ** (level - 1)))

    def get_level_progress(self, total_xp: int) -> LevelProgress:
        """Calcula el nivel actual y el progreso basado en la XP total"""
        current_level = 1
        accumulated_xp = 0
        xp_for_next = self.calculate_xp_for_level(2)

        # Encontrar el nivel actual
        while accumulated_xp + xp_for_next <= total_xp and current_level < self.max_level:
            accumulated_xp += xp_for_next
            current_level += 1
            xp_for_next = self.calculate_xp_for_level(current_level + 1)

        # Calcular XP en el nivel actual
        xp_in_current_level = total_xp - accumulated_xp
        progress_percentage = (xp_in_current_level / xp_for_next * 100) if xp_for_next > 0 else 100

        return LevelProgress(
            level=current_level,
            current_xp=xp_in_current_level,
            xp_for_next=xp_for_next,
            total_xp=total_xp,
            progress_percentage=progress_percentage
        )

    def get_level_rewards(self, level: int) -> LevelRewards:
        rewards = {
            'titles': [],
            'badges': [],
            'features': []
        }

        # Recompensas base
        if level >= 5:
            rewards['titles'].append(f'{self.difficulty.name} Novato')
            rewards['badges'].append(f'Insignia {self.difficulty_name} 1')
        if level >= 10:
            rewards['titles'].append(f'{self.difficulty.name} Aprendiz')
            rewards['badges'].append(f'Insignia {self.difficulty_name} 2')
        if level >= 25:
            rewards['titles'].append(f'{self.difficulty.name} Experto')
            rewards['badges'].append(f'Insignia {self.difficulty_name} 3')
            rewards['features'].append('custom_profile')
        if level >= 50:
            rewards['titles'].append(f'{self.difficulty.name} Legendario')
            rewards['badges'].append(f'Insignia {self.difficulty_name} 4')
            rewards['features'].append('create_custom_quizzes')

        # Recompensas exclusivas para dificultad difícil
        if self.difficulty.exclusive_rewards:
            if level >= 5:
                rewards['titles'].append('Maestro Intrépido')
                rewards['badges'].append('Corona de Espinas')
            if level >= 15:
                rewards['titles'].append('Sabio de la Geografía')
                rewards['badges'].append('Pergamino de la Sabiduría')
            if level >= 30:
                rewards['titles'].append('Leyenda Geográfica')
                rewards['badges'].append('Globo de Oro')
                rewards['features'].append('custom_theme')
            if level >= 60:
                rewards['titles'].append('Deidad Geográfica')
                rewards['badges'].append('Jardin del Edén')
                rewards['features'].append('create_challenges')

        return LevelRewards(**rewards)

    def calculate_exam_rewards(self, exam_base_xp: int,
                               correct_answers: int,
                               total_questions: int) -> ExamRewards:
        accuracy = correct_answers / total_questions

        # Bonificación base por completar
        completion_bonus = int(exam_base_xp * 0.1)

        # Bonificación por precisión
        accuracy_bonus = 0
        if accuracy >= 0.9:
            accuracy_bonus = int(exam_base_xp * 0.5)
        elif accuracy >= 0.75:
            accuracy_bonus = int(exam_base_xp * 0.25)

        # Aplicar multiplicador de dificultad
        base_xp_earned = int(exam_base_xp * accuracy * self.difficulty.reward_multiplier)
        completion_bonus = int(completion_bonus * self.difficulty.reward_multiplier)
        accuracy_bonus = int(accuracy_bonus * self.difficulty.reward_multiplier)

        total_xp = base_xp_earned + completion_bonus + accuracy_bonus

        return ExamRewards(
            base_xp=base_xp_earned,
            completion_bonus=completion_bonus,
            accuracy_bonus=accuracy_bonus,
            total_xp=total_xp,
            accuracy=accuracy * 100
        )

    def get_difficulty_info(self) -> Dict[str, Any]:
        """Obtiene información sobre la dificultad actual"""
        return {
            'name': self.difficulty.name,
            'description': self.difficulty.description,
            'base_xp': self.difficulty.base_xp,
            'reward_multiplier': self.difficulty.reward_multiplier,
            'exclusive_rewards': self.difficulty.exclusive_rewards,
            'max_level': self.difficulty.max_level
        }

    @classmethod
    def get_available_difficulties(cls) -> Dict[str, Dict[str, Any]]:
        """Obtiene información sobre todas las dificultades disponibles"""
        return {
            k: {
                'name': v.name,
                'description': v.description,
                'reward_multiplier': v.reward_multiplier,
                'exclusive_rewards': v.exclusive_rewards
            }
            for k, v in cls.DIFFICULTIES.items()
        }


class JsonProgressPersistence(AbstractProgressPersistence):
    """Implementación de persistencia usando JSON"""

    def __init__(self, save_dir: Path):
        self.save_dir = save_dir
        self.save_dir.mkdir(parents=True, exist_ok=True)

    def get_save_path(self, user_id: str) -> Path:
        return self.save_dir / f"progress_{user_id}.json"

    def save_progress(self, user_id: str, progress_data: Dict[str, Any]) -> bool:
        try:
            save_path = self.get_save_path(user_id)
            with open(save_path, 'w') as f:
                json.dump(progress_data, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving progress: {e}")
            return False

    def load_progress(self, user_id: str) -> Dict[str, Any]:
        try:
            save_path = self.get_save_path(user_id)
            if save_path.exists():
                with open(save_path, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"Error loading progress: {e}")
            return {}