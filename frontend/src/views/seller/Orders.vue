<template>
  <SellerLayout>
    <div class="seller-orders">
      <!-- Page Header -->
      <div class="page-header">
        <div class="header-content">
          <h1 class="page-title">Orders</h1>
          <p class="page-subtitle">Manage your sales and transactions</p>
        </div>
        
        <!-- Filter and Status Bar -->
        <div class="filter-bar">
          <div class="filter-group">
            <label for="status-filter">Status:</label>
            <select id="status-filter" v-model="selectedStatus" @change="loadOrders">
              <option value="">All Orders</option>
              <option value="pending">Pending</option>
              <option value="confirmed">Confirmed</option>
              <option value="cancelled">Cancelled</option>
              <option value="completed">Completed</option>
            </select>
          </div>
          
          <div class="orders-count">
            Total Orders: {{ totalOrders }}
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Loading orders...</p>
      </div>

      <!-- No Orders State -->
      <div v-else-if="!orders.length" class="no-orders">
        <div class="no-orders-content">
          <div class="icon">�</div>
          <h2>No Orders Yet</h2>
          <p>You haven't received any orders yet. When customers place orders for your items, they'll appear here.</p>
          <ActionButton
            variant="primary"
            icon="📦"
            text="Manage Items"
            @click="goToItems"
          />
        </div>
      </div>

      <!-- Orders List -->
      <div v-else class="orders-list">
        <div v-for="order in orders" :key="order.id" class="order-card">
          <div class="order-header">
            <div class="order-id">#{{ order.id }}</div>
            <div class="order-date">{{ formatDate(order.created_at) }}</div>
            <div class="order-status" :class="'status-' + order.status">
              {{ order.status.charAt(0).toUpperCase() + order.status.slice(1) }}
            </div>
          </div>
          
          <div class="order-body">
            <div class="item-info">
              <img 
                :src="getItemImage(order.item)" 
                :alt="order.item ? (order.item.title || order.item.name) : 'Item Image'"
                class="item-image"
                @error="handleImageError"
              />
              <div class="item-details">
                <h3 class="item-name">{{ order.item ? (order.item.title || order.item.name) : 'Item Deleted' }}</h3>
                <p class="item-category">{{ order.item ? order.item.category : 'N/A' }}</p>
                <p class="item-price">₱{{ order.item ? parseFloat(order.item.price).toFixed(2) : '0.00' }}</p>
                <p class="item-quantity"><strong>Quantity:</strong> {{ order.quantity || 1 }}</p>
                <p class="total-amount"><strong>Total:</strong> ₱{{ parseFloat(order.total_amount || (order.item ? order.item.price : 0) * (order.quantity || 1)).toFixed(2) }}</p>
              </div>
            </div>
            
            <div class="customer-info">
              <h4>Customer Information</h4>
              <p><strong>Name:</strong> {{ order.buyer ? `${order.buyer.first_name} ${order.buyer.last_name}` : (order.customer_name || 'N/A') }}</p>
              <p><strong>Email:</strong> {{ order.customer_email || order.buyer?.email || 'N/A' }}</p>
              <p><strong>Phone:</strong> {{ order.customer_phone || 'N/A' }}</p>
              <p><strong>Address:</strong> {{ order.shipping_address || order.customer_address || 'N/A' }}</p>
              <div v-if="order.customer_notes || order.notes" class="order-notes">
                <strong>Notes:</strong> {{ order.customer_notes || order.notes }}
              </div>
            </div>
          </div>
          
          <div class="order-actions" v-if="order.status === 'pending'">
            <ActionButton
              variant="success"
              icon="✓"
              text="Confirm Order"
              @click="confirmOrder(order.id)"
              :loading="updatingOrder === order.id"
            />
            <ActionButton
              variant="danger"
              icon="✕"
              text="Cancel Order"
              @click="cancelOrder(order.id)"
              :loading="updatingOrder === order.id"
            />
          </div>
          
        
        </div>
      </div>

      <!-- Pagination -->
      <Pagination
        v-if="totalPages > 1"
        :current-page="currentPage"
        :total-pages="totalPages"
        @page-changed="changePage"
      />

      <!-- Confirmation Modal -->
      <div v-if="showModal" class="modal-overlay" @click="closeModal">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h2>{{ modalTitle }}</h2>
            <button @click="closeModal" class="close-btn">&times;</button>
          </div>
          <div class="modal-body">
            <p>{{ modalMessage }}</p>
          </div>
          <div class="modal-actions">
            <button @click="closeModal" class="cancel-btn">Cancel</button>
            <button @click="confirmAction" class="confirm-btn" :class="modalType">
              {{ modalConfirmText }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </SellerLayout>
</template>

<script>
import SellerLayout from '@/components/seller/SellerLayout.vue'
import ActionButton from '@/components/seller/shared/ActionButton.vue'
import Pagination from '@/components/pagination.vue'

export default {
  name: 'SellerOrders',
  components: {
    SellerLayout,
    ActionButton,
    Pagination
  },
  data() {
    return {
      orders: [],
      currentPage: 1,
      totalPages: 1,
      totalOrders: 0,
      itemsPerPage: 10,
      loading: false,
      selectedStatus: '',
      updatingOrder: null,
      showModal: false,
      modalTitle: '',
      modalMessage: '',
      modalConfirmText: '',
      modalType: '',
      pendingAction: null,
      pendingOrderId: null
    }
  },
  mounted() {
    this.loadOrders()
  },
  methods: {
    async loadOrders() {
      this.loading = true
      try {
        const token = localStorage.getItem('access_token') || localStorage.getItem('token') || localStorage.getItem('jwt_token')
        if (!token) {
          this.$router.push('/login')
          return
        }

        const params = new URLSearchParams({
          page: this.currentPage,
          per_page: this.itemsPerPage
        })
        
        if (this.selectedStatus) {
          params.append('status', this.selectedStatus)
        }

        const response = await fetch(`http://localhost:5000/api/seller/orders?${params}`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })

        if (!response.ok) {
          if (response.status === 401) {
            localStorage.removeItem('access_token')
            localStorage.removeItem('token')
            localStorage.removeItem('jwt_token')
            this.$router.push('/login')
            return
          }
          throw new Error('Failed to fetch orders')
        }

        const data = await response.json()
        this.orders = data.orders || []
        this.totalOrders = data.pagination?.total || 0
        this.totalPages = data.pagination?.pages || Math.ceil(this.totalOrders / this.itemsPerPage)
      } catch (error) {
        console.error('Error loading orders:', error)
        this.orders = []
        this.totalOrders = 0
        this.totalPages = 1
      } finally {
        this.loading = false
      }
    },

    changePage(page) {
      this.currentPage = page
      this.loadOrders()
    },

    confirmOrder(orderId) {
      this.showModal = true
      this.modalTitle = 'Confirm Order'
      this.modalMessage = 'Are you sure you want to confirm this order? The customer will be notified.'
      this.modalConfirmText = 'Confirm Order'
      this.modalType = 'success'
      this.pendingAction = 'confirm'
      this.pendingOrderId = orderId
    },

    cancelOrder(orderId) {
      this.showModal = true
      this.modalTitle = 'Cancel Order'
      this.modalMessage = 'Are you sure you want to cancel this order? This action cannot be undone.'
      this.modalConfirmText = 'Cancel Order'
      this.modalType = 'danger'
      this.pendingAction = 'cancel'
      this.pendingOrderId = orderId
    },

    completeOrder(orderId) {
      this.showModal = true
      this.modalTitle = 'Complete Order'
      this.modalMessage = 'Are you sure you want to mark this order as completed?'
      this.modalConfirmText = 'Complete Order'
      this.modalType = 'primary'
      this.pendingAction = 'complete'
      this.pendingOrderId = orderId
    },

    async confirmAction() {
      if (!this.pendingOrderId || !this.pendingAction) return

      this.updatingOrder = this.pendingOrderId
      try {
        const token = localStorage.getItem('access_token') || localStorage.getItem('token') || localStorage.getItem('jwt_token')
        const response = await fetch(`http://localhost:5000/api/seller/orders/${this.pendingOrderId}/${this.pendingAction}`, {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })

        if (!response.ok) {
          throw new Error(`Failed to ${this.pendingAction} order`)
        }

        // Reload orders to reflect the change
        await this.loadOrders()
        this.closeModal()
      } catch (error) {
        console.error(`Error ${this.pendingAction}ing order:`, error)
        alert(`Failed to ${this.pendingAction} order. Please try again.`)
      } finally {
        this.updatingOrder = null
      }
    },

    closeModal() {
      this.showModal = false
      this.modalTitle = ''
      this.modalMessage = ''
      this.modalConfirmText = ''
      this.modalType = ''
      this.pendingAction = null
      this.pendingOrderId = null
    },

    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    },
    
    goToItems() {
      this.$router.push('/seller/items')
    },

    getItemImage(item) {
      if (!item) return 'http://localhost:5000/uploads/placeholder.svg'
      
      // Handle primary image from API - priority to primary image
      if (item?.primary_image?.url) {
        return item.primary_image.url
      }
      // Handle images array from API  
      if (item?.images && Array.isArray(item.images) && item.images.length > 0) {
        const primaryImage = item.images.find(img => img.isPrimary || img.is_primary)
        if (primaryImage?.url) {
          return primaryImage.url
        }
        // Fallback to first image
        if (item.images[0]?.url) {
          return item.images[0].url
        }
      }
      // Handle direct image_url property
      if (item?.image_url) {
        return item.image_url
      }
      // Handle single image property
      if (item?.image) {
        return item.image
      }
      return 'http://localhost:5000/uploads/placeholder.svg'
    },

    handleImageError(event) {
      event.target.src = 'http://localhost:5000/uploads/placeholder.svg'
    }
  }
}
</script>

