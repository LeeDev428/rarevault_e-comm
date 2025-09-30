<template>
  <SellerLayout>
    <div class="view-item">
      <!-- Loading State -->
      <div v-if="loading" class="loading-container">
        <div class="loading-spinner"></div>
        <p>Loading item details...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="error-container">
        <div class="error-icon">⚠️</div>
        <h3>{{ error }}</h3>
        <ActionButton
          variant="primary"
          text="Go Back to Items"
          @click="goBack"
        />
      </div>

      <!-- Item Content -->
      <div v-else-if="item">
        <!-- Page Header -->
        <div class="page-header">
          <div class="header-content">
            <ActionButton
              variant="secondary"
              icon="←"
              text="Back to Items"
              @click="goBack"
            />
            <div class="item-status">
              <span class="status-badge" :class="`status-${item.status}`">
                {{ item.status }}
              </span>
            </div>
          <!-- End of v-else-if="item" -->
          </div>
          
          <div class="header-actions">
            <ActionButton
              variant="secondary"
              icon="✏️"
              text="Edit Item"
              @click="editItem"
            />
            <ActionButton
              variant="danger"
              icon="🗑️"
              text="Delete Item"
              @click="deleteItem"
            />
          </div>
        </div>

        <div class="item-container">
          <!-- Image Gallery -->
          <div class="image-section">
            <div class="main-image">
              <img 
                :src="getItemImage(item)" 
                :alt="item.title"
                @error="$event.target.src = '/api/placeholder/400/400'"
                class="main-img"
              >
            </div>
            
            <div v-if="item.images && item.images.length > 1" class="thumbnail-grid">
              <div 
                v-for="(image, index) in item.images" 
                :key="index"
                class="thumbnail"
                :class="{ active: selectedImageIndex === index }"
                @click="selectImage(index)"
              >
                <img :src="image.url" :alt="`${item.title} - Image ${index + 1}`">
              </div>
            </div>
          </div>

          <!-- Item Details -->
          <div class="details-section">
            <div class="item-header">
              <h1 class="item-title">{{ item.title }}</h1>
              <div class="item-meta">
                <span class="item-id">Item ID: #{{ item.id }}</span>
                <span class="created-date">Listed {{ formatDate(item.created_at) }}</span>
              </div>
            </div>

            <div class="price-section">
              <div class="price">
                ${{ parseFloat(item.price).toFixed(2) }}
                <span v-if="item.isNegotiable" class="negotiable">OBO</span>
              </div>
              <div class="condition">
                Condition: <strong>{{ conditionName }}</strong>
              </div>
            </div>

            <div class="details-grid">
              <div class="detail-item">
                <label>Category</label>
                <span>{{ item?.category || 'N/A' }}</span>
              </div>
              
              <div class="detail-item">
                <label>Views</label>
                <span>{{ item?.views || 0 }}</span>
              </div>
              
              <div class="detail-item">
                <label>Favorites</label>
                <span>{{ item?.favorites || 0 }}</span>
              </div>
              
              <div class="detail-item">
                <label>Inquiries</label>
                <span>{{ item?.inquiries || 0 }}</span>
              </div>
            </div>

            <div class="description-section">
              <h3>Description</h3>
              <p class="description">{{ item?.description || 'No description available' }}</p>
            </div>

            <div v-if="item?.tags && item.tags.length" class="tags-section">
              <h3>Tags</h3>
              <div class="tags">
                <span v-for="tag in item.tags" :key="tag" class="tag">
                  {{ tag }}
                </span>
              </div>
            </div>

            <div class="badges-section">
              <div v-if="item?.isAuthenticated" class="badge authenticated">
                ✅ Authenticated
              </div>
              <div v-if="item?.isNegotiable" class="badge negotiable">
                💬 Price Negotiable
              </div>
            </div>

            <!-- Action Buttons -->
            <div class="item-actions">
              <ActionButton
                v-if="item?.status === 'active'"
                variant="warning"
                icon="⏸️"
                text="Pause Listing"
                @click="pauseListing"
              />
              <ActionButton
                v-if="item?.status === 'paused'"
                variant="success"
                icon="▶️"
                text="Resume Listing"
                @click="resumeListing"
              />
              <ActionButton
                variant="info"
                icon="📊"
                text="View Analytics"
                @click="viewAnalytics"
              />
              <ActionButton
                variant="secondary"
                icon="📋"
                text="Duplicate Item"
                @click="duplicateItem"
              />
            </div>
          </div>
        </div>

        <!-- Stats Section -->
        <div class="stats-section">
          <h2>Item Performance</h2>
          <div class="stats-grid">
            <div class="stat-card">
              <div class="stat-icon">👁️</div>
              <div class="stat-content">
                <h3>{{ item?.views || 0 }}</h3>
                <p>Views</p>
              </div>
            </div>
            
            <div class="stat-card">
              <div class="stat-icon">❤️</div>
              <div class="stat-content">
                <h3>{{ item?.favorites || 0 }}</h3>
                <p>Favorites</p>
              </div>
            </div>
            
            <div class="stat-card">
              <div class="stat-icon">💬</div>
              <div class="stat-content">
                <h3>{{ item?.inquiries || 0 }}</h3>
                <p>Inquiries</p>
              </div>
            </div>
            
            <div class="stat-card">
              <div class="stat-icon">📈</div>
              <div class="stat-content">
                <h3>{{ item?.engagement || 0 }}%</h3>
                <p>Engagement Rate</p>
              </div>
            </div>
          </div>
        </div>
      </div>

          <div v-if="item.tags.length" class="tags-section">
            <h3>Tags</h3>
            <div class="tags">
              <span v-for="tag in item.tags" :key="tag" class="tag">
                {{ tag }}
              </span>
            </div>
          </div>

          <div class="badges-section">
            <div v-if="item.isAuthenticated" class="badge authenticated">
              ✅ Authenticated
            </div>
            <div v-if="item.isNegotiable" class="badge negotiable">
              💬 Price Negotiable
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="item-actions">
            <ActionButton
              v-if="item.status === 'active'"
              variant="warning"
              icon="⏸️"
              text="Pause Listing"
              @click="pauseListing"
            />
            <ActionButton
              v-if="item.status === 'paused'"
              variant="success"
              icon="▶️"
              text="Resume Listing"
              @click="resumeListing"
            />
            <ActionButton
              variant="info"
              icon="📊"
              text="View Analytics"
              @click="viewAnalytics"
            />
            <ActionButton
              variant="secondary"
              icon="📋"
              text="Duplicate Item"
              @click="duplicateItem"
            />
          </div>
      
   

      <!-- Stats Section -->
      <div class="stats-section">
        <h2>Item Performance</h2>
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-icon">👁️</div>
            <div class="stat-content">
              <h3>{{ item.views || 0 }}</h3>
              <p>Total Views</p>
            </div>
          </div>
          
          <div class="stat-card">
            <div class="stat-icon">❤️</div>
            <div class="stat-content">
              <h3>{{ item.favorites || 0 }}</h3>
              <p>Favorites</p>
            </div>
          </div>
          
          <div class="stat-card">
            <div class="stat-icon">💬</div>
            <div class="stat-content">
              <h3>{{ item.inquiries || 0 }}</h3>
              <p>Inquiries</p>
            </div>
          </div>
          
          <div class="stat-card">
            <div class="stat-icon">📈</div>
            <div class="stat-content">
              <h3>{{ item.engagement || 0 }}%</h3>
              <p>Engagement Rate</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Confirmation Modal -->
      <ConfirmationModal
        v-if="item"
        :show="showDeleteModal"
        title="Delete Item"
        :message="`Are you sure you want to delete '${item.title}'? This action cannot be undone.`"
        type="danger"
        :loading="deleteLoading"
        @confirm="confirmDelete"
        @cancel="cancelDelete"
      />

      <!-- Message Toast -->
      <MessageToast
        :show="showMessage"
        :type="messageType"
        :title="messageTitle"
        :message="messageText"
        @close="hideMessage"
      />
    </div>
  </SellerLayout>
