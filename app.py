from flask import Flask, render_template, send_from_directory, request, jsonify, url_for
import os
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de la aplicación Flask
app = Flask(__name__, 
            template_folder='templates',
            static_folder='static',
            static_url_path='')  # Esto hace que los archivos estáticos se sirvan desde la raíz

# Configuración del correo
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = os.getenv('EMAIL_USER')
MAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
MAIL_DEFAULT_SENDER = os.getenv('EMAIL_USER')
MAIL_RECIPIENT = 'refrigeracionfrisol@gmail.com'

# Ruta principal
@app.route('/')
def home():
    return render_template('index.html')

# Ruta para servir archivos estáticos
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

# Ruta para el favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static/images', 'frissol-logo.jpg', mimetype='image/vnd.microsoft.icon')

def send_email(nombre, email, telefono, mensaje):
    try:
        # Crear mensaje de correo
        msg = MIMEMultipart()
        msg['From'] = MAIL_DEFAULT_SENDER
        msg['To'] = MAIL_RECIPIENT
        msg['Subject'] = f'Nuevo mensaje de {nombre} - Página web Frisol'
        
        # Cuerpo del mensaje
        body = f"""
        Has recibido un nuevo mensaje desde el formulario de contacto de la página web.
        
        Nombre: {nombre}
        Email: {email}
        Teléfono: {telefono or 'No proporcionado'}
        
        Mensaje:
        {mensaje}
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Configuración del servidor SMTP
        server = smtplib.SMTP(MAIL_SERVER, MAIL_PORT)
        server.ehlo()
        server.starttls()
        server.ehlo()
        
        # Iniciar sesión
        server.login(MAIL_USERNAME, MAIL_PASSWORD)
        
        # Enviar correo
        server.send_message(msg)
        server.quit()
        
        return True, "Mensaje enviado correctamente"
    except Exception as e:
        return False, str(e)

# Ruta para manejar el envío del formulario
@app.route('/enviar-mensaje', methods=['POST'])
def enviar_mensaje():
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        if not all(key in data for key in ['nombre', 'email', 'mensaje']):
            return jsonify({
                'success': False,
                'message': 'Faltan campos requeridos'
            }), 400
            
        # Validar formato de email
        if not re.match(r'[^@]+@[^@]+\.[^@]+', data['email']):
            return jsonify({
                'success': False,
                'message': 'El formato del correo electrónico no es válido'
            }), 400
        
        # Enviar correo
        success, message = send_email(
            data['nombre'],
            data['email'],
            data.get('telefono', ''),
            data['mensaje']
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': message
            })
        else:
            return jsonify({
                'success': False,
                'message': f'Error al enviar el correo: {message}'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error en el servidor: {str(e)}'
        }), 500

# Iniciar el servidor de desarrollo
if __name__ == '__main__':
    # Asegurarse de que los directorios existen
    os.makedirs('static', exist_ok=True)
    os.makedirs('uploads', exist_ok=True)
    
    # Imprimir rutas para depuración
    print("Ruta de trabajo actual:", os.getcwd())
    print("Ruta de archivos estáticos:", os.path.join(os.getcwd(), 'static'))
    print("URL para estilos:", url_for('static', filename='css/styles.css'))
    
    # Iniciar la aplicación
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))