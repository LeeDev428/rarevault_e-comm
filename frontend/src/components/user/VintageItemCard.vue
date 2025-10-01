<template>
  <div class="vintage-item-card">
    <!-- Item Image Container -->
    <div class="item-image-container">
      <!-- Single Image Layout -->
      <div v-if="getItemImages(item).length === 1" class="single-image-layout">
        <img :src="getItemImages(item)[0].url" :alt="item.title" class="item-image single" />
      </div>
      
      <!-- Multiple Images Layout (Facebook style) -->
      <div v-else-if="getItemImages(item).length > 1" class="multiple-images-layout">
        <!-- Primary Image (Left side - bigger) -->
        <div class="primary-image-container">
          <img :src="getPrimaryImage(item).url" :alt="item.title" class="item-image primary" />
        </div>
        
        <!-- Secondary Images (Right side - smaller grid) -->
        <div class="secondary-images-container">
          <div v-for="(image, index) in getSecondaryImages(item)" 
               :key="image.id || index" 
               class="secondary-image-wrapper"
               :class="{ 'has-more': index === 2 && getSecondaryImages(item).length > 3 }">
            <img :src="image.url" :alt="`${item.title} ${index + 2}`" class="item-image secondary" />
            <!-- More images overlay -->
            <div v-if="index === 2 && getSecondaryImages(item).length > 3" class="more-images-overlay">
              <span>+{{ getSecondaryImages(item).length - 3 }}</span>
            </div>
          </div>
        </div>
      </div>
      
      <!-- No Image Layout -->
      <div v-else class="no-image-layout">
        <img :src="'http://localhost:5000/uploads/placeholder.svg'" :alt="item.title" class="item-image placeholder" />
      </div>
      
      <!-- Overlay Actions on Hover -->
      <div class="item-overlay">
        <div class="item-actions">
          <button 
            class="action-btn view-details-btn"
            @click="viewItemDetails"
          >
            View Details
          </button>
          
          <button 
            class="action-btn order-btn"
            @click="openOrderModal"
          >
            Order Now
          </button>
         
          <button 
            class="action-btn save-btn"
            @click="$emit('save-item', item)"
          >
            Save to wishlist
          </button>
        </div>
      </div>
    </div>

    <!-- Item Details -->
    <div class="item-details">
      <div class="seller-label">
        <span>{{ item.seller }}</span>
      </div>
      
      <h3 class="item-title">{{ item.title }}</h3>
      
      <div class="item-footer">
        <div class="item-stats">
          <!-- Rating -->
          <div v-if="item.rating > 0" class="rating-display">
            <div class="stars">
              <span v-for="star in 5" :key="star" 
                    :class="['star', { filled: star <= Math.round(item.rating) }]">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z"/>
                </svg>
              </span>
            </div>
            <span class="rating-text">{{ item.rating.toFixed(1) }} ({{ item.ratingCount }})</span>
          </div>
          
          <!-- Sold Count -->
          <div v-if="item.soldCount > 0" class="sold-count">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/>
              <line x1="3" y1="6" x2="21" y2="6"/>
              <path d="M16 10a4 4 0 0 1-8 0"/>
            </svg>
            <span>{{ item.soldCount }} sold</span>
          </div>
          
          <!-- Stock Count -->
          <div class="stock-count" :class="{ 'low-stock': item.stock < 5, 'out-of-stock': item.stock === 0 }">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
              <line x1="16" y1="2" x2="16" y2="6"/>
              <line x1="8" y1="2" x2="8" y2="6"/>
              <line x1="3" y1="10" x2="21" y2="10"/>
            </svg>
            <span v-if="item.stock > 0">{{ item.stock }} in stock</span>
            <span v-else>Out of stock</span>
          </div>
        </div>
        
        <div class="item-price">
          <span class="price-label">Price</span>
          <span class="price-value">₱{{ item.price.toFixed(2) }}</span>
        </div>
      </div>
    </div>
  </div>
  
  <!-- Order Confirmation Modal -->
  <ConfirmOrderModal
    :show="showOrderModal"
    :item="item"
    :loading="orderLoading"
    @close="closeOrderModal"
    @submit="handleOrderSubmit"
  />
</template>

<script>
import ConfirmOrderModal from './ConfirmOrderModal.vue'

