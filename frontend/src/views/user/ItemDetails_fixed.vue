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

        <div class="main-layout">
          <!-- Left Side - Image Gallery -->
          <div class="image-gallery-section">
            <div class="item-title-header">
              <h1 class="item-title">{{ item.title }}</h1>
            </div>
            
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
            <!-- Description Section -->
            <div class="description-section">
              <h3 class="section-title">Description</h3>
              <div class="item-price">₱{{ formatPrice(item.price || 0) }}</div>
              <div class="description-content">
                <p v-if="item.description">{{ item.description }}</p>
                <p v-else class="no-description">No description provided for this item.</p>
              </div>
            </div>

            <!-- Details Section -->
            <div class="details-section">
              <h3 class="section-title">Details</h3>
              <div class="details-grid">
                <div class="detail-row">
                  <div class="detail-item">
                    <span class="detail-label">Condition</span>
                    <span class="detail-value">{{ formatCondition(item.condition || item.condition_status) }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Category</span>
                    <span class="detail-value">{{ formatCategoryName(item.category) }}</span>
                  </div>
                </div>
                <div class="detail-row">
                  <div class="detail-item">
                    <span class="detail-label">Price</span>
                    <span class="detail-value price">₱{{ formatPrice(item.price || 0) }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Stock</span>
                    <span class="detail-value" :class="{ 'low-stock': (item.stock || 0) < 5, 'out-of-stock': (item.stock || 0) === 0 }">
                      {{ (item.stock || 0) > 0 ? `${item.stock} available` : 'Out of stock' }}
                    </span>
                  </div>
                </div>
                <div v-if="item.isNegotiable" class="detail-row">
                  <div class="detail-item">
                    <span class="detail-label">Negotiable</span>
                    <span class="detail-value negotiable">Yes</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Map Section -->
            <div v-if="sellerProfile?.address" class="map-section">
              <div class="map-container">
                <div id="seller-map" class="seller-map"></div>
              </div>
            </div>

            <!-- Message Section -->
            <div class="message-section">
              <h3 class="section-title">Send seller a message</h3>
              <div class="message-input-container">
                <textarea 
                  v-model="messageText"
                  placeholder="Is this available?"
                  class="message-input"
                  rows="3"
                ></textarea>
              </div>
              <div class="action-buttons">
                <button 
                  @click="sendMessage"
                  :disabled="!messageText.trim() || isSendingMessage"
                  class="send-btn"
                >
                  {{ isSendingMessage ? 'SENDING...' : 'SEND' }}
                </button>
                <button 
                  @click="toggleWishlist"
                  :disabled="isAddingToWishlist"
                  class="wishlist-btn"
                  :class="{ 'in-wishlist': isInWishlist }"
                >
                  {{ isInWishlist ? 'REMOVE FROM WISHLIST' : 'ADD TO WISHLIST' }}
                </button>
              </div>
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
      :loading="orderLoading"
      @close="showOrderModal = false"
      @submit="handleOrderSubmit"
    />
  </UserLayout>
</template>

<script>
import UserLayout from '@/components/user/UserLayout.vue'
import ConfirmOrderModal from '@/components/user/ConfirmOrderModal.vue'
import axios from 'axios'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

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
      isAddingToWishlist: false,
      orderLoading: false,
      map: null,
      isInWishlist: false,
      messageText: '',
      isSendingMessage: false
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
    },
    
    sellerInitials() {
      if (!this.seller?.first_name || !this.seller?.last_name) {
        return 'S'
      }
      return `${this.seller.first_name.charAt(0)}${this.seller.last_name.charAt(0)}`.toUpperCase()
    }
  },
  async mounted() {
    await this.fetchItemDetails();
    
    // Initialize map after seller profile is loaded
    if (this.sellerProfile) {
      this.initMap();
    }
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
        
        // Fetch seller profile with additional details
        await this.fetchSellerProfile(sellerId)
      } catch (error) {
        console.error('Error fetching seller details:', error)
        // Don't show error, seller info is optional
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
        
        // Initialize map after seller profile is loaded
        this.$nextTick(() => {
          this.initMap();
        });
      } catch (error) {
        console.error('Error fetching seller profile:', error)
        // Seller profile is optional, don't show error
      }
    },
    
    async checkWishlistStatus() {
      try {
        const response = await axios.get(`http://localhost:5000/api/wishlist/check/${this.item.id}`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token') || localStorage.getItem('token')}`
          }
        });
        this.isInWishlist = response.data.inWishlist;
      } catch (error) {
        console.error('Error checking wishlist status:', error);
        // Don't show error, wishlist status is not critical
      }
    },
    
    async handleOrderSubmit(orderData) {
      try {
        this.orderLoading = true
        
        const response = await axios.post('http://localhost:5000/api/orders', {
          item_id: this.item.id,
          quantity: orderData.quantity,
          notes: orderData.notes
        }, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        })
        
        this.showOrderModal = false
        this.showToast('success', 'Order placed successfully!')
        
        // Optionally redirect to orders page or show confirmation
        setTimeout(() => {
          this.$router.push('/user/orders')
        }, 2000)
        
      } catch (error) {
        console.error('Error placing order:', error)
        this.showToast('error', error.response?.data?.error || 'Failed to place order')
      } finally {
        this.orderLoading = false
      }
    },
    
    getItemImage(item) {
      if (!item) return '/api/placeholder/400/400'
      
      // Try different image properties
      if (item.primary_image?.url) {
        return item.primary_image.url
      } else if (item.primary_image && typeof item.primary_image === 'string') {
        return item.primary_image
      } else if (item.image_url) {
        return item.image_url
      } else if (item.images && item.images.length > 0) {
        return item.images[0].url || item.images[0]
      }
      
      return '/api/placeholder/400/400'
    },
    
    handleImageError(event) {
      console.warn('Image failed to load:', event.target.src)
      event.target.src = '/api/placeholder/400/400'
    },
    
    formatPrice(price) {
      return new Intl.NumberFormat('en-PH', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      }).format(price)
    },
    
    formatCategoryName(category) {
      if (!category) return 'Unknown'
      
      // Handle both object and string formats
      if (typeof category === 'object' && category.name) {
        return category.name
      }
      
      // Handle string format - convert to title case
      return category.toString()
        .split('_')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
        .join(' ')
    },
    
    formatCondition(condition) {
      if (!condition) return 'Unknown'
      
      const conditionMap = {
        'mint': 'Mint',
        'excellent': 'Excellent', 
        'very_good': 'Very Good',
        'good': 'Good',
        'fair': 'Fair',
        'poor': 'Poor',
        'new': 'New',
        'like_new': 'Like New',
        'used': 'Used'
      }
      
      return conditionMap[condition] || condition.charAt(0).toUpperCase() + condition.slice(1)
    },
    
    showToast(type, message) {
      // Create toast element
      const toast = document.createElement('div');
      toast.className = `toast ${type}`;
      toast.textContent = message;
      
      // Add to page
      document.body.appendChild(toast);
      
      // Remove after 3 seconds
      setTimeout(() => {
        if (toast.parentNode) {
          toast.parentNode.removeChild(toast);
        }
      }, 3000);
    },

    async sendMessage() {
      if (!this.messageText.trim()) return;
      
      try {
        this.isSendingMessage = true;
        
        await axios.post('http://localhost:5000/api/messages', {
          seller_id: this.item.seller_id,
          item_id: this.item.id,
          message: this.messageText.trim()
        }, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token') || localStorage.getItem('token')}`
          }
        });
        
        this.messageText = '';
        this.showToast('success', 'Message sent successfully');
      } catch (error) {
        console.error('Error sending message:', error);
        this.showToast('error', 'Failed to send message');
      } finally {
        this.isSendingMessage = false;
      }
    },

    async toggleWishlist() {
      try {
        this.isAddingToWishlist = true;
        
        if (this.isInWishlist) {
          // Remove from wishlist
          await axios.delete(`http://localhost:5000/api/wishlist/${this.item.id}`, {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('access_token') || localStorage.getItem('token')}`
            }
          });
          this.isInWishlist = false;
          this.showToast('success', 'Removed from wishlist');
        } else {
          // Add to wishlist
          await axios.post(`http://localhost:5000/api/wishlist`, {
            item_id: this.item.id
          }, {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('access_token') || localStorage.getItem('token')}`
            }
          });
          this.isInWishlist = true;
          this.showToast('success', 'Added to wishlist');
        }
      } catch (error) {
        console.error('Error toggling wishlist:', error);
        this.showToast('error', 'Failed to update wishlist');
      } finally {
        this.isAddingToWishlist = false;
      }
    },

    async initMap() {
      if (!this.sellerProfile?.address) return;

      try {
        // Wait for the DOM element to be available
        await this.$nextTick();
        
        const mapElement = document.getElementById('seller-map');
        if (!mapElement) {
          console.warn('Map element not found');
          return;
        }

        // Geocode the address to get coordinates
        const coordinates = await this.geocodeAddress(this.sellerProfile.address);
        
        if (coordinates) {
          // Initialize the map
          this.map = L.map('seller-map').setView([coordinates.lat, coordinates.lng], 13);

          // Add tile layer
          L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors'
          }).addTo(this.map);

          // Add marker for seller location
          L.marker([coordinates.lat, coordinates.lng])
            .addTo(this.map)
            .bindPopup(`
              <div>
                <strong>${this.sellerProfile.business_name || 'Seller Location'}</strong><br>
                ${this.sellerProfile.address}
              </div>
            `);
        }
      } catch (error) {
        console.error('Error initializing map:', error);
      }
    },

    async geocodeAddress(address) {
      try {
        // Use Nominatim API for geocoding (free OpenStreetMap service)
        const response = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(address)}&limit=1`);
        const data = await response.json();
        
        if (data && data.length > 0) {
          return {
            lat: parseFloat(data[0].lat),
            lng: parseFloat(data[0].lon)
          };
        }
        
        // Fallback to Philippines center if geocoding fails
        console.warn('Could not geocode address, using default location');
        return {
          lat: 14.5995,  // Manila coordinates as fallback
          lng: 120.9842
        };
      } catch (error) {
        console.error('Geocoding error:', error);
        // Fallback to Philippines center
        return {
          lat: 14.5995,
          lng: 120.9842
        };
      }
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400;1,500;1,600;1,700;1,800&family=Inter:wght@300;400;500;600;700&display=swap');

.item-details-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

/* Breadcrumb */
.breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 20px;
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
  color: #9ca3af;
}

