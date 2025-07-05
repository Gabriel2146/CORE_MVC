<template>
  <div class="report-form-container">
    <h2>{{ isEdit ? 'Editar Reporte' : 'Nuevo Reporte' }}</h2>
    <form @submit.prevent="submitForm">
      <div>
        <label for="name">Nombre</label>
        <input v-model="form.name" id="name" type="text" required />
      </div>
      <div>
        <label for="type">Tipo</label>
        <input v-model="form.type" id="type" type="text" required />
      </div>
      <div>
        <label for="date">Fecha</label>
        <input v-model="form.date" id="date" type="date" required />
      </div>
      <div>
        <label for="content">Contenido</label>
        <textarea v-model="form.content" id="content" required></textarea>
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
  name: 'ReportForm',
  data() {
    return {
      form: {
        name: '',
        type: '',
        date: '',
        content: ''
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
        const res = await axios.get(`https://<TU_BACKEND_RENDER_URL>/api/reports/${this.$route.params.id}/`, {
          headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
        })
        this.form = {
          name: res.data.name,
          type: res.data.type,
          date: res.data.date,
          content: res.data.content
        }
      } catch (e) {
        this.error = 'Error al cargar el reporte.'
      }
    }
  },
  methods: {
    async submitForm() {
      this.error = ''
      this.success = ''
      try {
        if (this.isEdit) {
          await axios.put(`https://<TU_BACKEND_RENDER_URL>/api/reports/${this.$route.params.id}/`, this.form, {
            headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
          })
          this.success = 'Reporte actualizado correctamente.'
        } else {
          await axios.post('https://<TU_BACKEND_RENDER_URL>/api/reports/', this.form, {
            headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
          })
          this.success = 'Reporte creado correctamente.'
          this.form = { name: '', type: '', date: '', content: '' }
        }
      } catch (e) {
        this.error = 'Error al guardar el reporte.'
      }
    }
  }
}
</script>

<style scoped>
.report-form-container {
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
