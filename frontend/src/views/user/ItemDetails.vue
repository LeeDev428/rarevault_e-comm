<template>
  <UserLayout>
    <div class="item-details-container">
      <!-- Loading State -->
      <div v-if="loading" class="loading-container">
        <div class="loading-spinner"></div>
        <p>Loading item details...</p>
      </div>
      
      <!-- Error State -->
      <div v-else-if="error" class="error-container">
        <div class="error-message">
          <h3>Error Loading Item</h3>
          <p>{{ error }}</p>
          <button @click="fetchItemDetails" class="retry-btn">Try Again</button>
        </div>
      </div>
      
      <!-- Item Details -->
      <div v-else-if="item" class="item-details-content">
        <!-- Breadcrumb Navigation -->
        <nav class="breadcrumb">
          <router-link to="/user/dashboard" class="breadcrumb-link">Home</router-link>
          <span class="breadcrumb-separator">></span>
          <span class="breadcrumb-current">{{ item.title }}</span>
        </nav>

        <div class="item-details-layout">
          <!-- Left Side - Images -->
          <div class="item-images-section">
            <!-- Main Image -->
            <div class="main-image-container">
              <img 
                :src="selectedImage || getItemImage(item)" 
                :alt="item.title"
                class="main-image"
                @error="handleImageError"
              >
            </div>
            
            <!-- Image Thumbnails -->
            <div v-if="itemImages.length > 1" class="image-thumbnails">
              <div 
                v-for="(image, index) in itemImages" 
                :key="image.id || index"
                class="thumbnail-container"
                :class="{ active: selectedImage === image.url }"
                @click="selectedImage = image.url"
              >
                <img 
                  :src="image.url" 
                  :alt="`${item.title} ${index + 1}`"
                  class="thumbnail-image"
                >
              </div>
            </div>
          </div>

          <!-- Right Side - Item Information -->
          <div class="item-info-section">
            <!-- Item Title and Basic Info -->
            <div class="item-header">
              <h1 class="item-title">{{ item.title }}</h1>
              <div class="item-meta">
                <span class="item-category">{{ formatCategoryName(item.category) }}</span>
                <span class="item-condition">{{ formatCondition(item.condition || item.condition_status) }}</span>
                <span v-if="item.year" class="item-year">{{ item.year }}</span>
              </div>
            </div>

            <!-- Price and Stock -->
            <div class="price-section">
              <div class="price-info">
                <span class="price-label">Price</span>
                <span class="price-value">₱{{ formatPrice(item.price || 0) }}</span>
                <span v-if="item.isNegotiable" class="negotiable-tag">Negotiable</span>
              </div>
              <div class="stock-info">
                <span class="stock-label">Stock:</span>
                <span class="stock-value" :class="{ 'low-stock': (item.stock || 0) < 5, 'out-of-stock': (item.stock || 0) === 0 }">
                  {{ (item.stock || 0) > 0 ? `${item.stock} available` : 'Out of stock' }}
                </span>
              </div>
            </div>

            <!-- Rating and Sales Info -->
            <div v-if="(item.rating && item.rating > 0) || (item.soldCount && item.soldCount > 0)" class="stats-section">
              <div v-if="item.rating && item.rating > 0" class="rating-display">
                <div class="stars">
                  <span v-for="star in 5" :key="star" 
                        :class="['star', { filled: star <= Math.round(item.rating || 0) }]">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z"/>
                    </svg>
                  </span>
                </div>
                <span class="rating-text">{{ (item.rating || 0).toFixed(1) }} ({{ item.ratingCount || 0 }} reviews)</span>
              </div>
              
              <div v-if="item.soldCount && item.soldCount > 0" class="sold-info">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/>
                  <line x1="3" y1="6" x2="21" y2="6"/>
                  <path d="M16 10a4 4 0 0 1-8 0"/>
                </svg>
                <span>{{ item.soldCount }} sold</span>
              </div>
            </div>

            <!-- Seller Information -->
            <div class="seller-section">
              <h3 class="section-title">Seller Information</h3>
              <div class="seller-info">
                <div class="seller-avatar">
                  <div class="avatar-circle">
                    {{ getSellerInitials() }}
                  </div>
                </div>
                <div class="seller-details">
                  <div class="seller-main-info">
                    <span class="seller-name">{{ getSellerDisplayName() }}</span>
                    <span class="seller-role-badge">{{ seller?.role || 'Seller' }}</span>
                  </div>
                  
                  <div class="seller-meta">
                    <div v-if="seller?.created_at" class="seller-since">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <circle cx="12" cy="12" r="3"></circle>
                        <path d="M12 1v6m0 6v6"></path>
                        <path d="m21 12-6 0m-6 0-6 0"></path>
                      </svg>
                      Member since {{ formatDate(seller.created_at) }}
                    </div>
                    
                    <div v-if="sellerProfile?.total_sales && sellerProfile.total_sales > 0" class="seller-sales">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/>
                        <line x1="3" y1="6" x2="21" y2="6"/>
                        <path d="M16 10a4 4 0 0 1-8 0"/>
                      </svg>
                      {{ sellerProfile.total_sales }} total sales
                    </div>
                    
                    <div v-if="sellerProfile?.rating && sellerProfile.rating > 0" class="seller-rating">
                      <div class="seller-stars">
                        <span v-for="star in 5" :key="star" 
                              :class="['star', { filled: star <= Math.round(sellerProfile.rating) }]">
                          <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z"/>
                          </svg>
                        </span>
                      </div>
                      <span class="seller-rating-text">{{ sellerProfile.rating.toFixed(1) }} seller rating</span>
                    </div>
                  </div>
                  
                  <div v-if="sellerProfile?.business_name" class="seller-business">
                    <strong>{{ sellerProfile.business_name }}</strong>
                  </div>
                  
                  <div v-if="sellerProfile?.description" class="seller-description">
                    {{ sellerProfile.description }}
                  </div>
                  
                  <div v-if="sellerProfile?.verification_status === 'verified'" class="seller-verified">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                      <path d="M9 12l2 2 4-4"/>
                      <path d="M21 12c-1 0-3-1-3-3s2-3 3-3 3 1 3 3-2 3-3 3"/>
                      <path d="M3 12c1 0 3-1 3-3s-2-3-3-3-3 1-3 3 2 3 3 3"/>
                      <path d="M12 3c0 1-1 3-3 3s-3-2-3-3 1-3 3-3 3 2 3 3"/>
                      <path d="M12 21c0-1-1-3-3-3s-3 2-3 3 1 3 3 3 3-2 3-3"/>
                    </svg>
                    <span>Verified Seller</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Item Description -->
            <div class="description-section">
              <h3 class="section-title">Description</h3>
              <div class="description-content">
                <p v-if="item.description">{{ item.description }}</p>
                <p v-else class="no-description">No description provided for this item.</p>
              </div>
            </div>

            <!-- Tags -->
            <div v-if="item.tags && item.tags.length > 0" class="tags-section">
              <h3 class="section-title">Tags</h3>
              <div class="tags-container">
                <span v-for="tag in item.tags" :key="tag" class="tag">{{ tag }}</span>
              </div>
            </div>

            <!-- Action Buttons -->
            <div class="action-section">
              <button 
                v-if="(item.stock || 0) > 0"
                @click="showOrderModal = true"
                class="primary-btn order-btn"
                :disabled="(item.stock || 0) === 0"
              >
                Order Now
              </button>
              
          
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Order Confirmation Modal -->
    <ConfirmOrderModal
      v-if="showOrderModal"
      :show="showOrderModal"
      :item="item"
      @close="showOrderModal = false"
      @order-confirmed="handleOrderConfirmed"
    />
  </UserLayout>
