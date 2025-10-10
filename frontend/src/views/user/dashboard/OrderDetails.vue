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

/* Back Button */
.back-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: none;
  border: none;
  color: #6b7280;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 500;
  padding: 0.5rem 0;
  margin-bottom: 1.5rem;
  transition: color 0.2s ease;
}

.back-button:hover {
  color: #111827;
}

.back-button svg {
  stroke-width: 2;
}

/* Order Header */
.order-header {
  margin-bottom: 2rem;
}

.header-left {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.order-title {
  font-size: 1.875rem;
  font-weight: 700;
  color: #111827;
  margin: 0;
  letter-spacing: -0.025em;
}

.order-meta {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.875rem;
}

.order-date {
  color: #6b7280;
}

.meta-separator {
  color: #d1d5db;
}

.order-status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.order-status-badge.pending {
  background: #fef3c7;
  color: #92400e;
}

.order-status-badge.processing {
  background: #dbeafe;
  color: #1e40af;
}

.order-status-badge.shipped {
  background: #e0e7ff;
  color: #4338ca;
}

.order-status-badge.delivered {
  background: #d1fae5;
  color: #065f46;
}

.order-status-badge.cancelled {
  background: #fee2e2;
  color: #991b1b;
}

/* Main Grid Layout */
.order-grid {
  display: grid;
  grid-template-columns: 1fr 400px;
  gap: 2rem;
  align-items: start;
}

/* Card Styles */
.card {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 1.5rem;
}

.card-title {
  font-size: 0.875rem;
  font-weight: 600;
  color: #111827;
  margin: 0 0 1.5rem 0;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* Left Column */
.left-column {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Order Item Card */
.order-item-card {
  padding: 1.5rem;
}

.item-wrapper {
  display: flex;
  gap: 1.5rem;
}

.item-image-container {
  flex-shrink: 0;
}

.item-image {
  width: 120px;
  height: 120px;
  object-fit: cover;
  border-radius: 6px;
  border: 1px solid #e5e7eb;
}

.item-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.item-name {
  font-size: 1.125rem;
  font-weight: 600;
  color: #111827;
  margin: 0;
  line-height: 1.4;
}

.item-seller {
  font-size: 0.875rem;
  color: #6b7280;
  margin: 0;
}

.item-meta {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin-top: 0.25rem;
}

.meta-badge {
  padding: 0.25rem 0.625rem;
  background: #f3f4f6;
  border-radius: 4px;
  font-size: 0.75rem;
  color: #6b7280;
  text-transform: capitalize;
}

.item-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
  padding-top: 0.75rem;
  border-top: 1px solid #e5e7eb;
}

.item-quantity {
  font-size: 0.875rem;
  color: #6b7280;
}

.item-price {
  font-size: 1.25rem;
  font-weight: 700;
  color: #111827;
}

/* Delivery Card */
.delivery-card {
  padding: 1.5rem;
}

.delivery-section {
  margin-bottom: 2rem;
}

.delivery-section:last-child {
  margin-bottom: 0;
}

.subsection-title {
  font-size: 0.75rem;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin: 0 0 0.75rem 0;
}

.delivery-address-text {
  font-size: 0.875rem;
  color: #111827;
  line-height: 1.6;
  margin: 0;
}

/* Timeline */
.timeline {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.timeline-item {
  display: flex;
  gap: 1rem;
  position: relative;
}

.timeline-marker {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
}

.marker-dot {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #f3f4f6;
  border: 2px solid #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1;
  flex-shrink: 0;
}

.timeline-item.completed .marker-dot {
  background: #111827;
  border-color: #111827;
}

.timeline-item.completed .marker-dot svg {
  stroke: #ffffff;
}

.timeline-item.active .marker-dot {
  background: #ffffff;
  border-color: #111827;
  border-width: 3px;
}

.timeline-line {
  width: 2px;
  height: 24px;
  background: #e5e7eb;
  margin-top: 4px;
}

.timeline-item.completed .timeline-line {
  background: #111827;
}

.timeline-content {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  padding-top: 0.25rem;
}

.timeline-title {
  font-size: 0.875rem;
  font-weight: 500;
  color: #111827;
}

.timeline-item:not(.completed) .timeline-title {
  color: #9ca3af;
}

.timeline-date {
  font-size: 0.75rem;
  color: #6b7280;
}

/* Right Column */
.right-column {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Summary Card */
.summary-card {
  padding: 1.5rem;
}

.summary-rows {
  display: flex;
  flex-direction: column;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 0;
}

.row-label {
  font-size: 0.875rem;
  color: #6b7280;
}

.row-value {
  font-size: 0.875rem;
  font-weight: 500;
  color: #111827;
}

.summary-divider {
  height: 1px;
  background: #e5e7eb;
  margin: 0.5rem 0;
}

.summary-total {
  padding-top: 1rem;
}

.summary-total .row-label {
  font-size: 1rem;
  font-weight: 600;
  color: #111827;
}

.summary-total .row-value {
  font-size: 1.25rem;
  font-weight: 700;
  color: #111827;
}

/* Payment Card */
.payment-card {
  padding: 1.5rem;
}

.payment-method {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.payment-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 0;
  border-bottom: 1px solid #f3f4f6;
}

.payment-row:last-child {
  border-bottom: none;
}

.payment-label {
  font-size: 0.875rem;
  color: #6b7280;
}

.payment-value {
  font-size: 0.875rem;
  font-weight: 500;
  color: #111827;
  text-transform: capitalize;
}

.payment-status-badge {
  padding: 0.25rem 0.625rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.payment-status-badge.paid {
  background: #d1fae5;
  color: #065f46;
}

.payment-status-badge.pending {
  background: #fef3c7;
  color: #92400e;
}

.payment-notes {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e5e7eb;
}

.notes-label {
  display: block;
  font-size: 0.75rem;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.5rem;
}

.notes-text {
  font-size: 0.875rem;
  color: #111827;
  line-height: 1.6;
  margin: 0;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .order-grid {
    grid-template-columns: 1fr;
  }
  
  .right-column {
    order: -1;
  }
}

@media (max-width: 768px) {
  .order-details-container {
    padding: 1rem 0.5rem;
  }
  
  .order-title {
    font-size: 1.5rem;
  }
  
  .card {
    padding: 1rem;
  }
  
  .item-wrapper {
    flex-direction: column;
  }
  
  .item-image {
    width: 100%;
    height: 200px;
  }
  
  .item-bottom {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .timeline {
    margin-left: 0;
  }
}

@media (max-width: 480px) {
  .order-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .meta-separator {
    display: none;
  }
}
</style>
