<template>
  <SellerLayout>
    <div class="items-management">
      <!-- Page Header -->
      <div class="page-header">
        <div class="header-content">
          <h1 class="page-title">My Items</h1>
          <p class="page-subtitle">Manage your item listings</p>
        </div>
     
      </div>

      <!-- Filters and Search -->
      <div class="filters-section">
        <div class="search-box">
          <input 
            v-model="searchQuery"
            type="text"
            placeholder="Search items..."
            class="search-input"
          >
          <i class="search-icon">🔍</i>
        </div>
        
        <div class="filter-controls">
          <select v-model="statusFilter" class="filter-select">
            <option value="">All Status</option>
            <option value="active">Active</option>
            <option value="pending">Pending</option>
            <option value="sold">Sold</option>
            <option value="removed">Removed</option>
          </select>
          
          <select v-model="categoryFilter" class="filter-select">
            <option value="">All Categories</option>
            <option value="Watches">Watches</option>
            <option value="Antiques">Antiques</option>
            <option value="Coins">Coins</option>
            <option value="Art">Art</option>
            <option value="Jewelry">Jewelry</option>
          </select>
        </div>
      </div>

      <!-- Items Table -->
      <div class="items-table">
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>
                  <input 
                    type="checkbox" 
                    v-model="selectAll"
                    @change="toggleSelectAll"
                  >
                </th>
                <th>Item</th>
                <th>Price</th>
                <th>Category</th>
                <th>Status</th>
                <th>Stock</th>
                <th>Created</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="filteredItems.length === 0">
                <td colspan="8" class="empty-state">
                  <div class="empty-content">
                    <i class="empty-icon">📦</i>
                    <p v-if="searchQuery || statusFilter || categoryFilter">
                      No items found matching your filters.
                    </p>
                    <p v-else>
                      No items yet. Create your first item to get started!
                    </p>
                    <ActionButton
                      variant="primary"
                      icon="➕"
                      text="Create Item"
                      @click="goToCreateItem"
                    />
                  </div>
                </td>
              </tr>
              <tr v-for="item in filteredItems" :key="item.id">
                <td>
                  <input 
                    type="checkbox" 
                    v-model="selectedItems"
                    :value="item.id"
                  >
                </td>
                <td>
                  <div class="item-info">
                    <div class="item-image">
                      <img 
                        :src="getItemImage(item)" 
                        :alt="item.title"
                        @error="handleImageError"
                      />
                    </div>
                    <div class="item-details">
                      <div class="item-main-info">
                        <h4 class="item-title">{{ item.title }}</h4>
                        <p class="item-description">{{ item.description }}</p>
                      </div>
                      <div class="item-stats">
                        <div class="stat-item">
                          <div class="rating-display">
                            <div class="stars">
                              <span 
                                v-for="n in 5" 
                                :key="n"
                                class="star"
                                :class="{ filled: n <= Math.round(item.average_rating || 0) }"
                              >
                                ★
                              </span>
                            </div>
                            <span class="rating-value">{{ (item.average_rating || 0).toFixed(1) }}</span>
                          </div>
                        </div>
                        <div class="stat-item">
                          <span class="sold-count">Sold: {{ item.sold_count || 0 }}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </td>
                <td class="price">₱{{ item.price.toFixed(2) }}</td>
                <td class="category">{{ item.category }}</td>
                <td>
                  <span class="status-badge" :class="`status-${item.status}`">
                    {{ item.status }}
                  </span>
                </td>
                <td class="stock">{{ item.stock || 0 }}</td>
                <td class="date">{{ formatDate(item.created_at) }}</td>
                <td>
                  <div class="action-buttons">
                    <ActionButton
                      variant="info"
                      icon="👁️"
                      text="View"
                      @click="viewItem(item)"
                    />
                    <ActionButton
                      variant="secondary"
                      icon="✏️"
                      text="Edit"
                      @click="editItem(item)"
                    />
                    <ActionButton
                      variant="danger"
                      icon="🗑️"
                      text="Delete"
                      @click="deleteItem(item)"
                    />
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Bulk Actions -->
      <div v-if="selectedItems.length > 0" class="bulk-actions">
        <div class="bulk-info">
          {{ selectedItems.length }} item(s) selected
        </div>
        <div class="bulk-buttons">
          <ActionButton
            variant="warning"
            icon="📦"
            text="Bulk Update Status"
            @click="showBulkStatusModal = true"
          />
          <ActionButton
            variant="danger"
            icon="🗑️"
            text="Delete Selected"
            @click="bulkDelete"
          />
        </div>
      </div>
    </div>

    <!-- Bulk Status Update Modal -->
    <div v-if="showBulkStatusModal" class="modal-overlay" @click="showBulkStatusModal = false">
      <div class="bulk-modal" @click.stop>
        <div class="modal-header">
          <h3>Update Status for {{ selectedItems.length }} items</h3>
          <button class="close-btn" @click="showBulkStatusModal = false">×</button>
        </div>
        <div class="modal-body">
          <label class="form-label">New Status:</label>
          <select v-model="bulkStatus" class="form-select">
            <option value="active">Active</option>
            <option value="pending">Pending</option>
            <option value="sold">Sold</option>
            <option value="removed">Removed</option>
          </select>
        </div>
        <div class="modal-footer">
          <ActionButton
            variant="secondary"
            icon="❌"
            text="Cancel"
            @click="showBulkStatusModal = false"
          />
          <ActionButton
            variant="primary"
            icon="✅"
            text="Update"
            :loading="bulkLoading"
            @click="confirmBulkStatusUpdate"
          />
        </div>
      </div>
    </div>

    <!-- Confirmation Modal -->
    <ConfirmationModal
      :show="showDeleteModal"
      :title="bulkDeleteMode ? 'Delete Multiple Items' : 'Delete Item'"
      :message="bulkDeleteMode 
        ? `Are you sure you want to delete ${selectedItems.length} selected items? This action cannot be undone.`
        : `Are you sure you want to delete '${itemToDelete?.title}'? This action cannot be undone.`"
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
  name: 'ItemsManagement',
  components: {
    SellerLayout,
    ActionButton,
    ConfirmationModal,
    MessageToast
  },
  data() {
    return {
      searchQuery: '',
      statusFilter: '',
      categoryFilter: '',
      selectedItems: [],
      selectAll: false,
      items: [],
      loading: true,
      showDeleteModal: false,
      itemToDelete: null,
      deleteLoading: false,
      bulkDeleteMode: false,
      showBulkStatusModal: false,
      bulkStatus: 'active',
      bulkLoading: false,
      showMessage: false,
      messageType: 'info',
      messageTitle: '',
      messageText: ''
    }
  },
  
  mounted() {
    this.fetchItems();
  },
  
  computed: {
    filteredItems() {
      let filtered = this.items;
      
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        filtered = filtered.filter(item => 
          item.title.toLowerCase().includes(query) ||
          item.description.toLowerCase().includes(query) ||
          item.category.toLowerCase().includes(query)
        );
      }
      
      if (this.statusFilter) {
        filtered = filtered.filter(item => item.status === this.statusFilter);
      }
      
      if (this.categoryFilter) {
        filtered = filtered.filter(item => item.category === this.categoryFilter);
      }
      
      return filtered;
    }
  },
  
  watch: {
    selectedItems() {
      this.selectAll = this.selectedItems.length === this.filteredItems.length && this.filteredItems.length > 0;
    }
  },
  methods: {
    async fetchItems() {
      try {
        this.loading = true;
        
        // Get token with proper priority (access_token is what login stores)
        const token = localStorage.getItem('access_token') || localStorage.getItem('token') || localStorage.getItem('jwt_token');
        if (!token) {
          console.error('No authentication token found');
          this.showToast('Please log in to view your items.', 'error', 'Authentication Required');
          this.$router.push('/login');
          return;
        }
        
        console.log('Fetching items with token:', token.substring(0, 20) + '...');
        
        const response = await fetch('http://localhost:5000/api/seller/items', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });
        
        console.log('Response status:', response.status);
        console.log('Response headers:', Object.fromEntries(response.headers.entries()));
        
        if (!response.ok) {
          let errorData;
          const contentType = response.headers.get('content-type');
          
          if (contentType && contentType.includes('application/json')) {
            errorData = await response.json();
          } else {
            const textData = await response.text();
            console.error('Non-JSON response:', textData);
            errorData = { error: `Server returned: ${textData}` };
          }
          
          console.error('API Error Details:', {
            status: response.status,
            statusText: response.statusText,
            error: errorData,
            headers: Object.fromEntries(response.headers.entries())
          });
          
          // Only redirect to login for actual authentication errors
          if (response.status === 401) {
            this.showToast('Session expired. Please log in again.', 'error', 'Authentication Error');
            localStorage.removeItem('access_token');
            localStorage.removeItem('token'); 
            localStorage.removeItem('jwt_token');
            localStorage.removeItem('user_role');
            localStorage.removeItem('user_info');
            this.$router.push('/login');
            return;
          }
          
          if (response.status === 403) {
            this.showToast('Access denied. Make sure you have seller permissions.', 'error', 'Access Denied');
            return;
          }
          
          if (response.status === 422) {
            console.warn('422 Validation Error - but not redirecting to login');
            this.showToast(`Request validation failed: ${errorData.error || 'Please check your request'}`, 'error', 'Validation Error');
            return;
          }
          
          throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Fetched items:', data);
        this.items = data.items || [];
        
        if (this.items.length === 0) {
          this.showToast('No items found. Create your first item!', 'info', 'Getting Started');
        } else {
          console.log(`Successfully loaded ${this.items.length} items`);
        }
        
      } catch (error) {
        console.error('Error fetching items:', error);
        this.showToast(`Failed to load items: ${error.message}`, 'error', 'Load Failed');
      } finally {
        this.loading = false;
      }
    },
    
    goToCreateItem() {
      this.$router.push('/seller/create-product');
    },
    
    toggleSelectAll() {
      if (this.selectAll) {
        this.selectedItems = this.filteredItems.map(item => item.id);
      } else {
        this.selectedItems = [];
      }
    },
    
    viewItem(item) {
      this.$router.push(`/seller/items/${item.id}`);
    },
    
    editItem(item) {
      this.$router.push(`/seller/products/${item.id}/edit`);
    },
    
    deleteItem(item) {
      this.itemToDelete = item;
      this.bulkDeleteMode = false;
      this.showDeleteModal = true;
    },
    
    bulkDelete() {
      if (this.selectedItems.length === 0) return;
      this.bulkDeleteMode = true;
      this.showDeleteModal = true;
    },
    
    async confirmDelete() {
      try {
        this.deleteLoading = true;
        const token = localStorage.getItem('access_token') || localStorage.getItem('token') || localStorage.getItem('jwt_token');
        
        if (this.bulkDeleteMode) {
          // Delete multiple items
          const deletePromises = this.selectedItems.map(itemId =>
            fetch(`http://localhost:5000/api/seller/items/${itemId}`, {
              method: 'DELETE',
              headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
              }
            })
          );
          
          await Promise.all(deletePromises);
          
          // Remove items from local state
          this.items = this.items.filter(item => !this.selectedItems.includes(item.id));
          this.showToast(`${this.selectedItems.length} items have been deleted.`, 'success', 'Items Deleted');
          this.selectedItems = [];
        } else {
          // Delete single item
          const response = await fetch(`http://localhost:5000/api/seller/items/${this.itemToDelete.id}`, {
            method: 'DELETE',
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
            }
          });
          
          if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.error || 'Failed to delete item');
          }
          
          // Remove item from local state
          const index = this.items.findIndex(item => item.id === this.itemToDelete.id);
          if (index > -1) {
            this.items.splice(index, 1);
          }
          this.showToast(`Item '${this.itemToDelete.title}' has been deleted.`, 'success', 'Item Deleted');
        }
        
      } catch (error) {
        console.error('Delete error:', error);
        this.showToast(`Failed to delete: ${error.message}`, 'error', 'Delete Failed');
      } finally {
        this.deleteLoading = false;
        this.showDeleteModal = false;
        this.itemToDelete = null;
        this.bulkDeleteMode = false;
      }
    },
    
    cancelDelete() {
      this.showDeleteModal = false;
      this.itemToDelete = null;
      this.bulkDeleteMode = false;
    },
    
    async confirmBulkStatusUpdate() {
      try {
        this.bulkLoading = true;
        const token = localStorage.getItem('access_token') || localStorage.getItem('token') || localStorage.getItem('jwt_token');
        
        // Update status for selected items via API
        const updatePromises = this.selectedItems.map(itemId => {
          const item = this.items.find(i => i.id === itemId);
          return fetch(`http://localhost:5000/api/seller/items/${itemId}`, {
            method: 'PUT',
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              status: this.bulkStatus
            })
          });
        });
        
        await Promise.all(updatePromises);
        
        // Update local state
        this.items.forEach(item => {
          if (this.selectedItems.includes(item.id)) {
            item.status = this.bulkStatus;
          }
        });
        
        this.showToast(`${this.selectedItems.length} items updated to ${this.bulkStatus}.`, 'success', 'Status Updated');
        this.selectedItems = [];
        
      } catch (error) {
        console.error('Bulk update error:', error);
        this.showToast(`Failed to update items: ${error.message}`, 'error', 'Update Failed');
      } finally {
        this.bulkLoading = false;
        this.showBulkStatusModal = false;
      }
    },
    
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric'
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
    },

    getItemImage(item) {
      // Handle primary image from API - priority to primary image
      if (item?.images && Array.isArray(item.images) && item.images.length > 0) {
        const primaryImage = item.images.find(img => img.is_primary || img.isPrimary);
        if (primaryImage?.image_url) {
          return primaryImage.image_url;
        }
        if (primaryImage?.url) {
          return primaryImage.url;
        }
        // Fallback to first image
        if (item.images[0]?.image_url) {
          return item.images[0].image_url;
        }
        if (item.images[0]?.url) {
          return item.images[0].url;
        }
      }
      // Handle primary_image object from API
      if (item?.primary_image?.image_url) {
        return item.primary_image.image_url;
      }
      if (item?.primary_image?.url) {
        return item.primary_image.url;
      }
      // Handle direct image_url property
      if (item?.image_url) {
        return item.image_url;
      }
      // Handle single image property
      if (item?.image) {
        return item.image;
      }
      return 'http://localhost:5000/uploads/placeholder.svg';
    },

    handleImageError(event) {
      event.target.src = 'http://localhost:5000/uploads/placeholder.svg';
    }
  }
}
</script>

