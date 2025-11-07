import os
from app import app

# Asegurarse de que las rutas sean correctas
app.static_folder = 'static'
app.template_folder = 'templates'

# Esto es necesario para Vercel
application = app