<template>
  <UserLayout>
    <div class="ratings-container">
      <div class="ratings-header">
        <button @click="$router.go(-1)" class="back-btn">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M19 12H5M12 19l-7-7 7-7"/>
          </svg>
          Back to Orders
        </button>
        <h1 class="page-title">Rate Your Purchase</h1>
        <p class="page-subtitle">Share your experience with other customers</p>
      </div>

      <div class="rating-card" v-if="orderData">
        <!-- Item Information -->
        <div class="item-section">
          <div class="item-info">
            <img :src="getItemImage()" :alt="orderData.itemTitle" class="item-image" />
            <div class="item-details">
              <h3 class="item-title">{{ orderData.itemTitle }}</h3>
              <p class="order-info">Order #{{ orderData.orderId }}</p>
              <p class="seller-info">Sold by {{ sellerName }}</p>
            </div>
          </div>
        </div>

        <!-- Rating Form -->
        <form @submit.prevent="submitRating" class="rating-form">
          <!-- Star Rating -->
          <div class="rating-section">
            <label class="rating-label">Overall Rating *</label>
            <div class="star-rating">
              <button
                v-for="star in 5"
                :key="star"
                type="button"
                @click="setRating(star)"
                @mouseover="hoverRating = star"
                @mouseleave="hoverRating = 0"
                :class="['star-btn', { 
                  'filled': star <= (hoverRating || rating),
                  'hover': star <= hoverRating
                }]"
              >
                <svg width="32" height="32" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z"/>
                </svg>
              </button>
            </div>
            <p class="rating-text">{{ getRatingText() }}</p>
          </div>

          <!-- Written Review (Optional) -->
          <div class="review-section">
            <label for="review" class="review-label">Write a Review (Optional)</label>
            <textarea
              id="review"
              v-model="review"
              placeholder="Share your experience with this product. What did you like or dislike? Would you recommend it to others?"
              class="review-textarea"
              maxlength="500"
            ></textarea>
            <p class="character-count">{{ review.length }}/500 characters</p>
          </div>

          <!-- Photo Upload (Optional) -->
          <div class="photo-section">
            <label class="photo-label">Add Photos (Optional)</label>
            <div class="photo-upload">
              <input
                ref="fileInput"
                type="file"
                multiple
                accept="image/*"
                @change="handleFileUpload"
                class="file-input"
              />
              <button type="button" @click="$refs.fileInput.click()" class="upload-btn">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M21 15V19A2 2 0 0 1 19 21H5A2 2 0 0 1 3 19V15"/>
                  <polyline points="7,10 12,15 17,10"/>
                  <line x1="12" y1="15" x2="12" y2="3"/>
                </svg>
                Choose Photos
              </button>
              <span class="upload-text">or drag and drop images here</span>
            </div>
            
            <!-- Preview uploaded photos -->
            <div v-if="uploadedPhotos.length > 0" class="photo-preview">
              <div v-for="(photo, index) in uploadedPhotos" :key="index" class="photo-item">
                <img :src="photo.preview" :alt="`Photo ${index + 1}`" class="preview-image" />
                <button type="button" @click="removePhoto(index)" class="remove-photo">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <line x1="18" y1="6" x2="6" y2="18"/>
                    <line x1="6" y1="6" x2="18" y2="18"/>
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="form-actions">
            <button type="button" @click="skipRating" class="skip-btn">
              Skip for Now
            </button>
            <button type="submit" :disabled="!rating || submitting" class="submit-btn">
              <span v-if="submitting" class="loading-spinner"></span>
              {{ submitting ? 'Submitting...' : 'Submit Rating' }}
            </button>
          </div>
        </form>
      </div>

      <!-- Loading State -->
      <div v-else class="loading-state">
        <div class="loading-spinner large"></div>
        <p>Loading order details...</p>
      </div>
    </div>
  </UserLayout>
</template>

<script>
import UserLayout from '@/components/user/UserLayout.vue'

