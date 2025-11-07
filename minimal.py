from flask import Flask, jsonify, Response
import os
import sys
import logging

def log(message):
    """Log a message to stderr."""
    print(message, file=sys.stderr)

try:
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
                'type': type(e).__name__
            }), 500
    
    @app.route('/favicon.ico')
    def favicon():
        """Handle favicon requests."""
        return Response(status=204)  # No content
    
    @app.errorhandler(500)
    def handle_500(error):
        """Handle 500 errors with detailed information."""
        import traceback
        error_info = {
            'status': 'error',
            'error': str(error),
            'type': type(error).__name__,
            'traceback': traceback.format_exc()
        }
        log(f"500 Error: {error_info}")
        return jsonify(error_info), 500
    
    if __name__ == '__main__':
        port = int(os.environ.get('PORT', 5000))
        log(f"Starting minimal server on port {port}...")
        log(f"Current working directory: {os.getcwd()}")
        log(f"Files in root: {os.listdir('.')}")
        app.run(host='0.0.0.0', port=port, debug=True)
    
    # For Vercel
    app = create_minimal_app()

except Exception as e:
    # If we can't import Flask, provide a simple WSGI app that shows the error
    log(f"Failed to initialize Flask: {str(e)}")
    
    def simple_app(environ, start_response):
        """Simple WSGI app that shows the error.
        
        Args:
            environ: WSGI environment dictionary
            start_response: WSGI start_response callable
            
        Returns:
            Response with error information
        """
        import traceback
        error_info = f"""
        <h1>Error initializing Flask</h1>
        <h2>Error: {str(e)}</h2>
        <h3>Type: {type(e).__name__}</h3>
        <pre>{traceback.format_exc()}</pre>
        <h3>Python Path:</h3>
        <pre>\n".join(sys.path)}}</pre>
        <h3>Environment Variables:</h3>
        <pre>{'\n'.join(f"{k}={v}" for k, v in os.environ.items())}</pre>
        """
        start_response('500 Internal Server Error', [('Content-Type', 'text/html')])
        return [error_info.encode('utf-8')]
    
    if __name__ == '__main__':
        from wsgiref.simple_server import make_server
        port = int(os.environ.get('PORT', 5000))
        log(f"Starting fallback server on port {port}...")
        log(f"Error: {str(e)}")
        with make_server('0.0.0.0', port, simple_app) as httpd:
            httpd.serve_forever()
    
    # For Vercel
    app = simple_app
