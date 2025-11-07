import os
import sys
import traceback
from flask import Flask, send_from_directory, send_file, jsonify

# Configurar el registro de errores
def log_error(message):
    print(f"[ERROR] {message}", file=sys.stderr)
    sys.stderr.flush()

def log_info(message):
    print(f"[INFO] {message}", file=sys.stderr)
    sys.stderr.flush()

# Crear la aplicación Flask
app = Flask(__name__)

# Obtener la ruta al directorio base
try:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
    STATIC_DIR = os.path.join(BASE_DIR, 'static')
    
    log_info(f"Directorio base: {BASE_DIR}")
    log_info(f"Directorio de plantillas: {TEMPLATES_DIR}")
    log_info(f"Directorio estático: {STATIC_DIR}")
    
    # Verificar que los directorios existen
    if not os.path.exists(TEMPLATES_DIR):
        log_error(f"El directorio de plantillas no existe: {TEMPLATES_DIR}")
    if not os.path.exists(STATIC_DIR):
        log_error(f"El directorio estático no existe: {STATIC_DIR}")
        
    # Listar archivos en los directorios
    try:
        log_info("Contenido del directorio raíz:" + str(os.listdir(BASE_DIR)))
        if os.path.exists(TEMPLATES_DIR):
            log_info("Archivos en templates/:" + str(os.listdir(TEMPLATES_DIR)))
        if os.path.exists(STATIC_DIR):
            log_info("Archivos en static/:" + str(os.listdir(STATIC_DIR)))
    except Exception as e:
        log_error(f"Error al listar directorios: {str(e)}")
        
except Exception as e:
    log_error(f"Error en la configuración inicial: {str(e)}")
    log_error(traceback.format_exc())

@app.route('/')
def home():
    try:
        index_path = os.path.join(TEMPLATES_DIR, 'index.html')
        log_info(f"Intentando servir: {index_path}")
        
        if not os.path.exists(index_path):
            log_error(f"El archivo index.html no existe en {index_path}")
            return f"<h1>Error: index.html no encontrado</h1><p>Ruta: {index_path}</p>", 500
            
        return send_file(index_path)
    except Exception as e:
        error_msg = f"Error al cargar index.html: {str(e)}\n\n{traceback.format_exc()}"
        log_error(error_msg)
        return f"<h1>Error al cargar la página</h1><pre>{error_msg}</pre>", 500

@app.route('/<path:path>')
def serve_static(path):
    try:
        # Primero intentar servir archivos estáticos
        static_path = os.path.join(STATIC_DIR, path)
        if os.path.exists(static_path):
            log_info(f"Sirviendo archivo estático: {static_path}")
            return send_from_directory(STATIC_DIR, path)
            
        # Si no se encuentra en static, intentar servir desde templates
        template_path = os.path.join(TEMPLATES_DIR, path)
        if os.path.exists(template_path):
            log_info(f"Sirviendo plantilla: {template_path}")
            return send_from_directory(TEMPLATES_DIR, path)
            
        log_error(f"Archivo no encontrado: {path}")
        return "<h1>404 - Página no encontrada</h1>", 404
        
    except Exception as e:
        error_msg = f"Error al servir {path}: {str(e)}\n\n{traceback.format_exc()}"
        log_error(error_msg)
        return f"<h1>Error al cargar el recurso</h1><pre>{error_msg}</pre>", 500

# Manejador de errores global
@app.errorhandler(500)
def handle_500(error):
    error_msg = f"Error interno del servidor: {str(error)}\n\n{traceback.format_exc()}"
    log_error(error_msg)
    return f"<h1>500 - Error interno del servidor</h1><pre>{error_msg}</pre>", 500

# Punto de entrada para Vercel
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    log_info(f"Iniciando servidor en el puerto {port}...")
    app.run(host='0.0.0.0', port=port, debug=True)
