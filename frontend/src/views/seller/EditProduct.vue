<template>
  <SellerLayout>
    <div class="edit-product">
      <div class="product-form-container">
        <!-- Left Side - User Info and Photo Upload -->
        <div class="left-section">
          <!-- User Profile -->
          <div class="user-profile-section">
            <div class="user-avatar">
              <img :src="userInfo.avatar || 'https://via.placeholder.com/60'" alt="Profile" class="avatar-img" />
            </div>
            <div class="user-info">
              <h3 class="user-name">{{ userInfo.displayName }}</h3>
              <p class="listing-type">Editing product</p>
            </div>
          </div>

          <!-- Photo Upload Area -->
          <div class="photo-upload-section">
            <p class="photo-counter">Photos {{ uploadedPhotos.length }} / 10 - You can add up to 10 photos.</p>
            
            <div class="photo-upload-area" @click="triggerPhotoUpload" @dragover.prevent @drop.prevent="handlePhotoDrop">
              <div class="upload-content">
                <div class="upload-icon">📷</div>
                <h4>ADD PHOTOS</h4>
                <p>or drag and drop</p>
              </div>
              <input 
                ref="photoInput" 
                type="file" 
                multiple 
                accept="image/*" 
                style="display: none" 
                @change="handlePhotoUpload"
              />
            </div>

            <!-- Photo Preview Grid -->
            <div v-if="uploadedPhotos.length > 0" class="photo-preview-grid">
              <div 
                v-for="(photo, index) in uploadedPhotos" 
                :key="photo.id || index" 
                class="photo-preview-item"
              >
                <img 
                  :src="photo.url" 
                  :alt="`Photo ${index + 1}`" 
                  @error="handleImageError"
                />
                <button class="remove-photo-btn" @click="removePhoto(index)">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <line x1="18" y1="6" x2="6" y2="18"/>
                    <line x1="6" y1="6" x2="18" y2="18"/>
                  </svg>
                </button>
                <div v-if="photo.existing" class="existing-photo-badge">
                  Existing
                </div>
              </div>
            </div>
          </div>

          <!-- Location -->
          <div class="location-section">
            <div class="location-icon">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                <circle cx="12" cy="10" r="3"/>
              </svg>
            </div>
            <span class="location-text">{{ userInfo.location || 'Location not set' }}</span>
          </div>

          <!-- Meetup Preferences -->
          <div class="meetup-section">
            <h4>Meetup preferences</h4>
            <p class="meetup-description">Buyers will be able to see your preferences on your listing.</p>
            
            <div class="meetup-options">
              <label class="meetup-option">
                <input type="checkbox" v-model="meetupPreferences.publicMeetup" />
                <div class="option-content">
                  <div class="option-icon">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                      <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                      <circle cx="12" cy="7" r="4"/>
                    </svg>
                  </div>
                  <div class="option-details">
                    <span class="option-title">Public meetup</span>
                    <span class="option-subtitle">Meet at a public location.</span>
                  </div>
                </div>
              </label>

              <label class="meetup-option">
                <input type="checkbox" v-model="meetupPreferences.doorPickup" />
                <div class="option-content">
                  <div class="option-icon">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                      <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
                      <polyline points="9,22 9,12 15,12 15,22"/>
                    </svg>
                  </div>
                  <div class="option-details">
                    <span class="option-title">Door pickup</span>
                    <span class="option-subtitle">Buyers pickup at your door.</span>
                  </div>
                </div>
              </label>

              <label class="meetup-option">
                <input type="checkbox" v-model="meetupPreferences.doorDropoff" />
                <div class="option-content">
                  <div class="option-icon">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                      <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
                      <polyline points="9,22 9,12 15,12 15,22"/>
                    </svg>
                  </div>
                  <div class="option-details">
                    <span class="option-title">Door dropoff</span>
                    <span class="option-subtitle">Buyers pickup at your door.</span>
                  </div>
                </div>
              </label>
            </div>
          </div>
        </div>

        <!-- Right Side - Product Details Form -->
        <div class="right-section">
          <!-- Loading State -->
          <div v-if="isLoading" class="loading-state">
            <div class="loading-spinner"></div>
            <p>Loading product data...</p>
          </div>
          
          <form v-else @submit.prevent="updateProduct">
            <!-- Required Section -->
            <div class="form-section">
              <h3 class="section-title">Required</h3>
              <p class="section-subtitle">Be as descriptive as possible.</p>

              <div class="form-group">
                <label class="form-label">Title</label>
                <input 
                  v-model="productForm.title" 
                  type="text" 
                  class="form-input" 
                  placeholder="What are you selling?"
                  required
                />
              </div>

              <div class="form-group">
                <label class="form-label">Price</label>
                <input 
                  v-model="productForm.price" 
                  type="number" 
                  class="form-input" 
                  placeholder="₱0.00"
                  min="0"
                  step="0.01"
                  required
                />
              </div>

              <div class="form-group">
                <label class="form-label">Stock Quantity</label>
                <input 
                  v-model="productForm.stock" 
                  type="number" 
                  class="form-input" 
                  placeholder="Enter available stock"
                  min="0"
                  step="1"
                  required
                />
                <small class="form-hint">Number of items available for sale</small>
              </div>

              <div class="form-group">
                <label class="form-label">Category</label>
                <select v-model="productForm.category" class="form-select" required>
                  <option value="">Select a category</option>
                  <option value="antiques">Antiques</option>
                  <option value="collectibles">Collectibles</option>
                  <option value="coins">Coins</option>
                  <option value="electronics">Electronics</option>
                  <option value="clothing">Clothing</option>
                  <option value="books">Books</option>
                  <option value="toys">Toys & Games</option>
                  <option value="others">Others</option>
                </select>
              </div>

              <div class="form-group">
                <label class="form-label">Condition</label>
                <select v-model="productForm.condition" class="form-select" required>
                  <option value="">Select condition</option>
                  <option value="new">New</option>
                  <option value="like_new">Like New</option>
                  <option value="good">Good</option>
                  <option value="fair">Fair</option>
                  <option value="poor">Poor</option>
                </select>
              </div>
            </div>

            <!-- More Details Section -->
            <div class="form-section">
              <h3 class="section-title">More Details</h3>
              <p class="section-subtitle">Attract more interest by including more details.</p>

              <div class="form-group">
                <label class="form-label">Description</label>
                <textarea 
                  v-model="productForm.description" 
                  class="form-textarea" 
                  rows="6"
                  placeholder="Describe your item in detail..."
                ></textarea>
              </div>

              <div class="form-group">
                <label class="form-label">Product tags</label>
                <input 
                  v-model="productForm.tags" 
                  type="text" 
                  class="form-input" 
                  placeholder="Add tags separated by commas (e.g., vintage, rare, collectible)"
                />
                <small class="form-hint">Separate tags with commas to help buyers find your item</small>
              </div>
            </div>

            <!-- Action Buttons -->
            <div class="form-actions">
              <ActionButton
                variant="secondary"
                icon="←"
                text="Cancel"
                @click="$router.go(-1)"
              />

              <ActionButton
                variant="danger"
                icon="🗑️"
                text="Delete Product"
                @click="confirmDelete"
              />
              
              <ActionButton
                variant="primary"
                icon="💾"
                text="Update Product"
                :loading="isSubmitting"
                @click="updateProduct"
              />
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Toast Messages -->
    <MessageToast 
      v-if="toast.show"
      :message="toast.message"
      :type="toast.type"
      :title="toast.title"
      @close="hideToast"
    />

    <!-- Confirmation Modal -->
    <ConfirmationModal 
      v-if="showConfirmation"
      :title="confirmation.title"
      :message="confirmation.message"
      :confirmText="confirmation.confirmText"
      :cancelText="confirmation.cancelText"
      @confirm="confirmation.onConfirm"
      @cancel="hideConfirmation"
    />
  </SellerLayout>