<style scoped>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400;1,600;1,700;1,800&family=Inter:wght@300;400;500;600;700&family=Crimson+Text:wght@400;600;700&family=Libre+Baskerville:wght@400;700&display=swap');

.seller-orders {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px;
  font-family: 'Inter', sans-serif;
  background: #ffffff;
}

.page-header {
  margin-bottom: 48px;
  padding: 32px;
  background: #ffffff;
  border-radius: 24px;
  border: 1px solid #e5e7eb;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.page-title {
  margin: 0 0 8px 0;
  font-family: 'Playfair Display', serif;
  font-size: 42px;
  font-weight: 800;
  color: #1f2937;
  letter-spacing: -1px;
  font-style: italic;
}

.page-subtitle {
  margin: 0 0 32px 0;
  color: #8b5a3c;
  font-size: 16px;
  opacity: 0.8;
}

.filter-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 24px;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 12px;
}

.filter-group label {
  font-weight: 600;
  color: #8b5a3c;
  font-size: 14px;
}

.filter-group select {
  padding: 12px 16px;
  border: 1px solid #d4af94;
  border-radius: 12px;
  background: rgba(248, 246, 241, 0.7);
  color: #8b5a3c;
  font-family: 'Inter', sans-serif;
  transition: all 0.3s ease;
}

