<template>
  <SellerLayout>
    <div class="create-item">
      <!-- Page Header -->
      <div class="page-header">
        <div class="header-content">
          <h1 class="page-title">Add New Item</h1>
          <p class="page-subtitle">List a new item for sale</p>
        </div>
        
        <div class="header-actions">
          <ActionButton
            variant="secondary"
            icon="← "
            text="Back to Items"
            @click="goBack"
          />
        </div>
      </div>

      <div class="create-container">
        <!-- Main Form -->
        <div class="item-form">
          <form @submit.prevent="saveItem">
            <!-- Basic Information -->
            <div class="form-section">
              <h2 class="section-title">Basic Information</h2>
              
              <div class="form-group">
                <label class="form-label required">Item Title</label>
                <input 
                  v-model="item.title"
                  type="text" 
                  class="form-input"
                  placeholder="Enter a descriptive title for your item"
                  required
                >
              </div>

              <div class="form-group">
                <label class="form-label required">Description</label>
                <textarea 
                  v-model="item.description"
                  class="form-textarea"
                  rows="6"
                  placeholder="Describe your item in detail. Include condition, history, provenance, etc."
                  required
                ></textarea>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label class="form-label required">Price (PHP)</label>
                  <div class="price-input">
                    <span class="currency-symbol">₱</span>
                    <input 
                      v-model.number="item.price"
                      type="number"
                      step="0.01"
                      min="0"
                      class="form-input"
                      placeholder="0.00"
                      required
                    >
                  </div>
                </div>

                <div class="form-group">
                  <label class="form-label required">Stock Quantity</label>
                  <div class="stock-input">
                    <input 
                      v-model.number="item.stock"
                      type="number"
                      min="0"
                      class="form-input"
                      placeholder="Enter available stock quantity"
                      required
                    >
                  </div>
                  <small class="form-hint">Number of items available for sale</small>
                </div>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label class="form-label required">Category</label>
                  <select v-model="item.category" class="form-select" required>
                    <option value="">Select a category</option>
                    <option value="antiques">Antiques</option>
                    <option value="collectibles">Collectibles</option>
                    <option value="coins">Coins</option>
                    <option value="others">Others</option>
                  </select>
                </div>
              </div>

              <div class="form-group">
                <label class="form-label required">Condition</label>
                <div class="condition-options">
                  <label class="condition-option" v-for="condition in conditions" :key="condition.value">
                    <input 
                      type="radio" 
                      v-model="item.condition" 
                      :value="condition.value"
                      required
                    >
                    <div class="condition-content">
                      <span class="condition-name">{{ condition.name }}</span>
                      <span class="condition-desc">{{ condition.description }}</span>
                    </div>
                  </label>
                </div>
              </div>
            </div>

            <!-- Images Section -->
            <div class="form-section">
              <h2 class="section-title">Photos</h2>
              <p class="section-subtitle">Add high-quality photos to showcase your item</p>
              
              <div class="images-upload">
                <div class="upload-grid">
                  <div 
                    v-for="(image, index) in item.images" 
                    :key="index"
                    class="image-slot"
                  >
                    <img :src="image.url" :alt="`Item photo ${index + 1}`" class="uploaded-image">
                    <button 
                      type="button"
                      class="remove-image"
                      @click="removeImage(index)"
                    >
                      ×
                    </button>
                    <div class="image-controls">
                      <button 
                        v-if="!image.isPrimary && item.images.length > 1"
                        type="button"
                        class="set-primary-btn"
                        @click="setPrimaryImage(index)"
                      >
                        Set as Primary
                      </button>
                      <span v-if="image.isPrimary" class="primary-badge">Primary</span>
                    </div>
                  </div>
                  
                  <div 
                    v-if="item.images.length < 8"
                    class="upload-slot"
                    @click="selectImages"
                  >
                    <i class="upload-icon">📷</i>
                    <span class="upload-text">Add Photos</span>
                    <span class="upload-limit">({{ item.images.length }}/8)</span>
                  </div>
                </div>
                
                <div class="upload-info">
                  <p>• Upload up to 8 high-quality photos</p>
                  <p>• First photo will be the main display image</p>
                  <p>• Supported formats: JPEG, PNG (max 5MB each)</p>
                </div>
              </div>
            </div>

            <!-- Additional Details -->
            <div class="form-section">
              <h2 class="section-title">Additional Details</h2>
              
              <div class="form-group">
                <label class="form-label">Tags</label>
                <div class="tags-input">
                  <input 
                    v-model="tagInput"
                    type="text" 
                    class="form-input"
                    placeholder="Add tags to help buyers find your item (press Enter to add)"
                    @keydown.enter.prevent="addTag"
                  >
                  <div class="tags-list">
                    <span 
                      v-for="(tag, index) in item.tags" 
                      :key="index"
                      class="tag"
                    >
                      {{ tag }}
                      <button type="button" @click="removeTag(index)">×</button>
                    </span>
                  </div>
                </div>
              </div>

              <div class="form-group">
                <label class="form-label">
                  <input type="checkbox" v-model="item.isNegotiable">
                  Price is negotiable
                </label>
              </div>

              <div class="form-group">
                <label class="form-label">
                  <input type="checkbox" v-model="item.isAuthenticated">
                  Item has been authenticated/appraised
                </label>
              </div>
            </div>

            <!-- Form Actions -->
            <div class="form-actions">
              <ActionButton
                variant="secondary"
                icon="💾"
                text="Save as Draft"
                :loading="saveLoading"
                @click="saveAsDraft"
                type="button"
              />
              <ActionButton
                variant="primary"
                icon="🚀"
                text="Publish Item"
                :loading="publishLoading"
                @click="publishItem"
                type="button"
              />
            </div>
          </form>
        </div>

        <!-- Preview Card -->
        <div class="preview-section">
          <div class="preview-card">
            <h3 class="preview-title">Preview</h3>
            
            <div class="item-preview">
              <div class="preview-image">
                <div v-if="primaryImage" class="preview-img">
                  <img :src="primaryImage.url" alt="Item preview">
                </div>
                <div v-else class="preview-placeholder">
                  <i class="placeholder-icon">📷</i>
                  <span>No image uploaded</span>
                </div>
              </div>
              
              <div class="preview-content">
                <h4 class="preview-item-title">{{ item.title || 'Item Title' }}</h4>
                <p class="preview-price">
                  ₱{{ item.price ? item.price.toFixed(2) : '0.00' }}
                  <span v-if="item.isNegotiable" class="negotiable">OBO</span>
                </p>
                <p class="preview-category">{{ item.category || 'No category' }}</p>
                <p class="preview-condition">Condition: {{ getConditionName(item.condition) || 'Not specified' }}</p>
                <p class="preview-description">
                  {{ item.description ? item.description.substring(0, 100) + (item.description.length > 100 ? '...' : '') : 'No description' }}
                </p>
                
                <div v-if="item.tags.length" class="preview-tags">
                  <span v-for="tag in item.tags.slice(0, 3)" :key="tag" class="preview-tag">
                    {{ tag }}
                  </span>
                  <span v-if="item.tags.length > 3" class="more-tags">+{{ item.tags.length - 3 }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Success/Error Messages -->
    <MessageToast
      :show="showMessage"
      :type="messageType"
      :title="messageTitle"
      :message="messageText"
      @close="hideMessage"
    />
  </SellerLayout>
</template>

<script>
import SellerLayout from '@/components/seller/SellerLayout.vue'
import ActionButton from '@/components/seller/shared/ActionButton.vue'
import MessageToast from '@/components/seller/shared/MessageToast.vue'

export default {
  name: 'CreateItem',
  components: {
    SellerLayout,
    ActionButton,
    MessageToast
  },
  data() {
    return {
      item: {
        title: '',
        description: '',
        price: null,
        stock: null,
        category: '',
        condition: '',
        year: null,
        images: [],
        tags: [],
        isNegotiable: false,
        isAuthenticated: false
      },
      tagInput: '',
      conditions: [
        { value: 'new', name: 'New', description: 'Brand new, unused item' },
        { value: 'like_new', name: 'Like New', description: 'Excellent condition, barely used' },
        { value: 'good', name: 'Good', description: 'Normal wear, good working condition' },
        { value: 'fair', name: 'Fair', description: 'Some wear and tear, still functional' },
        { value: 'poor', name: 'Poor', description: 'Heavy wear, may need repair' }
      ],
      saveLoading: false,
      publishLoading: false,
      showMessage: false,
      messageType: 'info',
      messageTitle: '',
      messageText: ''
    }
  },
  computed: {
    primaryImage() {
      return this.item.images.find(img => img.isPrimary) || this.item.images[0];
    }
  },
  methods: {
    goBack() {
      this.$router.push('/seller/items');
    },
    
    selectImages() {
      const input = document.createElement('input');
      input.type = 'file';
      input.multiple = true;
      input.accept = 'image/jpeg,image/png';
      input.onchange = (event) => {
        const files = Array.from(event.target.files);
        this.processImages(files);
      };
      input.click();
    },
    
    processImages(files) {
      const remainingSlots = 8 - this.item.images.length;
      const filesToProcess = files.slice(0, remainingSlots);
      
      filesToProcess.forEach((file, index) => {
        // Validate file size (5MB)
        if (file.size > 5 * 1024 * 1024) {
          this.showToast(`File ${file.name} is too large. Maximum size is 5MB.`, 'error', 'File Too Large');
          return;
        }
        
        const reader = new FileReader();
        reader.onload = (e) => {
          this.item.images.push({
            url: e.target.result,
            isPrimary: this.item.images.length === 0 // First image is primary
          });
        };
        reader.readAsDataURL(file);
      });
    },
    
    removeImage(index) {
      const removedImage = this.item.images[index];
      this.item.images.splice(index, 1);
      
      // If primary image was removed, set first image as primary
      if (removedImage.isPrimary && this.item.images.length > 0) {
        this.item.images[0].isPrimary = true;
      }
    },
    
    setPrimaryImage(index) {
      this.item.images.forEach((img, i) => {
        img.isPrimary = i === index;
      });
    },
    
    addTag() {
      const tag = this.tagInput.trim().toLowerCase();
      if (tag && !this.item.tags.includes(tag) && this.item.tags.length < 10) {
        this.item.tags.push(tag);
        this.tagInput = '';
      }
    },
    
    removeTag(index) {
      this.item.tags.splice(index, 1);
    },
    
    getConditionName(value) {
      const condition = this.conditions.find(c => c.value === value);
      return condition ? condition.name : '';
    },
    
    validateForm() {
      const errors = [];
      
      if (!this.item.title?.trim()) errors.push('Title is required');
      if (!this.item.description?.trim()) errors.push('Description is required');
      if (!this.item.price || this.item.price <= 0) errors.push('Valid price is required');
      if (!this.item.stock || this.item.stock < 0) errors.push('Valid stock quantity is required');
      if (!this.item.category) errors.push('Category is required');
      if (!this.item.condition) errors.push('Condition is required');
      if (this.item.images.length === 0) errors.push('At least one image is required');
      
      return errors;
    },
    
    saveAsDraft() {
      this.saveLoading = true;
      
      setTimeout(() => {
        console.log('Saving as draft:', this.item);
        this.showToast('Item saved as draft successfully', 'success', 'Draft Saved');
        this.saveLoading = false;
        this.$router.push('/seller/items');
      }, 1500);
    },
    
    publishItem() {
      const errors = this.validateForm();
      if (errors.length > 0) {
        this.showToast(errors.join(', '), 'error', 'Validation Error');
        return;
      }
      
      this.publishLoading = true;
      
      // Prepare item data for API - ensure all required fields are present and valid
      const itemData = {
        title: this.item.title?.trim() || '',
        description: this.item.description?.trim() || '',
        price: parseFloat(this.item.price) || 0,
        stock: parseInt(this.item.stock) || 0,
        category: this.item.category ? this.item.category.toLowerCase() : '',
        condition: this.item.condition ? this.item.condition.toLowerCase() : '',
        year: this.item.year ? parseInt(this.item.year) : null,
        isNegotiable: this.item.isNegotiable || false,
        isAuthenticated: this.item.isAuthenticated || false,
        status: 'active',  // Set status to active by default
        tags: this.item.tags || [],
        images: this.item.images.map((img, index) => ({
          url: img.url,
          isPrimary: img.isPrimary || index === 0,
          displayOrder: index
        }))
      };
      
      // Additional validation before sending
      if (!itemData.title) {
        this.showToast('Title is required', 'error', 'Validation Error');
        this.publishLoading = false;
        return;
      }
      if (!itemData.description) {
        this.showToast('Description is required', 'error', 'Validation Error');
        this.publishLoading = false;
        return;
      }
      if (itemData.price <= 0) {
        this.showToast('Valid price is required', 'error', 'Validation Error');
        this.publishLoading = false;
        return;
      }
      if (itemData.stock < 0) {
        this.showToast('Valid stock quantity is required', 'error', 'Validation Error');
        this.publishLoading = false;
        return;
      }
      if (!itemData.category) {
        this.showToast('Category is required', 'error', 'Validation Error');
        this.publishLoading = false;
        return;
      }
      if (!itemData.condition) {
        this.showToast('Condition is required', 'error', 'Validation Error');
        this.publishLoading = false;
        return;
      }
      
      // Get JWT token from localStorage with proper priority (access_token is what login stores)
      const token = localStorage.getItem('access_token') || localStorage.getItem('token') || localStorage.getItem('jwt_token');
      
      if (!token) {
        this.showToast('Authentication required. Please log in again.', 'error', 'Authentication Error');
        this.publishLoading = false;
        this.$router.push('/login');
        return;
      }
      
      console.log('Sending item data:', itemData);
      console.log('Using token:', token ? 'Token found' : 'No token found');
      
      fetch('http://localhost:5000/api/seller/items', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(itemData)
      })
      .then(response => {
        console.log('Response status:', response.status);
        if (!response.ok) {
          // Try to get the error response body for better debugging
          return response.text().then(errorText => {
            let errorMessage = `HTTP error! status: ${response.status}`;
            try {
              const errorData = JSON.parse(errorText);
              console.error('Server error response:', errorData);
              
              // Handle specific JWT errors
              if (errorData.msg && errorData.msg.includes('Subject must be a string')) {
                errorMessage = 'Authentication token is invalid. Please log in again.';
                // Clear invalid tokens
                localStorage.removeItem('access_token');
                localStorage.removeItem('token');
                localStorage.removeItem('jwt_token');
                // Redirect to login
                setTimeout(() => {
                  this.$router.push('/login');
                }, 2000);
              } else {
                errorMessage = errorData.error || errorData.msg || errorData.message || errorMessage;
              }
            } catch (e) {
              // If it's not JSON, use the text as is
              errorMessage = errorText || errorMessage;
            }
            throw new Error(errorMessage);
          });
        }
        return response.json();
      })
      .then(data => {
        console.log('Item created successfully:', data);
        this.showToast('Item published successfully and is now live!', 'success', 'Item Published');
        this.publishLoading = false;
        this.$router.push('/seller/items');
      })
      .catch(error => {
        console.error('Error creating item:', error);
        this.showToast('Failed to publish item. Please try again.', 'error', 'Publish Failed');
        this.publishLoading = false;
      });
    },
    
    showToast(message, type = 'info', title = '') {
      this.messageText = message;
      this.messageType = type;
      this.messageTitle = title;
      this.showMessage = true;
    },
    
    hideMessage() {
      this.showMessage = false;
    }
  }
}
</script>