</template>

<script>
import UserLayout from '@/components/user/UserLayout.vue'
import ConfirmOrderModal from '@/components/user/ConfirmOrderModal.vue'
import axios from 'axios'

export default {
  name: 'ItemDetails',
  components: {
    UserLayout,
    ConfirmOrderModal
  },
  data() {
    return {
      item: null,
      seller: null,
      sellerProfile: null,
      loading: true,
      error: null,
      selectedImage: null,
      showOrderModal: false,
      isAddingToWishlist: false
    }
  },
  computed: {
    itemImages() {
      if (!this.item) return []
      
      let images = []
      
      // Handle images array from API
      if (this.item.images && Array.isArray(this.item.images) && this.item.images.length > 0) {
        images = this.item.images.filter(img => img.url)
      }
      // Handle primary_image as single image
      else if (this.item.primary_image?.url) {
        images = [this.item.primary_image]
      }
      // Handle primary_image as string
      else if (this.item.primary_image && typeof this.item.primary_image === 'string') {
        images = [{ url: this.item.primary_image, isPrimary: true }]
      }
      // Handle image_url property
      else if (this.item.image_url) {
        images = [{ url: this.item.image_url, isPrimary: true }]
      }
      
      return images
    }
  },
  async mounted() {
    await this.fetchItemDetails()
  },
  methods: {
    async fetchItemDetails() {
      try {
        this.loading = true
        this.error = null
        
        const itemId = this.$route.params.id
        console.log('Fetching item details for ID:', itemId)
        
        // Fetch item details
        const response = await axios.get(`http://localhost:5000/api/items/${itemId}`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        })
        
        console.log('API Response:', response.data)
        
        // The API returns {item: {...}} so we need to access response.data.item
        this.item = response.data.item || response.data
        console.log('Item data:', this.item)
        
        // Set the first image as selected
        if (this.itemImages.length > 0) {
          this.selectedImage = this.itemImages[0].url
        }
        
        // Fetch seller details
        if (this.item.seller_id) {
          await this.fetchSellerDetails(this.item.seller_id)
        }
        
      } catch (error) {
        console.error('Error fetching item details:', error)
        this.error = error.response?.data?.error || 'Failed to load item details'
      } finally {
        this.loading = false
      }
    },
    
    async fetchSellerDetails(sellerId) {
      try {
        // Fetch basic seller information
        const response = await axios.get(`http://localhost:5000/api/users/${sellerId}`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        })
        this.seller = response.data
        
        // Fetch seller profile if they are a seller
        if (response.data.role === 'seller') {
          await this.fetchSellerProfile(sellerId)
        }
      } catch (error) {
        console.error('Error fetching seller details:', error)
        // Don't show error for seller details, it's optional
      }
    },
    
    async fetchSellerProfile(sellerId) {
      try {
        const response = await axios.get(`http://localhost:5000/api/seller/profile/${sellerId}`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        })
        this.sellerProfile = response.data
      } catch (error) {
        console.error('Error fetching seller profile:', error)
        // Seller profile is optional, don't show error
      }
    },
    
    getItemImage(item) {
      // Handle direct image property
      if (item?.image && typeof item.image === 'string') {
        return item.image
      }
      
      // Handle primary image from API
      if (item?.primary_image?.url) {
        return item.primary_image.url
      }
      
      // Handle primary_image as string
      if (item?.primary_image && typeof item.primary_image === 'string') {
        return item.primary_image
      }
      
      // Handle images array from API  
      if (item?.images && Array.isArray(item.images) && item.images.length > 0) {
        const primaryImage = item.images.find(img => img.isPrimary)
        if (primaryImage?.url) {
          return primaryImage.url
        }
        if (item.images[0]?.url) {
          return item.images[0].url
        }
      }
      
      // Handle image_url property
      if (item?.image_url) {
        return item.image_url
      }
      
      // Default placeholder
      return 'http://localhost:5000/uploads/placeholder.svg'
    },
    
    handleImageError(event) {
      event.target.src = 'http://localhost:5000/uploads/placeholder.svg'
    },
    
    formatPrice(price) {
      const numPrice = parseFloat(price)
      if (isNaN(numPrice)) {
        return '0.00'
      }
      return numPrice.toFixed(2)
    },
    
    formatCategoryName(category) {
      if (!category) return 'Uncategorized'
      return category.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
    },
    
    formatCondition(condition) {
      if (!condition) return 'Not specified'
      return condition.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
    },
    
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'long' 
      })
    },
    
    async addToWishlist() {
      try {
        this.isAddingToWishlist = true
        
        await axios.post(`http://localhost:5000/api/wishlist`, {
          item_id: this.item.id
        }, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json'
          }
        })
        
        // Show success message (you can implement a toast notification)
        alert('Item added to wishlist!')
        
      } catch (error) {
        console.error('Error adding to wishlist:', error)
        const errorMessage = error.response?.data?.error || 'Failed to add item to wishlist'
        alert(errorMessage)
      } finally {
        this.isAddingToWishlist = false
      }
    },
    
    getSellerInitials() {
      if (this.seller?.first_name && this.seller?.last_name) {
        return `${this.seller.first_name.charAt(0)}${this.seller.last_name.charAt(0)}`.toUpperCase()
      } else if (this.seller?.username) {
        return this.seller.username.charAt(0).toUpperCase()
      } else if (this.item?.seller) {
        return this.item.seller.charAt(0).toUpperCase()
      }
      return 'S'
    },
    
    getSellerDisplayName() {
      if (this.seller?.first_name && this.seller?.last_name) {
        return `${this.seller.first_name} ${this.seller.last_name}`
      } else if (this.seller?.username) {
        return this.seller.username
      } else if (this.item?.seller) {
        return this.item.seller
      }
      return 'Seller'
    },
    
    handleOrderConfirmed(orderData) {
      this.showOrderModal = false
      // Navigate to orders page or show success message
      this.$router.push('/user/orders')
    }
  }
}
</script>

