<template>
  <UserLayout>
    <div class="wishlist-container">
      <div class="wishlist-header">
        <h1 class="page-title">My Wishlist</h1>
        <div class="wishlist-info">
          <span class="item-count">{{ totalItems }} item{{ totalItems !== 1 ? 's' : '' }}</span>
          <button v-if="wishlistItems.length > 0" @click="clearWishlist" class="clear-btn">
            Clear All
          </button>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Loading wishlist...</p>
      </div>

      <!-- Wishlist Actions -->
      <div v-else-if="wishlistItems.length > 0" class="wishlist-actions">
        <div class="selection-controls">
          <label class="select-all">
            <input 
              type="checkbox" 
              :checked="allSelected"
              @change="toggleSelectAll"
            />
            <span>Select All</span>
          </label>
          <span class="selected-count">{{ selectedItems.length }} selected</span>
        </div>
        
        <div class="bulk-actions" v-if="selectedItems.length > 0">
          <button @click="orderSelectedItems" class="action-btn primary">
            Order Selected ({{ selectedItems.length }})
          </button>
          <button @click="removeSelectedItems" class="action-btn secondary">
            Remove Selected
          </button>
        </div>
      </div>

      <!-- Wishlist Grid -->
      <div v-if="!loading && wishlistItems.length > 0" class="wishlist-grid">
        <div 
          v-for="item in wishlistItems" 
          :key="item.id"
          class="wishlist-item"
        >
          <!-- Selection Checkbox -->
          <div class="item-selection">
            <input 
              type="checkbox" 
              :checked="selectedItems.includes(item.wishlist_id)"
              @change="toggleItemSelection(item.wishlist_id)"
              class="selection-checkbox"
            />
          </div>

          <!-- Item Image -->
          <div class="item-image-container">
            <img :src="getItemImage(item)" 
                 :alt="item.title || 'Item'" 
                 class="item-image" />
            
            <!-- Remove Button -->
            <button @click="removeFromWishlist(item.wishlist_id)" class="remove-btn">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <line x1="18" y1="6" x2="6" y2="18"/>
                <line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>
          </div>

          <!-- Item Details -->
          <div class="item-details">
            <div class="seller-label">
              <span>{{ getSellerName(item) }}</span>
            </div>
            
            <h3 class="item-title">{{ item.title || 'Item Deleted' }}</h3>
            
            <div class="item-price">
              <span class="current-price">₱{{ (item.price || 0).toFixed(2) }}</span>
            </div>

            <div class="item-status">
              <span class="status-indicator available">
                {{ item.category || 'N/A' }}
              </span>
              <span v-if="item.added_to_wishlist" class="date-added">
                Added {{ formatDate(item.added_to_wishlist) }}
              </span>
            </div>

            <!-- Item Actions -->
            <div class="item-actions">
              <button 
                @click="orderItem(item)" 
                :disabled="!item.id"
                class="action-btn primary"
              >
                {{ item.id ? 'Order Now' : 'Unavailable' }}
              </button>
              <button @click="contactSeller(item)" class="action-btn secondary" :disabled="!item.id">
                Contact Seller
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Pagination -->
      <Pagination
        v-if="!loading && totalPages > 1"
        :current-page="currentPage"
        :total-pages="totalPages"
        @page-changed="changePage"
      />

      <!-- Empty Wishlist State -->
      <div v-else-if="!loading && wishlistItems.length === 0" class="empty-wishlist">
        <div class="empty-icon">
          <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
          </svg>
        </div>
        <h2>Your wishlist is empty</h2>
        <p>Save items you love to buy them later or share with friends.</p>
        <router-link to="/user/dashboard" class="btn-primary">
          Browse Items
        </router-link>
      </div>

      <!-- Order Confirmation Modal -->
      <ConfirmOrderModal
        :show="showOrderModal"
        :item="selectedOrderItem"
        :loading="submittingOrder"
        @close="closeOrderModal"
        @submit="submitOrder"
      />
    </div>
  </UserLayout>
</template>