export default {
  name: 'UserRatings',
  components: {
    UserLayout
  },
  data() {
    return {
      rating: 0,
      hoverRating: 0,
      review: '',
      uploadedPhotos: [],
      orderData: null,
      sellerName: '',
      submitting: false
    }
  },
  mounted() {
    this.loadOrderData()
  },
  methods: {
    loadOrderData() {
      const query = this.$route.query
      this.orderData = {
        orderId: query.orderId,
        itemId: query.itemId,
        itemTitle: query.itemTitle,
        sellerId: query.sellerId
      }
      
      // You might want to fetch additional order details here
      this.fetchOrderDetails()
    },

    async fetchOrderDetails() {
      try {
        const token = localStorage.getItem('access_token') || localStorage.getItem('token')
        if (!token) {
          this.$router.push('/login')
          return
        }

        // Fetch order details to get seller name and item image
        const response = await fetch(`http://localhost:5000/api/user/orders/${this.orderData.orderId}`, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })

        if (response.ok) {
          const data = await response.json()
          this.sellerName = data.order?.item?.seller?.username || 'Unknown Seller'
        }
      } catch (error) {
        console.error('Error fetching order details:', error)
        this.sellerName = 'Unknown Seller'
      }
    },

    setRating(star) {
      this.rating = star
    },

    getRatingText() {
      const texts = {
        1: 'Poor - Very dissatisfied',
        2: 'Fair - Somewhat dissatisfied', 
        3: 'Good - Satisfied',
        4: 'Very Good - Very satisfied',
        5: 'Excellent - Extremely satisfied'
      }
      return this.rating > 0 ? texts[this.rating] : 'Select a rating'
    },

    getItemImage() {
      // Return placeholder for now, you can enhance this to fetch actual item image
      return 'http://localhost:5000/uploads/placeholder.svg'
    },

    handleFileUpload(event) {
      const files = Array.from(event.target.files)
      
      files.forEach(file => {
        if (file.type.startsWith('image/') && this.uploadedPhotos.length < 5) {
          const reader = new FileReader()
          reader.onload = (e) => {
            this.uploadedPhotos.push({
              file: file,
              preview: e.target.result
            })
          }
          reader.readAsDataURL(file)
        }
      })
    },

    removePhoto(index) {
      this.uploadedPhotos.splice(index, 1)
    },

    async submitRating() {
      if (!this.rating) {
        alert('Please select a rating before submitting')
        return
      }

      this.submitting = true

      try {
        const token = localStorage.getItem('access_token') || localStorage.getItem('token')
        if (!token) {
          this.$router.push('/login')
          return
        }

        const formData = new FormData()
        formData.append('orderId', this.orderData.orderId)
        formData.append('itemId', this.orderData.itemId)
        formData.append('rating', this.rating)
        formData.append('review', this.review)
        formData.append('sellerId', this.orderData.sellerId)

        // Add photos if any
        this.uploadedPhotos.forEach((photo, index) => {
          formData.append(`photos`, photo.file)
        })

        const response = await fetch('http://localhost:5000/api/user/ratings', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`
          },
          body: formData
        })

        if (response.ok) {
          alert('Thank you for your rating!')
          this.$router.push('/user/orders')
        } else {
          throw new Error('Failed to submit rating')
        }
      } catch (error) {
        console.error('Error submitting rating:', error)
        alert('Failed to submit rating. Please try again.')
      } finally {
        this.submitting = false
      }
    },

    skipRating() {
      this.$router.push('/user/orders')
    }
  }
}
</script>

<style scoped>
.ratings-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

/* Header */
.ratings-header {
  text-align: center;
  margin-bottom: 32px;
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  background: none;
  border: none;
  color: #6b7280;
  cursor: pointer;
  padding: 8px;
  margin-bottom: 24px;
  transition: color 0.2s ease;
}

.back-btn:hover {
  color: #374151;
}

.page-title {
  font-size: 32px;
  font-weight: 700;
  color: #111827;
  margin: 0 0 8px 0;
}

.page-subtitle {
  font-size: 16px;
  color: #6b7280;
  margin: 0;
}

/* Rating Card */
.rating-card {
  background: white;
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

/* Item Section */
.item-section {
  border-bottom: 1px solid #e5e7eb;
  padding-bottom: 24px;
  margin-bottom: 32px;
}

.item-info {
  display: flex;
  gap: 20px;
  align-items: center;
}

.item-image {
  width: 80px;
  height: 80px;
  border-radius: 12px;
  object-fit: cover;
}

.item-title {
  font-size: 20px;
  font-weight: 600;
  color: #111827;
  margin: 0 0 8px 0;
}

.order-info {
  font-size: 14px;
  color: #6b7280;
  margin: 0 0 4px 0;
}

.seller-info {
  font-size: 14px;
  color: #6b7280;
  margin: 0;
}

/* Rating Form */
.rating-form {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.rating-section {
  text-align: center;
}

.rating-label {
  display: block;
  font-size: 18px;
  font-weight: 600;
  color: #111827;
  margin-bottom: 16px;
}

.star-rating {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-bottom: 12px;
}

.star-btn {
  background: none;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
  padding: 4px;
  border-radius: 4px;
  color: #d1d5db;
}

.star-btn:hover,
.star-btn.hover {
  color: #fbbf24;
  transform: scale(1.1);
}

.star-btn.filled {
  color: #f59e0b;
}

.rating-text {
  font-size: 16px;
  font-weight: 500;
  color: #374151;
  margin: 0;
}

/* Review Section */
.review-section {
  text-align: left;
}

.review-label {
  display: block;
  font-size: 16px;
  font-weight: 600;
  color: #111827;
  margin-bottom: 12px;
}

.review-textarea {
  width: 100%;
  min-height: 120px;
  padding: 16px;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  font-size: 14px;
  line-height: 1.5;
  resize: vertical;
  transition: border-color 0.2s ease;
}

.review-textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.character-count {
  font-size: 12px;
  color: #9ca3af;
  text-align: right;
  margin: 8px 0 0 0;
}

/* Photo Section */
.photo-section {
  text-align: left;
}

.photo-label {
  display: block;
  font-size: 16px;
  font-weight: 600;
  color: #111827;
  margin-bottom: 12px;
}

.photo-upload {
  border: 2px dashed #d1d5db;
  border-radius: 12px;
  padding: 32px;
  text-align: center;
  transition: border-color 0.2s ease;
}

.photo-upload:hover {
  border-color: #3b82f6;
}

.file-input {
  display: none;
}

.upload-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s ease;
}

.upload-btn:hover {
  background: #2563eb;
}

.upload-text {
  display: block;
  margin-top: 8px;
  font-size: 14px;
  color: #6b7280;
}

.photo-preview {
  display: flex;
  gap: 12px;
  margin-top: 16px;
  flex-wrap: wrap;
}

.photo-item {
  position: relative;
  width: 80px;
  height: 80px;
}

.preview-image {
  width: 100%;
  height: 100%;
  border-radius: 8px;
  object-fit: cover;
}

.remove-photo {
  position: absolute;
  top: -6px;
  right: -6px;
  width: 24px;
  height: 24px;
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.remove-photo:hover {
  background: #dc2626;
}

/* Form Actions */
.form-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
  padding-top: 24px;
  border-top: 1px solid #e5e7eb;
}

.skip-btn {
  padding: 12px 32px;
  background: #f9fafb;
  color: #374151;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.skip-btn:hover {
  background: #f3f4f6;
  border-color: #d1d5db;
}

.submit-btn {
  padding: 12px 32px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.submit-btn:hover:not(:disabled) {
  background: #2563eb;
}

.submit-btn:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

/* Loading States */
.loading-state {
  text-align: center;
  padding: 60px 20px;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid #e5e7eb;
  border-top: 2px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.loading-spinner.large {
  width: 40px;
  height: 40px;
  margin: 0 auto 16px auto;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Responsive */
@media (max-width: 768px) {
  .ratings-container {
    padding: 16px;
  }
  
  .rating-card {
    padding: 24px;
  }
  
  .item-info {
    flex-direction: column;
    text-align: center;
    gap: 16px;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .star-rating {
    gap: 4px;
  }
  
  .star-btn svg {
    width: 28px;
    height: 28px;
  }
}
</style>
