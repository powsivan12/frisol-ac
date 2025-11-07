from flask import Flask, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def home():
    try:
        # Ruta absoluta al index.html
        index_path = os.path.join(os.path.dirname(__file__), '../templates/index.html')
        with open(index_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"<h1>Error al cargar index.html</h1><p>{e}</p>", 500

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('../static', path)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('../static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')