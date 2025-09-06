<template>
  <UserLayout>
    <div class="settings-container">
      <div class="settings-header">
        <h1 class="page-title">Account Settings</h1>
        <p class="page-description">Manage your account preferences and security settings</p>
      </div>

      <div class="settings-content">
        <!-- Settings Navigation -->
        <div class="settings-nav">
          <div class="nav-item" 
               v-for="section in settingSections" 
               :key="section.id"
               :class="{ active: activeSection === section.id }"
               @click="activeSection = section.id"
          >
            <svg class="nav-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <component :is="section.icon" />
            </svg>
            <span>{{ section.label }}</span>
          </div>
        </div>

        <!-- Settings Panels -->
        <div class="settings-panel">
          <!-- Account Settings -->
          <div v-if="activeSection === 'account'" class="panel-content">
            <h2 class="panel-title">Account Information</h2>
            
            <form @submit.prevent="updateAccount" class="settings-form">
              <div class="form-group">
                <label for="username">Username</label>
                <input 
                  type="text" 
                  id="username" 
                  v-model="accountSettings.username"
                  class="form-input"
                  required
                />
              </div>

              <div class="form-group">
                <label for="email">Email Address</label>
                <input 
                  type="email" 
                  id="email" 
                  v-model="accountSettings.email"
                  class="form-input"
                  required
                />
              </div>

              <div class="form-group">
                <label for="phone">Phone Number</label>
                <input 
                  type="tel" 
                  id="phone" 
                  v-model="accountSettings.phone"
                  class="form-input"
                />
              </div>

              <div class="form-group">
                <label for="bio">Bio</label>
                <textarea 
                  id="bio" 
                  v-model="accountSettings.bio"
                  class="form-input"
                  rows="4"
                  placeholder="Tell us about yourself..."
                ></textarea>
              </div>

              <button type="submit" class="btn-primary" :disabled="saving">
                {{ saving ? 'Saving...' : 'Save Changes' }}
              </button>
            </form>
          </div>

          <!-- Security Settings -->
          <div v-if="activeSection === 'security'" class="panel-content">
            <h2 class="panel-title">Security & Privacy</h2>
            
            <!-- Password Change -->
            <div class="security-section">
              <h3>Change Password</h3>
              <form @submit.prevent="changePassword" class="settings-form">
                <div class="form-group">
                  <label for="currentPassword">Current Password</label>
                  <input 
                    type="password" 
                    id="currentPassword" 
                    v-model="passwordForm.current"
                    class="form-input"
                    required
                  />
                </div>

                <div class="form-group">
                  <label for="newPassword">New Password</label>
                  <input 
                    type="password" 
                    id="newPassword" 
                    v-model="passwordForm.new"
                    class="form-input"
                    required
                  />
                </div>

                <div class="form-group">
                  <label for="confirmPassword">Confirm New Password</label>
                  <input 
                    type="password" 
                    id="confirmPassword" 
                    v-model="passwordForm.confirm"
                    class="form-input"
                    required
                  />
                </div>

                <button type="submit" class="btn-primary" :disabled="saving">
                  Update Password
                </button>
              </form>
            </div>

            <!-- Two-Factor Authentication -->
            <div class="security-section">
              <h3>Two-Factor Authentication</h3>
              <div class="security-option">
                <div class="option-info">
                  <p>Add an extra layer of security to your account</p>
                  <span class="status-badge" :class="twoFactorEnabled ? 'enabled' : 'disabled'">
                    {{ twoFactorEnabled ? 'Enabled' : 'Disabled' }}
                  </span>
                </div>
                <button 
                  @click="toggleTwoFactor" 
                  class="btn-secondary"
                >
                  {{ twoFactorEnabled ? 'Disable' : 'Enable' }}
                </button>
              </div>
            </div>
          </div>

          <!-- Notifications Settings -->
          <div v-if="activeSection === 'notifications'" class="panel-content">
            <h2 class="panel-title">Notification Preferences</h2>
            
            <div class="notification-section">
              <h3>Email Notifications</h3>
              <div class="notification-options">
                <label class="notification-option">
                  <input 
                    type="checkbox" 
                    v-model="notificationSettings.orderUpdates"
                  />
                  <span>Order updates and shipping notifications</span>
                </label>
                
                <label class="notification-option">
                  <input 
                    type="checkbox" 
                    v-model="notificationSettings.promotions"
                  />
                  <span>Promotions and special offers</span>
                </label>
                
                <label class="notification-option">
                  <input 
                    type="checkbox" 
                    v-model="notificationSettings.newItems"
                  />
                  <span>New items from followed sellers</span>
                </label>
                
                <label class="notification-option">
                  <input 
                    type="checkbox" 
                    v-model="notificationSettings.priceDrops"
                  />
                  <span>Price drops on wishlist items</span>
                </label>
              </div>
            </div>

            <div class="notification-section">
              <h3>Push Notifications</h3>
              <div class="notification-options">
                <label class="notification-option">
                  <input 
                    type="checkbox" 
                    v-model="notificationSettings.messages"
                  />
                  <span>Messages from sellers</span>
                </label>
                
                <label class="notification-option">
                  <input 
                    type="checkbox" 
                    v-model="notificationSettings.bidding"
                  />
                  <span>Bidding and auction updates</span>
                </label>
              </div>
            </div>

            <button @click="saveNotifications" class="btn-primary" :disabled="saving">
              {{ saving ? 'Saving...' : 'Save Preferences' }}
            </button>
          </div>

          <!-- Privacy Settings -->
          <div v-if="activeSection === 'privacy'" class="panel-content">
            <h2 class="panel-title">Privacy Settings</h2>
            
            <div class="privacy-section">
              <h3>Profile Visibility</h3>
              <div class="privacy-options">
                <label class="privacy-option">
                  <input 
                    type="radio" 
                    v-model="privacySettings.profileVisibility"
                    value="public"
                    name="profileVisibility"
                  />
                  <span>Public - Anyone can see your profile</span>
                </label>
                
                <label class="privacy-option">
                  <input 
                    type="radio" 
                    v-model="privacySettings.profileVisibility"
                    value="private"
                    name="profileVisibility"
                  />
                  <span>Private - Only you can see your profile</span>
                </label>
              </div>
            </div>

            <div class="privacy-section">
              <h3>Data & Analytics</h3>
              <div class="privacy-options">
                <label class="privacy-option">
                  <input 
                    type="checkbox" 
                    v-model="privacySettings.analytics"
                  />
                  <span>Allow analytics to improve your experience</span>
                </label>
                
                <label class="privacy-option">
                  <input 
                    type="checkbox" 
                    v-model="privacySettings.marketing"
                  />
                  <span>Allow marketing communications</span>
                </label>
              </div>
            </div>

            <button @click="savePrivacy" class="btn-primary" :disabled="saving">
              {{ saving ? 'Saving...' : 'Save Settings' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </UserLayout>
</template>

<script>
import UserLayout from '@/components/user/UserLayout.vue'

export default {
  name: 'UserSettings',
  components: {
    UserLayout
  },
  data() {
    return {
      activeSection: 'account',
      saving: false,
      twoFactorEnabled: false,
      settingSections: [
        { 
          id: 'account', 
          label: 'Account', 
          icon: 'path'
        },
        { 
          id: 'security', 
          label: 'Security', 
          icon: 'path'
        },
        { 
          id: 'notifications', 
          label: 'Notifications', 
          icon: 'path'
        },
        { 
          id: 'privacy', 
          label: 'Privacy', 
          icon: 'path'
        }
      ],
      accountSettings: {
        username: 'johndoe',
        email: 'john.doe@example.com',
        phone: '+1 (555) 123-4567',
        bio: 'Vintage collector and enthusiast. Love finding unique pieces with history.'
      },
      passwordForm: {
        current: '',
        new: '',
        confirm: ''
      },
      notificationSettings: {
        orderUpdates: true,
        promotions: false,
        newItems: true,
        priceDrops: true,
        messages: true,
        bidding: false
      },
      privacySettings: {
        profileVisibility: 'public',
        analytics: true,
        marketing: false
      }
    }
  },
  methods: {
    async updateAccount() {
      this.saving = true
      
      try {
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1500))
        console.log('Account updated successfully')
      } catch (error) {
        console.error('Error updating account:', error)
      } finally {
        this.saving = false
      }
    },
    
    async changePassword() {
      if (this.passwordForm.new !== this.passwordForm.confirm) {
        alert('New passwords do not match')
        return
      }
      
      this.saving = true
      
      try {
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1500))
        console.log('Password changed successfully')
        
        // Reset form
        this.passwordForm = {
          current: '',
          new: '',
          confirm: ''
        }
      } catch (error) {
        console.error('Error changing password:', error)
      } finally {
        this.saving = false
      }
    },
    
    toggleTwoFactor() {
      this.twoFactorEnabled = !this.twoFactorEnabled
      console.log('Two-factor authentication:', this.twoFactorEnabled ? 'enabled' : 'disabled')
    },
    
    async saveNotifications() {
      this.saving = true
      
      try {
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1000))
        console.log('Notification preferences saved')
      } catch (error) {
        console.error('Error saving notifications:', error)
      } finally {
        this.saving = false
      }
    },
    
    async savePrivacy() {
      this.saving = true
      
      try {
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1000))
        console.log('Privacy settings saved')
      } catch (error) {
        console.error('Error saving privacy settings:', error)
      } finally {
        this.saving = false
      }
    }
  }
}
</script>

