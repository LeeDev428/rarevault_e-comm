<template>
  <UserLayout>
    <div class="profile-container">
      <!-- Header -->
      <div class="profile-header">
        <h1 class="page-title">Profile</h1>
        <p class="page-subtitle">Manage your personal information and preferences</p>
      </div>

      <!-- Profile Overview Card -->
      <div class="profile-overview">
        <div class="avatar-section">
          <div class="avatar-circle">
            <span>{{ userInitials }}</span>
          </div>
          <button class="edit-avatar-btn">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
              <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
            </svg>
          </button>
        </div>
        
        <div class="profile-meta">
          <h2 class="profile-name">{{ userProfile.name }}</h2>
          <p class="profile-email">{{ userProfile.email }}</p>
        </div>
        
        <div class="profile-stats">
          <div class="stat-item">
            <span class="stat-number">{{ userProfile.ordersCount }}</span>
            <span class="stat-label">Orders</span>
          </div>
          <div class="stat-divider"></div>
          <div class="stat-item">
            <span class="stat-number">{{ userProfile.wishlistCount }}</span>
            <span class="stat-label">Wishlist</span>
          </div>
          <div class="stat-divider"></div>
          <div class="stat-item">
            <span class="stat-number">{{ userProfile.joinedDays }}</span>
            <span class="stat-label">Days Active</span>
          </div>
        </div>
      </div>

      <!-- Personal Information Card -->
      <div class="info-card">
        <div class="card-header">
          <h3 class="card-title">Personal Information</h3>
        </div>
        
        <form @submit.prevent="updateProfile" class="info-form">
          <div class="form-row">
            <div class="form-group">
              <label for="name">Full Name</label>
              <input 
                type="text" 
                id="name" 
                v-model="profileForm.name"
                class="form-input"
                required
              />
            </div>

            <div class="form-group">
              <label for="email">Email Address</label>
              <input 
                type="email" 
                id="email" 
                v-model="profileForm.email"
                class="form-input"
                required
              />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="phone">Phone Number</label>
              <input 
                type="tel" 
                id="phone" 
                v-model="profileForm.phone"
                class="form-input"
                placeholder="+1 (555) 123-4567"
              />
            </div>

            <div class="form-group">
              <label for="city">City</label>
              <input 
                type="text" 
                id="city" 
                v-model="profileForm.city"
                class="form-input"
                placeholder="Enter your city"
              />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group full-width">
              <label for="address">Address</label>
              <textarea 
                id="address" 
                v-model="profileForm.address"
                class="form-input"
                rows="2"
                placeholder="Enter your full address"
              ></textarea>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="postalCode">Postal Code</label>
              <input 
                type="text" 
                id="postalCode" 
                v-model="profileForm.postalCode"
                class="form-input"
                placeholder="10001"
              />
            </div>
          </div>

          <div class="form-actions">
            <button type="button" class="btn-secondary" @click="resetForm">
              Reset
            </button>
            <button type="submit" class="btn-primary" :disabled="saving">
              {{ saving ? 'Saving...' : 'Save Changes' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </UserLayout>
</template>

<script>
import UserLayout from '@/components/user/UserLayout.vue'

export default {
  name: 'UserProfile',
  components: {
    UserLayout
  },
  data() {
    return {
      saving: false,
      userProfile: {
        name: 'John Doe',
        email: 'john.doe@example.com',
        ordersCount: 12,
        wishlistCount: 8,
        joinedDays: 45
      },
      profileForm: {
        name: 'John Doe',
        email: 'john.doe@example.com',
        phone: '+1 (555) 123-4567',
        address: '123 Main Street, Apt 4B',
        city: 'New York',
        postalCode: '10001'
      }
    }
  },
  computed: {
    userInitials() {
      return this.userProfile.name
        .split(' ')
        .map(name => name[0])
        .join('')
        .toUpperCase()
    }
  },
  methods: {
    async updateProfile() {
      this.saving = true
      
      try {
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1500))
        
        // Update user profile
        this.userProfile.name = this.profileForm.name
        this.userProfile.email = this.profileForm.email
        
        console.log('Profile updated successfully')
        
      } catch (error) {
        console.error('Error updating profile:', error)
      } finally {
        this.saving = false
      }
    },
    
    resetForm() {
      this.profileForm = {
        name: this.userProfile.name,
        email: this.userProfile.email,
        phone: '+1 (555) 123-4567',
        address: '123 Main Street, Apt 4B',
        city: 'New York',
        postalCode: '10001'
      }
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* {
  font-family: 'Inter', sans-serif;
}

.profile-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 0;
}

/* Header */
.profile-header {
  margin-bottom: 2rem;
}

.page-title {
  font-size: 1.875rem;
  font-weight: 700;
  color: #111827;
  margin: 0 0 0.5rem 0;
  letter-spacing: -0.025em;
}

.page-subtitle {
  font-size: 0.875rem;
  color: #6b7280;
  margin: 0;
  line-height: 1.5;
}

/* Profile Overview Card */
.profile-overview {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 2rem;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 2rem;
}

.avatar-section {
  position: relative;
  flex-shrink: 0;
}

.avatar-circle {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: #f3f4f6;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.75rem;
  font-weight: 600;
  color: #374151;
  border: 2px solid #e5e7eb;
}

.edit-avatar-btn {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #111827;
  color: white;
  border: 2px solid white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.15s ease;
}

.edit-avatar-btn:hover {
  background: #000000;
}

.profile-meta {
  flex: 1;
}

.profile-name {
  font-size: 1.5rem;
  font-weight: 600;
  color: #111827;
  margin: 0 0 0.25rem 0;
  letter-spacing: -0.025em;
}

.profile-email {
  font-size: 0.875rem;
  color: #6b7280;
  margin: 0;
}

.profile-stats {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 0 1.5rem;
  border-left: 1px solid #e5e7eb;
}

.stat-item {
  text-align: center;
}

.stat-number {
  display: block;
  font-size: 1.5rem;
  font-weight: 700;
  color: #111827;
  margin-bottom: 0.25rem;
  letter-spacing: -0.025em;
}

.stat-label {
  font-size: 0.75rem;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.stat-divider {
  width: 1px;
  height: 2rem;
  background: #e5e7eb;
}

/* Info Card */
.info-card {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  overflow: hidden;
}

.card-header {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.card-title {
  font-size: 1rem;
  font-weight: 600;
  color: #111827;
  margin: 0;
  letter-spacing: -0.025em;
}

/* Form */
.info-form {
  padding: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1rem;
}

.form-row:last-of-type {
  margin-bottom: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.form-group label {
  font-size: 0.75rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.form-input {
  padding: 0.625rem 0.875rem;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  font-size: 0.875rem;
  color: #111827;
  transition: all 0.15s ease;
  background: #ffffff;
}

.form-input::placeholder {
  color: #9ca3af;
}

.form-input:focus {
  outline: none;
  border-color: #111827;
  background: #ffffff;
}

textarea.form-input {
  resize: vertical;
  min-height: 60px;
  line-height: 1.5;
}

/* Form Actions */
.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  padding-top: 1rem;
  border-top: 1px solid #e5e7eb;
}

.btn-primary,
.btn-secondary {
  padding: 0.625rem 1.25rem;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s ease;
  border: 1px solid transparent;
}

.btn-primary {
  background: #111827;
  color: white;
  border-color: #111827;
}

.btn-primary:hover:not(:disabled) {
  background: #000000;
  border-color: #000000;
}

.btn-primary:disabled {
  background: #d1d5db;
  border-color: #d1d5db;
  color: #9ca3af;
  cursor: not-allowed;
}

.btn-secondary {
  background: white;
  color: #374151;
  border-color: #e5e7eb;
}

.btn-secondary:hover {
  background: #f9fafb;
  border-color: #d1d5db;
}

/* Responsive */
@media (max-width: 768px) {
  .profile-overview {
    flex-direction: column;
    align-items: flex-start;
    gap: 1.5rem;
    padding: 1.5rem;
  }
  
  .profile-stats {
    width: 100%;
    padding: 1rem 0 0 0;
    border-left: none;
    border-top: 1px solid #e5e7eb;
    justify-content: space-around;
  }
  
  .stat-divider {
    display: none;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .info-form {
    padding: 1.25rem;
  }
  
  .form-actions {
    flex-direction: column-reverse;
  }
  
  .btn-primary,
  .btn-secondary {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .page-title {
    font-size: 1.5rem;
  }
  
  .profile-name {
    font-size: 1.25rem;
  }
  
  .avatar-circle {
    width: 70px;
    height: 70px;
    font-size: 1.5rem;
  }
  
  .stat-number {
    font-size: 1.25rem;
  }
}
</style>
