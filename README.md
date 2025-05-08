# CORE MVC - Personalized Training Plan System

## Descripción

Este proyecto es un sistema para crear y gestionar planes de entrenamiento personalizados para deportistas con diferentes objetivos y niveles de condición física. La plataforma conecta entrenadores profesionales con deportistas, facilitando la creación, asignación y seguimiento de rutinas de ejercicios.

El sistema tiene cuatro tipos de usuarios:
- Administradores
- Entrenadores
- Deportistas
- Invitados

El backend está desarrollado con Django y Django REST Framework, y el frontend con Vue.js y Vite. La base de datos es PostgreSQL.

## Seguridad y Manejo de Usuarios

### Contraseña Encriptada

- El modelo User extiende AbstractUser de Django, que maneja automáticamente el hashing seguro de contraseñas.
- En el serializer UserRegisterSerializer se utiliza el método set_password para guardar la contraseña encriptada.
- Las contraseñas no se almacenan en texto plano, sino en formato hash en la base de datos.
- Puedes verificar esto revisando la base de datos PostgreSQL o probando el registro y autenticación de usuarios.

### Manejo del Rol y Validación de Inputs

- En el frontend, el formulario de registro (frontend/src/views/Register.vue) incluye un selector para el rol, evitando inputs arbitrarios.
- En el backend, el serializer UserRegisterSerializer valida y maneja correctamente el campo role, asegurando que solo se asignen roles válidos.
- Puedes probar registrando usuarios con diferentes roles y verificar que se asignan correctamente.
- También puedes probar enviar roles inválidos y verificar que el sistema los rechaza o maneja adecuadamente.

## Instalación y Dependencias

### Backend

1. Clona el repositorio:
   
   git clone <tu-repositorio>
   cd CORE_MVC
   

2. Crea y activa un entorno virtual:
   
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   

3. Instala las dependencias:
   
   pip install -r requirements.txt
  
3.1 Instala las dependencias branch Rollback funcional:

   pip install -r requirements_updated_v2.txt

5. Configura las variables de entorno necesarias, por ejemplo en un archivo .env o exportándolas:
   - DJANGO_SECRET_KEY
   - DJANGO_DEBUG
   - DJANGO_ALLOWED_HOSTS
   - POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT
   - FRONTEND_URL (URL del frontend desplegado para CORS)

6. Aplica migraciones:
   
   python manage.py migrate
   

7. Crea usuarios por defecto para pruebas:
   
   python manage.py create_default_users
   

8. Ejecuta el servidor:
   
   python manage.py runserver
   

### Frontend

1. Navega a la carpeta frontend:
   
   cd frontend
   

2. Instala las dependencias:
   
   npm install
   

3. Configura la variable de entorno VITE_API_BASE_URL en un archivo .env en la carpeta frontend:
   
   VITE_API_BASE_URL=http://localhost:8000
   

4. Ejecuta el servidor de desarrollo:
   
   npm run dev
   

5. Para producción, construye el proyecto:
   
   npm run build
   

## Despliegue

- Configura las variables de entorno en Render o el servicio que uses para que coincidan con las URLs y credenciales de producción.
- Asegúrate que el backend permita CORS desde el dominio del frontend.
- Ejecuta el comando para crear usuarios por defecto en producción si es necesario.

## Contacto

Para dudas o soporte, contacta al desarrollador.

---
Este README resume la seguridad, manejo de usuarios, instalación, dependencias y despliegue del proyecto CORE MVC.
