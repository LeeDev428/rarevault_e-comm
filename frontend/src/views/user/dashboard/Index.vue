<template>
  <UserLayout>
    <div class="marketplace-container">
      <!-- Left Sidebar Filters -->
      <aside class="filter-sidebar">
        <div class="filter-section">
          <h3 class="filter-title">Filter</h3>
          
          <!-- Search Box -->
          <div class="filter-group">
            <div class="search-box">
              <input 
                v-model="searchQuery"
                type="text"
                placeholder="Search items..."
                class="search-input"
                @input="debouncedSearch"
              >
              <i class="search-icon">🔍</i>
            </div>
          </div>

          <!-- Category Filters -->
          <div class="filter-group">
            <h4 class="filter-subtitle">Categories</h4>
            <div class="filter-item" 
                 v-for="category in availableCategories" 
                 :key="category"
                 @click="toggleCategory(category)"
                 :class="{ active: selectedCategory === category }">
              <span>{{ formatCategoryName(category) }}</span>
            </div>
            <div class="filter-item" 
                 @click="clearCategoryFilter"
                 :class="{ active: !selectedCategory }">
              <span>All Categories</span>
            </div>
          </div>

          <!-- Condition Filter -->
          <div class="filter-group">
            <h4 class="filter-subtitle">Condition</h4>
            <div class="filter-item" 
                 v-for="condition in availableConditions" 
                 :key="condition"
                 @click="toggleCondition(condition)"
                 :class="{ active: selectedCondition === condition }">
              <span>{{ formatConditionName(condition) }}</span>
            </div>
            <div class="filter-item" 
                 @click="clearConditionFilter"
                 :class="{ active: !selectedCondition }">
              <span>All Conditions</span>
            </div>
          </div>

          <!-- Price Range -->
          <div class="filter-group">
            <h4 class="filter-subtitle">Price Range</h4>
            <div class="price-inputs">
              <input 
                v-model.number="minPrice"
                type="number"
                placeholder="Min"
                class="price-input"
                @input="applyPriceFilter"
              >
              <span>to</span>
              <input 
                v-model.number="maxPrice"
                type="number"
                placeholder="Max"
                class="price-input"
                @input="applyPriceFilter"
              >
            </div>
          </div>

          <!-- Sort Options -->
          <div class="filter-group">
            <h4 class="filter-subtitle">Sort By</h4>
            <select v-model="sortBy" @change="applySorting" class="sort-select">
              <option value="newest">Newest First</option>
              <option value="oldest">Oldest First</option>
              <option value="price_low">Price: Low to High</option>
              <option value="price_high">Price: High to Low</option>
            </select>
          </div>
        </div>
      </aside>

      <!-- Main Content Area -->
      <div class="main-marketplace">
        <!-- Loading State -->
        <div v-if="loading" class="loading-state">
          <div class="spinner"></div>
          <p>Loading marketplace items...</p>
        </div>

        <!-- Empty State -->
        <div v-else-if="!loading && items.length === 0" class="empty-state">
          <div class="empty-icon">📦</div>
          <h3>No items found</h3>
          <p v-if="hasActiveFilters">Try adjusting your filters to see more items.</p>
          <p v-else>No items are currently available in the marketplace.</p>
        </div>

        <!-- Items Grid -->
        <div v-else class="items-grid">
          <VintageItemCard 
            v-for="item in items" 
            :key="item.id"
            :item="formatItemForCard(item)"
            @contact-seller="handleContactSeller"
            @save-item="handleSaveItem"
          ></VintageItemCard>
        </div>

        <!-- Load More if needed -->
        <div v-if="hasMoreItems && !loading" class="load-more">
          <button @click="loadMoreItems" class="load-more-btn" :disabled="loadingMore">
            <span v-if="loadingMore">Loading...</span>
            <span v-else>Load More Items</span>
          </button>
        </div>

        <!-- Pagination Info -->
        <div v-if="pagination.total > 0" class="pagination-info">
          Showing {{ items.length }} of {{ pagination.total }} items
        </div>
      </div>
    </div>
  </UserLayout>
</template>

<script>
import UserLayout from '@/components/user/UserLayout.vue'
import VintageItemCard from '@/components/user/VintageItemCard.vue'

