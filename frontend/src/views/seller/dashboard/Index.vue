<template>
  <SellerLayout>
    <div class="seller-dashboard" style="padding: 20px; background: white; margin: 20px; border-radius: 8px;">
      <h1 style="color: #333; font-size: 24px; margin-bottom: 16px;">🎯 Seller Dashboard</h1>
      <p style="color: #666; font-size: 16px; margin-bottom: 20px;">Welcome to your seller dashboard! This content should be visible.</p>
      
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 24px;">
        <div style="background: #f8f9fa; padding: 16px; border-radius: 8px; border: 1px solid #dee2e6;">
          <h3 style="color: #007bff; margin: 0 0 8px 0;">📦 Total Items</h3>
          <p style="font-size: 24px; font-weight: bold; margin: 0; color: #333;">{{ stats.totalItems }}</p>
        </div>
        
        <div style="background: #f8f9fa; padding: 16px; border-radius: 8px; border: 1px solid #dee2e6;">
          <h3 style="color: #28a745; margin: 0 0 8px 0;">✅ Active Items</h3>
          <p style="font-size: 24px; font-weight: bold; margin: 0; color: #333;">{{ stats.activeItems }}</p>
        </div>
        
        <div style="background: #f8f9fa; padding: 16px; border-radius: 8px; border: 1px solid #dee2e6;">
          <h3 style="color: #ffc107; margin: 0 0 8px 0;">⏳ Pending Items</h3>
          <p style="font-size: 24px; font-weight: bold; margin: 0; color: #333;">{{ stats.pendingItems }}</p>
        </div>
        
        <div style="background: #f8f9fa; padding: 16px; border-radius: 8px; border: 1px solid #dee2e6;">
          <h3 style="color: #dc3545; margin: 0 0 8px 0;">💰 Sold Items</h3>
          <p style="font-size: 24px; font-weight: bold; margin: 0; color: #333;">{{ stats.soldItems }}</p>
        </div>
      </div>
      
      <div style="margin-top: 24px;">
        <button 
          @click="goToCreateItem"
          style="background: #007bff; color: white; border: none; padding: 12px 24px; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: 500;"
        >
          ➕ Add New Item
        </button>
      </div>
      
      <div style="margin-top: 24px; padding: 16px; background: #e7f3ff; border-radius: 8px; border: 1px solid #b8daff;">
        <h3 style="color: #0056b3; margin: 0 0 8px 0;">🎉 Content is Working!</h3>
        <p style="color: #0056b3; margin: 0;">If you can see this message, the slot system is working correctly.</p>
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
        
        <div class="stat-card">
          <div class="stat-icon">✅</div>
          <div class="stat-content">
            <h3 class="stat-number">{{ stats.activeItems }}</h3>
            <p class="stat-label">Active Listings</p>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">💰</div>
          <div class="stat-content">
            <h3 class="stat-number">{{ stats.soldItems }}</h3>
            <p class="stat-label">Items Sold</p>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">🕒</div>
          <div class="stat-content">
            <h3 class="stat-number">{{ stats.pendingItems }}</h3>
            <p class="stat-label">Pending Sales</p>
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="section">
        <div class="section-header">
          <h2 class="section-title">Quick Actions</h2>
        </div>
        
        <div class="quick-actions">
          <ActionButton
            variant="primary"
            icon="➕"
            text="Create Item"
            @click="goToCreateItem"
          />
          <ActionButton
            variant="info"
            icon="👁️"
            text="View All Items"
            @click="goToViewItems"
          />
          <ActionButton
            variant="secondary"
            icon="👤"
            text="Edit Profile"
            @click="goToProfile"
          />
          <ActionButton
            variant="success"
            icon="📊"
            text="Sales Report"
            @click="showComingSoon"
          />
        </div>
      </div>

      <!-- Recent Items -->
      <div class="section">
        <div class="section-header">
          <h2 class="section-title">Recent Items</h2>
          <router-link to="/seller/items" class="see-all-link">See all</router-link>
        </div>
        
        <div class="items-table">
          <div class="table-container">
            <table>
              <thead>
                <tr>
                  <th>Item</th>
                  <th>Price</th>
                  <th>Status</th>
                  <th>Created</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="recentItems.length === 0">
                  <td colspan="5" class="empty-state">
                    <div class="empty-content">
                      <i class="empty-icon">📦</i>
                      <p>No items yet. Create your first item to get started!</p>
                      <ActionButton
                        variant="primary"
                        icon="➕"
                        text="Create Item"
                        @click="goToCreateItem"
                      />
                    </div>
                  </td>
                </tr>
                <tr v-for="item in recentItems" :key="item.id">
                  <td>
                    <div class="item-info">
                      <div class="item-image">
                        <div class="image-placeholder">📷</div>
                      </div>
                      <div class="item-details">
                        <h4 class="item-title">{{ item.title }}</h4>
                        <p class="item-category">{{ item.category }}</p>
                      </div>
                    </div>
                  </td>
                  <td class="price">₱{{ item.price.toFixed(2) }}</td>
                  <td>
                    <span class="status-badge" :class="`status-${item.status}`">
                      {{ item.status }}
                    </span>
                  </td>
                  <td class="date">{{ formatDate(item.created_at) }}</td>
                  <td>
                    <div class="action-buttons">
                      <button class="icon-btn" @click="viewItem(item)" title="View">
                        👁️
                      </button>
                      <button class="icon-btn" @click="editItem(item)" title="Edit">
                        ✏️
                      </button>
                      <button class="icon-btn danger" @click="deleteItem(item)" title="Delete">
                        🗑️
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- Confirmation Modal -->
    <ConfirmationModal
      :show="showDeleteModal"
      :title="'Delete Item'"
      :message="`Are you sure you want to delete '${itemToDelete?.title}'? This action cannot be undone.`"
      type="danger"
      :loading="deleteLoading"
      @confirm="confirmDelete"
      @cancel="cancelDelete"
    />

    <!-- Message Toast -->
    <MessageToast
      :show="showMessage"
      :type="messageType"
      :title="messageTitle"
      :message="messageText"
      @close="hideMessage"
    />
  </SellerLayout>
