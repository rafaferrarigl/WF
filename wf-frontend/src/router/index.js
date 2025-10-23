import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import UserDashboard from '../views/UserDashboard.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: Login },
  { path: '/admin/dashboard', component: AdminDashboard },
  { path: '/user/dashboard', component: UserDashboard },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
