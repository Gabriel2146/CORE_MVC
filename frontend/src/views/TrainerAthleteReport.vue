<template>
  <div class="athlete-report-container">
    <h2>Reporte de desempeño de deportistas</h2>
    <form class="mb-4" @submit.prevent>
      <label for="athlete" class="form-label">Selecciona un deportista:</label>
      <select id="athlete" class="form-select" v-model="selectedAthleteId" @change="fetchProgress">
        <option value="">-- Selecciona --</option>
        <option v-for="athlete in athletes" :key="athlete.id" :value="athlete.id">
          {{ athlete.username }} ({{ athlete.first_name }} {{ athlete.last_name }})
        </option>
      </select>
    </form>
    <div v-if="selectedAthlete">
      <h3>Desempeño de {{ selectedAthlete.username }}</h3>
      <div class="row mb-3">
        <div class="col-md-4">
          <div class="report-card">
            <div class="report-label">Sesiones registradas</div>
            <div class="report-value">{{ totalSessions }}</div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="report-card">
            <div class="report-label">Ejercicios distintos</div>
            <div class="report-value">{{ uniqueExercises }}</div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="report-card">
            <div class="report-label">Promedio repeticiones</div>
            <div class="report-value">{{ avgReps }}</div>
          </div>
        </div>
      </div>
      <div class="row mb-3">
        <div class="col-md-4">
          <div class="report-card">
            <div class="report-label">Promedio peso (kg)</div>
            <div class="report-value">{{ avgWeight }}</div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="report-card">
            <div class="report-label">Mejor marca (peso)</div>
            <div class="report-value">{{ maxWeight }}</div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="report-card">
            <div class="report-label">Última sesión</div>
            <div class="report-value">{{ lastSession }}</div>
          </div>
        </div>
      </div>
      <div class="table-responsive mt-4">
        <table class="table table-striped">
          <thead>
            <tr>
              <th>Ejercicio</th>
              <th>Fecha</th>
              <th>Series</th>
              <th>Repeticiones</th>
              <th>Peso</th>
              <th>Notas</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="entry in progressEntries" :key="entry.id">
              <td>{{ entry.exercise }}</td>
              <td>{{ entry.date }}</td>
              <td>{{ entry.sets }}</td>
              <td>{{ entry.reps }}</td>
              <td>{{ entry.weight }}</td>
              <td>{{ entry.notes }}</td>
            </tr>
            <tr v-if="progressEntries.length === 0">
              <td colspan="6">Sin registros de progreso.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
  </div>
</template>

<script>
import axios from 'axios'
import { ref, computed } from 'vue'

export default {
  name: 'TrainerAthleteReport',
  setup() {
    const athletes = ref([])
    const selectedAthleteId = ref('')
    const selectedAthlete = computed(() => athletes.value.find(a => a.id == selectedAthleteId.value))
    const progressEntries = ref([])
    const error = ref('')

    const fetchAthletes = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/users/list-api/', {
          headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
        })
        athletes.value = response.data.filter(u => u.role === 'athlete')
      } catch (err) {
        error.value = 'Error al cargar los deportistas'
      }
    }

    const fetchProgress = async () => {
      if (!selectedAthleteId.value) return
      try {
        const response = await axios.get(`http://localhost:8000/api/training/progress/?athlete_id=${selectedAthleteId.value}`, {
          headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
        })
        progressEntries.value = response.data
      } catch (err) {
        error.value = 'Error al cargar el progreso'
      }
    }

    fetchAthletes()

    // Métricas de desempeño
    const totalSessions = computed(() => progressEntries.value.length)
    const uniqueExercises = computed(() => new Set(progressEntries.value.map(e => e.exercise)).size)
    const avgReps = computed(() => {
      if (!progressEntries.value.length) return 0
      return (
        progressEntries.value.reduce((sum, e) => sum + (parseInt(e.reps) || 0), 0) / progressEntries.value.length
      ).toFixed(1)
    })
    const avgWeight = computed(() => {
      if (!progressEntries.value.length) return 0
      return (
        progressEntries.value.reduce((sum, e) => sum + (parseFloat(e.weight) || 0), 0) / progressEntries.value.length
      ).toFixed(1)
    })
    const maxWeight = computed(() => {
      if (!progressEntries.value.length) return 0
      return Math.max(...progressEntries.value.map(e => parseFloat(e.weight) || 0))
    })
    const lastSession = computed(() => {
      if (!progressEntries.value.length) return '-'
      return progressEntries.value.slice().sort((a, b) => new Date(b.date) - new Date(a.date))[0].date
    })

    return {
      athletes,
      selectedAthleteId,
      selectedAthlete,
      progressEntries,
      error,
      fetchProgress,
      totalSessions,
      uniqueExercises,
      avgReps,
      avgWeight,
      maxWeight,
      lastSession
    }
  }
}
</script>

<style scoped>
.athlete-report-container {
  max-width: 900px;
  margin: 40px auto;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  padding: 2rem 2.5rem 2rem 2.5rem;
}
h2 {
  font-size: 1.7rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  color: #2c3e50;
}
.report-card {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 1.2rem;
  margin-bottom: 1rem;
  text-align: center;
  box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
.report-label {
  font-size: 1rem;
  color: #888;
}
.report-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #007bff;
}
</style>
