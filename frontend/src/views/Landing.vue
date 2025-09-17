<template>
  <div class="landing-page">
    <!-- Header -->
    <header class="header">
      <div class="container">
        <div class="nav-wrapper">
          <div class="logo">
            <h1 class="logo-text font-display">RareVault.</h1>
          </div>
          <nav class="nav-links">
            <router-link to="/login" class="nav-link">Log In</router-link>
            <router-link to="/register" class="btn btn-primary">Sign Up</router-link>
          </nav>
        </div>
      </div>
    </header>

    <!-- Hero Section -->
    <section class="hero">
      <div class="container">
        <div class="hero-content">
          <div class="hero-text">
            <h1 class="hero-title font-display">
              Got vintage treasures, antiques, or rare collectibles collecting dust?
            </h1>
            <p class="hero-subtitle">
              Find fellow collectors and enthusiasts who value what you have.
            </p>
            <div class="hero-buttons">
              <router-link to="/register?role=admin" class="btn btn-primary btn-large">
                as admin
              </router-link>
              <router-link to="/register?role=user" class="btn btn-dark btn-large">
                seller / buyer
              </router-link>
            </div>
          </div>
          
          <!-- Vintage Item Visual -->
          <div class="hero-visual">
            <div class="vintage-item">
              <div class="vintage-card">
                <div class="card-content">
                  <div class="vintage-icon">
                    <svg width="60" height="60" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M12 2L15.09 8.26L22 9L17 14L18.18 21L12 17.77L5.82 21L7 14L2 9L8.91 8.26L12 2Z" fill="#8b5a3c"/>
                    </svg>
                  </div>
                  <h3 class="vintage-title">Rare Collectibles</h3>
                  <p class="vintage-desc">Discover unique vintage treasures</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features">
      <div class="container">
        <div class="features-grid">
          <div class="feature-card">
            <div class="feature-icon">
              <svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M16 7C16 9.20914 14.2091 11 12 11C9.79086 11 8 9.20914 8 7C8 4.79086 9.79086 3 12 3C14.2091 3 16 4.79086 16 7Z" stroke="#8b5a3c" stroke-width="2"/>
                <path d="M12 14C8.13401 14 5 17.134 5 21H19C19 17.134 15.866 14 12 14Z" stroke="#8b5a3c" stroke-width="2"/>
              </svg>
            </div>
            <h3>Trusted Collectors</h3>
            <p>Connect with verified collectors and antique enthusiasts</p>
          </div>
          
          <div class="feature-card">
            <div class="feature-icon">
              <svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M21 16V8C20.9996 7.64928 20.9071 7.30481 20.7315 7.00116C20.556 6.69751 20.3037 6.44536 20 6.27L13 2.27C12.696 2.09446 12.3511 2.00205 12 2.00205C11.6489 2.00205 11.304 2.09446 11 2.27L4 6.27C3.69626 6.44536 3.44398 6.69751 3.26846 7.00116C3.09294 7.30481 3.00036 7.64928 3 8V16C3.00036 16.3507 3.09294 16.6952 3.26846 16.9988C3.44398 17.3025 3.69626 17.5546 4 17.73L11 21.73C11.304 21.9055 11.6489 21.9979 12 21.9979C12.3511 21.9979 12.696 21.9055 13 21.73L20 17.73C20.3037 17.5546 20.556 17.3025 20.7315 16.9988C20.9071 16.6952 20.9996 16.3507 21 16Z" stroke="#8b5a3c" stroke-width="2"/>
                <path d="M7.5 4.21L12 6.81L16.5 4.21" stroke="#8b5a3c" stroke-width="2"/>
                <path d="M7.5 19.79V14.6L3 12" stroke="#8b5a3c" stroke-width="2"/>
                <path d="M21 12L16.5 14.6V19.79" stroke="#8b5a3c" stroke-width="2"/>
                <path d="M12 22.81V17.81" stroke="#8b5a3c" stroke-width="2"/>
                <path d="M12 6.81L21 12L12 17.81L3 12L12 6.81" stroke="#8b5a3c" stroke-width="2"/>
              </svg>
            </div>
            <h3>Secure Trading</h3>
            <p>Safe and secure platform for buying and selling antiques</p>
          </div>
          
          <div class="feature-card">
            <div class="feature-icon">
              <svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M9 11H15M9 15H15M17 21L20 18V7C20 5.89543 19.1046 5 18 5H6C4.89543 5 4 5.89543 4 7V18L7 21H17Z" stroke="#8b5a3c" stroke-width="2"/>
              </svg>
            </div>
            <h3>Expert Authentication</h3>
            <p>Get your items authenticated by certified experts</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Products Section -->
    <section class="products-section">
      <div class="container">
        <!-- Search and Filters -->
        <div class="search-filters">
          <!-- Search Bar -->
          <div class="search-bar">
            <div class="search-input-wrapper">
              <svg class="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M21 21L15 15M17 10C17 13.866 13.866 17 10 17C6.13401 17 3 13.866 3 10C3 6.13401 6.13401 3 10 3C13.866 3 17 6.13401 17 10Z" stroke="#9CA3AF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <input 
                type="text" 
                v-model="searchQuery"
                placeholder="Search for items..."
                class="search-input"
                @input="handleSearch"
              />
            </div>
          </div>

          <!-- Category Filters -->
          <div class="category-filters">
            <button 
              v-for="category in categories" 
              :key="category.value"
              @click="selectCategory(category.value)"
              :class="['category-btn', { active: selectedCategory === category.value }]"
            >
              <div class="category-icon">
                <component :is="category.icon" />
              </div>
              <span>{{ category.label }}</span>
            </button>
          </div>
        </div>

        <!-- Products Grid -->
        <div class="products-grid" v-if="paginatedItems.length > 0">
          <div 
            v-for="item in paginatedItems" 
            :key="item.id"
            class="product-card"
          >
            <div class="product-image">
              <img 
                :src="item.primary_image?.url || '/placeholder.svg'" 
                :alt="item.title"
                @error="handleImageError"
              />
              <div class="product-status" v-if="item.isAuthenticated">
                <span class="verified-badge">Verified</span>
              </div>
            </div>
            
            <div class="product-info">
              <h3 class="product-title">{{ item.title }}</h3>
              <p class="product-category">{{ item.category }}</p>
              <div class="product-details">
                <span class="product-price">₱ {{ formatPrice(item.price) }}</span>
                <span class="product-condition">{{ item.condition }}</span>
              </div>
              <div class="product-meta">
                <span class="product-year" v-if="item.year">{{ item.year }}</span>
                <div class="product-stats">
                  <!-- Rating Display -->
                  <div v-if="item.rating && item.rating > 0" class="rating-display">
                    <div class="stars">
                      <span v-for="star in 5" :key="star" 
                            :class="['star', { filled: star <= Math.round(item.rating) }]">
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor">
                          <path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z"/>
                        </svg>
                      </span>
                    </div>
                    <span class="rating-text">{{ item.rating.toFixed(1) }}</span>
                  </div>
                  
                  <!-- Sold Count -->
                  <div v-if="item.soldCount && item.soldCount > 0" class="sold-count">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                      <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/>
                      <line x1="3" y1="6" x2="21" y2="6"/>
                      <path d="M16 10a4 4 0 0 1-8 0"/>
                    </svg>
                    <span>{{ item.soldCount }} sold</span>
                  </div>
                  
                  <!-- Fallback if no rating or sold count -->
                  <div v-if="(!item.rating || item.rating === 0) && (!item.soldCount || item.soldCount === 0)" class="no-stats">
                    <span class="new-item">New listing</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Loading State -->
        <div class="loading-state" v-else-if="isLoading">
          <div class="loading-spinner"></div>
          <p>Loading items...</p>
        </div>

        <!-- Empty State -->
        <div class="empty-state" v-else>
          <div class="empty-icon">
            <svg width="64" height="64" viewBox="0 0 24 24" fill="none">
              <path d="M9.17 6L18.83 6C19.54 6 19.67 6.89 19.08 7.17L12.83 10.17C12.42 10.36 11.58 10.36 11.17 10.17L4.92 7.17C4.33 6.89 4.46 6 5.17 6L9.17 6Z" stroke="#9CA3AF" stroke-width="2"/>
              <path d="M12 11V19" stroke="#9CA3AF" stroke-width="2"/>
            </svg>
          </div>
          <h3>No items found</h3>
          <p>Try adjusting your search or category filters</p>
        </div>

        <!-- Pagination -->
        <Pagination
          v-if="filteredItems.length > itemsPerPage"
          :current-page="currentPage"
          :total-pages="totalPages"
          :total-items="filteredItems.length"
          :has-previous="currentPage > 1"
          :has-next="currentPage < totalPages"
          :items-per-page="itemsPerPage"
          item-label="items"
          @page-changed="handlePageChange"
        />
      </div>
    </section>
  </div>
