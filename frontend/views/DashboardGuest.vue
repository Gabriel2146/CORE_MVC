<template>
  <div class="dashboard-container">
    <h2>Bienvenido Invitado</h2>
    <div class="dashboard-links">
      <router-link to="/login">Iniciar Sesión</router-link>
      <router-link to="/register">Registrarse</router-link>
      <router-link to="/exercises">Ver Ejercicios</router-link>
    </div>
    <div class="dashboard-content">
      <p>Explora la plataforma. Para acceder a más funcionalidades, inicia sesión o regístrate.</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DashboardGuest'
}
</script>

<style scoped>
.dashboard-container {
  max-width: 800px;
  margin: 40px auto;
  padding: 24px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #fff;
}
.dashboard-links {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
}
.dashboard-links a {
  text-decoration: none;
  color: #1976d2;
  font-weight: bold;
}
</style>
