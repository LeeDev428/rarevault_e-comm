<template>
  <UserLayout>
    <div class="marketplace-container">
      <!-- Header -->
      <div class="marketplace-header">
        <h1 class="page-title">Coins & Currency Marketplace</h1>
        <p>Discover rare coins and collectible currency from verified sellers</p>
      </div>

      <!-- Search and Filters -->
      <div class="search-filters">
        <div class="search-bar">
          <input 
            type="text" 
            v-model="searchQuery" 
            @input="debouncedSearch"
            placeholder="Search coins and currency..." 
            class="search-input"
          />
        </div>
        
        <div class="filter-controls">
          <select v-model="sortBy" @change="fetchMarketplaceItems" class="sort-select">
            <option value="newest">Newest First</option>
            <option value="oldest">Oldest First</option>
            <option value="price_low">Price: Low to High</option>
            <option value="price_high">Price: High to Low</option>
          </select>
        </div>
      </div>

      <!-- Active Filters -->
      <div v-if="hasActiveFilters" class="active-filters">
        <span class="filter-label">Active Filters:</span>
        <span v-if="searchQuery" class="filter-tag">
          Search: "{{ searchQuery }}"
          <button @click="clearSearch" class="filter-remove">×</button>
        </span>
        <span v-if="selectedCondition" class="filter-tag">
          Condition: {{ formatConditionName(selectedCondition) }}
          <button @click="clearConditionFilter" class="filter-remove">×</button>
        </span>
        <span v-if="minPrice !== null || maxPrice !== null" class="filter-tag">
          Price: ₱{{ minPrice || 0 }} - ₱{{ maxPrice || '∞' }}
          <button @click="clearPriceFilter" class="filter-remove">×</button>
        </span>
        <button @click="clearAllFilters" class="clear-all-btn">Clear All</button>
      </div>

      <div class="marketplace-content">
        <!-- Filter Sidebar -->
        <aside class="filter-sidebar">
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

          <!-- Price Filter -->
          <div class="filter-group">
            <h4 class="filter-subtitle">Price Range</h4>
            <div class="price-inputs">
              <input 
                type="number" 
                v-model.number="minPrice" 
                @input="applyPriceFilter"
                placeholder="Min"
                class="price-input"
              />
              <span class="price-separator">to</span>
              <input 
                type="number" 
                v-model.number="maxPrice" 
                @input="applyPriceFilter"
                placeholder="Max"
                class="price-input"
              />
            </div>
          </div>
        </aside>

        <!-- Items Grid -->
        <main class="items-grid">
          <!-- Loading State -->
          <div v-if="loading" class="loading-container">
            <div class="loading-spinner"></div>
            <p>Loading coins...</p>
          </div>

          <!-- Empty State -->
          <div v-else-if="!loading && items.length === 0" class="empty-state">
            <h3>No coins found</h3>
            <p>Try adjusting your search or filters to find more items.</p>
          </div>

          <!-- Items -->
          <div v-else class="items-container">
            <VintageItemCard
              v-for="item in items"
              :key="item.id"
              :item="item"
              @contact-seller="handleContactSeller"
              @save-item="handleSaveItem"
            />
          </div>

          <!-- Load More -->
          <div v-if="hasMoreItems && !loading" class="load-more-container">
            <button 
              @click="loadMore" 
              :disabled="loadingMore"
              class="load-more-btn"
            >
              {{ loadingMore ? 'Loading...' : 'Load More Items' }}
            </button>
          </div>
        </main>
      </div>
    </div>
  </UserLayout>
</template>

<script>
import UserLayout from '@/components/user/UserLayout.vue'
import VintageItemCard from '@/components/user/VintageItemCard.vue'

