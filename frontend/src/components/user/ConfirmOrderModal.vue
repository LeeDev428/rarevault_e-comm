<template>
  <div v-if="show" class="modal-overlay" @click="closeModal">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h2>Confirm Order</h2>
        <button @click="closeModal" class="close-btn">✕</button>
      </div>
      
      <div class="order-confirmation">
        <!-- Item Summary -->
        <div class="item-summary">
          <img 
            :src="getItemImage(item)" 
            :alt="item?.title || 'Item'" 
            class="summary-image"
            @error="handleImageError"
          >
          <div class="summary-details">
            <h3>{{ item?.title || item?.name }}</h3>
            <p class="summary-category">{{ item?.category }}</p>
            <p class="summary-price">₱{{ formatPrice(item?.price) }}</p>
            <p class="summary-condition">Condition: {{ formatCondition(item?.condition || item?.condition_status) }}</p>
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
      orderForm: {
        customerName: '',
        customerPhone: '',
        customerEmail: '',
        shippingAddress: '',
        paymentMethod: 'cash_on_delivery',
        customerNotes: ''
      }
    }
  },
  watch: {
    show(newValue) {
      if (newValue) {
        this.initializeForm()
      }
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
        customerNotes: ''
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
      if (!item) return 'https://via.placeholder.com/80x80/f3f4f6/9ca3af?text=No+Image'
      
      // Handle different image formats from different sources
      if (item.primary_image?.url) {
        return item.primary_image.url;
      }
      
      if (item.primary_image?.image_url) {
        return item.primary_image.image_url;
      }
      
      if (item.images && item.images.length > 0) {
        const firstImage = item.images[0]
        if (typeof firstImage === 'string') {
          return firstImage;
        }
        return firstImage.url || firstImage.image_url || firstImage;
      }
      
      if (item.image_url) {
        return item.image_url;
      }
      
      // Try to construct image URL from item ID
      if (item.id) {
        return `http://localhost:5000/uploads/items/${item.id}/image_0.jpeg`;
      }
      
      return 'https://via.placeholder.com/80x80/f3f4f6/9ca3af?text=No+Image'
    },
    
    handleImageError(event) {
      event.target.src = 'https://via.placeholder.com/80x80/f3f4f6/9ca3af?text=No+Image';
    },
    
    formatPrice(price) {
      if (!price) return '0.00'
      return typeof price === 'number' ? price.toFixed(2) : parseFloat(price).toFixed(2)
    },
    
    formatCondition(condition) {
      if (!condition) return 'N/A'
      return condition.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
    },
    
    submitOrder() {
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
  background: white;
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

.modal-header h2 {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
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
  background: #f8fafc;
  border-radius: 12px;
  margin-bottom: 24px;
  border: 1px solid #e2e8f0;
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
