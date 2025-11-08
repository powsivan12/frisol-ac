import os
from app import app

if __name__ == "__main__":
    # Configuración para desarrollo local
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
log(f"Directorio base: {BASE_DIR}")

# Agregar el directorio actual al path
sys.path.insert(0, BASE_DIR)
log(f"Python path: {sys.path}")

# Crear una aplicación de error por defecto
def create_error_app(e):
    from flask import Flask, jsonify
    
    app = Flask(__name__)
    
    @app.route('/')
    def error():
        return jsonify({
            'status': 'error',
            'error': str(e),
            'type': type(e).__name__,
            'cwd': os.getcwd(),
            'files': os.listdir('.'),
            'python_path': sys.path
        }), 500
    
    return app

try:
    # Verificar dependencias
    log("Verificando dependencias...")
    try:
        import flask
        log(f"Flask version: {flask.__version__}")
    except ImportError as e:
        log(f"Error al importar Flask: {e}")
        raise
    
    # Intentar importar la aplicación
    log("Intentando importar la aplicación...")
    try:
        from minimal import app as application
        log("Aplicación importada exitosamente desde minimal.py")
    except ImportError as e:
        log(f"Error al importar la aplicación desde minimal.py: {e}")
        try:
            from app import app as application
            log("Aplicación importada exitosamente desde app.py")
        except ImportError as e:
            log(f"Error al importar la aplicación desde app.py: {e}")
            raise
    
    # Configurar rutas estáticas
    static_path = os.path.join(BASE_DIR, 'static')
    template_path = os.path.join(BASE_DIR, 'templates')
    
    if hasattr(application, 'static_folder'):
        log(f"Ruta estática configurada: {application.static_folder}")
    else:
        application.static_folder = static_path
        log(f"Estableciendo ruta estática a: {static_path}")
    
    if hasattr(application, 'template_folder'):
        log(f"Carpeta de plantillas configurada: {application.template_folder}")
    else:
        application.template_folder = template_path
        log(f"Estableciendo carpeta de plantillas a: {template_path}")
    
    # Configuración para producción
    application.config.update(
        ENV='production',
        DEBUG=False,
        PROPAGATE_EXCEPTIONS=True
    )
    
    # Verificar archivos importantes
    log("Verificando archivos importantes...")
    important_files = [
        ('templates/index.html', 'Archivo de plantilla principal'),
        ('static/css/styles.css', 'Hoja de estilos'),
        ('static/js/main.js', 'Archivo JavaScript principal'),
        ('requirements-vercel.txt', 'Archivo de dependencias')
    ]
    
    for file, desc in important_files:
        path = os.path.join(BASE_DIR, file)
        exists = os.path.exists(path)
        status = '✓' if exists else '✗'
        log(f"{status} {file.ljust(30)} - {desc}: {'Encontrado' if exists else 'No encontrado'}")
    
    # Verificar si la aplicación es invocable
    if not callable(application):
        raise TypeError("La aplicación no es invocable (no es una aplicación WSGI válida)")
    
    log("Aplicación configurada correctamente")
    
except Exception as e:
    log(f"\n=== ERROR FATAL ===")
    log(f"Tipo: {type(e).__name__}")
    log(f"Mensaje: {str(e)}")
    log("\nTraceback:")
    traceback.print_exc(file=sys.stderr)
    
    # Crear una aplicación de error
    application = create_error_app(e)
    
    log("Aplicación de error creada")

# Asegurarse de que la aplicación sea accesible
if __name__ == "__main__":
    log("Iniciando servidor de desarrollo...")
    try:
        port = int(os.environ.get('PORT', 5000))
        application.run(host='0.0.0.0', port=port)
    except Exception as e:
        log(f"Error al iniciar el servidor: {e}")
        raise