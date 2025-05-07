<template>
  <div class="login-container">
    <h2>Iniciar Sesión</h2>
    <form @submit.prevent="login">
      <div>
        <label for="username">Usuario:</label>
        <input id="username" v-model="username" required />
      </div>
      <div>
        <label for="password">Contraseña:</label>
        <input id="password" type="password" v-model="password" required />
      </div>
      <button type="submit">Entrar</button>
    </form>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script>
import axios from 'axios'
import { useRouter } from 'vue-router'

export default {
  name: 'Login',
  setup() {
    const router = useRouter()
    const username = ref('')
    const password = ref('')
    const error = ref('')

    const login = async () => {
      try {
        const response = await axios.post('http://localhost:8000/api/users/token/', {
          username: username.value,
          password: password.value
        })
        localStorage.setItem('access_token', response.data.access)
        localStorage.setItem('refresh_token', response.data.refresh)
        axios.defaults.headers.common['Authorization'] = 'Bearer ' + response.data.access
        router.push('/')
      } catch (err) {
        error.value = 'Credenciales inválidas'
      }
    }

    return { username, password, error, login }
  }
}
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 2rem auto;
  padding: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.error {
  color: red;
  margin-top: 1rem;
}
</style>
