<template>
  <div>
    <h2>Reporte de Atleta (Entrenador)</h2>
    <div>
      <label>Selecciona un atleta:</label>
      <select v-model="selectedAthleteId" @change="fetchReport">
        <option v-for="athlete in athletes" :key="athlete.id" :value="athlete.id">
          {{ athlete.username }}
        </option>
      </select>
    </div>
    <div v-if="loading">Cargando reporte...</div>
    <div v-else-if="report">
      <h3>Resumen</h3>
      <p><strong>Nombre:</strong> {{ report.athlete_name }}</p>
      <p><strong>Planes asignados:</strong> {{ report.plans_count }}</p>
      <p><strong>Sesiones completadas:</strong> {{ report.sessions_completed }}</p>
      <p><strong>Progreso promedio:</strong> {{ report.avg_progress }}</p>
      <!-- Puedes agregar más detalles según la estructura de tu API -->
    </div>
    <div v-else>
      <em>No hay reporte disponible para este atleta.</em>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'TrainerAthleteReport',
  data() {
    return {
      athletes: [],
      selectedAthleteId: null,
      report: null,
      loading: false
    }
  },
  async created() {
    try {
      const res = await axios.get('https://<TU_BACKEND_RENDER_URL>/api/users/?role=athlete', {
        headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
      })
      this.athletes = res.data
      if (this.athletes.length) {
        this.selectedAthleteId = this.athletes[0].id
        this.fetchReport()
      }
    } catch (e) {
      alert('Error al cargar atletas')
    }
  },
  methods: {
    async fetchReport() {
      if (!this.selectedAthleteId) return
      this.loading = true
      try {
        const res = await axios.get(`https://<TU_BACKEND_RENDER_URL>/api/training/athlete-report/${this.selectedAthleteId}/`, {
          headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
        })
        this.report = res.data
      } catch (e) {
        this.report = null
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
select {
  margin-bottom: 12px;
}
</style>
