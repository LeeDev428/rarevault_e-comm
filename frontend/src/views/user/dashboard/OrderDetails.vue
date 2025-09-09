<template>
  <UserLayout>
    <div class="order-details-container">
      <!-- Loading State -->
      <div v-if="loading" class="loading-state">
        <div class="loading-spinner"></div>
        <p>Loading order details...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="error-state">
        <div class="error-icon">⚠️</div>
        <h2>{{ error }}</h2>
        <button @click="goBack" class="action-btn primary">Back to Orders</button>
      </div>

      <!-- Order Content -->
      <div v-else-if="order" class="order-content-wrapper">
        <!-- Order Header -->
        <div class="order-header">
          <div class="header-top">
            <button @click="goBack" class="back-btn">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <polyline points="15,18 9,12 15,6"/>
              </svg>
              Back to Orders
            </button>
            
            <div class="order-actions">
              <button v-if="order.status === 'delivered'" @click="downloadInvoice" class="action-btn secondary">
                Download Invoice
              </button>
              <button v-if="order.status === 'pending' || order.status === 'processing'" @click="trackOrder" class="action-btn primary">
                Track Order
              </button>
            </div>
          </div>
          
          <div class="order-info">
            <h1 class="order-title">Order #{{ order.id }}</h1>
            <div class="order-meta">
              <span class="order-date">{{ formatDate(order.created_at || order.orderDate) }}</span>
              <span :class="['order-status', order.status]">{{ getStatusText(order.status) }}</span>
            </div>
          </div>
        </div>

        <!-- Order Content -->
        <div class="order-content">
          <!-- Order Items -->
          <div class="order-section">
            <h2 class="section-title">Order Items</h2>
            <div class="items-list">
              <div class="order-item">
                <img :src="getItemImage(order.item)" :alt="order.item.title" class="item-image" />
                
                <div class="item-details">
                  <h3 class="item-title">{{ order.item.title }}</h3>
                  <p class="item-seller">Sold by {{ getSellerName(order.item) }}</p>
                  <div class="item-specs">
                    <span v-if="order.item.condition">Condition: {{ order.item.condition }}</span>
                    <span v-if="order.item.category">Category: {{ order.item.category }}</span>
                  </div>
                </div>

                <div class="item-pricing">
                  <div class="quantity">Qty: {{ order.quantity || 1 }}</div>
                  <div class="price">₱{{ (order.total_amount || order.item.price).toFixed(2) }}</div>
                </div>

                <div class="item-actions">
                  <button @click="viewItem(order.item)" class="view-item-btn">
                    View Item
                  </button>
                  <button v-if="order.status === 'delivered'" @click="leaveReview(order.item)" class="review-btn">
                    Write Review
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Order Summary -->
          <div class="order-section">
            <h2 class="section-title">Order Summary</h2>
            <div class="summary-card">
              <div class="summary-row">
                <span>Item Price</span>
                <span>₱{{ (order.item?.price || 0).toFixed(2) }}</span>
              </div>
              <div class="summary-row">
                <span>Quantity</span>
                <span>{{ order.quantity || 1 }}</span>
              </div>
              <div class="summary-row">
                <span>Shipping</span>
                <span>₱{{ (order.shipping_cost || 0).toFixed(2) }}</span>
              </div>
              <div class="summary-row total">
                <span>Total</span>
                <span>₱{{ (order.total_amount || 0).toFixed(2) }}</span>
              </div>
            </div>
          </div>

          <!-- Delivery Information -->
          <div class="order-section">
            <h2 class="section-title">Delivery Information</h2>
            <div class="delivery-card">
              <div class="delivery-address">
                <h3>Shipping Address</h3>
                <div class="address">
                  <p>{{ order.shipping_address || 'Address not provided' }}</p>
                </div>
              </div>

              <div class="delivery-status">
                <h3>Delivery Status</h3>
                <div class="status-timeline">
                  <div 
                    v-for="(step, index) in deliverySteps" 
                    :key="index"
                    :class="['timeline-step', { 
                      completed: step.completed, 
                      current: step.current,
                      pending: !step.completed && !step.current
                    }]"
                  >
                    <div class="step-icon">
                      <svg v-if="step.completed" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <polyline points="20,6 9,17 4,12"/>
                      </svg>
                      <span v-else class="step-number">{{ index + 1 }}</span>
                    </div>
                    <div class="step-details">
                      <span class="step-title">{{ step.title }}</span>
                      <span v-if="step.date" class="step-date">{{ formatDate(step.date) }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Payment Information -->
          <div class="order-section">
            <h2 class="section-title">Payment Information</h2>
            <div class="payment-card">
              <div class="payment-method">
                <div class="method-info">
                  <span class="method-type">{{ order.payment_method || 'Cash on Delivery' }}</span>
                  <span class="method-details">{{ order.customer_notes || 'No additional details' }}</span>
                </div>
                <span class="payment-status">{{ order.status === 'delivered' ? 'Paid' : 'Pending' }}</span>
              </div>
              
              <div class="payment-date">
                Payment {{ order.status === 'delivered' ? 'completed' : 'pending' }} on {{ formatDate(order.created_at) }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </UserLayout>
</template>

<script>
import UserLayout from '@/components/user/UserLayout.vue'

export default {
  name: 'UserOrderDetails',
  components: {
    UserLayout
  },
  data() {
    return {
      order: null,
      loading: true,
      error: null,
      deliverySteps: []
    }
  },
  created() {
    this.loadOrderDetails()
  },
  methods: {
    async loadOrderDetails() {
      try {
        const orderId = this.$route.params.id
        if (!orderId) {
          this.error = 'Order ID not found'
          this.loading = false
          return
        }

        const token = localStorage.getItem('access_token') || localStorage.getItem('token')
        if (!token) {
          this.$router.push('/login')
          return
        }

        const response = await fetch(`http://localhost:5000/api/user/orders/${orderId}`, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })

        if (!response.ok) {
          if (response.status === 401) {
            this.$router.push('/login')
            return
          } else if (response.status === 404) {
            this.error = 'Order not found'
          } else {
            this.error = 'Failed to load order details'
          }
          this.loading = false
          return
        }

        const data = await response.json()
        this.order = data.order || data
        this.generateDeliverySteps()
        this.loading = false
      } catch (error) {
        console.error('Error loading order details:', error)
        this.error = 'Failed to load order details'
        this.loading = false
      }
    },

    generateDeliverySteps() {
      if (!this.order) return

      const steps = [
        {
          title: 'Order Placed',
          completed: true,
          date: this.order.created_at
        },
        {
          title: 'Order Confirmed',
          completed: ['confirmed', 'shipped', 'delivered'].includes(this.order.status),
          date: this.order.confirmed_at
        },
        {
          title: 'Shipped',
          completed: ['shipped', 'delivered'].includes(this.order.status),
          date: this.order.shipped_at
        },
        {
          title: 'Delivered',
          completed: this.order.status === 'delivered',
          current: this.order.status === 'delivered',
          date: this.order.delivered_at
        }
      ]

      this.deliverySteps = steps
    },
    
    goBack() {
      this.$router.push('/user/orders')
    },
    
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'long', 
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
    
    downloadInvoice() {
      console.log('Downloading invoice for order:', this.order.id)
    },
    
    trackOrder() {
      console.log('Tracking order:', this.order.id)
    },
    
    viewItem(item) {
      console.log('View item:', item.title)
    },
    
    leaveReview(item) {
      console.log('Leave review for:', item.title)
    },

    getItemImage(item) {
      // Handle primary image from API
      if (item?.primary_image?.url) {
        return `http://localhost:5000${item.primary_image.url}`;
      }
      // Handle images array from API  
      if (item?.images && Array.isArray(item.images) && item.images.length > 0) {
        const primaryImage = item.images.find(img => img.isPrimary);
        if (primaryImage?.url) {
          return `http://localhost:5000${primaryImage.url}`;
        }
        if (item.images[0]?.url) {
          return `http://localhost:5000${item.images[0].url}`;
        }
      }
      // Handle image_url property
      if (item?.image_url) {
        return `http://localhost:5000${item.image_url}`;
      }
      // Handle single image property
      if (item?.image) {
        return `http://localhost:5000${item.image}`;
      }
      return 'http://localhost:5000/uploads/placeholder.svg';
    },

    getSellerName(item) {
      return item?.seller?.username || item?.seller_name || 'Unknown Seller';
    }
  }
}
</script>

<style scoped>
.order-details-container {
  max-width: 1000px;
  margin: 0 auto;
}

/* Loading and Error States */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f4f6;
  border-top: 4px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-state p {
  color: #6b7280;
  font-size: 16px;
  margin: 0;
}

.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.error-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.error-state h2 {
  color: #dc2626;
  font-size: 20px;
  margin: 0 0 24px 0;
}

.error-state .action-btn {
  margin-top: 16px;
}

/* Order Header */
.order-header {
  background: white;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.header-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  background: none;
  border: none;
  color: #6b7280;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: color 0.2s ease;
}

.back-btn:hover {
  color: #374151;
}

.order-actions {
  display: flex;
  gap: 12px;
}

.order-info {
  border-top: 1px solid #e5e7eb;
  padding-top: 20px;
}

.order-title {
  font-size: 28px;
  font-weight: 700;
  color: #111827;
  margin: 0 0 8px 0;
}

.order-meta {
  display: flex;
  align-items: center;
  gap: 16px;
}

.order-date {
  color: #6b7280;
  font-size: 14px;
}

.order-status {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.order-status.pending {
  background: #fef3c7;
  color: #92400e;
}

.order-status.processing {
  background: #dbeafe;
  color: #1d4ed8;
}

.order-status.shipped {
  background: #e0e7ff;
  color: #3730a3;
}

.order-status.delivered {
  background: #d1fae5;
  color: #065f46;
}

/* Order Content */
.order-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.order-section {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  color: #111827;
  margin: 0 0 20px 0;
}

/* Order Items */
.items-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.order-item {
  display: grid;
  grid-template-columns: 80px 1fr auto auto;
  gap: 16px;
  align-items: center;
  padding: 16px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
}

.item-image {
  width: 80px;
  height: 80px;
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
  margin: 0 0 8px 0;
}

.item-specs {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.item-specs span {
  font-size: 12px;
  color: #9ca3af;
}

.item-pricing {
  text-align: right;
}

.quantity {
  font-size: 14px;
  color: #6b7280;
  margin-bottom: 4px;
}

.price {
  font-size: 18px;
  font-weight: 700;
  color: #111827;
}

.item-actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.view-item-btn,
.review-btn {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.view-item-btn {
  background: #f3f4f6;
  color: #374151;
}

.view-item-btn:hover {
  background: #e5e7eb;
}

.review-btn {
  background: #3b82f6;
  color: white;
}

.review-btn:hover {
  background: #2563eb;
}

/* Order Summary */
.summary-card {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 20px;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #f3f4f6;
}

.summary-row:last-child {
  border-bottom: none;
}

.summary-row.discount span:last-child {
  color: #059669;
}

.summary-row.total {
  font-size: 18px;
  font-weight: 700;
  border-top: 1px solid #e5e7eb;
  margin-top: 8px;
  padding-top: 16px;
}

/* Delivery Information */
.delivery-card {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 32px;
}

.delivery-address h3,
.delivery-status h3 {
  font-size: 16px;
  font-weight: 600;
  color: #111827;
  margin: 0 0 12px 0;
}

.address p {
  margin: 2px 0;
  color: #374151;
  line-height: 1.4;
}

/* Status Timeline */
.status-timeline {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.timeline-step {
  display: flex;
  align-items: center;
  gap: 12px;
}

.step-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.timeline-step.completed .step-icon {
  background: #059669;
  color: white;
}

.timeline-step.current .step-icon {
  background: #3b82f6;
  color: white;
}

.timeline-step.pending .step-icon {
  background: #f3f4f6;
  color: #9ca3af;
}

.step-number {
  font-size: 12px;
  font-weight: 600;
}

.step-details {
  display: flex;
  flex-direction: column;
}

.step-title {
  font-size: 14px;
  font-weight: 500;
  color: #111827;
}

.step-date {
  font-size: 12px;
  color: #6b7280;
}

.timeline-step.pending .step-title {
  color: #9ca3af;
}

/* Payment Information */
.payment-card {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 20px;
}

.payment-method {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.method-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.method-type {
  font-weight: 600;
  color: #111827;
}

.method-details {
  font-size: 14px;
  color: #6b7280;
}

.payment-status {
  background: #d1fae5;
  color: #065f46;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
}

.payment-date {
  font-size: 14px;
  color: #6b7280;
}

/* Action Buttons */
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

/* Responsive */
@media (max-width: 768px) {
  .header-top {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
  
  .order-item {
    grid-template-columns: 60px 1fr;
    gap: 12px;
  }
  
  .item-pricing,
  .item-actions {
    grid-column: 1 / -1;
    margin-top: 12px;
  }
  
  .item-actions {
    flex-direction: row;
    justify-content: center;
  }
  
  .delivery-card {
    grid-template-columns: 1fr;
    gap: 24px;
  }
  
  .payment-method {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
}
</style>