export default {
  name: 'UserMarketplace',
  components: {
    UserLayout,
    VintageItemCard
  },
  data() {
    return {
      // API Data
      items: [],
      availableCategories: [],
      availableConditions: ['new', 'like_new', 'good', 'fair', 'poor'],
      
      // Filter States
      searchQuery: '',
      selectedCategory: '',
      selectedCondition: '', // Ensure this is empty string, not 'new'
      minPrice: null,
      maxPrice: null,
      sortBy: 'newest',
      
      // Loading States
      loading: true,
      loadingMore: false,
      
      // Pagination
      currentPage: 1,
      pagination: {
        page: 1,
        pages: 1,
        per_page: 20,
        total: 0,
        has_next: false,
        has_prev: false
      },
      
      // Debounce timer
      searchTimeout: null
    }
  },
  
  computed: {
    hasMoreItems() {
      return this.pagination.has_next;
    },
    
    hasActiveFilters() {
      return this.searchQuery || this.selectedCategory || this.selectedCondition || 
             this.minPrice !== null || this.maxPrice !== null;
    }
  },

  watch: {
    selectedCondition(newVal, oldVal) {
      console.log('selectedCondition changed from', oldVal, 'to', newVal);
    }
  },
  
  mounted() {
    console.log('Component mounted, initial state:');
    console.log('  selectedCondition:', this.selectedCondition);
    console.log('  selectedCategory:', this.selectedCategory);
    this.testJWT();
    this.fetchMarketplaceItems();
  },
  
  methods: {
    async testJWT() {
      try {
        const token = localStorage.getItem('access_token') || localStorage.getItem('token');
        if (!token) {
          console.error('No token for JWT test');
          this.$router.push('/login');
          return;
        }
        
        console.log('Testing JWT token...');
        const response = await fetch('http://localhost:5000/api/user/test-jwt', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });
        
        if (response.ok) {
          const data = await response.json();
          console.log('JWT Test Success:', data);
        } else {
          const errorData = await response.json().catch(() => ({}));
          console.error('JWT Test Failed:', response.status, errorData);
          
          // If JWT test fails, likely need to re-login
          if (response.status === 401 || response.status === 422) {
            console.log('JWT token invalid, redirecting to login...');
            localStorage.removeItem('access_token');
            localStorage.removeItem('token');
            this.$router.push('/login');
            return;
          }
        }
      } catch (error) {
        console.error('JWT Test Error:', error);
        this.$router.push('/login');
      }
    },

    async fetchMarketplaceItems(isLoadMore = false) {
      try {
        if (!isLoadMore) {
          this.loading = true;
          this.currentPage = 1;
        } else {
          this.loadingMore = true;
          this.currentPage += 1;
        }
        
        const token = localStorage.getItem('access_token') || localStorage.getItem('token');
        if (!token) {
          console.error('No authentication token found');
          this.$router.push('/login');
          return;
        }
        console.log('Using token:', token ? 'Token present' : 'No token');
        
        // Build query parameters
        const params = new URLSearchParams({
          page: this.currentPage.toString(),
          per_page: '20',
          sort_by: this.sortBy
        });
        
        if (this.searchQuery) params.append('search', this.searchQuery);
        if (this.selectedCategory) params.append('category', this.selectedCategory);
        // Temporarily disable condition filter to debug
        // if (this.selectedCondition && this.selectedCondition.trim() !== '') {
        //   params.append('condition', this.selectedCondition);
        // }
        if (this.minPrice !== null) params.append('min_price', this.minPrice.toString());
        if (this.maxPrice !== null) params.append('max_price', this.maxPrice.toString());
        
        console.log('Current filter values:');
        console.log('  selectedCondition:', this.selectedCondition);
        console.log('  selectedCategory:', this.selectedCategory);
        console.log('  searchQuery:', this.searchQuery);
        console.log('Fetching marketplace items with params:', params.toString());
        
        const response = await fetch(`http://localhost:5000/api/user/marketplace?${params}`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });
        
        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}));
          console.error('API Error Response:', errorData);
          console.error('Request URL:', `http://localhost:5000/api/user/marketplace?${params}`);
          throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Marketplace data received:', data);
        
        if (isLoadMore) {
          this.items = [...this.items, ...data.items];
        } else {
          this.items = data.items || [];
        }
        
        this.pagination = data.pagination || {};
        this.availableCategories = data.filters?.categories || [];
        
      } catch (error) {
        console.error('Error fetching marketplace items:', error);
      } finally {
        this.loading = false;
        this.loadingMore = false;
      }
    },
    
    // Filter Methods
    toggleCategory(category) {
      this.selectedCategory = this.selectedCategory === category ? '' : category;
      this.fetchMarketplaceItems();
    },
    
    clearCategoryFilter() {
      this.selectedCategory = '';
      this.fetchMarketplaceItems();
    },
    
    toggleCondition(condition) {
      this.selectedCondition = this.selectedCondition === condition ? '' : condition;
      this.fetchMarketplaceItems();
    },
    
    clearConditionFilter() {
      this.selectedCondition = '';
      this.fetchMarketplaceItems();
    },
    
    applyPriceFilter() {
      // Debounce the price filter
      clearTimeout(this.searchTimeout);
      this.searchTimeout = setTimeout(() => {
        this.fetchMarketplaceItems();
      }, 500);
    },
    
    applySorting() {
      this.fetchMarketplaceItems();
    },
    
    debouncedSearch() {
      // Debounce the search input
      clearTimeout(this.searchTimeout);
      this.searchTimeout = setTimeout(() => {
        this.fetchMarketplaceItems();
      }, 500);
    },
    
    loadMoreItems() {
      if (this.hasMoreItems && !this.loadingMore) {
        this.fetchMarketplaceItems(true);
      }
    },
    
    // Utility Methods
    formatItemForCard(item) {
      return {
        id: item.id,
        title: item.title,
        price: item.price,
        image: this.getItemImage(item),
        seller: item.seller_id, // Could be enhanced to get seller name
        category: item.category,
        condition: item.condition_status || item.condition,
        year: item.year,
        description: item.description
      };
    },
    
    getItemImage(item) {
      if (item.images && Array.isArray(item.images) && item.images.length > 0) {
        return item.images[0];
      }
      return '/api/placeholder/300/300'; // Fallback image
    },
    
    formatCategoryName(category) {
      return category.charAt(0).toUpperCase() + category.slice(1).replace(/[_-]/g, ' ');
    },
    
    formatConditionName(condition) {
      return condition.charAt(0).toUpperCase() + condition.slice(1).replace('_', ' ');
    },
    
    // Event Handlers
    handleContactSeller(item) {
      console.log('Contact seller for item:', item);
      // TODO: Implement contact seller functionality
    },
    
    handleSaveItem(item) {
      console.log('Save item:', item);
      // TODO: Implement save to wishlist functionality
    }
  }
}
</script>

