<template>
  <div class="plan-form-container">
    <h2>{{ isEdit ? 'Editar Plan de Entrenamiento' : 'Nuevo Plan de Entrenamiento' }}</h2>
    <form @submit.prevent="submitForm">
      <div>
        <label for="name">Nombre</label>
        <input v-model="form.name" id="name" type="text" required />
      </div>
      <div>
        <label for="athlete_name">Atleta</label>
        <input v-model="form.athlete_name" id="athlete_name" type="text" required />
      </div>
      <div>
        <label for="trainer_name">Entrenador</label>
        <input v-model="form.trainer_name" id="trainer_name" type="text" required />
      </div>
      <div>
        <label for="duration">Duración (semanas)</label>
        <input v-model.number="form.duration" id="duration" type="number" min="1" required />
      </div>
      <div>
        <label for="sessions">Sesiones (un día y descripción por línea, ej: Lunes: Pecho y tríceps)</label>
        <textarea v-model="form.sessions" id="sessions" required></textarea>
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
  name: 'PlanForm',
  data() {
    return {
      form: {
        name: '',
        athlete_name: '',
        trainer_name: '',
        duration: 4,
        sessions: ''
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
        const res = await axios.get(`https://<TU_BACKEND_RENDER_URL>/api/training/plans/${this.$route.params.id}/`, {
          headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
        })
        this.form = {
          name: res.data.name,
          athlete_name: res.data.athlete_name,
          trainer_name: res.data.trainer_name,
          duration: res.data.duration,
          sessions: res.data.sessions ? res.data.sessions.map(s => `${s.day}: ${s.description}`).join('\n') : ''
        }
      } catch (e) {
        this.error = 'Error al cargar el plan.'
      }
    }
  },
  methods: {
    async submitForm() {
      this.error = ''
      this.success = ''
      // Convertir sesiones de texto a array de objetos
      const sessionsArr = this.form.sessions.split('\n').map(line => {
        const [day, ...desc] = line.split(':')
        return { day: day.trim(), description: desc.join(':').trim() }
      })
      const payload = { ...this.form, sessions: sessionsArr }
      try {
        if (this.isEdit) {
          await axios.put(`https://<TU_BACKEND_RENDER_URL>/api/training/plans/${this.$route.params.id}/`, payload, {
            headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
          })
          this.success = 'Plan actualizado correctamente.'
        } else {
          await axios.post('https://<TU_BACKEND_RENDER_URL>/api/training/plans/', payload, {
            headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
          })
          this.success = 'Plan creado correctamente.'
          this.form = { name: '', athlete_name: '', trainer_name: '', duration: 4, sessions: '' }
        }
      } catch (e) {
        this.error = 'Error al guardar el plan.'
      }
    }
  }
}
</script>

<style scoped>
.plan-form-container {
  max-width: 600px;
  margin: 40px auto;
  padding: 24px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #fff;
}
textarea {
  width: 100%;
  min-height: 80px;
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
