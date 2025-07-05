<template>
  <div class="progress-form-container">
    <h2>{{ isEdit ? 'Editar Progreso' : 'Nuevo Progreso' }}</h2>
    <form @submit.prevent="submitForm">
      <div>
        <label for="date">Fecha</label>
        <input v-model="form.date" id="date" type="date" required />
      </div>
      <div>
        <label for="exercise_name">Ejercicio</label>
        <input v-model="form.exercise_name" id="exercise_name" type="text" required />
      </div>
      <div>
        <label for="weight">Peso (kg)</label>
        <input v-model.number="form.weight" id="weight" type="number" min="0" required />
      </div>
      <div>
        <label for="reps">Repeticiones</label>
        <input v-model.number="form.reps" id="reps" type="number" min="1" required />
      </div>
      <div>
        <label for="sets">Series</label>
        <input v-model.number="form.sets" id="sets" type="number" min="1" required />
      </div>
      <button type="submit" class="btn btn-primary">{{ isEdit ? 'Guardar Cambios' : 'Crear' }}</button>
      <div v-if="error" class="error">{{ error }}</div>
      <div v-if="success" class="success">{{ success }}</div>
    </form>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'ProgressForm',
  data() {
    return {
      form: {
        date: '',
        exercise_name: '',
        weight: 0,
        reps: 1,
        sets: 1
      },
      isEdit: false,
      error: '',
      success: ''
    }
  },
  async mounted() {
    if (this.$route.params.id) {
      this.isEdit = true
      try {
        const res = await axios.get(`https://<TU_BACKEND_RENDER_URL>/api/training/progress/${this.$route.params.id}/`, {
          headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
        })
        this.form = {
          date: res.data.date,
          exercise_name: res.data.exercise_name,
          weight: res.data.weight,
          reps: res.data.reps,
          sets: res.data.sets
        }
      } catch (e) {
        this.error = 'Error al cargar el progreso.'
      }
    }
  },
  methods: {
    async submitForm() {
      this.error = ''
      this.success = ''
      try {
        if (this.isEdit) {
          await axios.put(`https://<TU_BACKEND_RENDER_URL>/api/training/progress/${this.$route.params.id}/`, this.form, {
            headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
          })
          this.success = 'Progreso actualizado correctamente.'
        } else {
          await axios.post('https://<TU_BACKEND_RENDER_URL>/api/training/progress/', this.form, {
            headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
          })
          this.success = 'Progreso creado correctamente.'
          this.form = { date: '', exercise_name: '', weight: 0, reps: 1, sets: 1 }
        }
      } catch (e) {
        this.error = 'Error al guardar el progreso.'
      }
    }
  }
}
</script>

<style scoped>
.progress-form-container {
  max-width: 500px;
  margin: 40px auto;
  padding: 24px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #fff;
}
.btn {
  margin-top: 16px;
}
.error {
  color: red;
  margin-top: 10px;
}
.success {
  color: green;
  margin-top: 10px;
}
</style>
