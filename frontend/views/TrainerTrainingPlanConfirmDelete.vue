<template>
  <div class="trainer-training-plan-confirm-delete-container">
    <h2>¿Estás seguro que deseas eliminar este plan de entrenamiento?</h2>
    <div v-if="loading">Cargando información...</div>
    <div v-else-if="plan">
      <p><b>Nombre:</b> {{ plan.name }}</p>
      <button @click="deletePlan" class="btn btn-danger">Eliminar</button>
      <router-link :to="cancelUrl" class="btn btn-secondary">Cancelar</router-link>
      <div v-if="error" class="error">{{ error }}</div>
      <div v-if="success" class="success">{{ success }}</div>
    </div>
    <div v-else>
      <div class="error">No se encontró el plan.</div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'TrainerTrainingPlanConfirmDelete',
  data() {
    return {
      plan: null,
      loading: true,
      error: '',
      success: '',
      cancelUrl: '/trainer/training-plans'
    }
  },
  async mounted() {
    try {
      const res = await axios.get(`https://<TU_BACKEND_RENDER_URL>/api/users/trainer-training-plans/${this.$route.params.id}/`, {
        headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
      })
      this.plan = res.data
    } catch (e) {
      this.error = 'Error al cargar el plan.'
    } finally {
      this.loading = false
    }
  },
  methods: {
    async deletePlan() {
      this.error = ''
      this.success = ''
      try {
        await axios.delete(`https://<TU_BACKEND_RENDER_URL>/api/users/trainer-training-plans/${this.$route.params.id}/`, {
          headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
        })
        this.success = 'Plan eliminado correctamente.'
        setTimeout(() => {
          this.$router.push(this.cancelUrl)
        }, 1000)
      } catch (e) {
        this.error = 'Error al eliminar el plan.'
      }
    }
  }
}
</script>

<style scoped>
.trainer-training-plan-confirm-delete-container {
  max-width: 400px;
  margin: 40px auto;
  padding: 24px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #fff;
  text-align: center;
}
.btn {
  margin: 8px;
}
.error {
  color: red;
  margin-top: 10px;
}
.success {
  color: green;
  margin-top: 10px;
}
</style>
