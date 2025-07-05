<template>
  <div class="login-container">
    <div class="login-title">Bienvenido a CORE MVC</div>
    <form @submit.prevent="login" autocomplete="off">
      <div class="mb-3 text-start">
        <label for="username" class="form-label">Usuario</label>
        <input type="text" id="username" v-model="username" class="form-control" required autofocus />
      </div>
      <div class="mb-3 text-start">
        <label for="password" class="form-label">Contraseña</label>
        <input type="password" id="password" v-model="password" class="form-control" required />
      </div>
      <button type="submit" class="btn btn-login w-100">Iniciar sesión</button>
    </form>
    <router-link class="login-link" to="/register">¿No tienes cuenta? Regístrate aquí</router-link>
    <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
  </div>
</template>

<script>
import axios from 'axios'
import { useRouter } from 'vue-router'
import { ref } from 'vue'

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

        // Fetch user info to get role
        const userResponse = await axios.get('http://localhost:8000/api/users/profile-api/', {
          headers: { Authorization: 'Bearer ' + response.data.access }
        })
        const user = userResponse.data
        if (user) {
          localStorage.setItem('user_role', user.role)
          // Redirect based on role
          switch (user.role) {
            case 'admin':
              router.push('/admin')
              break
            case 'trainer':
              router.push('/trainer')
              break
            case 'athlete':
              router.push('/athlete')
              break
            case 'guest':
              router.push('/guest')
              break
            default:
              router.push('/')
          }
        } else {
          router.push('/')
        }
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
    margin: 60px auto;
    background: #fff;
    border-radius: 16px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.10), 0 1.5px 4px rgba(0,0,0,0.08);
    padding: 2.5rem 2rem 2rem 2rem;
    text-align: center;
}
.login-title {
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
.btn-login {
    background: linear-gradient(90deg, #007bff 0%, #00c6ff 100%);
    color: #fff;
    font-weight: 600;
    border: none;
    border-radius: 8px;
    padding: 0.7rem 2.5rem;
    font-size: 1.1rem;
    transition: background 0.2s;
    width: 100%;
}
.btn-login:hover {
    background: linear-gradient(90deg, #0056b3 0%, #00aaff 100%);
}
.login-link {
    margin-top: 1.5rem;
    display: block;
    color: #007bff;
    text-decoration: none;
}
.login-link:hover {
    text-decoration: underline;
}
.alert {
    margin-top: 1rem;
}
</style>
