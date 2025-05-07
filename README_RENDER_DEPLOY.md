# Deployment Instructions for Render

## Backend (Django)

1. Ensure you have a PostgreSQL database created on Render.
2. Set the following environment variables in your Render Web Service:
   - DJANGO_SECRET_KEY
   - DJANGO_DEBUG=False
   - DJANGO_ALLOWED_HOSTS=your-backend-render-url
   - POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT (from your Render PostgreSQL instance)
   - FRONTEND_URL=your-frontend-render-url
3. Use the provided `render-backend-build.sh` script as your build command:
   ```
   bash render-backend-build.sh
   ```
4. Use the following start command:
   ```
   gunicorn core_mvc_backend.wsgi --log-file -
   ```
5. Ensure your Procfile contains:
   ```
   web: gunicorn core_mvc_backend.wsgi --log-file -
   ```

## Frontend (Vue)

1. Set up a Static Site or Web Service on Render.
2. Use the provided `render-frontend-build.sh` script as your build command:
   ```
   bash render-frontend-build.sh
   ```
3. Set the publish directory to `dist`.
4. Configure your frontend to point API requests to your backend Render URL.

## Notes

- Make sure CORS settings in Django allow requests from your frontend URL.
- After deployment, test the full flow: registration, login, plan generation.
- Check Render logs for any errors and fix accordingly.

This setup will allow you to deploy your Django backend and Vue frontend separately on Render, using PostgreSQL as the database.

If you need help with any specific step or configuration, let me know.
