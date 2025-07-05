<template>
  <div>
    <h2>Progreso del Deportista</h2>
    <button @click="fetchProgress">Actualizar</button>
    <ul v-if="progress.length">
      <li v-for="entry in progress" :key="entry.id">
        Fecha: {{ entry.date }} - Valor: {{ entry.value }}
      </li>
    </ul>
    <div v-else>
      <em>No hay datos de progreso disponibles.</em>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'AthleteProgress',
  data() {
    return {
      progress: []
    }
  },
  methods: {
    async fetchProgress() {
      try {
        const res = await axios.get('https://<TU_BACKEND_RENDER_URL>/api/training/progress/', {
          headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
        })
        this.progress = res.data
      } catch (e) {
        this.progress = []
      }
    }
  },
  mounted() {
    this.fetchProgress()
  }
}
</script>

<style scoped>
button {
  margin-bottom: 12px;
}
</style>