<style scoped>
.item-details-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

/* Loading and Error States */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  gap: 20px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f4f6;
  border-top: 4px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

.error-message {
  text-align: center;
  padding: 40px;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 8px;
  max-width: 400px;
}

.error-message h3 {
  color: #dc2626;
  margin-bottom: 10px;
}

.retry-btn {
  margin-top: 15px;
  padding: 10px 20px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

/* Breadcrumb */
.breadcrumb {
  margin-bottom: 30px;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
}

.breadcrumb-link {
  color: #3b82f6;
  text-decoration: none;
}

.breadcrumb-link:hover {
  text-decoration: underline;
}

.breadcrumb-separator {
  color: #6b7280;
}

.breadcrumb-current {
  color: #374151;
  font-weight: 500;
}

/* Main Layout */
.item-details-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  margin-top: 20px;
}

/* Images Section */
.item-images-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.main-image-container {
  width: 100%;
  height: 400px;
  border-radius: 12px;
  overflow: hidden;
  background: #f9fafb;
}

.main-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-thumbnails {
  display: flex;
  gap: 10px;
  overflow-x: auto;
  padding: 10px 0;
}

.thumbnail-container {
  flex-shrink: 0;
  width: 80px;
  height: 80px;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  border: 2px solid transparent;
  transition: border-color 0.2s ease;
}

