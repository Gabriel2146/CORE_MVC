<template>
  <div>
    <h1>Bienvenido a la Plataforma de Entrenamiento</h1>
    <p>Esta es la página principal. Selecciona una opción del menú según tu rol.</p>
    <div v-if="role === 'admin'">
      <p>Eres Administrador. Puedes gestionar la plataforma.</p>
      <router-link to="/admin">Ir al Panel de Administrador</router-link>
    </div>
    <div v-else-if="role === 'trainer'">
      <p>Eres Entrenador. Puedes diseñar planes y monitorear deportistas.</p>
      <router-link to="/trainer">Ir al Panel de Entrenador</router-link>
    </div>
    <div v-else-if="role === 'athlete'">
      <p>Eres Deportista. Puedes ver tus planes y registrar avances.</p>
      <router-link to="/athlete">Ir al Panel de Deportista</router-link>
    </div>
    <div v-else-if="role === 'guest'">
      <p>Eres Invitado. Acceso limitado a contenido público.</p>
      <router-link to="/guest">Ir al Panel de Invitado</router-link>
    </div>
    <div v-else>
      <p>Por favor, inicia sesión.</p>
      <router-link to="/login">Iniciar Sesión</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home',
  data() {
    return {
      role: localStorage.getItem('user_role') || null
    }
  }
}
</script>

<style scoped>
h1 {
  color: #34495e;
}
</style>
