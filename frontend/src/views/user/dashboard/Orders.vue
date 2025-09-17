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
              <h3 class="order-id">Order #{{ order.order_number || order.id }}</h3>
              <p class="order-date">{{ formatDate(order.created_at) }}</p>
            </div>
            <div class="order-status">
              <span :class="['status-badge', order.status]">
                {{ getStatusText(order.status) }}
              </span>
            </div>
          </div>

          <div class="order-items">
            <div class="item-preview">
              <img 
                :src="getItemImage(order.item)" 
                :alt="order.item?.title || 'Item'" 
                class="item-image"
                @error="handleImageError"
              />
              <div class="item-details">
                <h4 class="item-title">{{ order.item?.title || 'Item not available' }}</h4>
                <p class="item-seller">Sold by {{ getSellerName(order.item) }}</p>
                <span class="item-quantity">Qty: {{ order.quantity || 1 }}</span>
              </div>
            </div>
          </div>

          <div class="order-footer">
            <div class="order-total">
              <span class="total-label">Total:</span>
              <span class="total-amount">₱{{ (order.total_amount || 0).toFixed(2) }}</span>
            </div>
            <div class="order-actions">

               <button 
                class="action-btn primary"
                @click.stop="viewOrderDetails(order)"
              >
                Message Seller
              </button>

              <button 
                v-if="order.status === 'delivered'" 
                class="action-btn secondary"
                @click.stop="reorderItems(order)"
              >
                Reorder
              </button>
              <button 
                v-if="order.status === 'delivered'" 
                :class="['action-btn', order.isRated ? 'disabled' : 'rating']"
                :disabled="order.isRated"
                @click.stop="rateItem(order)"
              >
                {{ order.isRated ? 'Already Rated' : 'Rate Item' }}
              </button>
              <button 
                v-if="order.status === 'pending' || order.status === 'processing'" 
                class="action-btn secondary"
                @click.stop="trackOrder(order)"
              >
                Track Order
              </button>
              <button 
                v-if="order.status === 'confirmed'" 
                class="action-btn success"
                @click.stop="markAsReceived(order)"
              >
                Order Received
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

  <!-- Confirm Order Modal -->
  <ConfirmOrderModal
    :show="showReorderModal"
    :item="selectedItemForReorder"
    @close="closeReorderModal"
    @order-confirmed="handleReorderConfirmed"
  />
</template>

<script>
import UserLayout from '@/components/user/UserLayout.vue'
import ConfirmOrderModal from '@/components/user/ConfirmOrderModal.vue'

