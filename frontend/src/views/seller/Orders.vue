<template>
  <SellerLayout>
    <div class="seller-orders">
      <!-- Page Header -->
      <div class="page-header">
        <div class="header-content">
          <h1 class="page-title">Orders</h1>
          <p class="page-subtitle">Manage your sales and transactions</p>
        </div>
      </div>

      <!-- Coming Soon Message -->
      <div class="coming-soon">
        <div class="coming-soon-content">
          <div class="icon">🚧</div>
          <h2>Orders Management Coming Soon</h2>
          <p>We're working hard to bring you a comprehensive orders management system. This feature will include:</p>
          
          <div class="features-grid">
            <div class="feature-item">
              <div class="feature-icon">📦</div>
              <h3>Order Tracking</h3>
              <p>Track all your sales from inquiry to completion</p>
            </div>
            
            <div class="feature-item">
              <div class="feature-icon">💰</div>
              <h3>Payment Management</h3>
              <p>Handle payments and financial transactions</p>
            </div>
            
            <div class="feature-item">
              <div class="feature-icon">📋</div>
              <h3>Order History</h3>
              <p>Complete history of all your transactions</p>
            </div>
            
            <div class="feature-item">
              <div class="feature-icon">🔔</div>
              <h3>Notifications</h3>
              <p>Get notified about new orders and updates</p>
            </div>
          </div>
          
          <div class="action-buttons">
            <ActionButton
              variant="primary"
              icon="📊"
              text="View Dashboard"
              @click="goToDashboard"
            />
            <ActionButton
              variant="secondary"
              icon="📦"
              text="Manage Items"
              @click="goToItems"
            />
          </div>
        </div>
      </div>
    </div>
  </SellerLayout>
</template>

<script>
import SellerLayout from '@/components/seller/SellerLayout.vue'
import ActionButton from '@/components/seller/shared/ActionButton.vue'

export default {
  name: 'SellerOrders',
  components: {
    SellerLayout,
    ActionButton
  },
  methods: {
    goToDashboard() {
      this.$router.push('/seller/dashboard');
    },
    
    goToItems() {
      this.$router.push('/seller/items');
    }
  }
}
</script>

<style scoped>
.seller-orders {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 48px;
  padding-bottom: 24px;
  border-bottom: 1px solid #e9ecef;
}

.page-title {
  margin: 0 0 8px 0;
  font-size: 32px;
  font-weight: 700;
  color: #343a40;
}

.page-subtitle {
  margin: 0;
  color: #6c757d;
  font-size: 16px;
}

.coming-soon {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 500px;
}

.coming-soon-content {
  text-align: center;
  max-width: 800px;
  padding: 48px;
  background: white;
  border-radius: 16px;
  border: 1px solid #e9ecef;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.coming-soon-content .icon {
  font-size: 64px;
  margin-bottom: 24px;
}

.coming-soon-content h2 {
  margin: 0 0 16px 0;
  font-size: 28px;
  font-weight: 700;
  color: #343a40;
}

.coming-soon-content > p {
  margin: 0 0 40px 0;
  font-size: 16px;
  color: #6c757d;
  line-height: 1.6;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 32px;
  margin-bottom: 40px;
}

.feature-item {
  text-align: center;
  padding: 24px;
  background: #f8f9fa;
  border-radius: 12px;
  border: 1px solid #e9ecef;
}

.feature-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.feature-item h3 {
  margin: 0 0 8px 0;
  font-size: 18px;
  font-weight: 600;
  color: #343a40;
}

.feature-item p {
  margin: 0;
  font-size: 14px;
  color: #6c757d;
  line-height: 1.5;
}

.action-buttons {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
}

/* Responsive */
@media (max-width: 768px) {
  .coming-soon-content {
    padding: 32px 24px;
    margin: 0 16px;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
    gap: 24px;
  }
  
  .action-buttons {
    flex-direction: column;
    align-items: center;
  }
}
</style>
