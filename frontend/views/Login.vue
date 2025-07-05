<template>
  <div class="login-container">
    <h2>Iniciar Sesión</h2>
    <form @submit.prevent="login">
      <div>
        <label for="username">Usuario</label>
        <input v-model="username" id="username" type="text" required />
      </div>
      <div>
        <label for="password">Contraseña</label>
        <input v-model="password" id="password" type="password" required />
      </div>
      <button type="submit" class="btn btn-primary">Entrar</button>
      <div v-if="error" class="error">{{ error }}</div>
    </form>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'Login',
  data() {
    return {
      username: '',
      password: '',
      error: ''
    }
  },
  methods: {
    async login() {
      this.error = ''
      try {
        const res = await axios.post('https://<TU_BACKEND_RENDER_URL>/api/users/token/', {
          username: this.username,
          password: this.password
        })
        localStorage.setItem('access_token', res.data.access)
        localStorage.setItem('refresh_token', res.data.refresh)
        this.$router.push('/')
      } catch (e) {
        this.error = 'Usuario o contraseña incorrectos.'
      }
    }
  }
}
</script>

<style scoped>
.login-container {
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
.btn {
  margin-top: 16px;
}
</style>
