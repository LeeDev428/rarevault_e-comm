<template>
  <SellerLayout>
    <div class="ratings-container">
      <!-- Header -->
      <div class="ratings-header">
        <div class="header-content">
          <h1 class="page-title">Product Ratings & Reviews</h1>
          <p class="page-subtitle">Monitor customer feedback and improve your products</p>
        </div>
        
        <!-- Stats Overview -->
        <div class="ratings-stats">
          <div class="stat-card">
            <div class="stat-value">{{ overallRating }}</div>
            <div class="stat-label">Average Rating</div>
            <div class="stars-display">
              <span v-for="star in 5" :key="star" 
                    :class="['star', { filled: star <= Math.round(overallRating) }]">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z"/>
                </svg>
              </span>
            </div>
          </div>
          
          <div class="stat-card">
            <div class="stat-value">{{ totalRatings }}</div>
            <div class="stat-label">Total Reviews</div>
          </div>
          
          <div class="stat-card">
            <div class="stat-value">{{ responseRate }}%</div>
            <div class="stat-label">Response Rate</div>
          </div>
        </div>
      </div>

      <!-- Filters -->
      <div class="ratings-filters">
        <div class="filter-group">
          <label for="itemFilter">Filter by Item</label>
          <select id="itemFilter" v-model="selectedItem" @change="filterRatings">
            <option value="">All Items</option>
            <option v-for="item in sellerItems" :key="item.id" :value="item.id">
              {{ item.title }}
            </option>
          </select>
        </div>

        <div class="filter-group">
          <label for="ratingFilter">Filter by Rating</label>
          <select id="ratingFilter" v-model="selectedRating" @change="filterRatings">
            <option value="">All Ratings</option>
            <option value="5">5 Stars</option>
            <option value="4">4 Stars</option>
            <option value="3">3 Stars</option>
            <option value="2">2 Stars</option>
            <option value="1">1 Star</option>
          </select>
        </div>

        <div class="filter-group">
          <label for="sortBy">Sort by</label>
          <select id="sortBy" v-model="sortBy" @change="filterRatings">
            <option value="newest">Newest First</option>
            <option value="oldest">Oldest First</option>
            <option value="highest">Highest Rating</option>
            <option value="lowest">Lowest Rating</option>
          </select>
        </div>

        <div class="search-group">
          <input type="text" v-model="searchQuery" @input="filterRatings" 
                 placeholder="Search reviews..." class="search-input">
        </div>
      </div>

      <!-- Ratings Table -->
      <div class="ratings-table-container">
        <div v-if="loading" class="loading-state">
          <div class="loading-spinner"></div>
          <p>Loading ratings...</p>
        </div>

        <div v-else-if="filteredRatings.length === 0" class="empty-state">
          <div class="empty-icon">
            <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <circle cx="12" cy="12" r="10"/>
              <path d="M8 14s1.5 2 4 2 4-2 4-2"/>
              <line x1="9" y1="9" x2="9.01" y2="9"/>
              <line x1="15" y1="9" x2="15.01" y2="9"/>
            </svg>
          </div>
          <h3>No ratings found</h3>
          <p>{{ selectedItem || selectedRating ? 'No ratings match your current filters.' : 'Your products haven\'t received any ratings yet.' }}</p>
        </div>

        <div v-else class="ratings-table">
          <div class="table-header">
            <div class="header-cell">Customer</div>
            <div class="header-cell">Product</div>
            <div class="header-cell">Rating</div>
            <div class="header-cell">Review</div>
            <div class="header-cell">Date</div>
            <div class="header-cell">Actions</div>
          </div>

          <div v-for="rating in paginatedRatings" :key="rating.id" class="table-row">
            <div class="table-cell customer-cell">
              <div class="customer-info">
                <div class="customer-avatar">
                  <img :src="getCustomerAvatar(rating.user)" :alt="rating.user?.username || 'Anonymous'" />
                </div>
                <div class="customer-details">
                  <div class="customer-name">{{ rating.user?.username || 'Anonymous' }}</div>
                  <div class="customer-email">{{ rating.user?.email || 'N/A' }}</div>
                </div>
              </div>
            </div>

            <div class="table-cell product-cell">
              <div class="product-info">
                <img :src="getProductImage(rating.item)" :alt="rating.item?.title" class="product-image" />
                <div class="product-details">
                  <div class="product-title">{{ rating.item?.title }}</div>
                  <div class="product-price">₱{{ rating.item?.price?.toFixed(2) }}</div>
                </div>
              </div>
            </div>

            <div class="table-cell rating-cell">
              <div class="rating-value">
                <div class="stars">
                  <span v-for="star in 5" :key="star" 
                        :class="['star', { filled: star <= rating.rating }]">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z"/>
                    </svg>
                  </span>
                </div>
                <div class="rating-number">{{ rating.rating }}/5</div>
              </div>
            </div>

            <div class="table-cell review-cell">
              <div class="review-content">
                <div v-if="rating.review" class="review-text">
                  <p :class="{ 'expanded': rating.expanded }">{{ rating.review }}</p>
                  <button v-if="rating.review.length > 150" 
                          @click="rating.expanded = !rating.expanded" 
                          class="expand-btn">
                    {{ rating.expanded ? 'Show less' : 'Show more' }}
                  </button>
                </div>
                <div v-else class="no-review">No written review</div>
                
                <!-- Rating Photos -->
                <div v-if="rating.photos && rating.photos.length > 0" class="review-photos">
                  <div v-for="(photo, index) in rating.photos" :key="index" class="photo-thumbnail">
                    <img :src="photo" :alt="`Review photo ${index + 1}`" 
                         @click="openPhotoModal(rating.photos, index)" />
                  </div>
                </div>
              </div>
            </div>

            <div class="table-cell date-cell">
              <div class="date-info">
                <div class="date">{{ formatDate(rating.created_at) }}</div>
                <div class="time">{{ formatTime(rating.created_at) }}</div>
              </div>
            </div>

            <div class="table-cell actions-cell">
              <div class="action-buttons">
                <button @click="respondToReview(rating)" class="action-btn respond-btn">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                    <polyline points="7,10 12,15 17,10"/>
                    <line x1="12" y1="15" x2="12" y2="3"/>
                  </svg>
                  Respond
                </button>
                <button @click="reportReview(rating)" class="action-btn report-btn">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <circle cx="12" cy="12" r="10"/>
                    <line x1="12" y1="8" x2="12" y2="12"/>
                    <line x1="12" y1="16" x2="12.01" y2="16"/>
                  </svg>
                  Report
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Pagination -->
        <div v-if="filteredRatings.length > ratingsPerPage" class="pagination">
          <button @click="currentPage = Math.max(1, currentPage - 1)" 
                  :disabled="currentPage === 1" class="page-btn">
            Previous
          </button>
          <span class="page-info">
            Page {{ currentPage }} of {{ totalPages }}
          </span>
          <button @click="currentPage = Math.min(totalPages, currentPage + 1)" 
                  :disabled="currentPage === totalPages" class="page-btn">
            Next
          </button>
        </div>
      </div>
    </div>

    <!-- Photo Modal -->
    <div v-if="photoModal.show" class="photo-modal" @click="closePhotoModal">
      <div class="modal-content" @click.stop>
        <button @click="closePhotoModal" class="modal-close">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <line x1="18" y1="6" x2="6" y2="18"/>
            <line x1="6" y1="6" x2="18" y2="18"/>
          </svg>
        </button>
        <img :src="photoModal.photos[photoModal.currentIndex]" alt="Review photo" />
        <div class="modal-nav" v-if="photoModal.photos.length > 1">
          <button @click="previousPhoto" class="nav-btn">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <polyline points="15,18 9,12 15,6"/>
            </svg>
          </button>
          <span>{{ photoModal.currentIndex + 1 }} / {{ photoModal.photos.length }}</span>
          <button @click="nextPhoto" class="nav-btn">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <polyline points="9,18 15,12 9,6"/>
            </svg>
          </button>
        </div>
      </div>
    </div>
  </SellerLayout>
