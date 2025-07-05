<template>
  <div class="confirm-delete-container">
    <h2>¿Estás seguro que deseas eliminar este elemento?</h2>
    <div v-if="loading">Cargando información...</div>
    <div v-else-if="item">
      <p><b>{{ itemLabel }}:</b> {{ itemName }}</p>
      <button @click="deleteItem" class="btn btn-danger">Eliminar</button>
      <router-link :to="cancelUrl" class="btn btn-secondary">Cancelar</router-link>
      <div v-if="error" class="error">{{ error }}</div>
      <div v-if="success" class="success">{{ success }}</div>
    </div>
    <div v-else>
      <div class="error">No se encontró el elemento.</div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'ConfirmDelete',
  props: {
    apiUrl: { type: String, required: true },
    itemLabel: { type: String, default: 'Nombre' },
    itemNameKey: { type: String, default: 'name' },
    cancelUrl: { type: String, required: true }
  },
  data() {
    return {
      item: null,
      loading: true,
      error: '',
      success: ''
    }
  },
  computed: {
    itemName() {
      return this.item ? this.item[this.itemNameKey] : ''
    }
  },
  async mounted() {
    try {
      const res = await axios.get(this.apiUrl, {
        headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
      })
      this.item = res.data
    } catch (e) {
      this.error = 'Error al cargar el elemento.'
    } finally {
      this.loading = false
    }
  },
  methods: {
    async deleteItem() {
      this.error = ''
      this.success = ''
      try {
        await axios.delete(this.apiUrl, {
          headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
        })
        this.success = 'Elemento eliminado correctamente.'
        setTimeout(() => {
          this.$router.push(this.cancelUrl)
        }, 1000)
      } catch (e) {
        this.error = 'Error al eliminar el elemento.'
      }
    }
  }
}
</script>

<style scoped>
.confirm-delete-container {
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
