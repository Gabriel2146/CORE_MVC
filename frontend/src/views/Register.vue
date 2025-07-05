<template>
  <div class="register-container">
    <div class="register-title">Crea tu cuenta</div>
    <form @submit.prevent="register" autocomplete="off">
      <div class="mb-3 text-start">
        <label for="username" class="form-label">Usuario</label>
        <input id="username" v-model="username" class="form-control" required />
      </div>
      <div class="mb-3 text-start">
        <label for="email" class="form-label">Correo electrónico</label>
        <input id="email" type="email" v-model="email" class="form-control" required />
      </div>
      <div class="mb-3 text-start">
        <label for="password" class="form-label">Contraseña</label>
        <input id="password" type="password" v-model="password" class="form-control" required />
      </div>
      <div class="mb-3 text-start">
        <label for="password2" class="form-label">Confirmar Contraseña</label>
        <input id="password2" type="password" v-model="password2" class="form-control" required />
      </div>
      <div class="mb-3 text-start">
        <label for="role" class="form-label">Rol</label>
        <select id="role" v-model="role" class="form-control" required>
          <option value="guest">Invitado</option>
          <option value="athlete">Deportista</option>
          <option value="trainer">Entrenador</option>
        </select>
      </div>
      <button type="submit" class="btn btn-register w-100">Registrar</button>
    </form>
    <router-link class="register-link" to="/login">¿Ya tienes cuenta? Inicia sesión aquí</router-link>
    <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
    <div v-if="success" class="alert alert-success mt-3">{{ success }}</div>
  </div>
</template>

<script>
import axios from 'axios'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'Register',
  setup() {
    const router = useRouter()
    const username = ref('')
    const email = ref('')
    const password = ref('')
    const password2 = ref('')
    const role = ref('guest')
    const error = ref('')
    const success = ref('')

    const register = async () => {
      error.value = ''
      success.value = ''
      if (password.value !== password2.value) {
        error.value = 'Las contraseñas no coinciden'
        return
      }
      try {
        await axios.post('http://localhost:8000/api/users/register/', {
          username: username.value,
          email: email.value,
          password: password.value,
          role: role.value
        })
        success.value = 'Registro exitoso. Ahora puedes iniciar sesión.'
        setTimeout(() => router.push('/login'), 1500)
      } catch (err) {
        error.value = 'Error al registrar usuario'
      }
    }

    return { username, email, password, password2, role, error, success, register }
  }
}
</script>

<style scoped>
.register-container {
    max-width: 440px;
    margin: 60px auto;
    background: #fff;
    border-radius: 16px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.10), 0 1.5px 4px rgba(0,0,0,0.08);
    padding: 2.5rem 2rem 2rem 2rem;
    text-align: center;
}
.register-title {
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
.btn-register {
    background: linear-gradient(90deg, #00c6ff 0%, #007bff 100%);
    color: #fff;
    font-weight: 600;
    border: none;
    border-radius: 8px;
    padding: 0.7rem 2.5rem;
    font-size: 1.1rem;
    transition: background 0.2s;
    width: 100%;
}
.btn-register:hover {
    background: linear-gradient(90deg, #00aaff 0%, #0056b3 100%);
}
.register-link {
    margin-top: 1.5rem;
    display: block;
    color: #007bff;
    text-decoration: none;
}
.register-link:hover {
    text-decoration: underline;
}
.alert {
    margin-top: 1rem;
}
</style>