</template>

<script>
import SellerLayout from '@/components/seller/SellerLayout.vue'

export default {
  name: 'SellerRatings',
  components: {
    SellerLayout
  },
  data() {
    return {
      ratings: [],
      filteredRatings: [],
      sellerItems: [],
      loading: true,
      selectedItem: '',
      selectedRating: '',
      sortBy: 'newest',
      searchQuery: '',
      currentPage: 1,
      ratingsPerPage: 10,
      photoModal: {
        show: false,
        photos: [],
        currentIndex: 0
      }
    }
  },
  computed: {
    overallRating() {
      if (this.ratings.length === 0) return 0
      const sum = this.ratings.reduce((total, rating) => total + rating.rating, 0)
      return (sum / this.ratings.length).toFixed(1)
    },

    totalRatings() {
      return this.ratings.length
    },

    responseRate() {
      // Placeholder calculation - you can implement actual response rate logic
      return 85
    },

    totalPages() {
      return Math.ceil(this.filteredRatings.length / this.ratingsPerPage)
    },

    paginatedRatings() {
      const start = (this.currentPage - 1) * this.ratingsPerPage
      const end = start + this.ratingsPerPage
      return this.filteredRatings.slice(start, end)
    }
  },
  mounted() {
    this.fetchRatings()
    this.fetchSellerItems()
  },
  methods: {
    async fetchRatings() {
      try {
        this.loading = true
        const token = localStorage.getItem('access_token') || localStorage.getItem('token')
        if (!token) {
          console.error('No authentication token found')
          this.$router.push('/login')
          return
        }

        console.log('Fetching ratings with token:', token ? 'Token exists' : 'No token')
        const response = await fetch('http://localhost:5000/api/seller/ratings', {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })

        console.log('Ratings API response status:', response.status)
        
        if (response.ok) {
          const data = await response.json()
          console.log('Ratings data received:', data)
          this.ratings = data.ratings || []
          this.filteredRatings = [...this.ratings]
          
          // Update statistics
          if (data.statistics) {
            this.overallRating = data.statistics.average_rating || 0
            this.totalRatings = data.statistics.total_ratings || 0
          }
        } else {
          const errorData = await response.json().catch(() => ({}))
          console.error('Error response from ratings API:', errorData)
          throw new Error(errorData.error || 'Failed to fetch ratings')
        }
      } catch (error) {
        console.error('Error fetching ratings:', error)
        this.ratings = []
        this.filteredRatings = []
      } finally {
        this.loading = false
      }
    },

    async fetchSellerItems() {
      try {
        const token = localStorage.getItem('access_token') || localStorage.getItem('token')
        if (!token) return

        const response = await fetch('http://localhost:5000/api/seller/items', {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })

        if (response.ok) {
          const data = await response.json()
          this.sellerItems = data.items || []
        }
      } catch (error) {
        console.error('Error fetching seller items:', error)
      }
    },

    filterRatings() {
      let filtered = [...this.ratings]

      // Filter by item
      if (this.selectedItem) {
        filtered = filtered.filter(rating => rating.item_id == this.selectedItem)
      }

      // Filter by rating
      if (this.selectedRating) {
        filtered = filtered.filter(rating => rating.rating == this.selectedRating)
      }

      // Search in reviews
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        filtered = filtered.filter(rating =>
          rating.review?.toLowerCase().includes(query) ||
          rating.user?.username?.toLowerCase().includes(query) ||
          rating.item?.title?.toLowerCase().includes(query)
        )
      }

      // Sort
      filtered.sort((a, b) => {
        switch (this.sortBy) {
          case 'newest':
            return new Date(b.created_at) - new Date(a.created_at)
          case 'oldest':
            return new Date(a.created_at) - new Date(b.created_at)
          case 'highest':
            return b.rating - a.rating
          case 'lowest':
            return a.rating - b.rating
          default:
            return 0
        }
      })

      this.filteredRatings = filtered
      this.currentPage = 1
    },

    getRatingPercentage(rating) {
      if (this.ratings.length === 0) return 0
      const count = this.ratings.filter(r => r.rating === rating).length
      return (count / this.ratings.length) * 100
    },

    getRatingCount(rating) {
      return this.ratings.filter(r => r.rating === rating).length
    },

    getCustomerAvatar(user) {
      return user?.profile_image || `https://ui-avatars.com/api/?name=${user?.username || 'A'}&background=3b82f6&color=fff`
    },

    getProductImage(item) {
      if (item?.primary_image?.url) {
        return item.primary_image.url
      }
      if (item?.images && item.images.length > 0) {
        return item.images[0].url || item.images[0]
      }
      return 'http://localhost:5000/uploads/placeholder.svg'
    },

    formatDate(dateString) {
      if (!dateString) return 'N/A'
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    },

    formatTime(dateString) {
      if (!dateString) return 'N/A'
      const date = new Date(dateString)
      return date.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit'
      })
    },

    openPhotoModal(photos, index) {
      this.photoModal = {
        show: true,
        photos: photos,
        currentIndex: index
      }
    },

    closePhotoModal() {
      this.photoModal.show = false
    },

    previousPhoto() {
      if (this.photoModal.currentIndex > 0) {
        this.photoModal.currentIndex--
      }
    },

    nextPhoto() {
      if (this.photoModal.currentIndex < this.photoModal.photos.length - 1) {
        this.photoModal.currentIndex++
      }
    },

    respondToReview(rating) {
      // Implement response to review functionality
      console.log('Respond to review:', rating.id)
      alert('Response feature coming soon!')
    },

    reportReview(rating) {
      // Implement report review functionality
      console.log('Report review:', rating.id)
      alert('Report feature coming soon!')
    }
  }
}
</script>

