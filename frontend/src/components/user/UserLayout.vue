<template>
  <div class="user-layout">
    <!-- Header -->
    <header class="main-header">
      <div class="header-container">
        <!-- Left Side - Logo -->
        <div class="header-left">
          <router-link to="/user/dashboard" class="logo">
            <h1>RareVault</h1>
          </router-link>
        </div>

        <!-- Center - Search -->
        <div class="header-center">
          <div class="search-container">
            <div class="search-input-wrapper">
              <input 
                type="text" 
                placeholder="Search for items..." 
                class="search-input"
                v-model="searchQuery"
                @input="handleSearch"
              />
              <svg class="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <circle cx="11" cy="11" r="8"/>
                <path d="M21 21l-4.35-4.35"/>
              </svg>
            </div>
          </div>
        </div>

        <!-- Right Side - User Menu -->
        <div class="header-right">
          <div class="user-controls">
            <!-- Notifications -->
            <button class="notification-btn">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/>
                <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
              </svg>
            </button>

            <!-- Chat -->
            <button class="chat-btn">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
              </svg>
              <span class="chat-text">Chat</span>
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
          to="/user/collectibles" 
          class="category-item" 
          :class="{ active: $route.path === '/user/collectibles' }"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
          </svg>
          <span>Collectibles</span>
        </router-link>

        <router-link 
          to="/user/antiques" 
          class="category-item" 
          :class="{ active: $route.path === '/user/antiques' }"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <circle cx="12" cy="12" r="10"/>
            <polyline points="12,6 12,12 16,14"/>
          </svg>
          <span>Antiques</span>
        </router-link>

        <router-link 
          to="/user/coins" 
          class="category-item" 
          :class="{ active: $route.path === '/user/coins' }"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <circle cx="12" cy="12" r="10"/>
            <path d="M12 6v12M8 10l4-4 4 4"/>
          </svg>
          <span>Coins & Currency</span>
        </router-link>

        <router-link 
          to="/user/others" 
          class="category-item" 
          :class="{ active: $route.path === '/user/others' }"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <circle cx="12" cy="12" r="3"/>
            <circle cx="12" cy="4" r="1"/>
            <circle cx="12" cy="20" r="1"/>
            <circle cx="4" cy="12" r="1"/>
            <circle cx="20" cy="12" r="1"/>
          </svg>
          <span>Others</span>
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
export default {
  name: 'UserLayout',
  data() {
    return {
      searchQuery: '',
      showUserMenu: false,
      userName: 'John Doe',
      userInitials: 'JD'
    }
  },
  mounted() {
    document.addEventListener('click', this.closeUserMenu)
  },
  beforeUnmount() {
    document.removeEventListener('click', this.closeUserMenu)
  },
  methods: {
    handleSearch() {
      // Emit search event or handle search logic
      this.$emit('search', this.searchQuery)
    },
    
    toggleUserMenu(event) {
      event.stopPropagation()
      this.showUserMenu = !this.showUserMenu
    },
    
    closeUserMenu(event) {
      if (event && event.target && !event.target.closest('.user-profile')) {
        this.showUserMenu = false
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
    }
  }
}
</script>

<style scoped>
.user-layout {
  min-height: 100vh;
  background-color: #f8fafc;
}

/* Header */
.main-header {
  background: white;
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
  color: #111827;
}

.logo h1 {
  font-size: 24px;
  font-weight: 700;
  margin: 0;
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
  border: 1px solid #d1d5db;
  border-radius: 24px;
  font-size: 14px;
  background: #f9fafb;
  transition: all 0.2s ease;
}

.search-input:focus {
  outline: none;
  border-color: #3b82f6;
  background: white;
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
