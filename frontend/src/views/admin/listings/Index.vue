<template>
  <div class="manage-listings">
    <div class="page-header">
      <h1>Manage Listings</h1>
      <p class="subtitle">View and manage all item listings in the marketplace</p>
    </div>

    <!-- Filters Section -->
    <div class="filters-section">
      <div class="filter-group">
        <label for="status-filter">Status</label>
        <select id="status-filter" v-model="filters.status" @change="fetchListings" class="filter-select">
          <option value="all">All Status</option>
          <option value="active">Active</option>
          <option value="pending">Pending</option>
          <option value="sold">Sold</option>
          <option value="removed">Removed</option>
        </select>
      </div>

      <div class="filter-group">
        <label for="category-filter">Category</label>
        <select id="category-filter" v-model="filters.category" @change="fetchListings" class="filter-select">
          <option value="all">All Categories</option>
          <option value="Antiques">Antiques</option>
          <option value="Coins & Currency">Coins & Currency</option>
          <option value="Collectibles">Collectibles</option>
          <option value="Vintage Item">Vintage Items</option>
          <option value="Art">Art</option>
          <option value="Books">Books</option>
        </select>
      </div>

      <div class="filter-group">
        <label for="search-filter">Search</label>
        <input 
          id="search-filter"
          type="text" 
          v-model="filters.search" 
          @input="debounceSearch"
          placeholder="Search by title or seller..."
          class="filter-input"
        >
      </div>

      <div class="filter-actions">
        <button @click="resetFilters" class="btn-secondary">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
          </svg>
          Reset Filters
        </button>
      </div>
    </div>

    <!-- Actions Bar -->
    <div class="actions-bar">
      <div class="selected-info" v-if="selectedListings.length > 0">
        <span>{{ selectedListings.length }} item(s) selected</span>
      </div>
      
      <div class="bulk-actions">
        <button 
          @click="bulkAction('activate')" 
          :disabled="selectedListings.length === 0"
          class="btn-success"
        >
          Activate Selected
        </button>
        <button 
          @click="bulkAction('deactivate')" 
          :disabled="selectedListings.length === 0"
          class="btn-warning"
        >
          Deactivate Selected
        </button>
        <button 
          @click="bulkAction('delete')" 
          :disabled="selectedListings.length === 0"
          class="btn-danger"
        >
          Delete Selected
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Loading listings...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-state">
      <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="12" cy="12" r="10"></circle>
        <line x1="12" y1="8" x2="12" y2="12"></line>
        <line x1="12" y1="16" x2="12.01" y2="16"></line>
      </svg>
      <h3>Failed to load listings</h3>
      <p>{{ error }}</p>
      <button @click="fetchListings" class="btn-primary">Try Again</button>
    </div>

    <!-- Listings Table -->
    <div v-else-if="filteredListings.length > 0" class="listings-table">
      <table>
        <thead>
          <tr>
            <th class="col-checkbox">
              <input 
                type="checkbox" 
                @change="toggleSelectAll"
                :checked="selectedListings.length === filteredListings.length"
              >
            </th>
            <th class="col-image">Image</th>
            <th class="col-title">Title</th>
            <th class="col-seller">Seller</th>
            <th class="col-category">Category</th>
            <th class="col-price">Price</th>
            <th class="col-stock">Stock</th>
            <th class="col-status">Status</th>
            <th class="col-date">Created</th>
            <th class="col-actions">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="listing in paginatedListings" :key="listing.id">
            <td class="col-checkbox">
              <input 
                type="checkbox" 
                :value="listing.id"
                v-model="selectedListings"
              >
            </td>
            <td class="col-image">
              <div class="listing-image">
                <img v-if="listing.image" :src="listing.image" :alt="listing.title">
                <div v-else class="no-image">📷</div>
              </div>
            </td>
            <td class="col-title">
              <div class="listing-title">{{ listing.title }}</div>
            </td>
            <td class="col-seller">{{ listing.seller }}</td>
            <td class="col-category">
              <span class="category-tag">{{ listing.category }}</span>
            </td>
            <td class="col-price">₱{{ formatPrice(listing.price) }}</td>
            <td class="col-stock">{{ listing.stock }}</td>
            <td class="col-status">
              <span class="status-badge" :class="listing.status">
                {{ listing.status }}
              </span>
            </td>
            <td class="col-date">{{ formatDate(listing.created_at) }}</td>
            <td class="col-actions">
              <div class="action-buttons">
                <button @click="viewListing(listing.id)" class="btn-icon" title="View">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                    <circle cx="12" cy="12" r="3"></circle>
                  </svg>
                </button>
                <button @click="editListing(listing.id)" class="btn-icon" title="Edit">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                    <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                  </svg>
                </button>
                <button @click="deleteListing(listing.id)" class="btn-icon btn-danger" title="Delete">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="3 6 5 6 21 6"></polyline>
                    <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                  </svg>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Empty State -->
    <div v-else class="empty-state">
      <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1">
        <rect x="3" y="3" width="7" height="7"></rect>
        <rect x="14" y="3" width="7" height="7"></rect>
        <rect x="14" y="14" width="7" height="7"></rect>
        <rect x="3" y="14" width="7" height="7"></rect>
      </svg>
      <h3>No listings found</h3>
      <p>Try adjusting your filters or search terms</p>
    </div>

    <!-- Pagination -->
    <div v-if="totalPages > 1" class="pagination">
      <button 
        @click="currentPage--" 
        :disabled="currentPage === 1"
        class="btn-page"
      >
        Previous
      </button>
      
      <div class="page-numbers">
        <button 
          v-for="page in visiblePages" 
          :key="page"
          @click="currentPage = page"
          :class="['btn-page', { active: currentPage === page }]"
        >
          {{ page }}
        </button>
      </div>
      
      <button 
        @click="currentPage++" 
        :disabled="currentPage === totalPages"
        class="btn-page"
      >
        Next
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ManageListings',
  data() {
    return {
      listings: [],
      selectedListings: [],
      loading: true,
      error: null,
      filters: {
        status: 'all',
        category: 'all',
        search: ''
      },
      currentPage: 1,
      itemsPerPage: 20,
      searchTimeout: null
    }
  },
  async mounted() {
    await this.fetchListings()
  },
  computed: {
    filteredListings() {
      let filtered = [...this.listings]

      // Filter by search
      if (this.filters.search) {
        const search = this.filters.search.toLowerCase()
        filtered = filtered.filter(listing => 
          listing.title.toLowerCase().includes(search) ||
          listing.seller.toLowerCase().includes(search)
        )
      }

      // Filter by category
      if (this.filters.category !== 'all') {
        filtered = filtered.filter(listing => listing.category === this.filters.category)
      }

      return filtered
    },
    paginatedListings() {
      const start = (this.currentPage - 1) * this.itemsPerPage
      const end = start + this.itemsPerPage
      return this.filteredListings.slice(start, end)
    },
    totalPages() {
      return Math.ceil(this.filteredListings.length / this.itemsPerPage)
    },
    visiblePages() {
      const pages = []
      const total = this.totalPages
      const current = this.currentPage
      
      if (total <= 7) {
        for (let i = 1; i <= total; i++) pages.push(i)
      } else {
        if (current <= 4) {
          for (let i = 1; i <= 5; i++) pages.push(i)
          pages.push('...')
          pages.push(total)
        } else if (current >= total - 3) {
          pages.push(1)
          pages.push('...')
          for (let i = total - 4; i <= total; i++) pages.push(i)
        } else {
          pages.push(1)
          pages.push('...')
          for (let i = current - 1; i <= current + 1; i++) pages.push(i)
          pages.push('...')
          pages.push(total)
        }
      }
      
      return pages
    }
  },
  methods: {
    async fetchListings() {
      try {
        this.loading = true
        this.error = null
        const token = localStorage.getItem('access_token') || localStorage.getItem('token')
        
        const statusParam = this.filters.status === 'all' ? 'all' : this.filters.status
        const response = await fetch(`http://localhost:5000/api/admin/items?status=${statusParam}`, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })

        const data = await response.json()

        if (!response.ok) {
          throw new Error(data.error || 'Failed to fetch listings')
        }

        if (data.items && Array.isArray(data.items)) {
          this.listings = data.items.map(item => ({
            id: item.id,
            title: item.title,
            seller: item.posted_by || 'Unknown',
            category: item.category || 'N/A',
            price: item.price,
            stock: item.stock,
            status: item.status,
            image: item.primary_image?.url || item.images?.[0]?.url || null,
            created_at: item.created_at
          }))
          console.log('Successfully loaded', this.listings.length, 'listings')
        } else {
          throw new Error('Invalid response format: items array not found')
        }
      } catch (error) {
        console.error('Fetch listings error:', error)
        this.error = error.message
        this.listings = []
      } finally {
        this.loading = false
      }
    },
    
    debounceSearch() {
      clearTimeout(this.searchTimeout)
      this.searchTimeout = setTimeout(() => {
        this.currentPage = 1
      }, 300)
    },
    
    resetFilters() {
      this.filters = {
        status: 'all',
        category: 'all',
        search: ''
      }
      this.currentPage = 1
      this.fetchListings()
    },
    
    toggleSelectAll(event) {
      if (event.target.checked) {
        this.selectedListings = this.filteredListings.map(l => l.id)
      } else {
        this.selectedListings = []
      }
    },
    
    async bulkAction(action) {
      if (this.selectedListings.length === 0) return

      const confirmMessages = {
        activate: 'Are you sure you want to activate the selected listings?',
        deactivate: 'Are you sure you want to deactivate the selected listings?',
        delete: 'Are you sure you want to DELETE the selected listings? This cannot be undone!'
      }

      if (!confirm(confirmMessages[action])) return

      try {
        const token = localStorage.getItem('access_token') || localStorage.getItem('token')
        
        if (action === 'delete') {
          // Delete each selected listing
          await Promise.all(this.selectedListings.map(id => 
            fetch(`http://localhost:5000/api/admin/items/${id}`, {
              method: 'DELETE',
              headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
              }
            })
          ))
          alert(`${this.selectedListings.length} listing(s) deleted successfully`)
        } else {
          // Update status for each selected listing
          const newStatus = action === 'activate' ? 'active' : 'removed'
          await Promise.all(this.selectedListings.map(id => 
            fetch(`http://localhost:5000/api/admin/items/${id}`, {
              method: 'PATCH',
              headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
              },
              body: JSON.stringify({ status: newStatus })
            })
          ))
          alert(`${this.selectedListings.length} listing(s) ${action}d successfully`)
        }

        this.selectedListings = []
        await this.fetchListings()
      } catch (error) {
        console.error('Bulk action error:', error)
        alert('Failed to perform bulk action: ' + error.message)
      }
    },
    
    viewListing(id) {
      // Navigate to item details
      this.$router.push(`/admin/listings/${id}`)
    },
    
    editListing(id) {
      // Navigate to edit page
      this.$router.push(`/admin/listings/edit/${id}`)
    },
    
    async deleteListing(id) {
      if (!confirm('Are you sure you want to delete this listing?')) return

      try {
        const token = localStorage.getItem('access_token') || localStorage.getItem('token')
        
        const response = await fetch(`http://localhost:5000/api/admin/items/${id}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })

        const data = await response.json()

        if (!response.ok) {
          throw new Error(data.error || 'Failed to delete listing')
        }

        alert('Listing deleted successfully')
        await this.fetchListings()
      } catch (error) {
        console.error('Delete listing error:', error)
        alert('Failed to delete listing: ' + error.message)
      }
    },
    
    formatPrice(price) {
      return parseFloat(price).toLocaleString('en-US', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      })
    },
    
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    }
  }
}
</script>

<style scoped>
.manage-listings {
  max-width: 1400px;
  margin: 0 auto;
  padding: 32px 24px;
}

/* Page Header */
.page-header {
  margin-bottom: 32px;
}

.page-header h1 {
  font-size: 32px;
  font-weight: 700;
  color: #212529;
  margin: 0 0 8px 0;
}

.subtitle {
  font-size: 16px;
  color: #6c757d;
  margin: 0;
}

/* Filters Section */
.filters-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  padding: 24px;
  background: white;
  border-radius: 12px;
  border: 1px solid #e9ecef;
  margin-bottom: 24px;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.filter-group label {
  font-size: 14px;
  font-weight: 500;
  color: #495057;
}

.filter-select,
.filter-input {
  padding: 10px 14px;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  font-size: 14px;
  color: #212529;
  background: white;
  transition: all 0.2s;
}

.filter-select:focus,
.filter-input:focus {
  outline: none;
  border-color: #0d6efd;
  box-shadow: 0 0 0 3px rgba(13, 110, 253, 0.1);
}

.filter-actions {
  display: flex;
  align-items: flex-end;
}

/* Actions Bar */
.actions-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  background: white;
  border-radius: 12px;
  border: 1px solid #e9ecef;
  margin-bottom: 24px;
}

.selected-info {
  font-size: 14px;
  font-weight: 500;
  color: #495057;
}

.bulk-actions {
  display: flex;
  gap: 12px;
}

/* Buttons */
.btn-primary,
.btn-secondary,
.btn-success,
.btn-warning,
.btn-danger {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-primary {
  background: #0d6efd;
  color: white;
}

.btn-primary:hover {
  background: #0b5ed7;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #5c636a;
}

.btn-success {
  background: #198754;
  color: white;
}

.btn-success:hover:not(:disabled) {
  background: #157347;
}

.btn-warning {
  background: #ffc107;
  color: #000;
}

.btn-warning:hover:not(:disabled) {
  background: #ffca2c;
}

.btn-danger {
  background: #dc3545;
  color: white;
}

.btn-danger:hover:not(:disabled) {
  background: #bb2d3b;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Loading State */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 24px;
  background: white;
  border-radius: 12px;
  border: 1px solid #e9ecef;
}

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #f1f3f4;
  border-top-color: #0d6efd;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-state p {
  margin-top: 16px;
  font-size: 16px;
  color: #6c757d;
}

/* Error State */
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 24px;
  background: white;
  border-radius: 12px;
  border: 1px solid #e9ecef;
}

.error-state svg {
  color: #dc3545;
  margin-bottom: 16px;
}

.error-state h3 {
  font-size: 20px;
  font-weight: 600;
  color: #212529;
  margin: 0 0 8px 0;
}

.error-state p {
  font-size: 14px;
  color: #6c757d;
  margin: 0 0 24px 0;
}

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 24px;
  background: white;
  border-radius: 12px;
  border: 1px solid #e9ecef;
}

.empty-state svg {
  color: #adb5bd;
  margin-bottom: 16px;
}

.empty-state h3 {
  font-size: 20px;
  font-weight: 600;
  color: #212529;
  margin: 0 0 8px 0;
}

.empty-state p {
  font-size: 14px;
  color: #6c757d;
  margin: 0;
}

/* Table */
.listings-table {
  background: white;
  border-radius: 12px;
  border: 1px solid #e9ecef;
  overflow: hidden;
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background: #f8f9fa;
  border-bottom: 2px solid #dee2e6;
}

th {
  padding: 16px 12px;
  text-align: left;
  font-size: 13px;
  font-weight: 600;
  color: #495057;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

tbody tr {
  border-bottom: 1px solid #f1f3f4;
  transition: background-color 0.2s;
}

tbody tr:hover {
  background: #f8f9fa;
}

td {
  padding: 16px 12px;
  font-size: 14px;
  color: #495057;
  vertical-align: middle;
}

.col-checkbox {
  width: 40px;
}

.col-image {
  width: 80px;
}

.col-title {
  min-width: 200px;
}

.col-seller,
.col-category {
  width: 150px;
}

.col-price,
.col-stock {
  width: 100px;
}

.col-status {
  width: 120px;
}

.col-date {
  width: 120px;
}

.col-actions {
  width: 140px;
}

/* Listing Image */
.listing-image {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  overflow: hidden;
  background: #f8f9fa;
  display: flex;
  align-items: center;
  justify-content: center;
}

.listing-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.no-image {
  font-size: 24px;
  color: #adb5bd;
}

/* Listing Title */
.listing-title {
  font-weight: 500;
  color: #212529;
  line-height: 1.4;
}

/* Category Tag */
.category-tag {
  padding: 4px 10px;
  background: #e7f1ff;
  color: #0d6efd;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
}

/* Status Badge */
.status-badge {
  padding: 6px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  text-transform: capitalize;
}

.status-badge.active {
  background: #d4edda;
  color: #155724;
}

.status-badge.pending {
  background: #fff3cd;
  color: #856404;
}

.status-badge.sold {
  background: #d1ecf1;
  color: #0c5460;
}

.status-badge.removed {
  background: #f8d7da;
  color: #721c24;
}

/* Action Buttons */
.action-buttons {
  display: flex;
  gap: 8px;
}

.btn-icon {
  padding: 8px;
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-icon:hover {
  background: #e9ecef;
  border-color: #adb5bd;
}

.btn-icon.btn-danger:hover {
  background: #dc3545;
  border-color: #dc3545;
  color: white;
}

.btn-icon svg {
  display: block;
}

/* Pagination */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
  margin-top: 32px;
}

.page-numbers {
  display: flex;
  gap: 8px;
}

.btn-page {
  padding: 8px 16px;
  background: white;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  font-size: 14px;
  color: #495057;
  cursor: pointer;
  transition: all 0.2s;
  min-width: 40px;
}

.btn-page:hover:not(:disabled):not(.active) {
  background: #f8f9fa;
  border-color: #adb5bd;
}

.btn-page.active {
  background: #0d6efd;
  border-color: #0d6efd;
  color: white;
}

.btn-page:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .col-category,
  .col-date {
    display: none;
  }
}

@media (max-width: 768px) {
  .manage-listings {
    padding: 24px 16px;
  }

  .filters-section {
    grid-template-columns: 1fr;
  }

  .actions-bar {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }

  .bulk-actions {
    flex-direction: column;
  }

  .col-seller,
  .col-stock {
    display: none;
  }

  .listings-table {
    overflow-x: auto;
  }

  table {
    min-width: 600px;
  }
}
</style>