</template>

<script>
import SellerLayout from '@/components/seller/SellerLayout.vue'
import ActionButton from '@/components/seller/shared/ActionButton.vue'
import ConfirmationModal from '@/components/seller/shared/ConfirmationModal.vue'
import MessageToast from '@/components/seller/shared/MessageToast.vue'

export default {
  name: 'SellerDashboard',
  components: {
    SellerLayout,
    ActionButton,
    ConfirmationModal,
    MessageToast
  },
  data() {
    return {
      stats: {
        totalItems: 0,
        activeItems: 0,
        soldItems: 0,
        pendingItems: 0
      },
      recentItems: [
        {
          id: 1,
          title: 'Vintage Watch Collection',
          category: 'Watches',
          price: 299.99,
          status: 'active',
          created_at: '2024-01-15T10:30:00Z'
        },
        {
          id: 2,
          title: 'Antique Vase',
          category: 'Antiques',
          price: 149.50,
          status: 'pending',
          created_at: '2024-01-14T14:20:00Z'
        },
        {
          id: 3,
          title: 'Rare Coin Set',
          category: 'Coins',
          price: 89.99,
          status: 'sold',
          created_at: '2024-01-13T09:15:00Z'
        }
      ],
      showDeleteModal: false,
      itemToDelete: null,
      deleteLoading: false,
      showMessage: false,
      messageType: 'info',
      messageTitle: '',
      messageText: ''
    }
  },
  mounted() {
    this.loadDashboardData();
  },
  methods: {
    loadDashboardData() {
      // Calculate stats from items
      this.stats.totalItems = this.recentItems.length;
      this.stats.activeItems = this.recentItems.filter(item => item.status === 'active').length;
      this.stats.soldItems = this.recentItems.filter(item => item.status === 'sold').length;
      this.stats.pendingItems = this.recentItems.filter(item => item.status === 'pending').length;
    },
    
    goToCreateItem() {
      this.$router.push('/seller/create-item');
    },
    
    goToViewItems() {
      this.$router.push('/seller/items');
    },
    
    goToProfile() {
      this.$router.push('/seller/profile');
    },
    
    showComingSoon() {
      this.showToast('Sales report feature coming soon!', 'info', 'Coming Soon');
    },
    
    viewItem(item) {
      this.$router.push(`/seller/items/${item.id}`);
    },
    
    editItem(item) {
      this.$router.push(`/seller/items/${item.id}/edit`);
    },
    
    deleteItem(item) {
      this.itemToDelete = item;
      this.showDeleteModal = true;
    },
    
    confirmDelete() {
      this.deleteLoading = true;
      
      // Simulate API call
      setTimeout(() => {
        const index = this.recentItems.findIndex(item => item.id === this.itemToDelete.id);
        if (index > -1) {
          this.recentItems.splice(index, 1);
          this.loadDashboardData();
          this.showToast(`Item '${this.itemToDelete.title}' has been deleted.`, 'success', 'Item Deleted');
        }
        
        this.deleteLoading = false;
        this.showDeleteModal = false;
        this.itemToDelete = null;
      }, 1500);
    },
    
    cancelDelete() {
      this.showDeleteModal = false;
      this.itemToDelete = null;
    },
    
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric'
      });
    },
    
    showToast(message, type = 'info', title = '') {
      this.messageText = message;
      this.messageType = type;
      this.messageTitle = title;
      this.showMessage = true;
    },
    
    hideMessage() {
      this.showMessage = false;
    }
  }
}
</script>

