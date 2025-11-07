from flask import Flask, jsonify
import os
import sys

def log(message):
    print(f"[TEST] {message}", file=sys.stderr)
    sys.stderr.flush()

app = Flask(__name__)

@app.route('/')
def hello():
    try:
        # Basic system information
        info = {
            'status': 'success',
            'python_version': sys.version,
            'current_working_directory': os.getcwd(),
            'files_in_root': os.listdir('.'),
            'templates_exists': os.path.exists('templates'),
            'static_exists': os.path.exists('static'),
            'templates_files': os.listdir('templates') if os.path.exists('templates') else 'No templates directory',
            'static_files': os.listdir('static') if os.path.exists('static') else 'No static directory',
            'environment': dict(os.environ)
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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    log(f"Starting test server on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=True)
