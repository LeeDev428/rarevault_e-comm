<template>
  <div class="admin-layout">
    <!-- Header -->
    <header class="admin-header">
      <div class="header-left">
        <div class="logo">
          <h2>RareVault</h2>
        </div>
        <div class="search-container">
          <input 
            type="text" 
            placeholder="Search..." 
            class="search-input"
            v-model="searchQuery"
          />
          <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <circle cx="11" cy="11" r="8"></circle>
            <path d="m21 21-4.35-4.35"></path>
          </svg>
        </div>
      </div>
      
      <div class="header-right">
        <button class="notification-btn">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"></path>
            <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
          </svg>
        </button>
        
        <div class="user-profile">
          <img 
            :src="userAvatar" 
            :alt="userName" 
            class="user-avatar"
          />
          <div class="user-info">
            <span class="user-name">{{ userName }}</span>
            <button class="dropdown-btn" @click="toggleUserMenu">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <polyline points="6,9 12,15 18,9"></polyline>
              </svg>
            </button>
          </div>
          
          <!-- User Dropdown Menu -->
          <div v-if="showUserMenu" class="user-dropdown">
            <a href="#" class="dropdown-item">Profile</a>
            <a href="#" class="dropdown-item">Settings</a>
            <hr class="dropdown-divider">
            <a href="#" class="dropdown-item" @click="logout">Logout</a>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content Area -->
    <div class="admin-main">
      <!-- Sidebar -->
      <aside class="admin-sidebar">
        <nav class="sidebar-nav">
          <div class="nav-section">
            <h3 class="nav-title">DASHBOARD</h3>
            <ul class="nav-list">
              <li class="nav-item">
                <router-link to="/admin/dashboard" class="nav-link" :class="{ active: $route.path === '/admin/dashboard' }">
                  <svg class="nav-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <rect x="3" y="3" width="7" height="7"></rect>
                    <rect x="14" y="3" width="7" height="7"></rect>
                    <rect x="14" y="14" width="7" height="7"></rect>
                    <rect x="3" y="14" width="7" height="7"></rect>
                  </svg>
                  <span>Overview</span>
                </router-link>
              </li>
              
              <li class="nav-item">
                <a href="#" class="nav-link">
                  <svg class="nav-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                    <circle cx="12" cy="7" r="4"></circle>
                  </svg>
                  <span>Manage user page</span>
                </a>
              </li>
              
              <li class="nav-item">
                <a href="#" class="nav-link">
                  <svg class="nav-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path>
                    <circle cx="9" cy="7" r="4"></circle>
                    <path d="M22 21v-2a4 4 0 0 0-3-3.87"></path>
                    <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                  </svg>
                  <span>Manage Listings Page</span>
                </a>
              </li>
              
              <li class="nav-item">
                <router-link to="/admin/items" class="nav-link" :class="{ active: $route.path === '/admin/items' }">
                  <svg class="nav-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
                    <polyline points="3.27,6.96 12,12.01 20.73,6.96"></polyline>
                    <line x1="12" y1="22.08" x2="12" y2="12"></line>
                  </svg>
                  <span>Manage Items</span>
                </router-link>
              </li>
            </ul>
          </div>
        </nav>
      </aside>

      <!-- Content Area -->
      <main class="admin-content">
        <slot></slot>
      </main>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AdminLayout',
  data() {
    return {
      searchQuery: '',
      showUserMenu: false,
      userName: 'Soverenove',
      userAvatar: 'https://via.placeholder.com/40x40/4A5568/FFFFFF?text=S'
    }
  },
  mounted() {
    // Get user info from localStorage or API
    const userInfo = localStorage.getItem('user_info');
    if (userInfo) {
      const user = JSON.parse(userInfo);
      this.userName = `${user.first_name} ${user.last_name}`;
    }
    
    // Close dropdown when clicking outside
    document.addEventListener('click', this.handleClickOutside);
  },
  beforeUnmount() {
    document.removeEventListener('click', this.handleClickOutside);
  },
  methods: {
    toggleUserMenu() {
      this.showUserMenu = !this.showUserMenu;
    },
    handleClickOutside(event) {
      if (!this.$el.contains(event.target)) {
        this.showUserMenu = false;
      }
    },
    logout() {
      localStorage.removeItem('access_token');
      localStorage.removeItem('user_role');
      localStorage.removeItem('user_info');
      this.$router.push('/login');
    }
  }
}
</script>