<style scoped>
.seller-dashboard {
  max-width: 1200px;
  margin: 0 auto;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 1px solid #e9ecef;
}

.header-content h1 {
  margin: 0 0 8px 0;
  font-size: 32px;
  font-weight: 700;
  color: #343a40;
}

.header-content p {
  margin: 0;
  color: #6c757d;
  font-size: 16px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.stat-card {
  background: white;
  padding: 24px;
  border-radius: 12px;
  border: 1px solid #e9ecef;
  display: flex;
  align-items: center;
  gap: 16px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  font-size: 40px;
  width: 60px;
  height: 60px;
  background: #f8f9fa;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-number {
  margin: 0 0 4px 0;
  font-size: 32px;
  font-weight: 700;
  color: #343a40;
}

.stat-label {
  margin: 0;
  color: #6c757d;
  font-size: 14px;
  font-weight: 500;
}

.section {
  margin-bottom: 32px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-title {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  color: #343a40;
}

.see-all-link {
  color: #007bff;
  text-decoration: none;
  font-weight: 500;
}

.see-all-link:hover {
  text-decoration: underline;
}

.quick-actions {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.items-table {
  background: white;
  border-radius: 12px;
  border: 1px solid #e9ecef;
  overflow: hidden;
}

.table-container {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 16px;
  text-align: left;
  border-bottom: 1px solid #e9ecef;
}

th {
  background: #f8f9fa;
  font-weight: 600;
  color: #495057;
  font-size: 14px;
}

.item-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.item-image {
  width: 48px;
  height: 48px;
}

.image-placeholder {
  width: 100%;
  height: 100%;
  background: #f8f9fa;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  color: #6c757d;
}

.item-title {
  margin: 0 0 4px 0;
  font-size: 14px;
  font-weight: 600;
  color: #343a40;
}

.item-category {
  margin: 0;
  font-size: 12px;
  color: #6c757d;
}

.price {
  font-weight: 600;
  color: #28a745;
}

.status-badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  text-transform: capitalize;
}

.status-active {
  background: #d4edda;
  color: #155724;
}

.status-pending {
  background: #fff3cd;
  color: #856404;
}

.status-sold {
  background: #d1ecf1;
  color: #0c5460;
}

.date {
  color: #6c757d;
  font-size: 14px;
}

.action-buttons {
  display: flex;
  gap: 8px;
}

.icon-btn {
  background: none;
  border: none;
  padding: 6px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: background 0.2s ease;
}

.icon-btn:hover {
  background: #f8f9fa;
}

.icon-btn.danger:hover {
  background: #f8d7da;
}

.empty-state {
  text-align: center;
  padding: 48px 24px;
}

.empty-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.empty-icon {
  font-size: 48px;
  opacity: 0.5;
}

.empty-content p {
  margin: 0;
  color: #6c757d;
  font-size: 16px;
}

/* Responsive */
@media (max-width: 768px) {
  .dashboard-header {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .quick-actions {
    justify-content: center;
  }
  
  .section-header {
    flex-direction: column;
    align-items: stretch;
    gap: 12px;
  }
}
</style>
