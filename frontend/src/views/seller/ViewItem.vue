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
                :src="selectedImage?.url || '/api/placeholder/400/400'" 
                :alt="item.title"
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
                <span>{{ item.category }}</span>
              </div>
              
              <div class="detail-item">
                <label>Views</label>
                <span>{{ item.views || 0 }}</span>
              </div>
              
              <div class="detail-item">
                <label>Favorites</label>
                <span>{{ item.favorites || 0 }}</span>
              </div>
              
              <div class="detail-item">
                <label>Inquiries</label>
                <span>{{ item.inquiries || 0 }}</span>
              </div>
            </div>

            <div class="description-section">
              <h3>Description</h3>
              <p class="description">{{ item.description }}</p>
            </div>

            <div v-if="item.tags && item.tags.length" class="tags-section">
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
          </div>
        </div>

        <!-- Stats Section -->
        <div class="stats-section">
          <h2>Item Performance</h2>
          <div class="stats-grid">
            <div class="stat-card">
              <div class="stat-icon">👁️</div>
              <div class="stat-content">
                <h3>{{ item.views || 0 }}</h3>
                <p>Views</p>
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
      </div>
            <div class="detail-item">
              <label>Category</label>
              <span>{{ item.category }}</span>
            </div>
            
            <div class="detail-item">
              <label>Views</label>
              <span>{{ item.views || 0 }}</span>
            </div>
            
            <div class="detail-item">
              <label>Favorites</label>
              <span>{{ item.favorites || 0 }}</span>
            </div>
            
            <div class="detail-item">
              <label>Inquiries</label>
              <span>{{ item.inquiries || 0 }}</span>
            </div>
          </div>

          <div class="description-section">
            <h3>Description</h3>
            <p class="description">{{ item.description }}</p>
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
        </div>
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
.view-item {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 1px solid #e9ecef;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.item-status .status-badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 16px;
  font-size: 12px;
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

.item-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 48px;
  margin-bottom: 48px;
}

.image-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.main-image {
  aspect-ratio: 1;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid #e9ecef;
}

.main-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.thumbnail-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}

.thumbnail {
  aspect-ratio: 1;
  border-radius: 8px;
  overflow: hidden;
  border: 2px solid transparent;
  cursor: pointer;
  transition: border-color 0.2s ease;
}

.thumbnail.active {
  border-color: #007bff;
}

.thumbnail:hover {
  border-color: #007bff;
}

.thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.details-section {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.item-header {
  padding-bottom: 16px;
  border-bottom: 1px solid #e9ecef;
}

.item-title {
  margin: 0 0 8px 0;
  font-size: 32px;
  font-weight: 700;
  color: #343a40;
  line-height: 1.2;
}

.item-meta {
  display: flex;
  gap: 16px;
  font-size: 14px;
  color: #6c757d;
}

.price-section {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.price {
  font-size: 36px;
  font-weight: 700;
  color: #28a745;
}

.negotiable {
  font-size: 14px;
  color: #6c757d;
  font-weight: 400;
}

.condition {
  font-size: 16px;
  color: #495057;
}

.details-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.detail-item label {
  font-size: 14px;
  color: #6c757d;
  font-weight: 500;
}

.detail-item span {
  font-size: 16px;
  color: #343a40;
  font-weight: 600;
}

.description-section h3 {
  margin: 0 0 12px 0;
  font-size: 20px;
  font-weight: 600;
  color: #343a40;
}

.description {
  margin: 0;
  font-size: 16px;
  color: #495057;
  line-height: 1.6;
}

.tags-section h3 {
  margin: 0 0 12px 0;
  font-size: 20px;
  font-weight: 600;
  color: #343a40;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag {
  background: #e3f2fd;
  color: #1976d2;
  padding: 6px 12px;
  border-radius: 16px;
  font-size: 14px;
  font-weight: 500;
}

.badges-section {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
}

.badge.authenticated {
  background: #d4edda;
  color: #155724;
}

.badge.negotiable {
  background: #fff3cd;
  color: #856404;
}

.item-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  padding-top: 24px;
  border-top: 1px solid #e9ecef;
}

.stats-section {
  background: white;
  border-radius: 12px;
  border: 1px solid #e9ecef;
  padding: 32px;
}

.stats-section h2 {
  margin: 0 0 24px 0;
  font-size: 24px;
  font-weight: 600;
  color: #343a40;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 24px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 12px;
  border: 1px solid #e9ecef;
}

.stat-icon {
  font-size: 32px;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border-radius: 12px;
}

.stat-content h3 {
  margin: 0 0 4px 0;
  font-size: 24px;
  font-weight: 700;
  color: #343a40;
}

.stat-content p {
  margin: 0;
  font-size: 14px;
  color: #6c757d;
  font-weight: 500;
}

/* Responsive */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }
  
  .header-actions {
    justify-content: center;
  }
  
  .item-container {
    grid-template-columns: 1fr;
    gap: 32px;
  }
  
  .item-title {
    font-size: 24px;
  }
  
  .price {
    font-size: 28px;
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
}

@media (max-width: 480px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .header-content {
    flex-direction: column;
    align-items: stretch;
    gap: 12px;
  }
}
</style>
