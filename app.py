from flask import Flask, render_template, request, flash, redirect, url_for, jsonify, current_app, send_from_directory
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, TextAreaField, EmailField, TelField
from wtforms.validators import DataRequired, Email, Length
import os
import logging
from dotenv import load_dotenv

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'una_clave_secreta_muy_segura')

# Configuración para producción
app.config['ENV'] = 'production'
app.config['DEBUG'] = False

# Inicializar la protección CSRF
csrf = CSRFProtect(app)

# Configurar el logger
gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers if gunicorn_logger.handlers else []
app.logger.setLevel(gunicorn_logger.level if gunicorn_logger else logging.INFO)

# Configuración del servidor de correo
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('EMAIL_USER')

# Formulario de contacto
class ContactForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired('Por favor ingrese su nombre'), 
                                           Length(max=100, message='El nombre no puede tener más de 100 caracteres')])
    email = EmailField('Email', validators=[DataRequired('Por favor ingrese su correo electrónico'), 
                                          Email('Por favor ingrese un correo electrónico válido')])
    phone = TelField('Teléfono', validators=[Length(max=20, message='El teléfono no puede tener más de 20 caracteres')])
    message = TextAreaField('Mensaje', validators=[DataRequired('Por favor ingrese su mensaje'),
                                                 Length(max=1000, message='El mensaje no puede tener más de 1000 caracteres')])

# Ruta principal
@app.route('/')
def index():
    form = ContactForm()
    return render_template('index.html', form=form)

# Ruta para manejar el envío del formulario
@app.route('/enviar-mensaje', methods=['GET', 'POST'])
def enviar_mensaje():
    # Si es una petición GET, devolver el formulario (útil para pruebas)
    if request.method == 'GET':
        return jsonify({'status': 'form'})
    
    # Verificar si la solicitud es JSON
    if request.is_json:
        try:
            data = request.get_json()
            form = ContactForm(data=data, meta={'csrf': False})
        except:
            return jsonify({
                'success': False,
                'message': 'Formato de datos inválido'
            }), 400
    else:
        form = ContactForm()
    
    # Validar el formulario
    if form.validate_on_submit():
        try:
            # Crear un diccionario con los datos del formulario
            form_data = {
                'name': form.name.data,
                'email': form.email.data,
                'phone': form.phone.data or 'No proporcionado',
                'message': form.message.data
            }
            
            # Enviar notificación por WhatsApp al administrador
            whatsapp = WhatsAppService()
            success, message = whatsapp.send_admin_notification(form_data)
            
            if not success:
                current_app.logger.error(f"Error al enviar notificación por WhatsApp: {message}")
                # Aún así, consideramos el envío como exitoso para no afectar la experiencia del usuario
            
            # Aquí podrías agregar el envío del correo electrónico
            print(f"Mensaje recibido de {form.name.data} ({form.email.data}): {form.message.data}")
            
            return jsonify({
                'success': True,
                'message': '¡Mensaje enviado con éxito! Nos pondremos en contacto contigo pronto.'
            })
            
        except Exception as e:
            current_app.logger.error(f"Error al procesar el formulario: {str(e)}")
            return jsonify({
                'success': False,
                'message': f'Ocurrió un error al procesar tu mensaje: {str(e)}. Por favor, inténtalo de nuevo más tarde.'
            }), 500
    else:
        # Si hay errores de validación, los devolvemos
        errors = {field.name: field.errors for field in form if field.errors}
        print(f"Errores de validación: {errors}")  # Para depuración
        return jsonify({
            'success': False,
            'errors': errors,
            'message': 'Por favor corrija los errores en el formulario.'
        }), 400

# Manejador de errores 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    # Crear carpeta para archivos subidos
    os.makedirs('uploads', exist_ok=True)
    
    # Iniciar la aplicación
    app.run(debug=True, port=5000)
