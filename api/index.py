import os
import sys

def log(message):
    print(f"[APP] {message}", file=sys.stderr)
    sys.stderr.flush()

# Try to import Flask
try:
    from flask import Flask, jsonify, Response
    
    app = Flask(__name__)
    
    @app.route('/')
    def home():
        try:
            info = {
                'status': 'success',
                'message': 'Flask app is working!',
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
        return Response(status=204)  # No content
    
    # Vercel serverless function handler
    def handler(request, context):
        from flask import request as flask_request
        with app.request_context(flask_request.environ):
            try:
                return app.full_dispatch_request()
            except Exception as e:
                log(f"Error in handler: {str(e)}")
                return {
                    'statusCode': 500,
                    'body': str(e)
                }
    
    # For local development
    if __name__ == '__main__':
        port = int(os.environ.get('PORT', 5000))
        log(f"Starting server on port {port}...")
        log(f"Current working directory: {os.getcwd()}")
        app.run(host='0.0.0.0', port=port, debug=True)

except Exception as e:
    # If Flask import fails, provide a simple error handler
    log(f"Failed to initialize Flask: {str(e)}")
    
    def handler(event, context):
        import traceback
        error_info = {
            'status': 'error',
            'error': str(e),
            'type': type(e).__name__,
            'traceback': traceback.format_exc(),
            'python_path': sys.path,
            'cwd': os.getcwd(),
            'files_in_root': os.listdir('.')
        }
        log(f"Error in handler: {error_info}")
        return {
            'statusCode': 500,
            'body': str(error_info)
        }