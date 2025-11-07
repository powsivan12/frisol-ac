"""Minimal Flask application for Vercel deployment."""
import os
import sys

def log(message):
    """Log a message to stderr."""
    print(f"[MINIMAL] {message}", file=sys.stderr)
    sys.stderr.flush()

# Try to import Flask
try:
    from flask import Flask, jsonify, Response
    
    app = Flask(__name__)
    
    @app.route('/')
    def home():
        """Root endpoint that returns system information."""
        try:
            info = {
                'status': 'success',
                'message': 'Minimal Flask app is working!',
                'python_version': sys.version,
                'current_working_directory': os.getcwd(),
                'files_in_root': os.listdir('.'),
                'python_path': sys.path
            }
            log("Home endpoint called successfully")
            return jsonify(info)
        except Exception as e:
            log(f"Error in home endpoint: {str(e)}")
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
