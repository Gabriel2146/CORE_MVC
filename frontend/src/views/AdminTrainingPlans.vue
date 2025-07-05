<template>
  <div>
    <div class="admin-section-title">Gestión de Planes de Entrenamiento</div>
    <div class="mb-3">
      <router-link class="btn btn-secondary me-2 btn-back" to="/admin">Volver al Dashboard</router-link>
      <router-link class="btn btn-primary" to="/admin/training-plans/create">Crear Nuevo Plan</router-link>
    </div>
    <ul class="admin-plan-list">
      <li v-for="plan in plans" :key="plan.id">
        <span class="plan-label"><i class="bi bi-list-task"></i> {{ plan.name }}</span>
        <span class="plan-user">Usuario: {{ plan.user }}</span>
        <div>
          <router-link class="btn btn-sm btn-outline-primary me-1" :to="`/admin/training-plans/edit/${plan.id}`">Editar</router-link>
          <button class="btn btn-sm btn-outline-danger" @click="deletePlan(plan.id)">Eliminar</button>
        </div>
      </li>
      <li v-if="plans.length === 0">No hay planes registrados.</li>
    </ul>
    <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
    <div v-if="success" class="alert alert-success mt-3">{{ success }}</div>
  </div>
</template>

<script>
import axios from 'axios'
import { ref, onMounted } from 'vue'

export default {
  name: 'AdminTrainingPlans',
  setup() {
    const plans = ref([])
    const error = ref('')
    const success = ref('')

    const fetchPlans = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/training/plans/', {
          headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
        })
        plans.value = response.data
      } catch (err) {
        error.value = 'Error al cargar los planes'
      }
    }

    const deletePlan = async (id) => {
      if (!confirm('¿Seguro que deseas eliminar este plan?')) return
      try {
        await axios.delete(`http://localhost:8000/api/training/plans/${id}/`, {
          headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
        })
        success.value = 'Plan eliminado correctamente'
        fetchPlans()
      } catch (err) {
        error.value = 'Error al eliminar el plan'
      }
    }

    onMounted(fetchPlans)

    return { plans, error, success, deletePlan }
  }
}
</script>

<style scoped>
@import url('https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css');
.admin-section-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: #007bff;
    margin-bottom: 1.5rem;
    letter-spacing: 0.5px;
    text-align: center;
}
.admin-plan-list {
    max-width: 700px;
    margin: 0 auto 2rem auto;
    padding: 0;
    list-style: none;
}
.admin-plan-list li {
    background: #fff;
    border-radius: 14px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.07);
    margin-bottom: 1.1rem;
    padding: 1.2rem 1.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 1.13rem;
    font-weight: 500;
}
.admin-plan-list .plan-label {
    color: #007bff;
    font-weight: 700;
    font-size: 1.1rem;
}
.admin-plan-list .plan-user {
    color: #34495e;
    font-size: 1rem;
    margin-left: 0.7rem;
}
.admin-plan-list .bi {
    font-size: 1.3rem;
    margin-right: 0.7rem;
    color: #00c6ff;
}
.btn-back {
    margin-right: 1rem;
}
</style>