.breadcrumb-current {
  color: #6b7280;
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
  color: #dc2626;
}

.retry-btn {
  margin-top: 20px;
  padding: 10px 20px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

/* Main Layout - Matches the image exactly */
.main-layout {
  display: grid;
  grid-template-columns: 1fr 350px;
  gap: 30px;
  max-width: 1200px;
  margin: 0 auto;
}

/* Left Side - Image Gallery */
.image-gallery-section {
  background: white;
  border-radius: 8px;
  overflow: hidden;
}

.item-title-header {
  padding: 20px 20px 15px 20px;
  border-bottom: 1px solid #e5e7eb;
}

.item-title {
  font-size: 24px;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
  line-height: 1.3;
}

.main-image-container {
  background: #f8f9fa;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 400px;
}

.main-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  border-radius: 4px;
}

.image-thumbnails {
  display: flex;
  gap: 8px;
  padding: 15px 20px;
  background: #f8f9fa;
  border-top: 1px solid #e5e7eb;
}

.thumbnail-container {
  width: 60px;
  height: 60px;
  border-radius: 4px;
  overflow: hidden;
  cursor: pointer;
  border: 2px solid transparent;
  transition: border-color 0.2s;
}

.thumbnail-container:hover,
.thumbnail-container.active {
  border-color: #3b82f6;
}

