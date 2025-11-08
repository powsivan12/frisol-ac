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

# Asegurarse de que los directorios existan
os.makedirs(TEMPLATE_DIR, exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)

# Crear un index.html mínimo si no existe
index_path = os.path.join(TEMPLATE_DIR, 'index.html')
if not os.path.exists(index_path):
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write('''<!DOCTYPE html>
<html>
<head>
    <title>Frisol - Sitio en construcción</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            text-align: center; 
            padding: 50px; 
            background-color: #f5f5f5;
        }
        h1 { color: #333; }
        p { color: #666; }
    </style>
</head>
<body>
    <h1>¡Bienvenido a Frisol!</h1>
    <p>El sitio está en construcción.</p>
</body>
</html>''')

# Crear la aplicación Flask
app = Flask(__name__, 
           static_folder=STATIC_DIR,
           template_folder=TEMPLATE_DIR)

# Ruta principal
@app.route('/')
def home():
    try:
        return send_from_directory(TEMPLATE_DIR, 'index.html')
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "cwd": os.getcwd(),
            "files": os.listdir('.')
        }), 500

# Ruta para archivos estáticos
@app.route('/static/<path:path>')
def serve_static_file(path):
    try:
        log(f"Sirviendo archivo estático: {path}")
        return send_from_directory(STATIC_DIR, path)
    except Exception as e:
        log(f"Error al servir archivo estático {path}: {str(e)}")
        return str(e), 404

# Ruta para archivos CSS
@app.route('/css/<path:path>')
def serve_css(path):
    try:
        return send_from_directory(os.path.join(STATIC_DIR, 'css'), path)
    except Exception as e:
        log(f"Error al servir CSS {path}: {str(e)}")
        return str(e), 404

# Ruta para archivos JS
@app.route('/js/<path:path>')
def serve_js(path):
    try:
        return send_from_directory(os.path.join(STATIC_DIR, 'js'), path)
    except Exception as e:
        log(f"Error al servir JS {path}: {str(e)}")
        return str(e), 404

# Ruta para cualquier otra ruta
@app.route('/<path:path>')
def serve_any(path):
    try:
        # Si es un archivo estático, intentar servirlo
        if path.startswith('static/') or path.startswith('css/') or path.startswith('js/'):
            return serve_static_file(path.replace('static/', ''))
        
        # Si no, servir el index.html
        return send_from_directory(TEMPLATE_DIR, 'index.html')
    except Exception as e:
        log(f"Error en serve_any({path}): {str(e)}")
        return send_from_directory(TEMPLATE_DIR, 'index.html')

# Manejador para Vercel
def handler(request, context):
    try:
        with app.test_request_context(path=request.path, method=request.httpMethod):
            res = app.full_dispatch_request()
            return {
                'statusCode': res.status_code,
                'headers': dict(res.headers),
                'body': res.get_data(as_text=True)
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Error en el servidor: {str(e)}"
        }

# Para desarrollo local
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Iniciando servidor en http://localhost:{port}")
    print(f"Directorio actual: {os.getcwd()}")
    print(f"TEMPLATE_DIR: {TEMPLATE_DIR}")
    print(f"STATIC_DIR: {STATIC_DIR}")
    app.run(host='0.0.0.0', port=port, debug=True)