<style scoped>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

.ratings-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 32px;
  font-family: 'Inter', sans-serif;
}

/* Header */
.ratings-header {
  margin-bottom: 32px;
  padding: 0 0 24px;
  background: transparent;
  border-radius: 0;
  border: none;
  border-bottom: 1px solid #e5e7eb;
  box-shadow: none;
}

.header-content {
  margin-bottom: 24px;
}

.page-title {
  font-family: 'Inter', sans-serif;
  font-size: 28px;
  font-weight: 700;
  color: #000000;
  margin: 0 0 4px 0;
  letter-spacing: -0.5px;
  text-shadow: none;
}

.page-subtitle {
  font-size: 14px;
  color: #6b7280;
  font-weight: 400;
  margin: 0;
}

/* Stats */
.ratings-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.stat-card {
  background: #ffffff;
  padding: 24px;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  text-align: center;
  transition: box-shadow 0.2s ease;
}

.stat-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.stat-value {
  font-family: 'Inter', sans-serif;
  font-size: 32px;
  font-weight: 700;
  color: #000000;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 13px;
  color: #6b7280;
  font-weight: 500;
  margin-bottom: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stars-display {
  display: flex;
  justify-content: center;
  gap: 4px;
}

.stars-display .star {
  color: #e5e7eb;
  transition: color 0.2s ease;
}

.stars-display .star.filled {
  color: #000000;
}

/* Filters */
.ratings-filters {
  background: #ffffff;
  padding: 24px;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  margin-bottom: 24px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  align-items: end;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.filter-group label {
  font-size: 14px;
  font-weight: 500;
  color: #000000;
}

.filter-group select,
.search-input {
  padding: 10px 16px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  font-family: 'Inter', sans-serif;
  background: #ffffff;
  color: #111827;
  transition: all 0.2s ease;
  font-weight: 500;
}

.filter-group select:focus,
.search-input:focus {
  outline: none;
  border-color: #000000;
  box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.05);
  background: #ffffff;
}

.search-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

/* Table */
.ratings-table-container {
  background: #ffffff;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.ratings-table {
  display: flex;
  flex-direction: column;
}

.table-header {
  display: grid;
  grid-template-columns: 200px 250px 120px 1fr 120px 140px;
  gap: 20px;
  padding: 20px 32px;
  background: #f9fafb;
  border-bottom: 1px solid #e5e7eb;
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  color: #111827;
  font-size: 14px;
}

.table-row {
  display: grid;
  grid-template-columns: 200px 250px 120px 1fr 120px 140px;
  gap: 20px;
  padding: 20px 32px;
  border-bottom: 1px solid #f3f4f6;
  transition: all 0.2s ease;
}

.table-row:hover {
  background: #f9fafb;
}

.table-row:last-child {
  border-bottom: none;
}

.table-cell {
  display: flex;
  align-items: flex-start;
  font-size: 14px;
  color: #374151;
}

/* Customer Cell */
.customer-info {
  display: flex;
  align-items: center;
  gap: 16px;
}

.customer-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  overflow: hidden;
  border: 2px solid #e5e7eb;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.customer-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.customer-name {
  font-weight: 600;
  color: #111827;
  margin-bottom: 2px;
}

