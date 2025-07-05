<template>
  <div class="progress-graph-container">
    <h2>Gráfico de Progreso</h2>
    <div v-if="loading">Cargando gráfico...</div>
    <div v-else>
      <canvas v-if="chartData" ref="progressChart"></canvas>
      <div v-if="error" class="error">{{ error }}</div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { onMounted, ref } from 'vue'
import Chart from 'chart.js/auto'

export default {
  name: 'ProgressGraph',
  setup() {
    const loading = ref(true)
    const error = ref('')
    const chartData = ref(null)
    const progressChart = ref(null)

    onMounted(async () => {
      try {
        const res = await axios.get('https://<TU_BACKEND_RENDER_URL>/api/training/progress-graph/', {
          headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
        })
        chartData.value = res.data
        if (progressChart.value) {
          new Chart(progressChart.value, {
            type: 'line',
            data: {
              labels: chartData.value.labels,
              datasets: chartData.value.datasets
            },
            options: {
              responsive: true,
              plugins: {
                legend: { position: 'top' },
                title: { display: true, text: 'Progreso de Ejercicios' }
              }
            }
          })
        }
      } catch (e) {
        error.value = 'Error al cargar el gráfico.'
      } finally {
        loading.value = false
      }
    })

    return { loading, error, chartData, progressChart }
  }
}
</script>

<style scoped>
.progress-graph-container {
  max-width: 900px;
  margin: 40px auto;
  padding: 24px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #fff;
}
canvas {
  width: 100% !important;
  height: 400px !important;
}
.error {
  color: red;
  margin-top: 10px;
}
</style>
