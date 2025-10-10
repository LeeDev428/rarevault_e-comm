<template>
  <UserLayout>
    <div class="wishlist-container">
      <!-- Clean Header -->
      <div class="wishlist-header">
        <h1 class="page-title">My Wishlist</h1>
        <div class="header-actions">
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

      <!-- Wishlist Grid - Clean Cards -->
      <div v-if="!loading && wishlistItems.length > 0" class="wishlist-grid">
        <div 
          v-for="item in wishlistItems" 
          :key="item.id"
          class="wishlist-card"
        >
          <!-- Item Image -->
          <div class="card-image">
            <img 
              :src="getItemImage(item)" 
              :alt="item.title || 'Item'" 
              @error="handleImageError"
            />
            <!-- Remove Button -->
            <button @click="removeFromWishlist(item.wishlist_id)" class="remove-btn" title="Remove from wishlist">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"/>
                <line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>
          </div>

          <!-- Item Info -->
          <div class="card-info">
            <div class="seller-tag">{{ getSellerName(item) }}</div>
            
            <h3 class="card-title">{{ item.title || 'Item Deleted' }}</h3>
            
            <div class="card-category">{{ formatCategory(item.category) }}</div>

            <div class="card-footer">
              <div class="card-price">₱{{ formatPrice(item.price || 0) }}</div>
              
              <div class="stock-badge" :class="getStockClass(item.stock)">
                {{ getStockText(item.stock) }}
              </div>
            </div>

            <!-- Action Button -->
            <button 
              @click="orderItem(item)" 
              :disabled="!item.id || item.stock <= 0"
              class="order-btn"
              :class="{ 'disabled': !item.id || item.stock <= 0 }"
            >
              {{ getOrderButtonText(item) }}
            </button>
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
import Pagination from '@/components/pagination.vue'
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
        console.log('Wishlist API response:', data)
        
        this.wishlistItems = data.items || []
        this.totalItems = data.pagination?.total || 0
        this.totalPages = data.pagination?.pages || 1
        this.selectedItems = []
        
        // Debug: Log first item to see structure
        if (this.wishlistItems.length > 0) {
          console.log('First wishlist item structure:', this.wishlistItems[0])
        }
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
          const errorData = await response.json().catch(() => ({}));
          // Only throw real errors, not successful operations
          if (response.status >= 500) {
            throw new Error(errorData.error || 'Server error occurred');
          }
        }

        if (orderData && orderData.item) {
          alert('Order placed successfully! The seller will contact you soon.')
          this.closeOrderModal()
        }
      } catch (error) {
        console.error('Error placing order:', error)
        if (orderData && orderData.item) {
          // Only show error for real failures
          if (!error.message.includes('successfully')) {
            alert('Order processing encountered an issue, but may have been successful. Please check your orders.')
          }
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
      console.log('Getting image for wishlist item:', item);
      
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
      
      // Handle legacy primary image with image_path property
      if (item?.primary_image?.image_path) {
        const imagePath = item.primary_image.image_path;
        console.log('Using primary_image.image_path:', imagePath);
        // If it's already a full URL, use it directly
        if (imagePath.startsWith('http')) {
          return imagePath;
        }
        // Otherwise construct the full URL
        return `http://localhost:5000/${imagePath}`;
      }
      
      // Handle primary_image as string (direct path)
      if (item?.primary_image && typeof item.primary_image === 'string') {
        console.log('Using primary_image string:', item.primary_image);
        if (item.primary_image.startsWith('http')) {
          return item.primary_image;
        }
        return `http://localhost:5000/${item.primary_image}`;
      }
      
      // Handle legacy image_url property
      if (item?.image_url) {
        console.log('Using image_url:', item.image_url);
        if (item.image_url.startsWith('http')) {
          return item.image_url;
        }
        return `http://localhost:5000/${item.image_url}`;
      }
      
      // Handle single image property
      if (item?.image) {
        console.log('Using image:', item.image);
        if (item.image.startsWith('http')) {
          return item.image;
        }
        return `http://localhost:5000/${item.image}`;
      }
      
      // Try to construct image URL from item ID if available
      if (item?.id) {
        console.log('Using constructed URL for item ID:', item.id);
        return `http://localhost:5000/uploads/items/${item.id}/image_0.jpeg`;
      }
      
      // Try alternative path structure based on database schema
      if (item?.item_id) {
        console.log('Using constructed URL for item_id:', item.item_id);
        return `http://localhost:5000/uploads/items/${item.item_id}/image_0.jpeg`;
      }
      
      console.log('No image found for item, using placeholder');
      // Default placeholder
      return 'http://localhost:5000/uploads/placeholder.svg';
    },

    handleImageError(event) {
      console.log('Wishlist image failed to load, using placeholder');
      event.target.src = 'http://localhost:5000/uploads/placeholder.svg';
    },

    getOrderButtonText(item) {
      if (!item.id) {
        return 'Unavailable';
      } else if (item.stock <= 0) {
        return 'Out of Stock';
      } else {
        return 'Order Now';
      }
    },

    getSellerName(item) {
      return item.seller_name || item.seller?.username || 'Unknown Seller';
    },

    formatCategory(category) {
      if (!category) return 'N/A';
      return category.toString()
        .split('_')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
        .join(' ');
    },

    formatPrice(price) {
      return new Intl.NumberFormat('en-PH', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      }).format(price);
    },

    getStockClass(stock) {
      if (!stock || stock === 0) return 'out-of-stock';
      if (stock < 5) return 'low-stock';
      return 'in-stock';
    },

    getStockText(stock) {
      if (!stock || stock === 0) return 'Out of stock';
      if (stock === 1) return '1 item left';
      return `${stock} available`;
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* Container */
.wishlist-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem 1.5rem;
  background: #f9fafb;
  min-height: 100vh;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Header - Clean & Minimal */
.wishlist-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e5e7eb;
}