</template>

<script>
import Pagination from '../components/pagination.vue'

export default {
  name: 'Landing',
  components: {
    Pagination
  },
  data() {
    return {
      items: [],
      searchQuery: '',
      selectedCategory: 'all',
      isLoading: false,
      currentPage: 1,
      itemsPerPage: 9,
      categories: [
        {
          value: 'all',
          label: 'All Items',
          icon: 'AllItemsIcon'
        },
        {
          value: 'Vintage Items',
          label: 'Vintage Items',
          icon: 'VintageIcon'
        },
        {
          value: 'Collectibles',
          label: 'Collectibles',
          icon: 'CollectiblesIcon'
        },
        {
          value: 'Antiques',
          label: 'Antiques',
          icon: 'AntiquesIcon'
        },
        {
          value: 'Coins & Currency',
          label: 'Coins & Currency',
          icon: 'CoinsIcon'
        },
        {
          value: 'Others',
          label: 'Others',
          icon: 'OthersIcon'
        }
      ]
    }
  },
  computed: {
    filteredItems() {
      let filtered = this.items;

      // Filter by category
      if (this.selectedCategory !== 'all') {
        filtered = filtered.filter(item => 
          item.category && item.category.toLowerCase().includes(this.selectedCategory.toLowerCase())
        );
      }

      // Filter by search query
      if (this.searchQuery.trim()) {
        const query = this.searchQuery.toLowerCase();
        filtered = filtered.filter(item =>
          (item.title && item.title.toLowerCase().includes(query)) ||
          (item.description && item.description.toLowerCase().includes(query)) ||
          (item.category && item.category.toLowerCase().includes(query)) ||
          (item.tags && item.tags.some(tag => tag.toLowerCase().includes(query)))
        );
      }

      return filtered;
    },
    paginatedItems() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.filteredItems.slice(start, end);
    },
    totalPages() {
      return Math.ceil(this.filteredItems.length / this.itemsPerPage);
    }
  },
  mounted() {
    this.fetchItems();
  },
  methods: {
    async fetchItems() {
      this.isLoading = true;
      try {
        console.log('Fetching items from API...');
        const response = await fetch('http://localhost:5000/api/items');
        console.log('API Response status:', response.status);
        
        if (response.ok) {
          const data = await response.json();
          console.log('API Response data:', data);
          this.items = data.items || [];
          console.log('Items loaded:', this.items.length);
        } else {
          console.error('Failed to fetch items:', response.statusText);
          // Try to read error response
          const errorData = await response.text();
          console.error('Error details:', errorData);
        }
      } catch (error) {
        console.error('Error fetching items:', error);
        // If the main API fails, let's try without the /api prefix
        try {
          console.log('Trying alternative endpoint...');
          const altResponse = await fetch('http://localhost:5000/items');
          if (altResponse.ok) {
            const altData = await altResponse.json();
            console.log('Alternative API Response data:', altData);
            this.items = altData.items || [];
          }
        } catch (altError) {
          console.error('Alternative endpoint also failed:', altError);
        }
      } finally {
        this.isLoading = false;
      }
    },
    handleSearch() {
      // Reset to first page when searching
      this.currentPage = 1;
    },
    selectCategory(category) {
      this.selectedCategory = category;
      // Reset to first page when changing category
      this.currentPage = 1;
    },
    handlePageChange(page) {
      this.currentPage = page;
      // Scroll to top of products section
      const productsSection = document.querySelector('.products-section');
      if (productsSection) {
        productsSection.scrollIntoView({ behavior: 'smooth' });
      }
    },
    formatPrice(price) {
      if (price == null) return '0.00';
      return parseFloat(price).toFixed(2);
    },
    handleImageError(event) {
      event.target.src = '/placeholder.svg';
    }
  },
  components: {
    // Icon components for categories
    AllItemsIcon: {
      template: `
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
          <path d="M3 3H21V21H3V3Z" stroke="currentColor" stroke-width="2" fill="none"/>
          <path d="M9 9H15V15H9V9Z" stroke="currentColor" stroke-width="2" fill="none"/>
        </svg>
      `
    },
    VintageIcon: {
      template: `
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
          <path d="M12 2L15.09 8.26L22 9L17 14L18.18 21L12 17.77L5.82 21L7 14L2 9L8.91 8.26L12 2Z" fill="currentColor"/>
        </svg>
      `
    },
    CollectiblesIcon: {
      template: `
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
          <path d="M21 16V8C20.9996 7.64928 20.9071 7.30481 20.7315 7.00116C20.556 6.69751 20.3037 6.44536 20 6.27L13 2.27C12.696 2.09446 12.3511 2.00205 12 2.00205C11.6489 2.00205 11.304 2.09446 11 2.27L4 6.27C3.69626 6.44536 3.44398 6.69751 3.26846 7.00116C3.09294 7.30481 3.00036 7.64928 3 8V16C3.00036 16.3507 3.09294 16.6952 3.26846 16.9988C3.44398 17.3025 3.69626 17.5546 4 17.73L11 21.73C11.304 21.9055 11.6489 21.9979 12 21.9979C12.3511 21.9979 12.696 21.9055 13 21.73L20 17.73C20.3037 17.5546 20.556 17.3025 20.7315 16.9988C20.9071 16.6952 20.9996 16.3507 21 16Z" stroke="currentColor" stroke-width="2"/>
        </svg>
      `
    },
    AntiquesIcon: {
      template: `
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
          <path d="M7 21C7 21 3 17 3 13C3 10.79 4.79 9 7 9S11 10.79 11 13C11 17 7 21 7 21Z" stroke="currentColor" stroke-width="2"/>
          <path d="M17 21C17 21 13 17 13 13C13 10.79 14.79 9 17 9S21 10.79 21 13C21 17 17 21 17 21Z" stroke="currentColor" stroke-width="2"/>
          <path d="M7 3V9" stroke="currentColor" stroke-width="2"/>
          <path d="M17 3V9" stroke="currentColor" stroke-width="2"/>
        </svg>
      `
    },
    CoinsIcon: {
      template: `
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
          <circle cx="8" cy="8" r="6" stroke="currentColor" stroke-width="2"/>
          <path d="M18.09 10.37A6 6 0 1 1 10.37 18.09" stroke="currentColor" stroke-width="2"/>
          <path d="M7 6H9V10H7" stroke="currentColor" stroke-width="2"/>
          <path d="M13 16H15V20H13" stroke="currentColor" stroke-width="2"/>
        </svg>
      `
    },
    OthersIcon: {
      template: `
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
          <path d="M12 3V21M3 12H21" stroke="currentColor" stroke-width="2"/>
          <circle cx="12" cy="12" r="2" fill="currentColor"/>
        </svg>
      `
    }
  }
}
</script>

