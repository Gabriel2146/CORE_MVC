import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../components/Home.vue')
  },
  {
    path: '/admin',
    name: 'Admin',
    component: () => import('../components/Admin.vue')
  },
  {
    path: '/trainer',
    name: 'Trainer',
    component: () => import('../components/Trainer.vue')
  },
  {
    path: '/athlete',
    name: 'Athlete',
    component: () => import('../components/Athlete.vue')
  },
  {
    path: '/guest',
    name: 'Guest',
    component: () => import('../components/Guest.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