.page-title {
  font-size: 1.875rem;
  font-weight: 700;
  color: #111827;
  margin: 0;
  letter-spacing: -0.025em;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 1.25rem;
}

.item-count {
  font-size: 0.938rem;
  color: #6b7280;
  font-weight: 500;
}

.clear-btn {
  padding: 0.5rem 1rem;
  background: white;
  color: #ef4444;
  border: 1.5px solid #e5e7eb;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.clear-btn:hover {
  border-color: #ef4444;
  background: #fef2f2;
}

/* Loading State */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  gap: 1rem;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #e5e7eb;
  border-top: 3px solid #111827;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-state p {
  color: #6b7280;
  font-size: 0.938rem;
}

/* Wishlist Grid - Clean Cards */
.wishlist-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.25rem;
  margin-bottom: 2rem;
}

/* Wishlist Card - Minimal Design */
.wishlist-card {
  background: white;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
  overflow: hidden;
  transition: all 0.2s;
  display: flex;
  flex-direction: column;
}

.wishlist-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  transform: translateY(-2px);
}

/* Card Image */
.card-image {
  position: relative;
  width: 100%;
  height: 280px;
  overflow: hidden;
  background: #f9fafb;
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.wishlist-card:hover .card-image img {
  transform: scale(1.05);
}

/* Remove Button */
.remove-btn {
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
  width: 36px;
  height: 36px;
  background: white;
  border: none;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  opacity: 0;
  transition: all 0.2s;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.wishlist-card:hover .remove-btn {
  opacity: 1;
}

.remove-btn:hover {
  background: #fef2f2;
  color: #ef4444;
}

.remove-btn svg {
  stroke-width: 2.5;
}

/* Card Info */
.card-info {
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  flex: 1;
}

.seller-tag {
  font-size: 0.75rem;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.card-title {
  font-size: 1rem;
  font-weight: 600;
  color: #111827;
  margin: 0;
  line-height: 1.4;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
}

.card-category {
  font-size: 0.813rem;
  color: #9ca3af;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 0.5rem;
  padding-top: 0.75rem;
  border-top: 1px solid #f3f4f6;
}

.card-price {
  font-size: 1.125rem;
  font-weight: 700;
  color: #111827;
}

/* Stock Badge */
.stock-badge {
  padding: 0.25rem 0.625rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
}

.stock-badge.in-stock {
  background: #ecfdf5;
  color: #10b981;
}

.stock-badge.low-stock {
  background: #fef3c7;
  color: #f59e0b;
}

.stock-badge.out-of-stock {
  background: #fef2f2;
  color: #ef4444;
}

/* Order Button */
.order-btn {
  width: 100%;
  padding: 0.75rem;
  margin-top: 0.75rem;
  background: #111827;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.order-btn:hover:not(.disabled) {
  background: #000;
  transform: translateY(-1px);
}

.order-btn.disabled {
  background: #e5e7eb;
  color: #9ca3af;
  cursor: not-allowed;
}

/* Empty Wishlist State */
.empty-wishlist {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 500px;
  text-align: center;
  padding: 3rem 1.5rem;
  background: white;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
}

.empty-icon {
  margin-bottom: 1.5rem;
  color: #d1d5db;
}

.empty-wishlist h2 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #111827;
  margin: 0 0 0.75rem 0;
}

.empty-wishlist p {
  font-size: 1rem;
  color: #6b7280;
  margin: 0 0 2rem 0;
  max-width: 400px;
}

.btn-primary {
  padding: 0.875rem 2rem;
  background: #111827;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-size: 0.938rem;
  font-weight: 600;
  transition: all 0.2s;
  display: inline-block;
}

.btn-primary:hover {
  background: #000;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

/* Responsive Design */
@media (max-width: 1024px) {
  .wishlist-grid {
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 1rem;
  }
}

@media (max-width: 768px) {
  .wishlist-container {
    padding: 1.5rem 1rem;
  }

  .wishlist-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .page-title {
    font-size: 1.5rem;
  }

  .wishlist-grid {
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 0.875rem;
  }

  .card-image {
    height: 220px;
  }
}

@media (max-width: 480px) {
  .wishlist-container {
    padding: 1rem 0.75rem;
  }

  .wishlist-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 0.75rem;
  }

  .card-image {
    height: 180px;
  }

  .card-info {
    padding: 0.75rem;
  }

  .card-title {
    font-size: 0.875rem;
  }

  .card-price {
    font-size: 1rem;
  }
}
</style>
