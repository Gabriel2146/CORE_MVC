<template>
  <div class="progress-form-container">
    <h2>Registrar Progreso</h2>
    <form @submit.prevent="submitProgress">
      <div class="mb-3">
        <label for="exercise" class="form-label">Ejercicio</label>
        <input v-model="exercise" id="exercise" class="form-control" required />
      </div>
      <div class="mb-3">
        <label for="date" class="form-label">Fecha</label>
        <input v-model="date" id="date" type="date" class="form-control" required />
      </div>
      <div class="mb-3">
        <label for="sets" class="form-label">Series</label>
        <input v-model.number="sets" id="sets" type="number" min="1" class="form-control" required />
      </div>
      <div class="mb-3">
        <label for="reps" class="form-label">Repeticiones</label>
        <input v-model.number="reps" id="reps" type="number" min="1" class="form-control" required />
      </div>
      <div class="mb-3">
        <label for="weight" class="form-label">Peso (kg)</label>
        <input v-model.number="weight" id="weight" type="number" min="0" step="0.1" class="form-control" />
      </div>
      <div class="mb-3">
        <label for="notes" class="form-label">Notas</label>
        <textarea v-model="notes" id="notes" class="form-control"></textarea>
      </div>
      <button type="submit" class="btn btn-success">Registrar</button>
    </form>
    <div v-if="success" class="alert alert-success mt-3">¡Progreso registrado!</div>
    <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
  </div>
</template>

<script>
import axios from 'axios'
import { ref } from 'vue'

export default {
  name: 'AthleteProgressForm',
  setup() {
    const exercise = ref('')
    const date = ref(new Date().toISOString().slice(0, 10))
    const sets = ref(1)
    const reps = ref(1)
    const weight = ref(0)
    const notes = ref('')
    const success = ref(false)
    const error = ref('')

    const submitProgress = async () => {
      error.value = ''
      success.value = false
      try {
        const token = localStorage.getItem('access_token')
        await axios.post('http://localhost:8000/api/training/progress/', {
          exercise: exercise.value,
          date: date.value,
          sets: sets.value,
          reps: reps.value,
          weight: weight.value,
          notes: notes.value
        }, {
          headers: { Authorization: 'Bearer ' + token }
        })
        success.value = true
        // Limpiar formulario
        exercise.value = ''
        sets.value = 1
        reps.value = 1
        weight.value = 0
        notes.value = ''
      } catch (err) {
        error.value = 'No se pudo registrar el progreso.'
      }
    }

    return {
      exercise,
      date,
      sets,
      reps,
      weight,
      notes,
      success,
      error,
      submitProgress
    }
  }
}
</script>

<style scoped>
.progress-form-container {
  max-width: 600px;
  margin: 40px auto;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.10), 0 1.5px 4px rgba(0,0,0,0.08);
  padding: 2.5rem 2rem 2rem 2rem;
}
h2 {
  font-weight: 700;
  font-size: 2rem;
  margin-bottom: 1.5rem;
  color: #2c3e50;
  letter-spacing: 1px;
}
.form-label {
  font-weight: 500;
  color: #34495e;
}
.form-control {
  border-radius: 8px;
  margin-bottom: 1.2rem;
  font-size: 1.1rem;
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ccc;
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
}
.btn-success:hover {
  background: linear-gradient(90deg, #218838 0%, #00aaff 100%);
}
.alert {
  margin-top: 1rem;
}
</style>
