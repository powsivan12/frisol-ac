from flask import Flask, send_from_directory, jsonify
import os
import sys

def log(message):
    print(f"[APP] {message}", file=sys.stderr)
    sys.stderr.flush()

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

log(f"Iniciando aplicación en {BASE_DIR}")
log(f"TEMPLATE_DIR: {TEMPLATE_DIR}")
log(f"STATIC_DIR: {STATIC_DIR}")

# Crear la aplicación Flask
app = Flask(__name__, 
           static_folder=STATIC_DIR,
           template_folder=TEMPLATE_DIR)

@app.route('/')
def home():
    try:
        log("Acceso a la ruta raíz")
        index_path = os.path.join(TEMPLATE_DIR, 'index.html')
        log(f"Intentando servir: {index_path}")
        
        if not os.path.exists(index_path):
            raise FileNotFoundError(f"No se encontró index.html en {TEMPLATE_DIR}")
            
        return send_from_directory(TEMPLATE_DIR, 'index.html')
    except Exception as e:
        log(f"Error en home(): {str(e)}")
        return jsonify({
            "error": str(e),
            "cwd": os.getcwd(),
            "files_in_cwd": os.listdir('.'),
            "templates_exists": os.path.exists(TEMPLATE_DIR),
            "static_exists": os.path.exists(STATIC_DIR)
        }), 500

@app.route('/<path:path>')
def serve_static(path):
    try:
        log(f"Intentando servir: {path}")
        
        # Intentar servir archivos estáticos
        if path.startswith('static/') or '/' in path:
            static_path = os.path.join(STATIC_DIR, path.replace('static/', ''))
            if os.path.exists(static_path) and os.path.isfile(static_path):
                log(f"Sirviendo archivo estático: {static_path}")
                return send_from_directory(os.path.dirname(static_path), os.path.basename(static_path))
        
        # Si no es un archivo estático, intentar servir el index.html
        log("Archivo no encontrado, sirviendo index.html")
        return send_from_directory(TEMPLATE_DIR, 'index.html')
        
    except Exception as e:
        log(f"Error en serve_static({path}): {str(e)}")
        return jsonify({
            "error": str(e),
            "path": path,
            "static_dir": STATIC_DIR,
            "template_dir": TEMPLATE_DIR,
            "files_in_static": os.listdir(STATIC_DIR) if os.path.exists(STATIC_DIR) else "No existe",
            "files_in_templates": os.listdir(TEMPLATE_DIR) if os.path.exists(TEMPLATE_DIR) else "No existe"
        }), 500

def handler(request, context):
    try:
        log(f"Nueva solicitud: {request.path} {request.httpMethod}")
        
        with app.test_request_context(path=request.path, method=request.httpMethod):
            res = app.full_dispatch_request()
            return {
                'statusCode': res.status_code,
                'headers': dict(res.headers),
                'body': res.get_data(as_text=True)
            }
    except Exception as e:
        import traceback
        error_msg = f"Error en handler: {str(e)}\n{traceback.format_exc()}"
        log(error_msg)
        return {
            'statusCode': 500,
            'body': error_msg
        }

# Para desarrollo local
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    log(f"Iniciando servidor en puerto {port}...")
    log(f"Directorio actual: {os.getcwd()}")
    log(f"Ruta de templates: {TEMPLATE_DIR}")
    log(f"Ruta de archivos estáticos: {STATIC_DIR}")
    log(f"Archivos en templates: {os.listdir(TEMPLATE_DIR) if os.path.exists(TEMPLATE_DIR) else 'No existe'}")
    log(f"Archivos en static: {os.listdir(STATIC_DIR) if os.path.exists(STATIC_DIR) else 'No existe'}")
    
    app.run(host='0.0.0.0', port=port, debug=True)