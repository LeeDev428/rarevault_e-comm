<template>
  <SellerLayout>
    <div class="seller-dashboard">
      <!-- Dashboard Header -->
      <div class="dashboard-header">
        <div class="header-content">
          <h1>🎯 Seller Dashboard</h1>
          <p>Welcome to your seller dashboard! This content should be visible.</p>
        </div>
      </div>
      
      <!-- Stats Grid -->
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon">📦</div>
          <div class="stat-content">
            <h3 class="stat-number">{{ stats.totalItems }}</h3>
            <p class="stat-label">Total Items</p>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">✅</div>
          <div class="stat-content">
            <h3 class="stat-number">{{ stats.activeItems }}</h3>
            <p class="stat-label">Active Items</p>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">⏳</div>
          <div class="stat-content">
            <h3 class="stat-number">{{ stats.pendingItems }}</h3>
            <p class="stat-label">Pending Items</p>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">💰</div>
          <div class="stat-content">
            <h3 class="stat-number">{{ stats.soldItems }}</h3>
            <p class="stat-label">Sold Items</p>
          </div>
        </div>
      </div>
      
      <!-- Action Button -->
      <div class="action-section">
        <button class="create-item-btn" @click="goToCreateItem">
          ➕ Add New Item
        </button>
      </div>
      
      <!-- Status Message -->
      <div class="status-message">
        <h3>🎉 Content is Working!</h3>
        <p>If you can see this message, the slot system is working correctly.</p>
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
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

.seller-dashboard {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px;
  font-family: 'Inter', sans-serif;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 48px;
  padding: 32px;
  background: linear-gradient(135deg, #f8f6f1 0%, #e8ddd4 100%);
  border-radius: 24px;
  border: 1px solid #d4af94;
}

.header-content h1 {
  margin: 0 0 8px 0;
  font-family: 'Playfair Display', serif;
  font-size: 36px;
  font-weight: 600;
  color: #8b5a3c;
  text-shadow: 0 2px 4px rgba(139, 90, 60, 0.1);
}

.header-content p {
  margin: 0;
  color: #8b5a3c;
  font-size: 16px;
  font-weight: 400;
  opacity: 0.8;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 32px;
  margin-bottom: 48px;
}

.stat-card {
  background: linear-gradient(135deg, #f8f6f1 0%, #e8ddd4 100%);
  padding: 32px;
  border-radius: 20px;
  border: 1px solid #d4af94;
  display: flex;
  align-items: center;
  gap: 20px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(139, 90, 60, 0.08);
}

.stat-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 30px rgba(139, 90, 60, 0.15);
  border-color: #8b5a3c;
}

.stat-icon {
  font-size: 48px;
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #8b5a3c 0%, #d4af94 100%);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 15px rgba(139, 90, 60, 0.2);
}

.stat-content {
  flex: 1;
}

.stat-number {
  margin: 0 0 8px 0;
  font-family: 'Playfair Display', serif;
  font-size: 42px;
  font-weight: 700;
  color: #8b5a3c;
  line-height: 1;
}

.stat-label {
  margin: 0;
  color: #8b5a3c;
  font-size: 16px;
  font-weight: 500;
  opacity: 0.8;
}

.action-section {
  margin-bottom: 48px;
  text-align: center;
}

.create-item-btn {
  background: linear-gradient(135deg, #8b5a3c 0%, #d4af94 100%);
  color: #f8f6f1;
  border: none;
  padding: 16px 32px;
  border-radius: 16px;
  cursor: pointer;
  font-family: 'Inter', sans-serif;
  font-size: 16px;
  font-weight: 600;
  letter-spacing: 0.5px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(139, 90, 60, 0.2);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.create-item-btn:hover {
  background: linear-gradient(135deg, #6d4530 0%, #c19a7a 100%);
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(139, 90, 60, 0.3);
}

.status-message {
  padding: 32px;
  background: linear-gradient(135deg, #e8ddd4 0%, #d4af94 100%);
  border-radius: 20px;
  border: 1px solid #8b5a3c;
  text-align: center;
  box-shadow: 0 4px 15px rgba(139, 90, 60, 0.1);
}

.status-message h3 {
  margin: 0 0 12px 0;
  font-family: 'Playfair Display', serif;
  font-size: 24px;
  font-weight: 600;
  color: #8b5a3c;
}

.status-message p {
  margin: 0;
  color: #8b5a3c;
  font-size: 16px;
  opacity: 0.9;
}

/* Responsive */
@media (max-width: 768px) {
  .seller-dashboard {
    padding: 16px;
  }

  .dashboard-header {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
    padding: 24px;
  }

  .header-content h1 {
    font-size: 28px;
  }

  .stats-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .stat-card {
    padding: 24px;
  }

  .stat-icon {
    width: 60px;
    height: 60px;
    font-size: 32px;
  }

  .stat-number {
    font-size: 32px;
  }

  .create-item-btn {
    padding: 14px 28px;
    font-size: 14px;
  }

  .status-message {
    padding: 24px;
  }

  .status-message h3 {
    font-size: 20px;
  }
}
</style>