<style scoped>
.settings-container {
  max-width: 1200px;
  margin: 0 auto;
}

/* Settings Header */
.settings-header {
  margin-bottom: 32px;
}

.page-title {
  font-size: 32px;
  font-weight: 700;
  color: #111827;
  margin: 0 0 8px 0;
}

.page-description {
  font-size: 16px;
  color: #6b7280;
  margin: 0;
}

/* Settings Content */
.settings-content {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 32px;
}

/* Settings Navigation */
.settings-nav {
  background: white;
  border-radius: 12px;
  padding: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  height: fit-content;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  color: #6b7280;
  font-weight: 500;
}

.nav-item:hover {
  background: #f3f4f6;
  color: #374151;
}

.nav-item.active {
  background: #eff6ff;
  color: #2563eb;
}

.nav-icon {
  flex-shrink: 0;
}

/* Settings Panel */
.settings-panel {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.panel-content {
  padding: 32px;
}

.panel-title {
  font-size: 24px;
  font-weight: 600;
  color: #111827;
  margin: 0 0 24px 0;
}

/* Form Styles */
.settings-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-size: 14px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 6px;
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

textarea.form-input {
  resize: vertical;
  min-height: 100px;
}

/* Security Sections */
.security-section {
  margin-bottom: 32px;
  padding-bottom: 32px;
  border-bottom: 1px solid #e5e7eb;
}

.security-section:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.security-section h3 {
  font-size: 18px;
  font-weight: 600;
  color: #111827;
  margin: 0 0 16px 0;
}

.security-option {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background: #f9fafb;
  border-radius: 8px;
}

.option-info p {
  margin: 0 0 4px 0;
  color: #374151;
}

.status-badge {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
}

.status-badge.enabled {
  background: #d1fae5;
  color: #065f46;
}

.status-badge.disabled {
  background: #fee2e2;
  color: #991b1b;
}

/* Notification Sections */
.notification-section {
  margin-bottom: 32px;
}

.notification-section h3 {
  font-size: 18px;
  font-weight: 600;
  color: #111827;
  margin: 0 0 16px 0;
}

.notification-options {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.notification-option {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  padding: 8px 0;
}

.notification-option input[type="checkbox"] {
  width: 18px;
  height: 18px;
}

.notification-option span {
  color: #374151;
  font-size: 14px;
}

/* Privacy Sections */
.privacy-section {
  margin-bottom: 32px;
}

.privacy-section h3 {
  font-size: 18px;
  font-weight: 600;
  color: #111827;
  margin: 0 0 16px 0;
}

.privacy-options {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.privacy-option {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  cursor: pointer;
  padding: 8px 0;
}

.privacy-option input[type="radio"],
.privacy-option input[type="checkbox"] {
  width: 18px;
  height: 18px;
  margin-top: 2px;
}

.privacy-option span {
  color: #374151;
  font-size: 14px;
  line-height: 1.5;
}

/* Buttons */
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
  .settings-content {
    grid-template-columns: 1fr;
    gap: 24px;
  }
  
  .settings-nav {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    gap: 8px;
  }
  
  .nav-item {
    flex-direction: column;
    text-align: center;
    gap: 8px;
    padding: 12px 8px;
  }
  
  .panel-content {
    padding: 24px;
  }
  
  .security-option {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
}
</style>
