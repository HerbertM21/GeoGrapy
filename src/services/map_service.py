from src.utils.constants import DATA_PATH, RESOURCE_PATH
import json
import os
import traceback # traceback funciona para imprimir la traza de errores


class MapService:
    @staticmethod
    def get_map_html():
        """
        Carga y procesa los datos del mapa desde archivos JSON y HTML.

        Retorno:
            str: Contenido HTML del mapa con los datos insertados
        """
        try:
            # Cargar los datos JSON
            countries_path = os.path.join(DATA_PATH, 'countries.json')
            coordinates_path = os.path.join(DATA_PATH, 'coordinates.json')

            # Cargar los JSON
            with open(countries_path, 'r', encoding='utf-8') as f:
                countries_data = json.load(f)

            with open(coordinates_path, 'r', encoding='utf-8') as f:
                coordinates_data = json.load(f)

            # Leer la plantilla HTML
            with open(str(RESOURCE_PATH / 'styles' / 'index.html'), 'r', encoding='utf-8') as f:
                html_content = f.read()

            # Modificar el HTML para incluir los datos directamente
            html_content = html_content.replace(
                "// REPLACE",
                f"""
                    const countriesData = {json.dumps(countries_data)};
                    const coordinatesData = {json.dumps(coordinates_data)};
                """
            )

            return html_content

        except Exception as e:
            print(f"Error cargando el mapa: {e}")
            traceback.print_exc()
            return f"<html><body>Error cargando el mapa: {e}</body></html>"