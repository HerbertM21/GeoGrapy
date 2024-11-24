from pathlib import Path

# Obtener la ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Rutas principales
RESOURCE_PATH = BASE_DIR / 'resources'
STYLE_PATH = RESOURCE_PATH / 'styles'
ICON_PATH = RESOURCE_PATH / 'icon'
IMAGE_PATH = RESOURCE_PATH / 'images'
FONT_PATH = RESOURCE_PATH / 'fonts'
DATA_PATH = BASE_DIR / 'src' / 'data'
CONFIG_PATH = DATA_PATH / 'config'

# Rutas especificas de imágenes
COUNTRIES_PATH = IMAGE_PATH / 'countries'
CAPITALS_PATH = IMAGE_PATH / 'capitals'
BACKGROUNDS_PATH = IMAGE_PATH / 'backgrounds'

# Rutas de los datos
DATA_PATH = BASE_DIR / 'src' / 'data' / 'json'
COUNTRIES_DATA = DATA_PATH / 'countries.json'
EXAMS_DATA = DATA_PATH / 'exams.json'

# Crear directorios si no existen
DATA_PATH.mkdir(parents=True, exist_ok=True)
CONFIG_PATH.mkdir(parents=True, exist_ok=True)
FONT_PATH.mkdir(parents=True, exist_ok=True)