.thumbnail-container.active {
  border-color: #3b82f6;
}

.thumbnail-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Item Info Section */
.item-info-section {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.item-header {
  border-bottom: 1px solid #e5e7eb;
  padding-bottom: 20px;
}

.item-title {
  font-size: 32px;
  font-weight: 700;
  color: #111827;
  margin-bottom: 15px;
  line-height: 1.2;
}

.item-meta {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.item-category,
.item-condition,
.item-year {
  padding: 6px 12px;
  background: #f3f4f6;
  border-radius: 20px;
  font-size: 14px;
  color: #374151;
  font-weight: 500;
}

/* Price Section */
.price-section {
  padding: 20px;
  background: #f8fafc;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.price-info {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 15px;
}

.price-label {
  font-size: 16px;
  color: #6b7280;
}

.price-value {
  font-size: 28px;
  font-weight: 700;
  color: #059669;
}

.negotiable-tag {
  padding: 4px 8px;
  background: #dcfce7;
  color: #166534;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.stock-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.stock-label {
  font-size: 14px;
  color: #6b7280;
}

.stock-value {
  font-size: 14px;
  font-weight: 500;
  color: #059669;
}

.stock-value.low-stock {
  color: #d97706;
}

.stock-value.out-of-stock {
  color: #dc2626;
}

/* Stats Section */
.stats-section {
  display: flex;
  align-items: center;
  gap: 30px;
  padding: 15px 0;
  border-bottom: 1px solid #e5e7eb;
}

.rating-display {
  display: flex;
  align-items: center;
  gap: 10px;
}

.stars {
  display: flex;
  gap: 2px;
}

.star {
  color: #d1d5db;
}

.star.filled {
  color: #fbbf24;
}

.rating-text {
  font-size: 14px;
  color: #6b7280;
}

.sold-info {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: #6b7280;
}

/* Seller Section */
.seller-section {
  padding: 20px;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: #111827;
  margin-bottom: 15px;
}

.seller-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.seller-avatar {
  width: 50px;
  height: 50px;
  background: #f3f4f6;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.seller-details {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.seller-name {
  font-size: 16px;
  font-weight: 600;
  color: #111827;
}

.seller-role {
  font-size: 14px;
  color: #6b7280;
}

.seller-since {
  font-size: 12px;
  color: #9ca3af;
}

/* Description Section */
.description-section {
  padding: 20px;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
}

.description-content p {
  line-height: 1.6;
  color: #374151;
  margin: 0;
}

.no-description {
  color: #9ca3af;
  font-style: italic;
}

/* Tags Section */
.tags-section {
  padding: 20px;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag {
  padding: 6px 12px;
  background: #eff6ff;
  color: #1d4ed8;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
}

/* Action Section */
.action-section {
  display: flex;
  gap: 15px;
  padding-top: 20px;
}

.primary-btn,
.secondary-btn {
  padding: 15px 30px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  justify-content: center;
  min-width: 150px;
}

.primary-btn {
  background: #3b82f6;
  color: white;
  border: none;
}

.primary-btn:hover:not(:disabled) {
  background: #2563eb;
  transform: translateY(-1px);
}

.primary-btn:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

.secondary-btn {
  background: white;
  color: #374151;
  border: 2px solid #d1d5db;
}

.secondary-btn:hover:not(:disabled) {
  border-color: #9ca3af;
  background: #f9fafb;
}

.secondary-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Responsive Design */
@media (max-width: 768px) {
  .item-details-layout {
    grid-template-columns: 1fr;
    gap: 30px;
  }
  
  .item-title {
    font-size: 24px;
  }
  
  .price-value {
    font-size: 24px;
  }
  
  .action-section {
    flex-direction: column;
  }
  
  .primary-btn,
  .secondary-btn {
    width: 100%;
  }
}
</style>