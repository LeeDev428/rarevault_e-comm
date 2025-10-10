<template>
  <UserLayout>
    <div class="settings-container">
      <!-- Header -->
      <div class="settings-header">
        <h1 class="page-title">Settings</h1>
        <p class="page-subtitle">Manage your account preferences and security</p>
      </div>

      <!-- Settings Navigation Tabs -->
      <div class="settings-tabs">
        <button 
          v-for="section in settingSections" 
          :key="section.id"
          :class="['tab-button', { active: activeSection === section.id }]"
          @click="activeSection = section.id"
        >
          {{ section.label }}
        </button>
      </div>

      <!-- Settings Content -->
      <div class="settings-content">
        <!-- Account Settings -->
        <div v-if="activeSection === 'account'" class="settings-card">
          <div class="card-header">
            <h2 class="card-title">Account Information</h2>
          </div>
          
          <form @submit.prevent="updateAccount" class="card-content">
            <div class="form-row">
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
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="phone">Phone Number</label>
                <input 
                  type="tel" 
                  id="phone" 
                  v-model="accountSettings.phone"
                  class="form-input"
                  placeholder="+1 (555) 123-4567"
                />
              </div>
            </div>

            <div class="form-row">
              <div class="form-group full-width">
                <label for="bio">Bio</label>
                <textarea 
                  id="bio" 
                  v-model="accountSettings.bio"
                  class="form-input"
                  rows="3"
                  placeholder="Tell us about yourself..."
                ></textarea>
              </div>
            </div>

            <div class="form-actions">
              <button type="submit" class="btn-primary" :disabled="saving">
                {{ saving ? 'Saving...' : 'Save Changes' }}
              </button>
            </div>
          </form>
        </div>

        <!-- Security Settings -->
        <div v-if="activeSection === 'security'" class="settings-card">
          <div class="card-header">
            <h2 class="card-title">Security</h2>
          </div>
          
          <div class="card-content">
            <!-- Password Change -->
            <div class="setting-section">
              <h3 class="section-subtitle">Change Password</h3>
              <form @submit.prevent="changePassword" class="setting-form">
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
                  {{ saving ? 'Updating...' : 'Update Password' }}
                </button>
              </form>
            </div>

            <!-- Two-Factor Authentication -->
            <div class="setting-section">
              <h3 class="section-subtitle">Two-Factor Authentication</h3>
              <div class="setting-option">
                <div class="option-info">
                  <p class="option-text">Add an extra layer of security to your account</p>
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
        </div>

        <!-- Notifications Settings -->
        <div v-if="activeSection === 'notifications'" class="settings-card">
          <div class="card-header">
            <h2 class="card-title">Notifications</h2>
          </div>
          
          <div class="card-content">
            <div class="setting-section">
              <h3 class="section-subtitle">Email Notifications</h3>
              <div class="checkbox-group">
                <label class="checkbox-label">
                  <input 
                    type="checkbox" 
                    v-model="notificationSettings.orderUpdates"
                    class="checkbox-input"
                  />
                  <span>Order updates and shipping notifications</span>
                </label>
                
                <label class="checkbox-label">
                  <input 
                    type="checkbox" 
                    v-model="notificationSettings.promotions"
                    class="checkbox-input"
                  />
                  <span>Promotions and special offers</span>
                </label>
                
                <label class="checkbox-label">
                  <input 
                    type="checkbox" 
                    v-model="notificationSettings.newItems"
                    class="checkbox-input"
                  />
                  <span>New items from followed sellers</span>
                </label>
                
                <label class="checkbox-label">
                  <input 
                    type="checkbox" 
                    v-model="notificationSettings.priceDrops"
                    class="checkbox-input"
                  />
                  <span>Price drops on wishlist items</span>
                </label>
              </div>
            </div>

            <div class="setting-section">
              <h3 class="section-subtitle">Push Notifications</h3>
              <div class="checkbox-group">
                <label class="checkbox-label">
                  <input 
                    type="checkbox" 
                    v-model="notificationSettings.messages"
                    class="checkbox-input"
                  />
                  <span>Messages from sellers</span>
                </label>
                
                <label class="checkbox-label">
                  <input 
                    type="checkbox" 
                    v-model="notificationSettings.bidding"
                    class="checkbox-input"
                  />
                  <span>Bidding and auction updates</span>
                </label>
              </div>
            </div>

            <div class="form-actions">
              <button @click="saveNotifications" class="btn-primary" :disabled="saving">
                {{ saving ? 'Saving...' : 'Save Preferences' }}
              </button>
            </div>
          </div>
        </div>

        <!-- Privacy Settings -->
        <div v-if="activeSection === 'privacy'" class="settings-card">
          <div class="card-header">
            <h2 class="card-title">Privacy</h2>
          </div>
          
          <div class="card-content">
            <div class="setting-section">
              <h3 class="section-subtitle">Profile Visibility</h3>
              <div class="radio-group">
                <label class="radio-label">
                  <input 
                    type="radio" 
                    v-model="privacySettings.profileVisibility"
                    value="public"
                    name="profileVisibility"
                    class="radio-input"
                  />
                  <span>Public - Anyone can see your profile</span>
                </label>
                
                <label class="radio-label">
                  <input 
                    type="radio" 
                    v-model="privacySettings.profileVisibility"
                    value="private"
                    name="profileVisibility"
                    class="radio-input"
                  />
                  <span>Private - Only you can see your profile</span>
                </label>
              </div>
            </div>

            <div class="setting-section">
              <h3 class="section-subtitle">Data & Analytics</h3>
              <div class="checkbox-group">
                <label class="checkbox-label">
                  <input 
                    type="checkbox" 
                    v-model="privacySettings.analytics"
                    class="checkbox-input"
                  />
                  <span>Allow analytics to improve your experience</span>
                </label>
                
                <label class="checkbox-label">
                  <input 
                    type="checkbox" 
                    v-model="privacySettings.marketing"
                    class="checkbox-input"
                  />
                  <span>Allow marketing communications</span>
                </label>
              </div>
            </div>

            <div class="form-actions">
              <button @click="savePrivacy" class="btn-primary" :disabled="saving">
                {{ saving ? 'Saving...' : 'Save Settings' }}
              </button>
            </div>
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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* {
  font-family: 'Inter', sans-serif;
}

