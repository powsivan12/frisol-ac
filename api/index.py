from flask import Flask, send_from_directory, send_file
import os

app = Flask(__name__)

# Obtener la ruta al directorio base
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

@app.route('/')
def home():
    try:
        # Usar send_file para servir el archivo HTML
        return send_file(os.path.join(TEMPLATES_DIR, 'index.html'))
    except Exception as e:
        return f"<h1>Error al cargar index.html</h1><p>{str(e)}</p>", 500

@app.route('/<path:path>')
def serve_static(path):
    # Primero intentar servir archivos estáticos
    if os.path.exists(os.path.join(STATIC_DIR, path)):
        return send_from_directory(STATIC_DIR, path)
    # Si no se encuentra en static, intentar servir desde templates
    elif os.path.exists(os.path.join(TEMPLATES_DIR, path)):
        return send_from_directory(TEMPLATES_DIR, path)
    # Si no se encuentra en ningún lado, devolver 404
    return "<h1>404 - Página no encontrada</h1>", 404

# Este es el punto de entrada para Vercel
app = app
