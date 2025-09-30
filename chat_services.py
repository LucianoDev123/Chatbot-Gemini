# Importa módulos necesarios para que el servicio funcione.
from typing import Optional
from config import settings # Importa la configuración, como la API key y el modelo.
from roles import RolesPreset, ROLES_SYSTEM_PROMPTS # Importa los roles y sus descripciones.
from prompts import build_system_prompt, collapse_history # Funciones para preparar los mensajes.
from memory import ConversationMemory # La clase para guardar el historial del chat.
from llm_client import GeminiClient # El cliente para conectarse con la API de Gemini.

# Define la clase principal del servicio de chat.
class ChatService:
    # Método constructor que se ejecuta al crear una instancia de la clase.
    def __init__(self, role: RolesPreset = RolesPreset.ASISTENTE):
        # Asigna el rol inicial del chatbot (por defecto, "ASISTENTE").
        self.role = role
        # Inicializa un objeto de memoria para almacenar el historial de la conversación.
        self.memory = ConversationMemory(max_messages=settings.max_history_messages)
        # Crea una instancia del cliente de la API de Gemini.
        self.client = GeminiClient(api_key=settings.api_key, model_name=settings.model)

    # El método principal para enviar una pregunta al modelo y obtener una respuesta.
    def ask(self, prompt: str) -> str:
        # Crea el prompt del sistema basado en el rol actual (e.g., "Eres un profesor...").
        system_prompt = build_system_prompt(ROLES_SYSTEM_PROMPTS[self.role])
        # Colapsa el historial de la memoria en un formato que la API puede entender.
        history = collapse_history(self.memory.get())

        # Llama al cliente de Gemini para generar una respuesta.
        response_text = self.client.generate(
            system_prompt=system_prompt, # El prompt de "personalidad" del chatbot.
            history=history, # El historial de mensajes para que recuerde el contexto.
            user_message=prompt, # La pregunta o mensaje actual del usuario.
            max_retries=settings.max_retries, # Número máximo de intentos si la conexión falla.
            timeout_seconds=settings.timeout_seconds # Tiempo de espera para la respuesta.
        )

        # Guarda el mensaje del usuario y la respuesta del modelo en la memoria.
        self.memory.add_user_message(prompt)
        self.memory.add_model_message(response_text)
        # Devuelve la respuesta generada por la IA.
        return response_text
        #definiendo el set role que faltaba
            # Método para cambiar el rol del chatbot en caliente
    def set_role(self, role: RolesPreset):
        """Cambia el rol actual del chatbot y reinicia la memoria."""
        self.role = role
        self.reset()  # Opcional: reinicia la conversación al cambiar de rol


    # Método para reiniciar la conversación.
    def reset(self):
        # Limpia toda la memoria del historial, borrando el contexto de la conversación.
        self.memory.clear()