<template>
  <SellerLayout>
    <div class="seller-dashboard">
      <div class="dashboard-header">
        <h1 class="page-title">Seller Dashboard</h1>
        <p class="page-subtitle">Welcome to your seller dashboard!</p>
      </div>
      
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon"></div>
          <div class="stat-content">
            <h3 class="stat-label">Total Items</h3>
            <p class="stat-value">{{ stats.totalItems }}</p>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon"></div>
          <div class="stat-content">
            <h3 class="stat-label">Active Items</h3>
            <p class="stat-value">{{ stats.activeItems }}</p>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon"></div>
          <div class="stat-content">
            <h3 class="stat-label">Pending Items</h3>
            <p class="stat-value">{{ stats.pendingItems }}</p>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon"></div>
          <div class="stat-content">
            <h3 class="stat-label">Sold Items</h3>
            <p class="stat-value">{{ stats.soldItems }}</p>
          </div>
        </div>
      </div>
      
      <div class="dashboard-section">
        <h2 class="section-title">Quick Actions</h2>
        <div class="quick-actions">
          <button class="action-btn primary" @click="goToCreateItem">
             Create Item
          </button>
          <button class="action-btn secondary" @click="goToViewItems">
             View All Items
          </button>
          <button class="action-btn secondary" @click="goToProfile">
             Edit Profile
          </button>
        </div>
      </div>
    </div>
  </SellerLayout>
</template>

<script>
import SellerLayout from '@/components/seller/SellerLayout.vue'

export default {
  name: 'SellerDashboard',
  components: {
    SellerLayout
  },
  data() {
    return {
      stats: {
        totalItems: 12,
        activeItems: 8,
        soldItems: 3,
        pendingItems: 1
      }
    }
  },
  methods: {
    goToCreateItem() {
      this.$router.push('/seller/create-item')
    },
    goToViewItems() {
      this.$router.push('/seller/items')
    },
    goToProfile() {
      this.$router.push('/seller/profile')
    }
  }
}
</script>

<style scoped lang="scss">
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400;1,500;1,600;1,700;1,800&family=Inter:wght@300;400;500;600;700&display=swap');

.seller-dashboard {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  background: #ffffff;
  min-height: 100vh;
}

.dashboard-header {
  margin-bottom: 2.5rem;
  
  .page-title {
    font-family: 'Playfair Display', serif;
    font-style: italic;
    font-weight: 800;
    font-size: 2.5rem;
    letter-spacing: -1px;
    color: #1f2937;
    margin: 0 0 0.5rem 0;
  }
  
  .page-subtitle {
    font-family: 'Inter', sans-serif;
    font-size: 1.125rem;
    color: #6b7280;
    margin: 0;
  }
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.stat-card {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: all 0.2s ease;
  
  &:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    border-color: #d1d5db;
  }
  
  .stat-icon {
    width: 48px;
    height: 48px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    background: #f9fafb;
  }
  
  .stat-content {
    .stat-label {
      font-family: 'Inter', sans-serif;
      font-size: 0.875rem;
      font-weight: 500;
      color: #6b7280;
      margin: 0 0 0.25rem 0;
    }
    
    .stat-value {
      font-family: 'Playfair Display', serif;
      font-size: 1.875rem;
      font-weight: 700;
      color: #1f2937;
      margin: 0;
    }
  }
}

.dashboard-section {
  margin-bottom: 3rem;
  
  .section-title {
    font-family: 'Playfair Display', serif;
    font-style: italic;
    font-weight: 600;
    font-size: 1.5rem;
    color: #1f2937;
    margin: 0 0 1.5rem 0;
  }
}

.quick-actions {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.action-btn {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 1rem 1.5rem;
  font-family: 'Inter', sans-serif;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  
  &:hover {
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  }
  
  &.primary {
    background: #3b82f6;
    color: #ffffff;
    border-color: #3b82f6;
    
    &:hover {
      background: #2563eb;
      border-color: #2563eb;
    }
  }
  
  &.secondary {
    color: #374151;
    
    &:hover {
      background: #f9fafb;
      border-color: #d1d5db;
    }
  }
}

@media (max-width: 768px) {
  .seller-dashboard {
    padding: 1rem;
  }
  
  .dashboard-header .page-title {
    font-size: 2rem;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .quick-actions {
    grid-template-columns: 1fr;
  }
}
</style>
