<template>
  <div class="user-dashboard">
    <header class="dashboard-header">
      <div class="container">
        <div class="header-content">
          <div class="logo-section">
            <h1 class="logo-text font-display">RareVault.</h1>
            <span class="user-badge">Collector</span>
          </div>
          <div class="header-actions">
            <span class="welcome-text">Welcome, {{ user?.first_name }}</span>
            <button @click="logout" class="btn btn-secondary">Logout</button>
          </div>
        </div>
      </div>
    </header>

    <main class="dashboard-main">
      <div class="container">
        <div class="dashboard-content">
          <!-- Quick Actions -->
          <div class="quick-actions">
            <div class="action-card">
              <div class="action-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12 5V19M5 12H19" stroke="currentColor" stroke-width="2"/>
                </svg>
              </div>
              <h3>Add New Item</h3>
              <p>List a new vintage treasure or collectible</p>
              <button @click="showAddItemModal = true" class="btn btn-primary">Add Item</button>
            </div>

            <div class="action-card">
              <div class="action-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M15 3H6C4.89543 3 4 3.89543 4 5V19C4 20.1046 4.89543 21 6 21H18C19.1046 21 20 20.1046 20 19V8L15 3Z" stroke="currentColor" stroke-width="2"/>
                  <path d="M15 3V8H20" stroke="currentColor" stroke-width="2"/>
                </svg>
              </div>
              <h3>My Listings</h3>
              <p>Manage your current items and listings</p>
              <button @click="loadUserItems" class="btn btn-secondary">View All</button>
            </div>

            <div class="action-card">
              <div class="action-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M21 21L15 15L21 21ZM17 10C17 13.866 13.866 17 10 17C6.13401 17 3 13.866 3 10C3 6.13401 6.13401 3 10 3C13.866 3 17 6.13401 17 10Z" stroke="currentColor" stroke-width="2"/>
                </svg>
              </div>
              <h3>Browse Items</h3>
              <p>Discover unique collectibles from other sellers</p>
              <button @click="browseItems" class="btn btn-secondary">Browse</button>
            </div>
          </div>

          <!-- My Items Section -->
          <div class="section">
            <div class="section-header">
              <h2 class="section-title">My Items</h2>
              <div class="section-actions">
                <button @click="loadUserItems" class="btn btn-secondary" :disabled="loading">
                  <span v-if="loading" class="spinner"></span>
                  <span v-else>Refresh</span>
                </button>
                <button @click="showAddItemModal = true" class="btn btn-primary">Add New Item</button>
              </div>
            </div>

            <div class="items-grid" v-if="userItems.length">
              <div v-for="item in userItems" :key="item.id" class="item-card">
                <div class="item-image">
                  <div class="placeholder-image">
                    <svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M12 2L15.09 8.26L22 9L17 14L18.18 21L12 17.77L5.82 21L7 14L2 9L8.91 8.26L12 2Z" fill="currentColor"/>
                    </svg>
                  </div>
                </div>
                <div class="item-content">
                  <h3 class="item-title">{{ item.title }}</h3>
                  <p class="item-description">{{ item.description }}</p>
                  <div class="item-meta">
                    <span class="item-category">{{ item.category }}</span>
                    <span class="item-price">${{ item.price }}</span>
                  </div>
                  <div class="item-status">
                    <span class="status-badge" :class="item.status">
                      {{ item.status }}
                    </span>
                  </div>
                  <div class="item-actions">
                    <button @click="editItem(item)" class="btn btn-sm btn-secondary">Edit</button>
                    <button @click="deleteItem(item)" class="btn btn-sm btn-danger">Delete</button>
                  </div>
                </div>
              </div>
            </div>

            <div v-else-if="!loading" class="empty-state">
              <div class="empty-icon">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12 2L15.09 8.26L22 9L17 14L18.18 21L12 17.77L5.82 21L7 14L2 9L8.91 8.26L12 2Z" stroke="currentColor" stroke-width="2"/>
                </svg>
              </div>
              <h3>No items yet</h3>
              <p>Start by adding your first vintage treasure or collectible</p>
              <button @click="showAddItemModal = true" class="btn btn-primary">Add Your First Item</button>
            </div>

            <div v-if="loading" class="loading-state">
              <div class="spinner"></div>
              <p>Loading your items...</p>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Add Item Modal -->
    <div v-if="showAddItemModal" class="modal-overlay" @click="closeModal">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h3>Add New Item</h3>
          <button @click="closeModal" class="close-btn">×</button>
        </div>
        <form @submit.prevent="addItem" class="modal-form">
          <div class="form-group">
            <label class="form-label">Title</label>
            <input v-model="newItem.title" type="text" class="form-input" required>
          </div>
          
          <div class="form-group">
            <label class="form-label">Description</label>
            <textarea v-model="newItem.description" class="form-input" rows="3" required></textarea>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label class="form-label">Category</label>
              <select v-model="newItem.category" class="form-input" required>
                <option value="">Select category</option>
                <option value="antiques">Antiques</option>
                <option value="collectibles">Collectibles</option>
                <option value="vintage">Vintage Items</option>
                <option value="art">Art & Decor</option>
                <option value="jewelry">Jewelry</option>
                <option value="books">Books & Manuscripts</option>
                <option value="toys">Toys & Games</option>
                <option value="other">Other</option>
              </select>
            </div>
            
            <div class="form-group">
              <label class="form-label">Price ($)</label>
              <input v-model="newItem.price" type="number" step="0.01" class="form-input" required>
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label class="form-label">Condition</label>
              <select v-model="newItem.condition" class="form-input">
                <option value="">Select condition</option>
                <option value="excellent">Excellent</option>
                <option value="very-good">Very Good</option>
                <option value="good">Good</option>
                <option value="fair">Fair</option>
                <option value="poor">Poor</option>
              </select>
            </div>
            
            <div class="form-group">
              <label class="form-label">Year (optional)</label>
              <input v-model="newItem.year" type="number" class="form-input">
            </div>
          </div>
          
          <div class="modal-actions">
            <button type="button" @click="closeModal" class="btn btn-secondary">Cancel</button>
            <button type="submit" class="btn btn-primary" :disabled="addingItem">
              <span v-if="addingItem" class="spinner"></span>
              <span v-else>Add Item</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'UserDashboard',
  data() {
    return {
      user: null,
      userItems: [],
      loading: false,
      showAddItemModal: false,
      addingItem: false,
      newItem: {
        title: '',
        description: '',
        category: '',
        price: '',
        condition: '',
        year: ''
      }
    }
  },
  async mounted() {
    await this.loadUserInfo()
    await this.loadUserItems()
  },
  methods: {
    async loadUserInfo() {
      try {
        const userInfo = localStorage.getItem('user_info')
        if (userInfo) {
          this.user = JSON.parse(userInfo)
        }
      } catch (error) {
        console.error('Error loading user info:', error)
      }
    },
    
    async loadUserItems() {
      this.loading = true
      try {
        const token = localStorage.getItem('access_token')
        const response = await axios.get('/api/user/dashboard', {
          headers: { Authorization: `Bearer ${token}` }
        })
        this.userItems = response.data.items
      } catch (error) {
        console.error('Error loading user items:', error)
      } finally {
        this.loading = false
      }
    },
    
    async addItem() {
      this.addingItem = true
      try {
        const token = localStorage.getItem('access_token')
        const response = await axios.post('/api/user/items', this.newItem, {
          headers: { Authorization: `Bearer ${token}` }
        })
        
        this.userItems.unshift(response.data.item)
        this.closeModal()
        this.resetForm()
      } catch (error) {
        console.error('Error adding item:', error)
        alert('Failed to add item. Please try again.')
      } finally {
        this.addingItem = false
      }
    },
    
    async editItem(item) {
      // Implement edit functionality
      console.log('Edit item:', item)
    },
    
    async deleteItem(item) {
      if (confirm(`Are you sure you want to delete "${item.title}"?`)) {
        try {
          const token = localStorage.getItem('access_token')
          await axios.delete(`/api/user/items/${item.id}`, {
            headers: { Authorization: `Bearer ${token}` }
          })
          
          this.userItems = this.userItems.filter(i => i.id !== item.id)
        } catch (error) {
          console.error('Error deleting item:', error)
          alert('Failed to delete item. Please try again.')
        }
      }
    },
    
    browseItems() {
      // Implement browse functionality
      console.log('Browse items')
    },
    
    closeModal() {
      this.showAddItemModal = false
      this.resetForm()
    },
    
    resetForm() {
      this.newItem = {
        title: '',
        description: '',
        category: '',
        price: '',
        condition: '',
        year: ''
      }
    },
    
    logout() {
      localStorage.removeItem('access_token')
      localStorage.removeItem('user_role')
      localStorage.removeItem('user_info')
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
.user-dashboard {
  min-height: 100vh;
  background: var(--background-light);
}

.dashboard-header {
  background: white;
  box-shadow: var(--shadow-sm);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 0;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.logo-text {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-primary);
  background: var(--gradient-vintage);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
}

.user-badge {
  background: var(--gradient-vintage);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.welcome-text {
  color: var(--text-secondary);
  font-weight: 500;
}

.dashboard-main {
  padding: 2rem 0;
}

.dashboard-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.quick-actions {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}

.action-card {
  background: white;
  padding: 2rem;
  border-radius: 0.75rem;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-light);
  text-align: center;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.action-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.action-icon {
  width: 3rem;
  height: 3rem;
  background: var(--gradient-vintage);
  color: white;
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
}

.action-card h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 0.5rem 0;
}

.action-card p {
  color: var(--text-secondary);
  margin: 0 0 1.5rem 0;
  line-height: 1.5;
}

.section {
  background: white;
  border-radius: 0.75rem;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-light);
  overflow: hidden;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid var(--border-light);
}

.section-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.section-actions {
  display: flex;
  gap: 1rem;
}

.items-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  padding: 1.5rem;
}

