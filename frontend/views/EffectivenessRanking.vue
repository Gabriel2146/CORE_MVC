<template>
  <div class="effectiveness-ranking-container">
    <h2>Ranking de Efectividad de Entrenamientos</h2>
    <div v-if="loading">Cargando ranking...</div>
    <div v-else>
      <table class="ranking-table">
        <thead>
          <tr>
            <th>Ejercicio</th>
            <th>Índice de Efectividad</th>
            <th>Veces Realizado</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in ranking" :key="item.exercise_id">
            <td>{{ item.exercise_name }}</td>
            <td>{{ item.effectiveness_index }}</td>
            <td>{{ item.times_performed }}</td>
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
  name: 'EffectivenessRanking',
  data() {
    return {
      ranking: [],
      loading: true,
      error: ''
    }
  },
  async mounted() {
    try {
      const res = await axios.get('https://<TU_BACKEND_RENDER_URL>/api/training/effectiveness-ranking/', {
        headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
      })
      this.ranking = res.data
    } catch (e) {
      this.error = 'Error al cargar el ranking.'
    } finally {
      this.loading = false
    }
  }
}
</script>

<style scoped>
.effectiveness-ranking-container {
  max-width: 900px;
  margin: 40px auto;
  padding: 24px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #fff;
}
.ranking-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 16px;
}
.ranking-table th, .ranking-table td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: left;
}
.error {
  color: red;
  margin-top: 10px;
}
</style>
