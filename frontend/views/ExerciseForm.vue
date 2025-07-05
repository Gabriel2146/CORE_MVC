<template>
  <div class="exercise-form-container">
    <h2>{{ isEdit ? 'Editar Ejercicio' : 'Nuevo Ejercicio' }}</h2>
    <form @submit.prevent="submitForm">
      <div>
        <label for="name">Nombre</label>
        <input v-model="form.name" id="name" type="text" required />
      </div>
      <div>
        <label for="description">Descripción</label>
        <textarea v-model="form.description" id="description" required></textarea>
      </div>
      <div>
        <label for="main_muscle">Músculo principal</label>
        <input v-model="form.main_muscle" id="main_muscle" type="text" required />
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
  name: 'ExerciseForm',
  data() {
    return {
      form: {
        name: '',
        description: '',
        main_muscle: ''
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
        const res = await axios.get(`https://<TU_BACKEND_RENDER_URL>/api/wger/exercises/${this.$route.params.id}/`, {
          headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
        })
        this.form = {
          name: res.data.name,
          description: res.data.description,
          main_muscle: res.data.main_muscle
        }
      } catch (e) {
        this.error = 'Error al cargar el ejercicio.'
      }
    }
  },
  methods: {
    async submitForm() {
      this.error = ''
      this.success = ''
      try {
        if (this.isEdit) {
          await axios.put(`https://<TU_BACKEND_RENDER_URL>/api/wger/exercises/${this.$route.params.id}/`, this.form, {
            headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
          })
          this.success = 'Ejercicio actualizado correctamente.'
        } else {
          await axios.post('https://<TU_BACKEND_RENDER_URL>/api/wger/exercises/', this.form, {
            headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
          })
          this.success = 'Ejercicio creado correctamente.'
          this.form = { name: '', description: '', main_muscle: '' }
        }
      } catch (e) {
        this.error = 'Error al guardar el ejercicio.'
      }
    }
  }
}
</script>

<style scoped>
.exercise-form-container {
  max-width: 500px;
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
