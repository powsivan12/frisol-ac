import os
import sys
from flask import Flask, send_from_directory, jsonify

def create_app():
    # Crear la aplicación Flask
    app = Flask(__name__, 
               static_folder=os.path.abspath('static'),
               template_folder=os.path.abspath('templates'))
    
    # Configuración básica
    app.config.update(
        ENV='production',
        DEBUG=False,
        PREFERRED_URL_SCHEME='https',
        SERVER_NAME=os.environ.get('VERCEL_URL', 'localhost:5000')
    )
    
    # Registrar rutas
    @app.route('/')
    def index():
        try:
            return send_from_directory(app.template_folder, 'index.html')
        except Exception as e:
            app.logger.error(f"Error al cargar index.html: {str(e)}")
            return jsonify({
                'error': str(e),
                'type': type(e).__name__,
                'cwd': os.getcwd(),
                'templates': os.listdir(app.template_folder) if os.path.exists(app.template_folder) else 'No existe',
                'static': os.listdir(app.static_folder) if os.path.exists(app.static_folder) else 'No existe'
            }), 500
    
    @app.route('/static/<path:path>')
    def serve_static(path):
        return send_from_directory(app.static_folder, path)
    
    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(
            app.static_folder, 
            'favicon.ico', 
            mimetype='image/vnd.microsoft.icon'
        )
    
    # Manejador de errores
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'No encontrado', 'message': str(error)}), 404
    
    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'error': 'Error interno del servidor',
            'message': str(error),
            'type': type(error).__name__
        }), 500
    
    return app

# Crear la aplicación
app = create_app()

# Punto de entrada para ejecutar la aplicación localmente
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Iniciando servidor en el puerto {port}...")
    print(f"Directorio actual: {os.getcwd()}")
    print(f"Contenido del directorio: {os.listdir('.')}")
    if os.path.exists('templates'):
        print(f"Contenido de templates: {os.listdir('templates')}")
    if os.path.exists('static'):
        print(f"Contenido de static: {os.listdir('static')}")
    app.run(host='0.0.0.0', port=port)