</template>

<script>
import SellerLayout from '@/components/seller/SellerLayout.vue'
import ActionButton from '@/components/seller/shared/ActionButton.vue'
import ConfirmationModal from '@/components/seller/shared/ConfirmationModal.vue'
import MessageToast from '@/components/seller/shared/MessageToast.vue'

export default {
  name: 'ViewItem',
  components: {
    SellerLayout,
    ActionButton,
    ConfirmationModal,
    MessageToast
  },
  data() {
    return {
      selectedImageIndex: 0,
      item: null,
      loading: true,
      error: null,
      conditions: [
        { value: 'new', name: 'New' },
        { value: 'like_new', name: 'Like New' },
        { value: 'good', name: 'Good' },
        { value: 'fair', name: 'Fair' },
        { value: 'poor', name: 'Poor' }
      ],
      showDeleteModal: false,
      deleteLoading: false,
      showMessage: false,
      messageType: 'info',
      messageTitle: '',
      messageText: ''
    }
  },
  computed: {
    selectedImage() {
      return this.item?.images[this.selectedImageIndex];
    },
    conditionName() {
      const condition = this.conditions.find(c => c.value === this.item?.condition);
      return condition ? condition.name : '';
    }
  },
  mounted() {
    // In a real app, load item data based on route params
    const itemId = this.$route.params.id;
    this.loadItem(itemId);
  },
  methods: {
    getItemImage(item) {
      // Use primary_image from the item object
      if (item?.primary_image) {
        return item.primary_image;
      }
      
      // Fallback to images array if available
      if (item?.images && item.images.length > 0) {
        return item.images[0].url || item.images[0];
      }
      
      // Default placeholder
      return '/api/placeholder/400/400';
    },
    
    async loadItem(id) {
      try {
        this.loading = true;
        this.error = null;
        
        const token = localStorage.getItem('token');
        if (!token) {
          this.$router.push('/login');
          return;
        }

        const response = await fetch(`http://localhost:5000/api/seller/items/${id}`, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });

        if (!response.ok) {
          if (response.status === 401) {
            localStorage.removeItem('token');
            this.$router.push('/login');
            return;
          } else if (response.status === 404) {
            this.error = 'Item not found';
            return;
          }
          throw new Error('Failed to load item');
        }

        const data = await response.json();
        this.item = data.item;
        
        // Ensure images array exists
        if (!this.item.images) {
          this.item.images = [];
        }
        
      } catch (error) {
        console.error('Error loading item:', error);
        this.error = 'Failed to load item. Please try again.';
      } finally {
        this.loading = false;
      }
    },
    
    goBack() {
      this.$router.push('/seller/items');
    },
    
    editItem() {
      this.$router.push(`/seller/items/${this.item.id}/edit`);
    },
    
    deleteItem() {
      this.showDeleteModal = true;
    },
    
    confirmDelete() {
      this.deleteLoading = true;
      
      const deleteItem = async () => {
        try {
          const token = localStorage.getItem('token');
          if (!token) {
            this.$router.push('/login');
            return;
          }

          const response = await fetch(`http://localhost:5000/api/seller/items/${this.item.id}`, {
            method: 'DELETE',
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
            }
          });

          if (!response.ok) {
            if (response.status === 401) {
              localStorage.removeItem('token');
              this.$router.push('/login');
              return;
            }
            throw new Error('Failed to delete item');
          }

          this.showToast('Item deleted successfully', 'success', 'Item Deleted');
          this.deleteLoading = false;
          this.showDeleteModal = false;
          this.$router.push('/seller/items');
          
        } catch (error) {
          console.error('Error deleting item:', error);
          this.showToast('Failed to delete item. Please try again.', 'error', 'Delete Failed');
          this.deleteLoading = false;
        }
      };

      deleteItem();
    },
    
    cancelDelete() {
      this.showDeleteModal = false;
    },
    
    selectImage(index) {
      this.selectedImageIndex = index;
    },
    
    pauseListing() {
      this.item.status = 'paused';
      this.showToast('Item listing has been paused', 'success', 'Listing Paused');
    },
    
    resumeListing() {
      this.item.status = 'active';
      this.showToast('Item listing has been resumed', 'success', 'Listing Resumed');
    },
    
    viewAnalytics() {
      this.showToast('Analytics feature coming soon!', 'info', 'Coming Soon');
    },
    
    duplicateItem() {
      this.showToast('Item duplicated successfully', 'success', 'Item Duplicated');
    },
    
    getConditionName(value) {
      const condition = this.conditions.find(c => c.value === value);
      return condition ? condition.name : value;
    },
    
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
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
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400;1,600;1,700;1,800&family=Inter:wght@300;400;500;600;700&family=Crimson+Text:wght@400;600;700&family=Libre+Baskerville:wght@400;700&display=swap');

