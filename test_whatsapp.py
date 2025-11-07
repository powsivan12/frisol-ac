from whatsapp_service import WhatsAppService
import os

# Obtener el número de administrador del archivo .env
admin_number = os.getenv('WHATSAPP_ADMIN')

if not admin_number:
    print("Error: WHATSAPP_ADMIN no está configurado en el archivo .env")
    exit(1)

print(f"Probando envío de WhatsApp a: {admin_number}")

# Crear instancia del servicio
whatsapp = WhatsAppService()

# Mensaje de prueba (sin emoji para evitar problemas de codificación)
message = "*PRUEBA*: Este es un mensaje de prueba del sistema Frisol AC"

# Enviar mensaje
success, result = whatsapp.send_notification(admin_number, message)

if success:
    print("[OK] Mensaje de prueba enviado correctamente")
    print("Por favor, verifica tu WhatsApp en los próximos segundos...")
else:
    print(f"[ERROR] Error al enviar el mensaje: {result}")
    print("Asegúrate de que:")
    print("1. Tienes una sesión activa de WhatsApp Web")
    print("2. El número de teléfono es correcto y tiene el formato +[código de país][número]")
    print("3. Tienes conexión a Internet estable")
