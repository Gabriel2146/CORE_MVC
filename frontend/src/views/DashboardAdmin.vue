<template>
  <div>
    <div class="admin-dashboard-title mb-4">
      <i class="bi bi-person-gear"></i> Bienvenido, {{ username }} (Administrador)
    </div>
    <ul class="admin-admin-list">
      <li>
        <router-link class="admin-admin-link" to="/admin/exercises"><i class="bi bi-bar-chart"></i> Gestionar Ejercicios</router-link>
      </li>
      <li>
        <router-link class="admin-admin-link" to="/admin/training-plans"><i class="bi bi-list-task"></i> Gestionar Planes de Entrenamiento</router-link>
      </li>
      <li>
        <router-link class="admin-admin-link" to="/admin/users"><i class="bi bi-people"></i> Gestionar Usuarios</router-link>
      </li>
    </ul>
    <button class="logout-link" @click="logout"><i class="bi bi-box-arrow-right"></i> Cerrar sesión</button>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'DashboardAdmin',
  setup() {
    const username = ref('')
    const router = useRouter()

    onMounted(() => {
      // Obtener el nombre de usuario del localStorage o de un API si es necesario
      username.value = localStorage.getItem('username') || 'Administrador'
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
.admin-dashboard-title {
    font-weight: 700;
    font-size: 2.2rem;
    color: #007bff;
    margin-bottom: 2.2rem;
    letter-spacing: 1px;
    text-align: center;
}
.admin-admin-list {
    list-style: none;
    padding: 0;
    margin: 0 auto;
    max-width: 600px;
}
.admin-admin-list li {
    margin-bottom: 1.2rem;
}
.admin-admin-link {
    display: block;
    padding: 1.2rem 1rem;
    border-radius: 14px;
    background: #fff;
    color: #007bff;
    font-weight: 600;
    font-size: 1.15rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.07);
    text-decoration: none;
    transition: background 0.15s, color 0.15s;
}
.admin-admin-link:hover {
    background: #eaf6ff;
    color: #0056b3;
    text-decoration: none;
}
.logout-link {
    display: inline-block;
    margin-top: 2rem;
    color: #dc3545;
    font-weight: 600;
    text-decoration: none;
    font-size: 1.1rem;
    background: none;
    border: none;
    cursor: pointer;
}
.logout-link:hover {
    color: #a71d2a;
    text-decoration: underline;
}
</style>