export default {
  name: 'Coins',
  components: {
    UserLayout,
    VintageItemCard
  },
  data() {
    return {
      // API Data
      items: [],
      availableConditions: ['new', 'like_new', 'good', 'fair', 'poor'],
      
      // Filter States
      searchQuery: '',
      selectedCondition: '',
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
      return this.searchQuery || this.selectedCondition || 
             this.minPrice !== null || this.maxPrice !== null;
    }
  },

  mounted() {
    this.fetchMarketplaceItems();
  },
  
  methods: {
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
        
        const params = new URLSearchParams({
          page: isLoadMore ? this.currentPage : 1,
          per_page: 20,
          sort_by: this.sortBy,
          category: 'coins' // Filter specifically for coins
        });
        
        if (this.searchQuery) params.append('search', this.searchQuery);
        if (this.selectedCondition && this.selectedCondition.trim() !== '') {
          params.append('condition', this.selectedCondition);
        }
        if (this.minPrice !== null) params.append('min_price', this.minPrice.toString());
        if (this.maxPrice !== null) params.append('max_price', this.maxPrice.toString());
        
        const response = await fetch(`http://localhost:5000/api/user/marketplace?${params}`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });
        
        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}));
          if (response.status === 401 || response.status === 422) {
            localStorage.removeItem('access_token');
            localStorage.removeItem('token');
            this.$router.push('/login');
            return;
          }
          throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (isLoadMore) {
          this.items = [...this.items, ...data.items];
        } else {
          this.items = data.items || [];
        }
        
        this.pagination = data.pagination || {};
        
      } catch (error) {
        console.error('Error fetching coins:', error);
      } finally {
        this.loading = false;
        this.loadingMore = false;
      }
    },
    
    // Search Methods
    debouncedSearch() {
      clearTimeout(this.searchTimeout);
      this.searchTimeout = setTimeout(() => {
        this.fetchMarketplaceItems();
      }, 500);
    },
    
    clearSearch() {
      this.searchQuery = '';
      this.fetchMarketplaceItems();
    },
    
    // Filter Methods
    toggleCondition(condition) {
      this.selectedCondition = this.selectedCondition === condition ? '' : condition;
      this.fetchMarketplaceItems();
    },
    
    clearConditionFilter() {
      this.selectedCondition = '';
      this.fetchMarketplaceItems();
    },
    
    applyPriceFilter() {
      clearTimeout(this.searchTimeout);
      this.searchTimeout = setTimeout(() => {
        this.fetchMarketplaceItems();
      }, 500);
    },
    
    clearPriceFilter() {
      this.minPrice = null;
      this.maxPrice = null;
      this.fetchMarketplaceItems();
    },
    
    clearAllFilters() {
      this.searchQuery = '';
      this.selectedCondition = '';
      this.minPrice = null;
      this.maxPrice = null;
      this.fetchMarketplaceItems();
    },
    
    // Load More
    loadMore() {
      if (this.hasMoreItems && !this.loadingMore) {
        this.fetchMarketplaceItems(true);
      }
    },
    
    // Utility Methods
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
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400;1,500;1,600;1,700;1,800&family=Inter:wght@300;400;500;600;700&display=swap');

.page-title {
  font-family: 'Playfair Display', serif;
  font-style: italic;
  font-weight: 700;
  font-size: 2.5rem;
  letter-spacing: -1px;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.filter-label {
  font-family: 'Playfair Display', serif;
  font-style: italic;
  font-weight: 500;
  color: #374151;
}

.marketplace-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.marketplace-header {
  text-align: center;
  margin-bottom: 2rem;
}

.marketplace-header h1 {
  font-size: 2.5rem;
  font-weight: bold;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.marketplace-header p {
  color: #6b7280;
  font-size: 1.1rem;
}

.search-filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  align-items: center;
}

.search-bar {
  flex: 1;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 1rem;
}

.search-input:focus {
  outline: none;
  border-color: #8b5cf6;
}

.sort-select {
  padding: 0.75rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  background: white;
  font-size: 1rem;
  min-width: 200px;
}

.active-filters {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  align-items: center;
}

.filter-label {
  font-weight: 600;
  color: #374151;
}

.filter-tag {
  background: #f3f4f6;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.filter-remove {
  background: none;
  border: none;
  color: #6b7280;
  cursor: pointer;
  font-size: 1.2rem;
  padding: 0;
  margin-left: 0.25rem;
}

.clear-all-btn {
  background: #ef4444;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.875rem;
}

.marketplace-content {
  display: grid;
  grid-template-columns: 250px 1fr;
  gap: 2rem;
}

.filter-sidebar {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  height: fit-content;
}

.filter-group {
  margin-bottom: 2rem;
}

.filter-subtitle {
  font-size: 1.1rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 1rem;
}

.filter-item {
  padding: 0.75rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  margin-bottom: 0.5rem;
  transition: all 0.2s;
  background: #f9fafb;
}

.filter-item:hover {
  background: #f3f4f6;
}

.filter-item.active {
  background: #8b5cf6;
  color: white;
}

.price-inputs {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.price-input {
  flex: 1;
  padding: 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 0.875rem;
}

.price-separator {
  color: #6b7280;
  font-size: 0.875rem;
}

.items-grid {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  text-align: center;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f4f6;
  border-top: 4px solid #8b5cf6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: #6b7280;
}

.empty-state h3 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  color: #374151;
}

.items-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}

.load-more-container {
  text-align: center;
  margin-top: 2rem;
}

.load-more-btn {
  background: #8b5cf6;
  color: white;
  border: none;
  padding: 0.75rem 2rem;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.2s;
}

.load-more-btn:hover:not(:disabled) {
  background: #7c3aed;
}

.load-more-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .marketplace-content {
    grid-template-columns: 1fr;
  }
  
  .search-filters {
    flex-direction: column;
  }
  
  .items-container {
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  }
}
</style>
