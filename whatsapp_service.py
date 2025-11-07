import os
import time
from datetime import datetime, timedelta
import pywhatkit
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class WhatsAppService:
    def __init__(self):
        self.admin_number = os.getenv('WHATSAPP_ADMIN', '')
        
    def send_notification(self, to_number, message):
        """
        Envía una notificación por WhatsApp
        
        Args:
            to_number (str): Número de teléfono con código de país (ej: '+521234567890')
            message (str): Mensaje a enviar
            
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            print(f"\n=== Iniciando envío de WhatsApp ===")
            print(f"Destinatario: {to_number}")
            print(f"Mensaje: {message}")
            
            if not to_number or not isinstance(to_number, str):
                error_msg = "Número de teléfono no válido"
                print(f"Error: {error_msg}")
                return False, error_msg
                
            # Limpiar el número de teléfono (eliminar espacios, guiones, etc.)
            to_number = ''.join(c for c in to_number if c.isdigit() or c == '+')
            
            if not to_number.startswith('+'):
                error_msg = "El número debe incluir el código de país (ej: +521234567890)"
                print(f"Error: {error_msg}")
                return False, error_msg
            
            # Verificar que el número tenga al menos 10 dígitos (sin contar el +)
            if len(to_number) < 11:  # +52 + 10 dígitos
                error_msg = "El número de teléfono es demasiado corto"
                print(f"Error: {error_msg}")
                return False, error_msg
            
            # Configurar el tiempo de envío (1 minuto en el futuro)
            now = datetime.now()
            send_time = now + timedelta(minutes=1)
            print(f"Programando envío para: {send_time}")
            
            try:
                # Configurar pywhatkit para que no cierre la pestaña
                pywhatkit.sendwhatmsg(
                    phone_no=to_number,
                    message=message,
                    time_hour=send_time.hour,
                    time_min=send_time.minute,
                    wait_time=15,  # Reducir el tiempo de espera
                    tab_close=False,
                    close_time=3  # Cerrar después de 3 segundos
                )
                print("✅ Mensaje programado para envío")
                return True, "Notificación enviada correctamente"
                
            except Exception as e:
                # Si hay un error, intentar una alternativa más simple
                print(f"Error al enviar con pywhatkit: {str(e)}")
                print("Intentando método alternativo...")
                
                import webbrowser
                import urllib.parse
                
                # Codificar el mensaje para URL
                encoded_message = urllib.parse.quote(message)
                # Crear la URL de WhatsApp
                whatsapp_url = f"https://web.whatsapp.com/send?phone={to_number[1:]}&text={encoded_message}"
                # Abrir en el navegador
                webbrowser.open(whatsapp_url)
                
                return True, "Se abrió WhatsApp Web. Por favor envía el mensaje manualmente."
            
            return True, "Notificación enviada correctamente"
            
        except Exception as e:
            return False, f"Error al enviar la notificación: {str(e)}"
    
    def send_admin_notification(self, form_data):
        """
        Envía una notificación al administrador con los datos del formulario de contacto
        
        Args:
            form_data: Diccionario con los datos del formulario
            
        Returns:
            tuple: (success: bool, message: str)
        """
        if not self.admin_number:
            return False, "Número de administrador no configurado"
        
        try:
            # Asegurarse de que todos los campos requeridos estén presentes
            required_fields = ['name', 'email', 'message']
            for field in required_fields:
                if field not in form_data or not form_data[field]:
                    return False, f"Campo requerido faltante: {field}"
            
            # Construir el mensaje
            message = ("📞 *Nuevo mensaje de contacto*\n\n"
                     f"*Nombre:* {form_data['name']}\n"
                     f"*Email:* {form_data['email']}\n"
                     f"*Teléfono:* {form_data.get('phone', 'No proporcionado')}\n\n"
                     f"*Mensaje:*\n{form_data['message']}")
            
            return self.send_notification(self.admin_number, message)
            
        except Exception as e:
            return False, f"Error al procesar los datos del formulario: {str(e)}"
        
        return self.send_notification(self.admin_number, message)

# Ejemplo de uso
if __name__ == "__main__":
    whatsapp = WhatsAppService()
    
    # Ejemplo de envío de notificación
    result, message = whatsapp.send_notification(
        "+521234567890",  # Reemplaza con tu número
        "Hola, este es un mensaje de prueba desde la aplicación"
    )
    print(f"Resultado: {result}")
    print(f"Mensaje: {message}")
