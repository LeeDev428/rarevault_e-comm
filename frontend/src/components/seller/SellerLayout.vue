<template>
  <div class="seller-layout">
    <!-- Header -->
    <header class="header">
      <div class="header-content">
        <div class="logo">
          <h2 class="logo-text font-display" style="color: rgb(139, 90, 60); font-size: 28px;">RareVault</h2>
        </div>
        
        <div class="search-container">
          <div class="search-bar">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="11" cy="11" r="8"/>
              <path d="m21 21-4.35-4.35"/>
            </svg>
            <input 
              type="text" 
              placeholder="Search for items..."
              v-model="searchQuery"
            >
          </div>
        </div>

        <div class="header-actions">
          <!-- Notifications -->
          <div class="notification-container">
            <button class="notification-btn" @click="toggleNotifications">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/>
                <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
              </svg>
              <span v-if="notificationCount > 0" class="notification-badge">{{ notificationCount }}</span>
            </button>

            <!-- Notifications Dropdown -->
            <div v-if="showNotifications" class="notifications-dropdown" @click.stop>
              <div class="notifications-header">
                <h3>Notifications</h3>
                <span class="notification-count">{{ notificationCount }} new</span>
              </div>
              
              <div class="notifications-list" v-if="notifications.length > 0">
                <div 
                  v-for="notification in notifications" 
                  :key="notification.id"
                  class="notification-item"
                  @click="handleNotificationClick(notification)"
                >
                  <div class="notification-icon">
                    <svg v-if="notification.status === 'pending'" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                      <circle cx="9" cy="21" r="1"/>
                      <circle cx="20" cy="21" r="1"/>
                      <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/>
                    </svg>
                    <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                      <path d="M9 12l2 2 4-4"/>
                      <circle cx="12" cy="12" r="10"/>
                    </svg>
                  </div>
                  <div class="notification-content">
                    <div class="notification-title">{{ notification.title }}</div>
                    <div class="notification-message">{{ notification.message }}</div>
                    <div class="notification-time">{{ formatNotificationTime(notification.created_at) }}</div>
                  </div>
                  <div class="notification-amount">₱{{ notification.amount.toFixed(2) }}</div>
                </div>
              </div>

              <div v-else class="no-notifications">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/>
                  <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
                </svg>
                <p>No notifications yet</p>
                <small>You'll see order updates here</small>
              </div>
            </div>
          </div>
          
          <div class="user-profile" @click="toggleUserMenu">
            <div class="user-avatar">
              <div class="avatar-placeholder">
                {{ userInitials }}
              </div>
            </div>
            <span class="username">{{ currentUser?.name || 'Seller' }}</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="6,9 12,15 18,9"/>
            </svg>
            
            <!-- User Dropdown Menu -->
            <div v-if="showUserMenu" class="user-dropdown" @click.stop>
              <div class="dropdown-item" @click="goToProfile">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                  <circle cx="12" cy="7" r="4"/>
                </svg>
                Profile
              </div>
              <div class="dropdown-item" @click="goToSettings">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="3"/>
                  <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1 1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>
                </svg>
                Settings
              </div>
              <div class="dropdown-divider"></div>
              <div class="dropdown-item logout" @click="logout">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
                  <polyline points="16,17 21,12 16,7"/>
                  <line x1="21" y1="12" x2="9" y2="12"/>
                </svg>
                Logout
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>

    <div class="main-container">
      <!-- Sidebar -->
      <aside class="sidebar">
        <nav class="nav-menu">
          <div 
            class="nav-item"
            :class="{ active: $route.path === '/seller/dashboard' }"
            @click="$router.push('/seller/dashboard')"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="3" width="7" height="7"/>
              <rect x="14" y="3" width="7" height="7"/>
              <rect x="14" y="14" width="7" height="7"/>
              <rect x="3" y="14" width="7" height="7"/>
            </svg>
            <span>Dashboard</span>
          </div>
          
          <div 
            class="nav-item"
            :class="{ active: $route.path.includes('/seller/items') }"
            @click="$router.push('/seller/items')"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>
              <polyline points="3.27,6.96 12,12.01 20.73,6.96"/>
              <line x1="12" y1="22.08" x2="12" y2="12"/>
            </svg>
            <span>My Items</span>
          </div>
          
          <div 
            class="nav-item"
            :class="{ active: $route.path === '/seller/create-item' }"
            @click="$router.push('/seller/create-item')"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="12" y1="5" x2="12" y2="19"/>
              <line x1="5" y1="12" x2="19" y2="12"/>
            </svg>
            <span>Add Item</span>
          </div>
          
          <div 
            class="nav-item"
            :class="{ active: $route.path === '/seller/orders' }"
            @click="$router.push('/seller/orders')"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="9" cy="21" r="1"/>
              <circle cx="20" cy="21" r="1"/>
              <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/>
            </svg>
            <span>Orders</span>
          </div>
          
          <div 
            class="nav-item"
            :class="{ active: $route.path.includes('/seller/messages') }"
            @click="$router.push('/seller/messages')"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
            </svg>
            <span>Messages</span>
            <span v-if="unreadMessageCount > 0" class="message-badge">{{ unreadMessageCount }}</span>
          </div>
          
          <div 
            class="nav-item"
            :class="{ active: $route.path === '/seller/ratings' }"
            @click="$router.push('/seller/ratings')"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polygon points="12,2 15.09,8.26 22,9.27 17,14.14 18.18,21.02 12,17.77 5.82,21.02 7,14.14 2,9.27 8.91,8.26"/>
            </svg>
            <span>Ratings</span>
          </div>
          
          <div 
            class="nav-item"
            :class="{ active: $route.path === '/seller/profile' }"
            @click="$router.push('/seller/profile')"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
              <circle cx="12" cy="7" r="4"/>
            </svg>
            <span>Profile</span>
          </div>
          
          <div 
            class="nav-item"
            :class="{ active: $route.path === '/seller/settings' }"
            @click="$router.push('/seller/settings')"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="3"/>
              <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1 1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>
            </svg>
            <span>Settings</span>
          </div>
          
          <div class="nav-divider"></div>
          
          <button class="nav-item logout-btn" @click="logout">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
              <polyline points="16,17 21,12 16,7"/>
              <line x1="21" y1="12" x2="9" y2="12"/>
            </svg>
            <span>Logout</span>
          </button>
        </nav>
      </aside>

      <!-- Main Content -->
      <main class="main-content">
        <slot />
      </main>
    </div>

    <!-- Toast Messages -->
    <div class="toast-container">
      <div 
        v-for="toast in toasts" 
        :key="toast.id"
        class="toast"
        :class="toast.type"
      >
        <i class="toast-icon">
          {{ toast.type === 'success' ? '✅' : toast.type === 'error' ? '❌' : 'ℹ️' }}
        </i>
        <span>{{ toast.message }}</span>
        <button class="toast-close" @click="removeToast(toast.id)">×</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'SellerLayout',
  data() {
    return {
      searchQuery: '',
      showUserMenu: false,
      showNotifications: false,
      currentUser: {
        name: 'John Seller',
        email: 'seller@example.com',
        role: 'seller'
      },
      notificationCount: 0,
      notifications: [],
      unreadMessageCount: 0,
      toasts: [],
      notificationInterval: null,
      messageCountInterval: null
    }
  },
  computed: {
    userInitials() {
      if (!this.currentUser?.name) return 'S';
      return this.currentUser.name
        .split(' ')
        .map(n => n[0])
        .join('')
        .toUpperCase()
        .slice(0, 2);
    }
  },
  mounted() {
    // Close dropdown when clicking outside
    document.addEventListener('click', this.closeDropdowns)
    this.loadNotificationCount()
    this.loadUnreadMessageCount()
    this.startPolling()
  },
  beforeUnmount() {
    document.removeEventListener('click', this.closeDropdowns)
    this.stopPolling()
  },
  methods: {
    toggleUserMenu(event) {
      event.stopPropagation()
      this.showUserMenu = !this.showUserMenu
      this.showNotifications = false
    },
    toggleNotifications(event) {
      event.stopPropagation()
      this.showNotifications = !this.showNotifications
      this.showUserMenu = false
      if (this.showNotifications) {
        this.loadNotifications()
      }
    },
    closeDropdowns(event) {
      if (event && event.target) {
        if (!event.target.closest('.user-profile')) {
          this.showUserMenu = false
        }
        if (!event.target.closest('.notification-container')) {
          this.showNotifications = false
        }
      }
    },
    async loadNotificationCount() {
      try {
        const token = localStorage.getItem('access_token') || localStorage.getItem('token')
        if (!token) return

        const response = await axios.get('http://localhost:5000/api/seller/notifications/count', {
          headers: { 'Authorization': `Bearer ${token}` }
        })

        if (response.data.success) {
          this.notificationCount = response.data.notification_count
        }
      } catch (error) {
        console.error('Error loading notification count:', error)
      }
    },
    async loadNotifications() {
      try {
        const token = localStorage.getItem('access_token') || localStorage.getItem('token')
        if (!token) return

        const response = await axios.get('http://localhost:5000/api/seller/notifications', {
          headers: { 'Authorization': `Bearer ${token}` }
        })

        if (response.data.success) {
          this.notifications = response.data.notifications || []
        }
      } catch (error) {
        console.error('Error loading notifications:', error)
        this.notifications = []
      }
    },
    async loadUnreadMessageCount() {
      try {
        const token = localStorage.getItem('access_token') || localStorage.getItem('token')
        if (!token) return

        const response = await axios.get('http://localhost:5000/api/seller/messages/unread-count', {
          headers: { 'Authorization': `Bearer ${token}` }
        })

        if (response.data.success) {
          this.unreadMessageCount = response.data.unread_count
        }
      } catch (error) {
        console.error('Error loading unread message count:', error)
      }
    },
    handleNotificationClick(notification) {
      // Navigate to orders page to see order details
      this.$router.push('/seller/orders')
      this.showNotifications = false
    },
    formatNotificationTime(timeString) {
      try {
        const date = new Date(timeString)
        const now = new Date()
        const diffTime = Math.abs(now - date)
        const diffMinutes = Math.ceil(diffTime / (1000 * 60))
        const diffHours = Math.ceil(diffTime / (1000 * 60 * 60))
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

        if (diffMinutes < 60) {
          return `${diffMinutes}m ago`
        } else if (diffHours < 24) {
          return `${diffHours}h ago`
        } else if (diffDays < 7) {
          return `${diffDays}d ago`
        } else {
          return date.toLocaleDateString()
        }
      } catch (error) {
        return 'Recently'
      }
    },
    startPolling() {
      // Poll counts every 30 seconds
      this.notificationInterval = setInterval(() => {
        this.loadNotificationCount()
      }, 30000)
      
      this.messageCountInterval = setInterval(() => {
        this.loadUnreadMessageCount()
      }, 30000)
    },
    stopPolling() {
      if (this.notificationInterval) {
        clearInterval(this.notificationInterval)
        this.notificationInterval = null
      }
      if (this.messageCountInterval) {
        clearInterval(this.messageCountInterval)
        this.messageCountInterval = null
      }
    },
    goToProfile() {
      this.$router.push('/seller/profile')
      this.showUserMenu = false
    },
    goToSettings() {
      this.$router.push('/seller/settings')
      this.showUserMenu = false
    },
    logout() {
      // Clear authentication data
      localStorage.removeItem('access_token')
      localStorage.removeItem('user_role')
      localStorage.removeItem('user_data')
      
      // Show confirmation message
      this.showToast('You have been logged out successfully', 'success', 'Logged Out')
      
      // Redirect to login page after a short delay
      setTimeout(() => {
        this.$router.push('/login')
      }, 1500)
      
      this.showUserMenu = false
    },
    showToast(message, type = 'info') {
      const toast = {
        id: Date.now(),
        message,
        type
      };
      this.toasts.push(toast);
      
      // Auto remove after 5 seconds
      setTimeout(() => {
        this.removeToast(toast.id);
      }, 5000);
    },
    removeToast(id) {
      const index = this.toasts.findIndex(t => t.id === id);
      if (index > -1) {
        this.toasts.splice(index, 1);
      }
    }
  },
  provide() {
    return {
      showToast: this.showToast
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700&family=Crimson+Text:wght@400;600;700&display=swap');

.seller-layout {
  min-height: 100vh;
  background: #ffffff;
  font-family: 'Inter', sans-serif;
}

/* Header Styles */
.header {
  background: #ffffff;
  border-bottom: 1px solid #e5e7eb;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  height: 70px;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 32px;
  height: 100%;
  max-width: 1600px;
  margin: 0 auto;
}

.logo h2 {
  color: #1f2937;
  margin: 0;
  font-size: 32px;
  font-weight: 800;
  font-family: 'Playfair Display', serif;
  letter-spacing: -1px;
  font-style: italic;
}

.search-container {
  flex: 1;
  max-width: 500px;
  margin: 0 48px;
}

.search-bar {
  position: relative;
  display: flex;
  align-items: center;
}

.search-bar input {
  width: 100%;
  padding: 14px 20px 14px 48px;
  border: 1px solid #d1d5db;
  border-radius: 25px;
  background: #ffffff;
  font-size: 15px;
  color: #374151;
  transition: all 0.3s ease;
  font-family: 'Inter', sans-serif;
}

.search-bar input:focus {
  outline: none;
  border-color: #3b82f6;
  background: white;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.search-bar svg {
  position: absolute;
  left: 16px;
  color: #a0958a;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 20px;
}

.notification-container {
  position: relative;
}

.notification-btn {
  position: relative;
  background: #ffffff;
  border: 1px solid #d1d5db;
  padding: 12px;
  border-radius: 15px;
  cursor: pointer;
  color: #374151;
  transition: all 0.3s ease;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.notification-btn:hover {
  background: #f9fafb;
  border-color: #9ca3af;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.notification-badge {
  position: absolute;
  top: -4px;
  right: -4px;
  background: linear-gradient(135deg, #d4af94 0%, #b8936f 100%);
  color: white;
  border-radius: 50%;
  min-width: 22px;
  height: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
  line-height: 1;
  border: 2px solid white;
  box-shadow: 0 2px 6px rgba(139, 90, 60, 0.3);
}

/* Notifications Dropdown */
.notifications-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  background: white;
  border: 2px solid #e8ddd4;
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(139, 90, 60, 0.15);
  width: 420px;
  max-height: 500px;
  z-index: 1000;
  margin-top: 12px;
}

.notifications-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 28px;
  border-bottom: 2px solid #f5f1eb;
  background: linear-gradient(135deg, #fefdfb 0%, #f8f6f1 100%);
  border-radius: 18px 18px 0 0;
}

.notifications-header h3 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: #5a4a3a;
  font-family: 'Playfair Display', serif;
}

.notification-count {
  color: #a0958a;
  font-size: 14px;
  font-weight: 500;
}

.notifications-list {
  max-height: 400px;
  overflow-y: auto;
}

.notification-item {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 20px 28px;
  border-bottom: 1px solid #f5f1eb;
  cursor: pointer;
  transition: all 0.3s ease;
}

.notification-item:hover {
  background: linear-gradient(135deg, #fefdfb 0%, #f8f6f1 100%);
}

.notification-item:last-child {
  border-bottom: none;
  border-radius: 0 0 18px 18px;
}

.notification-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #e8ddd4 0%, #d4af94 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #8b5a3c;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(139, 90, 60, 0.15);
}

.notification-content {
  flex: 1;
}

.notification-title {
  font-weight: 600;
  color: #5a4a3a;
  margin-bottom: 6px;
  font-size: 15px;
}

.notification-message {
  color: #8b7968;
  font-size: 14px;
  margin-bottom: 6px;
  line-height: 1.4;
}

.notification-time {
  color: #a0958a;
  font-size: 12px;
  font-weight: 500;
}

.notification-amount {
  font-weight: 600;
  color: #8b5a3c;
  font-size: 15px;
  font-family: 'Playfair Display', serif;
}

.no-notifications {
  text-align: center;
  padding: 48px 28px;
  color: #a0958a;
}

.no-notifications svg {
  margin-bottom: 20px;
  opacity: 0.6;
  color: #d4af94;
}

.no-notifications p {
  margin: 0 0 8px 0;
  font-weight: 500;
  color: #8b7968;
  font-size: 16px;
}

.no-notifications small {
  opacity: 0.8;
  color: #a0958a;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px 20px;
  border-radius: 18px;
  cursor: pointer;
  position: relative;
  transition: all 0.3s ease;
  background: linear-gradient(135deg, #f8f6f1 0%, #ede8e0 100%);
  border: 2px solid #e8ddd4;
  box-shadow: 0 2px 8px rgba(139, 90, 60, 0.1);
}

.user-profile:hover {
  background: linear-gradient(135deg, #f0ede6 0%, #e8ddd4 100%);
  border-color: #d4af94;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(139, 90, 60, 0.15);
}

.user-avatar {
  width: 42px;
  height: 42px;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: linear-gradient(135deg, #d4af94 0%, #b8936f 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  font-size: 16px;
  box-shadow: 0 4px 12px rgba(139, 90, 60, 0.25);
  border: 2px solid white;
}

.username {
  font-weight: 500;
  color: #5a4a3a;
  font-size: 15px;
  font-family: 'Inter', sans-serif;
}

/* User Dropdown */
.user-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  background: white;
  border: 2px solid #e8ddd4;
  border-radius: 16px;
  box-shadow: 0 12px 32px rgba(139, 90, 60, 0.15);
  min-width: 200px;
  z-index: 1000;
  margin-top: 12px;
  padding: 12px 0;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 24px;
  cursor: pointer;
  font-size: 15px;
  color: #5a4a3a;
  transition: all 0.3s ease;
  text-decoration: none;
  font-weight: 500;
}

.dropdown-item:hover {
  background: linear-gradient(135deg, #fefdfb 0%, #f8f6f1 100%);
  color: #8b5a3c;
}

.dropdown-item.logout {
  color: #d4af94;
}

.dropdown-item.logout:hover {
  background: linear-gradient(135deg, #fef8f6 0%, #f8f0eb 100%);
  color: #b8936f;
}

.dropdown-item svg {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

.dropdown-divider {
  height: 1px;
  background: #e9ecef;
  margin: 8px 0;
}

/* Main Container */
.main-container {
  display: flex;
  margin-top: 70px;
  min-height: calc(100vh - 70px);
}

/* Sidebar */
.sidebar {
  width: 280px;
  background: #ffffff;
  border-right: 1px solid #e5e7eb;
  box-shadow: 2px 0 4px rgba(0, 0, 0, 0.05);
  position: fixed;
  left: 0;
  top: 70px;
  bottom: 0;
  overflow-y: auto;
}

.nav-menu {
  padding: 32px 20px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 20px;
  margin-bottom: 8px;
  border-radius: 16px;
  text-decoration: none;
  color: #6b7280;
  font-weight: 500;
  transition: all 0.3s ease;
  border: none;
  background: none;
  width: 100%;
  cursor: pointer;
  font-size: 15px;
  position: relative;
  font-family: 'Inter', sans-serif;
}

.nav-item:hover {
  background: #f9fafb;
  color: #374151;
  transform: translateX(4px);
}

.nav-item.active {
  background: #3b82f6;
  color: #ffffff;
  box-shadow: 0 4px 16px rgba(139, 90, 60, 0.2);
  font-weight: 600;
}

.nav-item svg {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

.message-badge {
  position: absolute;
  right: 12px;
  background: linear-gradient(135deg, #d4af94 0%, #b8936f 100%);
  color: white;
  border-radius: 50%;
  min-width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 600;
  line-height: 1;
  border: 2px solid white;
  box-shadow: 0 2px 6px rgba(139, 90, 60, 0.3);
}

.nav-divider {
  height: 2px;
  background: linear-gradient(90deg, transparent 0%, #e8ddd4 50%, transparent 100%);
  margin: 24px 0;
}

.logout-btn {
  color: #d4af94 !important;
}

.logout-btn:hover {
  background: linear-gradient(135deg, #fef8f6 0%, #f8f0eb 100%) !important;
  color: #b8936f !important;
}

/* Main Content */
.main-content {
  flex: 1;
  margin-left: 280px;
  padding: 32px;
  background: linear-gradient(135deg, #faf8f3 0%, #f5f1eb 100%);
  min-height: calc(100vh - 70px);
}

/* Toast Messages */
.toast-container {
  position: fixed;
  top: 90px;
  right: 32px;
  z-index: 1050;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.toast {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 24px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(139, 90, 60, 0.15);
  border-left: 4px solid #d4af94;
  min-width: 350px;
  animation: slideIn 0.4s ease;
  border: 2px solid #f5f1eb;
}

.toast.success {
  border-left-color: #8b5a3c;
  background: linear-gradient(135deg, #fefdfb 0%, #f8f6f1 100%);
}

.toast.error {
  border-left-color: #d4af94;
  background: linear-gradient(135deg, #fef8f6 0%, #f8f0eb 100%);
}

.toast.warning {
  border-left-color: #e8ddd4;
  background: linear-gradient(135deg, #fefdfb 0%, #f8f6f1 100%);
}

.toast-icon {
  font-size: 18px;
}

.toast-close {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #a0958a;
  margin-left: auto;
  padding: 4px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.toast-close:hover {
  background: #f5f1eb;
  color: #8b7968;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

/* Responsive */
@media (max-width: 768px) {
  .sidebar {
    transform: translateX(-100%);
    transition: transform 0.3s;
  }
  
  .main-content {
    margin-left: 0;
  }
  
  .search-container {
    display: none;
  }
  
  .header {
    height: 60px;
  }
  
  .main-container {
    margin-top: 60px;
  }
  
  .header-content {
    padding: 0 20px;
  }
  
  .logo h2 {
    font-size: 24px;
  }
  
  .user-profile {
    padding: 8px 12px;
    gap: 12px;
  }
  
  .username {
    display: none;
  }
  
  .toast-container {
    right: 16px;
    left: 16px;
  }
  
  .toast {
    min-width: auto;
  }
}
</style>
