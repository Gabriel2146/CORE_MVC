<template>
  <div class="dashboard-container">
    <h2>Panel de Atleta</h2>
    <div class="dashboard-links">
      <router-link to="/athlete/my-plans">Mis Planes</router-link>
      <router-link to="/athlete/progress">Mi Progreso</router-link>
      <router-link to="/athlete/exercises">Ejercicios</router-link>
      <router-link to="/athlete/report">Reportes</router-link>
    </div>
    <div class="dashboard-content">
      <p>Bienvenido al panel de atleta. Selecciona una opción del menú.</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DashboardAthlete'
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
