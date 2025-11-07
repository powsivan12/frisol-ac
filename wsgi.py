import os
import sys
import traceback

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(f"=== Iniciando aplicación en {BASE_DIR} ===", file=sys.stderr)

# Agregar el directorio actual al path
sys.path.insert(0, BASE_DIR)

# Imprimir información del entorno
print("\n=== Variables de entorno ===", file=sys.stderr)
for key, value in os.environ.items():
    print(f"{key}: {value}", file=sys.stderr)

# Imprimir información del directorio
print("\n=== Estructura de directorios ===", file=sys.stderr)
for root, dirs, files in os.walk('.'):
    level = root.replace('.', '').count(os.sep)
    indent = ' ' * 4 * (level)
    print(f"{indent}{os.path.basename(root)}/", file=sys.stderr)
    subindent = ' ' * 4 * (level + 1)
    for f in files:
        print(f"{subindent}{f}", file=sys.stderr)

try:
    # Intentar importar la aplicación
    print("\n=== Importando aplicación ===", file=sys.stderr)
    from app import app as application
    
    # Configuración de rutas
    application.static_folder = os.path.join(BASE_DIR, 'static')
    application.template_folder = os.path.join(BASE_DIR, 'templates')
    
    # Configuración para producción
    application.config['ENV'] = 'production'
    application.config['DEBUG'] = False
    
    # Verificar archivos importantes
    print("\n=== Verificando archivos importantes ===", file=sys.stderr)
    important_files = [
        'templates/index.html',
        'static/css/styles.css',
        'static/js/main.js'
    ]
    
    for file in important_files:
        path = os.path.join(BASE_DIR, file)
        exists = os.path.exists(path)
        print(f"{'✓' if exists else '✗'} {file} - {'Existe' if exists else 'No existe'}", file=sys.stderr)
    
    print("\n=== Aplicación lista ===", file=sys.stderr)
    
except Exception as e:
    print(f"\n=== ERROR al cargar la aplicación ===", file=sys.stderr)
    print(f"Tipo de error: {type(e).__name__}", file=sys.stderr)
    print(f"Mensaje: {str(e)}", file=sys.stderr)
    print("\nTraceback:", file=sys.stderr)
    traceback.print_exc(file=sys.stderr)
    
    # Crear una aplicación de error mínima
    from flask import Flask, jsonify
    application = Flask(__name__)
    
    @application.route('/')
    def error():
        return jsonify({
            'error': str(e),
            'type': type(e).__name__,
            'cwd': os.getcwd(),
            'files': os.listdir('.')
        }), 500