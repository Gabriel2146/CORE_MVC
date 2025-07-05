<template>
  <div>
    <div class="trainer-dashboard-title mb-4">
      <i class="bi bi-person-badge"></i> Bienvenido, {{ username }} (Entrenador)
    </div>
    <ul class="trainer-dashboard-list">
      <li>
        <router-link class="trainer-dashboard-link" to="/trainer/training-plans"><i class="bi bi-list-task"></i> Gestionar Planes de Entrenamiento</router-link>
      </li>
      <li>
        <router-link class="trainer-dashboard-link" to="/trainer/exercises"><i class="bi bi-bar-chart"></i> Catálogo de Ejercicios</router-link>
      </li>
      <li>
        <router-link class="trainer-dashboard-link" to="/trainer/athlete-progress"><i class="bi bi-graph-up-arrow"></i> Progreso de Deportistas</router-link>
      </li>
      <li>
        <router-link class="trainer-dashboard-link" to="/trainer/auto-generate-plan"><i class="bi bi-lightning-charge"></i> Generar plan automático para un deportista</router-link>
      </li>
      <li>
        <router-link class="trainer-dashboard-link" to="/trainer/athlete-report"><i class="bi bi-trophy"></i> Reporte de desempeño de deportistas</router-link>
      </li>
      <li>
        <router-link class="trainer-dashboard-link" to="/trainer/effectiveness-ranking"><i class="bi bi-award"></i> Ranking de efectividad de sesiones</router-link>
      </li>
    </ul>
    <button class="logout-link" @click="logout"><i class="bi bi-box-arrow-right"></i> Cerrar sesión</button>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'DashboardTrainer',
  setup() {
    const username = ref('')
    const router = useRouter()

    onMounted(() => {
      username.value = localStorage.getItem('username') || 'Entrenador'
    })

    const logout = () => {
      localStorage.clear()
      router.push('/login')
    }

    return { username, logout }
  }
}
</script>

<style scoped>
@import url('https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css');
.trainer-dashboard-title {
    font-weight: 700;
    font-size: 2.3rem;
    color: #007bff;
    margin-bottom: 2.2rem;
    letter-spacing: 1px;
    text-align: center;
}
.trainer-dashboard-list {
    list-style: none;
    padding: 0;
    margin: 0 auto;
    max-width: 600px;
}
.trainer-dashboard-list li {
    margin-bottom: 1.2rem;
}
.trainer-dashboard-link {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    padding: 1.2rem 1rem;
    border-radius: 16px;
    background: linear-gradient(90deg, #f8fafd 0%, #eaf6ff 100%);
    color: #007bff;
    font-weight: 600;
    font-size: 1.18rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.07);
    text-decoration: none;
    transition: background 0.15s, color 0.15s, box-shadow 0.15s;
}
.trainer-dashboard-link i {
    font-size: 1.7rem;
    color: #00c6ff;
    min-width: 2.2rem;
    text-align: center;
}
.trainer-dashboard-link:hover {
    background: linear-gradient(90deg, #eaf6ff 0%, #cce6ff 100%);
    color: #0056b3;
    text-decoration: none;
    box-shadow: 0 4px 16px rgba(0,123,255,0.10);
}
.logout-link {
    display: block;
    margin: 2.5rem auto 0 auto;
    color: #dc3545;
    font-weight: 600;
    text-decoration: none;
    font-size: 1.1rem;
    text-align: center;
    background: none;
    border: none;
    cursor: pointer;
}
.logout-link:hover {
    color: #a71d2a;
    text-decoration: underline;
}
</style>
