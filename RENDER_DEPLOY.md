# Render.com configuration for Django + PostgreSQL

# 1. requirements.txt
# (Ya lo tienes, asegúrate de que incluye gunicorn y psycopg2-binary)
# Si falta, agrega:
# gunicorn
# psycopg2-binary

# 2. Procfile
web: gunicorn core_mvc_backend.wsgi:application --log-file -

# 3. render.yaml (opcional, para despliegue automático)
# Puedes crear este archivo para definir servicios y base de datos en Render.
# Ejemplo básico:

services:
  - type: web
    name: core-mvc-web
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "gunicorn core_mvc_backend.wsgi:application --log-file -"
    envVars:
      - key: DJANGO_SETTINGS_MODULE
        value: core_mvc_backend.settings
      - key: SECRET_KEY
        value: "pon-un-valor-seguro-aqui"
      - key: DATABASE_URL
        fromDatabase:
          name: core-mvc-db
          property: connectionString
      - key: ALLOWED_HOSTS
        value: "<tu-dominio-render>"
    autoDeploy: true
    plan: free

  - type: postgres
    name: core-mvc-db
    plan: free

# 4. settings.py (ajustes para producción y Render)
# Modifica la gestión de la base de datos y variables de entorno.
# Puedes usar dj-database-url para facilitar la configuración:
# Agrega a requirements.txt:
# dj-database-url

# En settings.py, reemplaza la sección DATABASES por:

import dj_database_url
import os

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL')
    )
}

# Y para ALLOWED_HOSTS y SECRET_KEY:

SECRET_KEY = os.environ.get('SECRET_KEY', 'inseguro-para-dev')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# 5. Archivos estáticos
# Agrega en settings.py:

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# 6. collectstatic
# Render ejecuta automáticamente 'python manage.py collectstatic' si detecta STATIC_ROOT.

# 7. Despliegue
# - Sube tu código a GitHub.
# - Crea un nuevo servicio web en Render, conecta tu repo, selecciona Python, y usa el comando de inicio del Procfile.
# - Crea una base de datos PostgreSQL en Render y vincúlala.
# - Configura las variables de entorno: SECRET_KEY, ALLOWED_HOSTS, DEBUG (ponlo en False), etc.

# 8. (Opcional) Ejecutar comandos de administración automáticamente
# Si no tienes acceso a la terminal de Render, puedes agregar temporalmente este comando en el apartado de comandos de tu archivo render.yaml o en la sección de comandos de Render:
#
#   - 'python manage.py create_default_users'
#
# Esto creará los usuarios por defecto en la base de datos de Render durante el despliegue. Luego puedes quitarlo para evitar duplicados.

# ¡Listo! Render instalará dependencias, migrará la base y servirá tu app Django profesionalmente.
