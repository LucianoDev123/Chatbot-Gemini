# Se importan las librerías necesarias.
# 'typing' se usa para tipar los objetos 'List' y 'Dict', lo que mejora la legibilidad del código y permite a las herramientas de análisis estático detectar errores.
from typing import List, Dict

# ---

# Se define la función 'build_system_prompt'.
# Esta función es responsable de crear el 'prompt' de sistema que guía el comportamiento del modelo de IA.
# Recibe 'role_instructions' como un string, que son instrucciones específicas para el rol del modelo en una conversación.
def build_system_prompt(role_instructions: str) -> str:
    # Se define la base del prompt de sistema.
    # Estas son las instrucciones generales que el modelo debe seguir siempre (por ejemplo, el idioma, el estilo de respuesta, etc.).
    base = (
        "Eres un chat de consola que responde en español de forma clara y útil. "
        "Si el usuario pide código, incluye explicaciones breves. "
        "Evita información inventada y pide aclaraciones si faltan datos. "
    )
    
    # Se combina el 'prompt' base con las instrucciones de rol específicas.
    # Esto crea un 'prompt' completo y personalizado para cada uso del modelo.
    return base + f"Contexto de rol: {role_instructions}"

# ---

# Se define la función 'collapse_history'.
# Su propósito es limitar el tamaño del historial de la conversación.
# Recibe 'history', una lista de diccionarios que representan los mensajes de la conversación.
def collapse_history(history: List[Dict[str, str]]) -> List[Dict[str, str]]:
    # Se devuelve una 'slice' de los últimos 12 mensajes del historial.
    # Esto es una forma sencilla de mantener la memoria de la conversación dentro de un límite razonable para evitar que las solicitudes a la API sean demasiado largas o costosas.
    return history[-12:]