.view-item {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px;
  font-family: 'Inter', sans-serif;
}

.loading-container, .error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 32px;
  text-align: center;
  background: linear-gradient(135deg, #f8f6f1 0%, #e8ddd4 100%);
  border-radius: 24px;
  border: 1px solid #d4af94;
  box-shadow: 0 8px 25px rgba(139, 90, 60, 0.1);
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 4px solid rgba(139, 90, 60, 0.1);
  border-left: 4px solid #8b5a3c;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-container .error-icon {
  font-size: 64px;
  margin-bottom: 20px;
  opacity: 0.7;
}

.error-container h3 {
  font-family: 'Playfair Display', serif;
  color: #8b5a3c;
  margin-bottom: 32px;
  font-size: 24px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 48px;
  padding: 32px;
  background: #ffffff;
  border-radius: 24px;
  border: 1px solid #e5e7eb;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.header-content {
  display: flex;
  align-items: center;
  gap: 20px;
}

.header-actions {
  display: flex;
  gap: 16px;
}

.item-status .status-badge {
  display: inline-block;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: capitalize;
  letter-spacing: 0.5px;
}

.status-active {
  background: linear-gradient(135deg, #d4edda 0%, #a8e6cf 100%);
  color: #155724;
  border: 1px solid #a8e6cf;
}

.status-paused {
  background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
  color: #856404;
  border: 1px solid #ffeaa7;
}

.status-sold {
  background: linear-gradient(135deg, #d1ecf1 0%, #a8d8ea 100%);
  color: #0c5460;
  border: 1px solid #a8d8ea;
}

.item-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 64px;
  margin-bottom: 64px;
}

.image-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.main-image {
  aspect-ratio: 1;
  border-radius: 20px;
  overflow: hidden;
  border: 2px solid #d4af94;
  box-shadow: 0 8px 25px rgba(139, 90, 60, 0.1);
}

.main-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.thumbnail-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.thumbnail {
  aspect-ratio: 1;
  border-radius: 12px;
  overflow: hidden;
  border: 2px solid transparent;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(139, 90, 60, 0.1);
}

.thumbnail.active {
  border-color: #8b5a3c;
  transform: scale(1.05);
  box-shadow: 0 6px 20px rgba(139, 90, 60, 0.2);
}

.thumbnail:hover {
  border-color: #8b5a3c;
  transform: scale(1.02);
}

.thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.details-section {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.item-header {
  padding-bottom: 24px;
  border-bottom: 1px solid #d4af94;
}

.item-title {
  margin: 0 0 12px 0;
  font-family: 'Playfair Display', serif;
  font-size: 36px;
  font-weight: 700;
  color: #1f2937;
  line-height: 1.2;
  text-shadow: none;
}

.item-meta {
  display: flex;
  gap: 20px;
  font-size: 14px;
  color: #8b5a3c;
  opacity: 0.8;
}

.price-section {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.price {
  font-family: 'Playfair Display', serif;
  font-size: 42px;
  font-weight: 600;
  color: #8b5a3c;
}

.negotiable {
  font-size: 14px;
  color: #8b5a3c;
  opacity: 0.7;
  font-weight: 500;
}

.condition {
  font-size: 16px;
  color: #8b5a3c;
  font-weight: 500;
}

.details-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 16px;
  background: rgba(139, 90, 60, 0.05);
  border-radius: 12px;
  border: 1px solid rgba(212, 175, 148, 0.3);
}

.detail-item label {
  font-size: 14px;
  color: #8b5a3c;
  font-weight: 500;
  opacity: 0.8;
}

.detail-item span {
  font-size: 16px;
  color: #8b5a3c;
  font-weight: 600;
}

.description-section h3 {
  margin: 0 0 16px 0;
  font-family: 'Playfair Display', serif;
  font-size: 24px;
  font-weight: 600;
  color: #8b5a3c;
}

.description {
  margin: 0;
  font-size: 16px;
  color: #8b5a3c;
  line-height: 1.6;
  opacity: 0.9;
}

.tags-section h3 {
  margin: 0 0 16px 0;
  font-family: 'Playfair Display', serif;
  font-size: 24px;
  font-weight: 600;
  color: #8b5a3c;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.tag {
  background: linear-gradient(135deg, #e8ddd4 0%, #d4af94 100%);
  color: #8b5a3c;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
  border: 1px solid #d4af94;
  box-shadow: 0 2px 8px rgba(139, 90, 60, 0.1);
}

.badges-section {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  border-radius: 25px;
  font-size: 14px;
  font-weight: 500;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.badge.authenticated {
  background: linear-gradient(135deg, #d4edda 0%, #a8e6cf 100%);
  color: #155724;
  border: 1px solid #a8e6cf;
}

.badge.negotiable {
  background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
  color: #856404;
  border: 1px solid #ffeaa7;
}

.item-actions {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  padding-top: 32px;
  border-top: 1px solid #d4af94;
}

.stats-section {
  background: linear-gradient(135deg, #f8f6f1 0%, #e8ddd4 100%);
  border-radius: 24px;
  border: 1px solid #d4af94;
  padding: 48px;
  box-shadow: 0 8px 25px rgba(139, 90, 60, 0.1);
}

.stats-section h2 {
  margin: 0 0 32px 0;
  font-family: 'Playfair Display', serif;
  font-size: 28px;
  font-weight: 600;
  color: #8b5a3c;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 32px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 24px;
  background: rgba(248, 246, 241, 0.7);
  border-radius: 16px;
  border: 1px solid rgba(212, 175, 148, 0.5);
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(139, 90, 60, 0.15);
  background: rgba(248, 246, 241, 1);
}

.stat-icon {
  font-size: 36px;
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #8b5a3c 0%, #a06749 100%);
  color: white;
  border-radius: 16px;
  box-shadow: 0 4px 15px rgba(139, 90, 60, 0.3);
}

.stat-content h3 {
  margin: 0 0 4px 0;
  font-family: 'Playfair Display', serif;
  font-size: 28px;
  font-weight: 600;
  color: #8b5a3c;
}

.stat-content p {
  margin: 0;
  font-size: 14px;
  color: #8b5a3c;
  font-weight: 500;
  opacity: 0.8;
}

/* Responsive */
@media (max-width: 768px) {
  .view-item {
    padding: 24px;
  }
  
  .page-header {
    flex-direction: column;
    gap: 20px;
    align-items: stretch;
    padding: 24px;
  }
  
  .header-actions {
    justify-content: center;
  }
  
  .item-container {
    grid-template-columns: 1fr;
    gap: 48px;
  }
  
  .item-title {
    font-size: 28px;
  }
  
  .price {
    font-size: 32px;
  }
  
  .details-grid {
    grid-template-columns: 1fr;
  }
  
  .item-actions {
    flex-direction: column;
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .thumbnail-grid {
    grid-template-columns: repeat(3, 1fr);
  }
  
  .stats-section {
    padding: 32px 24px;
  }
}

@media (max-width: 480px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .header-content {
    flex-direction: column;
    align-items: stretch;
    gap: 16px;
  }
  
  .stat-card {
    padding: 20px;
  }
  
  .item-title {
    font-size: 24px;
  }
  
  .price {
    font-size: 28px;
  }
}
</style>
