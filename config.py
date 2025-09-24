# Importa la clase 'dataclass' para crear clases de datos
from dataclasses import dataclass
# 'os' permite interactuar con el sistema operativo, incluyendo las variables de entorno
import os
# Importa la función para cargar variables desde un archivo .env
from dotenv import load_dotenv

# Carga las variables del archivo .env que está en la misma carpeta
load_dotenv()

# El decorador @dataclass crea una clase con superpoderes para guardar datos.
# 'frozen=True' hace que los valores de la clase no se puedan cambiar después de su creación.
@dataclass(frozen=True)
class Settings:
    # Obtiene el valor de la variable de entorno 'GEMINI_API_KEY'.
    # Si no existe, su valor será 'None'.
    api_key: str = os.getenv("GEMINI_API_KEY")

    # Obtiene el nombre del modelo de Gemini que usarás, por ejemplo, 'gemini-1.5-flash'.
    model: str = os.getenv("MODEL")

    # Obtiene el número máximo de reintentos para conectar con la API.
    # Si la variable 'MAX_RETRIES' no existe, usa 3 como valor por defecto.
    # int() convierte el valor a un número entero.
    max_retries: int = int(os.getenv("MAX_RETRIES", 3))

    # Obtiene el tiempo de espera en segundos.
    # Si la variable no existe, usa 30.0 como valor por defecto.
    # float() convierte el valor a un número con decimales (flotante).
    timeout_seconds: float = float(os.getenv("TIMEOUT_SECONDS", "30.0")) # <--- Línea corregida

    # Obtiene el número de mensajes del historial que el chatbot recordará.
    # El valor por defecto es 12.
    max_history_messages: int = int(os.getenv("MAX_HISTORY_MESSAGES", 12))

    # Obtiene el nombre del sistema que se mostrará en la consola.
    # Si la variable no existe, usa "Chatbot Gemini" por defecto.
    system_name: str = os.getenv("SYSTEM_NAME", "Chatbot Gemini")

# Crea una instancia de la clase Settings para que sus valores puedan ser usados
# fácilmente en cualquier parte del programa.
settings = Settings()