from pathlib import Path
import json
from datetime import datetime
from typing import Dict, Optional


class NotesSystem:
    """Sistema para manejar la persistencia de apuntes"""

    def __init__(self, save_dir: Path = None):
        if save_dir is None:
            save_dir = Path.home() / '.geograpy' / 'notes'
        self.save_dir = save_dir
        self.save_dir.mkdir(parents=True, exist_ok=True)

        # Archivo para guardar los apuntes
        self.notes_file = self.save_dir / 'user_notes.json'

        # Estructura inicial de apuntes
        self.default_notes = {
            'categories': {},
            'metadata': {
                'last_modified': str(datetime.now()),
                'version': '2.0'
            }
        }

        # Inicializar archivo si no existe
        if not self.notes_file.exists():
            self.save_notes(self.default_notes['categories'])

    def load_notes(self) -> dict:
        """Carga los apuntes del usuario"""
        try:
            with open(self.notes_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('categories', {})
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_notes(self, notes: dict) -> bool:
        """Guarda los apuntes del usuario"""
        try:
            self.save_dir.mkdir(parents=True, exist_ok=True)

            data = {
                'categories': notes,
                'metadata': {
                    'last_modified': str(datetime.now()),
                    'version': '2.0'
                }
            }

            with open(self.notes_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error al guardar los apuntes: {e}")
            return False

    def add_note(self, category: str, subcategory: str, note_data: Dict) -> bool:
        """
        Añade una nueva nota

        Args:
            category: Categoría de la nota
            subcategory: Se mantiene por compatibilidad pero ya no se usa
            note_data: Diccionario con los datos de la nota
        """
        notes = self.load_notes()

        # Crear la categoría si no existe
        if category not in notes:
            notes[category] = {'default': []}

        # Añadir nota a la categoría
        notes[category]['default'].append(note_data)

        return self.save_notes(notes)

    def get_categories(self) -> list:
        """Retorna la lista de categorías disponibles"""
        return list(self.load_notes().keys())