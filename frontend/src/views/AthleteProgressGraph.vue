<template>
  <div class="athlete-progress-graph-container">
    <h1>Progreso de Métricas</h1>
    <form class="mb-3" @submit.prevent>
      <label for="plan_id">Selecciona un plan:</label>
      <select v-model="selectedPlanId" id="plan_id" class="form-select d-inline w-auto" @change="fetchGraphData" required>
        <option value="">-- Selecciona plan --</option>
        <option v-for="plan in plans" :key="plan.id" :value="plan.id">{{ plan.name }}</option>
      </select>
    </form>
    <canvas v-if="chartData" ref="chartCanvas" width="600" height="300"></canvas>
    <div v-else-if="!loading" class="alert alert-info">No hay datos de progreso para graficar.</div>
    <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
    <router-link class="btn btn-outline-primary mt-3" to="/athlete">Volver</router-link>
  </div>
</template>

<script>
import axios from 'axios'
import { ref, onMounted, nextTick, watch } from 'vue'
import Chart from 'chart.js/auto'

export default {
  name: 'AthleteProgressGraph',
  setup() {
    const plans = ref([])
    const selectedPlanId = ref('')
    const chartData = ref(null)
    const chartCanvas = ref(null)
    const error = ref('')
    const loading = ref(false)
    let chartInstance = null

    const fetchPlans = async () => {
      try {
        const token = localStorage.getItem('access_token')
        const res = await axios.get('http://localhost:8000/api/training/plans/?athlete_id=self', {
          headers: { Authorization: 'Bearer ' + token }
        })
        plans.value = res.data
      } catch (err) {
        error.value = 'No se pudieron cargar los planes.'
      }
    }

    const fetchGraphData = async () => {
      if (!selectedPlanId.value) return
      loading.value = true
      error.value = ''
      try {
        const token = localStorage.getItem('access_token')
        const res = await axios.get(`http://localhost:8000/api/training/progress/?plan_id=${selectedPlanId.value}`, {
          headers: { Authorization: 'Bearer ' + token }
        })
        const data = res.data
        if (data.length) {
          // Agrupar por fecha y sumar peso
          const grouped = {}
          data.forEach(entry => {
            if (!grouped[entry.date]) grouped[entry.date] = 0
            grouped[entry.date] += parseFloat(entry.weight) || 0
          })
          chartData.value = {
            labels: Object.keys(grouped),
            datasets: [{
              label: 'Peso levantado (kg)',
              data: Object.values(grouped),
              borderColor: 'blue',
              fill: false
            }]
          }
          await nextTick()
          if (chartInstance) chartInstance.destroy()
          chartInstance = new Chart(chartCanvas.value, {
            type: 'line',
            data: chartData.value,
            options: {
              responsive: true,
              scales: {
                x: { title: { display: true, text: 'Fecha' } },
                y: { title: { display: true, text: 'Peso (kg)' } }
              }
            }
          })
        } else {
          chartData.value = null
        }
      } catch (err) {
        error.value = 'No se pudo cargar el progreso.'
      } finally {
        loading.value = false
      }
    }

    onMounted(fetchPlans)
    watch(selectedPlanId, fetchGraphData)

    return { plans, selectedPlanId, chartData, chartCanvas, error, loading, fetchGraphData }
  }
}
</script>

<style scoped>
.athlete-progress-graph-container {
  max-width: 900px;
  margin: 40px auto;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.10), 0 1.5px 4px rgba(0,0,0,0.08);
  padding: 2.5rem 2rem 2rem 2rem;
}
h1 {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  color: #2c3e50;
}
</style>
