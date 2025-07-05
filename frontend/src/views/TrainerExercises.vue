<template>
  <div>
    <div class="trainer-section-title"><i class="bi bi-bar-chart"></i> Catálogo de Ejercicios</div>
    <form class="row g-2 mb-3 justify-content-center trainer-exercise-filter" @submit.prevent="fetchExercises">
      <div class="col-md-5 col-12 mb-2 mb-md-0">
        <input type="text" v-model="query" class="form-control" placeholder="Buscar por nombre" />
      </div>
      <div class="col-md-5 col-12 mb-2 mb-md-0">
        <input type="text" v-model="category" class="form-control" placeholder="Categoría" />
      </div>
      <div class="col-md-2 col-12">
        <button type="submit" class="btn btn-primary w-100"><i class="bi bi-funnel"></i> Filtrar</button>
      </div>
    </form>
    <div class="table-responsive">
      <table class="table table-hover table-striped trainer-exercise-table align-middle">
        <thead>
          <tr>
            <th>Tipo</th>
            <th>ID wger</th>
            <th>Nombre</th>
            <th>Categoría</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="exercise in exercises" :key="exercise.id">
            <td><span class="badge bg-info text-dark">{{ exercise.type }}</span></td>
            <td>{{ exercise.wger_id }}</td>
            <td class="fw-semibold">{{ exercise.name }}</td>
            <td>{{ exercise.category }}</td>
            <td>
              <router-link class="btn btn-sm btn-outline-info" :to="`/trainer/exercises/${exercise.type}/${exercise.id}`"><i class="bi bi-eye"></i> Ver detalle</router-link>
            </td>
          </tr>
          <tr v-if="exercises.length === 0">
            <td colspan="5">No hay ejercicios disponibles.</td>
          </tr>
        </tbody>
      </table>
    </div>
    <router-link class="btn btn-secondary mt-3" to="/trainer"><i class="bi bi-arrow-left"></i> Volver al Dashboard</router-link>
    <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
  </div>
</template>

<script>
import axios from 'axios'
import { ref } from 'vue'

export default {
  name: 'TrainerExercises',
  setup() {
    const exercises = ref([])
    const query = ref('')
    const category = ref('')
    const error = ref('')

    const fetchExercises = async () => {
      try {
        const params = {}
        if (query.value) params.q = query.value
        if (category.value) params.category = category.value
        const response = await axios.get('http://localhost:8000/api/training/exercises/', {
          headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') },
          params
        })
        exercises.value = response.data
      } catch (err) {
        error.value = 'Error al cargar los ejercicios'
      }
    }

    // Cargar ejercicios al montar
    fetchExercises()

    return { exercises, query, category, error, fetchExercises }
  }
}
</script>

<style scoped>
@import url('https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css');
.trainer-section-title {
    font-size: 1.8rem;
    font-weight: 700;
    color: #007bff;
    margin-bottom: 2rem;
    letter-spacing: 0.5px;
    text-align: center;
}
.trainer-exercise-filter {
    max-width: 700px;
    margin: 0 auto 2rem auto;
    background: #f8fafd;
    border-radius: 14px;
    padding: 1.5rem 2rem 1rem 2rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}
.trainer-exercise-table th {
    background: #f5f8fa;
    font-weight: 600;
    text-align: center;
}
.trainer-exercise-table td, .trainer-exercise-table th {
    vertical-align: middle;
    text-align: center;
}
.trainer-exercise-table .bi {
    color: #00c6ff;
    font-size: 1.1rem;
    margin-right: 0.3rem;
}
.trainer-exercise-table tr {
    transition: background 0.12s;
}
.trainer-exercise-table tr:hover {
    background: #eaf6ff;
}
@media (max-width: 768px) {
    .trainer-exercise-filter { padding: 1rem 0.5rem; }
}
</style>