<style scoped>
/* Main Container */
.marketplace-container {
  display: flex;
  gap: 24px;
  max-width: 1400px;
  margin: 0 auto;
}

/* Filter Sidebar */
.filter-sidebar {
  width: 280px;
  flex-shrink: 0;
}

.filter-section {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 1px solid #e5e7eb;
}

.filter-title {
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 24px;
  color: #111827;
  border-bottom: 2px solid #e5e7eb;
  padding-bottom: 12px;
}

.filter-group {
  margin-bottom: 28px;
}

.filter-subtitle {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 16px;
  color: #374151;
}

/* Search Box */
.search-box {
  position: relative;
  margin-bottom: 20px;
}

.search-input {
  width: 100%;
  padding: 12px 40px 12px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  background: #fafafa;
  transition: all 0.2s ease;
}

.search-input:focus {
  outline: none;
  border-color: #2563eb;
  background: white;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.search-icon {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #6b7280;
  font-size: 16px;
}

/* Filter Items */
.filter-item {
  padding: 12px 16px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  color: #6b7280;
  margin-bottom: 6px;
  transition: all 0.2s ease;
  border: 1px solid transparent;
}

.filter-item:hover {
  background: #f8fafc;
  color: #374151;
  border-color: #e5e7eb;
}

.filter-item.active {
  background: #eff6ff;
  color: #2563eb;
  font-weight: 600;
  border-color: #bfdbfe;
}

/* Price Inputs */
.price-inputs {
  display: flex;
  align-items: center;
  gap: 8px;
}

.price-input {
  flex: 1;
  padding: 10px 12px;
  border: 2px solid #e5e7eb;
  border-radius: 6px;
  font-size: 14px;
  text-align: center;
}

.price-input:focus {
  outline: none;
  border-color: #2563eb;
}

/* Sort Select */
.sort-select {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  background: white;
  cursor: pointer;
}

.sort-select:focus {
  outline: none;
  border-color: #2563eb;
}

/* Main Marketplace */
.main-marketplace {
  flex: 1;
  min-height: 600px;
}

/* Loading State */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  color: #6b7280;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e5e7eb;
  border-left-color: #2563eb;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  text-align: center;
  color: #6b7280;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.empty-state h3 {
  font-size: 24px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 8px;
}

.empty-state p {
  font-size: 16px;
  max-width: 400px;
  line-height: 1.5;
}

/* Items Grid */
.items-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
  margin-bottom: 40px;
}

/* Load More */
.load-more {
  text-align: center;
  margin: 40px 0;
}

.load-more-btn {
  background: #2563eb;
  color: white;
  border: none;
  padding: 14px 28px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 140px;
}

.load-more-btn:hover:not(:disabled) {
  background: #1d4ed8;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
}

.load-more-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Pagination Info */
.pagination-info {
  text-align: center;
  padding: 20px 0;
  color: #6b7280;
  font-size: 14px;
  border-top: 1px solid #e5e7eb;
  margin-top: 20px;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .marketplace-container {
    gap: 20px;
  }
  
  .filter-sidebar {
    width: 240px;
  }
  
  .items-grid {
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 20px;
  }
}

@media (max-width: 768px) {
  .marketplace-container {
    flex-direction: column;
    gap: 16px;
  }
  
  .filter-sidebar {
    width: 100%;
    order: 2;
  }
  
  .main-marketplace {
    order: 1;
  }
  
  .items-grid {
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 16px;
  }
  
  .filter-section {
    padding: 20px;
  }
  
  .price-inputs {
    flex-direction: column;
    gap: 12px;
  }
}

@media (max-width: 480px) {
  .items-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .marketplace-container {
    margin: 0 16px;
  }
}
</style>