.thumbnail-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Right Side - Item Information */
.item-info-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* Description Section */
.description-section {
  background: white;
  border-radius: 8px;
  padding: 20px;
  border: 1px solid #e5e7eb;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 15px 0;
}

.item-price {
  font-size: 16px;
  font-weight: 600;
  color: #059669;
  margin-bottom: 15px;
}

.description-content {
  color: #374151;
  line-height: 1.6;
}

.description-content p {
  margin: 0;
}

.no-description {
  color: #9ca3af;
  font-style: italic;
}

/* Details Section */
.details-section {
  background: white;
  border-radius: 8px;
  padding: 20px;
  border: 1px solid #e5e7eb;
}

.details-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.detail-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.detail-label {
  font-size: 12px;
  font-weight: 500;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.detail-value {
  font-size: 14px;
  font-weight: 600;
  color: #1f2937;
}

.detail-value.price {
  color: #059669;
}

.detail-value.negotiable {
  color: #3b82f6;
}

.detail-value.low-stock {
  color: #f59e0b;
}

.detail-value.out-of-stock {
  color: #dc2626;
}

/* Map Section */
.map-section {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #e5e7eb;
}

.map-container {
  height: 200px;
  width: 100%;
}

.seller-map {
  height: 100%;
  width: 100%;
}

/* Message Section */
.message-section {
  background: white;
  border-radius: 8px;
  padding: 20px;
  border: 1px solid #e5e7eb;
}

.message-input-container {
  margin-bottom: 15px;
}

.message-input {
  width: 100%;
  padding: 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 14px;
  font-family: inherit;
  resize: vertical;
  min-height: 80px;
}

.message-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.message-input::placeholder {
  color: #9ca3af;
}

/* Action Buttons */
.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.send-btn,
.wishlist-btn {
  width: 100%;
  padding: 12px 20px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.send-btn {
  background: #1f2937;
  color: white;
}

.send-btn:hover:not(:disabled) {
  background: #111827;
}

.send-btn:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

.wishlist-btn {
  background: #3b82f6;
  color: white;
}

.wishlist-btn:hover:not(:disabled) {
  background: #2563eb;
}

.wishlist-btn.in-wishlist {
  background: #dc2626;
}

.wishlist-btn.in-wishlist:hover:not(:disabled) {
  background: #b91c1c;
}

.wishlist-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Toast notifications */
.toast {
  position: fixed;
  top: 20px;
  right: 20px;
  padding: 12px 20px;
  border-radius: 6px;
  color: white;
  font-weight: 500;
  z-index: 1000;
  animation: slideIn 0.3s ease-out;
}

.toast.success {
  background: #059669;
}

.toast.error {
  background: #dc2626;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

/* Responsive Design */
@media (max-width: 768px) {
  .main-layout {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .item-details-container {
    padding: 15px;
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  .detail-row {
    grid-template-columns: 1fr;
  }
  
  .image-thumbnails {
    flex-wrap: wrap;
  }
}
</style>