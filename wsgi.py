import os
import sys
from app import app as application

# Asegurarse de que las rutas sean correctas
application.static_folder = 'static'
application.template_folder = 'templates'

# Configuración para producción
application.config['ENV'] = 'production'
application.config['DEBUG'] = False

# Imprimir información de depuración
print("=== Configuración de la aplicación ===", file=sys.stderr)
print(f"Directorio actual: {os.getcwd()}", file=sys.stderr)
print(f"Contenido del directorio: {os.listdir('.')}", file=sys.stderr)
if os.path.exists('templates'):
    print(f"Contenido de templates: {os.listdir('templates')}", file=sys.stderr)
else:
    print("La carpeta templates no existe", file=sys.stderr)