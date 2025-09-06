<template>
  <UserLayout>
    <div class="order-details-container">
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
            <span class="order-date">{{ formatDate(order.orderDate) }}</span>
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
            <div v-for="item in order.items" :key="item.id" class="order-item">
              <img :src="item.image" :alt="item.title" class="item-image" />
              
              <div class="item-details">
                <h3 class="item-title">{{ item.title }}</h3>
                <p class="item-seller">Sold by {{ item.seller }}</p>
                <div class="item-specs">
                  <span v-if="item.condition">Condition: {{ item.condition }}</span>
                  <span v-if="item.category">Category: {{ item.category }}</span>
                </div>
              </div>

              <div class="item-pricing">
                <div class="quantity">Qty: {{ item.quantity }}</div>
                <div class="price">${{ (item.price * item.quantity).toFixed(2) }}</div>
              </div>

              <div class="item-actions">
                <button @click="viewItem(item)" class="view-item-btn">
                  View Item
                </button>
                <button v-if="order.status === 'delivered'" @click="leaveReview(item)" class="review-btn">
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
              <span>Subtotal</span>
              <span>${{ order.subtotal.toFixed(2) }}</span>
            </div>
            <div class="summary-row">
              <span>Shipping</span>
              <span>${{ order.shipping.toFixed(2) }}</span>
            </div>
            <div class="summary-row">
              <span>Tax</span>
              <span>${{ order.tax.toFixed(2) }}</span>
            </div>
            <div v-if="order.discount > 0" class="summary-row discount">
              <span>Discount</span>
              <span>-${{ order.discount.toFixed(2) }}</span>
            </div>
            <div class="summary-row total">
              <span>Total</span>
              <span>${{ order.total.toFixed(2) }}</span>
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
                <p>{{ order.shippingAddress.name }}</p>
                <p>{{ order.shippingAddress.street }}</p>
                <p>{{ order.shippingAddress.city }}, {{ order.shippingAddress.state }} {{ order.shippingAddress.zip }}</p>
                <p>{{ order.shippingAddress.country }}</p>
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
                <span class="method-type">{{ order.paymentMethod.type }}</span>
                <span class="method-details">**** **** **** {{ order.paymentMethod.last4 }}</span>
              </div>
              <span class="payment-status">Paid</span>
            </div>
            
            <div class="payment-date">
              Payment completed on {{ formatDate(order.paymentDate) }}
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
      order: {
        id: '20240001',
        orderDate: '2024-03-15',
        status: 'delivered',
        paymentDate: '2024-03-15',
        subtotal: 315.00,
        shipping: 25.00,
        tax: 30.40,
        discount: 0,
        total: 370.40,
        paymentMethod: {
          type: 'Credit Card',
          last4: '4242'
        },
        shippingAddress: {
          name: 'John Doe',
          street: '123 Main Street, Apt 4B',
          city: 'New York',
          state: 'NY',
          zip: '10001',
          country: 'United States'
        },
        items: [
          {
            id: 1,
            title: 'Vintage Pocket Watch',
            seller: 'Vintage Items',
            image: '/api/placeholder/80/80',
            price: 150.00,
            quantity: 1,
            condition: 'Excellent',
            category: 'Collectibles'
          },
          {
            id: 2,
            title: 'Antique Silver Spoons Set',
            seller: 'Vintage Items', 
            image: '/api/placeholder/80/80',
            price: 165.00,
            quantity: 1,
            condition: 'Very Good',
            category: 'Home & Decor'
          }
        ]
      },
      deliverySteps: [
        {
          title: 'Order Placed',
          completed: true,
          date: '2024-03-15'
        },
        {
          title: 'Order Confirmed',
          completed: true,
          date: '2024-03-15'
        },
        {
          title: 'Shipped',
          completed: true,
          date: '2024-03-16'
        },
        {
          title: 'Out for Delivery',
          completed: true,
          date: '2024-03-18'
        },
        {
          title: 'Delivered',
          completed: true,
          current: true,
          date: '2024-03-18'
        }
      ]
    }
  },
  created() {
    this.loadOrderDetails()
  },
  methods: {
    loadOrderDetails() {
      const orderId = this.$route.params.id
      // Load order details based on orderId
      console.log('Loading order:', orderId)
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
    }
  }
}
</script>

<style scoped>
.order-details-container {
  max-width: 1000px;
  margin: 0 auto;
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
