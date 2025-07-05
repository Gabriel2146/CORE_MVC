<template>
  <div>
    <h1 class="mb-4">Gestión de Ejercicios</h1>
    <div class="mb-3">
      <router-link class="btn btn-secondary me-2" to="/admin">Volver al Dashboard</router-link>
      <router-link class="btn btn-primary me-2" to="/admin/exercises/create">Crear Nuevo Ejercicio</router-link>
      <button class="btn btn-info text-white" @click="syncWger">Sincronizar Ejercicios desde wger</button>
    </div>
    <table class="table table-striped admin-table">
      <thead>
        <tr>
          <th>ID wger</th>
          <th>Nombre</th>
          <th>Descripción</th>
          <th>Categoría</th>
          <th>Equipamiento</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="exercise in exercises" :key="exercise.id">
          <td>{{ exercise.wger_id }}</td>
          <td>{{ exercise.name }}</td>
          <td v-html="exercise.description"></td>
          <td>{{ exercise.category }}</td>
          <td>{{ exercise.equipment }}</td>
          <td>
            <router-link class="btn btn-sm btn-outline-primary" :to="`/admin/exercises/edit/${exercise.id}`">Editar</router-link>
            <button class="btn btn-sm btn-outline-danger ms-1" @click="deleteExercise(exercise.id)">Eliminar</button>
          </td>
        </tr>
        <tr v-if="exercises.length === 0">
          <td colspan="6">No hay ejercicios registrados.</td>
        </tr>
      </tbody>
    </table>
    <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
    <div v-if="success" class="alert alert-success mt-3">{{ success }}</div>
  </div>
</template>

<script>
import axios from 'axios'
import { ref, onMounted } from 'vue'

export default {
  name: 'AdminExercises',
  setup() {
    const exercises = ref([])
    const error = ref('')
    const success = ref('')

    const fetchExercises = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/training/exercises/', {
          headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
        })
        exercises.value = response.data
      } catch (err) {
        error.value = 'Error al cargar los ejercicios'
      }
    }

    const deleteExercise = async (id) => {
      if (!confirm('¿Seguro que deseas eliminar este ejercicio?')) return
      try {
        await axios.delete(`http://localhost:8000/api/training/exercises/${id}/`, {
          headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
        })
        success.value = 'Ejercicio eliminado correctamente'
        fetchExercises()
      } catch (err) {
        error.value = 'Error al eliminar el ejercicio'
      }
    }

    const syncWger = async () => {
      try {
        await axios.post('http://localhost:8000/api/wger-integration/sync/', {}, {
          headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
        })
        success.value = 'Sincronización completada'
        fetchExercises()
      } catch (err) {
        error.value = 'Error al sincronizar con wger'
      }
    }

    onMounted(fetchExercises)

    return { exercises, error, success, deleteExercise, syncWger }
  }
}
</script>

<style scoped>
.admin-table th {
    background: #f5f8fa;
    font-weight: 600;
}
.admin-table td, .admin-table th {
    vertical-align: middle;
}
</style>
