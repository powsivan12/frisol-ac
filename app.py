from flask import Flask, send_from_directory
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

# Configuración básica
app.config['ENV'] = 'production'
app.config['DEBUG'] = False

# Ruta principal
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

# Punto de entrada para ejecutar la aplicación localmente
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Iniciando servidor en el puerto {port}...")
    print(f"Directorio actual: {os.getcwd()}")
    print(f"Contenido del directorio: {os.listdir('.')}")
    if os.path.exists('templates'):
        print(f"Contenido de templates: {os.listdir('templates')}")
    app.run(host='0.0.0.0', port=port)