.customer-email {
  font-size: 12px;
  color: #6b7280;
  opacity: 1;
}

/* Product Cell */
.product-info {
  display: flex;
  align-items: center;
  gap: 16px;
}

.product-image {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  object-fit: cover;
  border: 1px solid #e5e7eb;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.product-title {
  font-weight: 600;
  color: #111827;
  margin-bottom: 4px;
  line-height: 1.3;
}

.product-price {
  font-size: 12px;
  color: #6b7280;
  opacity: 1;
  font-weight: 600;
}

/* Rating Cell */
.rating-value {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.stars {
  display: flex;
  gap: 4px;
}

.star {
  color: #d4af94;
  transition: color 0.3s ease;
}

.star.filled {
  color: #daa520;
}

.rating-number {
  font-size: 12px;
  font-weight: 600;
  color: #111827;
}

/* Review Cell */
.review-content {
  max-width: 100%;
}

.review-text p {
  margin: 0 0 8px 0;
  line-height: 1.5;
  color: #374151;
  opacity: 1;
}

.expand-btn {
  background: none;
  border: none;
  color: #000000;
  cursor: pointer;
  font-size: 12px;
  text-decoration: underline;
  font-weight: 500;
}

.expand-btn:hover {
  opacity: 0.7;
}

.no-review {
  color: #9ca3af;
  opacity: 1;
  font-style: italic;
}

.review-photos {
  display: flex;
  gap: 8px;
  margin-top: 12px;
  flex-wrap: wrap;
}

.photo-thumbnail {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s ease;
  border: 1px solid #e5e7eb;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.photo-thumbnail:hover {
  transform: scale(1.05);
}

.photo-thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Date Cell */
.date-info {
  text-align: center;
}

.date {
  font-weight: 600;
  color: #111827;
  margin-bottom: 2px;
}

.time {
  font-size: 12px;
  color: #6b7280;
  opacity: 1;
}

/* Actions Cell */
.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.action-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 10px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 6px;
  font-family: 'Inter', sans-serif;
}

