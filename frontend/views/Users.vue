<template>
  <div class="users-container">
    <h2>Gestión de Usuarios</h2>
    <router-link to="/users/new" class="btn btn-success">Nuevo Usuario</router-link>
    <div v-if="loading">Cargando usuarios...</div>
    <div v-else>
      <table class="users-table">
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
              <router-link :to="`/users/${user.id}`" class="btn btn-info">Ver</router-link>
              <router-link :to="`/users/${user.id}/edit`" class="btn btn-warning">Editar</router-link>
              <router-link :to="`/users/${user.id}/delete`" class="btn btn-danger">Eliminar</router-link>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-if="error" class="error">{{ error }}</div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'Users',
  data() {
    return {
      users: [],
      loading: true,
      error: ''
    }
  },
  async mounted() {
    try {
      const res = await axios.get('https://<TU_BACKEND_RENDER_URL>/api/users/', {
        headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
      })
      this.users = res.data
    } catch (e) {
      this.error = 'Error al cargar los usuarios.'
    } finally {
      this.loading = false
    }
  }
}
</script>

<style scoped>
.users-container {
  max-width: 900px;
  margin: 40px auto;
  padding: 24px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #fff;
}
.users-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 16px;
}
.users-table th, .users-table td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: left;
}
.btn {
  margin-right: 8px;
}
.error {
  color: red;
  margin-top: 10px;
}
</style>
