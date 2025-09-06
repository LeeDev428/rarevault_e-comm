<template>
  <UserLayout>
    <div class="marketplace-container">
      <!-- Left Sidebar Filters -->
      <aside class="filter-sidebar">
        <div class="filter-section">
          <h3 class="filter-title">Filter</h3>
          
          <!-- Category Filters -->
          <div class="filter-group">
            <div class="filter-item" 
                 v-for="category in categories" 
                 :key="category.id"
                 @click="toggleCategory(category.id)"
                 :class="{ active: selectedCategories.includes(category.id) }">
              <span>{{ category.name }}</span>
            </div>
          </div>

          <!-- Date Posted Filter -->
          <div class="filter-group">
            <h4 class="filter-subtitle">Date posted</h4>
            <div class="date-filter">
              <div class="date-options">
                <label class="radio-option">
                  <input type="radio" v-model="dateFilter" value="today" name="date">
                  <span class="radio-custom"></span>
                  Today
                </label>
                <label class="radio-option">
                  <input type="radio" v-model="dateFilter" value="week" name="date">
                  <span class="radio-custom"></span>
                  In this week
                </label>
                <label class="radio-option">
                  <input type="radio" v-model="dateFilter" value="month" name="date">
                  <span class="radio-custom"></span>
                  In this month
                </label>
                <label class="radio-option">
                  <input type="radio" v-model="dateFilter" value="year" name="date">
                  <span class="radio-custom"></span>
                  In this year
                </label>
              </div>
            </div>
          </div>
        </div>
      </aside>

      <!-- Main Content Area -->
      <div class="main-marketplace">
        <!-- Items Grid -->
        <div class="items-grid">
          <VintageItemCard 
            v-for="item in filteredItems" 
            :key="item.id"
            :item="item"
            @contact-seller="handleContactSeller"
            @save-item="handleSaveItem"
          />
        </div>

        <!-- Load More if needed -->
        <div v-if="hasMoreItems" class="load-more">
          <button @click="loadMoreItems" class="load-more-btn">
            Load More Items
          </button>
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
      selectedCategories: [], // Empty by default - no filters selected
      dateFilter: 'month',
      hasMoreItems: true,
      categories: [
        { id: 'vintage-fashion', name: 'Vintage Fashion' },
        { id: 'vintage-collectibles', name: 'Vintage Collectibles' },
        { id: 'vintage-home-decor', name: 'Vintage Home Decor' },
        { id: 'vintage-electronics', name: 'Vintage Electronics' },
        { id: 'vintage-toys-games', name: 'Vintage Toys & Games' },
        { id: 'vintage-books-accessories', name: 'Vintage Books & Accessories' }
      ],
      items: [
        {
          id: 1,
          title: 'Vintage Pocket Watch',
          price: 150.00,
          image: '/api/placeholder/300/300',
          seller: 'Vintage Items',
          category: 'vintage-collectibles'
        },
        {
          id: 2,
          title: 'Vintage Cola Sign',
          price: 85.00,
          image: '/api/placeholder/300/300',
          seller: 'Vintage Items',
          category: 'vintage-collectibles'
        },
        {
          id: 3,
          title: 'Vintage Spoons Set',
          price: 45.00,
          image: '/api/placeholder/300/300',
          seller: 'Vintage Items',
          category: 'vintage-home-decor'
        },
        {
          id: 4,
          title: 'Vintage Wrist Watch',
          price: 120.00,
          image: '/api/placeholder/300/300',
          seller: 'Vintage Items',
          category: 'vintage-fashion'
        },
        {
          id: 5,
          title: 'Vintage Camera',
          price: 200.00,
          image: '/api/placeholder/300/300',
          seller: 'Vintage Items',
          category: 'vintage-electronics'
        },
        {
          id: 6,
          title: 'Vintage Typewriter',
          price: 180.00,
          image: '/api/placeholder/300/300',
          seller: 'Vintage Items',
          category: 'vintage-electronics'
        }
      ]
    }
  },
  computed: {
    filteredItems() {
      return this.items.filter(item => {
        const categoryMatch = this.selectedCategories.includes(item.category)
        // Add date filtering logic here based on dateFilter
        return categoryMatch
      })
    }
  },
  methods: {
    toggleCategory(categoryId) {
      const index = this.selectedCategories.indexOf(categoryId)
      if (index > -1) {
        this.selectedCategories.splice(index, 1)
      } else {
        this.selectedCategories.push(categoryId)
      }
    },
    
    handleContactSeller(item) {
      // Handle contact seller logic
      console.log('Contact seller for:', item.title)
    },
    
    handleSaveItem(item) {
      // Handle save item to wishlist logic
      console.log('Save item:', item.title)
    },
    
    loadMoreItems() {
      // Load more items logic
      console.log('Loading more items...')
    }
  }
}
</script>

<style scoped>
.marketplace-container {
  display: flex;
  gap: 24px;
  max-width: 1400px;
  margin: 0 auto;
}

/* Filter Sidebar */
.filter-sidebar {
  width: 250px;
  flex-shrink: 0;
}

.filter-section {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.filter-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 20px;
  color: #111827;
}

.filter-group {
  margin-bottom: 24px;
}

.filter-subtitle {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 12px;
  color: #374151;
}

.filter-item {
  padding: 8px 12px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  color: #6b7280;
  margin-bottom: 4px;
  transition: all 0.2s ease;
}

.filter-item:hover {
  background: #f3f4f6;
  color: #374151;
}

.filter-item.active {
  background: #eff6ff;
  color: #2563eb;
  font-weight: 500;
}

/* Date Filter */
.date-options {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.radio-option {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  font-size: 14px;
  color: #374151;
}

.radio-option input[type="radio"] {
  display: none;
}

.radio-custom {
  width: 16px;
  height: 16px;
  border: 2px solid #d1d5db;
  border-radius: 50%;
  position: relative;
  transition: all 0.2s ease;
}

.radio-option input[type="radio"]:checked + .radio-custom {
  border-color: #2563eb;
}

.radio-option input[type="radio"]:checked + .radio-custom::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 8px;
  height: 8px;
  background: #2563eb;
  border-radius: 50%;
}

/* Main Marketplace */
.main-marketplace {
  flex: 1;
}

.items-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

/* Load More */
.load-more {
  text-align: center;
  margin-top: 40px;
}

.load-more-btn {
  background: #2563eb;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s ease;
}

.load-more-btn:hover {
  background: #1d4ed8;
}

/* Responsive */
@media (max-width: 768px) {
  .marketplace-container {
    flex-direction: column;
  }
  
  .filter-sidebar {
    width: 100%;
  }
  
  .items-grid {
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 16px;
  }
}
</style>
