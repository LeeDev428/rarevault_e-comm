<template>
  <div class="user-layout">
    <!-- Header -->
    <header class="main-header">
      <div class="header-container">
        <!-- Left Side - Logo -->
        <div class="header-left">
          <router-link to="/user/dashboard" class="logo">
            <h2 class="logo-text">RareVault</h2>
          </router-link>
        </div>

      

        <!-- Right Side - User Menu -->
        <div class="header-right">
          <div class="user-controls">
            <!-- Notifications -->
            <div class="notification-container">
              <button class="notification-btn" @click="toggleNotifications">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/>
                  <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
                </svg>
                <span v-if="unreadNotificationCount > 0" class="notification-badge">{{ unreadNotificationCount }}</span>
              </button>

              <!-- Notification Dropdown -->
              <div v-if="showNotifications" class="notification-dropdown" @click.stop>
                <div class="notification-header">
                  <h3>Notifications</h3>
                  <div class="notification-actions">
                    <button @click="markAllAsRead" class="mark-all-btn" v-if="unreadNotificationCount > 0">
                      Mark all as read
                    </button>
                    <button @click="showNotifications = false" class="close-notifications">✕</button>
                  </div>
                </div>
                
                <div class="notification-list" v-if="notifications.length > 0">
                  <div 
                    v-for="notification in notifications" 
                    :key="notification.id"
                    :class="['notification-item', { 'unread': !notification.is_read }]"
                    @click="handleNotificationClick(notification)"
                  >
                    <div class="notification-icon">
                      <svg v-if="notification.type === 'order_confirmed'" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <path d="M9 12l2 2 4-4"/>
                        <path d="M21 12c-1 0-3-1-3-3s2-3 3-3 3 1 3 3-2 3-3 3"/>
                        <path d="M3 12c1 0 3-1 3-3s-2-3-3-3-3 1-3 3 2 3 3 3"/>
                      </svg>
                      <svg v-else-if="notification.type === 'order_shipped'" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <rect x="1" y="3" width="15" height="13"/>
                        <polygon points="16,8 20,8 23,11 23,16 16,16"/>
                        <circle cx="5.5" cy="18.5" r="2.5"/>
                        <circle cx="18.5" cy="18.5" r="2.5"/>
                      </svg>
                      <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/>
                        <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
                      </svg>
                    </div>
                    <div class="notification-content">
                      <div class="notification-title">{{ notification.title }}</div>
                      <div class="notification-message">{{ notification.message }}</div>
                      <div class="notification-time">{{ formatNotificationTime(notification.created_at) }}</div>
                    </div>
                    <div v-if="!notification.is_read" class="unread-indicator"></div>
                  </div>
                </div>
                
                <div v-else class="no-notifications">
                  <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/>
                    <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
                  </svg>
                  <p>No notifications yet</p>
                  <small>You'll see notifications here when there are updates</small>
                </div>
                
              
              </div>
            </div>

            <!-- Chat -->
            <button class="chat-btn" @click="navigateToMessages">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
              </svg>
              <span class="chat-text">Chat</span>
              <span v-if="unreadMessageCount > 0" class="chat-badge">{{ unreadMessageCount }}</span>
            </button>

            <!-- User Profile Dropdown -->
            <div class="user-profile" @click="toggleUserMenu">
              <div class="user-avatar">
                <div class="avatar-circle">
                  <span>{{ userInitials }}</span>
                </div>
              </div>
              <span class="user-name">{{ userName }}</span>
              <svg class="dropdown-arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <polyline points="6,9 12,15 18,9"/>
              </svg>

              <!-- User Dropdown -->
              <div v-if="showUserMenu" class="user-dropdown" @click.stop>
                <div class="dropdown-item" @click="goToDashboard">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <rect x="3" y="3" width="7" height="7"/>
                    <rect x="14" y="3" width="7" height="7"/>
                    <rect x="14" y="14" width="7" height="7"/>
                    <rect x="3" y="14" width="7" height="7"/>
                  </svg>
                  Dashboard
                </div>
                <div class="dropdown-item" @click="goToProfile">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                    <circle cx="12" cy="7" r="4"/>
                  </svg>
                  Profile
                </div>
                <div class="dropdown-item" @click="goToOrders">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M9 12l2 2 4-4"/>
                    <path d="M21 12c-1 0-3-1-3-3s2-3 3-3 3 1 3 3-2 3-3 3"/>
                    <path d="M3 12c1 0 3-1 3-3s-2-3-3-3-3 1-3 3 2 3 3 3"/>
                  </svg>
                  My Orders
                </div>
                <div class="dropdown-item" @click="goToWishlist">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
                  </svg>
                  Wishlist
                </div>
                <div class="dropdown-item" @click="goToSettings">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <circle cx="12" cy="12" r="3"/>
                    <path d="M12 1v6m0 6v6m11-7h-6M7 12H1m15.5-3.5l-5.66 5.66M12.34 5.66L6.68 11.32M17.5 17.5l-5.66-5.66M5.66 17.5l5.66-5.66"/>
                  </svg>
                  Settings
                </div>
                <div class="dropdown-divider"></div>
                <div class="dropdown-item logout" @click="logout">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
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
      </div>
    </header>

    <!-- Navigation Categories -->
    <nav class="category-nav">
      <div class="nav-container">
        <router-link 
          to="/user/dashboard" 
          class="category-item" 
          :class="{ active: $route.path === '/user/dashboard' }"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <rect x="3" y="3" width="7" height="7"/>
            <rect x="14" y="3" width="7" height="7"/>
            <rect x="14" y="14" width="7" height="7"/>
            <rect x="3" y="14" width="7" height="7"/>
          </svg>
          <span>Vintage Items</span>
        </router-link>

        <router-link 
          to="/user/others" 
          class="category-item" 
          :class="{ active: $route.path === '/user/others' }"
        >
        
        
        </router-link>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="main-content">
      <div class="content-container">
        <slot />
      </div>
    </main>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'UserLayout',
  data() {
    return {
      searchQuery: '',
      showUserMenu: false,
      showNotifications: false,
      userName: 'John Doe',
      userInitials: 'JD',
      unreadMessageCount: 0,
      unreadNotificationCount: 0,
      notifications: [],
      messageCountInterval: null,
      notificationCountInterval: null
    }
  },
  mounted() {
    document.addEventListener('click', this.closeMenus)
    this.loadUserInfo()
    this.loadUnreadMessageCount()
    this.loadUnreadNotificationCount()
    this.loadNotifications()
    this.startMessageCountPolling()
    this.startNotificationPolling()
  },
  beforeUnmount() {
    document.removeEventListener('click', this.closeMenus)
    this.stopMessageCountPolling()
    this.stopNotificationPolling()
  },
  methods: {
    handleSearch() {
      // Emit search event or handle search logic
      this.$emit('search', this.searchQuery)
    },
    
    toggleUserMenu(event) {
      event.stopPropagation()
      this.showUserMenu = !this.showUserMenu
      if (this.showUserMenu) {
        this.showNotifications = false
      }
    },
    
    toggleNotifications(event) {
      event.stopPropagation()
      this.showNotifications = !this.showNotifications
      if (this.showNotifications) {
        this.showUserMenu = false
        this.loadNotifications()
      }
    },
    
    closeMenus(event) {
      if (event && event.target) {
        if (!event.target.closest('.user-profile')) {
          this.showUserMenu = false
        }
        if (!event.target.closest('.notification-container')) {
          this.showNotifications = false
        }
      }
    },
    
    goToDashboard() {
      this.$router.push('/user/dashboard')
      this.showUserMenu = false
    },
    
    goToProfile() {
      this.$router.push('/user/profile')
      this.showUserMenu = false
    },
    
    goToOrders() {
      this.$router.push('/user/orders')
      this.showUserMenu = false
    },
    
    goToWishlist() {
      this.$router.push('/user/wishlist')
      this.showUserMenu = false
    },
    
    goToSettings() {
      this.$router.push('/user/settings')
      this.showUserMenu = false
    },
    
    logout() {
      localStorage.removeItem('access_token')
      localStorage.removeItem('user_role')
      localStorage.removeItem('user_data')
      
      this.$router.push('/login')
      this.showUserMenu = false
    },

    navigateToMessages() {
      this.$router.push('/user/messages')
    },

    async loadUserInfo() {
      try {
        const token = localStorage.getItem('access_token') || localStorage.getItem('token')
        if (!token) return

        // Try to get user info from localStorage first
        const cachedUserInfo = localStorage.getItem('user_info')
        if (cachedUserInfo) {
          const user = JSON.parse(cachedUserInfo)
          this.updateUserDisplay(user)
        }

        // Also fetch fresh data from API if available
        const response = await axios.get('http://localhost:5000/api/user/profile', {
          headers: { 'Authorization': `Bearer ${token}` }
        })

        if (response.data) {
          this.updateUserDisplay(response.data)
          // Update localStorage with fresh data
          localStorage.setItem('user_info', JSON.stringify(response.data))
        }
      } catch (error) {
        console.error('Error loading user info:', error)
        // Fallback to cached data or default
        const cachedUserInfo = localStorage.getItem('user_info')
        if (cachedUserInfo) {
          const user = JSON.parse(cachedUserInfo)
          this.updateUserDisplay(user)
        }
      }
    },

    updateUserDisplay(user) {
      // Use first_name and last_name if available, otherwise fallback to username
      if (user.first_name && user.last_name) {
        this.userName = `${user.first_name} ${user.last_name}`
        this.userInitials = `${user.first_name.charAt(0)}${user.last_name.charAt(0)}`.toUpperCase()
      } else if (user.first_name) {
        this.userName = user.first_name
        this.userInitials = user.first_name.charAt(0).toUpperCase()
      } else if (user.username) {
        this.userName = user.username
        this.userInitials = user.username.charAt(0).toUpperCase()
      }
    },

    async loadUnreadMessageCount() {
      try {
        const token = localStorage.getItem('access_token') || localStorage.getItem('token')
        if (!token) return

        const response = await axios.get('http://localhost:5000/api/messages/unread-count', {
          headers: { 'Authorization': `Bearer ${token}` }
        })

        if (response.data.success) {
          this.unreadMessageCount = response.data.unread_count
        }
      } catch (error) {
        console.error('Error loading unread message count:', error)
        // Don't show error to user, just fail silently
      }
    },

    startMessageCountPolling() {
      // Poll unread count every 30 seconds
      this.messageCountInterval = setInterval(() => {
        this.loadUnreadMessageCount()
      }, 30000)
    },

    stopMessageCountPolling() {
      if (this.messageCountInterval) {
        clearInterval(this.messageCountInterval)
        this.messageCountInterval = null
      }
    },

    // Notification methods
    async loadNotifications() {
      try {
        const token = localStorage.getItem('access_token') || localStorage.getItem('token')
        if (!token) return

        const response = await axios.get('http://localhost:5000/api/notifications', {
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

    async loadUnreadNotificationCount() {
      try {
        const token = localStorage.getItem('access_token') || localStorage.getItem('token')
        if (!token) return

        const response = await axios.get('http://localhost:5000/api/notifications/count', {
          headers: { 'Authorization': `Bearer ${token}` }
        })

        if (response.data.success) {
          this.unreadNotificationCount = response.data.notification_count
        }
      } catch (error) {
        console.error('Error loading notification count:', error)
        // Don't show error to user, just fail silently
      }
    },

    async markAllAsRead() {
      try {
        const token = localStorage.getItem('access_token') || localStorage.getItem('token')
        if (!token) return

        await axios.post('http://localhost:5000/api/notifications/mark-seen', {}, {
          headers: { 'Authorization': `Bearer ${token}` }
        })

        // Update local state - since we're counting confirmed orders, we can just reset count
        this.unreadNotificationCount = 0
      } catch (error) {
        console.error('Error marking notifications as seen:', error)
      }
    },

    handleNotificationClick(notification) {
      // Navigate to orders page to see confirmed order details
      this.$router.push('/user/orders')
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

    startNotificationPolling() {
      // Poll notification count every 30 seconds
      this.notificationCountInterval = setInterval(() => {
        this.loadUnreadNotificationCount()
        // Reload notifications if dropdown is open
        if (this.showNotifications) {
          this.loadNotifications()
        }
      }, 30000)
    },

    stopNotificationPolling() {
      if (this.notificationCountInterval) {
        clearInterval(this.notificationCountInterval)
        this.notificationCountInterval = null
      }
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400;1,500;1,600;1,700;1,800&family=Inter:wght@300;400;500;600;700&display=swap');

.user-layout {
  min-height: 100vh;
  background-color: #ffffff;
}

/* Header */
.main-header {
  background: #ffffff;
  border-bottom: 1px solid #e5e7eb;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 72px;
}

/* Logo */
.logo {
  text-decoration: none;
  color: #1f2937;
}

.logo-text {
  font-family: 'Playfair Display', serif;
  font-style: italic;
  font-weight: 800;
  font-size: 28px;
  letter-spacing: -1px;
  color: #1f2937;
  margin: 0;
  transition: color 0.2s ease;
}

.logo:hover .logo-text {
  color: #3b82f6;
}

/* Search */
.header-center {
  flex: 1;
  max-width: 600px;
  margin: 0 40px;
}

.search-container {
  position: relative;
}

.search-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.search-input {
  width: 100%;
  padding: 12px 16px 12px 48px;
  border: 1px solid #e5e7eb;
  border-radius: 24px;
  font-size: 14px;
  font-family: 'Inter', sans-serif;
  background: #ffffff;
  transition: all 0.2s ease;
}

.search-input:focus {
  outline: none;
  border-color: #3b82f6;
  background: #ffffff;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.search-icon {
  position: absolute;
  left: 16px;
  color: #6b7280;
  pointer-events: none;
}

/* User Controls */
.header-right {
  display: flex;
  align-items: center;
}

.user-controls {
  display: flex;
  align-items: center;
  gap: 16px;
}

.notification-btn,
.chat-btn {
  position: relative;
  padding: 8px;
  border: none;
  background: none;
  border-radius: 8px;
  cursor: pointer;
  color: #6b7280;
  transition: all 0.2s ease;
}

.notification-btn:hover,
.chat-btn:hover {
  background: #f3f4f6;
  color: #374151;
}

.notification-container {
  position: relative;
}

.notification-badge {
  position: absolute;
  top: 2px;
  right: 2px;
  background: #ef4444;
  color: white;
  border-radius: 50%;
  min-width: 16px;
  height: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  font-weight: 600;
  line-height: 1;
}

/* Notification Dropdown */
.notification-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 8px;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  width: 380px;
  max-height: 500px;
  z-index: 1000;
  overflow: hidden;
}

.notification-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #e5e7eb;
  background: #f9fafb;
}

.notification-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #111827;
}

.notification-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.mark-all-btn {
  background: none;
  border: none;
  color: #3b82f6;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.mark-all-btn:hover {
  background: #eff6ff;
}

.close-notifications {
  background: none;
  border: none;
  font-size: 16px;
  cursor: pointer;
  color: #6b7280;
  padding: 4px;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.close-notifications:hover {
  background: #f3f4f6;
  color: #374151;
}

.notification-list {
  max-height: 400px;
  overflow-y: auto;
}

.notification-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px 20px;
  border-bottom: 1px solid #f3f4f6;
  cursor: pointer;
  transition: background-color 0.2s;
  position: relative;
}

.notification-item:hover {
  background: #f9fafb;
}

.notification-item.unread {
  background: #fef3f2;
}

.notification-item.unread:hover {
  background: #fde8e8;
}

.notification-icon {
  flex-shrink: 0;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #eff6ff;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #3b82f6;
}

.notification-item.unread .notification-icon {
  background: #dcfce7;
  color: #16a34a;
}

.notification-content {
  flex: 1;
  min-width: 0;
}

.notification-title {
  font-size: 14px;
  font-weight: 600;
  color: #111827;
  margin-bottom: 4px;
  line-height: 1.2;
}

.notification-message {
  font-size: 13px;
  color: #6b7280;
  line-height: 1.4;
  margin-bottom: 4px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  line-clamp: 2;
  overflow: hidden;
}

.notification-time {
  font-size: 11px;
  color: #9ca3af;
  font-weight: 500;
}

.unread-indicator {
  flex-shrink: 0;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #ef4444;
  margin-top: 4px;
}

.no-notifications {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  text-align: center;
  color: #6b7280;
}

.no-notifications svg {
  color: #d1d5db;
  margin-bottom: 12px;
}

.no-notifications p {
  margin: 0 0 4px 0;
  font-size: 14px;
  font-weight: 500;
  color: #374151;
}

.no-notifications small {
  font-size: 12px;
  color: #9ca3af;
}

.view-all-notifications {
  padding: 12px 20px;
  border-top: 1px solid #e5e7eb;
  background: #f9fafb;
}

.view-all-btn {
  width: 100%;
  padding: 8px 16px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.view-all-btn:hover {
  background: #2563eb;
}

.chat-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
}

.chat-text {
  font-size: 14px;
  font-weight: 500;
}

.chat-badge {
  background: #ef4444;
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

/* User Profile */
.user-profile {
  position: relative;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: 12px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.user-profile:hover {
  background: #f3f4f6;
}

.user-avatar {
  width: 32px;
  height: 32px;
}

.avatar-circle {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  font-size: 12px;
}

.user-name {
  font-size: 14px;
  font-weight: 500;
  color: #111827;
}

.dropdown-arrow {
  color: #6b7280;
  transition: transform 0.2s ease;
}

.user-profile:hover .dropdown-arrow {
  transform: rotate(180deg);
}

/* User Dropdown */
.user-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 8px;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  min-width: 200px;
  padding: 8px 0;
  z-index: 1000;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  color: #374151;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.dropdown-item:hover {
  background: #f3f4f6;
}

.dropdown-item.logout {
  color: #ef4444;
}

.dropdown-item.logout:hover {
  background: #fef2f2;
}

.dropdown-divider {
  height: 1px;
  background: #e5e7eb;
  margin: 8px 0;
}

/* Category Navigation */
.category-nav {
  background: white;
  border-bottom: 1px solid #e5e7eb;
  padding: 16px 0;
}

.nav-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  gap: 32px;
}

.category-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
  color: #6b7280;
  font-weight: 500;
  transition: all 0.2s ease;
}

.category-item:hover {
  background: #f3f4f6;
  color: #374151;
}

.category-item.active {
  background: #eff6ff;
  color: #2563eb;
}

.category-item span {
  font-size: 14px;
  white-space: nowrap;
}

/* Main Content */
.main-content {
  flex: 1;
  padding: 24px 0;
}

.content-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 24px;
}

/* Responsive */
@media (max-width: 768px) {
  .header-container {
    padding: 0 16px;
    height: 64px;
  }
  
  .header-center {
    margin: 0 16px;
  }
  
  .nav-container {
    padding: 0 16px;
    overflow-x: auto;
    gap: 16px;
  }
  
  .category-item {
    flex-shrink: 0;
  }
  
  .content-container {
    padding: 0 16px;
  }
  
  .user-info {
    display: none;
  }
}
</style>
