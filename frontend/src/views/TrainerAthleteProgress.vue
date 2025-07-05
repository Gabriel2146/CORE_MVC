<template>
  <div>
    <div class="trainer-section-title"><i class="bi bi-graph-up-arrow"></i> Progreso de Deportistas</div>
    <form class="trainer-select mb-4" @submit.prevent>
      <label for="athlete" class="form-label">Selecciona un deportista:</label>
      <select id="athlete" class="form-select" v-model="selectedAthleteId" @change="fetchProgress">
        <option value="">-- Selecciona --</option>
        <option v-for="athlete in athletes" :key="athlete.id" :value="athlete.id">{{ athlete.username }}</option>
      </select>
    </form>
    <div v-if="selectedAthlete">
      <h2 class="mb-3">Progreso de {{ selectedAthlete.username }}</h2>
      <router-link class="btn btn-outline-info mb-2" :to="`/trainer/athlete-progress-graph/${selectedAthlete.id}`"><i class="bi bi-graph-up"></i> Ver gráfico de progreso</router-link>
      <router-link class="btn btn-outline-primary mb-2" :to="`/trainer/athlete-plans/${selectedAthlete.id}`"><i class="bi bi-list-task"></i> Ver historial de planes</router-link>
      <div class="table-responsive">
        <table class="table table-striped trainer-progress-table">
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
    <router-link class="btn btn-secondary mt-3" to="/trainer"><i class="bi bi-arrow-left"></i> Volver al Dashboard</router-link>
    <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
  </div>
</template>

<script>
import axios from 'axios'
import { ref, computed } from 'vue'

export default {
  name: 'TrainerAthleteProgress',
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
        // Filtrar solo deportistas
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

    return { athletes, selectedAthleteId, selectedAthlete, progressEntries, error, fetchProgress }
  }
}
</script>

<style scoped>
@import url('https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css');
.trainer-section-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: #007bff;
    margin-bottom: 1.5rem;
    letter-spacing: 0.5px;
    text-align: center;
}
.trainer-select {
    max-width: 350px;
    margin: 0 auto 2rem auto;
}
.trainer-progress-table th {
    background: #f5f8fa;
    font-weight: 600;
}
.trainer-progress-table td, .trainer-progress-table th {
    vertical-align: middle;
}
</style>
