from flask import Flask, send_from_directory, render_template_string
import os

app = Flask(__name__)

# Configuración básica
app.config['ENV'] = 'production'
app.config['DEBUG'] = False

# Ruta de prueba simple
@app.route('/')
def hello():
    try:
        # Intenta servir el archivo index.html directamente
        return send_from_directory('templates', 'index.html')
    except Exception as e:
        # Si falla, muestra un mensaje de error con información
        error_msg = f"""
        <h1>Error al cargar la aplicación</h1>
        <p>Error: {str(e)}</p>
        <p>Directorio actual: {os.getcwd()}</p>
        <p>Contenido del directorio: {os.listdir('.')}</p>
        """
        return error_msg, 500

# Ruta para archivos estáticos
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

# Ruta para favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

from flask import Flask, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def hello():
    try:
        return send_from_directory('templates', 'index.html')
    except Exception as e:
        return f"<h1>Error: {e}</h1>", 500

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')