<style scoped>
.landing-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
}

.header {
  background: white;
  box-shadow: var(--shadow-sm);
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 0;
}

.logo-text {
  font-size: 1.75rem;
  font-weight: 600;
  color: var(--text-primary);
  background: var(--gradient-vintage);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.nav-link {
  color: var(--text-secondary);
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s ease;
}

.nav-link:hover {
  color: var(--text-primary);
}

.hero {
  padding: 4rem 0 6rem;
}

.hero-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
  min-height: 60vh;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 600;
  line-height: 1.2;
  color: var(--text-primary);
  margin-bottom: 1.5rem;
}

.hero-subtitle {
  font-size: 1.25rem;
  color: var(--text-secondary);
  margin-bottom: 2.5rem;
  line-height: 1.6;
}

.hero-buttons {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.btn-large {
  padding: 1rem 2rem;
  font-size: 1rem;
  min-height: 3.5rem;
  font-weight: 600;
}

.hero-visual {
  display: flex;
  justify-content: center;
  align-items: center;
}

.vintage-item {
  position: relative;
  transform: perspective(1000px) rotateY(-15deg) rotateX(10deg);
  animation: float 6s ease-in-out infinite;
}

.vintage-card {
  background: white;
  border-radius: 1rem;
  padding: 2rem;
  box-shadow: 
    0 10px 25px rgba(0, 0, 0, 0.1),
    0 20px 40px rgba(0, 0, 0, 0.05),
    0 0 0 1px rgba(255, 255, 255, 0.5);
  border: 1px solid rgba(139, 90, 60, 0.1);
  min-width: 280px;
  text-align: center;
}

.card-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.vintage-icon {
  background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
  padding: 1.5rem;
  border-radius: 50%;
  border: 2px solid rgba(139, 90, 60, 0.1);
}

.vintage-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.vintage-desc {
  color: var(--text-secondary);
  margin: 0;
}

.features {
  padding: 4rem 0;
  background: white;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.feature-card {
  text-align: center;
  padding: 2rem;
  border-radius: 1rem;
  background: var(--background-light);
  border: 1px solid var(--border-light);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-lg);
}

.feature-icon {
  display: flex;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.feature-card h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 1rem;
}

.feature-card p {
  color: var(--text-secondary);
  line-height: 1.6;
}

/* Products Section */
.products-section {
  padding: 4rem 0;
  background: var(--background-light);
}

.search-filters {
  margin-bottom: 3rem;
}

.search-bar {
  margin-bottom: 2rem;
  display: flex;
  justify-content: center;
}

.search-input-wrapper {
  position: relative;
  max-width: 600px;
  width: 100%;
}

.search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  z-index: 2;
}