.respond-btn {
  background: #f9fafb;
  color: #000000;
  border: 1px solid #e5e7eb;
}

.respond-btn:hover {
  background: #ffffff;
  border-color: #000000;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.report-btn {
  background: #fef2f2;
  color: #991b1b;
  border: 1px solid #fecaca;
}

.report-btn:hover {
  background: #fee2e2;
  border-color: #dc2626;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(220, 38, 38, 0.1);
}

/* Loading and Empty States */
.loading-state,
.empty-state {
  padding: 80px 48px;
  text-align: center;
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #f3f4f6;
  border-top: 4px solid #000000;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px auto;
}

.empty-icon {
  color: #9ca3af;
  opacity: 1;
  margin-bottom: 20px;
}

.empty-state h3 {
  font-family: 'Inter', sans-serif;
  font-size: 18px;
  font-weight: 600;
  color: #111827;
  margin: 0 0 8px 0;
}

.empty-state p {
  color: #6b7280;
  opacity: 1;
  margin: 0;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Pagination */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  padding: 24px;
  border-top: 1px solid #d4af94;
}

.page-btn {
  padding: 12px 20px;
  border: 1px solid #d4af94;
  background: linear-gradient(135deg, #f8f6f1 0%, #e8ddd4 100%);
  color: #8b5a3c;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'Inter', sans-serif;
}

.page-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #e8ddd4 0%, #d4af94 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(139, 90, 60, 0.2);
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  font-size: 14px;
  color: #8b5a3c;
  opacity: 0.8;
}

/* Photo Modal */
.photo-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(139, 90, 60, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}

.modal-content {
  position: relative;
  max-width: 90vw;
  max-height: 90vh;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(139, 90, 60, 0.4);
}

.modal-content img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.modal-close {
  position: absolute;
  top: 20px;
  right: 20px;
  width: 44px;
  height: 44px;
  border: none;
  background: rgba(139, 90, 60, 0.8);
  color: white;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  font-size: 18px;
}

.modal-close:hover {
  background: rgba(139, 90, 60, 1);
  transform: scale(1.1);
}

.modal-nav {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  gap: 20px;
  background: rgba(139, 90, 60, 0.9);
  padding: 12px 20px;
  border-radius: 25px;
  color: white;
  font-size: 14px;
  font-family: 'Inter', sans-serif;
}

.nav-btn {
  width: 36px;
  height: 36px;
  border: none;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.nav-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: scale(1.1);
}

/* Responsive */
@media (max-width: 1200px) {
  .table-header,
  .table-row {
    grid-template-columns: 180px 220px 100px 1fr 100px 120px;
    padding: 20px 24px;
    gap: 16px;
  }
}

@media (max-width: 968px) {
  .ratings-container {
    padding: 24px;
  }
  
  .ratings-header {
    padding: 24px;
  }
  
  .ratings-filters {
    grid-template-columns: 1fr;
    padding: 24px;
  }
  
  .table-header,
  .table-row {
    grid-template-columns: 1fr;
    gap: 16px;
    padding: 20px 24px;
  }
  
  .table-cell {
    border-bottom: 1px solid rgba(212, 175, 148, 0.3);
    padding-bottom: 16px;
  }
  
  .table-cell:last-child {
    border-bottom: none;
  }
  
  .action-buttons {
    flex-direction: row;
  }
  
  .page-title {
    font-size: 28px;
  }
}

@media (max-width: 640px) {
  .ratings-stats {
    grid-template-columns: 1fr;
  }
  
  .customer-info,
  .product-info {
    flex-direction: column;
    text-align: center;
    gap: 12px;
  }
  
  .stat-card {
    padding: 24px;
  }
  
  .stat-value {
    font-size: 32px;
  }
}
</style>
