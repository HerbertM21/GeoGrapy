from openai import OpenAI
import os
from dotenv import load_dotenv
from src.utils.constants import CONFIG_PATH


class ChatService:
    """Servicio para manejar la comunicación con GRAPY"""

    def __init__(self):
        """Inicializa el servicio de chat"""
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = None
        self.config_file = CONFIG_PATH / 'chatbot_config.txt'
        self.system_message = self.load_system_message()
        self.is_available = self._initialize_client()

    def _initialize_client(self) -> bool:
        """Inicializa el cliente de OpenAI y verifica si está disponible

        Returns:
            bool: True si el cliente se inicializó correctamente, False en caso contrario
        """
        if not self.api_key:
            print("Error: No se encontró la API KEY de OpenAI")
            return False

        try:
            self.client = OpenAI(api_key=self.api_key)
            # Hacer una pequeña prueba de conexión
            self.client.models.list()
            return True
        except Exception as e:
            print(f"Error al inicializar el cliente de OpenAI: {e}")
            return False

    def load_system_message(self) -> str:
        """Carga el mensaje del sistema desde el archivo de configuración"""
        default_message = (
            "Eres Grapy, un asistente virtual especializado en geografía. "
            "Tus creadores son Herbert Mayorga, Margarita Elgueta y Camilo Olmedo. "
            "Solo debes responder preguntas relacionadas con geografía y no abordar otros temas. "
            "Tus respuestas deben ser concisas y directas."
        )

        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    return content if content else default_message
            else:
                self.config_file.parent.mkdir(parents=True, exist_ok=True)
                with open(self.config_file, 'w', encoding='utf-8') as f:
                    f.write(default_message)
                return default_message
        except Exception as e:
            print(f"Error al cargar la configuración del chatbot: {e}")
            return default_message

    def get_response(self, user_message: str) -> str:
        """Obtiene una respuesta de ChatGPT

        Args:
            user_message (str): El mensaje del usuario para procesar
        Returns:
            str: La respuesta generada por el modelo o un mensaje de error
        """
        if not self.is_available:
            return ("Lo siento, el servicio de chat no está disponible en este momento. "
                    "Por favor, verifica tu API KEY de OpenAI en el archivo .env")

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self.system_message},
                    {"role": "user", "content": user_message},
                ],
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            error_message = str(e)
            if "api_key" in error_message.lower():
                return ("Error de autenticación con OpenAI. "
                        "Por favor, verifica tu API KEY en el archivo .env")
            return f"Error al procesar tu mensaje: {error_message}"

    def update_system_message(self, new_message: str) -> bool:
        """Actualiza el mensaje del sistema"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                f.write(new_message)
            self.system_message = new_message
            return True
        except Exception as e:
            print(f"Error al actualizar el mensaje del sistema: {e}")
            return False