export default {
  name: 'UserOrders',
  components: {
    UserLayout,
    ConfirmOrderModal
  },
  data() {
    return {
      selectedStatus: 'all',
      searchQuery: '',
      loading: true,
      orders: [],
      showReorderModal: false,
      selectedItemForReorder: null,
      orderStatuses: [
        { value: 'all', label: 'All Orders' },
        { value: 'pending', label: 'Pending' },
        { value: 'confirmed', label: 'Confirmed' },
        { value: 'shipped', label: 'Shipped' },
        { value: 'delivered', label: 'Delivered' },
        { value: 'cancelled', label: 'Cancelled' }
      ]
    }
  },
  computed: {
    filteredOrders() {
      let filtered = this.orders
      
      if (this.selectedStatus !== 'all') {
        filtered = filtered.filter(order => order.status === this.selectedStatus)
      }
      
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        filtered = filtered.filter(order => 
          order.order_number?.toLowerCase().includes(query) ||
          order.item?.title?.toLowerCase().includes(query) ||
          order.customer_name?.toLowerCase().includes(query)
        )
      }
      
      return filtered
    },
    
    totalOrders() {
      return this.orders.length
    },
    
    pendingOrders() {
      return this.orders.filter(order => order.status === 'pending').length
    },
    
    completedOrders() {
      return this.orders.filter(order => order.status === 'delivered').length
    }
  },
  mounted() {
    this.fetchOrders()
  },
  methods: {
    async fetchOrders() {
      try {
        this.loading = true
        const token = localStorage.getItem('access_token') || localStorage.getItem('token')
        if (!token) {
          this.$router.push('/login')
          return
        }

        const response = await fetch('http://localhost:5000/api/user/orders', {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })

        if (!response.ok) {
          throw new Error('Failed to fetch orders')
        }

        const data = await response.json()
        this.orders = data.orders || []
        
        // Check rating status for each order
        await this.checkRatingStatus()
      } catch (error) {
        console.error('Error fetching orders:', error)
        this.orders = []
      } finally {
        this.loading = false
      }
    },

    async checkRatingStatus() {
      const token = localStorage.getItem('access_token') || localStorage.getItem('token')
      if (!token || this.orders.length === 0) return

      try {
        // Check rating status for each delivered order
        for (let order of this.orders) {
          if (order.status === 'delivered' && order.item?.id) {
            const response = await fetch(`http://localhost:5000/api/user/ratings/check/${order.item.id}`, {
              headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
              }
            })

            if (response.ok) {
              const ratingData = await response.json()
              order.isRated = ratingData.is_rated || false
            } else {
              order.isRated = false
            }
          }
        }
      } catch (error) {
        console.error('Error checking rating status:', error)
      }
    },
    
    formatDate(dateString) {
      if (!dateString) return 'N/A'
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
        confirmed: 'Confirmed',
        declined: 'Declined',
        shipped: 'Shipped',
        delivered: 'Delivered',
        cancelled: 'Cancelled'
      }
      return statusMap[status] || status
    },
    
    getItemImage(item) {
      console.log('Orders.vue - getItemImage called with item:', item);
      
      // Handle images array from API (most common case)
      if (item?.images && Array.isArray(item.images) && item.images.length > 0) {
        // Find primary image first, then fallback to first image
        const primaryImage = item.images.find(img => img.is_primary || img.isPrimary) || item.images[0];
        if (primaryImage?.url) {
          let imageUrl = primaryImage.url;
          
          // Fix duplicate path issue (e.g., /uploads/items/13/13/image_0.png)
          if (imageUrl.includes('/uploads/items/')) {
            const regex = /\/uploads\/items\/(\d+)\/\1\//;
            const match = imageUrl.match(regex);
            if (match) {
              const itemId = match[1];
              imageUrl = imageUrl.replace(`/uploads/items/${itemId}/${itemId}/`, `/uploads/items/${itemId}/`);
              console.log('Fixed duplicate path, corrected URL:', imageUrl);
            }
          }
          
          console.log('Using images array primary/first url:', imageUrl);
          return imageUrl;
        }
      }
      
      // Handle primary_image object from API
      if (item?.primary_image?.url) {
        let imageUrl = item.primary_image.url;
        
        // Fix duplicate path issue
        if (imageUrl.includes('/uploads/items/')) {
          const regex = /\/uploads\/items\/(\d+)\/\1\//;
          const match = imageUrl.match(regex);
          if (match) {
            const itemId = match[1];
            imageUrl = imageUrl.replace(`/uploads/items/${itemId}/${itemId}/`, `/uploads/items/${itemId}/`);
            console.log('Fixed duplicate path in primary_image, corrected URL:', imageUrl);
          }
        }
        
        console.log('Using primary_image.url:', imageUrl);
        return imageUrl;
      }
      
      // Handle primary_image as string (direct URL)
      if (item?.primary_image && typeof item.primary_image === 'string') {
        console.log('Using primary_image string:', item.primary_image);
        return item.primary_image.startsWith('http') ? item.primary_image : `http://localhost:5000${item.primary_image}`;
      }
      
      // Handle legacy image_url or image properties
      if (item?.image_url) {
        console.log('Using image_url:', item.image_url);
        return item.image_url.startsWith('http') ? item.image_url : `http://localhost:5000${item.image_url}`;
      }
      
      if (item?.image) {
        console.log('Using image:', item.image);
        return item.image.startsWith('http') ? item.image : `http://localhost:5000${item.image}`;
      }
      
      // Try to construct image URL from item ID if available
      if (item?.id) {
        const constructedUrl = `http://localhost:5000/uploads/items/${item.id}/image_0.jpeg`;
        console.log('Attempting constructed URL:', constructedUrl);
        return constructedUrl;
      }
      
      console.log('Using placeholder image for item:', item?.id);
      return 'http://localhost:5000/uploads/placeholder.svg';
    },

    handleImageError(event) {
      console.log('Image failed to load, using placeholder');
      event.target.src = 'http://localhost:5000/uploads/placeholder.svg';
    },

    getSellerName(item) {
      return item?.seller?.username || item?.seller_name || 'Unknown Seller';
    },
    
    viewOrderDetails(order) {
      this.$router.push(`/user/orders/${order.id}`)
    },
    
    async markAsReceived(order) {
      try {
        const token = localStorage.getItem('access_token') || localStorage.getItem('token')
        if (!token) {
          this.$router.push('/login')
          return
        }

        const response = await fetch(`http://localhost:5000/api/user/orders/${order.id}/received`, {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })

        if (!response.ok) {
          throw new Error('Failed to mark order as received')
        }

        // Update the order status locally
        const orderIndex = this.orders.findIndex(o => o.id === order.id)
        if (orderIndex !== -1) {
          this.orders[orderIndex].status = 'delivered'
        }

        // Show success message
        alert('Order marked as received successfully!')
      } catch (error) {
        console.error('Error marking order as received:', error)
        alert('Failed to mark order as received. Please try again.')
      }
    },
    
    trackOrder(order) {
      console.log('Track order:', order.order_number)
    },
    
    reorderItems(order) {
      // Show reorder modal with item details
      if (order.item?.id) {
        this.selectedItemForReorder = order.item
        this.showReorderModal = true
      } else {
        alert('Item is no longer available for reorder')
      }
    },

    closeReorderModal() {
      this.showReorderModal = false
      this.selectedItemForReorder = null
    },

    handleReorderConfirmed(orderData) {
      console.log('Reorder confirmed:', orderData)
      this.closeReorderModal()
      // You can add additional logic here like showing a success message
      alert('Reorder placed successfully!')
    },

    rateItem(order) {
      // Don't navigate if item is already rated
      if (order.isRated) {
        return
      }
      
      // Navigate to ratings page with order data for rating the item
      this.$router.push({
        path: '/user/ratings',
        query: {
          orderId: order.id,
          itemId: order.item?.id,
          itemTitle: order.item?.title,
          sellerId: order.item?.seller_id || order.seller_id
        }
      })
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

.action-btn.rating {
  background: #fbbf24;
  color: white;
}

.action-btn.rating:hover {
  background: #f59e0b;
}

.action-btn.disabled {
  background: #9ca3af;
  color: white;
  cursor: not-allowed;
}

.action-btn.disabled:hover {
  background: #9ca3af;
}

.action-btn.success {
  background: #10b981;
  color: white;
}

.action-btn.success:hover {
  background: #059669;
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
