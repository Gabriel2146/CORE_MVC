<template>
  <div>
    <h2>Confirmar Eliminación de Plan</h2>
    <div v-if="plan">
      <p>¿Estás seguro que deseas eliminar el plan <strong>{{ plan.name }}</strong>?</p>
      <button @click="deletePlan" class="btn btn-danger">Eliminar</button>
      <button @click="$router.back()" class="btn">Cancelar</button>
    </div>
    <div v-else>
      <em>Cargando plan...</em>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'TrainingPlanConfirmDelete',
  data() {
    return {
      plan: null
    }
  },
  async created() {
    try {
      const res = await axios.get(`https://<TU_BACKEND_RENDER_URL>/api/training/training-plans/${this.$route.params.id}/`, {
        headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
      })
      this.plan = res.data
    } catch (e) {
      alert('Error al cargar el plan')
      this.$router.push('/training-plans')
    }
  },
  methods: {
    async deletePlan() {
      if (!confirm('¿Seguro que deseas eliminar este plan?')) return
      try {
        await axios.delete(`https://<TU_BACKEND_RENDER_URL>/api/training/training-plans/${this.$route.params.id}/`, {
          headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
        })
        this.$router.push('/training-plans')
      } catch (e) {
        alert('Error al eliminar el plan')
      }
    }
  }
}
</script>

<style scoped>
.btn {
  margin-right: 8px;
}
</style>