<style scoped>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

.create-item {
  max-width: 1400px;
  margin: 0 auto;
  padding: 32px;
  font-family: 'Inter', sans-serif;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 48px;
  padding: 32px;
  background: linear-gradient(135deg, #f8f6f1 0%, #e8ddd4 100%);
  border-radius: 24px;
  border: 1px solid #d4af94;
  box-shadow: 0 8px 25px rgba(139, 90, 60, 0.1);
}

.page-title {
  margin: 0 0 8px 0;
  font-family: 'Playfair Display', serif;
  font-size: 36px;
  font-weight: 600;
  color: #8b5a3c;
  text-shadow: 0 2px 4px rgba(139, 90, 60, 0.1);
}

.page-subtitle {
  margin: 0;
  color: #8b5a3c;
  font-size: 16px;
  opacity: 0.8;
}

.create-container {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 48px;
  align-items: start;
}

.item-form {
  background: linear-gradient(135deg, #f8f6f1 0%, #e8ddd4 100%);
  border-radius: 24px;
  border: 1px solid #d4af94;
  padding: 0;
  box-shadow: 0 8px 25px rgba(139, 90, 60, 0.1);
  overflow: hidden;
}

.form-section {
  padding: 32px;
  border-bottom: 1px solid #e8ddd4;
}

.form-section:last-child {
  border-bottom: none;
}

.section-title {
  margin: 0 0 8px 0;
  font-family: 'Playfair Display', serif;
  font-size: 24px;
  font-weight: 600;
  color: #8b5a3c;
}

.section-subtitle {
  margin: 0 0 24px 0;
  color: #8b5a3c;
  opacity: 0.8;
  font-size: 14px;
}

.form-group {
  margin-bottom: 24px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.form-label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #8b5a3c;
  font-size: 14px;
}

.form-label.required::after {
  content: ' *';
  color: #dc3545;
}

.form-input {
  width: 100%;
  padding: 16px;
  border: 1px solid #d4af94;
  border-radius: 12px;
  font-size: 14px;
  background: rgba(248, 246, 241, 0.7);
  color: #8b5a3c;
  transition: all 0.3s ease;
  font-family: 'Inter', sans-serif;
}

.form-input:focus {
  outline: none;
  border-color: #8b5a3c;
  box-shadow: 0 0 0 3px rgba(139, 90, 60, 0.1);
  background: rgba(248, 246, 241, 1);
}

.form-input::placeholder {
  color: #8b5a3c;
  opacity: 0.6;
}

.form-textarea {
  width: 100%;
  padding: 16px;
  border: 1px solid #d4af94;
  border-radius: 12px;
  font-size: 14px;
  font-family: 'Inter', sans-serif;
  resize: vertical;
  min-height: 120px;
  background: rgba(248, 246, 241, 0.7);
  color: #8b5a3c;
  transition: all 0.3s ease;
}

.form-textarea:focus {
  outline: none;
  border-color: #8b5a3c;
  box-shadow: 0 0 0 3px rgba(139, 90, 60, 0.1);
  background: rgba(248, 246, 241, 1);
}

.form-textarea::placeholder {
  color: #8b5a3c;
  opacity: 0.6;
}

.form-select {
  width: 100%;
  padding: 16px;
  border: 1px solid #d4af94;
  border-radius: 12px;
  font-size: 14px;
  background: rgba(248, 246, 241, 0.7);
  color: #8b5a3c;
  font-family: 'Inter', sans-serif;
  transition: all 0.3s ease;
}

.form-select:focus {
  outline: none;
  border-color: #8b5a3c;
  box-shadow: 0 0 0 3px rgba(139, 90, 60, 0.1);
  background: rgba(248, 246, 241, 1);
}

.price-input {
  position: relative;
}

.price-input .form-input {
  padding-left: 32px;
}

.currency-symbol {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #6c757d;
  font-weight: 500;
}

.stock-input {
  position: relative;
}

.stock-input .form-input {
  padding: 12px 16px;
}

.form-hint {
  color: #6c757d;
  font-size: 12px;
  margin-top: 4px;
  display: block;
}

.currency-symbol {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #6c757d;
  font-weight: 500;
}

.price-input .form-input {
  padding-left: 28px;
}

.condition-options {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.condition-option {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  cursor: pointer;
  transition: border-color 0.2s ease;
}

.condition-option:hover {
  border-color: #007bff;
}

.condition-option input[type="radio"] {
  margin: 0;
}

.condition-content {
  display: flex;
  flex-direction: column;
}

.condition-name {
  font-weight: 500;
  color: #343a40;
}

.condition-desc {
  font-size: 12px;
  color: #6c757d;
}

/* Images Upload */
.upload-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 16px;
  margin-bottom: 16px;
}

.image-slot {
  position: relative;
  aspect-ratio: 1;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #dee2e6;
}

.uploaded-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.remove-image {
  position: absolute;
  top: 4px;
  right: 4px;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  border: none;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  cursor: pointer;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.image-controls {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.7);
  padding: 4px;
  text-align: center;
}

.set-primary-btn {
  background: none;
  border: none;
  color: white;
  font-size: 10px;
  cursor: pointer;
}

.primary-badge {
  color: white;
  font-size: 10px;
  font-weight: 500;
}

.upload-slot {
  aspect-ratio: 1;
  border: 2px dashed #dee2e6;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: border-color 0.2s ease;
}

.upload-slot:hover {
  border-color: #007bff;
}

.upload-icon {
  font-size: 32px;
  color: #6c757d;
  margin-bottom: 8px;
}

.upload-text {
  font-size: 14px;
  color: #6c757d;
  font-weight: 500;
}

.upload-limit {
  font-size: 12px;
  color: #6c757d;
}

.upload-info {
  font-size: 12px;
  color: #6c757d;
  line-height: 1.5;
}

.upload-info p {
  margin: 4px 0;
}

/* Tags */
.tags-input .form-input {
  margin-bottom: 12px;
}

.tags-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: #e3f2fd;
  color: #1976d2;
  padding: 4px 8px;
  border-radius: 16px;
  font-size: 12px;
  font-weight: 500;
}

.tag button {
  background: none;
  border: none;
  color: inherit;
  cursor: pointer;
  font-size: 14px;
  line-height: 1;
}

/* Form Actions */
.form-actions {
  display: flex;
  gap: 16px;
  justify-content: flex-end;
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid #e9ecef;
}

/* Preview Section */
.preview-section {
  position: sticky;
  top: 24px;
}

.preview-card {
  background: white;
  border-radius: 12px;
  border: 1px solid #e9ecef;
  padding: 24px;
}

.preview-title {
  margin: 0 0 20px 0;
  font-size: 18px;
  font-weight: 600;
  color: #343a40;
}

.item-preview {
  border: 1px solid #e9ecef;
  border-radius: 8px;
  overflow: hidden;
}

.preview-image {
  aspect-ratio: 1;
  background: #f8f9fa;
}

.preview-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.preview-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #6c757d;
}

.placeholder-icon {
  font-size: 48px;
  margin-bottom: 8px;
}

.preview-content {
  padding: 16px;
}

.preview-item-title {
  margin: 0 0 8px 0;
  font-size: 16px;
  font-weight: 600;
  color: #343a40;
}

.preview-price {
  margin: 0 0 8px 0;
  font-size: 20px;
  font-weight: 700;
  color: #28a745;
}

.negotiable {
  font-size: 12px;
  color: #6c757d;
  font-weight: 400;
}

.preview-category,
.preview-condition {
  margin: 0 0 8px 0;
  font-size: 14px;
  color: #6c757d;
}

.preview-description {
  margin: 0 0 12px 0;
  font-size: 14px;
  color: #495057;
  line-height: 1.4;
}

.preview-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.preview-tag {
  background: #f8f9fa;
  color: #495057;
  padding: 2px 6px;
  border-radius: 12px;
  font-size: 10px;
  font-weight: 500;
}

.more-tags {
  background: #e9ecef;
  color: #6c757d;
  padding: 2px 6px;
  border-radius: 12px;
  font-size: 10px;
}

/* Responsive */
@media (max-width: 768px) {
  .create-container {
    grid-template-columns: 1fr;
    gap: 24px;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .upload-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
</style>
