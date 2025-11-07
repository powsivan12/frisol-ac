from flask import Flask, jsonify
import os
import sys

def create_minimal_app():
    app = Flask(__name__)
    
    # Configuración básica
    app.config.update(
        ENV='production',
        DEBUG=False
    )
    
    # Ruta de prueba
    @app.route('/')
    def index():
        try:
            # Intenta listar el directorio actual
            files = os.listdir('.')
            
            # Verificar si existe la carpeta templates
            templates_exist = os.path.exists('templates')
            templates_files = os.listdir('templates') if templates_exist else []
            
            # Verificar si existe la carpeta static
            static_exist = os.path.exists('static')
            static_files = os.listdir('static') if static_exist else []
            
            return jsonify({
                'status': 'ok',
                'message': 'Aplicación mínima funcionando',
                'cwd': os.getcwd(),
                'files': files,
                'templates': {
                    'exists': templates_exist,
                    'files': templates_files
                },
                'static': {
                    'exists': static_exist,
                    'files': static_files
                },
                'environment': dict(os.environ)
            })
            
        except Exception as e:
            import traceback
            return jsonify({
                'status': 'error',
                'error': str(e),
                'type': type(e).__name__,
                'traceback': traceback.format_exc(),
                'cwd': os.getcwd(),
                'sys_path': sys.path
            }), 500
    
    return app

# Crear la aplicación
app = create_minimal_app()

# Punto de entrada para ejecutar la aplicación localmente
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Iniciando servidor en el puerto {port}...")
    print(f"Directorio actual: {os.getcwd()}")
    print(f"Contenido del directorio: {os.listdir('.')}")
    app.run(host='0.0.0.0', port=port)
