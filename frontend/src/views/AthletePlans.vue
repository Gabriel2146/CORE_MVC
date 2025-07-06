<template>
  <div class="athlete-plans-container">
    <h1>Planes de Entrenamiento</h1>
    <ul>
      <li v-for="plan in plans" :key="plan.id">
        <strong>{{ plan.name }}</strong> ({{ plan.created_at ? plan.created_at.slice(0,10) : '' }}) - Objetivo: {{ plan.goals || plan.goal }}
        <form class="mt-2" @submit.prevent="submitFeedback(plan.id, plan.newComment)">
          <textarea v-model="plan.newComment" rows="2" placeholder="Deja tu comentario sobre este plan..." required></textarea>
          <button type="submit">Enviar feedback</button>
        </form>
        <ul>
          <li v-if="plan.feedbacks && plan.feedbacks.length" v-for="fb in plan.feedbacks" :key="fb.id">
            <em>{{ fb.user }}</em> ({{ fb.created_at ? fb.created_at.slice(0,16).replace('T',' ') : '' }}): {{ fb.comment }}
          </li>
          <li v-else>No hay comentarios.</li>
        </ul>
      </li>
      <li v-if="plans.length === 0">No tienes planes asignados.</li>
    </ul>
    <router-link class="btn btn-outline-primary mt-3" to="/athlete">Volver al Dashboard</router-link>
  </div>
</template>

<script>
import axios from 'axios'
import { ref, onMounted } from 'vue'

export default {
  name: 'AthletePlans',
  setup() {
    const plans = ref([])

    const fetchPlans = async () => {
      try {
        const token = localStorage.getItem('access_token')
        const res = await axios.get('http://localhost:8000/api/training/plans/?athlete_id=self', {
          headers: { Authorization: 'Bearer ' + token }
        })
        // Suponiendo que cada plan trae feedbacks como array
        plans.value = res.data.map(plan => ({ ...plan, newComment: '', feedbacks: plan.feedbacks || [] }))
      } catch (err) {
        plans.value = []
      }
    }

    const submitFeedback = async (planId, comment) => {
      if (!comment) return
      try {
        const token = localStorage.getItem('access_token')
        await axios.post('http://localhost:8000/api/training/plan-feedback/', {
          plan_id: planId,
          comment
        }, {
          headers: { Authorization: 'Bearer ' + token }
        })
        // Limpiar comentario y recargar feedbacks
        const plan = plans.value.find(p => p.id === planId)
        if (plan) plan.newComment = ''
        fetchPlans()
      } catch (err) {}
    }

    onMounted(fetchPlans)

    return { plans, submitFeedback }
  }
}
</script>

<style scoped>
.athlete-plans-container {
  max-width: 900px;
  margin: 40px auto;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.10), 0 1.5px 4px rgba(0,0,0,0.08);
  padding: 2.5rem 2rem 2rem 2rem;
}
h1 {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  color: #2c3e50;
}
</style>