<style scoped>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

.items-management {
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

.header-content h1 {
  margin: 0 0 8px 0;
  font-family: 'Playfair Display', serif;
  font-size: 36px;
  font-weight: 600;
  color: #8b5a3c;
  text-shadow: 0 2px 4px rgba(139, 90, 60, 0.1);
}

.header-content p {
  margin: 0;
  color: #8b5a3c;
  font-size: 16px;
  opacity: 0.8;
}

.filters-section {
  display: flex;
  gap: 24px;
  margin-bottom: 32px;
  flex-wrap: wrap;
  padding: 24px;
  background: linear-gradient(135deg, #f8f6f1 0%, #e8ddd4 100%);
  border-radius: 20px;
  border: 1px solid #d4af94;
}

.search-box {
  position: relative;
  flex: 1;
  min-width: 300px;
}

.search-input {
  width: 100%;
  padding: 16px 16px 16px 48px;
  border: 1px solid #d4af94;
  border-radius: 12px;
  background: rgba(248, 246, 241, 0.7);
  font-size: 14px;
  color: #8b5a3c;
  transition: all 0.3s ease;
  font-family: 'Inter', sans-serif;
}

.search-input:focus {
  outline: none;
  border-color: #8b5a3c;
  box-shadow: 0 0 0 3px rgba(139, 90, 60, 0.1);
  background: rgba(248, 246, 241, 1);
}

.search-input::placeholder {
  color: #8b5a3c;
  opacity: 0.6;
}

.search-icon {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  color: #8b5a3c;
  font-size: 18px;
  opacity: 0.7;
}

.filter-controls {
  display: flex;
  gap: 16px;
}

.filter-select {
  padding: 16px;
  border: 1px solid #d4af94;
  border-radius: 12px;
  background: rgba(248, 246, 241, 0.7);
  font-size: 14px;
  min-width: 150px;
  color: #8b5a3c;
  font-family: 'Inter', sans-serif;
  transition: all 0.3s ease;
}

.filter-select:focus {
  outline: none;
  border-color: #8b5a3c;
  box-shadow: 0 0 0 3px rgba(139, 90, 60, 0.1);
  background: rgba(248, 246, 241, 1);
}

.items-table {
  background: linear-gradient(135deg, #f8f6f1 0%, #e8ddd4 100%);
  border-radius: 20px;
  border: 1px solid #d4af94;
  overflow: hidden;
  margin-bottom: 32px;
  box-shadow: 0 8px 25px rgba(139, 90, 60, 0.1);
}

.table-container {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 20px;
  text-align: left;
  border-bottom: 1px solid #e8ddd4;
}

th {
  background: linear-gradient(135deg, #8b5a3c 0%, #d4af94 100%);
  font-family: 'Playfair Display', serif;
  font-weight: 600;
  color: #f8f6f1;
  font-size: 16px;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

th:first-child {
  border-top-left-radius: 20px;
}

th:last-child {
  border-top-right-radius: 20px;
}

td {
  background: rgba(248, 246, 241, 0.7);
  color: #8b5a3c;
}

.item-info {
  display: flex;
  align-items: center;
  gap: 16px;
}

.item-image {
  width: 72px;
  height: 72px;
  flex-shrink: 0;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid #d4af94;
  box-shadow: 0 2px 8px rgba(139, 90, 60, 0.1);
}

.item-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #e8ddd4 0%, #d4af94 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: #8b5a3c;
  opacity: 0.7;
}

.item-details {
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.item-main-info {
  flex: 1;
}

.item-title {
  margin: 0 0 4px 0;
  font-family: 'Playfair Display', serif;
  font-size: 18px;
  font-weight: 600;
  color: #8b5a3c;
}

.item-description {
  margin: 0;
  font-size: 14px;
  color: #8b5a3c;
  opacity: 0.8;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 220px;
}

.item-stats {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-top: 4px;
}

.stat-item {
  display: flex;
  align-items: center;
  font-size: 12px;
}

.rating-display {
  display: flex;
  align-items: center;
  gap: 4px;
}

.stars {
  display: flex;
  gap: 1px;
}

.star {
  color: #ddd;
  font-size: 12px;
  transition: color 0.2s;
}

.star.filled {
  color: #ffc107;
}

.rating-value {
  color: #6c757d;
  font-weight: 500;
  margin-left: 2px;
}

.sold-count {
  color: #28a745;
  font-weight: 500;
}

.price {
  font-weight: 600;
  color: #28a745;
  font-size: 16px;
}

.category {
  color: #495057;
  font-weight: 500;
}

.status-badge {
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

.status-pending {
  background: #fff3cd;
  color: #856404;
}

.status-sold {
  background: #d1ecf1;
  color: #0c5460;
}

.status-removed {
  background: #f8d7da;
  color: #721c24;
}

.stock {
  color: #6c757d;
  font-weight: 500;
}

.date {
  color: #6c757d;
  font-size: 14px;
}

.action-buttons {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.bulk-actions {
  background: white;
  padding: 16px 24px;
  border-radius: 8px;
  border: 1px solid #e9ecef;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 16px;
}

.bulk-info {
  font-weight: 500;
  color: #495057;
}

.bulk-buttons {
  display: flex;
  gap: 12px;
}

.empty-state {
  text-align: center;
  padding: 48px 24px;
}

.empty-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.empty-icon {
  font-size: 64px;
  opacity: 0.5;
}

.empty-content p {
  margin: 0;
  color: #6c757d;
  font-size: 16px;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1060;
  padding: 20px;
}

.bulk-modal {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  max-width: 400px;
  width: 100%;
  animation: modalSlideIn 0.3s ease;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #e9ecef;
}

.modal-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #343a40;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #6c757d;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
}

.close-btn:hover {
  background: #f8f9fa;
  color: #343a40;
}

.modal-body {
  padding: 24px;
}

.form-label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #495057;
}

.form-select {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  background: white;
  font-size: 14px;
}

.form-select:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
}

.modal-footer {
  display: flex;
  gap: 12px;
  padding: 0 24px 24px;
  justify-content: flex-end;
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: scale(0.9) translateY(-20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

/* Responsive */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }
  
  .filters-section {
    flex-direction: column;
  }
  
  .filter-controls {
    flex-direction: column;
  }
  
  .bulk-actions {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }
  
  .bulk-buttons {
    justify-content: center;
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  .item-description {
    max-width: 150px;
  }
}
</style>
