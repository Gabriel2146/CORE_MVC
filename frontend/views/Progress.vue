<template>
  <div class="progress-container">
    <h2>Mi Progreso</h2>
    <div v-if="loading">Cargando progreso...</div>
    <div v-else>
      <table class="progress-table">
        <thead>
          <tr>
            <th>Fecha</th>
            <th>Ejercicio</th>
            <th>Peso (kg)</th>
            <th>Repeticiones</th>
            <th>Series</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="entry in progress" :key="entry.id">
            <td>{{ entry.date }}</td>
            <td>{{ entry.exercise_name }}</td>
            <td>{{ entry.weight }}</td>
            <td>{{ entry.reps }}</td>
            <td>{{ entry.sets }}</td>
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
  name: 'Progress',
  data() {
    return {
      progress: [],
      loading: true,
      error: ''
    }
  },
  async mounted() {
    try {
      const res = await axios.get('https://<TU_BACKEND_RENDER_URL>/api/training/progress/', {
        headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
      })
      this.progress = res.data
    } catch (e) {
      this.error = 'Error al cargar el progreso.'
    } finally {
      this.loading = false
    }
  }
}
</script>

<style scoped>
.progress-container {
  max-width: 900px;
  margin: 40px auto;
  padding: 24px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #fff;
}
.progress-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 16px;
}
.progress-table th, .progress-table td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: left;
}
.error {
  color: red;
  margin-top: 10px;
}
</style>
