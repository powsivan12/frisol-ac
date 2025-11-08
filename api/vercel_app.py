from flask import Flask, send_from_directory, request, jsonify
import os

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

app = Flask(__name__, 
           static_folder=STATIC_DIR,
           template_folder=TEMPLATE_DIR)

@app.route('/')
def home():
    try:
        return send_from_directory(TEMPLATE_DIR, 'index.html')
    except Exception as e:
        return str(e), 500

@app.route('/<path:path>')
def serve_static(path):
    # Intentar servir archivos estáticos primero
    static_file = os.path.join(STATIC_DIR, path)
    if os.path.exists(static_file) and os.path.isfile(static_file):
        return send_from_directory(STATIC_DIR, path)
    
    # Si no es un archivo estático, intentar servir el index.html
    try:
        return send_from_directory(TEMPLATE_DIR, 'index.html')
    except Exception as e:
        return str(e), 500

# Manejador para Vercel
def handler(event, context):
    from vercel import Response
    
    with app.test_request_context(path=event['path'], method=event['httpMethod']):
        try:
            res = app.full_dispatch_request()
            return Response({
                'statusCode': res.status_code,
                'headers': dict(res.headers),
                'body': res.get_data(as_text=True)
            })
        except Exception as e:
            return Response({
                'statusCode': 500,
                'body': f"Error: {str(e)}"
            })

# Para desarrollo local
if __name__ == '__main__':
    app.run(debug=True)
