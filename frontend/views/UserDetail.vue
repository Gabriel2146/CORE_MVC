<template>
  <div class="user-detail-container">
    <h2>Detalle de Usuario</h2>
    <div v-if="loading">Cargando usuario...</div>
    <div v-else-if="user">
      <h3>{{ user.username }}</h3>
      <p><b>Email:</b> {{ user.email }}</p>
      <p><b>Rol:</b> {{ user.role }}</p>
      <router-link :to="`/users/${user.id}/edit`" class="btn btn-warning">Editar</router-link>
      <router-link :to="`/users/${user.id}/delete`" class="btn btn-danger">Eliminar</router-link>
    </div>
    <div v-else>
      <div class="error">No se encontró el usuario.</div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'UserDetail',
  data() {
    return {
      user: null,
      loading: true,
      error: ''
    }
  },
  async mounted() {
    try {
      const res = await axios.get(`https://<TU_BACKEND_RENDER_URL>/api/users/${this.$route.params.id}/`, {
        headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
      })
      this.user = res.data
    } catch (e) {
      this.error = 'Error al cargar el usuario.'
    } finally {
      this.loading = false
    }
  }
}
</script>

<style scoped>
.user-detail-container {
  max-width: 500px;
  margin: 40px auto;
  padding: 24px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #fff;
}
.btn {
  margin-right: 8px;
}
.error {
  color: red;
  margin-top: 10px;
}
</style>
