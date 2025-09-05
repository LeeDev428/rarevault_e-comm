<template>
  <SellerLayout>
    <div class="edit-item">
      <!-- Page Header -->
      <div class="page-header">
        <div class="header-content">
          <h1 class="page-title">Edit Item</h1>
          <p class="page-subtitle">Update your item details</p>
        </div>
        
        <div class="header-actions">
          <ActionButton
            variant="secondary"
            icon="←"
            text="Back to Item"
            @click="goBack"
          />
        </div>
      </div>

      <div class="edit-container">
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
                  <label class="form-label required">Price (USD)</label>
                  <div class="price-input">
                    <span class="currency-symbol">$</span>
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
                  <label class="form-label required">Category</label>
                  <select v-model="item.category" class="form-select" required>
                    <option value="">Select a category</option>
                    <option value="Watches">Watches</option>
                    <option value="Antiques">Antiques</option>
                    <option value="Coins">Coins</option>
                    <option value="Art">Art</option>
                    <option value="Jewelry">Jewelry</option>
                    <option value="Books">Books</option>
                    <option value="Collectibles">Collectibles</option>
                    <option value="Furniture">Furniture</option>
                    <option value="Other">Other</option>
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

              <div class="form-group">
                <label class="form-label required">Status</label>
                <select v-model="item.status" class="form-select" required>
                  <option value="active">Active - Visible to buyers</option>
                  <option value="paused">Paused - Hidden from buyers</option>
                  <option value="sold">Sold - Marked as sold</option>
                </select>
              </div>
            </div>

            <!-- Images Section -->
            <div class="form-section">
              <h2 class="section-title">Photos</h2>
              <p class="section-subtitle">Manage your item photos</p>
              
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
                icon="❌"
                text="Cancel"
                @click="cancelEdit"
                type="button"
              />
              <ActionButton
                variant="primary"
                icon="💾"
                text="Save Changes"
                :loading="saveLoading"
                @click="saveChanges"
                type="button"
              />
            </div>
          </form>
        </div>

        <!-- Current Item Preview -->
        <div class="preview-section">
          <div class="preview-card">
            <h3 class="preview-title">Preview Changes</h3>
            
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
                  ${{ item.price ? item.price.toFixed(2) : '0.00' }}
                  <span v-if="item.isNegotiable" class="negotiable">OBO</span>
                </p>
                <p class="preview-category">{{ item.category || 'No category' }}</p>
                <p class="preview-condition">Condition: {{ getConditionName(item.condition) || 'Not specified' }}</p>
                <p class="preview-status">
                  Status: 
                  <span class="status-badge" :class="`status-${item.status}`">
                    {{ item.status || 'Not set' }}
                  </span>
                </p>
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

            <!-- Change Summary -->
            <div v-if="hasChanges" class="changes-summary">
              <h4>Changes Made:</h4>
              <ul class="changes-list">
                <li v-for="change in changesList" :key="change">{{ change }}</li>
              </ul>
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
  name: 'EditItem',
  components: {
    SellerLayout,
    ActionButton,
    MessageToast
  },
  data() {
    return {
      item: {
        id: 1,
        title: 'Vintage Rolex Submariner Watch',
        description: 'This is a rare vintage Rolex Submariner from 1965 in excellent condition. The watch has been well-maintained and comes with original box and papers.',
        price: 8500.00,
        category: 'Watches',
        condition: 'good',
        status: 'active',
        images: [
          { url: '/api/placeholder/400/400', isPrimary: true },
          { url: '/api/placeholder/400/401', isPrimary: false },
          { url: '/api/placeholder/400/402', isPrimary: false }
        ],
        tags: ['vintage', 'rolex', 'submariner', 'collectible'],
        isNegotiable: true,
        isAuthenticated: true
      },
      originalItem: {},
      tagInput: '',
      conditions: [
        { value: 'new', name: 'New', description: 'Brand new, unused item' },
        { value: 'like_new', name: 'Like New', description: 'Excellent condition, barely used' },
        { value: 'good', name: 'Good', description: 'Normal wear, good working condition' },
        { value: 'fair', name: 'Fair', description: 'Some wear and tear, still functional' },
        { value: 'poor', name: 'Poor', description: 'Heavy wear, may need repair' }
      ],
      saveLoading: false,
      showMessage: false,
      messageType: 'info',
      messageTitle: '',
      messageText: ''
    }
  },
  computed: {
    primaryImage() {
      return this.item.images.find(img => img.isPrimary) || this.item.images[0];
    },
    hasChanges() {
      return JSON.stringify(this.item) !== JSON.stringify(this.originalItem);
    },
    changesList() {
      const changes = [];
      if (this.item.title !== this.originalItem.title) changes.push('Title updated');
      if (this.item.description !== this.originalItem.description) changes.push('Description updated');
      if (this.item.price !== this.originalItem.price) changes.push('Price updated');
      if (this.item.category !== this.originalItem.category) changes.push('Category updated');
      if (this.item.condition !== this.originalItem.condition) changes.push('Condition updated');
      if (this.item.status !== this.originalItem.status) changes.push('Status updated');
      if (JSON.stringify(this.item.tags) !== JSON.stringify(this.originalItem.tags)) changes.push('Tags updated');
      if (this.item.isNegotiable !== this.originalItem.isNegotiable) changes.push('Negotiable setting updated');
      if (this.item.isAuthenticated !== this.originalItem.isAuthenticated) changes.push('Authentication status updated');
      if (JSON.stringify(this.item.images) !== JSON.stringify(this.originalItem.images)) changes.push('Images updated');
      return changes;
    }
  },
  mounted() {
    // In a real app, load item data based on route params
    const itemId = this.$route.params.id;
    this.loadItem(itemId);
    // Store original for comparison
    this.originalItem = JSON.parse(JSON.stringify(this.item));
  },
  methods: {
    loadItem(id) {
      // Simulate loading item data
      console.log('Loading item for edit:', id);
      // In real app, make API call here
    },
    
    goBack() {
      this.$router.push(`/seller/items/${this.item.id}`);
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
      if (!this.item.category) errors.push('Category is required');
      if (!this.item.condition) errors.push('Condition is required');
      if (!this.item.status) errors.push('Status is required');
      if (this.item.images.length === 0) errors.push('At least one image is required');
      
      return errors;
    },
    
    cancelEdit() {
      if (this.hasChanges) {
        if (confirm('You have unsaved changes. Are you sure you want to cancel?')) {
          this.goBack();
        }
      } else {
        this.goBack();
      }
    },
    
    saveChanges() {
      const errors = this.validateForm();
      if (errors.length > 0) {
        this.showToast(errors.join(', '), 'error', 'Validation Error');
        return;
      }
      
      this.saveLoading = true;
      
      setTimeout(() => {
        console.log('Saving item changes:', this.item);
        this.showToast('Item updated successfully!', 'success', 'Changes Saved');
        this.saveLoading = false;
        this.originalItem = JSON.parse(JSON.stringify(this.item));
        // Redirect to view item
        setTimeout(() => {
          this.$router.push(`/seller/items/${this.item.id}`);
        }, 1000);
      }, 2000);
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
.edit-item {
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 1px solid #e9ecef;
}

.page-title {
  margin: 0 0 8px 0;
  font-size: 32px;
  font-weight: 700;
  color: #343a40;
}

.page-subtitle {
  margin: 0;
  color: #6c757d;
  font-size: 16px;
}

.edit-container {
  display: grid;
  grid-template-columns: 1fr 350px;
  gap: 32px;
  align-items: start;
}

.item-form {
  background: white;
  border-radius: 12px;
  border: 1px solid #e9ecef;
  padding: 32px;
}

.form-section {
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 1px solid #f1f3f4;
}

.form-section:last-child {
  margin-bottom: 0;
  padding-bottom: 0;
  border-bottom: none;
}

.section-title {
  margin: 0 0 8px 0;
  font-size: 20px;
  font-weight: 600;
  color: #343a40;
}

.section-subtitle {
  margin: 0 0 20px 0;
  color: #6c757d;
  font-size: 14px;
}

.form-group {
  margin-bottom: 20px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.form-label {
  display: block;
  margin-bottom: 6px;
  font-weight: 500;
  color: #495057;
  font-size: 14px;
}

.form-label.required::after {
  content: ' *';
  color: #dc3545;
}

.form-input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  font-size: 14px;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.form-input:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
}

.form-textarea {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  font-size: 14px;
  font-family: inherit;
  resize: vertical;
  min-height: 120px;
}

.form-textarea:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
}

.form-select {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  font-size: 14px;
  background: white;
}

.form-select:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
}

.price-input {
  position: relative;
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
  margin-bottom: 20px;
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
.preview-condition,
.preview-status {
  margin: 0 0 8px 0;
  font-size: 14px;
  color: #6c757d;
}

.status-badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 10px;
  font-weight: 500;
  text-transform: capitalize;
}

.status-active {
  background: #d4edda;
  color: #155724;
}

.status-paused {
  background: #fff3cd;
  color: #856404;
}

.status-sold {
  background: #d1ecf1;
  color: #0c5460;
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

.changes-summary {
  border-top: 1px solid #e9ecef;
  padding-top: 16px;
}

.changes-summary h4 {
  margin: 0 0 8px 0;
  font-size: 14px;
  font-weight: 600;
  color: #343a40;
}

.changes-list {
  margin: 0;
  padding: 0 0 0 16px;
  font-size: 12px;
  color: #6c757d;
}

.changes-list li {
  margin-bottom: 4px;
}

/* Responsive */
@media (max-width: 768px) {
  .edit-container {
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
