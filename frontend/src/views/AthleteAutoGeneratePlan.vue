<template>
  <div class="auto-plan-container">
    <h1>Generar Plan de Entrenamiento Automático</h1>
    <form @submit.prevent="generatePlan">
      <label>Objetivo:</label>
      <select v-model="goal" required>
        <option value="General">General</option>
        <option value="Fuerza">Fuerza</option>
        <option value="Resistencia">Resistencia</option>
        <option value="Básico">Básico</option>
      </select><br>
      <label>Días por semana:</label>
      <input type="number" v-model.number="days" min="1" max="7" required><br>
      <button type="submit">Generar Plan</button>
    </form>
    <div v-if="loading" class="mb-3">Generando plan...</div>
    <div v-if="error" class="alert alert-danger">{{ error }}</div>
    <div v-if="plan" class="plan-result mt-4">
      <h4>Plan sugerido</h4>
      <pre>{{ plan }}</pre>
      <button class="btn btn-success mt-2" @click="acceptPlan">Aceptar plan</button>
      <div v-if="assignMessage" class="alert alert-info mt-2">{{ assignMessage }}</div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { ref } from 'vue'

export default {
  name: 'AthleteAutoGeneratePlan',
  setup() {
    const goal = ref('General')
    const days = ref(3)
    const plan = ref(null)
    const loading = ref(false)
    const error = ref('')
    const assignMessage = ref('')

    const generatePlan = async () => {
      error.value = ''
      plan.value = null
      assignMessage.value = ''
      loading.value = true
      try {
        const token = localStorage.getItem('access_token')
        const res = await axios.post('http://localhost:8000/api/training/auto-generate-plan/', {
          goal: goal.value,
          days: days.value
        }, {
          headers: { Authorization: 'Bearer ' + token }
        })
        plan.value = res.data.plan
      } catch (err) {
        error.value = 'No se pudo generar el plan. Verifique los datos.'
      } finally {
        loading.value = false
      }
    }

    const acceptPlan = async () => {
      assignMessage.value = ''
      try {
        const token = localStorage.getItem('access_token')
        await axios.post('http://localhost:8000/api/training/assign-plan/', {
          plan: plan.value
        }, {
          headers: { Authorization: 'Bearer ' + token }
        })
        assignMessage.value = '¡Plan aceptado y asignado exitosamente!'
      } catch (err) {
        assignMessage.value = 'Error al aceptar el plan.'
      }
    }

    return {
      goal,
      days,
      plan,
      loading,
      error,
      assignMessage,
      generatePlan,
      acceptPlan
    }
  }
}
</script>

<style scoped>
.auto-plan-container {
  max-width: 600px;
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
label {
  font-weight: 500;
  color: #34495e;
  display: block;
  margin-bottom: 0.5rem;
}
select, input[type="number"] {
  border-radius: 8px;
  margin-bottom: 1.2rem;
  font-size: 1.1rem;
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ccc;
}
button[type="submit"] {
  background: linear-gradient(90deg, #007bff 0%, #00c6ff 100%);
  color: #fff;
  font-weight: 600;
  border: none;
  border-radius: 8px;
  padding: 0.7rem 2.5rem;
  font-size: 1.1rem;
  transition: background 0.2s;
  width: 100%;
}
button[type="submit"]:hover {
  background: linear-gradient(90deg, #0056b3 0%, #00aaff 100%);
}
.btn-success {
  background: linear-gradient(90deg, #28a745 0%, #00c6ff 100%);
  color: #fff;
  font-weight: 600;
  border: none;
  border-radius: 8px;
  padding: 0.7rem 2.5rem;
  font-size: 1.1rem;
  transition: background 0.2s;
  width: 100%;
}
.btn-success:hover {
  background: linear-gradient(90deg, #218838 0%, #00aaff 100%);
}
.plan-result {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 1.2rem;
  margin-top: 1.5rem;
}
pre {
  background: #e9ecef;
  border-radius: 6px;
  padding: 1rem;
  font-size: 1rem;
  white-space: pre-wrap;
}
.alert {
  margin-top: 1rem;
}
</style>
