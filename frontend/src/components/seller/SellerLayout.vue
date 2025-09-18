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
                  <div class="notification-amount">${{ notification.amount.toFixed(2) }}</div>
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
.seller-layout {
  min-height: 100vh;
  background-color: #f8f9fa;
}

/* Header Styles */
.header {
  background: white;
  border-bottom: 1px solid #e9ecef;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  height: 64px;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  height: 100%;
  max-width: 1400px;
  margin: 0 auto;
}

.logo h2 {
  color: #343a40;
  margin: 0;
  font-size: 24px;
  font-weight: 600;
}

.search-container {
  flex: 1;
  max-width: 400px;
  margin: 0 40px;
}

.search-bar {
  position: relative;
  display: flex;
  align-items: center;
}

.search-bar input {
  width: 100%;
  padding: 12px 16px 12px 40px;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  background: #f8f9fa;
  font-size: 14px;
}

.search-bar input:focus {
  outline: none;
  border-color: #007bff;
  background: white;
}

.search-bar svg {
  position: absolute;
  left: 12px;
  color: #6c757d;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.notification-container {
  position: relative;
}

.notification-btn {
  position: relative;
  background: none;
  border: none;
  padding: 8px;
  border-radius: 6px;
  cursor: pointer;
  color: #6c757d;
  transition: background-color 0.2s;
}

.notification-btn:hover {
  background: #f8f9fa;
}

.notification-badge {
  position: absolute;
  top: 2px;
  right: 2px;
  background: #dc3545;
  color: white;
  border-radius: 50%;
  min-width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 600;
  line-height: 1;
}

/* Notifications Dropdown */
.notifications-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  background: white;
  border: 1px solid #e9ecef;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  width: 380px;
  max-height: 500px;
  z-index: 1000;
  margin-top: 8px;
}

.notifications-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #e9ecef;
}

.notifications-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #343a40;
}

.notification-count {
  color: #6c757d;
  font-size: 14px;
}

.notifications-list {
  max-height: 400px;
  overflow-y: auto;
}

.notification-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px 20px;
  border-bottom: 1px solid #f8f9fa;
  cursor: pointer;
  transition: background-color 0.2s;
}

.notification-item:hover {
  background: #f8f9fa;
}

.notification-item:last-child {
  border-bottom: none;
}

.notification-icon {
  width: 40px;
  height: 40px;
  background: #e3f2fd;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #1976d2;
  flex-shrink: 0;
}

.notification-content {
  flex: 1;
}

.notification-title {
  font-weight: 600;
  color: #343a40;
  margin-bottom: 4px;
}

.notification-message {
  color: #6c757d;
  font-size: 14px;
  margin-bottom: 4px;
}

.notification-time {
  color: #adb5bd;
  font-size: 12px;
}

.notification-amount {
  font-weight: 600;
  color: #28a745;
  font-size: 14px;
}

.no-notifications {
  text-align: center;
  padding: 40px 20px;
  color: #6c757d;
}

.no-notifications svg {
  margin-bottom: 16px;
  opacity: 0.5;
}

.no-notifications p {
  margin: 0 0 8px 0;
  font-weight: 500;
}

.no-notifications small {
  opacity: 0.7;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 12px;
  border-radius: 8px;
  cursor: pointer;
  position: relative;
  transition: background-color 0.2s;
}

.user-profile:hover {
  background: #f8f9fa;
}

.user-avatar {
  width: 36px;
  height: 36px;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: linear-gradient(135deg, #007bff, #0056b3);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  font-size: 14px;
}

.username {
  font-weight: 500;
  color: #343a40;
  font-size: 14px;
}

/* User Dropdown */
.user-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  background: white;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  min-width: 180px;
  z-index: 1000;
  margin-top: 8px;
  padding: 8px 0;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  cursor: pointer;
  font-size: 14px;
  color: #495057;
  transition: background-color 0.2s;
  text-decoration: none;
}

.dropdown-item:hover {
  background: #f8f9fa;
}

.dropdown-item.logout {
  color: #dc3545;
}

.dropdown-item.logout:hover {
  background: #f8d7da;
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
  margin-top: 64px;
  min-height: calc(100vh - 64px);
}

/* Sidebar */
.sidebar {
  width: 250px;
  background: white;
  border-right: 1px solid #e9ecef;
  position: fixed;
  left: 0;
  top: 64px;
  bottom: 0;
  overflow-y: auto;
}

.nav-menu {
  padding: 24px 16px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  margin-bottom: 4px;
  border-radius: 8px;
  text-decoration: none;
  color: #6c757d;
  font-weight: 500;
  transition: all 0.2s;
  border: none;
  background: none;
  width: 100%;
  cursor: pointer;
  font-size: 14px;
  position: relative;
}

.nav-item:hover {
  background: #f8f9fa;
  color: #343a40;
}

.nav-item.active {
  background: #e3f2fd;
  color: #1976d2;
}

.nav-item svg {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}

.message-badge {
  position: absolute;
  right: 8px;
  background: #dc3545;
  color: white;
  border-radius: 50%;
  min-width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 600;
  line-height: 1;
}

.nav-divider {
  height: 1px;
  background: #e9ecef;
  margin: 16px 0;
}

.logout-btn {
  color: #dc3545 !important;
}

.logout-btn:hover {
  background: #f8d7da !important;
}

/* Main Content */
.main-content {
  flex: 1;
  margin-left: 250px;
  padding: 24px;
  background: #f8f9fa;
  min-height: calc(100vh - 64px);
}

/* Toast Messages */
.toast-container {
  position: fixed;
  top: 80px;
  right: 24px;
  z-index: 1050;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.toast {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-left: 4px solid #007bff;
  min-width: 300px;
  animation: slideIn 0.3s ease;
}

.toast.success {
  border-left-color: #28a745;
}

.toast.error {
  border-left-color: #dc3545;
}

.toast.warning {
  border-left-color: #ffc107;
}

.toast-icon {
  font-size: 16px;
}

.toast-close {
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
  color: #6c757d;
  margin-left: auto;
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
}
</style>
