from openai import OpenAI
import os
from dotenv import load_dotenv
from src.utils.constants import CONFIG_PATH


class ChatService:
    """Servicio para manejar la comunicación con GRAPY"""

    def __init__(self):
        """Inicializa el servicio de chat"""
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.config_file = CONFIG_PATH / 'chatbot_config.txt'
        self.system_message = self.load_system_message()


    def load_system_message(self) -> str:
        """Carga el mensaje del sistema desde el archivo de configuración

            Args:
                None
            Returns:
                str: El mensaje de sistema cargado del archivo de configuración
        """
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
                # Crear el archivo con el mensaje por defecto si no existe
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
            str: La respuesta generada por el modelo GPT-4
        """
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
            return f"Error al conectarse con la API: {str(e)}"

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