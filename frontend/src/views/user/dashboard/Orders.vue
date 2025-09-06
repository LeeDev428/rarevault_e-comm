<template>
  <UserLayout>
    <div class="orders-container">
      <div class="orders-header">
        <h1 class="page-title">My Orders</h1>
        <div class="orders-stats">
          <div class="stat-card">
            <span class="stat-number">{{ totalOrders }}</span>
            <span class="stat-label">Total Orders</span>
          </div>
          <div class="stat-card">
            <span class="stat-number">{{ pendingOrders }}</span>
            <span class="stat-label">Pending</span>
          </div>
          <div class="stat-card">
            <span class="stat-number">{{ completedOrders }}</span>
            <span class="stat-label">Completed</span>
          </div>
        </div>
      </div>

      <!-- Order Filters -->
      <div class="order-filters">
        <div class="filter-tabs">
          <button 
            v-for="status in orderStatuses" 
            :key="status.value"
            @click="selectedStatus = status.value"
            :class="['filter-tab', { active: selectedStatus === status.value }]"
          >
            {{ status.label }}
          </button>
        </div>
        
        <div class="search-filter">
          <input 
            type="text" 
            placeholder="Search orders..." 
            v-model="searchQuery"
            class="search-input"
          />
        </div>
      </div>

      <!-- Orders List -->
      <div class="orders-list">
        <div 
          v-for="order in filteredOrders" 
          :key="order.id"
          class="order-card"
          @click="viewOrderDetails(order)"
        >
          <div class="order-header">
            <div class="order-info">
              <h3 class="order-id">Order #{{ order.id }}</h3>
              <p class="order-date">{{ formatDate(order.orderDate) }}</p>
            </div>
            <div class="order-status">
              <span :class="['status-badge', order.status]">
                {{ getStatusText(order.status) }}
              </span>
            </div>
          </div>

          <div class="order-items">
            <div class="item-preview">
              <img :src="order.items[0].image" :alt="order.items[0].title" class="item-image" />
              <div class="item-details">
                <h4 class="item-title">{{ order.items[0].title }}</h4>
                <p class="item-seller">Sold by {{ order.items[0].seller }}</p>
                <span v-if="order.items.length > 1" class="more-items">
                  +{{ order.items.length - 1 }} more item{{ order.items.length > 2 ? 's' : '' }}
                </span>
              </div>
            </div>
          </div>

          <div class="order-footer">
            <div class="order-total">
              <span class="total-label">Total:</span>
              <span class="total-amount">${{ order.total.toFixed(2) }}</span>
            </div>
            <div class="order-actions">
              <button 
                v-if="order.status === 'delivered'" 
                class="action-btn secondary"
                @click.stop="reorderItems(order)"
              >
                Reorder
              </button>
              <button 
                v-if="order.status === 'pending' || order.status === 'processing'" 
                class="action-btn secondary"
                @click.stop="trackOrder(order)"
              >
                Track Order
              </button>
              <button 
                class="action-btn primary"
                @click.stop="viewOrderDetails(order)"
              >
                View Details
              </button>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-if="filteredOrders.length === 0" class="empty-state">
          <div class="empty-icon">
            <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M9 12l2 2 4-4"/>
              <path d="M21 12c-1 0-3-1-3-3s2-3 3-3 3 1 3 3-2 3-3 3"/>
              <path d="M3 12c1 0 3-1 3-3s-2-3-3-3-3 1-3 3 2 3 3 3"/>
            </svg>
          </div>
          <h3>No orders found</h3>
          <p>{{ selectedStatus === 'all' ? 'You haven\'t placed any orders yet.' : `No ${selectedStatus} orders found.` }}</p>
          <router-link to="/user/dashboard" class="btn-primary">
            Browse Items
          </router-link>
        </div>
      </div>
    </div>
  </UserLayout>
</template>

<script>
import UserLayout from '@/components/user/UserLayout.vue'

export default {
  name: 'UserOrders',
  components: {
    UserLayout
  },
  data() {
    return {
      selectedStatus: 'all',
      searchQuery: '',
      orderStatuses: [
        { value: 'all', label: 'All Orders' },
        { value: 'pending', label: 'Pending' },
        { value: 'processing', label: 'Processing' },
        { value: 'shipped', label: 'Shipped' },
        { value: 'delivered', label: 'Delivered' },
        { value: 'cancelled', label: 'Cancelled' }
      ],
      orders: [
        {
          id: '20240001',
          orderDate: '2024-03-15',
          status: 'delivered',
          total: 345.00,
          items: [
            {
              title: 'Vintage Pocket Watch',
              seller: 'Vintage Items',
              image: '/api/placeholder/60/60'
            },
            {
              title: 'Antique Silver Spoons',
              seller: 'Vintage Items',
              image: '/api/placeholder/60/60'
            }
          ]
        },
        {
          id: '20240002',
          orderDate: '2024-03-18',
          status: 'shipped',
          total: 120.00,
          items: [
            {
              title: 'Vintage Wrist Watch',
              seller: 'Vintage Items',
              image: '/api/placeholder/60/60'
            }
          ]
        },
        {
          id: '20240003',
          orderDate: '2024-03-20',
          status: 'processing',
          total: 85.00,
          items: [
            {
              title: 'Vintage Cola Sign',
              seller: 'Vintage Items',
              image: '/api/placeholder/60/60'
            }
          ]
        },
        {
          id: '20240004',
          orderDate: '2024-03-22',
          status: 'pending',
          total: 200.00,
          items: [
            {
              title: 'Vintage Camera',
              seller: 'Vintage Items',
              image: '/api/placeholder/60/60'
            }
          ]
        }
      ]
    }
  },
  computed: {
    filteredOrders() {
      let filtered = this.orders

      // Filter by status
      if (this.selectedStatus !== 'all') {
        filtered = filtered.filter(order => order.status === this.selectedStatus)
      }

      // Filter by search query
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        filtered = filtered.filter(order => 
          order.id.toLowerCase().includes(query) ||
          order.items.some(item => 
            item.title.toLowerCase().includes(query) ||
            item.seller.toLowerCase().includes(query)
          )
        )
      }

      return filtered
    },
    
    totalOrders() {
      return this.orders.length
    },
    
    pendingOrders() {
      return this.orders.filter(order => 
        order.status === 'pending' || order.status === 'processing'
      ).length
    },
    
    completedOrders() {
      return this.orders.filter(order => order.status === 'delivered').length
    }
  },
  methods: {
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
      })
    },
    
    getStatusText(status) {
      const statusMap = {
        pending: 'Pending',
        processing: 'Processing',
        shipped: 'Shipped',
        delivered: 'Delivered',
        cancelled: 'Cancelled'
      }
      return statusMap[status] || status
    },
    
    viewOrderDetails(order) {
      this.$router.push(`/user/orders/${order.id}`)
    },
    
    trackOrder(order) {
      console.log('Track order:', order.id)
    },
    
    reorderItems(order) {
      console.log('Reorder items from order:', order.id)
    }
  }
}
</script>

