<template>
  <div class="trainer-training-plans-container">
    <h2>Planes de Entrenamiento del Entrenador</h2>
    <router-link to="/plans/new" class="btn btn-success">Nuevo Plan</router-link>
    <div v-if="loading">Cargando planes...</div>
    <div v-else>
      <table class="plans-table">
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Atleta</th>
            <th>Duración</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="plan in plans" :key="plan.id">
            <td>{{ plan.name }}</td>
            <td>{{ plan.athlete_name }}</td>
            <td>{{ plan.duration }} semanas</td>
            <td>
              <router-link :to="`/plans/${plan.id}`" class="btn btn-info">Ver</router-link>
              <router-link :to="`/plans/${plan.id}/edit`" class="btn btn-warning">Editar</router-link>
              <router-link :to="`/plans/${plan.id}/delete`" class="btn btn-danger">Eliminar</router-link>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-if="error" class="error">{{ error }}</div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'TrainerTrainingPlans',
  data() {
    return {
      plans: [],
      loading: true,
      error: ''
    }
  },
  async mounted() {
    try {
      const res = await axios.get('https://<TU_BACKEND_RENDER_URL>/api/users/trainer-training-plans/', {
        headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
      })
      this.plans = res.data
    } catch (e) {
      this.error = 'Error al cargar los planes.'
    } finally {
      this.loading = false
    }
  }
}
</script>

<style scoped>
.trainer-training-plans-container {
  max-width: 900px;
  margin: 40px auto;
  padding: 24px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #fff;
}
.plans-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 16px;
}
.plans-table th, .plans-table td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: left;
}
.btn {
  margin-right: 8px;
}
.error {
  color: red;
  margin-top: 10px;
}
</style>
