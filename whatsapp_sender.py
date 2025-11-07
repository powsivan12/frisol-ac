import pywhatkit
import time
from datetime import datetime, timedelta

def send_whatsapp_message(phone_number, message):
    """
    Envía un mensaje de WhatsApp al número especificado
    
    Args:
        phone_number (str): Número de teléfono con código de país (ej: '+521234567890')
        message (str): Mensaje a enviar
    """
    try:
        # Obtener la hora actual y sumar 1 minuto para el envío
        now = datetime.now()
        send_time = now + timedelta(minutes=1)
        
        print(f"Preparando para enviar mensaje a {phone_number}...")
        
        # Enviar el mensaje
        pywhatkit.sendwhatmsg(
            phone_no=phone_number,
            message=message,
            time_hour=send_time.hour,
            time_min=send_time.minute,
            wait_time=15,
            tab_close=True
        )
        
        print("✅ Mensaje programado para enviarse.")
        print("Nota: Asegúrate de tener WhatsApp Web abierto en tu navegador.")
        return True
        
    except Exception as e:
        print(f"❌ Error al enviar el mensaje: {str(e)}")
        return False

def main():
    # Ejemplo de uso
    phone = input("Ingresa el número de teléfono con código de país (ej: +521234567890): ")
    message = input("Escribe tu mensaje: ")
    
    print("\n--- Configuración Inicial ---")
    print("1. Abre WhatsApp Web en tu navegador (https://web.whatsapp.com/)")
    print("2. Escanea el código QR con tu teléfono")
    print("3. Asegúrate de estar conectado correctamente")
    input("\nPresiona Enter cuando hayas completado los pasos anteriores...")
    
    send_whatsapp_message(phone, message)

if __name__ == "__main__":
    main()
