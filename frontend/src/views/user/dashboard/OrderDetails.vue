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
        <button @click="goBack" class="back-btn-primary">Back to Orders</button>
      </div>

      <!-- Order Content -->
      <div v-else-if="order" class="order-content-wrapper">
        <!-- Back Button -->
        <button @click="goBack" class="back-button">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="15 18 9 12 15 6"/>
          </svg>
          <span>Back to Orders</span>
        </button>

        <!-- Order Header -->
        <div class="order-header">
          <div class="header-left">
            <h1 class="order-title">Order #{{ order.id }}</h1>
            <div class="order-meta">
              <span class="order-date">{{ formatDate(order.created_at || order.orderDate) }}</span>
              <span class="meta-separator">•</span>
              <span :class="['order-status-badge', order.status]">{{ getStatusText(order.status) }}</span>
            </div>
          </div>
        </div>

        <!-- Main Grid Layout -->
        <div class="order-grid">
          <!-- Left Column -->
          <div class="left-column">
            <!-- Order Item Card -->
            <div class="card order-item-card">
              <h2 class="card-title">Order Items</h2>
              
              <div class="item-wrapper">
                <div class="item-image-container">
                  <img 
                    :src="getItemImage(order.item)" 
                    :alt="order.item.title" 
                    class="item-image"
                    @error="handleImageError"
                  />
                </div>
                
                <div class="item-info">
                  <h3 class="item-name">{{ order.item.title }}</h3>
                  <p class="item-seller">Sold by {{ getSellerName(order.item) }}</p>
                  
                  <div class="item-meta">
                    <span v-if="order.item.condition" class="meta-badge">{{ order.item.condition }}</span>
                    <span v-if="order.item.category" class="meta-badge">{{ order.item.category }}</span>
                  </div>
                  
                  <div class="item-bottom">
                    <span class="item-quantity">Qty {{ order.quantity || 1 }}</span>
                    <span class="item-price">₱{{ (order.total_amount || order.item.price).toFixed(2) }}</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Delivery Information Card -->
            <div class="card delivery-card">
              <h2 class="card-title">Delivery Information</h2>
              
              <div class="delivery-section">
                <h3 class="subsection-title">SHIPPING ADDRESS</h3>
                <p class="delivery-address-text">{{ order.shipping_address || 'Address not provided' }}</p>
              </div>

              <div class="delivery-section">
                <h3 class="subsection-title">DELIVERY STATUS</h3>
                <div class="timeline">
                  <div 
                    v-for="(step, index) in deliverySteps" 
                    :key="index"
                    :class="['timeline-item', { 
                      completed: step.completed, 
                      active: step.current
                    }]"
                  >
                    <div class="timeline-marker">
                      <div class="marker-dot">
                        <svg v-if="step.completed" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
                          <polyline points="20 6 9 17 4 12"/>
                        </svg>
                      </div>
                      <div v-if="index < deliverySteps.length - 1" class="timeline-line"></div>
                    </div>
                    <div class="timeline-content">
                      <span class="timeline-title">{{ step.title }}</span>
                      <span v-if="step.date" class="timeline-date">{{ formatDate(step.date) }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Right Column -->
          <div class="right-column">
            <!-- Order Summary Card -->
            <div class="card summary-card">
              <h2 class="card-title">Order Summary</h2>
              
              <div class="summary-rows">
                <div class="summary-row">
                  <span class="row-label">Item Price</span>
                  <span class="row-value">₱{{ (order.item?.price || 0).toFixed(2) }}</span>
                </div>
                <div class="summary-row">
                  <span class="row-label">Quantity</span>
                  <span class="row-value">{{ order.quantity || 1 }}</span>
                </div>
                <div class="summary-row">
                  <span class="row-label">Shipping</span>
                  <span class="row-value">₱{{ (order.shipping_cost || 0).toFixed(2) }}</span>
                </div>
                
                <div class="summary-divider"></div>
                
                <div class="summary-row summary-total">
                  <span class="row-label">Total</span>
                  <span class="row-value">₱{{ (order.total_amount || 0).toFixed(2) }}</span>
                </div>
              </div>
            </div>

            <!-- Payment Information Card -->
            <div class="card payment-card">
              <h2 class="card-title">Payment Information</h2>
              
              <div class="payment-method">
                <div class="payment-row">
                  <span class="payment-label">Method</span>
                  <span class="payment-value">{{ order.payment_method || 'cash_on_delivery' }}</span>
                </div>
                
                <div class="payment-row">
                  <span class="payment-label">Status</span>
                  <span :class="['payment-status-badge', order.status === 'delivered' ? 'paid' : 'pending']">
                    {{ order.status === 'delivered' ? 'Paid' : 'Pending' }}
                  </span>
                </div>
                
                <div v-if="order.customer_notes" class="payment-notes">
                  <span class="notes-label">Notes</span>
                  <p class="notes-text">{{ order.customer_notes }}</p>
                </div>
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
        
        // Comprehensive debugging
        console.log('=== OrderDetails Debug Information ===')
        console.log('1. Raw response data:', data)
        console.log('2. Final order object:', this.order)
        console.log('3. Order item:', this.order?.item)
        console.log('4. Item images array:', this.order?.item?.images)
        console.log('5. Item primary_image:', this.order?.item?.primary_image)
        
        if (this.order?.item?.images) {
          this.order.item.images.forEach((img, index) => {
            console.log(`6. Image ${index}:`, img)
            console.log(`   - URL: ${img.url}`)
            console.log(`   - is_primary: ${img.is_primary}`)
            console.log(`   - isPrimary: ${img.isPrimary}`)
          })
        }
        
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
      console.log('=== getItemImage Debug ===')
      console.log('Item received:', item);
      
      // Handle images array from API (most common case)
      if (item?.images && Array.isArray(item.images) && item.images.length > 0) {
        console.log('Found images array with length:', item.images.length);
        
        // Find primary image first, then fallback to first image
        const primaryImage = item.images.find(img => img.is_primary || img.isPrimary) || item.images[0];
        console.log('Selected primary/first image:', primaryImage);
        
        if (primaryImage?.url) {
          let imageUrl = primaryImage.url;
          
          // Fix duplicate path issue (e.g., /uploads/items/13/13/image_0.png)
          if (imageUrl.includes('/uploads/items/')) {
            const regex = /\/uploads\/items\/(\d+)\/\1\//;
            const match = imageUrl.match(regex);
            if (match) {
              const itemId = match[1];
              imageUrl = imageUrl.replace(`/uploads/items/${itemId}/${itemId}/`, `/uploads/items/${itemId}/`);
              console.log('✓ Fixed duplicate path, corrected URL:', imageUrl);
            }
          }
          
          console.log('✓ Using images array url:', imageUrl);
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
            console.log('✓ Fixed duplicate path in primary_image, corrected URL:', imageUrl);
          }
        }
        
        console.log('✓ Using primary_image.url:', imageUrl);
        return imageUrl;
      }
      
      // Handle primary_image as string
      if (item?.primary_image && typeof item.primary_image === 'string') {
        console.log('✓ Using primary_image string:', item.primary_image);
        return item.primary_image.startsWith('http') ? item.primary_image : `http://localhost:5000${item.primary_image}`;
      }
      
      // Handle legacy image_url property
      if (item?.image_url) {
        console.log('✓ Using image_url:', item.image_url);
        return item.image_url.startsWith('http') ? item.image_url : `http://localhost:5000${item.image_url}`;
      }
      
      // Handle single image property
      if (item?.image) {
        console.log('✓ Using image:', item.image);
        return item.image.startsWith('http') ? item.image : `http://localhost:5000${item.image}`;
      }
      
      // Try to construct image URL from item ID if available
      if (item?.id) {
        const constructedUrl = `http://localhost:5000/uploads/items/${item.id}/image_0.jpeg`;
        console.log('⚠ Attempting constructed URL:', constructedUrl);
        return constructedUrl;
      }
      
      console.log('❌ No image source found, using placeholder');
      return 'http://localhost:5000/uploads/placeholder.svg';
    },

    handleImageError(event) {
      console.log('❌ OrderDetails.vue - Image failed to load');
      console.log('Failed URL:', event.target.src);
      event.target.src = 'http://localhost:5000/uploads/placeholder.svg';
      
      // Try to diagnose the issue
      setTimeout(() => {
        console.log('=== Image Error Diagnosis ===');
        console.log('Order data at error time:', this.order);
        console.log('Item data at error time:', this.order?.item);
      }, 100);
    },

    getSellerName(item) {
      return item?.seller?.username || item?.seller_name || 'Unknown Seller';
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* {
  font-family: 'Inter', sans-serif;
}

.order-details-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

/* Loading State */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  background: #ffffff;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 3px solid #f3f4f6;
  border-top: 3px solid #111827;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-state p {
  color: #6b7280;
  font-size: 0.875rem;
  margin: 0;
}

/* Error State */
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  background: #ffffff;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
  text-align: center;
}

.error-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.error-state h2 {
  color: #111827;
  font-size: 1.125rem;
  font-weight: 600;
  margin: 0 0 1.5rem 0;
}

.back-btn-primary {
  padding: 0.75rem 1.5rem;
  background: #111827;
  color: #ffffff;
  border: none;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.back-btn-primary:hover {
  background: #000000;
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
