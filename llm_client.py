# llm_client.py
# Se importan las librerías necesarias.
import time
from typing import List, Dict, Optional
import google.generativeai as genai
from config import settings

# ---

# Se define la clase GeminiClient, que actúa como un wrapper para la API de Gemini.
class GeminiClient:
    
    # El constructor de la clase.
    def __init__(self, api_key: str, model_name: str):
        if not api_key:
            raise ValueError("API key no configurado.")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name=model_name)

    # ---

    # Método para generar una respuesta del modelo.
    # TODO EL CÓDIGO DE ESTA FUNCIÓN DEBE ESTAR INDENTADO DENTRO DE LA CLASE
    def generate(self,
                system_prompt: str,
                history: List[Dict[str, str]],
                user_message: str,
                max_retries: int,
                timeout_seconds: int) -> str:
        
        attempts = 0
        last_error: Optional[Exception] = None
        
        formatted_history = []
        
        if system_prompt:
            formatted_history.append({'role': 'user', 'parts': [{'text': system_prompt}]})
        
        for msg in history:
            formatted_history.append({'role': msg['role'], 'parts': [{'text': msg['content']}]})
            
        convo = self.model.start_chat(history=formatted_history)

        while attempts < max_retries:
            try:
                response = convo.send_message(
                    content=user_message,
                    request_options={"timeout": timeout_seconds}
                )
                return response.text
            except Exception as e:
                last_error = e
                time.sleep(2 ** attempts)
                attempts += 1
                
        raise RuntimeError(f"Error al generar respuesta después de {max_retries} intentos: {last_error}")