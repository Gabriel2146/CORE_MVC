<template>
  <div class="dashboard-container">
    <h2>Panel de Administrador</h2>
    <div class="dashboard-links">
      <router-link to="/users">Gestión de Usuarios</router-link>
      <router-link to="/users/create">Crear Usuario</router-link>
      <router-link to="/exercises">Gestión de Ejercicios</router-link>
      <router-link to="/exercises/create">Crear Ejercicio</router-link>
      <router-link to="/plans">Planes de Entrenamiento</router-link>
      <router-link to="/plans/create">Crear Plan</router-link>
      <router-link to="/reports">Reportes</router-link>
      <router-link to="/effectiveness-ranking">Ranking de Efectividad</router-link>
      <router-link to="/plan-feedback">Feedback de Planes</router-link>
      <a href="/api/users/admin/export/users/" target="_blank">Exportar Usuarios (CSV)</a>
    </div>
    <div class="dashboard-content">
      <p>Bienvenido al panel de administración. Selecciona una opción del menú para gestionar el sistema.</p>
      <!-- Aquí puedes agregar widgets o estadísticas generales si lo deseas -->
    </div>
  </div>
</template>

<script>
export default {
  name: 'DashboardAdmin'
}
</script>

<style scoped>
.dashboard-container {
  max-width: 900px;
  margin: 40px auto;
  padding: 24px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #fff;
}
.dashboard-links {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 24px;
}
.dashboard-links a, .dashboard-links .router-link-active {
  text-decoration: none;
  color: #1976d2;
  font-weight: bold;
  border: 1px solid #1976d2;
  border-radius: 4px;
  padding: 6px 12px;
  background: #f5faff;
  transition: background 0.2s;
}
.dashboard-links a:hover {
  background: #e3f2fd;
}
</style>
