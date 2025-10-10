<template>
  <div class="admin-layout">
    <!-- Top Header -->
    <header class="top-header">
      <div class="header-content">
        <div class="logo">
          <h1 class="logo-text font-display" style=" font-size: 30px;">RareVault.</h1>
        </div>
        <!-- <div class="search-section">
          <div class="search-bar">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <circle cx="11" cy="11" r="8"></circle>
              <path d="m21 21-4.35-4.35"></path>
            </svg>
            <input type="text" placeholder="Search">
          </div>
        </div> -->
        
        <div class="header-right">
          <!-- <div class="notification-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"></path>
              <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
            </svg>
          </div> -->
          
          <div class="user-profile" @click="toggleUserMenu">
            
            <div class="user-info">
              <span class="user-role">Admin</span>
            </div>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <polyline points="6,9 12,15 18,9"></polyline>
            </svg>
            
            <!-- User Dropdown Menu -->
            <div v-if="showUserMenu" class="user-dropdown" @click.stop>
              <!-- <div class="dropdown-item" @click="goToProfile">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                  <circle cx="12" cy="7" r="4"></circle>
                </svg>
                Profile
              </div>
              <div class="dropdown-item" @click="goToSettings">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <circle cx="12" cy="12" r="3"></circle>
                  <path d="M12 1v6m0 6v6m11-7h-6M7 12H1m15.5-3.5l-5.66 5.66M12.34 5.66L6.68 11.32M17.5 17.5l-5.66-5.66M5.66 17.5l5.66-5.66"></path>
                </svg>
                Settings
              </div> -->
              <div class="dropdown-divider"></div>
              <div class="dropdown-item logout" @click="logout">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                  <polyline points="16,17 21,12 16,7"></polyline>
                  <line x1="21" y1="12" x2="9" y2="12"></line>
                </svg>
                Logout
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>

    <div class="main-layout">
      <!-- Sidebar -->
      <aside class="sidebar">
        <div class="sidebar-content">
          <div class="sidebar-header">
            <h2>DASHBOARD</h2>
          </div>
          
          <nav class="sidebar-nav">
            <div class="nav-item" :class="{ active: $route.path.includes('/admin/dashboard') }">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                <circle cx="12" cy="7" r="4"></circle>
              </svg>
              <router-link to="/admin/dashboard" class="nav-link">Manage user page</router-link>
            </div>
        
            <div class="nav-item" :class="{ active: $route.path.includes('/admin/listings') }">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                <line x1="16" y1="2" x2="16" y2="6"></line>
                <line x1="8" y1="2" x2="8" y2="6"></line>
                <line x1="3" y1="10" x2="21" y2="10"></line>
              </svg>
              <router-link to="/admin/listings" class="nav-link">Manage Listings Page</router-link>
            </div> 
            
    <div class="nav-item" :class="{ active: $route.path.includes('/admin/reports') }">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                <polyline points="14,2 14,8 20,8"></polyline>
                <line x1="16" y1="13" x2="8" y2="13"></line>
                <line x1="16" y1="17" x2="8" y2="17"></line>
                <polyline points="10,9 9,9 8,9"></polyline>
              </svg>
              <router-link to="/admin/reports" class="nav-link">Reports / Logs Page</router-link>
            </div> 
          </nav>   </div>
      </aside>

      <!-- Main Content -->
      <main class="main-content">
        <div class="content-header">
          <button class="back-btn" @click="$router.go(-1)">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <polyline points="15,18 9,12 15,6"></polyline>
            </svg>
            Back
          </button>
        </div>
        
        <div class="page-content">
          <slot />
        </div>
      </main>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AdminLayout',
  data() {
    return {
      showUserMenu: false
    }
  },
  mounted() {
    // Close dropdown when clicking outside
    document.addEventListener('click', this.closeUserMenu)
  },
  beforeUnmount() {
    document.removeEventListener('click', this.closeUserMenu)
  },
  methods: {
    toggleUserMenu(event) {
      event.stopPropagation()
      this.showUserMenu = !this.showUserMenu
    },
    closeUserMenu(event) {
      if (event && event.target && !event.target.closest('.user-profile')) {
        this.showUserMenu = false
      }
    },
    goToProfile() {
      this.$router.push('/admin/profile')
      this.showUserMenu = false
    },
    goToSettings() {
      this.$router.push('/admin/settings')
      this.showUserMenu = false
    },
    logout() {
      // Clear authentication data
      localStorage.removeItem('access_token')
      localStorage.removeItem('user_role')
      localStorage.removeItem('user_data')
      
      // Show confirmation message
      this.$nextTick(() => {
        alert('You have been logged out successfully')
        // Redirect to login page
        this.$router.push('/login')
      })
      
      this.showUserMenu = false
    }
  }
}
</script>