<script>
import UserLayout from '@/components/user/UserLayout.vue'
import Pagination from '@/components/user/Pagination.vue'
import ConfirmOrderModal from '@/components/user/ConfirmOrderModal.vue'

export default {
  name: 'UserWishlist',
  components: {
    UserLayout,
    Pagination,
    ConfirmOrderModal
  },
  data() {
    return {
      selectedItems: [],
      wishlistItems: [],
      currentPage: 1,
      totalPages: 1,
      totalItems: 0,
      itemsPerPage: 12,
      loading: false,
      showOrderModal: false,
      selectedOrderItem: null,
      submittingOrder: false
    }
  },
  computed: {
    allSelected() {
      return this.wishlistItems.length > 0 && 
             this.selectedItems.length === this.wishlistItems.length
    }
  },
  mounted() {
    this.loadWishlist()
  },
  methods: {
    async loadWishlist() {
      this.loading = true
      try {
        const token = localStorage.getItem('access_token') || localStorage.getItem('token')
        if (!token) {
          this.$router.push('/login')
          return
        }

        const params = new URLSearchParams({
          page: this.currentPage,
          per_page: this.itemsPerPage
        })

        const response = await fetch(`http://localhost:5000/api/user/wishlist?${params}`, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })

        if (!response.ok) {
          throw new Error('Failed to fetch wishlist')
        }

        const data = await response.json()
        this.wishlistItems = data.items || []
        this.totalItems = data.pagination?.total || 0
        this.totalPages = data.pagination?.pages || 1
        this.selectedItems = []
      } catch (error) {
        console.error('Error loading wishlist:', error)
        this.wishlistItems = []
        this.totalItems = 0
        this.totalPages = 1
      } finally {
        this.loading = false
      }
    },

    changePage(page) {
      this.currentPage = page
      this.loadWishlist()
    },

    toggleSelectAll() {
      if (this.allSelected) {
        this.selectedItems = []
      } else {
        this.selectedItems = this.wishlistItems.map(item => item.wishlist_id)
      }
    },
    
    toggleItemSelection(itemId) {
      const index = this.selectedItems.indexOf(itemId)
      if (index > -1) {
        this.selectedItems.splice(index, 1)
      } else {
        this.selectedItems.push(itemId)
      }
    },
    
    async orderSelectedItems() {
      const items = this.wishlistItems.filter(item => 
        this.selectedItems.includes(item.wishlist_id) && item.id
      )
      
      if (items.length === 0) {
        alert('No valid items selected for ordering.')
        return
      }

      // For multiple items, we could implement batch ordering
      // For now, let's order them one by one
      for (const item of items) {
        await this.orderItem(item, false)
      }
      
      this.selectedItems = []
      alert(`Successfully placed orders for ${items.length} items!`)
    },
    
    async removeSelectedItems() {
      if (this.selectedItems.length === 0) return
      
      if (!confirm(`Are you sure you want to remove ${this.selectedItems.length} item(s) from your wishlist?`)) {
        return
      }

      try {
        const token = localStorage.getItem('access_token') || localStorage.getItem('token')
        const removePromises = this.selectedItems.map(wishlistId => {
          const item = this.wishlistItems.find(item => item.wishlist_id === wishlistId);
          const itemId = item ? item.id : null;
          if (itemId) {
            return fetch(`http://localhost:5000/api/user/wishlist/${itemId}`, {
              method: 'DELETE',
              headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
              }
            });
          }
          return Promise.resolve();
        }).filter(Boolean)

        await Promise.all(removePromises)
        await this.loadWishlist()
        this.selectedItems = []
      } catch (error) {
        console.error('Error removing items:', error)
        alert('Failed to remove some items. Please try again.')
      }
    },
    
    async removeFromWishlist(wishlistId) {
      if (!confirm('Are you sure you want to remove this item from your wishlist?')) {
        return
      }

      try {
        const token = localStorage.getItem('access_token') || localStorage.getItem('token')
        const item = this.wishlistItems.find(item => item.wishlist_id === wishlistId);
        const itemId = item ? item.id : null;
        
        if (!itemId) {
          alert('Unable to remove item. Please refresh and try again.');
          return;
        }
        
        const response = await fetch(`http://localhost:5000/api/user/wishlist/${itemId}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })

        if (!response.ok) {
          throw new Error('Failed to remove item')
        }

        await this.loadWishlist()
        this.selectedItems = this.selectedItems.filter(id => id !== wishlistId)
      } catch (error) {
        console.error('Error removing item:', error)
        alert('Failed to remove item. Please try again.')
      }
    },
    
    async clearWishlist() {
      if (!confirm('Are you sure you want to clear your entire wishlist?')) {
        return
      }

      try {
        const token = localStorage.getItem('access_token') || localStorage.getItem('token')
        const response = await fetch('http://localhost:5000/api/user/wishlist/clear', {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })

        if (!response.ok) {
          throw new Error('Failed to clear wishlist')
        }

        await this.loadWishlist()
        this.selectedItems = []
      } catch (error) {
        console.error('Error clearing wishlist:', error)
        alert('Failed to clear wishlist. Please try again.')
      }
    },
    
    orderItem(item, showModal = true) {
      if (!item.id) {
        alert('This item is no longer available.')
        return
      }

      if (showModal) {
        this.selectedOrderItem = item
        this.showOrderModal = true
      } else {
        // For batch ordering, use default values
        return this.submitOrder(item)
      }
    },

    async submitOrder(orderData) {
      // Handle both new modal data and legacy batch ordering
      let item, formData;
      
      if (orderData && orderData.item) {
        // New modal structure
        item = orderData.item;
        formData = orderData;
      } else {
        // Legacy batch ordering (fallback)
        item = orderData || this.selectedOrderItem;
        formData = {
          customerName: 'Customer',
          customerEmail: 'customer@example.com',
          customerPhone: 'N/A',
          shippingAddress: 'N/A',
          paymentMethod: 'cash_on_delivery',
          customerNotes: ''
        };
      }

      if (!item || !item.id) return

      this.submittingOrder = true
      try {
        const token = localStorage.getItem('access_token') || localStorage.getItem('token')
        const response = await fetch('http://localhost:5000/api/user/orders', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            item_id: item.id,
            customer_name: formData.customerName || 'Customer',
            customer_email: formData.customerEmail || 'customer@example.com',
            customer_phone: formData.customerPhone || 'N/A',
            customer_address: formData.shippingAddress || 'N/A',
            payment_method: formData.paymentMethod || 'cash_on_delivery',
            notes: formData.customerNotes || ''
          })
        })

        if (!response.ok) {
          throw new Error('Failed to place order')
        }

        if (orderData && orderData.item) {
          alert('Order placed successfully! The seller will contact you soon.')
          this.closeOrderModal()
        }
      } catch (error) {
        console.error('Error placing order:', error)
        if (orderData && orderData.item) {
          alert('Failed to place order. Please try again.')
        }
      } finally {
        this.submittingOrder = false
      }
    },

    closeOrderModal() {
      this.showOrderModal = false
      this.selectedOrderItem = null
    },
    
    contactSeller(item) {
      if (!item.id) {
        alert('This item is no longer available.')
        return
      }
      console.log('Contact seller for:', item.name)
      // Handle contact seller logic
      alert('Contact seller functionality will be implemented soon.')
    },
    
    formatDate(dateString) {
      const date = new Date(dateString)
      const now = new Date()
      const diffTime = Math.abs(now - date)
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
      
      if (diffDays === 1) {
        return 'yesterday'
      } else if (diffDays < 7) {
        return `${diffDays} days ago`
      } else if (diffDays < 30) {
        const weeks = Math.floor(diffDays / 7)
        return `${weeks} week${weeks > 1 ? 's' : ''} ago`
      } else {
        return date.toLocaleDateString('en-US', { 
          month: 'short', 
          day: 'numeric' 
        })
      }
    },

    getItemImage(item) {
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
      
      // Handle single image property
      if (item?.image) {
        return item.image;
      }
      
      // Default placeholder
      return 'http://localhost:5000/uploads/placeholder.svg';
    },

    getSellerName(item) {
      return item.seller_name || item.seller?.username || 'Unknown Seller';
    }
  }
}
</script>

<style scoped>
.wishlist-container {
  max-width: 1200px;
  margin: 0 auto;
}

/* Wishlist Header */
.wishlist-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
}

.page-title {
  font-size: 32px;
  font-weight: 700;
  color: #111827;
  margin: 0;
}

.wishlist-info {
  display: flex;
  align-items: center;
  gap: 16px;
}

.item-count {
  font-size: 16px;
  color: #6b7280;
}

.clear-btn {
  padding: 8px 16px;
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s ease;
}

.clear-btn:hover {
  background: #dc2626;
}

/* Wishlist Actions */
.wishlist-actions {
  background: white;
  padding: 20px 24px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.selection-controls {
  display: flex;
  align-items: center;
  gap: 16px;
}

.select-all {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  font-weight: 500;
}

.selected-count {
  font-size: 14px;
  color: #6b7280;
}

.bulk-actions {
  display: flex;
  gap: 12px;
}

/* Wishlist Grid */
.wishlist-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 24px;
}

.wishlist-item {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.2s ease;
  position: relative;
}

.wishlist-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

/* Item Selection */
.item-selection {
  position: absolute;
  top: 12px;
  left: 12px;
  z-index: 10;
}

.selection-checkbox {
  width: 18px;
  height: 18px;
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(4px);
}

/* Item Image */
.item-image-container {
  position: relative;
  width: 100%;
  height: 200px;
  overflow: hidden;
}

.item-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.remove-btn {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: rgba(239, 68, 68, 0.9);
  color: white;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  opacity: 0;
}

.wishlist-item:hover .remove-btn {
  opacity: 1;
}

.remove-btn:hover {
  background: #dc2626;
  transform: scale(1.1);
}

/* Item Details */
.item-details {
  padding: 20px;
}

.seller-label span {
  font-size: 12px;
  color: #6b7280;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.item-title {
  font-size: 18px;
  font-weight: 600;
  color: #111827;
  margin: 8px 0 12px 0;
  line-height: 1.4;
}

.item-price {
  margin-bottom: 12px;
}

.current-price {
  font-size: 20px;
  font-weight: 700;
  color: #111827;
  margin-right: 8px;
}

.original-price {
  font-size: 16px;
  color: #9ca3af;
  text-decoration: line-through;
}

.item-status {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.status-indicator {
  font-size: 12px;
  font-weight: 600;
  padding: 4px 8px;
  border-radius: 4px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-indicator.available {
  background: #d1fae5;
  color: #065f46;
}

.status-indicator.unavailable {
  background: #fee2e2;
  color: #991b1b;
}

.date-added {
  font-size: 12px;
  color: #9ca3af;
}

/* Item Actions */
.item-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  flex: 1;
  padding: 10px 16px;
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

.action-btn.primary:hover:not(:disabled) {
  background: #2563eb;
}

.action-btn.primary:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

.action-btn.secondary {
  background: #f3f4f6;
  color: #374151;
}

.action-btn.secondary:hover {
  background: #e5e7eb;
}

/* Empty Wishlist */
.empty-wishlist {
  text-align: center;
  padding: 80px 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.empty-icon {
  margin-bottom: 24px;
  color: #d1d5db;
}

.empty-wishlist h2 {
  font-size: 24px;
  font-weight: 600;
  color: #374151;
  margin: 0 0 8px 0;
}

.empty-wishlist p {
  font-size: 16px;
  color: #6b7280;
  margin: 0 0 32px 0;
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
  .wishlist-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
  
  .wishlist-actions {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }
  
  .bulk-actions {
    justify-content: center;
  }
  
  .wishlist-grid {
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 16px;
  }
  
  .item-actions {
    flex-direction: column;
  }
}

/* Loading State */
.loading-state {
  text-align: center;
  padding: 48px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #007bff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 16px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
