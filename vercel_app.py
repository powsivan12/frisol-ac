"""Flask application for Vercel deployment."""
import os
import sys
from flask import Flask, jsonify, Response, send_from_directory

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

def log(message):
    """Log a message to stderr."""
    print(f"[APP] {message}", file=sys.stderr)
    sys.stderr.flush()

# Asegurarse de que las rutas estén en el path
sys.path.append(BASE_DIR)

# Try to import Flask
try:
    app = Flask(__name__, 
               static_folder=STATIC_DIR,
               template_folder=TEMPLATE_DIR)
    
    @app.route('/')
    def home():
        """Root endpoint that serves index.html."""
        try:
            return send_from_directory(TEMPLATE_DIR, 'index.html')
        except Exception as e:
            log(f"Error serving index.html: {str(e)}")
            return jsonify({
                'status': 'error',
                'error': str(e),
                'type': type(e).__name__
            }), 500
    
    @app.route('/<path:path>')
    def serve_static(path):
        """Serve static files."""
        try:
            if os.path.exists(os.path.join(STATIC_DIR, path)):
                return send_from_directory(STATIC_DIR, path)
            return jsonify({"error": "Not found"}), 404
        except Exception as e:
            log(f"Error serving static file {path}: {str(e)}")
            return jsonify({"error": str(e)}), 500
    
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
        log(f"Starting server on port {port}...")
        log(f"Current working directory: {os.getcwd()}")
        log(f"Files in root: {os.listdir('.')}")
        app.run(host='0.0.0.0', port=port, debug=True)

except Exception as e:
    # If we can't import Flask, provide a simple WSGI app that shows the error
    log(f"Failed to initialize Flask: {str(e)}")
    
    def simple_app(environ, start_response):
        """Simple WSGI app that shows the error."""
        import traceback
        error_info = f"""
        <h1>Error initializing Flask</h1>
        <h2>Error: {str(e)}</h2>
        <h3>Type: {type(e).__name__}</h3>
        <pre>{traceback.format_exc()}</pre>
        <h3>Python Path:</h3>
        <pre>{'<br>'.join(sys.path)}</pre>
        <h3>Environment Variables:</h3>
        <pre>{'<br>'.join(f"{k}={v}" for k, v in os.environ.items())}</pre>
        """
        start_response('500 Internal Server Error', [
            ('Content-Type', 'text/html'),
            ('Content-Length', str(len(error_info)))
        ])
        return [error_info.encode('utf-8')]
    
    # For Vercel
    app = simple_app
    
    if __name__ == '__main__':
        from wsgiref.simple_server import make_server
        port = int(os.environ.get('PORT', 5000))
        log(f"Starting fallback server on port {port}...")
        with make_server('0.0.0.0', port, simple_app) as httpd:
            httpd.serve_forever()
