from app import app
import os

# Configuración para producción
app.config['ENV'] = 'production'
app.config['DEBUG'] = False

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
