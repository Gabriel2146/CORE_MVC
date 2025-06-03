# CORE_MVC - Plataforma de Gestión Deportiva

## Descripción
CORE_MVC es una plataforma web desarrollada en Django para la gestión de entrenamientos deportivos. Permite a administradores y entrenadores gestionar usuarios, ejercicios, planes y el seguimiento de deportistas. Incluye dashboards visuales, reportes comparativos, integración con la API de wger y exportación de datos.

## Características principales
- Gestión de usuarios con roles: administrador, entrenador, deportista, invitado.
- Dashboard visual para cada rol.
- Catálogo de ejercicios (locales y desde wger).
- Asignación y seguimiento de planes de entrenamiento.
- Registro y visualización de progreso de los deportistas.
- Reporte visual comparativo de desempeño y mejora.
- Exportación de reportes en CSV.
- Seguridad: autenticación, validación de contraseñas, CORS.

## Instalación y ejecución
1. Clona el repositorio y entra a la carpeta del proyecto:
   ```sh
   git clone <repo-url>
   cd CORE_MVC
   ```
2. Instala las dependencias:
   ```sh
   pip install -r requirements.txt
   ```
3. Realiza las migraciones:
   ```sh
   python manage.py migrate
   ```
4. (Opcional) Pobla la base de datos con datos de ejemplo:
   ```sh
   python manage.py populate_progress_entries
   ```
5. Ejecuta el servidor de desarrollo:
   ```sh
   python manage.py runserver
   ```
6. Accede a la plataforma en [http://localhost:8000](http://localhost:8000)

## Comando de datos de ejemplo
El comando `populate_progress_entries` crea datos de progreso para todos los deportistas en el ejercicio "Chin Up" para las fechas 01/06/2025 y 02/06/2025, con valores distintos y mejora visible para cada usuario.

## Reporte de desempeño
- Accede como entrenador y entra al reporte visual desde el dashboard.
- Filtra por ejercicio y rango de fechas para comparar la mejora de los deportistas.
- Se muestra el peso inicial, final, mejora en kg y % de mejora.

## Estructura del proyecto
- `core_mvc_backend/`: Configuración principal de Django.
- `users/`: Gestión de usuarios, vistas, templates y comandos.
- `training/`: Modelos y lógica de entrenamiento, progreso y ejercicios.
- `wger_integration/`: Integración con la API wger.
- `frontend/`: (opcional) Código de frontend moderno (Vue.js).

## Notas
- Puedes personalizar los datos de ejemplo editando el comando en `users/management/commands/populate_progress_entries.py`.
- El sistema está preparado para producción y despliegue en servicios como Render o DomCloud.

## Licencia
MIT
