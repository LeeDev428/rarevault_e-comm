import { createRouter, createWebHistory } from 'vue-router'
import Landing from '@/views/Landing.vue'
import Login from '@/views/Login.vue'
import Register from '@/views/Register.vue'
import UserDashboard from '@/views/user/Dashboard.vue'
import AdminDashboard from '@/views/admin/Dashboard.vue'

const routes = [
  {
    path: '/',
    name: 'Landing',
    component: Landing
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
    path: '/user/dashboard',
    name: 'UserDashboard',
    component: UserDashboard,
    meta: { requiresAuth: true, role: 'user' }
  },
  {
    path: '/admin/dashboard',
    name: 'AdminDashboard',
    component: AdminDashboard,
    meta: { requiresAuth: true, role: 'admin' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token')
  const userRole = localStorage.getItem('user_role')
  
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else if (to.meta.role && userRole !== to.meta.role) {
    // Redirect to appropriate dashboard based on role
    if (userRole === 'admin') {
      next('/admin/dashboard')
    } else {
      next('/user/dashboard')
    }
  } else {
    next()
  }
})

export default router
