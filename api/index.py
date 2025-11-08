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

# Crear la aplicación Flask
app = Flask(__name__, 
           static_folder=STATIC_DIR,
           template_folder=TEMPLATE_DIR)

@app.route('/')
def home():
    try:
        log(f"Sirviendo index.html desde: {TEMPLATE_DIR}")
        # Verificar si el archivo existe
        if not os.path.exists(os.path.join(TEMPLATE_DIR, 'index.html')):
            raise FileNotFoundError(f"No se encontró index.html en {TEMPLATE_DIR}")
        return send_from_directory(TEMPLATE_DIR, 'index.html')
    except Exception as e:
        log(f"Error en home(): {str(e)}")
        return jsonify({"error": str(e), "cwd": os.getcwd()}), 500

@app.route('/<path:path>')
def serve_static(path):
    try:
        # Intentar servir archivos estáticos
        static_path = os.path.join(STATIC_DIR, path)
        if os.path.exists(static_path) and os.path.isfile(static_path):
            log(f"Sirviendo archivo estático: {path}")
            return send_from_directory(STATIC_DIR, path)
        
        # Si no es un archivo estático, intentar servir el index.html
        log(f"Archivo no encontrado: {path}, sirviendo index.html")
        if not os.path.exists(os.path.join(TEMPLATE_DIR, 'index.html')):
            raise FileNotFoundError(f"No se encontró index.html en {TEMPLATE_DIR}")
        return send_from_directory(TEMPLATE_DIR, 'index.html')
    except Exception as e:
        log(f"Error en serve_static({path}): {str(e)}")
        return jsonify({"error": str(e), "static_dir": STATIC_DIR, "template_dir": TEMPLATE_DIR}), 500

# Manejador para Vercel
def handler(request, context):
    from vercel import Response
    
    with app.test_request_context(path=request.path, method=request.httpMethod):
        try:
            res = app.full_dispatch_request()
            return Response({
                'statusCode': res.status_code,
                'headers': dict(res.headers),
                'body': res.get_data(as_text=True)
            })
        except Exception as e:
            error_info = {
                'error': str(e),
                'type': type(e).__name__,
                'cwd': os.getcwd(),
                'files_in_root': os.listdir('.'),
                'templates': os.listdir(TEMPLATE_DIR) if os.path.exists(TEMPLATE_DIR) else 'No existe',
                'static': os.listdir(STATIC_DIR) if os.path.exists(STATIC_DIR) else 'No existe'
            }
            log(f"Error en handler: {error_info}")
            return Response({
                'statusCode': 500,
                'body': str(error_info)
            })

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