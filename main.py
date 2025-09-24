# Importa los módulos necesarios
import sys
from roles import RolesPreset
from chat_service import ChatService
from config import settings # Importa los ajustes de configuración

# Define la función para elegir un rol al inicio
def chose_role() -> RolesPreset:
    print("\nElige un rol para el chat:")
    print("1. Profesor, 2. Traductor, 3. Programador, 4. Asistente")
    sel = input("\nSelecciona una opción (1-4): ")

    # Mapea la selección del usuario a un rol predefinido
    mapping = {
        '1': RolesPreset.PROFESOR,
        '2': RolesPreset.TRADUCTOR,
        '3': RolesPreset.PROGRAMADOR,
        '4': RolesPreset.ASISTENTE
    }
    # Retorna el rol seleccionado, o Asistente si la opción no es válida
    return mapping.get(sel, RolesPreset.ASISTENTE)

# Muestra los comandos disponibles para el usuario
def print_help():
    print("\nComandos disponibles:")
    print("Rol <nombre>: profesor, traductor, programador, asistente. Cambia el rol actual.")
    print("Reset - Reiniciar la conversación")
    print("Salir - Salir del chat")
    print("Ayuda - Muestra este menú")
    print("")

# La función principal que arranca el programa
def main():
    print("")
    print("")
    # Muestra el nombre del sistema desde la configuración
    print(f"🤖 {settings.system_name}")
    print("")
    
    # Inicia el chatbot con un rol inicial
    role = chose_role()
    chat = ChatService(role=role)
    print_help()

    # Bucle infinito que mantiene el chat activo
    while True:
        try:
            user_input = input("🥰Tú: ").strip()
            print("")
        except (KeyboardInterrupt, EOFError):
            print("\nSaliendo del chat. ¡Hasta luego!")
            print("")
            break

        # Ignora la entrada vacía
        if not user_input:
            continue
        
        # Convierte el input a minúsculas para manejar los comandos
        lower_input = user_input.lower()
        
        # Maneja los comandos de salida
        if lower_input in ['salir', 'exit', 'quit']:
            print("Saliendo del chat. ¡Hasta luego!")
            print("")
            break

        # Maneja el comando de reinicio
        elif lower_input in ['reset', 'reiniciar']:
            chat.reset_conversation()
            print("🤖 Chat reiniciado. ¿En qué puedo ayudarte?")
            print("")
            continue
        
        # Maneja el comando para cambiar el rol
        elif lower_input.startswith('rol'):
            new_role_str = lower_input.split(' ', 1)
            if len(new_role_str) < 2:
                print("🤖 Formato incorrecto. Usa: Rol <nombre> (ej. Rol profesor)")
                print("")
                continue

            new_role_name = new_role_str[1]
            mapping = {
                'profesor': RolesPreset.PROFESOR,
                'traductor': RolesPreset.TRADUCTOR,
                'programador': RolesPreset.PROGRAMADOR,
                'asistente': RolesPreset.ASISTENTE
            }

            if new_role_name in mapping:
                chat.set_role(mapping[new_role_name])
                print(f"🤖 Rol cambiado a {new_role_name.capitalize()}. ¿En qué puedo ayudarte?")
                print("")
            else:
                print("🤖 Rol no reconocido. Opciones: profesor, traductor, programador, asistente.")
                print("") 
            continue
        
        # Maneja el comando de ayuda
        elif lower_input in ['ayuda', 'help', '?']:
            print_help()
            continue

        # Envía la pregunta al servicio de chat si no es un comando
        try:
            answer = chat.ask(user_input)
            print(f"🤖 {answer}")
            print("")
        except Exception as e:
            print(f"🤖 Error al obtener respuesta: {e}")
            print("")

# El programa solo se ejecuta si se inicia directamente (no si se importa)
if __name__ == "__main__":
    main()