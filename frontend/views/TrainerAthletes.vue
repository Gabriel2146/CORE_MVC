<template>
  <div class="trainer-athletes-container">
    <h2>Mis Atletas</h2>
    <div v-if="loading">Cargando atletas...</div>
    <div v-else>
      <table class="athletes-table">
        <thead>
          <tr>
            <th>Nombre de Usuario</th>
            <th>Email</th>
            <th>Progreso</th>
            <th>Planes</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="athlete in athletes" :key="athlete.id">
            <td>{{ athlete.username }}</td>
            <td>{{ athlete.email }}</td>
            <td>
              <router-link :to="`/athlete/${athlete.id}/progress`" class="btn btn-info">Ver Progreso</router-link>
            </td>
            <td>
              <router-link :to="`/athlete/${athlete.id}/plans`" class="btn btn-info">Ver Planes</router-link>
            </td>
            <td>
              <router-link :to="`/athlete/${athlete.id}/report`" class="btn btn-success">Reporte</router-link>
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
  name: 'TrainerAthletes',
  data() {
    return {
      athletes: [],
      loading: true,
      error: ''
    }
  },
  async mounted() {
    try {
      const res = await axios.get('https://<TU_BACKEND_RENDER_URL>/api/users/trainer-athletes/', {
        headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
      })
      this.athletes = res.data
    } catch (e) {
      this.error = 'Error al cargar los atletas.'
    } finally {
      this.loading = false
    }
  }
}
</script>

<style scoped>
.trainer-athletes-container {
  max-width: 900px;
  margin: 40px auto;
  padding: 24px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #fff;
}
.athletes-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 16px;
}
.athletes-table th, .athletes-table td {
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
