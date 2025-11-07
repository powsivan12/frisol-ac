from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__, static_folder='static', template_folder='templates')


# Ruta para archivos estáticos
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

# Ruta para favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join('static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

# Ruta principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para manejar el envío del formulario (solo para evitar errores 404)
@app.route('/enviar-mensaje', methods=['POST'])
def enviar_mensaje():
    return {'success': True, 'message': 'Mensaje recibido (simulado)'}

# Manejador de errores 404
@app.errorhandler(404)
def page_not_found(e):
    return 'Página no encontrada', 404

if __name__ == '__main__':
    # Iniciar la aplicación
    app.run(debug=True)
