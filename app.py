import os
import sys
from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS

def create_app():
    # Crear la aplicación Flask
    app = Flask(__name__, 
               static_folder=os.path.abspath('static'),
               template_folder=os.path.abspath('templates'))
    
    # Habilitar CORS
    CORS(app, resources={
        r"/*": {
            "origins": ["*"],
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"]
        }
    })
    
    # Configurar cabeceras CORS
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
    
    # Configuración básica
    app.config.update(
        ENV='production',
        DEBUG=False,
        PREFERRED_URL_SCHEME='https',
        SERVER_NAME=os.environ.get('VERCEL_URL', 'localhost:5000')
    )
    
    # Ruta para verificar el estado del servidor
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'ok',
            'cwd': os.getcwd(),
            'files': os.listdir('.'),
            'templates': os.listdir(app.template_folder) if os.path.exists(app.template_folder) else 'No existe',
            'static': os.listdir(app.static_folder) if os.path.exists(app.static_folder) else 'No existe'
        })

    # Registrar rutas
    @app.route('/', methods=['GET', 'OPTIONS'])
    def index():
        if request.method == 'OPTIONS':
            return '', 200
            
        try:
            # Verificar si el archivo existe
            index_path = os.path.join(app.template_folder, 'index.html')
            if not os.path.exists(index_path):
                raise FileNotFoundError(f'No se encontró el archivo: {index_path}')
                
            return send_from_directory(app.template_folder, 'index.html')
        except Exception as e:
            app.logger.error(f"Error al cargar index.html: {str(e)}", exc_info=True)
            return jsonify({
                'status': 'error',
                'error': str(e),
                'type': type(e).__name__,
                'cwd': os.getcwd(),
                'files': os.listdir('.'),
                'templates': os.listdir(app.template_folder) if os.path.exists(app.template_folder) else 'No existe',
                'static': os.listdir(app.static_folder) if os.path.exists(app.static_folder) else 'No existe',
                'path': index_path if 'index_path' in locals() else 'No definido'
            }), 500
    
    @app.route('/static/<path:path>', methods=['GET', 'OPTIONS'])
    def serve_static(path):
        if request.method == 'OPTIONS':
            return '', 200
            
        try:
            return send_from_directory(app.static_folder, path)
        except Exception as e:
            app.logger.error(f"Error al servir archivo estático {path}: {str(e)}")
            return jsonify({
                'status': 'error',
                'error': str(e),
                'type': type(e).__name__,
                'path': os.path.join(app.static_folder, path) if 'path' in locals() else 'No definido',
                'static_files': os.listdir(app.static_folder) if os.path.exists(app.static_folder) else 'No existe'
            }), 404
    
    @app.route('/favicon.ico', methods=['GET', 'OPTIONS'])
    def favicon():
        if request.method == 'OPTIONS':
            return '', 200
            
        try:
            return send_from_directory(
                app.static_folder, 
                'favicon.ico', 
                mimetype='image/vnd.microsoft.icon'
            )
        except Exception as e:
            app.logger.error(f"Error al cargar favicon.ico: {str(e)}")
            return jsonify({
                'status': 'error',
                'error': str(e),
                'type': type(e).__name__,
                'static_files': os.listdir(app.static_folder) if os.path.exists(app.static_folder) else 'No existe'
            }), 404
    
    # Manejador de errores
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'status': 'error',
            'code': 400,
            'error': 'Solicitud incorrecta',
            'message': str(error)
        }), 400
        
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'status': 'error',
            'code': 404,
            'error': 'No encontrado',
            'message': str(error),
            'path': request.path,
            'method': request.method
        }), 404
    
    @app.errorhandler(500)
    def server_error(error):
        import traceback
        return jsonify({
            'status': 'error',
            'code': 500,
            'error': 'Error interno del servidor',
            'message': str(error),
            'type': type(error).__name__,
            'traceback': traceback.format_exc()
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
