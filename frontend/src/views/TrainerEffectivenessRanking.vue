<template>
  <div class="effectiveness-ranking-container">
    <h2>Ranking de efectividad de sesiones</h2>
    <div v-if="loading" class="mb-3">Cargando ranking...</div>
    <div v-if="error" class="alert alert-danger">{{ error }}</div>
    <div v-if="ranking.length" class="table-responsive mt-4">
      <table class="table table-striped">
        <thead>
          <tr>
            <th>#</th>
            <th>Deportista</th>
            <th>Sesiones</th>
            <th>Sesiones cumplidas</th>
            <th>Efectividad (%)</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(athlete, idx) in ranking" :key="athlete.id" :class="{ 'table-success': idx === 0, 'table-warning': idx === 1, 'table-info': idx === 2 }">
            <td>{{ idx + 1 }}</td>
            <td>{{ athlete.username }} ({{ athlete.first_name }} {{ athlete.last_name }})</td>
            <td>{{ athlete.total_sessions }}</td>
            <td>{{ athlete.completed_sessions }}</td>
            <td><b>{{ athlete.effectiveness }}</b></td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-if="!loading && !ranking.length && !error" class="alert alert-info">No hay datos de efectividad disponibles.</div>
  </div>
</template>

<script>
import axios from 'axios'
import { ref, onMounted } from 'vue'

export default {
  name: 'TrainerEffectivenessRanking',
  setup() {
    const ranking = ref([])
    const loading = ref(true)
    const error = ref('')

    const fetchRanking = async () => {
      loading.value = true
      error.value = ''
      try {
        const token = localStorage.getItem('access_token')
        // Suponiendo que el backend expone un endpoint para ranking de efectividad
        const res = await axios.get('http://localhost:8000/api/training/effectiveness-ranking/', {
          headers: { Authorization: 'Bearer ' + token }
        })
        // Ordenar por efectividad descendente
        ranking.value = res.data.sort((a, b) => b.effectiveness - a.effectiveness)
      } catch (err) {
        error.value = 'No se pudo cargar el ranking.'
      } finally {
        loading.value = false
      }
    }

    onMounted(fetchRanking)

    return { ranking, loading, error }
  }
}
</script>

<style scoped>
.effectiveness-ranking-container {
  max-width: 800px;
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
.table-success {
  background: #d4edda !important;
}
.table-warning {
  background: #fff3cd !important;
}
.table-info {
  background: #d1ecf1 !important;
}
</style>
