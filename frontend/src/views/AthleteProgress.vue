<template>
  <div class="athlete-progress-container">
    <h1>Mi Progreso</h1>
    <form class="mb-3" @submit.prevent>
      <label for="plan_id">Selecciona un plan:</label>
      <select v-model="selectedPlanId" id="plan_id" class="form-select d-inline w-auto" @change="fetchProgress" required>
        <option value="">-- Selecciona plan --</option>
        <option v-for="plan in plans" :key="plan.id" :value="plan.id">{{ plan.name }}</option>
      </select>
    </form>
    <div v-if="selectedPlan">
      <form class="mb-4" @submit.prevent="submitProgress">
        <div class="row g-2 align-items-end">
          <div class="col-md-3">
            <label for="exercise">Ejercicio:</label>
            <select v-model="exerciseId" id="exercise" class="form-select" required>
              <option value="">-- Selecciona ejercicio --</option>
              <option v-for="ex in exercises" :key="ex.id" :value="ex.id">{{ ex.name }}</option>
            </select>
          </div>
          <div class="col-md-2">
            <label>Series:</label>
            <input v-model.number="sets" type="number" min="1" class="form-control" required />
          </div>
          <div class="col-md-2">
            <label>Repeticiones:</label>
            <input v-model.number="reps" type="number" min="1" class="form-control" required />
          </div>
          <div class="col-md-2">
            <label>Peso:</label>
            <input v-model.number="weight" type="number" min="0" step="0.1" class="form-control" />
          </div>
          <div class="col-md-3">
            <label>Notas:</label>
            <input v-model="notes" class="form-control" />
          </div>
          <div class="col-md-12 mt-2">
            <button type="submit" class="btn btn-primary">Registrar Progreso</button>
          </div>
        </div>
      </form>
      <h2>Historial de Progreso</h2>
      <table class="table table-striped">
        <thead>
          <tr>
            <th>Fecha</th>
            <th>Ejercicio</th>
            <th>Series</th>
            <th>Repeticiones</th>
            <th>Peso</th>
            <th>Notas</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="entry in progressEntries" :key="entry.id">
            <td>{{ entry.date }}</td>
            <td>{{ entry.exercise }}</td>
            <td>{{ entry.sets }}</td>
            <td>{{ entry.reps }}</td>
            <td>{{ entry.weight }}</td>
            <td>{{ entry.notes }}</td>
          </tr>
          <tr v-if="progressEntries.length === 0">
            <td colspan="6">No hay registros de progreso para este plan.</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
    <div v-if="success" class="alert alert-success mt-3">¡Progreso registrado!</div>
  </div>
</template>

<script>
import axios from 'axios'
import { ref, computed, onMounted, watch } from 'vue'

export default {
  name: 'AthleteProgress',
  setup() {
    const plans = ref([])
    const selectedPlanId = ref('')
    const selectedPlan = computed(() => plans.value.find(p => p.id == selectedPlanId.value))
    const exercises = ref([])
    const exerciseId = ref('')
    const sets = ref(1)
    const reps = ref(1)
    const weight = ref(0)
    const notes = ref('')
    const progressEntries = ref([])
    const error = ref('')
    const success = ref(false)

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

    const fetchExercises = async () => {
      if (!selectedPlanId.value) return
      try {
        const token = localStorage.getItem('access_token')
        const res = await axios.get(`http://localhost:8000/api/training/exercises/?plan_id=${selectedPlanId.value}`, {
          headers: { Authorization: 'Bearer ' + token }
        })
        exercises.value = res.data
      } catch (err) {
        error.value = 'No se pudieron cargar los ejercicios.'
      }
    }

    const fetchProgress = async () => {
      if (!selectedPlanId.value) return
      try {
        const token = localStorage.getItem('access_token')
        const res = await axios.get(`http://localhost:8000/api/training/progress/?plan_id=${selectedPlanId.value}`, {
          headers: { Authorization: 'Bearer ' + token }
        })
        progressEntries.value = res.data
      } catch (err) {
        error.value = 'No se pudo cargar el progreso.'
      }
    }

    const submitProgress = async () => {
      error.value = ''
      success.value = false
      try {
        const token = localStorage.getItem('access_token')
        await axios.post('http://localhost:8000/api/training/progress/', {
          plan_id: selectedPlanId.value,
          exercise: exerciseId.value,
          sets: sets.value,
          reps: reps.value,
          weight: weight.value,
          notes: notes.value
        }, {
          headers: { Authorization: 'Bearer ' + token }
        })
        success.value = true
        fetchProgress()
      } catch (err) {
        error.value = 'No se pudo registrar el progreso.'
      }
    }

    onMounted(fetchPlans)
    watch(selectedPlanId, () => {
      fetchExercises()
      fetchProgress()
      // Reset exercise selection and progress data when changing plan
      exerciseId.value = ''
      sets.value = 1
      reps.value = 1
      weight.value = 0
      notes.value = ''
      progressEntries.value = []
    })

    return {
      plans,
      selectedPlanId,
      selectedPlan,
      exercises,
      exerciseId,
      sets,
      reps,
      weight,
      notes,
      progressEntries,
      error,
      success,
      fetchProgress,
      submitProgress
    }
  }
}
</script>

<style scoped>
.athlete-progress-container {
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
.table {
  border-radius: 10px;
  overflow: hidden;
  background: #f8f9fa;
}
.btn-primary {
  background: linear-gradient(90deg, #007bff 0%, #00c6ff 100%);
  color: #fff;
  font-weight: 600;
  border: none;
  border-radius: 8px;
  padding: 0.5rem 2rem;
  font-size: 1.1rem;
  transition: background 0.2s;
}
.btn-primary:hover {
  background: linear-gradient(90deg, #0056b3 0%, #00aaff 100%);
}
.alert {
  margin-top: 1rem;
}
</style>