</template>

<script>
import SellerLayout from '@/components/seller/SellerLayout.vue'
import ActionButton from '@/components/seller/shared/ActionButton.vue'
import MessageToast from '@/components/seller/shared/MessageToast.vue'
import ConfirmationModal from '@/components/seller/shared/ConfirmationModal.vue'

export default {
  name: 'EditProduct',
  components: {
    SellerLayout,
    ActionButton,
    MessageToast,
    ConfirmationModal
  },
  data() {
    return {
      productId: null,
      isLoading: true,
      userInfo: {
        displayName: 'Loading...',
        avatar: null,
        location: 'Loading...'
      },
      productForm: {
        title: '',
        price: '',
        stock: '',
        category: '',
        condition: '',
        description: '',
        tags: ''
      },
      meetupPreferences: {
        publicMeetup: false,
        doorPickup: false,
        doorDropoff: false
      },
      uploadedPhotos: [],
      isSubmitting: false,
      toast: {
        show: false,
        message: '',
        type: 'success',
        title: ''
      },
      showConfirmation: false,
      confirmation: {
        title: '',
        message: '',
        confirmText: 'Confirm',
        cancelText: 'Cancel',
        onConfirm: () => {}
      }
    }
  },
  async mounted() {
    this.productId = this.$route.params.id
    console.log('EditProduct mounted with ID:', this.productId)
    
    if (!this.productId) {
      this.showToast('No product ID provided', 'error', 'Error')
      this.$router.push('/seller/items')
      return
    }
    
    await Promise.all([
      this.loadUserInfo(),
      this.loadProduct()
    ])
  },
  methods: {
    async loadUserInfo() {
      try {
        const token = localStorage.getItem('access_token') || localStorage.getItem('token')
        if (!token) {
          this.$router.push('/login')
          return
        }

        const userInfoString = localStorage.getItem('user_info')
        if (userInfoString) {
          const userInfo = JSON.parse(userInfoString)
          this.userInfo = {
            displayName: userInfo.first_name && userInfo.last_name 
              ? `${userInfo.first_name} ${userInfo.last_name}` 
              : userInfo.username || 'User',
            avatar: userInfo.avatar || null,
            location: userInfo.address || 'Location not set'
          }
        }
      } catch (error) {
        console.error('Error loading user info:', error)
      }
    },

    async loadProduct() {
      this.isLoading = true
      try {
        const token = localStorage.getItem('access_token') || localStorage.getItem('token')
        if (!token) {
          this.$router.push('/login')
          return
        }

        const response = await fetch(`http://localhost:5000/api/seller/items/${this.productId}`, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })

        if (!response.ok) {x``
          if (response.status === 404) {
            this.showToast('Product not found', 'error', 'Error')
            this.$router.push('/seller/items')
            return
          }
          throw new Error('Failed to load product')
        }

        const productData = await response.json()
        console.log('Loaded product data:', productData)
        
        // Handle different possible response formats
        const item = productData.item || productData
        
        // Populate form with loaded data - ensure all fields are auto-populated
        this.productForm = {
          title: item.title || '',
          price: item.price || '',
          stock: item.stock || 0,
          category: item.category || '',
          condition: item.condition_status || item.condition || '',
          description: item.description || '',
          tags: Array.isArray(item.tags) ? item.tags.join(', ') : (item.tags || '')
        }
        
        console.log('Form populated with:', this.productForm)
        
        // Load images from different possible formats
        let images = []
        if (item.images && Array.isArray(item.images)) {
          images = item.images
        } else if (productData.images && Array.isArray(productData.images)) {
          images = productData.images
        }
        
        if (images.length > 0) {
          this.uploadedPhotos = images.map((img, index) => ({
            id: img.id || index,
            url: img.image_url || img.url || `http://localhost:5000/uploads/items/${item.id}/image_${index}.jpeg`,
            name: `image_${img.id || index}`,
            existing: true
          }))
          console.log('Images loaded:', this.uploadedPhotos)
        } else {
          console.log('No images found for this product')
        }
        
      } catch (error) {
        console.error('Error loading product:', error)
        this.showToast('Failed to load product data', 'error', 'Error')
      } finally {
        this.isLoading = false
      }
    },
    
    triggerPhotoUpload() {
      this.$refs.photoInput.click()
    },
    
    handlePhotoUpload(event) {
      const files = Array.from(event.target.files)
      this.processPhotos(files)
    },
    
    handlePhotoDrop(event) {
      const files = Array.from(event.dataTransfer.files)
      this.processPhotos(files)
    },
    
    processPhotos(files) {
      if (this.uploadedPhotos.length + files.length > 10) {
        this.showToast('You can only upload up to 10 photos', 'error', 'Upload Limit')
        return
      }
      
      files.forEach(file => {
        if (file.type.startsWith('image/')) {
          const reader = new FileReader()
          reader.onload = (e) => {
            this.uploadedPhotos.push({
              file: file,
              url: e.target.result,
              name: file.name,
              existing: false
            })
          }
          reader.readAsDataURL(file)
        }
      })
    },

    handleImageError(event) {
      console.log('Image failed to load, using placeholder')
      event.target.src = 'https://via.placeholder.com/200x200/f3f4f6/9ca3af?text=No+Image'
    },
    
    removePhoto(index) {
      this.uploadedPhotos.splice(index, 1)
    },
    
    updateProduct() {
      if (!this.validateForm()) {
        return
      }
      
      this.showConfirmation = true
      this.confirmation = {
        title: 'Update Product',
        message: 'Are you sure you want to save these changes to your product?',
        confirmText: 'Update',
        cancelText: 'Cancel',
        onConfirm: this.confirmUpdate
      }
    },
    
    validateForm() {
      if (!this.productForm.title) {
        this.showToast('Please enter a product title', 'error', 'Validation Error')
        return false
      }
      
      if (!this.productForm.price || this.productForm.price <= 0) {
        this.showToast('Please enter a valid price', 'error', 'Validation Error')
        return false
      }

      if (this.productForm.stock === '' || this.productForm.stock < 0) {
        this.showToast('Please enter a valid stock quantity', 'error', 'Validation Error')
        return false
      }
      
      if (!this.productForm.category) {
        this.showToast('Please select a category', 'error', 'Validation Error')
        return false
      }
      
      if (!this.productForm.condition) {
        this.showToast('Please select item condition', 'error', 'Validation Error')
        return false
      }
      
      if (this.uploadedPhotos.length === 0) {
        this.showToast('Please add at least one photo', 'error', 'Validation Error')
        return false
      }
      
      return true
    },
    
    async confirmUpdate() {
      this.isSubmitting = true
      this.hideConfirmation()
      
      try {
        const token = localStorage.getItem('access_token') || localStorage.getItem('token')
        if (!token) {
          this.$router.push('/login')
          return
        }

        // Prepare the product data
        const productData = {
          title: this.productForm.title,
          price: parseFloat(this.productForm.price),
          stock: parseInt(this.productForm.stock),
          category: this.productForm.category,
          condition: this.productForm.condition,
          description: this.productForm.description,
          tags: this.productForm.tags.split(',').map(tag => tag.trim()).filter(tag => tag),
          status: 'active'
        }

        console.log('Updating product with data:', productData)

        const response = await fetch(`http://localhost:5000/api/seller/items/${this.productId}`, {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(productData)
        })

        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}))
          throw new Error(errorData.error || 'Failed to update product')
        }

        this.showToast('Product updated successfully!', 'success', 'Success')
        
        // Redirect back to items list
        setTimeout(() => {
          this.$router.push('/seller/items')
        }, 2000)
        
      } catch (error) {
        console.error('Error updating product:', error)
        this.showToast(`Failed to update product: ${error.message}`, 'error', 'Error')
      } finally {
        this.isSubmitting = false
      }
    },

    confirmDelete() {
      this.showConfirmation = true
      this.confirmation = {
        title: 'Delete Product',
        message: 'Are you sure you want to delete this product? This action cannot be undone.',
        confirmText: 'Delete',
        cancelText: 'Cancel',
        onConfirm: this.deleteProduct
      }
    },

    async deleteProduct() {
      this.isSubmitting = true
      this.hideConfirmation()
      
      try {
        const token = localStorage.getItem('access_token') || localStorage.getItem('token')
        if (!token) {
          this.$router.push('/login')
          return
        }

        const response = await fetch(`http://localhost:5000/api/seller/items/${this.productId}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })

        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}))
          throw new Error(errorData.error || 'Failed to delete product')
        }
        
        this.showToast('Product deleted successfully!', 'success', 'Success')
        
        // Redirect back to items list
        setTimeout(() => {
          this.$router.push('/seller/items')
        }, 1500)
        
      } catch (error) {
        console.error('Error deleting product:', error)
        this.showToast(`Failed to delete product: ${error.message}`, 'error', 'Error')
      } finally {
        this.isSubmitting = false
      }
    },
    
    showToast(message, type = 'success', title = '') {
      this.toast = {
        show: true,
        message,
        type,
        title
      }
    },
    
    hideToast() {
      this.toast.show = false
    },
    
    hideConfirmation() {
      this.showConfirmation = false
    }
  }
}
</script>

<style scoped>
/* Same styles as CreateProduct.vue */
.edit-product {
  padding: 24px;
}

.product-form-container {
  display: grid;
  grid-template-columns: 400px 1fr;
  gap: 32px;
  max-width: 1200px;
  margin: 0 auto;
}

/* Left Section */
.left-section {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.user-profile-section {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: white;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
}

.user-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  overflow: hidden;
}

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.user-info {
  flex: 1;
}

.user-name {
  font-size: 16px;
  font-weight: 600;
  color: #111827;
  margin: 0;
}

.listing-type {
  font-size: 14px;
  color: #6b7280;
  margin: 0;
}

.photo-upload-section {
  background: white;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  padding: 20px;
}

.photo-counter {
  font-size: 14px;
  color: #6b7280;
  margin: 0 0 16px 0;
}

.photo-upload-area {
  border: 2px dashed #d1d5db;
  border-radius: 8px;
  padding: 40px 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.photo-upload-area:hover {
  border-color: #3b82f6;
  background-color: #f8fafc;
}

.upload-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.upload-icon {
  font-size: 32px;
  margin-bottom: 8px;
}

.upload-content h4 {
  font-size: 16px;
  font-weight: 600;
  color: #111827;
  margin: 0;
}

.upload-content p {
  font-size: 14px;
  color: #6b7280;
  margin: 0;
}

.photo-preview-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
  gap: 12px;
  margin-top: 16px;
}

.photo-preview-item {
  position: relative;
  aspect-ratio: 1;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #e5e7eb;
}

.photo-preview-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.remove-photo-btn {
  position: absolute;
  top: 4px;
  right: 4px;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: rgba(239, 68, 68, 0.9);
  color: white;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s ease;
}

.remove-photo-btn:hover {
  background: rgba(220, 38, 38, 1);
}

.existing-photo-badge {
  position: absolute;
  bottom: 4px;
  left: 4px;
  background: rgba(59, 130, 246, 0.9);
  color: white;
  font-size: 10px;
  padding: 2px 6px;
  border-radius: 4px;
  font-weight: 500;
}

.location-section {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  background: white;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.location-icon {
  color: #6b7280;
}

.location-text {
  font-size: 14px;
  color: #111827;
}

.meetup-section {
  background: white;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  padding: 20px;
}

.meetup-section h4 {
  font-size: 16px;
  font-weight: 600;
  color: #111827;
  margin: 0 0 8px 0;
}

.meetup-description {
  font-size: 14px;
  color: #6b7280;
  margin: 0 0 20px 0;
}

.meetup-options {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.meetup-option {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  cursor: pointer;
}

.meetup-option input[type="checkbox"] {
  margin-top: 2px;
}

.option-content {
  display: flex;
  align-items: center;
  gap: 12px;
}

.option-icon {
  color: #6b7280;
}

.option-details {
  display: flex;
  flex-direction: column;
}

.option-title {
  font-size: 14px;
  font-weight: 500;
  color: #111827;
}

.option-subtitle {
  font-size: 13px;
  color: #6b7280;
}

/* Right Section */
.right-section {
  background: white;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  padding: 24px;
}

.form-section {
  margin-bottom: 32px;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: #111827;
  margin: 0 0 8px 0;
}

.section-subtitle {
  font-size: 14px;
  color: #6b7280;
  margin: 0 0 24px 0;
}

.form-group {
  margin-bottom: 20px;
}

.form-label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: #374151;
  margin-bottom: 6px;
}

.form-input,
.form-select,
.form-textarea {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 14px;
  transition: border-color 0.2s ease;
  background: white;
}

.form-input:focus,
.form-select:focus,
.form-textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-textarea {
  resize: vertical;
  font-family: inherit;
}

.form-hint {
  display: block;
  font-size: 12px;
  color: #6b7280;
  margin-top: 4px;
}

.form-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid #e5e7eb;
}

/* Responsive */
@media (max-width: 768px) {
  .product-form-container {
    grid-template-columns: 1fr;
    gap: 24px;
  }
  
  .form-actions {
    flex-direction: column;
  }
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f4f6;
  border-top: 4px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-state p {
  color: #6b7280;
  font-size: 14px;
  margin: 0;
}
</style>
