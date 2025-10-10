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
          <router-link to="/user/dashboard" class="breadcrumb-link">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
            </svg>
            Home
          </router-link>
          <span class="breadcrumb-separator">/</span>
          <span class="breadcrumb-current">{{ item.title }}</span>
        </nav>

        <div class="modern-layout">
          <!-- Left Side - Image Gallery -->
          <div class="gallery-section">
            <!-- Main Image with Modern Frame -->
            <div class="main-image-wrapper">
              <img 
                :src="selectedImage || getItemImage(item)" 
                :alt="item.title"
                class="main-image"
                @error="handleImageError"
              >
            </div>
            
            <!-- Image Thumbnails - Compact -->
            <div v-if="itemImages.length > 1" class="image-thumbnails">
              <div 
                v-for="(image, index) in itemImages" 
                :key="image.id || index"
                class="thumbnail-item"
                :class="{ 'active': selectedImage === image.url }"
                @click="selectedImage = image.url"
              >
                <img 
                  :src="image.url" 
                  :alt="`View ${index + 1}`"
                  class="thumbnail-img"
                >
              </div>
            </div>

            <!-- Condition & Statistics Combined Card -->
            <div class="info-card-compact">
              <!-- Condition Row -->
              <div class="compact-row">
                <span class="compact-label">CONDITION</span>
                <div class="compact-value">
                  <span class="status-dot"></span>
                  {{ formatCondition(item.condition || item.condition_status) }}
                </div>
              </div>

              <!-- Statistics Grid - Compact -->
              <div class="stats-grid-compact">
                <div class="stat-item-compact">
                  <div class="stat-value">{{ item.views || 0 }}</div>
                  <div class="stat-name">Views</div>
                </div>
                <div class="stat-item-compact">
                  <div class="stat-value">{{ item.favorites || 0 }}</div>
                  <div class="stat-name">Favorites</div>
                </div>
                <div class="stat-item-compact">
                  <div class="stat-value">{{ item.inquiries || 0 }}</div>
                  <div class="stat-name">Inquiries</div>
                </div>
                <div class="stat-item-compact">
                  <div class="stat-value">{{ formatEngagement(item.engagement) }}%</div>
                  <div class="stat-name">Engagement</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Right Side - Item Information -->
          <div class="info-section">
            <!-- Title & Price - Clean Header -->
            <div class="product-header">
              <h1 class="product-title">{{ item.title }}</h1>
              <div class="product-price">₱{{ formatPrice(item.price || 0) }}</div>
              <div v-if="item.isNegotiable" class="negotiable-tag">Price Negotiable</div>
            </div>

            <!-- Description - Minimal Card -->
            <div class="detail-card">
              <div class="card-label">DESCRIPTION</div>
              <p v-if="item.description" class="detail-text">{{ item.description }}</p>
              <p v-else class="detail-text muted">No description provided.</p>
            </div>

            <!-- Details - Clean List -->
            <div class="detail-card">
              <div class="card-label">DETAILS</div>
              <div class="detail-list">
                <div class="detail-item">
                  <span class="item-label">Category</span>
                  <span class="item-value">{{ formatCategoryName(item.category) }}</span>
                </div>
                <div class="detail-item">
                  <span class="item-label">Authentication</span>
                  <span class="item-value" :class="{ 'verified-text': item.isAuthenticated }">
                    {{ item.isAuthenticated ? '✓ Verified' : 'Not verified' }}
                  </span>
                </div>
                <div class="detail-item">
                  <span class="item-label">Year</span>
                  <span class="item-value">{{ item.year || 'Not specified' }}</span>
                </div>
                <div class="detail-item">
                  <span class="item-label">Stock</span>
                  <span class="item-value" :class="{ 'warning-text': (item.stock || 0) < 5, 'error-text': (item.stock || 0) === 0 }">
                    {{ (item.stock || 0) > 0 ? `${item.stock} available` : 'Out of stock' }}
                  </span>
                </div>
              </div>
              
              <!-- Tags - Minimal Pills -->
              <div v-if="item.tags && parseTags(item.tags).length > 0" class="tags-row">
                <span 
                  v-for="tag in parseTags(item.tags)" 
                  :key="tag"
                  class="tag-pill"
                >
                  {{ tag }}
                </span>
              </div>
            </div>

            <!-- Location - Compact Card -->
            <div class="detail-card">
              <div class="card-label">LOCATION</div>
              <div class="map-compact">
                <div id="seller-map" class="map-embed"></div>
              </div>
              <div class="location-text">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                  <circle cx="12" cy="10" r="3"></circle>
                </svg>
                {{ sellerProfile?.address || 'Silangan, Calauan, Laguna' }}
              </div>
              <div class="meta-row">
                <span class="meta-text">Listed {{ formatDateShort(item.created_at) }}</span>
                <span class="meta-separator">•</span>
                <span class="meta-text">Updated {{ formatDateShort(item.updated_at) }}</span>
              </div>
            </div>

            <!-- Action Buttons - Minimalist -->
            <div class="action-bar">
              <button 
                @click="toggleWishlist"
                :disabled="isAddingToWishlist"
                class="action-btn btn-outline"
                :class="{ 'active': isInWishlist }"
              >
                <svg width="18" height="18" viewBox="0 0 24 24" :fill="isInWishlist ? 'currentColor' : 'none'" stroke="currentColor" stroke-width="2">
                  <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
                </svg>
                {{ isInWishlist ? 'Saved' : 'Save' }}
              </button>

              <button 
                class="action-btn btn-primary"
                @click="messageSellerAction"
              >
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                </svg>
                Message Seller
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
        const token = localStorage.getItem('access_token') || localStorage.getItem('token');
        if (!token) {
          console.log('No token, skipping wishlist check');
          this.isInWishlist = false;
          return;
        }
        
        console.log('🔍 Checking wishlist status for item:', this.item.id);
        const response = await axios.get(`http://localhost:5000/api/user/wishlist/check/${this.item.id}`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        
        console.log('Wishlist check response:', response.data);
        this.isInWishlist = response.data.inWishlist;
        console.log('Is in wishlist:', this.isInWishlist);
      } catch (error) {
        console.error('Error checking wishlist status:', error);
        // Don't show error, wishlist status is not critical
        this.isInWishlist = false;
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

    messageSellerAction() {
      // Navigate to messages page with seller context
      if (!this.item?.seller_id) {
        this.showToast('error', 'Seller information not available');
        return;
      }
      
      this.$router.push({
        path: '/user/messages',
        query: { 
          sellerId: this.item.seller_id,
          itemId: this.item.id 
        }
      });
    },

    async toggleWishlist() {
      try {
        console.log('🔄 toggleWishlist called');
        console.log('Current item:', this.item);
        console.log('Item ID:', this.item.id);
        console.log('Is in wishlist:', this.isInWishlist);
        
        this.isAddingToWishlist = true;
        
        const token = localStorage.getItem('access_token') || localStorage.getItem('token');
        console.log('Token found:', token ? 'Yes' : 'No');
        
        if (!token) {
          console.log('❌ No token found, redirecting to login');
          this.showToast('error', 'Please login to save items');
          this.$router.push('/login');
          return;
        }
        
        if (this.isInWishlist) {
          // Remove from wishlist
          console.log('🗑️ Removing from wishlist...');
          const response = await fetch(`http://localhost:5000/api/user/wishlist/${this.item.id}`, {
            method: 'DELETE',
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
            }
          });
          
          console.log('Remove response status:', response.status);
          const responseData = await response.json();
          console.log('Remove response data:', responseData);
          
          if (!response.ok) {
            throw new Error(responseData.error || 'Failed to remove from wishlist');
          }
          
          this.isInWishlist = false;
          this.showToast('success', responseData.message || 'Removed from wishlist');
          console.log('✅ Successfully removed from wishlist');
        } else {
          // Add to wishlist
          console.log('💾 Adding to wishlist...');
          const response = await fetch(`http://localhost:5000/api/user/wishlist/${this.item.id}`, {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
            }
          });
          
          console.log('Add response status:', response.status);
          const responseData = await response.json();
          console.log('Add response data:', responseData);
          
          if (!response.ok) {
            throw new Error(responseData.error || 'Failed to add to wishlist');
          }
          
          this.isInWishlist = true;
          this.showToast('success', responseData.message || 'Added to wishlist');
          console.log('✅ Successfully added to wishlist');
          console.log('Wishlist ID:', responseData.wishlist_id);
        }
      } catch (error) {
        console.error('❌ Error toggling wishlist:', error);
        console.error('Error details:', error.message);
        this.showToast('error', error.message || 'Failed to update wishlist');
      } finally {
        this.isAddingToWishlist = false;
        console.log('🏁 toggleWishlist finished');
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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

.item-details-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem 1.5rem;
  background: #f9fafb;
  min-height: 100vh;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Breadcrumb - Modern minimalist style */
.breadcrumb {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 2rem;
  font-size: 0.875rem;
  color: #6b7280;
}

.breadcrumb-link {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  color: #111827;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}

.breadcrumb-link:hover {
  color: #000;
}

.breadcrumb-link svg {
  width: 16px;
  height: 16px;
}

.breadcrumb-separator {
  color: #d1d5db;
  font-weight: 300;
}

.breadcrumb-current {
  color: #6b7280;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 300px;
}

/* Loading and Error States */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 500px;
  gap: 1.25rem;
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 3px solid #e5e7eb;
  border-top: 3px solid #111827;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 500px;
  padding: 2rem;
}

.error-message {
  text-align: center;
  padding: 3rem;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  color: #111827;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.retry-btn {
  margin-top: 1.5rem;
  padding: 0.75rem 1.5rem;
  background: #111827;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.retry-btn:hover {
  background: #000;
}

/* Modern Layout - Two Column Grid */
.modern-layout {
  display: grid;
  grid-template-columns: 1.2fr 400px;
  gap: 1.5rem;
  align-items: start;
}

/* Gallery Section - Left Side */
.gallery-section {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

/* Main Image - Clean Minimal */
.main-image-wrapper {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #e5e7eb;
}

.main-image {
  width: 100%;
  height: 450px;
  object-fit: cover;
  display: block;
}

/* Image Thumbnails - Compact */
.image-thumbnails {
  display: flex;
  gap: 0.5rem;
  overflow-x: auto;
}

.thumbnail-item {
  flex-shrink: 0;
  width: 60px;
  height: 60px;
  border-radius: 4px;
  overflow: hidden;
  cursor: pointer;
  border: 2px solid #e5e7eb;
  transition: all 0.15s;
  background: white;
}

.thumbnail-item:hover {
  border-color: #9ca3af;
}

.thumbnail-item.active {
  border-color: #111827;
}

.thumbnail-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Info Card Compact - Combined Condition & Stats */
.info-card-compact {
  background: white;
  border-radius: 8px;
  padding: 1rem;
  border: 1px solid #e5e7eb;
}

.compact-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 0.875rem;
  margin-bottom: 0.875rem;
  border-bottom: 1px solid #f3f4f6;
}

.compact-label {
  font-size: 0.688rem;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.compact-value {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: #111827;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #10b981;
}

/* Stats Grid - Compact */
.stats-grid-compact {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.75rem;
}

.stat-item-compact {
  text-align: center;
}

.stat-value {
  display: block;
  font-size: 1.125rem;
  font-weight: 700;
  color: #111827;
  margin-bottom: 0.125rem;
}

.stat-name {
  font-size: 0.688rem;
  font-weight: 500;
  color: #6b7280;
}

/* Info Section - Right Side */
.info-section {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

/* Product Header - Clean & Minimal */
.product-header {
  background: white;
  border-radius: 8px;
  padding: 1.25rem;
  border: 1px solid #e5e7eb;
}

.product-title {
  font-size: 0.9rem;
  font-weight: 700;
  color: #111827;
  margin: 0 0 0.75rem 0;
  line-height: 1.3;
}

.product-price {
  font-size: 1.1rem;
  font-weight: 700;
  color: #111827;
  letter-spacing: -0.02em;
}

.negotiable-tag {
  display: inline-block;
  margin-top: 0.5rem;
  padding: 0.25rem 0.625rem;
  background: #ecfdf5;
  color: #10b981;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
}

/* Detail Cards - Minimalist */
.detail-card {
  background: white;
  border-radius: 8px;
  padding: 1.25rem;
  border: 1px solid #e5e7eb;
}

.card-label {
  font-size: 0.688rem;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.875rem;
}

.detail-text {
  color: #374151;
  line-height: 1.6;
  font-size: 0.875rem;
  margin: 0;
}

.detail-text.muted {
  color: #9ca3af;
  font-style: italic;
}

/* Detail List - Clean Rows */
.detail-list {
  display: flex;
  flex-direction: column;
  gap: 0.625rem;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
}

.item-label {
  font-size: 0.813rem;
  color: #6b7280;
  font-weight: 500;
}

.item-value {
  font-size: 0.813rem;
  color: #111827;
  font-weight: 600;
  text-align: right;
}

.item-value.verified-text {
  color: #10b981;
}

.item-value.warning-text {
  color: #f59e0b;
}

.item-value.error-text {
  color: #ef4444;
}

/* Tags Row - Minimal Pills */
.tags-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.375rem;
  margin-top: 0.875rem;
  padding-top: 0.875rem;
  border-top: 1px solid #f3f4f6;
}

.tag-pill {
  padding: 0.25rem 0.625rem;
  background: #f9fafb;
  color: #6b7280;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
}

/* Map Compact */
.map-compact {
  border-radius: 6px;
  overflow: hidden;
  height: 180px;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  margin-bottom: 0.625rem;
}

.map-embed {
  width: 100%;
  height: 100%;
}

.location-text {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  margin: 0 0 0.625rem 0;
  font-size: 0.813rem;
  color: #374151;
}

.location-text svg {
  flex-shrink: 0;
  color: #9ca3af;
}

.meta-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding-top: 0.625rem;
  border-top: 1px solid #f3f4f6;
}

.meta-text {
  font-size: 0.75rem;
  color: #9ca3af;
}

.meta-separator {
  color: #d1d5db;
}

/* Action Bar - Minimalist Buttons */
.action-bar {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.375rem;
  padding: 0.875rem 1.25rem;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
  border: none;
}

.action-btn svg {
  width: 18px;
  height: 18px;
}

.btn-outline {
  background: white;
  color: #111827;
  border: 1.5px solid #e5e7eb;
}

.btn-outline:hover {
  border-color: #9ca3af;
}

.btn-outline.active {
  background: #fef2f2;
  border-color: #ef4444;
  color: #ef4444;
}

.btn-outline:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-primary {
  background: #111827;
  color: white;
  border: 1.5px solid #111827;
}

.btn-primary:hover {
  background: #000;
  border-color: #000;
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
  background: #10b981;
}

.toast.error {
  background: #ef4444;
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
@media (max-width: 1024px) {
  .modern-layout {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .main-image {
    height: 400px;
  }
  
  .stats-grid-compact {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .item-details-container {
    padding: 1rem;
  }
  
  .breadcrumb-current {
    max-width: 180px;
  }
  
  .main-image {
    height: 320px;
  }
  
  .product-title {
    font-size: 0.8rem;
  }
  
  .product-price {
    font-size: 1.625rem;
  }
  
  .action-bar {
    flex-direction: column;
  }
  
  .action-btn {
    width: 100%;
  }
  
  .detail-card,
  .product-header,
  .info-card-compact {
    padding: 1rem;
  }
}

@media (max-width: 480px) {
  .item-details-container {
    padding: 0.75rem;
  }
  
  .main-image {
    height: 280px;
  }
  
  .product-title {
    font-size: 1rem;
  }
  
  .product-price {
    font-size: 1.5rem;
  }
  
  .stat-value {
    font-size: 1rem;
  }
  
  .stat-name {
    font-size: 0.625rem;
  }
  
  .thumbnail-item {
    width: 50px;
    height: 50px;
  }
  
  .action-btn {
    padding: 0.75rem 1rem;
    font-size: 0.813rem;
  }
}
</style>