<style scoped>
.admin-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #f8fafc;
}

/* Header Styles */
.admin-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 24px;
  height: 64px;
  background-color: white;
  border-bottom: 1px solid #e2e8f0;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 24px;
}

.logo h2 {
  font-size: 20px;
  font-weight: 600;
  color: #1a202c;
  margin: 0;
}

.search-container {
  position: relative;
  width: 300px;
}

.search-input {
  width: 100%;
  padding: 8px 12px 8px 40px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
  background-color: #f7fafc;
  transition: all 0.2s;
}

.search-input:focus {
  outline: none;
  border-color: #4299e1;
  background-color: white;
}

.search-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #a0aec0;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.notification-btn {
  padding: 8px;
  border: none;
  background: none;
  color: #4a5568;
  cursor: pointer;
  border-radius: 6px;
  transition: background-color 0.2s;
}

.notification-btn:hover {
  background-color: #f7fafc;
}

.user-profile {
  position: relative;
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.user-name {
  font-size: 14px;
  font-weight: 500;
  color: #2d3748;
}

.dropdown-btn {
  border: none;
  background: none;
  color: #a0aec0;
  cursor: pointer;
  padding: 2px;
}

.user-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 8px;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  min-width: 150px;
  z-index: 1000;
}

.dropdown-item {
  display: block;
  padding: 12px 16px;
  text-decoration: none;
  color: #4a5568;
  font-size: 14px;
  transition: background-color 0.2s;
}

.dropdown-item:hover {
  background-color: #f7fafc;
}

.dropdown-divider {
  margin: 0;
  border: none;
  border-top: 1px solid #e2e8f0;
}

/* Main Content Area */
.admin-main {
  display: flex;
  flex: 1;
  overflow: hidden;
}

/* Sidebar Styles */
.admin-sidebar {
  width: 280px;
  background-color: white;
  border-right: 1px solid #e2e8f0;
  overflow-y: auto;
}

.sidebar-nav {
  padding: 24px 0;
}

.nav-section {
  margin-bottom: 32px;
}

.nav-title {
  font-size: 11px;
  font-weight: 600;
  color: #a0aec0;
  letter-spacing: 0.5px;
  margin: 0 24px 16px;
  text-transform: uppercase;
}

.nav-list {
  list-style: none;
  margin: 0;
  padding: 0;
}

.nav-item {
  margin-bottom: 4px;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 24px;
  text-decoration: none;
  color: #4a5568;
  font-size: 14px;
  transition: all 0.2s;
  border-right: 3px solid transparent;
}

.nav-link:hover {
  background-color: #f7fafc;
  color: #2d3748;
}

.nav-link.active {
  background-color: #ebf8ff;
  color: #3182ce;
  border-right-color: #3182ce;
}

.nav-icon {
  flex-shrink: 0;
}

/* Content Area */
.admin-content {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
  background-color: #f8fafc;
}

/* Responsive Design */
@media (max-width: 768px) {
  .admin-sidebar {
    width: 240px;
  }
  
  .search-container {
    width: 200px;
  }
  
  .admin-content {
    padding: 16px;
  }
}

@media (max-width: 640px) {
  .admin-sidebar {
    position: fixed;
    left: -280px;
    top: 64px;
    height: calc(100vh - 64px);
    z-index: 999;
    transition: left 0.3s;
  }
  
  .admin-sidebar.open {
    left: 0;
  }
  
  .search-container {
    display: none;
  }
}
</style>