.search-input {
  width: 100%;
  padding: 1rem 1rem 1rem 3rem;
  border: 2px solid var(--border-light);
  border-radius: 2rem;
  background: white;
  font-size: 1rem;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.search-input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(139, 90, 60, 0.1);
}

.category-filters {
  display: flex;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
  overflow-x: auto;
  padding-bottom: 0.5rem;
}

.category-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border: 2px solid var(--border-light);
  border-radius: 2rem;
  background: white;
  color: var(--text-secondary);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
  min-height: 3rem;
}

.category-btn:hover {
  border-color: var(--primary-color);
  color: var(--primary-color);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(139, 90, 60, 0.15);
}

.category-btn.active {
  background: var(--primary-color);
  border-color: var(--primary-color);
  color: white;
  box-shadow: 0 4px 12px rgba(139, 90, 60, 0.25);
}

.category-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.product-card {
  background: white;
  border-radius: 1rem;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  border: 1px solid var(--border-light);
}

.product-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.15);
}

.product-image {
  position: relative;
  width: 100%;
  height: 200px;
  overflow: hidden;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.product-card:hover .product-image img {
  transform: scale(1.05);
}

.product-status {
  position: absolute;
  top: 1rem;
  right: 1rem;
}

.verified-badge {
  background: rgba(34, 197, 94, 0.9);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.75rem;
  font-weight: 600;
  backdrop-filter: blur(4px);
}

.product-info {
  padding: 1.5rem;
}

.product-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.product-category {
  color: var(--text-secondary);
  font-size: 0.875rem;
  margin-bottom: 1rem;
  text-transform: capitalize;
}

.product-details {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.product-price {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--primary-color);
}

.product-condition {
  background: var(--background-light);
  color: var(--text-secondary);
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.75rem;
  text-transform: capitalize;
}

.product-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: var(--text-secondary);
  font-size: 0.875rem;
}

