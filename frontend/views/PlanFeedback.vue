<template>
  <div class="plan-feedback-container">
    <h2>Feedback del Plan</h2>
    <form @submit.prevent="submitFeedback">
      <div>
        <label for="rating">Calificación</label>
        <select v-model="form.rating" id="rating" required>
          <option value="">Selecciona</option>
          <option value="1">1 - Muy malo</option>
          <option value="2">2 - Malo</option>
          <option value="3">3 - Regular</option>
          <option value="4">4 - Bueno</option>
          <option value="5">5 - Excelente</option>
        </select>
      </div>
      <div>
        <label for="comment">Comentario</label>
        <textarea v-model="form.comment" id="comment" required></textarea>
      </div>
      <button type="submit" class="btn btn-primary">Enviar Feedback</button>
      <div v-if="error" class="error">{{ error }}</div>
      <div v-if="success" class="success">{{ success }}</div>
    </form>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'PlanFeedback',
  data() {
    return {
      form: {
        rating: '',
        comment: ''
      },
      error: '',
      success: ''
    }
  },
  methods: {
    async submitFeedback() {
      this.error = ''
      this.success = ''
      try {
        await axios.post(`https://<TU_BACKEND_RENDER_URL>/api/training/plan-feedback/`, {
          plan: this.$route.params.id,
          rating: this.form.rating,
          comment: this.form.comment
        }, {
          headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
        })
        this.success = '¡Gracias por tu feedback!'
        this.form = { rating: '', comment: '' }
      } catch (e) {
        this.error = 'Error al enviar el feedback.'
      }
    }
  }
}
</script>

<style scoped>
.plan-feedback-container {
  max-width: 500px;
  margin: 40px auto;
  padding: 24px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #fff;
}
textarea {
  width: 100%;
  min-height: 80px;
}
.btn {
  margin-top: 16px;
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
