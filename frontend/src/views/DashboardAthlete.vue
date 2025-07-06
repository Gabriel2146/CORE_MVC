<template>
  <div class="athlete-dashboard-container">
    <h1>Bienvenido, {{ user?.username }} (Deportista)</h1>
    <p>Panel de deportista.</p>
    <h2>Acciones rápidas</h2>
    <ul class="quick-actions">
      <li><router-link to="/athlete/auto-generate-plan">Generar plan automático</router-link></li>
      <li><router-link to="/athlete/progress-graph">Ver gráfico de progreso</router-link></li>
      <li><router-link to="/athlete/plans">Ver mis planes</router-link></li>
      <li><router-link to="/athlete/exercises">Ver mis ejercicios</router-link></li>
      <li><router-link to="/athlete/progress-form">Registrar progreso</router-link></li>
    </ul>
    <h2>Menú</h2>
    <ul class="main-menu">
      <li><router-link to="/athlete/plans">Mis Planes de Entrenamiento</router-link></li>
      <li><router-link to="/athlete/exercises">Mis Ejercicios</router-link></li>
      <li><router-link to="/athlete/progress">Mi Progreso</router-link></li>
      <li><a href="#" @click.prevent="logout">Cerrar sesión</a></li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'DashboardAthlete',
  setup() {
    const user = ref(null)
    const router = useRouter()

    const fetchUser = async () => {
      try {
        const token = localStorage.getItem('access_token')
        const res = await axios.get('http://localhost:8000/api/users/profile-api/', {
          headers: { Authorization: 'Bearer ' + token }
        })
        user.value = res.data
      } catch (err) {
        user.value = { username: 'Usuario' }
      }
    }

    const logout = () => {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user_role')
      delete axios.defaults.headers.common['Authorization']
      router.push('/login')
    }

    onMounted(fetchUser)

    return { user, logout }
  }
}
</script>

<style scoped>
.athlete-dashboard-container {
  max-width: 600px;
  margin: 40px auto;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.10), 0 1.5px 4px rgba(0,0,0,0.08);
  padding: 2.5rem 2rem 2rem 2rem;
}
h1 {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 1rem;
  color: #2c3e50;
}
h2 {
  font-size: 1.3rem;
  font-weight: 600;
  margin-top: 2rem;
  margin-bottom: 1rem;
  color: #007bff;
}
.quick-actions, .main-menu {
  list-style: none;
  padding: 0;
  margin-bottom: 1.5rem;
}
.quick-actions li, .main-menu li {
  margin-bottom: 0.7rem;
}
.quick-actions a, .main-menu a {
  color: #007bff;
  text-decoration: none;
  font-weight: 500;
  font-size: 1.1rem;
  transition: color 0.2s;
}
.quick-actions a:hover, .main-menu a:hover {
  text-decoration: underline;
  color: #0056b3;
}
</style>
