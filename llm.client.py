# Se importan las librerías necesarias.
# 'time' se usa para pausar la ejecución en caso de error (reintentos).
# 'typing' para tipado estático (List, Dict, Optional), lo que mejora la legibilidad y la detección de errores.
# 'google.generativeai' es el SDK oficial de Google para interactuar con los modelos Gemini.
# 'config' es un módulo local que presumiblemente contiene la configuración de la API.
import time
from typing import List, Dict, Optional
import google.generativeai as genai
from config import settings

# ---

# Se define la clase GeminiClient, que actúa como un wrapper para la API de Gemini.
# Esto centraliza la lógica de conexión y generación de respuestas, haciendo el código más limpio.
class GeminiClient:
    
    # El constructor de la clase se ejecuta al crear una nueva instancia.
    # Recibe la 'api_key' y el 'model_name'.
    def __init__(self, api_key: str, model_name: str):
        # Se verifica si la 'api_key' existe. Si no, se lanza un error.
        if not api_key:
            raise ValueError("API key no configurado.")
        
        # Se configura globalmente el SDK de Gemini con la clave de API.
        genai.configure(api_key=api_key)
        
        # Se instancia el modelo generativo específico (por ejemplo, 'gemini-pro').
        self.model = genai.GenerativeModel(model_name=model_name)

    # ---

    # Método para generar una respuesta del modelo.
    # Recibe varios parámetros para configurar la solicitud.
    # Código corregido
    def generate(self,
                system_prompt: str,
                history: List[Dict[str, str]],
                user_message: str,
                max_retries: int,
                timeout_seconds: int) -> str:
        
        attempts = 0
        last_error: Optional[Exception] = None
        
        # 1. Creamos el historial completo, incluyendo el system_prompt
        full_history = [{"role": "user", "parts": [system_prompt]}] + history
        
        # 2. Iniciamos el chat con el historial completo
        convo = self.model.start_chat(history=full_history)

        # 3. Y aquí solo se envía el mensaje del usuario
        while attempts < max_retries:
            try:
                response = convo.send_message(
                    content=user_message,
                    # ¡Ya no se pasa el system_prompt aquí!
                    request_options={"timeout": timeout_seconds}
                )
                # ... el resto de tu código
                return response.text
            except Exception as e:
                # ... la lógica de reintentos
                last_error = e
                time.sleep(2 ** attempts)
                attempts += 1
                
        raise RuntimeError(f"Error al generar respuesta después de {max_retries} intentos: {last_error}")