.item-card {
  border: 1px solid var(--border-light);
  border-radius: 0.5rem;
  overflow: hidden;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.item-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.item-image {
  height: 8rem;
  background: var(--background-light);
  display: flex;
  align-items: center;
  justify-content: center;
}

.placeholder-image {
  color: var(--text-light);
}

.item-content {
  padding: 1rem;
}

.item-title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 0.5rem 0;
}

.item-description {
  color: var(--text-secondary);
  font-size: 0.875rem;
  margin: 0 0 1rem 0;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.item-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.item-category {
  background: var(--background-light);
  color: var(--text-secondary);
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  text-transform: capitalize;
}

.item-price {
  font-weight: 600;
  color: var(--text-primary);
}

.item-status {
  margin-bottom: 1rem;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: capitalize;
}

.status-badge.available {
  background: #f0fdf4;
  color: #16a34a;
}

.status-badge.sold {
  background: #fef2f2;
  color: #dc2626;
}

.status-badge.pending {
  background: #fef3c7;
  color: #d97706;
}

.item-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-sm {
  padding: 0.5rem 1rem;
  font-size: 0.75rem;
  min-height: auto;
  flex: 1;
}

.btn-danger {
  background: #dc2626;
  color: white;
}

.btn-danger:hover {
  background: #b91c1c;
}

.empty-state {
  padding: 3rem;
  text-align: center;
  color: var(--text-secondary);
}

.empty-icon {
  width: 4rem;
  height: 4rem;
  margin: 0 auto 1rem;
  color: var(--text-light);
}

.empty-state h3 {
  color: var(--text-primary);
  margin: 0 0 0.5rem 0;
}

.empty-state p {
  margin: 0 0 1.5rem 0;
}

.loading-state {
  padding: 3rem;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  color: var(--text-secondary);
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
  z-index: 1000;
  padding: 1rem;
}

.modal {
  background: white;
  border-radius: 0.75rem;
  box-shadow: var(--shadow-lg);
  max-width: 500px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid var(--border-light);
}

.modal-header h3 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: var(--text-light);
  padding: 0;
  width: 2rem;
  height: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  color: var(--text-primary);
}

.modal-form {
  padding: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 1.5rem;
}

/* Responsive */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .header-actions {
    flex-direction: column;
    width: 100%;
  }
  
  .section-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .section-actions {
    flex-direction: column;
  }
  
  .items-grid {
    grid-template-columns: 1fr;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .dashboard-main {
    padding: 1rem 0;
  }
  
  .quick-actions {
    grid-template-columns: 1fr;
  }
  
  .modal {
    margin: 0;
    border-radius: 0;
    height: 100vh;
  }
}
</style>
