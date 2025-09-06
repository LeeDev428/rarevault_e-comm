<template>
  <UserLayout>
    <div class="wishlist-container">
      <div class="wishlist-header">
        <h1 class="page-title">My Wishlist</h1>
        <div class="wishlist-info">
          <span class="item-count">{{ wishlistItems.length }} item{{ wishlistItems.length !== 1 ? 's' : '' }}</span>
          <button v-if="wishlistItems.length > 0" @click="clearWishlist" class="clear-btn">
            Clear All
          </button>
        </div>
      </div>

      <!-- Wishlist Actions -->
      <div v-if="wishlistItems.length > 0" class="wishlist-actions">
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
          <button @click="addSelectedToCart" class="action-btn primary">
            Add to Cart ({{ selectedItems.length }})
          </button>
          <button @click="removeSelectedItems" class="action-btn secondary">
            Remove Selected
          </button>
        </div>
      </div>

      <!-- Wishlist Grid -->
      <div v-if="wishlistItems.length > 0" class="wishlist-grid">
        <div 
          v-for="item in wishlistItems" 
          :key="item.id"
          class="wishlist-item"
        >
          <!-- Selection Checkbox -->
          <div class="item-selection">
            <input 
              type="checkbox" 
              :checked="selectedItems.includes(item.id)"
              @change="toggleItemSelection(item.id)"
              class="selection-checkbox"
            />
          </div>

          <!-- Item Image -->
          <div class="item-image-container">
            <img :src="item.image" :alt="item.title" class="item-image" />
            
            <!-- Remove Button -->
            <button @click="removeFromWishlist(item.id)" class="remove-btn">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <line x1="18" y1="6" x2="6" y2="18"/>
                <line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>
          </div>

          <!-- Item Details -->
          <div class="item-details">
            <div class="seller-label">
              <span>{{ item.seller }}</span>
            </div>
            
            <h3 class="item-title">{{ item.title }}</h3>
            
            <div class="item-price">
              <span class="current-price">${{ item.price.toFixed(2) }}</span>
              <span v-if="item.originalPrice && item.originalPrice > item.price" class="original-price">
                ${{ item.originalPrice.toFixed(2) }}
              </span>
            </div>

            <div class="item-status">
              <span :class="['status-indicator', item.available ? 'available' : 'unavailable']">
                {{ item.available ? 'Available' : 'Out of Stock' }}
              </span>
              <span v-if="item.dateAdded" class="date-added">
                Added {{ formatDate(item.dateAdded) }}
              </span>
            </div>

            <!-- Item Actions -->
            <div class="item-actions">
              <button 
                @click="addToCart(item)" 
                :disabled="!item.available"
                class="action-btn primary"
              >
                {{ item.available ? 'Add to Cart' : 'Unavailable' }}
              </button>
              <button @click="contactSeller(item)" class="action-btn secondary">
                Contact Seller
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty Wishlist State -->
      <div v-else class="empty-wishlist">
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
    </div>
  </UserLayout>
</template>

<script>
import UserLayout from '@/components/user/UserLayout.vue'

export default {
  name: 'UserWishlist',
  components: {
    UserLayout
  },
  data() {
    return {
      selectedItems: [],
      wishlistItems: [
        {
          id: 1,
          title: 'Vintage Pocket Watch',
          price: 150.00,
          originalPrice: 175.00,
          image: '/api/placeholder/300/300',
          seller: 'Vintage Items',
          available: true,
          dateAdded: '2024-03-15'
        },
        {
          id: 2,
          title: 'Antique Silver Spoons Set',
          price: 85.00,
          image: '/api/placeholder/300/300',
          seller: 'Vintage Items',
          available: true,
          dateAdded: '2024-03-18'
        },
        {
          id: 3,
          title: 'Vintage Camera',
          price: 220.00,
          image: '/api/placeholder/300/300',
          seller: 'Vintage Items',
          available: false,
          dateAdded: '2024-03-20'
        },
        {
          id: 4,
          title: 'Classic Wrist Watch',
          price: 120.00,
          originalPrice: 140.00,
          image: '/api/placeholder/300/300',
          seller: 'Vintage Items',
          available: true,
          dateAdded: '2024-03-22'
        },
        {
          id: 5,
          title: 'Vintage Typewriter',
          price: 180.00,
          image: '/api/placeholder/300/300',
          seller: 'Vintage Items',
          available: true,
          dateAdded: '2024-03-25'
        }
      ]
    }
  },
  computed: {
    allSelected() {
      return this.wishlistItems.length > 0 && 
             this.selectedItems.length === this.wishlistItems.length
    }
  },
  methods: {
    toggleSelectAll() {
      if (this.allSelected) {
        this.selectedItems = []
      } else {
        this.selectedItems = this.wishlistItems.map(item => item.id)
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
    
    addSelectedToCart() {
      const items = this.wishlistItems.filter(item => 
        this.selectedItems.includes(item.id) && item.available
      )
      console.log('Adding to cart:', items)
      // Handle add to cart logic
      this.selectedItems = []
    },
    
    removeSelectedItems() {
      this.wishlistItems = this.wishlistItems.filter(item => 
        !this.selectedItems.includes(item.id)
      )
      this.selectedItems = []
    },
    
    removeFromWishlist(itemId) {
      this.wishlistItems = this.wishlistItems.filter(item => item.id !== itemId)
      this.selectedItems = this.selectedItems.filter(id => id !== itemId)
    },
    
    clearWishlist() {
      if (confirm('Are you sure you want to clear your entire wishlist?')) {
        this.wishlistItems = []
        this.selectedItems = []
      }
    },
    
    addToCart(item) {
      if (item.available) {
        console.log('Adding to cart:', item)
        // Handle add to cart logic
      }
    },
    
    contactSeller(item) {
      console.log('Contact seller for:', item.title)
      // Handle contact seller logic
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
</style>
