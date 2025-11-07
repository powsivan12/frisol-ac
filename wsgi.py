"""
WSGI config for Frisol project.
It exposes the WSGI callable as a module-level variable named ``application``.
"""
import os
from app import app

# Configuración para producción
app.config['ENV'] = 'production'
app.config['DEBUG'] = False

# Asegurarse de que las rutas sean correctas
app.static_folder = 'static'
app.template_folder = 'templates'

application = app