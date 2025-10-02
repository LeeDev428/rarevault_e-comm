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
            
            <!-- Condition Section -->
            <div class="condition-section">
              <h3 class="section-title">Condition</h3>
              <div v-if="item.condition" class="condition-rating">
                <span class="condition-text">{{ formatCondition(item.condition || item.condition_status) }}</span>
              </div>
              <div v-else class="no-ratings">
                <span class="no-ratings-text">No condition specified</span>
              </div>
            </div>

            <!-- Item Statistics Section - Box Layout -->
            <div class="item-statistics">
              <h3 class="section-title">Item Statistics</h3>
              <div class="stats-grid">
                <div class="stat-box">
                  <span class="stat-number">{{ item.views || 0 }}</span>
                  <span class="stat-text">Views</span>
                </div>
                <div class="stat-box">
                  <span class="stat-number">{{ item.favorites || 0 }}</span>
                  <span class="stat-text">Favorites</span>
                </div>
                <div class="stat-box">
                  <span class="stat-number">{{ item.inquiries || 0 }}</span>
                  <span class="stat-text">Inquiries</span>
                </div>
                <div class="stat-box">
                  <span class="stat-number">{{ formatEngagement(item.engagement) }}%</span>
                  <span class="stat-text">Engagement</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Right Side - Item Information -->
          <div class="item-info-section">
            <!-- Price and Description Section -->
            <div class="price-description-section">
              <div class="item-price">₱{{ formatPrice(item.price || 0) }}</div>
              <h3 class="section-title">Description</h3>
              <div class="description-content">
                <p v-if="item.description">{{ item.description }}</p>
                <p v-else class="no-description">No description provided for this item.</p>
              </div>
            </div>

            <!-- Details Section - Compact Box Layout -->
            <div class="details-section">
              <h3 class="section-title">Details</h3>
              <div class="details-box-grid">
                <div class="detail-box">
                  <span class="detail-label">Category</span>
                  <span class="detail-value">{{ formatCategoryName(item.category) }}</span>
                </div>
                <div class="detail-box">
                  <span class="detail-label">Authentication</span>
                  <span class="detail-value" :class="{ 'authenticated': item.isAuthenticated, 'not-authenticated': !item.isAuthenticated }">
                    {{ item.isAuthenticated ? 'Verified' : 'Not verified' }}
                  </span>
                </div>
                <div class="detail-box">
                  <span class="detail-label">Year</span>
                  <span class="detail-value">{{ item.year || 'Not specified' }}</span>
                </div>
                <div class="detail-box">
                  <span class="detail-label">Stock</span>
                  <span class="detail-value" :class="{ 'low-stock': (item.stock || 0) < 5, 'out-of-stock': (item.stock || 0) === 0 }">
                    {{ (item.stock || 0) > 0 ? `${item.stock} available` : 'Out of stock' }}
                  </span>
                </div>
                <div v-if="item.isNegotiable" class="detail-box negotiable-box">
                  <span class="detail-label">Price</span>
                  <span class="detail-value negotiable">Negotiable</span>
                </div>
              </div>
              
              <!-- Tags Section -->
              <div v-if="item.tags && parseTags(item.tags).length > 0" class="tags-section">
                <span class="tags-label">Tags:</span>
                <div class="tags-container">
                  <span 
                    v-for="tag in parseTags(item.tags)" 
                    :key="tag"
                    class="tag-item"
                  >
                    {{ tag }}
                  </span>
                </div>
              </div>
              
              <!-- Listing Info -->
              <div class="listing-info">
                <div class="info-item">
                  <span class="info-label">Listed:</span>
                  <span class="info-value">{{ formatDateShort(item.created_at) }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">Updated:</span>
                  <span class="info-value">{{ formatDateShort(item.updated_at) }}</span>
                </div>
              </div>
            </div>

            <!-- Map Section -->
            <div class="map-section">
              <h3 class="section-title">Location</h3>
              <div class="map-container">
                <div id="seller-map" class="seller-map"></div>
                <p v-if="sellerProfile?.address" class="address-text">{{ sellerProfile.address }}</p>
                <p v-else class="address-text">Silangan, Calauan, Laguna</p>
              </div>
            </div>

            <!-- Wishlist Section -->
            <div class="wishlist-section">
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
    await this.checkWishlistStatus();
    
    // Always initialize map, even if seller profile fails to load
    this.$nextTick(() => {
      console.log('🗺️ Initializing map from mounted()');
      this.initMap();
    });
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
        console.log('🏪 Fetching seller profile for seller ID:', sellerId);
        const response = await axios.get(`http://localhost:5000/api/seller/profile/${sellerId}`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        })
        console.log('🏪 Seller profile response:', response.data);
        this.sellerProfile = response.data
        console.log('🏪 Seller profile set:', this.sellerProfile);
        
        // Initialize map after seller profile is loaded
        this.$nextTick(() => {
          console.log('⏭️ Calling initMap from fetchSellerProfile');
          this.initMap();
        });
      } catch (error) {
        console.error('❌ Error fetching seller profile:', error)
        console.error('❌ Full error details:', error.response);
        // Try fallback: create a mock seller profile with address for testing
        this.sellerProfile = {
          address: 'Silangan, Calauan, Laguna',
          business_name: 'Seller Location'
        };
        console.log('🔄 Using fallback seller profile for map');
        this.$nextTick(() => {
          this.initMap();
        });
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

    parseTags(tags) {
      if (!tags) return []
      
      // Handle if tags is already an array
      if (Array.isArray(tags)) {
        return tags
      }
      
      // Handle if tags is a JSON string
      try {
        const parsed = JSON.parse(tags)
        return Array.isArray(parsed) ? parsed : []
      } catch (error) {
        console.warn('Failed to parse tags:', error)
        return []
      }
    },

    formatEngagement(engagement) {
      if (!engagement) return '0.00'
      return parseFloat(engagement).toFixed(2)
    },

    formatDate(dateString) {
      if (!dateString) return 'Not available'
      
      try {
        const date = new Date(dateString)
        return date.toLocaleDateString('en-US', {
          year: 'numeric',
          month: 'long',
          day: 'numeric'
        })
      } catch (error) {
        console.warn('Failed to format date:', error)
        return 'Invalid date'
      }
    },

    formatDateShort(dateString) {
      if (!dateString) return 'N/A'
      
      try {
        const date = new Date(dateString)
        return date.toLocaleDateString('en-US', {
          month: 'short',
          day: 'numeric',
          year: 'numeric'
        })
      } catch (error) {
        return 'N/A'
      }
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
      console.log('🗺️ initMap called');
      console.log('sellerProfile:', this.sellerProfile);
      
      // Use seller profile address or fallback to default
      const address = this.sellerProfile?.address || 'Silangan, Calauan, Laguna';
      console.log('Using address:', address);

      try {
        console.log('⏳ Waiting for DOM element...');
        // Wait for the DOM element to be available
        await this.$nextTick();
        
        const mapElement = document.getElementById('seller-map');
        console.log('🎯 Map element found:', !!mapElement);
        if (!mapElement) {
          console.warn('❌ Map element not found');
          return;
        }

        console.log('🌍 Starting geocoding for:', address);
        // Geocode the address to get coordinates
        const coordinates = await this.geocodeAddress(address);
        console.log('📍 Coordinates obtained:', coordinates);
        
        if (coordinates) {
          console.log('🗺️ Initializing Leaflet map...');
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
                <strong>${this.sellerProfile?.business_name || 'Seller Location'}</strong><br>
                ${address}
              </div>
            `);
          
          console.log('✅ Map initialized successfully!');
        }
      } catch (error) {
        console.error('❌ Error initializing map:', error);
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

/* Condition Section */
.condition-section {
  background: white;
  border-radius: 8px;
  padding: 20px;
  border: 1px solid #e5e7eb;
  margin-top: 15px;
}

.condition-rating {
  display: flex;
  align-items: center;
  gap: 10px;
}

.condition-text {
  font-size: 16px;
  font-weight: 600;
  color: #059669;
  padding: 8px 16px;
  background: #ecfdf5;
  border-radius: 20px;
  border: 1px solid #d1fae5;
}

.no-ratings {
  text-align: center;
  padding: 20px;
}

.no-ratings-text {
  color: #9ca3af;
  font-style: italic;
  font-size: 14px;
}

/* Item Statistics Section */
.item-statistics {
  background: white;
  border-radius: 8px;
  padding: 20px;
  border: 1px solid #e5e7eb;
  margin-top: 15px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
}

.stat-box {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  text-align: center;
  border: 1px solid #e9ecef;
}

.stat-number {
  display: block;
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 4px;
}

.stat-text {
  font-size: 12px;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Right Side - Item Information */
.item-info-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* Price and Description Section */
.price-description-section {
  background: white;
  border-radius: 8px;
  padding: 20px;
  border: 1px solid #e5e7eb;
}

.item-price {
  font-size: 32px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 20px;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 15px 0;
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

/* Details Section - Professional Box Layout */
.details-section {
  background: white;
  border-radius: 8px;
  padding: 20px;
  border: 1px solid #e5e7eb;
}

.details-box-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-bottom: 20px;
}

.detail-box {
  background: #fafbfc;
  padding: 16px;
  border-radius: 8px;
  border: 1px solid #e1e5e9;
  display: flex;
  flex-direction: column;
  gap: 6px;
  transition: all 0.2s ease;
}

.detail-box:hover {
  background: #f0f4f8;
  border-color: #cbd5e1;
}

.detail-box.negotiable-box {
  background: #f0fdf4;
  border-color: #bbf7d0;
}

.detail-box.negotiable-box:hover {
  background: #ecfdf5;
  border-color: #86efac;
}

.detail-label {
  font-size: 12px;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  margin-bottom: 2px;
}

.detail-value {
  font-size: 15px;
  font-weight: 600;
  color: #1e293b;
  line-height: 1.3;
}

.detail-value.negotiable {
  color: #059669;
  font-weight: 700;
}

.detail-value.low-stock {
  color: #f59e0b;
}

.detail-value.out-of-stock {
  color: #dc2626;
}

.detail-value.authenticated {
  color: #059669;
}

.detail-value.not-authenticated {
  color: #f59e0b;
}

/* Tags Section */
.tags-section {
  margin-bottom: 20px;
  padding: 16px;
  background: #fafbfc;
  border-radius: 8px;
  border: 1px solid #e1e5e9;
}

.tags-label {
  font-size: 13px;
  font-weight: 600;
  color: #64748b;
  margin-bottom: 10px;
  display: block;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag-item {
  padding: 6px 12px;
  background: #e0f2fe;
  color: #0369a1;
  border-radius: 16px;
  font-size: 13px;
  font-weight: 500;
  border: 1px solid #bae6fd;
  transition: all 0.2s ease;
}

.tag-item:hover {
  background: #0284c7;
  color: white;
  transform: translateY(-1px);
}

/* Listing Info */
.listing-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background: #f8fafc;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
  text-align: center;
}

.info-label {
  font-size: 11px;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.8px;
}

.info-value {
  font-size: 14px;
  font-weight: 600;
  color: #334155;
}

/* Map Section */
.map-section {
  background: white;
  border-radius: 8px;
  padding: 20px;
  border: 1px solid #e5e7eb;
}

.map-container {
  height: 200px;
  width: 100%;
  margin-bottom: 10px;
}

.seller-map {
  height: 100%;
  width: 100%;
  border-radius: 6px;
}

.address-text {
  margin: 10px 0 0 0;
  font-size: 14px;
  color: #6b7280;
  text-align: center;
}

.no-map-container {
  padding: 40px 20px;
  text-align: center;
  background: #f9fafb;
  border-radius: 6px;
}

.no-map-text {
  margin: 0 0 10px 0;
  color: #6b7280;
  font-size: 14px;
}

.debug-info {
  margin: 0;
  font-size: 12px;
  color: #9ca3af;
  font-family: monospace;
}

/* Wishlist Section */
.wishlist-section {
  background: white;
  border-radius: 8px;
  padding: 20px;
  border: 1px solid #e5e7eb;
}

.wishlist-btn {
  width: 100%;
  padding: 15px 20px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  background: #3b82f6;
  color: white;
  box-shadow: 0 2px 4px rgba(59, 130, 246, 0.2);
}

.wishlist-btn:hover:not(:disabled) {
  background: #2563eb;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(59, 130, 246, 0.3);
}

.wishlist-btn.in-wishlist {
  background: #dc2626;
  box-shadow: 0 2px 4px rgba(220, 38, 38, 0.2);
}

.wishlist-btn.in-wishlist:hover:not(:disabled) {
  background: #b91c1c;
  box-shadow: 0 4px 8px rgba(220, 38, 38, 0.3);
}

.wishlist-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
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
  
  .wishlist-btn {
    font-size: 14px;
    padding: 12px 16px;
  }
  
  .details-box-grid {
    grid-template-columns: 1fr;
    gap: 10px;
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
  }
  
  .listing-info {
    flex-direction: column;
    gap: 10px;
    align-items: flex-start;
  }
  
  .image-thumbnails {
    flex-wrap: wrap;
  }
  
  .tags-container {
    gap: 4px;
  }
  
  .tag-item {
    font-size: 10px;
    padding: 3px 8px;
  }
  
  .item-price {
    font-size: 24px;
  }
}
</style>