<style scoped>
.orders-container {
  max-width: 1200px;
  margin: 0 auto;
}

/* Orders Header */
.orders-header {
  margin-bottom: 32px;
}

.page-title {
  font-size: 32px;
  font-weight: 700;
  color: #111827;
  margin: 0 0 24px 0;
}

.orders-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 16px;
}

.stat-card {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.stat-number {
  display: block;
  font-size: 28px;
  font-weight: 700;
  color: #3b82f6;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #6b7280;
  font-weight: 500;
}

/* Order Filters */
.order-filters {
  background: white;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 24px;
}

.filter-tabs {
  display: flex;
  gap: 8px;
}

.filter-tab {
  padding: 8px 16px;
  border: none;
  background: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s ease;
}

.filter-tab:hover {
  background: #f3f4f6;
  color: #374151;
}

.filter-tab.active {
  background: #eff6ff;
  color: #2563eb;
}

.search-filter {
  min-width: 250px;
}

.search-input {
  width: 100%;
  padding: 10px 16px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 14px;
}

.search-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* Orders List */
.orders-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.order-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: all 0.2s ease;
}

.order-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
}

.order-id {
  font-size: 18px;
  font-weight: 600;
  color: #111827;
  margin: 0 0 4px 0;
}

.order-date {
  font-size: 14px;
  color: #6b7280;
  margin: 0;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-badge.pending {
  background: #fef3c7;
  color: #92400e;
}

.status-badge.processing {
  background: #dbeafe;
  color: #1d4ed8;
}

.status-badge.shipped {
  background: #e0e7ff;
  color: #3730a3;
}

.status-badge.delivered {
  background: #d1fae5;
  color: #065f46;
}

.status-badge.cancelled {
  background: #fee2e2;
  color: #991b1b;
}

/* Order Items */
.order-items {
  margin-bottom: 20px;
}

.item-preview {
  display: flex;
  gap: 16px;
  align-items: center;
}

.item-image {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  object-fit: cover;
}

.item-details {
  flex: 1;
}

.item-title {
  font-size: 16px;
  font-weight: 600;
  color: #111827;
  margin: 0 0 4px 0;
}

.item-seller {
  font-size: 14px;
  color: #6b7280;
  margin: 0 0 4px 0;
}

.more-items {
  font-size: 12px;
  color: #9ca3af;
  font-style: italic;
}

/* Order Footer */
.order-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid #e5e7eb;
  padding-top: 20px;
}

.total-label {
  font-size: 14px;
  color: #6b7280;
  margin-right: 8px;
}

.total-amount {
  font-size: 20px;
  font-weight: 700;
  color: #111827;
}

.order-actions {
  display: flex;
  gap: 12px;
}

.action-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-btn.primary {
  background: #3b82f6;
  color: white;
}

.action-btn.primary:hover {
  background: #2563eb;
}

.action-btn.secondary {
  background: #f3f4f6;
  color: #374151;
}

.action-btn.secondary:hover {
  background: #e5e7eb;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.empty-icon {
  margin-bottom: 24px;
  color: #9ca3af;
}

.empty-state h3 {
  font-size: 20px;
  font-weight: 600;
  color: #374151;
  margin: 0 0 8px 0;
}

.empty-state p {
  font-size: 16px;
  color: #6b7280;
  margin: 0 0 24px 0;
}

.btn-primary {
  display: inline-block;
  padding: 12px 24px;
  background: #3b82f6;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 500;
  transition: background 0.2s ease;
}

.btn-primary:hover {
  background: #2563eb;
}

/* Responsive */
@media (max-width: 768px) {
  .order-filters {
    flex-direction: column;
    align-items: stretch;
    gap: 16px;
  }
  
  .filter-tabs {
    overflow-x: auto;
    padding-bottom: 8px;
  }
  
  .search-filter {
    min-width: auto;
  }
  
  .order-footer {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }
  
  .order-actions {
    justify-content: center;
  }
  
  .orders-stats {
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  }
}
</style>
