<template>
  <div class="auto-plan-container">
    <h2>Generar plan automático para un deportista</h2>
    <form @submit.prevent="generatePlan" class="mb-4">
      <div class="mb-3">
        <label for="athlete" class="form-label">Seleccionar atleta</label>
        <select v-model="selectedAthlete" id="athlete" class="form-control" required>
          <option value="" disabled>Seleccione un atleta</option>
          <option v-for="athlete in athletes" :key="athlete.id" :value="athlete.id">
            {{ athlete.username }} ({{ athlete.first_name }} {{ athlete.last_name }})
          </option>
        </select>
      </div>
      <div class="mb-3">
        <label for="goal" class="form-label">Objetivo</label>
        <input v-model="goal" id="goal" class="form-control" placeholder="Ej: Mejorar resistencia" required />
      </div>
      <div class="mb-3">
        <label for="weeks" class="form-label">Duración (semanas)</label>
        <input v-model.number="weeks" id="weeks" type="number" min="1" class="form-control" required />
      </div>
      <button type="submit" class="btn btn-primary">Generar plan</button>
    </form>

    <div v-if="loading" class="mb-3">Generando plan...</div>
    <div v-if="error" class="alert alert-danger">{{ error }}</div>

    <div v-if="plan" class="plan-result">
      <h4>Plan sugerido</h4>
      <pre>{{ plan }}</pre>
      <button class="btn btn-success mt-2" @click="assignPlan">Asignar plan al atleta</button>
      <div v-if="assignMessage" class="alert alert-info mt-2">{{ assignMessage }}</div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { ref, onMounted } from 'vue'

export default {
  name: 'TrainerAutoGeneratePlan',
  setup() {
    const athletes = ref([])
    const selectedAthlete = ref('')
    const goal = ref('')
    const weeks = ref(4)
    const plan = ref(null)
    const loading = ref(false)
    const error = ref('')
    const assignMessage = ref('')

    // Fetch athletes (users with role 'athlete')
    const fetchAthletes = async () => {
      try {
        const token = localStorage.getItem('access_token')
        const res = await axios.get('http://localhost:8000/api/users/athletes/', {
          headers: { Authorization: 'Bearer ' + token }
        })
        athletes.value = res.data
      } catch (err) {
        error.value = 'No se pudieron cargar los atletas.'
      }
    }

    onMounted(fetchAthletes)

    // Generate plan
    const generatePlan = async () => {
      error.value = ''
      plan.value = null
      assignMessage.value = ''
      loading.value = true
      try {
        const token = localStorage.getItem('access_token')
        const res = await axios.post('http://localhost:8000/api/training/auto-generate-plan/', {
          athlete_id: selectedAthlete.value,
          goal: goal.value,
          weeks: weeks.value
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

    // Assign plan to athlete
    const assignPlan = async () => {
      assignMessage.value = ''
      try {
        const token = localStorage.getItem('access_token')
        await axios.post('http://localhost:8000/api/training/assign-plan/', {
          athlete_id: selectedAthlete.value,
          plan: plan.value
        }, {
          headers: { Authorization: 'Bearer ' + token }
        })
        assignMessage.value = '¡Plan asignado exitosamente!'
      } catch (err) {
        assignMessage.value = 'Error al asignar el plan.'
      }
    }

    return {
      athletes,
      selectedAthlete,
      goal,
      weeks,
      plan,
      loading,
      error,
      assignPlan,
      assignMessage,
      generatePlan
    }
  }
}
</script>

<style scoped>
.auto-plan-container {
  max-width: 600px;
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
</style>
