<template>
  <div>
    <h1 class="mb-4">Gestión de Usuarios</h1>
    <div class="mb-3">
      <router-link class="btn btn-secondary me-2" to="/admin">Volver al Dashboard</router-link>
      <router-link class="btn btn-primary" to="/admin/users/create">Crear Nuevo Usuario</router-link>
    </div>
    <table class="table table-striped admin-table">
      <thead>
        <tr>
          <th>Usuario</th>
          <th>Email</th>
          <th>Rol</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id">
          <td>{{ user.username }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user.role }}</td>
          <td>
            <router-link class="btn btn-sm btn-outline-primary" :to="`/admin/users/edit/${user.id}`">Editar</router-link>
            <button class="btn btn-sm btn-outline-danger ms-1" @click="deleteUser(user.id)">Eliminar</button>
          </td>
        </tr>
        <tr v-if="users.length === 0">
          <td colspan="4">No hay usuarios registrados.</td>
        </tr>
      </tbody>
    </table>
    <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
    <div v-if="success" class="alert alert-success mt-3">{{ success }}</div>
  </div>
</template>

<script>
import axios from 'axios'
import { ref, onMounted } from 'vue'

export default {
  name: 'AdminUsers',
  setup() {
    const users = ref([])
    const error = ref('')
    const success = ref('')

    const fetchUsers = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/users/list-api/', {
          headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
        })
        users.value = response.data
      } catch (err) {
        error.value = 'Error al cargar los usuarios'
      }
    }

    const deleteUser = async (id) => {
      if (!confirm('¿Seguro que deseas eliminar este usuario?')) return
      try {
        await axios.delete(`http://localhost:8000/api/users/${id}/`, {
          headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
        })
        success.value = 'Usuario eliminado correctamente'
        fetchUsers()
      } catch (err) {
        error.value = 'Error al eliminar el usuario'
      }
    }

    onMounted(fetchUsers)

    return { users, error, success, deleteUser }
  }
}
</script>

<style scoped>
.admin-table th {
    background: #f5f8fa;
    font-weight: 600;
}
.admin-table td, .admin-table th {
    vertical-align: middle;
}
</style>
