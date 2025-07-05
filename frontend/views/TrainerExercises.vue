<template>
  <div class="trainer-exercises-container">
    <h2>Ejercicios del Entrenador</h2>
    <div v-if="loading">Cargando ejercicios...</div>
    <div v-else>
      <table class="exercise-table">
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Músculo principal</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="exercise in exercises" :key="exercise.id">
            <td>{{ exercise.name }}</td>
            <td>{{ exercise.main_muscle }}</td>
            <td>
              <router-link :to="`/exercises/${exercise.id}`" class="btn btn-info">Ver</router-link>
              <router-link :to="`/exercises/${exercise.id}/edit`" class="btn btn-warning">Editar</router-link>
              <router-link :to="`/exercises/${exercise.id}/delete`" class="btn btn-danger">Eliminar</router-link>
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
  name: 'TrainerExercises',
  data() {
    return {
      exercises: [],
      loading: true,
      error: ''
    }
  },
  async mounted() {
    try {
      const res = await axios.get('https://<TU_BACKEND_RENDER_URL>/api/users/trainer-exercises/', {
        headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
      })
      this.exercises = res.data
    } catch (e) {
      this.error = 'Error al cargar los ejercicios.'
    } finally {
      this.loading = false
    }
  }
}
</script>

<style scoped>
.trainer-exercises-container {
  max-width: 900px;
  margin: 40px auto;
  padding: 24px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #fff;
}
.exercise-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 16px;
}
.exercise-table th, .exercise-table td {
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
