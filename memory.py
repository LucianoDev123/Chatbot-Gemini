# Se importan las librerías necesarias.
# 'deque' de 'collections' es una lista con un tamaño máximo que elimina automáticamente los elementos más antiguos cuando se llena. Esto es ideal para la memoria de una conversación.
# 'typing' se utiliza para tipar 'Deque', 'List' y 'Dict', mejorando la legibilidad y la seguridad del código.
from collections import deque
from typing import Deque, List, Dict

# ---

# Se define la clase 'ConversationMemory'.
# Su propósito es gestionar el historial de una conversación con un modelo de IA, manteniendo solo un número limitado de mensajes recientes.
class ConversationMemory:
    
    # El constructor de la clase se ejecuta al crear una instancia.
    # 'max_messages' define el número máximo de mensajes que se guardarán en la memoria.
    def __init__(self, max_messages: int = 12):
        # Se inicializa el atributo 'memory' como un 'deque'.
        # 'maxlen=max_messages' asegura que el deque no crezca más allá del límite establecido, eliminando el mensaje más antiguo cuando se añade uno nuevo.
        self.memory: Deque[Dict[str, str]] = deque(maxlen=max_messages)

    # ---

    # Método para añadir un mensaje del usuario a la memoria.
    # 'content' es el texto del mensaje.
    def add_user_message(self, content: str):
        # Se añade un diccionario a la memoria con el rol 'user' y el contenido del mensaje.
        self.memory.append({'role': 'user', 'content': content})

    # ---

    # Método para añadir un mensaje del modelo (IA) a la memoria.
    # 'content' es el texto de la respuesta del modelo.
    def add_model_message(self, content: str):
        # Se añade un diccionario a la memoria con el rol 'model' y el contenido del mensaje.
        self.memory.append({'role': 'model', 'content': content})

    # ---

    # Método para obtener todo el historial de la conversación.
    def get(self) -> List[Dict[str, str]]:
        # Se convierte el 'deque' en una lista y se devuelve.
        # Esto es útil para pasar el historial a la API del modelo de IA, que generalmente espera una lista.
        return list(self.memory)
    
    # ---

    # Método para borrar toda la memoria de la conversación.
    def clear(self):
        # Se utiliza el método 'clear()' del 'deque' para eliminar todos los elementos.
        # Esto es útil para iniciar una nueva conversación.
        self.memory.clear()