import { createRouter, createWebHistory } from 'vue-router'
import Landing from '@/views/Landing.vue'
import Login from '@/views/Login.vue'
import Register from '@/views/Register.vue'
import AdminDashboard from '@/views/admin/dashboard/Index.vue'
import SellerDashboard from '@/views/seller/dashboard/TestIndex.vue'
import SellerItems from '@/views/seller/Items.vue'
import SellerProfile from '@/views/seller/Profile.vue'

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
  // User Routes
  {
    path: '/user/dashboard',
    name: 'UserDashboard',
    component: () => import('@/views/user/dashboard/Index.vue'),
    meta: { requiresAuth: true, role: 'user' }
  },
  {
    path: '/user/profile',
    name: 'UserProfile',
    component: () => import('@/views/user/dashboard/Profile.vue'),
    meta: { requiresAuth: true, role: 'user' }
  },
  {
    path: '/user/orders',
    name: 'UserOrders',
    component: () => import('@/views/user/dashboard/Orders.vue'),
    meta: { requiresAuth: true, role: 'user' }
  },
  {
    path: '/user/orders/:id',
    name: 'UserOrderDetails',
    component: () => import('@/views/user/dashboard/OrderDetails.vue'),
    meta: { requiresAuth: true, role: 'user' }
  },
  {
    path: '/user/wishlist',
    name: 'UserWishlist',
    component: () => import('@/views/user/dashboard/Wishlist.vue'),
    meta: { requiresAuth: true, role: 'user' }
  },
  {
    path: '/user/settings',
    name: 'UserSettings',
    component: () => import('@/views/user/dashboard/Settings.vue'),
    meta: { requiresAuth: true, role: 'user' }
  },
  {
    path: '/user/ratings',
    name: 'UserRatings',
    component: () => import('@/views/user/Ratings.vue'),
    meta: { requiresAuth: true, role: 'user' }
  },
  {
    path: '/user/items/:id',
    name: 'ItemDetails',
    component: () => import('@/views/user/ItemDetails.vue'),
    meta: { requiresAuth: true, role: 'user' }
  },
  {
    path: '/user/dashboard/items/:id',
    name: 'UserItemDetails',
    component: () => import('@/views/user/dashboard/ItemDetails.vue'),
    meta: { requiresAuth: true, role: 'user' }
  },
  // Category Routes
  {
    path: '/user/collectibles',
    name: 'UserCollectibles',
    component: () => import('@/views/user/dashboard/Collectibles.vue'),
    meta: { requiresAuth: true, role: 'user' }
  },
  {
    path: '/user/antiques',
    name: 'UserAntiques',
    component: () => import('@/views/user/dashboard/Antiques.vue'),
    meta: { requiresAuth: true, role: 'user' }
  },
  {
    path: '/user/coins',
    name: 'UserCoins',
    component: () => import('@/views/user/dashboard/Coins.vue'),
    meta: { requiresAuth: true, role: 'user' }
  },
  {
    path: '/user/others',
    name: 'UserOthers',
    component: () => import('@/views/user/dashboard/Others.vue'),
    meta: { requiresAuth: true, role: 'user' }
  },
  // User Messages Routes
  {
    path: '/user/messages',
    name: 'UserMessages',
    component: () => import('@/views/user/messages/Index.vue'),
    meta: { requiresAuth: true, role: 'user' }
  },
  {
    path: '/user/messages/create',
    name: 'UserCreateMessage',
    component: () => import('@/views/user/messages/Create.vue'),
    meta: { requiresAuth: true, role: 'user' }
  },
  {
    path: '/admin/dashboard',
    name: 'AdminDashboard',
    component: AdminDashboard,
    meta: { requiresAuth: true, role: 'admin' }
  },
  // Seller Routes
  {
    path: '/seller/dashboard',
    name: 'SellerDashboard',
    component: SellerDashboard,
    meta: { requiresAuth: true, role: 'seller' }
  },
  {
    path: '/seller/items',
    name: 'SellerItems',
    component: SellerItems,
    meta: { requiresAuth: true, role: 'seller' }
  },
  {
    path: '/seller/profile',
    name: 'SellerProfile',
    component: SellerProfile,
    meta: { requiresAuth: true, role: 'seller' }
  },
  {
    path: '/seller/create-product',
    name: 'SellerCreateProduct',
    component: () => import('@/views/seller/CreateProduct.vue'),
    meta: { requiresAuth: true, role: 'seller' }
  },
  {
    path: '/seller/create-item',
    name: 'SellerCreateItem',
    component: () => import('@/views/seller/CreateItem.vue'),
    meta: { requiresAuth: true, role: 'seller' }
  },
  {
    path: '/seller/items/:id',
    name: 'SellerViewItem',
    component: () => import('@/views/seller/ViewItem.vue'),
    meta: { requiresAuth: true, role: 'seller' }
  },
  {
    path: '/seller/items/:id/edit',
    name: 'SellerEditItem',
    component: () => import('@/views/seller/EditItem.vue'),
    meta: { requiresAuth: true, role: 'seller' }
  },
  {
    path: '/seller/products/:id/edit',
    name: 'SellerEditProduct',
    component: () => import('@/views/seller/EditProduct.vue'),
    meta: { requiresAuth: true, role: 'seller' }
  },
  {
    path: '/seller/orders',
    name: 'SellerOrders',
    component: () => import('@/views/seller/Orders.vue'),
    meta: { requiresAuth: true, role: 'seller' }
  },
  {
    path: '/seller/ratings',
    name: 'SellerRatings',
    component: () => import('@/views/seller/Ratings.vue'),
    meta: { requiresAuth: true, role: 'seller' }
  },
  {
    path: '/seller/settings',
    name: 'SellerSettings',
    component: () => import('@/views/seller/Settings.vue'),
    meta: { requiresAuth: true, role: 'seller' }
  },
  // Seller Messages Routes
  {
    path: '/seller/messages',
    name: 'SellerMessages',
    component: () => import('@/views/seller/messages/Index.vue'),
    meta: { requiresAuth: true, role: 'seller' }
  },
  {
    path: '/seller/messages/create',
    name: 'SellerCreateMessage',
    component: () => import('@/views/seller/messages/Create.vue'),
    meta: { requiresAuth: true, role: 'seller' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token') || localStorage.getItem('token')
  const userRole = localStorage.getItem('user_role')
  
  // If route requires authentication and no token, redirect to login
  if (to.meta.requiresAuth && !token) {
    next('/login')
    return
  }
  
  // If route requires specific role
  if (to.meta.role) {
    // For seller routes, be more permissive - if they have a token and are accessing seller routes, allow it
    if (to.meta.role === 'seller' && token) {
      // Ensure the user_role is set correctly for seller routes
      if (userRole !== 'seller') {
        localStorage.setItem('user_role', 'seller')
      }
      next()
      return
    }
    
    // For other roles, check strictly
    if (userRole !== to.meta.role) {
      // Redirect to appropriate dashboard based on role
      if (userRole === 'admin') {
        next('/admin/dashboard')
      } else if (userRole === 'seller') {
        next('/seller/dashboard')
      } else {
        next('/user/dashboard')
      }
      return
    }
  }
  
  next()
})

export default router
