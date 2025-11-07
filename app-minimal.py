from flask import Flask, send_from_directory, render_template_string
import os

app = Flask(__name__)

# Ruta de prueba simple
@app.route('/')
def home():
    try:
        # Intenta leer el archivo index.html directamente
        with open('templates/index.html', 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        # Si falla, muestra un mensaje de error con información
        error_msg = f"""
        <h1>Error al cargar la aplicación</h1>
        <p>Error: {str(e)}</p>
        <p>Directorio actual: {os.getcwd()}</p>
        <p>Contenido del directorio: {os.listdir('.')}</p>
        <p>Contenido de templates: {os.listdir('templates') if os.path.exists('templates') else 'No existe la carpeta templates'}</p>
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

if __name__ == '__main__':
    app.run(debug=True)