.settings-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 0;
}

/* Header */
.settings-header {
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

/* Settings Tabs */
.settings-tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  padding-bottom: 0;
}

.tab-button {
  padding: 0.75rem 1.25rem;
  background: transparent;
  border: none;
  border-bottom: 2px solid transparent;
  font-size: 0.875rem;
  font-weight: 500;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.15s ease;
  position: relative;
  bottom: -1px;
}

.tab-button:hover {
  color: #111827;
}

.tab-button.active {
  color: #111827;
  border-bottom-color: #111827;
}

/* Settings Content */
.settings-content {
  display: block;
}

/* Settings Card */
.settings-card {
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

.card-content {
  padding: 1.5rem;
}

/* Setting Sections */
.setting-section {
  padding-bottom: 1.5rem;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.setting-section:last-child {
  padding-bottom: 0;
  margin-bottom: 0;
  border-bottom: none;
}

.section-subtitle {
  font-size: 0.875rem;
  font-weight: 600;
  color: #111827;
  margin: 0 0 1rem 0;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* Forms */
.setting-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
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
}

textarea.form-input {
  resize: vertical;
  min-height: 60px;
  line-height: 1.5;
}

/* Setting Option (2FA) */
.setting-option {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: #f9fafb;
  border-radius: 6px;
  gap: 1rem;
}

.option-info {
  flex: 1;
}

.option-text {
  margin: 0 0 0.5rem 0;
  color: #374151;
  font-size: 0.875rem;
  line-height: 1.5;
}

.status-badge {
  display: inline-block;
  padding: 0.25rem 0.625rem;
  border-radius: 4px;
  font-size: 0.625rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.status-badge.enabled {
  background: #d1fae5;
  color: #065f46;
}

.status-badge.disabled {
  background: #fee2e2;
  color: #991b1b;
}

/* Checkbox Group */
.checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
  padding: 0.5rem 0;
  transition: opacity 0.15s ease;
}

.checkbox-label:hover {
  opacity: 0.8;
}

.checkbox-input {
  width: 18px;
  height: 18px;
  cursor: pointer;
  flex-shrink: 0;
}

.checkbox-label span {
  color: #374151;
  font-size: 0.875rem;
  line-height: 1.5;
}

/* Radio Group */
.radio-group {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.radio-label {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  cursor: pointer;
  padding: 0.5rem 0;
  transition: opacity 0.15s ease;
}

.radio-label:hover {
  opacity: 0.8;
}

.radio-input {
  width: 18px;
  height: 18px;
  cursor: pointer;
  flex-shrink: 0;
  margin-top: 2px;
}

.radio-label span {
  color: #374151;
  font-size: 0.875rem;
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

/* Buttons */
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
  .settings-tabs {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }
  
  .tab-button {
    white-space: nowrap;
  }
  
  .card-content {
    padding: 1.25rem;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .setting-option {
    flex-direction: column;
    align-items: flex-start;
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
}
</style>
