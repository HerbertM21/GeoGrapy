# NO SE USA EN LA APLICACION ORIGINAL

import json
from pathlib import Path
from src.utils.constants import COUNTRIES_DATA

class CountryData:
    _instance = None
    # Se usa singleton para crear una única instancia de la clase
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.load_data()
        return cls._instance

    def load_data(self):
        with open(COUNTRIES_DATA, 'r', encoding='utf-8') as f:
            self.countries = json.load(f)['paises']

    def get_all_countries(self):
        return self.countries

    def get_country(self, name):
        return next((country for country in self.countries
                    if country['nombre'].lower() == name.lower()), None)