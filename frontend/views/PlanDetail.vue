<template>
  <div class="plan-detail-container">
    <h2>Detalle del Plan de Entrenamiento</h2>
    <div v-if="loading">Cargando plan...</div>
    <div v-else-if="plan">
      <h3>{{ plan.name }}</h3>
      <p><b>Atleta:</b> {{ plan.athlete_name }}</p>
      <p><b>Entrenador:</b> {{ plan.trainer_name }}</p>
      <p><b>Duración:</b> {{ plan.duration }} semanas</p>
      <h4>Sesiones</h4>
      <ul>
        <li v-for="session in plan.sessions" :key="session.id">
          <b>{{ session.day }}:</b> {{ session.description }}
        </li>
      </ul>
      <router-link :to="`/plans/${plan.id}/edit`" class="btn btn-warning">Editar</router-link>
      <router-link :to="`/plans/${plan.id}/delete`" class="btn btn-danger">Eliminar</router-link>
    </div>
    <div v-else>
      <div class="error">No se encontró el plan.</div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'PlanDetail',
  data() {
    return {
      plan: null,
      loading: true,
      error: ''
    }
  },
  async mounted() {
    try {
      const res = await axios.get(`https://<TU_BACKEND_RENDER_URL>/api/training/plans/${this.$route.params.id}/`, {
        headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
      })
      this.plan = res.data
    } catch (e) {
      this.error = 'Error al cargar el plan.'
    } finally {
      this.loading = false
    }
  }
}
</script>

<style scoped>
.plan-detail-container {
  max-width: 700px;
  margin: 40px auto;
  padding: 24px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #fff;
}
.btn {
  margin-right: 8px;
}
.error {
  color: red;
  margin-top: 10px;
}
</style>
