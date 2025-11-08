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
@app.route('/<path:path>')
def serve_static(path):
    try:
        # Si es un archivo estático, intentar servirlo
        if path.startswith('static/'):
            static_path = os.path.join(STATIC_DIR, path.replace('static/', ''))
            if os.path.exists(static_path) and os.path.isfile(static_path):
                return send_from_directory(os.path.dirname(static_path), os.path.basename(static_path))
        
        # Si no es un archivo estático, servir el index.html
        return send_from_directory(TEMPLATE_DIR, 'index.html')
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "path": path,
            "static_dir": STATIC_DIR,
            "template_dir": TEMPLATE_DIR
        }), 500

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