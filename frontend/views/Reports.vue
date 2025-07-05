<template>
  <div class="reports-container">
    <h2>Reportes</h2>
    <div v-if="loading">Cargando reportes...</div>
    <div v-else>
      <table class="reports-table">
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Tipo</th>
            <th>Fecha</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="report in reports" :key="report.id">
            <td>{{ report.name }}</td>
            <td>{{ report.type }}</td>
            <td>{{ report.date }}</td>
            <td>
              <router-link :to="`/reports/${report.id}`" class="btn btn-info">Ver</router-link>
              <router-link :to="`/reports/${report.id}/download`" class="btn btn-success">Descargar</router-link>
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
  name: 'Reports',
  data() {
    return {
      reports: [],
      loading: true,
      error: ''
    }
  },
  async mounted() {
    try {
      const res = await axios.get('https://<TU_BACKEND_RENDER_URL>/api/reports/', {
        headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
      })
      this.reports = res.data
    } catch (e) {
      this.error = 'Error al cargar los reportes.'
    } finally {
      this.loading = false
    }
  }
}
</script>

<style scoped>
.reports-container {
  max-width: 900px;
  margin: 40px auto;
  padding: 24px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #fff;
}
.reports-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 16px;
}
.reports-table th, .reports-table td {
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
