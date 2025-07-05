<template>
  <div class="register-container">
    <h2>Registro</h2>
    <form @submit.prevent="register">
      <div>
        <label for="username">Usuario</label>
        <input v-model="username" id="username" type="text" required />
      </div>
      <div>
        <label for="email">Email</label>
        <input v-model="email" id="email" type="email" required />
      </div>
      <div>
        <label for="password1">Contraseña</label>
        <input v-model="password1" id="password1" type="password" required />
      </div>
      <div>
        <label for="password2">Repetir Contraseña</label>
        <input v-model="password2" id="password2" type="password" required />
      </div>
      <button type="submit" class="btn btn-primary">Registrarse</button>
      <div v-if="error" class="error">{{ error }}</div>
      <div v-if="success" class="success">{{ success }}</div>
    </form>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'Register',
  data() {
    return {
      username: '',
      email: '',
      password1: '',
      password2: '',
      error: '',
      success: ''
    }
  },
  methods: {
    async register() {
      this.error = ''
      this.success = ''
      if (this.password1 !== this.password2) {
        this.error = 'Las contraseñas no coinciden.'
        return
      }
      try {
        await axios.post('https://<TU_BACKEND_RENDER_URL>/api/users/register/', {
          username: this.username,
          email: this.email,
          password: this.password1
        })
        this.success = 'Registro exitoso. Ahora puedes iniciar sesión.'
        this.username = ''
        this.email = ''
        this.password1 = ''
        this.password2 = ''
      } catch (e) {
        this.error = 'Error en el registro. Verifica los datos.'
      }
    }
  }
}
</script>

<style scoped>
.register-container {
  max-width: 400px;
  margin: 40px auto;
  padding: 24px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #fff;
}
.error {
  color: red;
  margin-top: 10px;
}
.success {
  color: green;
  margin-top: 10px;
}
.btn {
  margin-top: 16px;
}
</style>
