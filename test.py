from flask import Flask, jsonify, send_from_directory
import os
import sys
import traceback

def log(message):
    print(f"[TEST] {message}", file=sys.stderr)
    sys.stderr.flush()

app = Flask(__name__)

@app.route('/favicon.ico')
def favicon():
    try:
        log("Serving favicon.ico")
        return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')
    except Exception as e:
        log(f"Error serving favicon: {str(e)}")
        return jsonify({'status': 'error', 'message': 'favicon.ico not found'}), 404

@app.route('/')
def hello():
    try:
        # Basic system information
        root_dir = os.getcwd()
        static_dir = os.path.join(root_dir, 'static')
        templates_dir = os.path.join(root_dir, 'templates')
        
        # Check if static and templates directories exist
        static_exists = os.path.exists(static_dir)
        templates_exists = os.path.exists(templates_dir)
        
        # List files in directories if they exist
        static_files = []
        if static_exists:
            try:
                static_files = os.listdir(static_dir)
            except Exception as e:
                static_files = f"Error listing static directory: {str(e)}"
        
        templates_files = []
        if templates_exists:
            try:
                templates_files = os.listdir(templates_dir)
            except Exception as e:
                templates_files = f"Error listing templates directory: {str(e)}"
        
        # Get environment variables (filter out sensitive ones)
        env_vars = {k: v for k, v in os.environ.items() if not any(skip in k.lower() for skip in ['key', 'secret', 'token', 'password'])}
        
        info = {
            'status': 'success',
            'python_version': sys.version,
            'current_working_directory': root_dir,
            'files_in_root': os.listdir('.'),
            'static': {
                'path': static_dir,
                'exists': static_exists,
                'files': static_files
            },
            'templates': {
                'path': templates_dir,
                'exists': templates_exists,
                'files': templates_files
            },
            'environment': env_vars
        }
        log("Test endpoint called successfully")
        return jsonify(info)
    except Exception as e:
        error_info = {
            'status': 'error',
            'error': str(e),
            'type': type(e).__name__,
            'traceback': str(sys.exc_info())
        }
        log(f"Error in test endpoint: {error_info}")
        return jsonify(error_info), 500

# Add error handler
@app.errorhandler(500)
def handle_500(error):
    error_info = {
        'status': 'error',
        'error': str(error),
        'type': type(error).__name__,
        'traceback': traceback.format_exc()
    }
    log(f"500 Error: {error_info}")
    return jsonify(error_info), 500

if __name__ == '__main__':
    try:
        port = int(os.environ.get('PORT', 5000))
        log(f"Starting test server on port {port}...")
        log(f"Current working directory: {os.getcwd()}")
        log(f"Files in root: {os.listdir('.')}")
        
        # Check if static directory exists
        if os.path.exists('static'):
            log(f"Static directory contents: {os.listdir('static')}")
        else:
            log("Static directory does not exist")
            
        # Check if templates directory exists
        if os.path.exists('templates'):
            log(f"Templates directory contents: {os.listdir('templates')}")
        else:
            log("Templates directory does not exist")
            
        app.run(host='0.0.0.0', port=port, debug=True)
    except Exception as e:
        log(f"Fatal error: {str(e)}\n{traceback.format_exc()}")
        raise
