<template>
  <SellerLayout>
    <div class="create-message-container">
      <!-- Header -->
      <div class="page-header">
        <div class="header-content">
          <h1 class="page-title">Start New Conversation</h1>
          <p class="page-subtitle">Reach out to customers about your items</p>
        </div>
        <router-link to="/seller/messages" class="back-btn">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="m15 18-6-6 6-6"/>
          </svg>
          Back to Messages
        </router-link>
      </div>

      <!-- Error Banner -->
      <div v-if="error" class="error-banner">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"/>
          <line x1="15" y1="9" x2="9" y2="15"/>
          <line x1="9" y1="9" x2="15" y2="15"/>
        </svg>
        {{ error }}
        <button @click="error = ''" class="close-error">×</button>
      </div>

      <!-- Main Content -->
      <div class="create-content">
        <!-- Step Indicator -->
        <div class="step-indicator">
          <div class="step" :class="{ active: currentStep === 1, completed: currentStep > 1 }">
            <div class="step-number">1</div>
            <div class="step-label">Select Item</div>
          </div>
          <div class="step-divider"></div>
          <div class="step" :class="{ active: currentStep === 2, completed: currentStep > 2 }">
            <div class="step-number">2</div>
            <div class="step-label">Choose Customer</div>
          </div>
          <div class="step-divider"></div>
          <div class="step" :class="{ active: currentStep === 3 }">
            <div class="step-number">3</div>
            <div class="step-label">Write Message</div>
          </div>
        </div>

        <!-- Step 1: Select Item -->
        <div v-if="currentStep === 1" class="step-content">
          <div class="step-header">
            <h2>Select an Item</h2>
            <p>Choose which item you want to start a conversation about</p>
          </div>

          <!-- Item Search -->
          <div class="search-section">
            <div class="search-input-wrapper">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="11" cy="11" r="8"/>
                <path d="m21 21-4.35-4.35"/>
              </svg>
              <input
                type="text"
                v-model="itemSearch"
                placeholder="Search your items..."
                class="search-input"
              />
            </div>
          </div>

          <!-- Items Grid -->
          <div v-if="loading.items" class="loading-section">
            <div class="loading-spinner"></div>
            <p>Loading your items...</p>
          </div>

          <div v-else-if="filteredItems.length === 0" class="empty-section">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
              <circle cx="9" cy="9" r="2"/>
              <path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/>
            </svg>
            <h3>No Items Found</h3>
            <p>{{ itemSearch ? 'No items match your search.' : 'You haven\'t listed any items yet.' }}</p>
            <router-link to="/seller/items/create" class="create-item-btn">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="12" y1="5" x2="12" y2="19"/>
                <line x1="5" y1="12" x2="19" y2="12"/>
              </svg>
              Create Your First Item
            </router-link>
          </div>

          <div v-else class="items-grid">
            <div 
              v-for="item in filteredItems" 
              :key="item.id"
              class="item-card"
              :class="{ selected: selectedItem?.id === item.id }"
              @click="selectItem(item)"
            >
              <div class="item-image-container">
                <img 
                  v-if="item.images && item.images.length > 0" 
                  :src="getImageUrl(item.images[0])"
                  :alt="item.title"
                  class="item-image"
                  @error="handleImageError"
                />
                <div v-else class="no-image">
                  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                    <circle cx="9" cy="9" r="2"/>
                    <path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/>
                  </svg>
                </div>
                <div v-if="selectedItem?.id === item.id" class="selected-indicator">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
                    <polyline points="20,6 9,17 4,12"/>
                  </svg>
                </div>
              </div>
              
              <div class="item-details">
                <h3 class="item-title">{{ item.title }}</h3>
                <p class="item-description">{{ truncateText(item.description, 80) }}</p>
                <div class="item-meta">
                  <span class="item-price">${{ formatPrice(item.price) }}</span>
                  <span class="item-status" :class="item.status">{{ item.status }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Continue Button -->
          <div v-if="selectedItem" class="step-actions">
            <button @click="goToStep(2)" class="continue-btn">
              Continue with "{{ selectedItem.title }}"
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="m9 18 6-6-6-6"/>
              </svg>
            </button>
          </div>
        </div>

        <!-- Step 2: Choose Customer -->
        <div v-if="currentStep === 2" class="step-content">
          <div class="step-header">
            <h2>Choose Customer</h2>
            <p>Select who you want to message about "{{ selectedItem?.title }}"</p>
          </div>

          <!-- Customer Search -->
          <div class="search-section">
            <div class="search-input-wrapper">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="11" cy="11" r="8"/>
                <path d="m21 21-4.35-4.35"/>
              </svg>
              <input
                type="text"
                v-model="customerSearch"
                placeholder="Search customers by name or email..."
                class="search-input"
              />
            </div>
          </div>

          <!-- Customer Type Filter -->
          <div class="filter-section">
            <div class="filter-tabs">
              <button 
                @click="customerFilter = 'all'"
                class="filter-tab"
                :class="{ active: customerFilter === 'all' }"
              >
                All Customers
              </button>
              <button 
                @click="customerFilter = 'interested'"
                class="filter-tab"
                :class="{ active: customerFilter === 'interested' }"
              >
                Interested in This Item
              </button>
              <button 
                @click="customerFilter = 'purchased'"
                class="filter-tab"
                :class="{ active: customerFilter === 'purchased' }"
              >
                Previous Buyers
              </button>
            </div>
          </div>

          <!-- Customers List -->
          <div v-if="loading.customers" class="loading-section">
            <div class="loading-spinner"></div>
            <p>Loading customers...</p>
          </div>

          <div v-else-if="filteredCustomers.length === 0" class="empty-section">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
              <circle cx="9" cy="7" r="4"/>
              <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
              <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
            </svg>
            <h3>No Customers Found</h3>
            <p>{{ customerSearch ? 'No customers match your search.' : 'No customers available for this filter.' }}</p>
          </div>

          <div v-else class="customers-list">
            <div 
              v-for="customer in filteredCustomers" 
              :key="customer.id"
              class="customer-card"
              :class="{ selected: selectedCustomer?.id === customer.id }"
              @click="selectCustomer(customer)"
            >
              <div class="customer-avatar">
                <div class="avatar-circle">
                  {{ getInitials(customer.username) }}
                </div>
                <div v-if="selectedCustomer?.id === customer.id" class="selected-indicator">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
                    <polyline points="20,6 9,17 4,12"/>
                  </svg>
                </div>
              </div>
              
              <div class="customer-info">
                <div class="customer-header">
                  <h3 class="customer-name">{{ customer.username }}</h3>
                  <div class="customer-badges">
                    <span v-if="customer.isInterestedInItem" class="badge interested">Interested</span>
                    <span v-if="customer.hasPurchasedFromSeller" class="badge buyer">Previous Buyer</span>
                  </div>
                </div>
                <p class="customer-email">{{ customer.email }}</p>
                <div class="customer-stats">
                  <span class="stat">{{ customer.totalOrders || 0 }} orders</span>
                  <span class="stat">Member since {{ formatDate(customer.created_at) }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Step Actions -->
          <div class="step-actions">
            <button @click="goToStep(1)" class="back-btn secondary">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="m15 18-6-6 6-6"/>
              </svg>
              Back to Items
            </button>
            <button 
              v-if="selectedCustomer" 
              @click="goToStep(3)" 
              class="continue-btn"
            >
              Message {{ selectedCustomer.username }}
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="m9 18 6-6-6-6"/>
              </svg>
            </button>
          </div>
        </div>

        <!-- Step 3: Write Message -->
        <div v-if="currentStep === 3" class="step-content">
          <div class="step-header">
            <h2>Write Your Message</h2>
            <p>Compose your message to {{ selectedCustomer?.username }} about "{{ selectedItem?.title }}"</p>
          </div>

          <!-- Conversation Preview -->
          <div class="conversation-preview">
            <div class="preview-header">
              <h3>Conversation Preview</h3>
            </div>
            
            <div class="preview-participants">
              <div class="participant">
                <div class="participant-avatar">
                  {{ getInitials(selectedCustomer?.username || '') }}
                </div>
                <div class="participant-info">
                  <span class="participant-name">{{ selectedCustomer?.username }}</span>
                  <span class="participant-role">Customer</span>
                </div>
              </div>
              
              <div class="conversation-about">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
                </svg>
                About: {{ selectedItem?.title }}
              </div>
            </div>

            <div class="preview-item">
              <div class="item-preview">
                <div class="item-image-small">
                  <img 
                    v-if="selectedItem?.images && selectedItem.images.length > 0" 
                    :src="getImageUrl(selectedItem.images[0])"
                    :alt="selectedItem.title"
                    class="preview-image"
                  />
                  <div v-else class="no-preview-image">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                      <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                      <circle cx="9" cy="9" r="2"/>
                      <path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/>
                    </svg>
                  </div>
                </div>
                <div class="item-preview-info">
                  <h4>{{ selectedItem?.title }}</h4>
                  <p class="preview-price">${{ formatPrice(selectedItem?.price || 0) }}</p>
                  <span class="preview-status" :class="selectedItem?.status">{{ selectedItem?.status }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Message Form -->
          <form @submit.prevent="sendMessage" class="message-form">
            <div class="form-group">
              <label for="subject" class="form-label">Subject (Optional)</label>
              <input
                id="subject"
                type="text"
                v-model="messageForm.subject"
                placeholder="e.g., Question about your item"
                class="form-input"
                :disabled="loading.sending"
              />
            </div>

            <div class="form-group">
              <label for="message" class="form-label">Message *</label>
              <textarea
                id="message"
                v-model="messageForm.content"
                placeholder="Write your message here..."
                class="form-textarea"
                rows="6"
                required
                :disabled="loading.sending"
              ></textarea>
              <div class="character-count">
                {{ messageForm.content.length }}/{{ maxMessageLength }} characters
              </div>
            </div>

            <!-- Quick Templates -->
            <div class="quick-templates">
              <h4>Quick Templates</h4>
              <div class="template-buttons">
                <button 
                  type="button"
                  @click="useTemplate('greeting')"
                  class="template-btn"
                  :disabled="loading.sending"
                >
                  Friendly Greeting
                </button>
                <button 
                  type="button"
                  @click="useTemplate('question')"
                  class="template-btn"
                  :disabled="loading.sending"
                >
                  Ask Question
                </button>
                <button 
                  type="button"
                  @click="useTemplate('offer')"
                  class="template-btn"
                  :disabled="loading.sending"
                >
                  Special Offer
                </button>
                <button 
                  type="button"
                  @click="useTemplate('followup')"
                  class="template-btn"
                  :disabled="loading.sending"
                >
                  Follow Up
                </button>
              </div>
            </div>

            <!-- Form Actions -->
            <div class="form-actions">
              <button 
                type="button" 
                @click="goToStep(2)" 
                class="back-btn secondary"
                :disabled="loading.sending"
              >
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="m15 18-6-6 6-6"/>
                </svg>
                Back to Customers
              </button>
              
              <button 
                type="submit" 
                class="send-btn"
                :disabled="!messageForm.content.trim() || loading.sending"
              >
                <svg v-if="loading.sending" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="spinning">
                  <path d="M21 12a9 9 0 11-6.219-8.56"/>
                </svg>
                <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="22" y1="2" x2="11" y2="13"/>
                  <polygon points="22,2 15,22 11,13 2,9 22,2"/>
                </svg>
                {{ loading.sending ? 'Sending...' : 'Send Message' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </SellerLayout>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import SellerLayout from '../../layouts/SellerLayout.vue'

export default {
  name: 'CreateMessage',
  components: {
    SellerLayout
  },
  setup() {
    const router = useRouter()
    
    // Reactive data
    const currentStep = ref(1)
    const error = ref('')
    
    const loading = ref({
      items: false,
      customers: false,
      sending: false
    })
    
    // Items
    const items = ref([])
    const selectedItem = ref(null)
    const itemSearch = ref('')
    
    // Customers
    const customers = ref([])
    const selectedCustomer = ref(null)
    const customerSearch = ref('')
    const customerFilter = ref('all')
    
    // Message form
    const messageForm = ref({
      subject: '',
      content: ''
    })
    const maxMessageLength = 2000
    
    // Computed properties
    const filteredItems = computed(() => {
      if (!itemSearch.value) return items.value
      const search = itemSearch.value.toLowerCase()
      return items.value.filter(item => 
        item.title.toLowerCase().includes(search) ||
        item.description.toLowerCase().includes(search)
      )
    })
    
    const filteredCustomers = computed(() => {
      let filtered = customers.value
      
      // Apply search filter
      if (customerSearch.value) {
        const search = customerSearch.value.toLowerCase()
        filtered = filtered.filter(customer => 
          customer.username.toLowerCase().includes(search) ||
          customer.email.toLowerCase().includes(search)
        )
      }
      
      // Apply type filter
      if (customerFilter.value === 'interested') {
        filtered = filtered.filter(customer => customer.isInterestedInItem)
      } else if (customerFilter.value === 'purchased') {
        filtered = filtered.filter(customer => customer.hasPurchasedFromSeller)
      }
      
      return filtered
    })
    
    // Methods
    const loadItems = async () => {
      try {
        loading.value.items = true
        const token = localStorage.getItem('token')
        const response = await axios.get('/api/seller/items', {
          headers: { Authorization: `Bearer ${token}` }
        })
        items.value = response.data.items || []
      } catch (err) {
        console.error('Error loading items:', err)
        error.value = 'Failed to load your items. Please try again.'
      } finally {
        loading.value.items = false
      }
    }
    
    const loadCustomers = async () => {
      try {
        loading.value.customers = true
        const token = localStorage.getItem('token')
        const params = selectedItem.value ? { item_id: selectedItem.value.id } : {}
        
        const response = await axios.get('/api/seller/customers', {
          headers: { Authorization: `Bearer ${token}` },
          params
        })
        customers.value = response.data.customers || []
      } catch (err) {
        console.error('Error loading customers:', err)
        error.value = 'Failed to load customers. Please try again.'
      } finally {
        loading.value.customers = false
      }
    }
    
    const selectItem = (item) => {
      selectedItem.value = item
    }
    
    const selectCustomer = (customer) => {
      selectedCustomer.value = customer
    }
    
    const goToStep = async (step) => {
      if (step === 2 && !selectedItem.value) {
        error.value = 'Please select an item first.'
        return
      }
      
      if (step === 3 && !selectedCustomer.value) {
        error.value = 'Please select a customer first.'
        return
      }
      
      currentStep.value = step
      
      // Load customers when going to step 2
      if (step === 2) {
        await loadCustomers()
      }
    }
    
    const sendMessage = async () => {
      if (!messageForm.value.content.trim()) {
        error.value = 'Please enter a message.'
        return
      }
      
      if (messageForm.value.content.length > maxMessageLength) {
        error.value = `Message is too long. Maximum ${maxMessageLength} characters allowed.`
        return
      }
      
      try {
        loading.value.sending = true
        const token = localStorage.getItem('token')
        
        const messageData = {
          recipient_id: selectedCustomer.value.id,
          content: messageForm.value.content.trim(),
          item_id: selectedItem.value.id
        }
        
        if (messageForm.value.subject.trim()) {
          messageData.subject = messageForm.value.subject.trim()
        }
        
        await axios.post('/api/messages/send', messageData, {
          headers: { Authorization: `Bearer ${token}` }
        })
        
        // Redirect to messages with success
        router.push({
          path: '/seller/messages',
          query: { success: 'Message sent successfully!' }
        })
        
      } catch (err) {
        console.error('Error sending message:', err)
        error.value = err.response?.data?.error || 'Failed to send message. Please try again.'
      } finally {
        loading.value.sending = false
      }
    }
    
    const useTemplate = (type) => {
      const templates = {
        greeting: `Hi ${selectedCustomer.value?.username || '[Customer]'}! I hope you're doing well. I wanted to reach out about my item "${selectedItem.value?.title || '[Item]'}".`,
        question: `Hi! I noticed you might be interested in "${selectedItem.value?.title || '[Item]'}". Do you have any questions about it?`,
        offer: `Hello! I have a special offer for "${selectedItem.value?.title || '[Item]'}". Would you like to hear about it?`,
        followup: `Hi ${selectedCustomer.value?.username || '[Customer]'}! I wanted to follow up with you about "${selectedItem.value?.title || '[Item]'}". Are you still interested?`
      }
      
      messageForm.value.content = templates[type] || ''
    }
    
    // Utility functions
    const getImageUrl = (imagePath) => {
      if (!imagePath) return '/placeholder.svg'
      return imagePath.startsWith('http') ? imagePath : `/uploads/${imagePath}`
    }
    
    const handleImageError = (event) => {
      event.target.src = '/placeholder.svg'
    }
    
    const getInitials = (name) => {
      if (!name) return '?'
      return name.split(' ').map(word => word[0]).join('').toUpperCase().slice(0, 2)
    }
    
    const formatPrice = (price) => {
      return parseFloat(price || 0).toFixed(2)
    }
    
    const formatDate = (dateString) => {
      if (!dateString) return 'Unknown'
      return new Date(dateString).getFullYear()
    }
    
    const truncateText = (text, length) => {
      if (!text) return ''
      return text.length > length ? text.substring(0, length) + '...' : text
    }
    
    // Lifecycle
    onMounted(() => {
      loadItems()
    })
    
    return {
      currentStep,
      error,
      loading,
      items,
      selectedItem,
      itemSearch,
      customers,
      selectedCustomer,
      customerSearch,
      customerFilter,
      messageForm,
      maxMessageLength,
      filteredItems,
      filteredCustomers,
      loadItems,
      loadCustomers,
      selectItem,
      selectCustomer,
      goToStep,
      sendMessage,
      useTemplate,
      getImageUrl,
      handleImageError,
      getInitials,
      formatPrice,
      formatDate,
      truncateText
    }
  }
}
</script>

<style scoped>
/* Main Container */
.create-message-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* Page Header */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 1px solid #e5e7eb;
}

.header-content h1.page-title {
  font-size: 32px;
  font-weight: 700;
  color: #111827;
  margin: 0 0 8px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.page-subtitle {
  margin: 0;
  color: #6b7280;
  font-size: 16px;
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  color: #475569;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.2s;
}

.back-btn:hover {
  background: #e2e8f0;
  border-color: #cbd5e1;
  color: #334155;
}

/* Error Banner */
.error-banner {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #dc2626;
  padding: 12px 16px;
  border-radius: 8px;
  margin-bottom: 24px;
  display: flex;
  align-items: center;
  gap: 8px;
  position: relative;
}

.close-error {
  position: absolute;
  right: 12px;
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
  color: #dc2626;
}

/* Step Indicator */
.step-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 48px;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.step-number {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #e5e7eb;
  color: #6b7280;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  transition: all 0.3s;
}

.step.active .step-number {
  background: #3b82f6;
  color: white;
}

.step.completed .step-number {
  background: #10b981;
  color: white;
}

.step-label {
  font-size: 14px;
  color: #6b7280;
  font-weight: 500;
}

.step.active .step-label {
  color: #3b82f6;
  font-weight: 600;
}

.step.completed .step-label {
  color: #10b981;
}

.step-divider {
  width: 60px;
  height: 2px;
  background: #e5e7eb;
  margin: 0 20px;
}

/* Step Content */
.step-content {
  background: white;
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid #e5e7eb;
}

.step-header {
  text-align: center;
  margin-bottom: 32px;
}

.step-header h2 {
  font-size: 24px;
  font-weight: 600;
  color: #111827;
  margin: 0 0 8px;
}

.step-header p {
  margin: 0;
  color: #6b7280;
  font-size: 16px;
}

/* Search Section */
.search-section {
  margin-bottom: 24px;
}

.search-input-wrapper {
  position: relative;
  max-width: 400px;
  margin: 0 auto;
}

.search-input-wrapper svg {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  color: #9ca3af;
}

.search-input {
  width: 100%;
  padding: 12px 16px 12px 48px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 14px;
  background: #f9fafb;
  transition: all 0.2s;
}

.search-input:focus {
  outline: none;
  border-color: #3b82f6;
  background: white;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* Filter Section */
.filter-section {
  margin-bottom: 24px;
}

.filter-tabs {
  display: flex;
  justify-content: center;
  gap: 8px;
}

.filter-tab {
  padding: 8px 16px;
  background: #f3f4f6;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  color: #6b7280;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-tab:hover {
  background: #e5e7eb;
}

.filter-tab.active {
  background: #3b82f6;
  border-color: #3b82f6;
  color: white;
}

/* Loading and Empty States */
.loading-section, .empty-section {
  text-align: center;
  padding: 60px 20px;
  color: #6b7280;
}

.loading-section svg, .empty-section svg {
  margin-bottom: 20px;
  color: #d1d5db;
}

.loading-spinner {
  width: 32px;
  height: 32px;
  border: 3px solid #e5e7eb;
  border-top: 3px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 16px;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.empty-section h3 {
  color: #374151;
  margin: 0 0 8px;
  font-size: 18px;
}

.empty-section p {
  margin: 0 0 20px;
  font-size: 14px;
}

.create-item-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: #3b82f6;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.2s;
}

.create-item-btn:hover {
  background: #2563eb;
  transform: translateY(-1px);
}

/* Items Grid */
.items-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

.item-card {
  background: white;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
}

.item-card:hover {
  border-color: #3b82f6;
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.item-card.selected {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.item-image-container {
  position: relative;
  height: 200px;
  background: #f3f4f6;
  display: flex;
  align-items: center;
  justify-content: center;
}

.item-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.no-image {
  color: #9ca3af;
}

.selected-indicator {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 32px;
  height: 32px;
  background: #10b981;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.item-details {
  padding: 16px;
}

.item-title {
  font-size: 16px;
  font-weight: 600;
  color: #111827;
  margin: 0 0 8px;
}

.item-description {
  font-size: 14px;
  color: #6b7280;
  margin: 0 0 12px;
  line-height: 1.4;
}

.item-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.item-price {
  font-size: 18px;
  font-weight: 700;
  color: #059669;
}

.item-status {
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
}

.item-status.active { background: #dcfce7; color: #16a34a; }
.item-status.sold { background: #fee2e2; color: #dc2626; }
.item-status.pending { background: #fef3c7; color: #d97706; }

/* Customers List */
.customers-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 32px;
  max-height: 400px;
  overflow-y: auto;
}

.customer-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
  background: white;
}

.customer-card:hover {
  border-color: #3b82f6;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.customer-card.selected {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.customer-avatar {
  position: relative;
  flex-shrink: 0;
}

.avatar-circle {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 18px;
}

.customer-avatar .selected-indicator {
  position: absolute;
  bottom: -4px;
  right: -4px;
  width: 24px;
  height: 24px;
  background: #10b981;
  border: 2px solid white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.customer-info {
  flex: 1;
}

.customer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.customer-name {
  font-size: 16px;
  font-weight: 600;
  color: #111827;
  margin: 0;
}

.customer-badges {
  display: flex;
  gap: 6px;
}

.badge {
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
}

.badge.interested { background: #dbeafe; color: #2563eb; }
.badge.buyer { background: #dcfce7; color: #16a34a; }

.customer-email {
  font-size: 14px;
  color: #6b7280;
  margin: 0 0 8px;
}

.customer-stats {
  display: flex;
  gap: 16px;
}

.stat {
  font-size: 12px;
  color: #9ca3af;
  font-weight: 500;
}

/* Conversation Preview */
.conversation-preview {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 24px;
}

.preview-header h3 {
  margin: 0 0 16px;
  font-size: 16px;
  font-weight: 600;
  color: #374151;
}

.preview-participants {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.participant {
  display: flex;
  align-items: center;
  gap: 12px;
}

.participant-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 14px;
}

.participant-info {
  display: flex;
  flex-direction: column;
}

.participant-name {
  font-size: 14px;
  font-weight: 600;
  color: #111827;
}

.participant-role {
  font-size: 12px;
  color: #6b7280;
  text-transform: uppercase;
  font-weight: 500;
}

.conversation-about {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #3b82f6;
  font-weight: 500;
}

.preview-item {
  padding-top: 16px;
  border-top: 1px solid #e2e8f0;
}

.item-preview {
  display: flex;
  align-items: center;
  gap: 12px;
}

.item-image-small {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  overflow: hidden;
  background: #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: center;
}

.preview-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.no-preview-image {
  color: #9ca3af;
}

.item-preview-info h4 {
  margin: 0 0 4px;
  font-size: 14px;
  font-weight: 600;
  color: #111827;
}

.preview-price {
  font-size: 16px;
  font-weight: 700;
  color: #059669;
  margin: 0 0 4px;
}

.preview-status {
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
}

.preview-status.active { background: #dcfce7; color: #16a34a; }
.preview-status.sold { background: #fee2e2; color: #dc2626; }
.preview-status.pending { background: #fef3c7; color: #d97706; }

/* Message Form */
.message-form {
  margin-bottom: 24px;
}

.form-group {
  margin-bottom: 20px;
}

.form-label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 8px;
}

.form-input, .form-textarea {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 14px;
  font-family: inherit;
  background: #f9fafb;
  transition: all 0.2s;
}

.form-input:focus, .form-textarea:focus {
  outline: none;
  border-color: #3b82f6;
  background: white;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-textarea {
  resize: vertical;
  min-height: 120px;
}

.character-count {
  text-align: right;
  font-size: 12px;
  color: #9ca3af;
  margin-top: 4px;
}

/* Quick Templates */
.quick-templates {
  margin-bottom: 24px;
}

.quick-templates h4 {
  margin: 0 0 12px;
  font-size: 14px;
  font-weight: 600;
  color: #374151;
}

.template-buttons {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.template-btn {
  padding: 8px 12px;
  background: #e5e7eb;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 12px;
  color: #4b5563;
  cursor: pointer;
  transition: all 0.2s;
}

.template-btn:hover:not(:disabled) {
  background: #d1d5db;
  border-color: #9ca3af;
}

.template-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Step Actions */
.step-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  margin-top: 32px;
}

.continue-btn, .send-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
}

.continue-btn:hover:not(:disabled), .send-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

.continue-btn:disabled, .send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
}

.back-btn.secondary {
  background: #f3f4f6;
  color: #6b7280;
  border: 1px solid #d1d5db;
  box-shadow: none;
}

.back-btn.secondary:hover:not(:disabled) {
  background: #e5e7eb;
  border-color: #9ca3af;
  color: #4b5563;
}

.spinning {
  animation: spin 1s linear infinite;
}

/* Form Actions */
.form-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  padding-top: 24px;
  border-top: 1px solid #e5e7eb;
}

/* Responsive Design */
@media (max-width: 768px) {
  .create-message-container {
    padding: 0 16px;
  }
  
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
  
  .step-content {
    padding: 20px;
  }
  
  .items-grid {
    grid-template-columns: 1fr;
  }
  
  .step-actions, .form-actions {
    flex-direction: column;
    gap: 12px;
  }
  
  .continue-btn, .send-btn, .back-btn {
    width: 100%;
    justify-content: center;
  }
  
  .template-buttons {
    flex-direction: column;
  }
  
  .template-btn {
    width: 100%;
    text-align: center;
  }
}
</style>
