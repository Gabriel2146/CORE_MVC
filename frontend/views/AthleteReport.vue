<template>
  <div class="athlete-report-container">
    <h2>Reporte de Atleta</h2>
    <div v-if="loading">Cargando reporte...</div>
    <div v-else-if="report">
      <h3>{{ report.athlete_name }}</h3>
      <p><b>Entrenador:</b> {{ report.trainer_name }}</p>
      <p><b>Progreso:</b> {{ report.progress_summary }}</p>
      <h4>Observaciones</h4>
      <ul>
        <li v-for="obs in report.observations" :key="obs.id">{{ obs.text }}</li>
      </ul>
      <h4>Recomendaciones</h4>
      <ul>
        <li v-for="rec in report.recommendations" :key="rec.id">{{ rec.text }}</li>
      </ul>
    </div>
    <div v-else>
      <div class="error">No se encontró el reporte.</div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'AthleteReport',
  data() {
    return {
      report: null,
      loading: true,
      error: ''
    }
  },
  async mounted() {
    try {
      const res = await axios.get(`https://<TU_BACKEND_RENDER_URL>/api/users/athlete-report/${this.$route.params.id}/`, {
        headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
      })
      this.report = res.data
    } catch (e) {
      this.error = 'Error al cargar el reporte.'
    } finally {
      this.loading = false
    }
  }
}
</script>

<style scoped>
.athlete-report-container {
  max-width: 700px;
  margin: 40px auto;
  padding: 24px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #fff;
}
.error {
  color: red;
  margin-top: 10px;
}
</style>
