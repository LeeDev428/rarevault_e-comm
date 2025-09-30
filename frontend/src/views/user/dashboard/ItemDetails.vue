<template>
  <UserLayout>
    <div class="item-details-container">
      <div class="back-navigation">
        <button @click="goBack" class="back-btn">
          <i class="back-icon">←</i>
          Back to Dashboard
        </button>
      </div>

      <div v-if="loading" class="loading-state">
        <div class="loading-spinner"></div>
        <p>Loading item details...</p>
      </div>

      <div v-else-if="error" class="error-state">
        <div class="error-message">
          <i class="error-icon">⚠️</i>
          <h3>Error Loading Item</h3>
          <p>{{ error }}</p>
          <button @click="fetchItem" class="retry-btn">Try Again</button>
        </div>
      </div>

      <div v-else-if="item" class="item-details">
        <!-- Item Images -->
        <div class="item-images">
          <div class="main-image">
            <img :src="currentImage" :alt="item.title" @error="handleImageError">
          </div>
          <div class="thumbnail-images" v-if="item.images && item.images.length > 1">
            <div 
              v-for="(image, index) in item.images" 
              :key="index"
              class="thumbnail"
              :class="{ active: currentImageIndex === index }"
              @click="selectImage(index)"
            >
              <img :src="image" :alt="`${item.title} image ${index + 1}`" @error="handleImageError">
            </div>
          </div>
        </div>

        <!-- Item Information -->
        <div class="item-info">
          <div class="item-header">
            <h1 class="item-title">{{ item.title }}</h1>
            <div class="item-price">₱{{ formatPrice(item.price) }}</div>
          </div>

          <div class="item-meta">
            <div class="meta-item">
              <span class="meta-label">Category:</span>
              <span class="meta-value">{{ formatCategoryName(item.category) }}</span>
            </div>
            <div class="meta-item">
              <span class="meta-label">Condition:</span>
              <span class="meta-value">{{ item.condition }}</span>
            </div>
            <div class="meta-item">
              <span class="meta-label">Seller:</span>
              <span class="meta-value">{{ item.seller_name || 'Unknown' }}</span>
            </div>
            <div class="meta-item" v-if="item.average_rating">
              <span class="meta-label">Rating:</span>
              <div class="rating-display">
                <div class="stars">
                  <span 
                    v-for="n in 5" 
                    :key="n"
                    class="star"
                    :class="{ filled: n <= Math.round(item.average_rating) }"
                  >
                    ★
                  </span>
                </div>
                <span class="rating-text">{{ item.average_rating.toFixed(1) }}</span>
              </div>
            </div>
            <div class="meta-item" v-if="item.sold_count">
              <span class="meta-label">Sold:</span>
              <span class="meta-value">{{ item.sold_count }} times</span>
            </div>
          </div>

          <div class="item-description">
            <h3>Description</h3>
            <p>{{ item.description || 'No description available.' }}</p>
          </div>

          <div class="item-actions">
            <button 
              @click="addToCart" 
              class="action-btn primary"
              :disabled="item.stock <= 0"
            >
              <i class="btn-icon">🛒</i>
              {{ item.stock <= 0 ? 'Out of Stock' : 'Add to Cart' }}
            </button>
            <button @click="addToWishlist" class="action-btn secondary">
              <i class="btn-icon">❤️</i>
              Add to Wishlist
            </button>
          </div>
        </div>
      </div>
    </div>
  </UserLayout>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import UserLayout from '@/components/user/UserLayout.vue'

