<template>
  <SellerLayout>
    <div class="seller-dashboard">
      <!-- Dashboard Header -->
      <div class="dashboard-header">
        <div class="header-content">
          <h1>Seller Dashboard</h1>
          <p>Welcome back! Here's an overview of your store.</p>
        </div>
      </div>
      
      <!-- Stats Grid -->
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon">
        <svg width="24" height="24" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/>
        </svg>
          </div>
          <div class="stat-content">
        <h3 class="stat-number">{{ stats.totalItems }}</h3>
        <p class="stat-label">Total Items</p>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">
        <svg width="24" height="24" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
        </svg>
          </div>
          <div class="stat-content">
        <h3 class="stat-number">{{ stats.activeItems }}</h3>
        <p class="stat-label">Active Items</p>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">
        <svg width="24" height="24" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
        </svg>
          </div>
          <div class="stat-content">
        <h3 class="stat-number">{{ stats.pendingItems }}</h3>
        <p class="stat-label">Pending Items</p>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">
        <svg width="24" height="24" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"/>
        </svg>
          </div>
          <div class="stat-content">
        <h3 class="stat-number">{{ stats.soldItems }}</h3>
        <p class="stat-label">Sold Items</p>
          </div>
        </div>
      </div>
      
      <!-- Action Button -->
      <div class="action-section">
        <button class="create-item-btn" @click="goToCreateItem">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="12" y1="5" x2="12" y2="19"/>
            <line x1="5" y1="12" x2="19" y2="12"/>
          </svg>
          Add New Item
        </button>
      </div>
      
      <!-- Status Message -->
      <div class="status-message">
        <h3>Dashboard Active</h3>
        <p>Your seller dashboard is ready to use. Start managing your inventory.</p>
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
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

.seller-dashboard {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 32px;
  padding: 0;
  background: transparent;
  border-radius: 0;
  border: none;
}

.header-content h1 {
  margin: 0 0 4px 0;
  font-family: 'Inter', sans-serif;
  font-size: 28px;
  font-weight: 700;
  color: #111827;
  letter-spacing: -0.5px;
}

.header-content p {
  margin: 0;
  color: #6b7280;
  font-size: 14px;
  font-weight: 400;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

.stat-card {
  background: #ffffff;
  padding: 24px;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  gap: 16px;
  transition: all 0.2s ease;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  border-color: #d1d5db;
}

.stat-icon {
  font-size: 32px;
  width: 56px;
  height: 56px;
  background: #f3f4f6;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-content {
  flex: 1;
}

.stat-number {
  margin: 0 0 4px 0;
  font-family: 'Inter', sans-serif;
  font-size: 32px;
  font-weight: 700;
  color: #111827;
  line-height: 1;
  letter-spacing: -1px;
}

.stat-label {
  margin: 0;
  color: #6b7280;
  font-size: 14px;
  font-weight: 500;
}

.action-section {
  margin-bottom: 32px;
  text-align: left;
}

.create-item-btn {
  background: #000000;
  color: #ffffff;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  cursor: pointer;
  font-family: 'Inter', sans-serif;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.2s ease;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.create-item-btn:hover {
  background: #1f2937;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.status-message {
  padding: 24px;
  background: #ffffff;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  text-align: center;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.status-message h3 {
  margin: 0 0 8px 0;
  font-family: 'Inter', sans-serif;
  font-size: 18px;
  font-weight: 600;
  color: #111827;
}

.status-message p {
  margin: 0;
  color: #6b7280;
  font-size: 14px;
}

/* Responsive */
@media (max-width: 768px) {
  .seller-dashboard {
    padding: 0;
  }

  .dashboard-header {
    flex-direction: column;
    gap: 12px;
    align-items: stretch;
    padding: 0;
  }

  .header-content h1 {
    font-size: 24px;
  }

  .header-content p {
    font-size: 13px;
  }

  .stats-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .stat-card {
    padding: 20px;
  }

  .stat-icon {
    width: 48px;
    height: 48px;
    font-size: 24px;
  }

  .stat-number {
    font-size: 28px;
  }

  .stat-label {
    font-size: 13px;
  }

  .create-item-btn {
    width: 100%;
    padding: 12px 20px;
  }

  .status-message {
    padding: 20px;
  }

  .status-message h3 {
    font-size: 16px;
  }

  .status-message p {
    font-size: 13px;
  }
}
</style>