.filter-group select:focus {
  outline: none;
  border-color: #8b5a3c;
  box-shadow: 0 0 0 3px rgba(139, 90, 60, 0.1);
  background: rgba(248, 246, 241, 1);
}

.orders-count {
  color: #8b5a3c;
  font-weight: 600;
  font-size: 14px;
  padding: 8px 16px;
  background: rgba(139, 90, 60, 0.1);
  border-radius: 20px;
}

.loading-state {
  text-align: center;
  padding: 64px;
  color: #8b5a3c;
}

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid rgba(139, 90, 60, 0.1);
  border-top: 4px solid #8b5a3c;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 24px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.no-orders {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 400px;
}

.no-orders-content {
  text-align: center;
  max-width: 450px;
  padding: 48px;
  background: linear-gradient(135deg, #f8f6f1 0%, #e8ddd4 100%);
  border-radius: 24px;
  border: 1px solid #d4af94;
  box-shadow: 0 8px 25px rgba(139, 90, 60, 0.1);
}

.no-orders-content .icon {
  font-size: 72px;
  margin-bottom: 32px;
  opacity: 0.7;
}

.no-orders-content h2 {
  margin: 0 0 16px 0;
  font-family: 'Playfair Display', serif;
  font-size: 28px;
  font-weight: 600;
  color: #8b5a3c;
}

.no-orders-content p {
  margin: 0 0 32px 0;
  color: #8b5a3c;
  line-height: 1.6;
  opacity: 0.8;
}

.orders-list {
  display: flex;
  flex-direction: column;
  gap: 32px;
  margin-bottom: 32px;
}

.order-card {
  background: linear-gradient(135deg, #f8f6f1 0%, #e8ddd4 100%);
  border: 1px solid #d4af94;
  border-radius: 24px;
  box-shadow: 0 8px 25px rgba(139, 90, 60, 0.1);
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.order-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 35px rgba(139, 90, 60, 0.15);
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 32px;
  background: rgba(139, 90, 60, 0.05);
  border-bottom: 1px solid #d4af94;
}

.order-id {
  font-family: 'Playfair Display', serif;
  font-weight: 600;
  color: #8b5a3c;
  font-size: 20px;
}

.order-date {
  color: #8b5a3c;
  font-size: 14px;
  opacity: 0.8;
}

.order-status {
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-pending {
  background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
  color: #856404;
  border: 1px solid #ffeaa7;
}

.status-confirmed {
  background: linear-gradient(135deg, #d4edda 0%, #a8e6cf 100%);
  color: #155724;
  border: 1px solid #a8e6cf;
}

.status-cancelled {
  background: linear-gradient(135deg, #f8d7da 0%, #ffb3ba 100%);
  color: #721c24;
  border: 1px solid #ffb3ba;
}

.status-completed {
  background: linear-gradient(135deg, #d1ecf1 0%, #a8d8ea 100%);
  color: #0c5460;
  border: 1px solid #a8d8ea;
}

.order-body {
  padding: 32px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 48px;
}

.item-info {
  display: flex;
  gap: 20px;
}

.item-image {
  width: 120px;
  height: 120px;
  object-fit: cover;
  border-radius: 16px;
  border: 2px solid #d4af94;
  box-shadow: 0 4px 15px rgba(139, 90, 60, 0.1);
}

.item-details h3 {
  margin: 0 0 8px 0;
  font-family: 'Playfair Display', serif;
  font-size: 20px;
  font-weight: 600;
  color: #8b5a3c;
}

.item-category {
  margin: 0 0 8px 0;
  color: #8b5a3c;
  font-size: 14px;
  opacity: 0.7;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.item-price {
  margin: 0;
  font-size: 24px;
  font-weight: 700;
  color: #8b5a3c;
}

.customer-info h4 {
  margin: 0 0 16px 0;
  font-family: 'Playfair Display', serif;
  font-size: 18px;
  font-weight: 600;
  color: #8b5a3c;
}

.customer-info p {
  margin: 0 0 8px 0;
  color: #8b5a3c;
  font-size: 14px;
  opacity: 0.9;
}

.order-notes {
  margin-top: 20px;
  padding: 16px;
  background: rgba(139, 90, 60, 0.05);
  border-radius: 12px;
  border-left: 4px solid #8b5a3c;
}

.order-actions {
  padding: 24px 32px;
  background: rgba(139, 90, 60, 0.03);
  border-top: 1px solid #d4af94;
  display: flex;
  gap: 16px;
  justify-content: flex-end;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(139, 90, 60, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}

.modal-content {
  background: linear-gradient(135deg, #f8f6f1 0%, #e8ddd4 100%);
  border-radius: 24px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 20px 60px rgba(139, 90, 60, 0.3);
  border: 1px solid #d4af94;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 32px;
  border-bottom: 1px solid #d4af94;
}

.modal-header h2 {
  margin: 0;
  font-family: 'Playfair Display', serif;
  color: #8b5a3c;
  font-size: 24px;
  font-weight: 600;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #8b5a3c;
  opacity: 0.7;
  transition: opacity 0.3s ease;
}

.close-btn:hover {
  opacity: 1;
}

.modal-body {
  padding: 32px;
}

.modal-body p {
  margin: 0;
  color: #8b5a3c;
  line-height: 1.6;
  opacity: 0.9;
}

.modal-actions {
  display: flex;
  gap: 16px;
  padding: 24px 32px;
  border-top: 1px solid #d4af94;
  justify-content: flex-end;
}

.cancel-btn,
.confirm-btn {
  padding: 12px 24px;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  font-weight: 600;
  font-family: 'Inter', sans-serif;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.cancel-btn {
  background: linear-gradient(135deg, #6c757d 0%, #868e96 100%);
  color: white;
}

.cancel-btn:hover {
  background: linear-gradient(135deg, #545b62 0%, #6c757d 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.confirm-btn {
  color: white;
}

.confirm-btn.success {
  background: linear-gradient(135deg, #28a745 0%, #34ce57 100%);
}

.confirm-btn.success:hover {
  background: linear-gradient(135deg, #218838 0%, #28a745 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(40, 167, 69, 0.3);
}

.confirm-btn.danger {
  background: linear-gradient(135deg, #dc3545 0%, #e74c3c 100%);
}

.confirm-btn.danger:hover {
  background: linear-gradient(135deg, #c82333 0%, #dc3545 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(220, 53, 69, 0.3);
}

.confirm-btn.primary {
  background: linear-gradient(135deg, #8b5a3c 0%, #a06749 100%);
}

.confirm-btn.primary:hover {
  background: linear-gradient(135deg, #744a32 0%, #8b5a3c 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(139, 90, 60, 0.3);
}

/* Responsive */
@media (max-width: 768px) {
  .seller-orders {
    padding: 24px;
  }
  
  .page-header {
    padding: 24px;
  }
  
  .filter-bar {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .order-body {
    grid-template-columns: 1fr;
    gap: 32px;
    padding: 24px;
  }
  
  .order-header {
    padding: 20px 24px;
  }
  
  .order-actions {
    flex-direction: column;
    padding: 20px 24px;
  }
  
  .item-info {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  
  .modal-actions {
    flex-direction: column;
  }
  
  .page-title {
    font-size: 28px;
  }
}

@media (max-width: 480px) {
  .order-header {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }
  
  .item-image {
    width: 100px;
    height: 100px;
  }
  
  .modal-header,
  .modal-body,
  .modal-actions {
    padding: 20px 24px;
  }
}
</style>
