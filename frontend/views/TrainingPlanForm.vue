<template>
  <div>
    <h2>{{ isEdit ? 'Editar Plan de Entrenamiento' : 'Crear Plan de Entrenamiento' }}</h2>
    <form @submit.prevent="handleSubmit">
      <div>
        <label>Nombre:</label>
        <input v-model="form.name" required />
      </div>
      <div>
        <label>Objetivo:</label>
        <input v-model="form.goals" required />
      </div>
      <div>
        <label>Duración (semanas):</label>
        <input v-model.number="form.duration" type="number" min="1" required />
      </div>
      <div>
        <label>Descripción:</label>
        <textarea v-model="form.description"></textarea>
      </div>
      <button type="submit" class="btn btn-primary">{{ isEdit ? 'Guardar Cambios' : 'Crear Plan' }}</button>
      <button @click="$router.back()" type="button" class="btn">Cancelar</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'TrainingPlanForm',
  data() {
    return {
      form: {
        name: '',
        goals: '',
        duration: 4,
        description: ''
      },
      isEdit: false
    }
  },
  async created() {
    if (this.$route.params.id) {
      this.isEdit = true
      try {
        const res = await axios.get(`https://<TU_BACKEND_RENDER_URL>/api/training/training-plans/${this.$route.params.id}/`, {
          headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
        })
        this.form = { ...res.data }
      } catch (e) {
        alert('Error al cargar el plan')
      }
    }
  },
  methods: {
    async handleSubmit() {
      try {
        if (this.isEdit) {
          await axios.put(`https://<TU_BACKEND_RENDER_URL>/api/training/training-plans/${this.$route.params.id}/`, this.form, {
            headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
          })
        } else {
          await axios.post('https://<TU_BACKEND_RENDER_URL>/api/training/training-plans/', this.form, {
            headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
          })
        }
        this.$router.push('/training-plans')
      } catch (e) {
        alert('Error al guardar el plan')
      }
    }
  }
}
</script>

<style scoped>
form > div {
  margin-bottom: 12px;
}
.btn {
  margin-right: 8px;
}
</style>