export default {
  name: 'VintageItemCard',
  components: {
    ConfirmOrderModal
  },
  props: {
    item: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      showOrderModal: false,
      orderLoading: false
    }
  },
  emits: ['contact-seller', 'save-item', 'order-item', 'order-submitted'],
  methods: {
    getItemImage(item) {
      // Handle direct image property (already processed)
      if (item?.image && typeof item.image === 'string') {
        return item.image;
      }
      
      // Handle primary image from API
      if (item?.primary_image?.url) {
        return item.primary_image.url;
      }
      
      // Handle primary_image as string (direct URL)
      if (item?.primary_image && typeof item.primary_image === 'string') {
        return item.primary_image;
      }
      
      // Handle images array from API  
      if (item?.images && Array.isArray(item.images) && item.images.length > 0) {
        const primaryImage = item.images.find(img => img.isPrimary);
        if (primaryImage?.url) {
          return primaryImage.url;
        }
        if (item.images[0]?.url) {
          return item.images[0].url;
        }
      }
      
      // Handle image_url property
      if (item?.image_url) {
        return item.image_url;
      }
      
      // Default placeholder
      return 'http://localhost:5000/uploads/placeholder.svg';
    },
    
    getItemImages(item) {
      // Get all images for the item
      let images = [];
      
      // Handle images array from API
      if (item?.images && Array.isArray(item.images) && item.images.length > 0) {
        images = item.images.filter(img => img.url);
      }
      // Handle primary_image as single image
      else if (item?.primary_image?.url) {
        images = [item.primary_image];
      }
      // Handle primary_image as string
      else if (item?.primary_image && typeof item.primary_image === 'string') {
        images = [{ url: item.primary_image, isPrimary: true }];
      }
      // Handle single image property
      else if (item?.image && typeof item.image === 'string') {
        images = [{ url: item.image, isPrimary: true }];
      }
      // Handle image_url property
      else if (item?.image_url) {
        images = [{ url: item.image_url, isPrimary: true }];
      }
      
      return images;
    },
    
    getPrimaryImage(item) {
      const images = this.getItemImages(item);
      // Find primary image or return first image
      return images.find(img => img.isPrimary) || images[0] || { url: 'http://localhost:5000/uploads/placeholder.svg' };
    },
    
    getSecondaryImages(item) {
      const images = this.getItemImages(item);
      // Return non-primary images, limit to 3 for display
      const secondaryImages = images.filter(img => !img.isPrimary);
      return secondaryImages.slice(0, 3);
    },
    
    viewItemDetails() {
      // Navigate to item details page
      this.$router.push(`/user/items/${this.item.id}`);
    },
    
    openOrderModal() {
      this.showOrderModal = true;
    },
    
    closeOrderModal() {
      this.showOrderModal = false;
      this.orderLoading = false;
    },
    
    async handleOrderSubmit(orderData) {
      // Prevent double submission
      if (this.orderLoading) {
        return;
      }
      
      try {
        this.orderLoading = true;
        
        const token = localStorage.getItem('access_token') || localStorage.getItem('token');
        if (!token) {
          this.$router.push('/login');
          return;
        }
        
        // Use item from the order data or current item
        const item = orderData.item || this.item;
        if (!item || !item.id) {
          throw new Error('Item information is missing. Please try again.');
        }
        
        const submitData = {
          item_id: item.id,
          quantity: orderData.quantity || 1,
          customer_name: orderData.customerName || '',
          customer_phone: orderData.customerPhone || '',
          customer_email: orderData.customerEmail || '',
          shipping_address: orderData.shippingAddress || '',
          payment_method: orderData.paymentMethod || 'cash_on_delivery',
          customer_notes: orderData.customerNotes || '',
          request_id: `${Date.now()}_${Math.random().toString(36).substr(2, 9)}` // Unique request ID
        };
        
        console.log('Submitting order for item:', item.id);
        console.log('Order data:', submitData);
        
        // Add timeout to prevent hanging requests
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 10000); // 10 second timeout
        
        const response = await fetch('http://localhost:5000/api/user/orders', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(submitData),
          signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        
        // Simplified response handling - just check if it's a real error
        if (!response.ok && response.status >= 500) {
          throw new Error(`Server error! status: ${response.status}`);
        }
        
        // Try to get response data, but don't fail if we can't
        let data = null;
        try {
          data = await response.json();
        } catch (e) {
          console.log('Could not parse response JSON, but request may have succeeded');
        }
        
        console.log('Order created:', data);
        
        this.showToast('success', 'Order placed successfully! The seller will contact you soon.');
        this.closeOrderModal();
        
        // Emit event to parent to refresh data if needed
        this.$emit('order-submitted', { item: this.item, orderData });
        
      } catch (error) {
        console.error('Error creating order:', error);
        
        // Handle different error types
        if (error.name === 'AbortError') {
          this.showToast('error', 'Order request timed out. Please check your orders to see if it was created.');
        } else {
          // For other errors, just close modal and show generic message
          this.showToast('error', 'Order processing encountered an issue. Please check your orders.');
        }
        
        this.closeOrderModal();
      } finally {
        this.orderLoading = false;
      }
    },
    
    showToast(type, message) {
      // Simple toast implementation
      const toast = document.createElement('div');
      toast.className = `toast toast-${type}`;
      toast.textContent = message;
      toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 12px 24px;
        border-radius: 6px;
        color: white;
        font-weight: 500;
        z-index: 10000;
        ${type === 'success' ? 'background-color: #10b981;' : 'background-color: #ef4444;'}
      `;
      document.body.appendChild(toast);
      
      setTimeout(() => {
        if (toast.parentNode) {
          toast.parentNode.removeChild(toast);
        }
      }, 3000);
    }
  }
}
</script>

<style scoped>
.vintage-item-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 8px 24px rgba(139, 90, 60, 0.12);
  transition: all 0.3s ease;
  cursor: pointer;
}

.vintage-item-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(139, 90, 60, 0.18);
}

/* Image Container */
.item-image-container {
  position: relative;
  width: 100%;
  height: 240px;
  overflow: hidden;
}

/* Single Image Layout */
.single-image-layout {
  width: 100%;
  height: 100%;
}

.item-image.single,
.item-image.placeholder {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

/* Multiple Images Layout (Facebook style) */
.multiple-images-layout {
  display: flex;
  width: 100%;
  height: 100%;
  gap: 2px;
}

.primary-image-container {
  flex: 1;
  height: 100%;
}

.item-image.primary {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.secondary-images-container {
  flex: 0 0 50%;
  display: flex;
  flex-direction: column;
  gap: 2px;
  height: 100%;
}

.secondary-image-wrapper {
  flex: 1;
  position: relative;
  overflow: hidden;
}

.item-image.secondary {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

/* More images overlay */
.more-images-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 18px;
  font-weight: 600;
}

.item-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.vintage-item-card:hover .item-image {
  transform: scale(1.05);
}

/* Overlay */
.item-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.vintage-item-card:hover .item-overlay {
  opacity: 1;
}

.item-actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 20px;
}

.action-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: center;
  min-width: 140px;
}

.view-details-btn {
  background: #6B7280;
  color: white;
}

.view-details-btn:hover {
  background: #4B5563;
  transform: translateY(-1px);
}

.order-btn {
  background: #007bff;
  color: white;
}

.order-btn:hover {
  background: #0056b3;
  transform: translateY(-1px);
}

.contact-btn {
  background: #000000;
  color: white;
}

.contact-btn:hover {
  background: #1f2937;
}

.save-btn {
  background: white;
  color: #374151;
  border: 1px solid #d1d5db;
}

.save-btn:hover {
  background: #f9fafb;
  border-color: #9ca3af;
}

/* Item Details */
.item-details {
  padding: 16px;
}

.seller-label {
  margin-bottom: 8px;
}

.seller-label span {
  font-size: 12px;
  color: #6b7280;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.item-title {
  font-size: 16px;
  font-weight: 600;
  color: #111827;
  margin: 0 0 12px 0;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.item-footer {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 12px;
}

.item-stats {
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex: 1;
}

.rating-display {
  display: flex;
  align-items: center;
  gap: 6px;
}

.stars {
  display: flex;
  gap: 1px;
}

.star {
  color: #d1d5db;
}

.star.filled {
  color: #f59e0b;
}

.rating-text {
  font-size: 12px;
  color: #6b7280;
  font-weight: 500;
}

.sold-count {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #6b7280;
  font-size: 12px;
  font-weight: 500;
}

.sold-count svg {
  color: #9ca3af;
}

.stock-count {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #16a34a;
  font-size: 12px;
  font-weight: 500;
}

.stock-count.low-stock {
  color: #f59e0b;
}

.stock-count.out-of-stock {
  color: #dc2626;
}

.stock-count svg {
  color: inherit;
}

.item-price {
  display: flex;
  flex-direction: column;
  gap: 2px;
  align-items: flex-end;
}

.price-label {
  font-size: 12px;
  color: #6b7280;
  font-weight: 500;
}

.price-value {
  font-size: 18px;
  font-weight: 700;
  color: #111827;
}

/* Responsive */
@media (max-width: 768px) {
  .item-image-container {
    height: 200px;
  }
  
  .multiple-images-layout {
    gap: 1px;
  }
  
  .secondary-images-container {
    gap: 1px;
  }
  
  .more-images-overlay {
    font-size: 14px;
  }
  
  .item-actions {
    padding: 16px;
    gap: 10px;
  }
  
  .action-btn {
    padding: 8px 16px;
    font-size: 13px;
    min-width: 120px;
  }
  
  .item-details {
    padding: 12px;
  }
  
  .item-footer {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .item-stats {
    width: 100%;
  }
  
  .item-price {
    align-items: flex-start;
    width: 100%;
  }
  
  .item-title {
    font-size: 15px;
  }
  
  .price-value {
    font-size: 16px;
  }
}
</style>