<style scoped>
.admin-layout {
  min-height: 100vh;
  background: #f8f9fa;
}

/* Top Header */
.top-header {
  background: white;
  border-bottom: 1px solid #e9ecef;
  padding: 0 24px;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
  max-width: 1440px;
  margin: 0 auto;
}

.logo h1 {
  font-size: 20px;
  font-weight: 600;
  color: #212529;
  margin: 0;
}

.search-section {
  flex: 1;
  max-width: 400px;
  margin: 0 40px;
}

.search-bar {
  display: flex;
  align-items: center;
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 8px 12px;
  gap: 8px;
}

.search-bar svg {
  color: #6c757d;
}

.search-bar input {
  border: none;
  background: none;
  outline: none;
  flex: 1;
  font-size: 14px;
  color: #495057;
}

.search-bar input::placeholder {
  color: #adb5bd;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.notification-icon {
  padding: 8px;
  color: #6c757d;
  cursor: pointer;
  border-radius: 6px;
  transition: background-color 0.2s;
}

.notification-icon:hover {
  background: #f8f9fa;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px;
  cursor: pointer;
  border-radius: 8px;
  transition: background-color 0.2s;
  position: relative;
}

.user-profile:hover {
  background: #f8f9fa;
}

.user-avatar img,
.user-avatar .avatar-placeholder {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
}

.avatar-placeholder {
  background: #e9ecef;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  color: #6c757d;
  font-size: 14px;
}

.user-info {
  display: flex;
  flex-direction: column;
  text-align: left;
}

.user-name {
  font-size: 14px;
  font-weight: 500;
  color: #212529;
  line-height: 1.2;
}

.user-role {
  font-size: 12px;
  color: #6c757d;
  line-height: 1.2;
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

/* Main Layout */
.main-layout {
  display: flex;
  max-width: 1440px;
  margin: 0 auto;
}

/* Sidebar */
.sidebar {
  width: 240px;
  background: #f8f9fa;
  border-right: 1px solid #e9ecef;
  min-height: calc(100vh - 64px);
}

.sidebar-content {
  padding: 24px 0;
}

.sidebar-header {
  padding: 0 24px 16px;
  margin-bottom: 16px;
}

.sidebar-header h2 {
  font-size: 14px;
  font-weight: 600;
  color: #212529;
  margin: 0;
  letter-spacing: 0.5px;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 8px 24px;
  margin-bottom: 4px;
  transition: background-color 0.2s;
}

.nav-item:hover {
  background: #e9ecef;
}

.nav-item.active {
  background: #e7f3ff;
  border-right: 3px solid #0d6efd;
}

.nav-item svg {
  width: 16px;
  height: 16px;
  color: #6c757d;
  margin-right: 12px;
  flex-shrink: 0;
}

.nav-item.active svg {
  color: #0d6efd;
}

.nav-link {
  text-decoration: none;
  color: #495057;
  font-size: 14px;
  font-weight: 400;
  flex: 1;
}

.nav-item.active .nav-link {
  color: #0d6efd;
  font-weight: 500;
}

/* Main Content */
.main-content {
  flex: 1;
  background: white;
}

.content-header {
  padding: 16px 24px;
  border-bottom: 1px solid #e9ecef;
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  background: none;
  border: none;
  color: #6c757d;
  font-size: 14px;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 6px;
  transition: all 0.2s;
}

.back-btn:hover {
  background: #f8f9fa;
  color: #495057;
}

.page-content {
  padding: 24px;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .sidebar {
    width: 200px;
  }
  
  .search-section {
    margin: 0 20px;
  }
}

@media (max-width: 768px) {
  .header-content {
    padding: 0 16px;
  }
  
  .search-section {
    display: none;
  }
  
  .sidebar {
    position: fixed;
    left: -240px;
    top: 64px;
    height: calc(100vh - 64px);
    z-index: 50;
    transition: left 0.3s;
  }
  
  .main-content {
    width: 100%;
  }
  
  .page-content {
    padding: 16px;
  }
}
</style>
