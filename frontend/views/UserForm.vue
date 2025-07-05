<template>
  <div class="user-form-container">
    <h2>{{ isEdit ? 'Editar Usuario' : 'Nuevo Usuario' }}</h2>
    <form @submit.prevent="submitForm">
      <div>
        <label for="username">Usuario</label>
        <input v-model="form.username" id="username" type="text" required />
      </div>
      <div>
        <label for="email">Email</label>
        <input v-model="form.email" id="email" type="email" required />
      </div>
      <div>
        <label for="role">Rol</label>
        <select v-model="form.role" id="role" required>
          <option value="">Selecciona un rol</option>
          <option value="admin">Admin</option>
          <option value="trainer">Entrenador</option>
          <option value="athlete">Atleta</option>
          <option value="guest">Invitado</option>
        </select>
      </div>
      <div v-if="!isEdit">
        <label for="password">Contraseña</label>
        <input v-model="form.password" id="password" type="password" required />
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
  name: 'UserForm',
  data() {
    return {
      form: {
        username: '',
        email: '',
        role: '',
        password: ''
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
        const res = await axios.get(`https://<TU_BACKEND_RENDER_URL>/api/users/${this.$route.params.id}/`, {
          headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
        })
        this.form = {
          username: res.data.username,
          email: res.data.email,
          role: res.data.role,
          password: ''
        }
      } catch (e) {
        this.error = 'Error al cargar el usuario.'
      }
    }
  },
  methods: {
    async submitForm() {
      this.error = ''
      this.success = ''
      try {
        if (this.isEdit) {
          await axios.put(`https://<TU_BACKEND_RENDER_URL>/api/users/${this.$route.params.id}/`, this.form, {
            headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
          })
          this.success = 'Usuario actualizado correctamente.'
        } else {
          await axios.post('https://<TU_BACKEND_RENDER_URL>/api/users/', this.form, {
            headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
          })
          this.success = 'Usuario creado correctamente.'
          this.form = { username: '', email: '', role: '', password: '' }
        }
      } catch (e) {
        this.error = 'Error al guardar el usuario.'
      }
    }
  }
}
</script>

<style scoped>
.user-form-container {
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
