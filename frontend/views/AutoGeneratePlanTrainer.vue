<template>
  <div class="auto-generate-plan-trainer-container">
    <h2>Generar Plan Automático para Atleta</h2>
    <form @submit.prevent="generatePlan">
      <div>
        <label for="athlete">Atleta</label>
        <input v-model="athlete" id="athlete" type="text" required />
      </div>
      <div>
        <label for="goal">Objetivo</label>
        <select v-model="goal" id="goal" required>
          <option value="">Selecciona un objetivo</option>
          <option value="fuerza">Fuerza</option>
          <option value="hipertrofia">Hipertrofia</option>
          <option value="resistencia">Resistencia</option>
        </select>
      </div>
      <div>
        <label for="duration">Duración (semanas)</label>
        <input v-model.number="duration" id="duration" type="number" min="1" required />
      </div>
      <button type="submit" class="btn btn-primary">Generar</button>
    </form>
    <div v-if="loading">Generando plan...</div>
    <div v-if="error" class="error">{{ error }}</div>
    <div v-if="plan" class="plan-result">
      <h3>Plan Generado</h3>
      <pre>{{ plan }}</pre>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'AutoGeneratePlanTrainer',
  data() {
    return {
      athlete: '',
      goal: '',
      duration: 4,
      loading: false,
      error: '',
      plan: null
    }
  },
  methods: {
    async generatePlan() {
      this.loading = true
      this.error = ''
      this.plan = null
      try {
        const res = await axios.post('https://<TU_BACKEND_RENDER_URL>/api/training/auto-generate-plan-trainer/', {
          athlete: this.athlete,
          goal: this.goal,
          duration: this.duration
        }, {
          headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
        })
        this.plan = res.data
      } catch (e) {
        this.error = 'Error al generar el plan.'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.auto-generate-plan-trainer-container {
  max-width: 500px;
  margin: 40px auto;
  padding: 24px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #fff;
}
.plan-result {
  margin-top: 24px;
  background: #f7f7f7;
  padding: 16px;
  border-radius: 6px;
}
.error {
  color: red;
  margin-top: 10px;
}
.btn {
  margin-top: 16px;
}
</style>
