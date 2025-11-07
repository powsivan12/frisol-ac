import os
import sys
import traceback
import platform
from flask import Flask, send_from_directory, send_file, jsonify, request

# Configurar el registro de errores
def log_error(message):
    print(f"[ERROR] {message}", file=sys.stderr)
    sys.stderr.flush()

def log_info(message):
    print(f"[INFO] {message}", file=sys.stderr)
    sys.stderr.flush()

# Crear la aplicación Flask
app = Flask(__name__)
app.config['PREFERRED_URL_SCHEME'] = 'https'

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
        # Obtener información del entorno
        env_info = {
            'python_version': platform.python_version(),
            'platform': platform.platform(),
            'current_working_dir': os.getcwd(),
            'base_dir': BASE_DIR,
            'templates_dir': TEMPLATES_DIR,
            'static_dir': STATIC_DIR,
            'path_exists': os.path.exists(TEMPLATES_DIR),
            'files_in_templates': os.listdir(TEMPLATES_DIR) if os.path.exists(TEMPLATES_DIR) else 'No existe',
            'request_headers': dict(request.headers)
        }
        
        log_info(f"Información del entorno: {env_info}")
        
        index_path = os.path.join(TEMPLATES_DIR, 'index.html')
        log_info(f"Intentando servir: {index_path}")
        
        if not os.path.exists(index_path):
            error_msg = f"El archivo index.html no existe en {index_path}"
            log_error(error_msg)
            return f"""
            <h1>Error: index.html no encontrado</h1>
            <h2>Información de depuración:</h2>
            <pre>{json.dumps(env_info, indent=2, ensure_ascii=False)}</pre>
            <p>Ruta probada: {index_path}</p>
            """, 500
            
        # Verificar permisos del archivo
        if not os.access(index_path, os.R_OK):
            error_msg = f"Permiso denegado para leer: {index_path}"
            log_error(error_msg)
            return f"<h1>Error de permisos</h1><p>{error_msg}</p>", 500
            
        log_info(f"Enviando archivo: {index_path}")
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

# Ruta de diagnóstico
@app.route('/debug')
def debug():
    try:
        import flask
        import werkzeug
        return f"""
        <h1>Información de depuración</h1>
        <h2>Versiones:</h2>
        <ul>
            <li>Python: {platform.python_version()}</li>
            <li>Flask: {flask.__version__}</li>
            <li>Werkzeug: {werkzeug.__version__}</li>
        </ul>
        <h2>Variables de entorno:</h2>
        <pre>{json.dumps(dict(os.environ), indent=2, ensure_ascii=False)}</pre>
        <h2>Estructura de directorios:</h2>
        <pre>BASE_DIR: {BASE_DIR}
        
Templates: {os.listdir(TEMPLATES_DIR) if os.path.exists(TEMPLATES_DIR) else 'No existe'}
Static: {os.listdir(STATIC_DIR) if os.path.exists(STATIC_DIR) else 'No existe'}
        </pre>
        """
    except Exception as e:
        return f"<h1>Error en la página de depuración</h1><pre>{str(e)}\n\n{traceback.format_exc()}</pre>", 500

# Punto de entrada para Vercel
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    log_info(f"Iniciando servidor en el puerto {port}...")
    log_info(f"Directorio de trabajo: {os.getcwd()}")
    log_info(f"Variables de entorno: {dict(os.environ)}")
    
    # Verificar archivos importantes
    try:
        log_info("Verificando archivos importantes...")
        important_files = [
            (os.path.join(TEMPLATES_DIR, 'index.html'), 'index.html'),
            (os.path.join(STATIC_DIR, 'css/styles.css'), 'styles.css'),
            (os.path.join(STATIC_DIR, 'js/main.js'), 'main.js')
        ]
        
        for path, desc in important_files:
            exists = os.path.exists(path)
            log_info(f"{'✓' if exists else '✗'} {desc}: {path} ({'Existe' if exists else 'No existe'})")
            if exists:
                log_info(f"   Tamaño: {os.path.getsize(path)} bytes")
                log_info(f"   Permisos: {'Lectura' if os.access(path, os.R_OK) else 'Sin lectura'}")
    except Exception as e:
        log_error(f"Error al verificar archivos: {str(e)}")
    
    app.run(host='0.0.0.0', port=port, debug=True)
