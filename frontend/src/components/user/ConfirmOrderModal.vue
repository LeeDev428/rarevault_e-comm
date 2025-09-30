<template>
  <div v-if="show" class="modal-overlay" @click="closeModal">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h2 class="modal-title">Confirm Order</h2>
        <button @click="closeModal" class="close-btn">✕</button>
      </div>
      
      <div class="order-confirmation">
        <!-- Item Summary -->
        <div class="item-summary">
          <div class="image-container">
            <img 
              :src="getItemImage(item)" 
              :alt="item?.title || 'Item'" 
              class="summary-image"
              @error="handleImageError"
              @load="imageLoaded = true"
            >
            <div v-if="!imageLoaded" class="image-loading">
              <div class="loading-spinner"></div>
            </div>
          </div>
          <div class="summary-details">
            <h3>{{ item?.title || item?.name }}</h3>
            <p class="summary-category">{{ item?.category }}</p>
            <p class="summary-price">₱{{ formatPrice(item?.price) }}</p>
            <p class="summary-condition">Condition: {{ formatCondition(item?.condition || item?.condition_status) }}</p>
          </div>
        </div>

        <!-- Quantity Selection -->
        <div class="quantity-section">
          <div class="quantity-selector">
            <label for="quantity">Quantity:</label>
            <div class="quantity-controls">
              <button type="button" @click="decreaseQuantity" :disabled="orderForm.quantity <= 1" class="qty-btn">-</button>
              <input 
                type="number" 
                id="quantity"
                v-model.number="orderForm.quantity" 
                :min="1" 
                :max="item?.stock || 1"
                @input="validateQuantity"
                class="qty-input"
              >
              <button type="button" @click="increaseQuantity" :disabled="orderForm.quantity >= (item?.stock || 1)" class="qty-btn">+</button>
            </div>
            <span class="stock-info">{{ item?.stock || 0 }} available</span>
          </div>
          <div class="total-price">
            <span class="total-label">Total:</span>
            <span class="total-value">₱{{ formatPrice((item?.price || 0) * orderForm.quantity) }}</span>
          </div>
        </div>

        <!-- Order Form -->
        <div class="order-form">
          <form @submit.prevent="submitOrder">
            <div class="form-group">
              <label for="customerName">Full Name *</label>
              <input 
                type="text" 
                id="customerName"
                v-model="orderForm.customerName" 
                required
                placeholder="Enter your full name"
              >
            </div>

            <div class="form-group">
              <label for="customerPhone">Phone Number</label>
              <input 
                type="tel" 
                id="customerPhone"
                v-model="orderForm.customerPhone" 
                placeholder="Enter your phone number"
              >
            </div>

            <div class="form-group">
              <label for="customerEmail">Email</label>
              <input 
                type="email" 
                id="customerEmail"
                v-model="orderForm.customerEmail" 
                placeholder="Enter your email"
              >
            </div>

            <div class="form-group">
              <label for="shippingAddress">Shipping Address *</label>
              <textarea 
                id="shippingAddress"
                v-model="orderForm.shippingAddress" 
                required
                placeholder="Enter your complete shipping address"
                rows="3"
              ></textarea>
            </div>

            <div class="form-group">
              <label for="paymentMethod">Payment Method</label>
              <select id="paymentMethod" v-model="orderForm.paymentMethod">
                <option value="cash_on_delivery">Cash on Delivery</option>
                <option value="bank_transfer">Bank Transfer</option>
                <option value="gcash">GCash</option>
              </select>
            </div>

            <div class="form-group">
              <label for="customerNotes">Additional Notes</label>
              <textarea 
                id="customerNotes"
                v-model="orderForm.customerNotes" 
                placeholder="Any special instructions or notes"
                rows="2"
              ></textarea>
            </div>

            <div class="modal-actions">
              <button type="button" @click="closeModal" class="cancel-btn">
                Cancel
              </button>
              <button type="submit" :disabled="loading" class="submit-btn">
                {{ loading ? 'Placing Order...' : 'Confirm Order' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ConfirmOrderModal',
  props: {
    show: {
      type: Boolean,
      default: false
    },
    item: {
      type: Object,
      default: null
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      imageLoaded: false,
      orderForm: {
        customerName: '',
        customerPhone: '',
        customerEmail: '',
        shippingAddress: '',
        paymentMethod: 'cash_on_delivery',
        customerNotes: '',
        quantity: 1
      },
      loading: false
    }
  },
  watch: {
    show(newValue) {
      if (newValue) {
        this.imageLoaded = false // Reset image loading state
        this.initializeForm()
      }
    },
    item() {
      this.imageLoaded = false // Reset when item changes
    }
  },
  methods: {
    initializeForm() {
      // Get user info from localStorage and pre-fill the form
      const userInfo = this.getUserInfo()
      
      this.orderForm = {
        customerName: userInfo.fullName || '',
        customerPhone: userInfo.phone || '',
        customerEmail: userInfo.email || '',
        shippingAddress: userInfo.address || '',
        paymentMethod: 'cash_on_delivery',
        customerNotes: '',
        quantity: 1
      }
    },
    
    getUserInfo() {
      try {
        const userInfo = localStorage.getItem('user_info')
        if (userInfo) {
          const user = JSON.parse(userInfo)
          return {
            fullName: user.first_name && user.last_name 
              ? `${user.first_name} ${user.last_name}` 
              : user.username || '',
            email: user.email || '',
            phone: user.phone || '',
            address: user.address || ''
          }
        }
      } catch (error) {
        console.error('Error parsing user info:', error)
      }
      return {}
    },
    
    getItemImage(item) {
      if (!item) return 'http://localhost:5000/uploads/placeholder.svg'
      
      console.log('ConfirmOrderModal - getItemImage called with item:', item);
      
      // Handle direct image property (already processed)
      if (item?.image && typeof item.image === 'string') {
        console.log('Found item.image:', item.image);
        return item.image;
      }
      
      // Handle primary image from API
      if (item?.primary_image?.url) {
        console.log('Found item.primary_image.url:', item.primary_image.url);
        return item.primary_image.url;
      }
      
      // Handle primary_image as string (direct URL)
      if (item?.primary_image && typeof item.primary_image === 'string') {
        console.log('Found item.primary_image as string:', item.primary_image);
        return item.primary_image;
      }
      
      // Handle images array from API  
      if (item?.images && Array.isArray(item.images) && item.images.length > 0) {
        console.log('Found item.images array:', item.images);
        const primaryImage = item.images.find(img => img.isPrimary);
        if (primaryImage?.url) {
          console.log('Found primary image in array:', primaryImage.url);
          return primaryImage.url;
        }
        if (item.images[0]?.url) {
          console.log('Using first image in array:', item.images[0].url);
          return item.images[0].url;
        }
      }
      
      // Handle image_url property
      if (item?.image_url) {
        console.log('Found item.image_url:', item.image_url);
        return item.image_url;
      }
      
      // Default placeholder
      console.log('Using placeholder image');
      return 'http://localhost:5000/uploads/placeholder.svg';
    },
    
    handleImageError(event) {
      event.target.src = 'http://localhost:5000/uploads/placeholder.svg';
    },
    
    formatPrice(price) {
      if (!price) return '0.00'
      return typeof price === 'number' ? price.toFixed(2) : parseFloat(price).toFixed(2)
    },
    
    formatCondition(condition) {
      if (!condition) return 'N/A'
      return condition.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
    },
    
    increaseQuantity() {
      const maxStock = this.item?.stock || 1
      if (this.orderForm.quantity < maxStock) {
        this.orderForm.quantity++
      }
    },
    
    decreaseQuantity() {
      if (this.orderForm.quantity > 1) {
        this.orderForm.quantity--
      }
    },
    
    validateQuantity() {
      const maxStock = this.item?.stock || 1
      if (this.orderForm.quantity > maxStock) {
        this.orderForm.quantity = maxStock
      } else if (this.orderForm.quantity < 1) {
        this.orderForm.quantity = 1
      }
    },
    
    submitOrder() {
      // Prevent double submission
      if (this.loading) {
        return;
      }
      
      // Emit the form data back to the parent component
      this.$emit('submit', {
        ...this.orderForm,
        item: this.item
      })
    },
    
    closeModal() {
      this.$emit('close')
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400;1,500;1,600;1,700;1,800&family=Inter:wght@300;400;500;600;700&display=swap');

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background: #ffffff;
  border-radius: 12px;
  width: 100%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 24px 0;
  border-bottom: 1px solid #e5e7eb;
  margin-bottom: 24px;
}

.modal-title {
  margin: 0;
  font-family: 'Playfair Display', serif;
  font-style: italic;
  font-weight: 700;
  font-size: 24px;
  letter-spacing: -0.5px;
  color: #1f2937;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #6b7280;
  padding: 8px;
  border-radius: 8px;
  transition: all 0.2s;
}

.close-btn:hover {
  background: #f3f4f6;
  color: #1f2937;
}

.order-confirmation {
  padding: 0 24px 24px;
}

.item-summary {
  display: flex;
  gap: 16px;
  padding: 16px;
  background: #ffffff;
  border-radius: 12px;
  margin-bottom: 24px;
  border: 1px solid #e5e7eb;
}

.summary-image {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  background-color: #f8fafc;
  flex-shrink: 0; /* Prevent image from shrinking */
}

.image-container {
  position: relative;
  width: 80px;
  height: 80px;
  flex-shrink: 0;
}

.image-loading {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f8fafc;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid #e2e8f0;
  border-top: 2px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.summary-details {
  flex: 1;
  min-width: 0;
}

.summary-details h3 {
  margin: 0 0 8px 0;
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.summary-category {
  margin: 0 0 4px 0;
  font-size: 14px;
  color: #6b7280;
  text-transform: capitalize;
}

.summary-price {
  margin: 0 0 4px 0;
  font-size: 20px;
  font-weight: 700;
  color: #059669;
}

.summary-condition {
  margin: 0;
  font-size: 14px;
  color: #6b7280;
}

.image-loading {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f8fafc;
  border-radius: 8px;
}

.loading-spinner {
  width: 24px;
  height: 24px;
  border: 2px solid #e5e7eb;
  border-top: 2px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.quantity-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background: #f8fafc;
  border-radius: 12px;
  margin-bottom: 24px;
  border: 1px solid #e2e8f0;
}

.quantity-selector {
  display: flex;
  align-items: center;
  gap: 12px;
}

.quantity-selector label {
  font-weight: 500;
  color: #374151;
  margin: 0;
}

.quantity-controls {
  display: flex;
  align-items: center;
  gap: 2px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  overflow: hidden;
}

.qty-btn {
  width: 32px;
  height: 32px;
  border: none;
  background: #f9fafb;
  color: #374151;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.qty-btn:hover:not(:disabled) {
  background: #e5e7eb;
}

.qty-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.qty-input {
  width: 50px;
  height: 32px;
  border: none;
  text-align: center;
  font-size: 14px;
  font-weight: 500;
  background: white;
}

.qty-input:focus {
  outline: none;
  background: #f9fafb;
}

.stock-info {
  font-size: 12px;
  color: #6b7280;
}

.total-price {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 2px;
}

.total-label {
  font-size: 14px;
  color: #6b7280;
}

.total-value {
  font-size: 20px;
  font-weight: 700;
  color: #059669;
}

.order-form {
  background: white;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #374151;
  font-size: 14px;
}

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 16px;
  transition: border-color 0.2s, box-shadow 0.2s;
  background: white;
  box-sizing: border-box;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-group textarea {
  resize: vertical;
  min-height: 80px;
}

.modal-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid #e5e7eb;
}

.cancel-btn {
  padding: 12px 24px;
  background: #f3f4f6;
  color: #374151;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.cancel-btn:hover {
  background: #e5e7eb;
}

.submit-btn {
  padding: 12px 24px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  min-width: 140px;
}

.submit-btn:hover:not(:disabled) {
  background: #2563eb;
}

.submit-btn:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

/* Responsive Design */
@media (max-width: 640px) {
  .modal-overlay {
    padding: 12px;
  }
  
  .modal-content {
    border-radius: 8px;
  }
  
  .modal-header {
    padding: 20px 20px 0;
  }
  
  .order-confirmation {
    padding: 0 20px 20px;
  }
  
  .item-summary {
    flex-direction: column;
    text-align: center;
  }
  
  .summary-image {
    align-self: center;
  }
  
  .summary-details h3 {
    white-space: normal;
  }
  
  .modal-actions {
    flex-direction: column-reverse;
  }
  
  .modal-actions button {
    width: 100%;
  }
}
</style>