.product-year {
  font-weight: 500;
}

.product-stats {
  display: flex;
  gap: 1rem;
  align-items: center;
  flex-wrap: wrap;
}

.rating-display {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.stars {
  display: flex;
  gap: 1px;
}

.star {
  color: #d1d5db;
  transition: color 0.2s ease;
}

.star.filled {
  color: #fbbf24;
}

.rating-text {
  font-size: 0.75rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.sold-count {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.75rem;
  color: var(--text-secondary);
}

.sold-count svg {
  color: #10b981;
}

.no-stats .new-item {
  font-size: 0.75rem;
  color: var(--primary-color);
  font-weight: 500;
  background: rgba(139, 90, 60, 0.1);
  padding: 0.125rem 0.5rem;
  border-radius: 0.5rem;
}

/* Loading and Empty States */
.loading-state, .empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: var(--text-secondary);
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--border-light);
  border-top: 3px solid var(--primary-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

.empty-state {
  max-width: 400px;
  margin: 0 auto;
}

.empty-icon {
  margin-bottom: 1rem;
  display: flex;
  justify-content: center;
}

.empty-state h3 {
  color: var(--text-primary);
  margin-bottom: 0.5rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes float {
  0%, 100% {
    transform: perspective(1000px) rotateY(-15deg) rotateX(10deg) translateY(0px);
  }
  50% {
    transform: perspective(1000px) rotateY(-15deg) rotateX(10deg) translateY(-10px);
  }
}

/* Responsive */
@media (max-width: 768px) {
  .nav-wrapper {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .nav-links {
    flex-direction: column;
    width: 100%;
  }
  
  .nav-link, .btn {
    width: 100%;
    text-align: center;
  }
  
  .hero-content {
    grid-template-columns: 1fr;
    gap: 2rem;
    text-align: center;
  }
  
  .hero-title {
    font-size: 2.5rem;
  }
  
  .hero-buttons {
    justify-content: center;
  }
  
  .btn-large {
    flex: 1;
    min-width: 200px;
  }
  
  .vintage-item {
    transform: none;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
  }

  /* Products section responsive */
  .search-input-wrapper {
    max-width: 100%;
  }
  
  .category-filters {
    justify-content: flex-start;
    padding: 0 1rem;
  }
  
  .category-btn {
    font-size: 0.875rem;
    padding: 0.5rem 1rem;
    min-height: 2.5rem;
  }
  
  .products-grid {
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 1.5rem;
  }
  
  .product-info {
    padding: 1rem;
  }
}

@media (max-width: 480px) {
  .hero-title {
    font-size: 2rem;
  }
  
  .hero-buttons {
    flex-direction: column;
  }
  
  .btn-large {
    width: 100%;
  }

  /* Mobile-specific product styles */
  .search-input {
    font-size: 1rem;
    padding: 0.875rem 0.875rem 0.875rem 2.5rem;
  }
  
  .category-filters {
    gap: 0.5rem;
  }
  
  .category-btn {
    font-size: 0.75rem;
    padding: 0.5rem 0.75rem;
    min-height: 2.25rem;
  }
  
  .category-btn span {
    display: none;
  }
  
  .category-icon {
    width: 18px;
    height: 18px;
  }
  
  .products-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .product-details {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .product-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
}
</style>
