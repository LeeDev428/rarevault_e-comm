<template>
  <UserLayout>
    <div class="profile-container">
      <div class="profile-content">
        <!-- Profile Header -->
        <div class="profile-header">
          <div class="profile-avatar">
            <div class="avatar-circle">
              <span>{{ userInitials }}</span>
            </div>
            <button class="edit-avatar-btn">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
              </svg>
            </button>
          </div>
          
          <div class="profile-info">
            <h1 class="profile-name">{{ userProfile.name }}</h1>
            <p class="profile-email">{{ userProfile.email }}</p>
            <div class="profile-stats">
              <div class="stat-item">
                <span class="stat-number">{{ userProfile.ordersCount }}</span>
                <span class="stat-label">Orders</span>
              </div>
              <div class="stat-item">
                <span class="stat-number">{{ userProfile.wishlistCount }}</span>
                <span class="stat-label">Wishlist</span>
              </div>
              <div class="stat-item">
                <span class="stat-number">{{ userProfile.joinedDays }}</span>
                <span class="stat-label">Days Active</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Profile Form -->
        <div class="profile-form">
          <h2>Personal Information</h2>
          
          <form @submit.prevent="updateProfile" class="form-grid">
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

            <div class="form-group">
              <label for="phone">Phone Number</label>
              <input 
                type="tel" 
                id="phone" 
                v-model="profileForm.phone"
                class="form-input"
              />
            </div>

            <div class="form-group">
              <label for="address">Address</label>
              <textarea 
                id="address" 
                v-model="profileForm.address"
                class="form-input"
                rows="3"
              ></textarea>
            </div>

            <div class="form-group">
              <label for="city">City</label>
              <input 
                type="text" 
                id="city" 
                v-model="profileForm.city"
                class="form-input"
              />
            </div>

            <div class="form-group">
              <label for="postalCode">Postal Code</label>
              <input 
                type="text" 
                id="postalCode" 
                v-model="profileForm.postalCode"
                class="form-input"
              />
            </div>

            <div class="form-actions">
              <button type="submit" class="btn-primary" :disabled="saving">
                {{ saving ? 'Saving...' : 'Save Changes' }}
              </button>
              <button type="button" class="btn-secondary" @click="resetForm">
                Reset
              </button>
            </div>
          </form>
        </div>
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
.profile-container {
  max-width: 1000px;
  margin: 0 auto;
}

.profile-content {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* Profile Header */
.profile-header {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  padding: 40px;
  display: flex;
  align-items: center;
  gap: 32px;
}

.profile-avatar {
  position: relative;
}

.avatar-circle {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 36px;
  font-weight: 700;
  backdrop-filter: blur(10px);
}

.edit-avatar-btn {
  position: absolute;
  bottom: -5px;
  right: -5px;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #374151;
  color: white;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.2s ease;
}

.edit-avatar-btn:hover {
  background: #1f2937;
}

.profile-info {
  flex: 1;
}

.profile-name {
  font-size: 32px;
  font-weight: 700;
  margin: 0 0 8px 0;
}

.profile-email {
  font-size: 16px;
  opacity: 0.9;
  margin: 0 0 24px 0;
}

.profile-stats {
  display: flex;
  gap: 40px;
}

.stat-item {
  text-align: center;
}

.stat-number {
  display: block;
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  opacity: 0.8;
}

/* Profile Form */
.profile-form {
  padding: 40px;
}

.profile-form h2 {
  font-size: 24px;
  font-weight: 600;
  color: #111827;
  margin: 0 0 32px 0;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-size: 14px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 8px;
}

.form-input {
  padding: 12px 16px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 14px;
  transition: all 0.2s ease;
}

.form-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-input:invalid {
  border-color: #ef4444;
}

textarea.form-input {
  resize: vertical;
  min-height: 80px;
}

.form-actions {
  grid-column: 1 / -1;
  display: flex;
  gap: 16px;
  margin-top: 16px;
}

.btn-primary,
.btn-secondary {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary {
  background: #3b82f6;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #2563eb;
}

.btn-primary:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

.btn-secondary {
  background: #f3f4f6;
  color: #374151;
}

.btn-secondary:hover {
  background: #e5e7eb;
}

/* Responsive */
@media (max-width: 768px) {
  .profile-header {
    flex-direction: column;
    text-align: center;
    padding: 32px 24px;
    gap: 24px;
  }
  
  .profile-stats {
    gap: 24px;
  }
  
  .profile-form {
    padding: 24px;
  }
  
  .form-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .form-actions {
    flex-direction: column;
  }
}
</style>
