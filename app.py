from flask import Flask, render_template, send_from_directory, jsonify
import os

app = Flask(__name__, static_url_path='', 
            static_folder='static',
            template_folder='templates')

# Configuración para producción
app.config['ENV'] = 'production'
app.config['DEBUG'] = False

# Ruta principal
@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        return f"Error al cargar la página: {str(e)}", 500

# Ruta para archivos estáticos
@app.route('/<path:path>')
def serve_static(path):
    try:
        if path.startswith('static/'):
            return send_from_directory('.', path)
        return send_from_directory('static', path)
    except Exception as e:
        return f"Error al cargar el recurso: {str(e)}", 404

# Ruta para favicon
@app.route('/favicon.ico')
def favicon():
    try:
        return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')
    except:
        return '', 404

# Ruta para el envío de formulario
@app.route('/enviar-mensaje', methods=['POST'])
def enviar_mensaje():
    try:
        # Aquí iría la lógica para procesar el formulario
        return jsonify({
            'success': True, 
            'message': 'Mensaje recibido correctamente'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al procesar la solicitud: {str(e)}'
        }), 500

# Manejador de errores 404
@app.errorhandler(404)
def page_not_found(e):
    return 'Página no encontrada', 404

# Manejador de errores 500
@app.errorhandler(500)
def internal_server_error(e):
    return 'Error interno del servidor', 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