export default {
  name: 'ItemDetails',
  components: {
    UserLayout
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    
    const item = ref(null)
    const loading = ref(true)
    const error = ref(null)
    const currentImageIndex = ref(0)
    
    const itemId = computed(() => route.params.id)
    
    const currentImage = computed(() => {
      if (!item.value?.images?.length) return '/uploads/placeholder.svg'
      return item.value.images[currentImageIndex.value] || '/uploads/placeholder.svg'
    })
    
    const fetchItem = async () => {
      try {
        loading.value = true
        error.value = null
        
        const token = localStorage.getItem('access_token')
        if (!token) {
          router.push('/login')
          return
        }
        
        const response = await fetch(`/api/items/${itemId.value}`, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })
        
        if (!response.ok) {
          throw new Error(`Failed to fetch item: ${response.statusText}`)
        }
        
        const data = await response.json()
        item.value = data
        
      } catch (err) {
        console.error('Error fetching item:', err)
        error.value = err.message || 'Failed to load item details'
      } finally {
        loading.value = false
      }
    }
    
    const goBack = () => {
      router.go(-1)
    }
    
    const selectImage = (index) => {
      currentImageIndex.value = index
    }
    
    const handleImageError = (event) => {
      event.target.src = '/uploads/placeholder.svg'
    }
    
    const formatPrice = (price) => {
      return new Intl.NumberFormat('en-PH').format(price)
    }
    
    const formatCategoryName = (category) => {
      return category
        .split('_')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ')
    }
    
    const addToCart = async () => {
      try {
        const token = localStorage.getItem('access_token')
        if (!token) {
          router.push('/login')
          return
        }
        
        // Implement add to cart functionality
        console.log('Adding to cart:', item.value.id)
        // You would typically make an API call here
        
      } catch (err) {
        console.error('Error adding to cart:', err)
      }
    }
    
    const addToWishlist = async () => {
      try {
        const token = localStorage.getItem('access_token')
        if (!token) {
          router.push('/login')
          return
        }
        
        // Implement add to wishlist functionality
        console.log('Adding to wishlist:', item.value.id)
        // You would typically make an API call here
        
      } catch (err) {
        console.error('Error adding to wishlist:', err)
      }
    }
    
    onMounted(() => {
      fetchItem()
    })
    
    return {
      item,
      loading,
      error,
      currentImage,
      currentImageIndex,
      fetchItem,
      goBack,
      selectImage,
      handleImageError,
      formatPrice,
      formatCategoryName,
      addToCart,
      addToWishlist
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400;1,500;1,600;1,700;1,800&family=Inter:wght@300;400;500;600;700&display=swap');

.item-title {
  font-family: 'Playfair Display', serif;
  font-style: italic;
  font-weight: 700;
  font-size: 2rem;
  letter-spacing: -1px;
  color: #1f2937;
}

.section-title {
  font-family: 'Playfair Display', serif;
  font-style: italic;
  font-weight: 600;
  font-size: 1.5rem;
  letter-spacing: -0.5px;
  color: #1f2937;
}

.item-details-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.back-navigation {
  margin-bottom: 20px;
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  color: #495057;
  text-decoration: none;
  transition: all 0.2s;
  cursor: pointer;
}

.back-btn:hover {
  background: #e9ecef;
  color: #212529;
}

.back-icon {
  font-size: 18px;
}

.loading-state,
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  text-align: center;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #007bff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-message {
  max-width: 400px;
}

.error-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.retry-btn {
  padding: 10px 20px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  margin-top: 16px;
}

.retry-btn:hover {
  background: #0056b3;
}

.item-details {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  align-items: start;
}

.item-images {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.main-image {
  aspect-ratio: 1;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.main-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.thumbnail-images {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.thumbnail {
  width: 80px;
  height: 80px;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  border: 2px solid transparent;
  transition: border-color 0.2s;
}

.thumbnail.active {
  border-color: #007bff;
}

.thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.item-info {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.item-header {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.item-title {
  font-size: 2rem;
  font-weight: 700;
  color: #212529;
  margin: 0;
}

.item-price {
  font-size: 1.75rem;
  font-weight: 600;
  color: #007bff;
}

.item-meta {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.meta-label {
  font-weight: 600;
  color: #6c757d;
  min-width: 80px;
}

.meta-value {
  color: #212529;
}

.rating-display {
  display: flex;
  align-items: center;
  gap: 8px;
}

.stars {
  display: flex;
  gap: 2px;
}

.star {
  color: #ddd;
  font-size: 16px;
  transition: color 0.2s;
}

.star.filled {
  color: #ffc107;
}

.rating-text {
  font-size: 14px;
  color: #6c757d;
}

.item-description h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #212529;
  margin-bottom: 12px;
}

.item-description p {
  color: #6c757d;
  line-height: 1.6;
}

.item-actions {
  display: flex;
  gap: 16px;
}

.action-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 14px 24px;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

.action-btn.primary {
  background: #007bff;
  color: white;
}

.action-btn.primary:hover:not(:disabled) {
  background: #0056b3;
}

.action-btn.secondary {
  background: #f8f9fa;
  color: #495057;
  border: 1px solid #dee2e6;
}

.action-btn.secondary:hover {
  background: #e9ecef;
}

.btn-icon {
  font-size: 18px;
}

@media (max-width: 768px) {
  .item-details {
    grid-template-columns: 1fr;
    gap: 24px;
  }
  
  .item-title {
    font-size: 1.5rem;
  }
  
  .item-price {
    font-size: 1.5rem;
  }
  
  .item-actions {
    flex-direction: column;
  }
}
</style>
