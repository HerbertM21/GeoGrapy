# src/services/exam_data.py
from src.utils.constants import EXAMS_DATA
import json

def get_exams_by_category(categoria: str) -> list:
    try:
        with open(EXAMS_DATA, 'r', encoding='utf-8') as file:
            exams = json.load(file)
            return exams.get(categoria, [])
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {EXAMS_DATA}")
        return []