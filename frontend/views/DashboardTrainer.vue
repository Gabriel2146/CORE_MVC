<template>
  <div class="dashboard-container">
    <h2>Panel de Entrenador</h2>
    <div class="dashboard-links">
      <router-link to="/trainer/athletes">Mis Atletas</router-link>
      <router-link to="/trainer/exercises">Ejercicios</router-link>
      <router-link to="/trainer/training-plans">Planes de Entrenamiento</router-link>
      <router-link to="/trainer/reports">Reportes</router-link>
      <router-link to="/trainer/auto-generate-plan">Generar Plan Automático</router-link>
    </div>
    <div class="dashboard-content">
      <p>Bienvenido al panel de entrenador. Selecciona una opción del menú.</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DashboardTrainer'
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
