<template>
  <UserLayout>
    <div class="marketplace-container">
      <!-- Filter Sidebar -->
      <aside class="filter-sidebar">
        <div class="filter-section">
          <h3>Categories</h3>
          <div class="filter-group">
            <label class="filter-item">
              <input type="checkbox" v-model="filters.categories" value="ancient">
              <span>Ancient Coins</span>
            </label>
            <label class="filter-item">
              <input type="checkbox" v-model="filters.categories" value="paper">
              <span>Paper Money</span>
            </label>
            <label class="filter-item">
              <input type="checkbox" v-model="filters.categories" value="commemorative">
              <span>Commemorative</span>
            </label>
            <label class="filter-item">
              <input type="checkbox" v-model="filters.categories" value="foreign">
              <span>Foreign Currency</span>
            </label>
          </div>
        </div>

        <div class="filter-section">
          <h3>Condition</h3>
          <div class="filter-group">
            <label class="filter-item">
              <input type="checkbox" v-model="filters.condition" value="ms70">
              <span>MS-70 (Perfect)</span>
            </label>
            <label class="filter-item">
              <input type="checkbox" v-model="filters.condition" value="ms65">
              <span>MS-65 (Gem)</span>
            </label>
            <label class="filter-item">
              <input type="checkbox" v-model="filters.condition" value="ms60">
              <span>MS-60 (Uncirculated)</span>
            </label>
            <label class="filter-item">
              <input type="checkbox" v-model="filters.condition" value="au">
              <span>AU (About Uncirculated)</span>
            </label>
          </div>
        </div>

        <div class="filter-section">
          <h3>Price Range</h3>
          <div class="price-range">
            <input type="number" v-model="filters.priceMin" placeholder="Min" class="price-input">
            <input type="number" v-model="filters.priceMax" placeholder="Max" class="price-input">
          </div>
        </div>

        <div class="filter-section">
          <h3>Era</h3>
          <div class="filter-group">
            <label class="filter-item">
              <input type="checkbox" v-model="filters.era" value="modern">
              <span>Modern (1965+)</span>
            </label>
            <label class="filter-item">
              <input type="checkbox" v-model="filters.era" value="classic">
              <span>Classic (1793-1964)</span>
            </label>
            <label class="filter-item">
              <input type="checkbox" v-model="filters.era" value="colonial">
              <span>Colonial (Pre-1793)</span>
            </label>
          </div>
        </div>
      </aside>

      <!-- Main Content -->
      <main class="marketplace-main">
        <div class="marketplace-header">
          <h1>Coins & Currency</h1>
          <div class="header-actions">
            <select v-model="sortBy" class="sort-select">
              <option value="newest">Newest First</option>
              <option value="price-low">Price: Low to High</option>
              <option value="price-high">Price: High to Low</option>
              <option value="popular">Most Popular</option>
            </select>
          </div>
        </div>

        <!-- Items Grid -->
        <div class="items-grid">
          <VintageItemCard
            v-for="item in filteredItems"
            :key="item.id"
            :item="item"
            @contact-seller="handleContactSeller"
            @save-to-wishlist="handleSaveToWishlist"
          />
        </div>

        <!-- Load More -->
        <div class="load-more-section" v-if="hasMoreItems">
          <button @click="loadMoreItems" class="load-more-btn">
            Load More Items
          </button>
        </div>
      </main>
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
      sortBy: 'newest',
      hasMoreItems: true,
      filters: {
        categories: [],
        condition: [],
        era: [],
        priceMin: null,
        priceMax: null
      },
      items: [
        {
          id: 1,
          title: "1921 Morgan Silver Dollar",
          price: 299.99,
          image: "https://images.unsplash.com/photo-1541753866388-0b3c701627d3?w=300&h=300&fit=crop",
          seller: "CoinCollector1",
          category: "ancient",
          condition: "ms65",
          era: "classic"
        },
        {
          id: 2,
          title: "Series 1928 $20 Gold Certificate",
          price: 1599.99,
          image: "https://images.unsplash.com/photo-1560472355-536de3962603?w=300&h=300&fit=crop",
          seller: "CurrencyExpert",
          category: "paper",
          condition: "au",
          era: "classic"
        },
        {
          id: 3,
          title: "1886 Indian Head Penny",
          price: 45.00,
          image: "https://images.unsplash.com/photo-1541753866388-0b3c701627d3?w=300&h=300&fit=crop",
          seller: "VintageCoinShop",
          category: "commemorative",
          condition: "ms60",
          era: "classic"
        }
      ]
    }
  },
  computed: {
    filteredItems() {
      let filtered = this.items

      if (this.filters.categories.length > 0) {
        filtered = filtered.filter(item => this.filters.categories.includes(item.category))
      }

      if (this.filters.condition.length > 0) {
        filtered = filtered.filter(item => this.filters.condition.includes(item.condition))
      }

      if (this.filters.era.length > 0) {
        filtered = filtered.filter(item => this.filters.era.includes(item.era))
      }

      if (this.filters.priceMin !== null && this.filters.priceMin !== '') {
        filtered = filtered.filter(item => item.price >= Number(this.filters.priceMin))
      }

      if (this.filters.priceMax !== null && this.filters.priceMax !== '') {
        filtered = filtered.filter(item => item.price <= Number(this.filters.priceMax))
      }

      return this.sortItems(filtered)
    }
  },
  methods: {
    sortItems(items) {
      const sorted = [...items]
      switch (this.sortBy) {
        case 'price-low':
          return sorted.sort((a, b) => a.price - b.price)
        case 'price-high':
          return sorted.sort((a, b) => b.price - a.price)
        case 'popular':
          return sorted.sort((a, b) => b.views - a.views)
        case 'newest':
        default:
          return sorted.sort((a, b) => b.id - a.id)
      }
    },
    handleContactSeller(item) {
      console.log('Contact seller for:', item.title)
    },
    handleSaveToWishlist(item) {
      console.log('Save to wishlist:', item.title)
    },
    loadMoreItems() {
      console.log('Loading more coins & currency...')
    }
  }
}
</script>

<style scoped>
.marketplace-container {
  display: flex;
  gap: 24px;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.filter-sidebar {
  width: 250px;
  flex-shrink: 0;
}

.filter-section {
  background: white;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 16px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.filter-section h3 {
  margin: 0 0 16px 0;
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.filter-item {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  font-size: 14px;
  color: #4b5563;
}

.filter-item input[type="checkbox"] {
  margin: 0;
}

.price-range {
  display: flex;
  gap: 8px;
}

.price-input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  font-size: 14px;
}

.marketplace-main {
  flex: 1;
}

.marketplace-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.marketplace-header h1 {
  margin: 0;
  font-size: 28px;
  font-weight: 700;
  color: #1f2937;
}

.sort-select {
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  background: white;
  font-size: 14px;
}

.items-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
  margin-bottom: 40px;
}

.load-more-section {
  text-align: center;
}

.load-more-btn {
  background: #3b82f6;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.load-more-btn:hover {
  background: #2563eb;
}
</style>
