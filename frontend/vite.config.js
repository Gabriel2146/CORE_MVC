import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3000,
    // Proxy solo para desarrollo local, eliminar o comentar para producción
    // proxy: {
    //   '/api': 'http://localhost:8000'
    // }
  }
})
