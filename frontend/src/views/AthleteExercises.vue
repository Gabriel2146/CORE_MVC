<template>
  <div class="athlete-exercises-container">
    <h1>Mis Ejercicios</h1>
    <form class="mb-3" @submit.prevent>
      <label for="plan_id">Selecciona un plan:</label>
      <select v-model="selectedPlanId" id="plan_id" @change="fetchExercises" class="form-select d-inline w-auto">
        <option value="">-- Selecciona --</option>
        <option v-for="plan in plans" :key="plan.id" :value="plan.id">{{ plan.name }}</option>
      </select>
    </form>
    <div v-if="selectedPlan">
      <h2>Ejercicios del plan: {{ selectedPlan.name }}</h2>
      <div v-if="mensaje" class="alert alert-warning">{{ mensaje }}</div>
      <table class="table table-bordered">
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Categoría</th>
            <th>Grupo muscular</th>
            <th>Dificultad</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="exercise in exercises" :key="exercise.id">
            <td>{{ exercise.name }}</td>
            <td>{{ exercise.category }}</td>
            <td>{{ exercise.muscle_group }}</td>
            <td>{{ exercise.difficulty }}</td>
            <td><router-link :to="`/athlete/exercise/${exercise.id}`">Ver detalle</router-link></td>
          </tr>
          <tr v-if="exercises.length === 0">
            <td colspan="5">No hay ejercicios asignados en este plan.</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else>
      <p>Selecciona un plan para ver los ejercicios asignados.</p>
    </div>
    <router-link class="btn btn-outline-primary mt-3" to="/athlete">Volver al Dashboard</router-link>
  </div>
</template>

<script>
import axios from 'axios'
import { ref, computed, onMounted } from 'vue'

export default {
  name: 'AthleteExercises',
  setup() {
    const plans = ref([])
    const selectedPlanId = ref('')
    const selectedPlan = computed(() => plans.value.find(p => p.id == selectedPlanId.value))
    const exercises = ref([])
    const mensaje = ref('')

    const fetchPlans = async () => {
      try {
        const token = localStorage.getItem('access_token')
        const res = await axios.get('http://localhost:8000/api/training/plans/?athlete_id=self', {
          headers: { Authorization: 'Bearer ' + token }
        })
        plans.value = res.data
      } catch (err) {
        mensaje.value = 'No se pudieron cargar los planes.'
      }
    }

    const fetchExercises = async () => {
      if (!selectedPlanId.value) return
      try {
        const token = localStorage.getItem('access_token')
        const res = await axios.get(`http://localhost:8000/api/training/exercises/?plan_id=${selectedPlanId.value}`, {
          headers: { Authorization: 'Bearer ' + token }
        })
        exercises.value = res.data
        mensaje.value = ''
      } catch (err) {
        mensaje.value = 'No se pudieron cargar los ejercicios.'
      }
    }

    onMounted(fetchPlans)

    return {
      plans,
      selectedPlanId,
      selectedPlan,
      exercises,
      mensaje,
      fetchExercises
    }
  }
}
</script>

<style scoped>
.athlete-exercises-container {
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
.table {
  border-radius: 10px;
  overflow: hidden;
  background: #f8f9fa;
}
.alert {
  margin-top: 1rem;
}
</style>
