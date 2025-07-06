import { createRouter, createWebHistory } from 'vue-router'
import Home from '../components/Home.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Admin from '../components/Admin.vue'
import Trainer from '../components/Trainer.vue'
import Athlete from '../components/Athlete.vue'
import Guest from '../components/Guest.vue'
import TrainingPlanList from '../components/TrainingPlanList.vue'
import TrainingPlanCreate from '../components/TrainingPlanCreate.vue'
import DashboardAdmin from '../views/DashboardAdmin.vue'
import AdminExercises from '../views/AdminExercises.vue'
import AdminTrainingPlans from '../views/AdminTrainingPlans.vue'
import AdminUsers from '../views/AdminUsers.vue'
import DashboardTrainer from '../views/DashboardTrainer.vue'
import TrainerTrainingPlans from '../views/TrainerTrainingPlans.vue'
import TrainerExercises from '../views/TrainerExercises.vue'
import TrainerAthleteProgress from '../views/TrainerAthleteProgress.vue'
import TrainerAutoGeneratePlan from '../views/TrainerAutoGeneratePlan.vue'
import TrainerAthleteReport from '../views/TrainerAthleteReport.vue'
import TrainerEffectivenessRanking from '../views/TrainerEffectivenessRanking.vue'
import DashboardAthlete from '../views/DashboardAthlete.vue'
import AthleteAutoGeneratePlan from '../views/AthleteAutoGeneratePlan.vue'
import AthleteProgress from '../views/AthleteProgress.vue'
import AthleteProgressForm from '../views/AthleteProgressForm.vue'
import AthleteProgressGraph from '../views/AthleteProgressGraph.vue'
import AthletePlans from '../views/AthletePlans.vue'
import AthleteExercises from '../views/AthleteExercises.vue'

const routes = [
  {
    path: '/',
    name: 'LoginRedirect',
    beforeEnter: (to, from, next) => {
      const token = localStorage.getItem('access_token')
      if (token) {
        next({ name: 'Login' })
      } else {
        next({ name: 'Home' })
      }
    }
  },
  {
    path: '/home',
    name: 'Home',
    component: Home,
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/admin',
    name: 'Admin',
    component: DashboardAdmin,
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/admin/exercises',
    name: 'AdminExercises',
    component: AdminExercises,
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/admin/training-plans',
    name: 'AdminTrainingPlans',
    component: AdminTrainingPlans,
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/admin/users',
    name: 'AdminUsers',
    component: AdminUsers,
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/trainer',
    name: 'Trainer',
    component: DashboardTrainer,
    meta: { requiresAuth: true, role: 'trainer' }
  },
  {
    path: '/athlete',
    name: 'Athlete',
    component: DashboardAthlete,
    meta: { requiresAuth: true, role: 'athlete' }
  },
  {
    path: '/guest',
    name: 'Guest',
    component: Guest,
    meta: { requiresAuth: true, role: 'guest' }
  },
  {
    path: '/training-plans',
    name: 'TrainingPlanList',
    component: TrainingPlanList,
    meta: { requiresAuth: true }
  },
  {
    path: '/training-plan/create',
    name: 'TrainingPlanCreate',
    component: TrainingPlanCreate,
    meta: { requiresAuth: true }
  },
  {
    path: '/trainer/training-plans',
    name: 'TrainerTrainingPlans',
    component: TrainerTrainingPlans,
    meta: { requiresAuth: true, role: 'trainer' }
  },
  {
    path: '/trainer/exercises',
    name: 'TrainerExercises',
    component: TrainerExercises,
    meta: { requiresAuth: true, role: 'trainer' }
  },
  {
    path: '/trainer/athlete-progress',
    name: 'TrainerAthleteProgress',
    component: TrainerAthleteProgress,
    meta: { requiresAuth: true, role: 'trainer' }
  },
  {
    path: '/trainer/auto-generate-plan',
    name: 'TrainerAutoGeneratePlan',
    component: TrainerAutoGeneratePlan,
    meta: { requiresAuth: true, role: 'trainer' }
  },
  {
    path: '/trainer/athlete-report',
    name: 'TrainerAthleteReport',
    component: TrainerAthleteReport,
    meta: { requiresAuth: true, role: 'trainer' }
  },
  {
    path: '/trainer/effectiveness-ranking',
    name: 'TrainerEffectivenessRanking',
    component: TrainerEffectivenessRanking,
    meta: { requiresAuth: true, role: 'trainer' }
  },
  {
    path: '/athlete/auto-generate-plan',
    name: 'AthleteAutoGeneratePlan',
    component: AthleteAutoGeneratePlan,
    meta: { requiresAuth: true, role: 'athlete' }
  },
  {
    path: '/athlete/progress',
    name: 'AthleteProgress',
    component: AthleteProgress,
    meta: { requiresAuth: true, role: 'athlete' }
  },
  {
    path: '/athlete/progress-form',
    name: 'AthleteProgressForm',
    component: AthleteProgressForm,
    meta: { requiresAuth: true, role: 'athlete' }
  },
  {
    path: '/athlete/progress-graph',
    name: 'AthleteProgressGraph',
    component: AthleteProgressGraph,
    meta: { requiresAuth: true, role: 'athlete' }
  },
  {
    path: '/athlete/plans',
    name: 'AthletePlans',
    component: AthletePlans,
    meta: { requiresAuth: true, role: 'athlete' }
  },
  {
    path: '/athlete/exercises',
    name: 'AthleteExercises',
    component: AthleteExercises,
    meta: { requiresAuth: true, role: 'athlete' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token')
  const userRole = localStorage.getItem('user_role') // You need to set this on login

  if (to.meta.requiresAuth && !token) {
    next({ name: 'Login' })
  } else if (to.meta.role && to.meta.role !== userRole) {
    next({ name: 'Home' }) // Redirect if role does not match
  } else {
    next()
  }
})

export default router
