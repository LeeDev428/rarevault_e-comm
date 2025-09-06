<template>
  <SellerLayout>
    <div class="items-management">
      <!-- Page Header -->
      <div class="page-header">
        <div class="header-content">
          <h1 class="page-title">My Items</h1>
          <p class="page-subtitle">Manage your item listings</p>
        </div>
        
        <div class="header-actions">
          <ActionButton
            variant="primary"
            icon="➕"
            text="Add New Item"
            @click="goToCreateItem"
          />
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
                <th>Views</th>
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
                      <div class="image-placeholder">📷</div>
                    </div>
                    <div class="item-details">
                      <h4 class="item-title">{{ item.title }}</h4>
                      <p class="item-description">{{ item.description }}</p>
                    </div>
                  </div>
                </td>
                <td class="price">${{ item.price.toFixed(2) }}</td>
                <td class="category">{{ item.category }}</td>
                <td>
                  <span class="status-badge" :class="`status-${item.status}`">
                    {{ item.status }}
                  </span>
                </td>
                <td class="views">{{ item.views || 0 }}</td>
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
        
        // Get token and add better validation
        const token = localStorage.getItem('token');
        if (!token) {
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
        
        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}));
          console.error('API Error:', errorData);
          
          if (response.status === 401 || response.status === 403) {
            this.showToast('Authentication failed. Please log in again.', 'error', 'Authentication Error');
            this.$router.push('/login');
            return;
          }
          
          throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Fetched items:', data);
        this.items = data.items || [];
        
        if (this.items.length === 0) {
          this.showToast('No items found. Create your first item!', 'info', 'Getting Started');
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
    
    confirmDelete() {
      this.deleteLoading = true;
      
      setTimeout(() => {
        if (this.bulkDeleteMode) {
          // Remove selected items
          this.items = this.items.filter(item => !this.selectedItems.includes(item.id));
          this.showToast(`${this.selectedItems.length} items have been deleted.`, 'success', 'Items Deleted');
          this.selectedItems = [];
        } else {
          // Remove single item
          const index = this.items.findIndex(item => item.id === this.itemToDelete.id);
          if (index > -1) {
            this.items.splice(index, 1);
            this.showToast(`Item '${this.itemToDelete.title}' has been deleted.`, 'success', 'Item Deleted');
          }
        }
        
        this.deleteLoading = false;
        this.showDeleteModal = false;
        this.itemToDelete = null;
        this.bulkDeleteMode = false;
      }, 1500);
    },
    
    cancelDelete() {
      this.showDeleteModal = false;
      this.itemToDelete = null;
      this.bulkDeleteMode = false;
    },
    
    confirmBulkStatusUpdate() {
      this.bulkLoading = true;
      
      setTimeout(() => {
        // Update status for selected items
        this.items.forEach(item => {
          if (this.selectedItems.includes(item.id)) {
            item.status = this.bulkStatus;
          }
        });
        
        this.showToast(`${this.selectedItems.length} items updated to ${this.bulkStatus}.`, 'success', 'Status Updated');
        this.selectedItems = [];
        this.bulkLoading = false;
        this.showBulkStatusModal = false;
      }, 1000);
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
    }
  }
}
</script>

<style scoped>
.items-management {
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

.header-content h1 {
  margin: 0 0 8px 0;
  font-size: 32px;
  font-weight: 700;
  color: #343a40;
}

.header-content p {
  margin: 0;
  color: #6c757d;
  font-size: 16px;
}

.filters-section {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.search-box {
  position: relative;
  flex: 1;
  min-width: 250px;
}

.search-input {
  width: 100%;
  padding: 12px 16px 12px 40px;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  background: white;
  font-size: 14px;
}

.search-input:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
}

.search-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #6c757d;
  font-size: 16px;
}

.filter-controls {
  display: flex;
  gap: 12px;
}

.filter-select {
  padding: 12px 16px;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  background: white;
  font-size: 14px;
  min-width: 120px;
}

.filter-select:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
}

.items-table {
  background: white;
  border-radius: 12px;
  border: 1px solid #e9ecef;
  overflow: hidden;
  margin-bottom: 24px;
}

.table-container {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 16px;
  text-align: left;
  border-bottom: 1px solid #e9ecef;
}

th {
  background: #f8f9fa;
  font-weight: 600;
  color: #495057;
  font-size: 14px;
}

.item-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.item-image {
  width: 64px;
  height: 64px;
  flex-shrink: 0;
}

.image-placeholder {
  width: 100%;
  height: 100%;
  background: #f8f9fa;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: #6c757d;
}

.item-details {
  min-width: 0;
}

.item-title {
  margin: 0 0 4px 0;
  font-size: 16px;
  font-weight: 600;
  color: #343a40;
}

.item-description {
  margin: 0;
  font-size: 14px;
  color: #6c757d;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 200px;
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

.views {
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
