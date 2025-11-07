import os
from dotenv import load_dotenv
from whatsapp_service import WhatsAppService

def test_whatsapp_connection():
    # Cargar variables de entorno
    load_dotenv()
    
    # Obtener el número de administrador
    admin_number = os.getenv('WHATSAPP_ADMIN')
    
    if not admin_number:
        print("ERROR: No se encontró el número de administrador en el archivo .env")
        return False
    
    print(f"Probando conexión con WhatsApp para el número: {admin_number}")
    
    try:
        # Crear instancia del servicio
        whatsapp = WhatsAppService()
        
        # Mensaje de prueba
        test_message = "🔍 *PRUEBA*: Este es un mensaje de prueba del sistema Frisol AC"
        
        print(f"\nEnviando mensaje de prueba...")
        success, message = whatsapp.send_notification(admin_number, test_message)
        
        if success:
            print("✅ Prueba exitosa. Deberías recibir un mensaje en WhatsApp en los próximos segundos.")
            print(f"Mensaje: {message}")
        else:
            print(f"❌ Error al enviar el mensaje: {message}")
        
        return success
        
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        return False

if __name__ == "__main__":
    test_whatsapp_connection()
