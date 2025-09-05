<template>
  <SellerLayout>
    <div class="seller-settings">
      <!-- Page Header -->
      <div class="page-header">
        <div class="header-content">
          <h1 class="page-title">Settings</h1>
          <p class="page-subtitle">Manage your account and preferences</p>
        </div>
      </div>

      <div class="settings-container">
        <!-- Settings Navigation -->
        <div class="settings-nav">
          <div class="nav-item" :class="{ active: activeTab === 'account' }" @click="activeTab = 'account'">
            <i class="nav-icon">👤</i>
            <span>Account Settings</span>
          </div>
          <div class="nav-item" :class="{ active: activeTab === 'notifications' }" @click="activeTab = 'notifications'">
            <i class="nav-icon">🔔</i>
            <span>Notifications</span>
          </div>
          <div class="nav-item" :class="{ active: activeTab === 'privacy' }" @click="activeTab = 'privacy'">
            <i class="nav-icon">🔒</i>
            <span>Privacy & Security</span>
          </div>
          <div class="nav-item" :class="{ active: activeTab === 'payment' }" @click="activeTab = 'payment'">
            <i class="nav-icon">💳</i>
            <span>Payment Settings</span>
          </div>
        </div>

        <!-- Settings Content -->
        <div class="settings-content">
          <!-- Account Settings -->
          <div v-show="activeTab === 'account'" class="settings-section">
            <h2 class="section-title">Account Settings</h2>
            
            <div class="setting-group">
              <h3 class="group-title">Profile Information</h3>
              <div class="setting-item">
                <label class="setting-label">Display Name</label>
                <input v-model="settings.account.displayName" type="text" class="setting-input">
                <small class="setting-help">This name will be visible to buyers</small>
              </div>
              
              <div class="setting-item">
                <label class="setting-label">Email Address</label>
                <input v-model="settings.account.email" type="email" class="setting-input">
                <ActionButton
                  variant="secondary"
                  icon="✏️"
                  text="Change Email"
                  @click="changeEmail"
                />
              </div>
              
              <div class="setting-item">
                <label class="setting-label">Phone Number</label>
                <input v-model="settings.account.phone" type="tel" class="setting-input">
              </div>
            </div>

            <div class="setting-group">
              <h3 class="group-title">Shop Settings</h3>
              <div class="setting-item">
                <label class="setting-label">Shop Name</label>
                <input v-model="settings.account.shopName" type="text" class="setting-input">
              </div>
              
              <div class="setting-item">
                <label class="setting-label">Shop Description</label>
                <textarea v-model="settings.account.shopDescription" class="setting-textarea" rows="4"></textarea>
              </div>
            </div>

            <div class="setting-actions">
              <ActionButton
                variant="primary"
                icon="💾"
                text="Save Changes"
                :loading="saveLoading.account"
                @click="saveAccountSettings"
              />
            </div>
          </div>

          <!-- Notifications -->
          <div v-show="activeTab === 'notifications'" class="settings-section">
            <h2 class="section-title">Notification Preferences</h2>
            
            <div class="setting-group">
              <h3 class="group-title">Email Notifications</h3>
              <div class="setting-item toggle-item">
                <div class="toggle-content">
                  <label class="setting-label">New Messages</label>
                  <small class="setting-help">Get notified when buyers send you messages</small>
                </div>
                <label class="toggle-switch">
                  <input type="checkbox" v-model="settings.notifications.newMessages">
                  <span class="toggle-slider"></span>
                </label>
              </div>
              
              <div class="setting-item toggle-item">
                <div class="toggle-content">
                  <label class="setting-label">Item Views</label>
                  <small class="setting-help">Weekly summary of item views and engagement</small>
                </div>
                <label class="toggle-switch">
                  <input type="checkbox" v-model="settings.notifications.itemViews">
                  <span class="toggle-slider"></span>
                </label>
              </div>
              
              <div class="setting-item toggle-item">
                <div class="toggle-content">
                  <label class="setting-label">Price Alerts</label>
                  <small class="setting-help">Notifications about market price changes</small>
                </div>
                <label class="toggle-switch">
                  <input type="checkbox" v-model="settings.notifications.priceAlerts">
                  <span class="toggle-slider"></span>
                </label>
              </div>
            </div>

            <div class="setting-group">
              <h3 class="group-title">Push Notifications</h3>
              <div class="setting-item toggle-item">
                <div class="toggle-content">
                  <label class="setting-label">Instant Messages</label>
                  <small class="setting-help">Immediate push notifications for messages</small>
                </div>
                <label class="toggle-switch">
                  <input type="checkbox" v-model="settings.notifications.pushMessages">
                  <span class="toggle-slider"></span>
                </label>
              </div>
              
              <div class="setting-item toggle-item">
                <div class="toggle-content">
                  <label class="setting-label">Order Updates</label>
                  <small class="setting-help">Notifications about order status changes</small>
                </div>
                <label class="toggle-switch">
                  <input type="checkbox" v-model="settings.notifications.orderUpdates">
                  <span class="toggle-slider"></span>
                </label>
              </div>
            </div>

            <div class="setting-actions">
              <ActionButton
                variant="primary"
                icon="💾"
                text="Save Preferences"
                :loading="saveLoading.notifications"
                @click="saveNotificationSettings"
              />
            </div>
          </div>

          <!-- Privacy & Security -->
          <div v-show="activeTab === 'privacy'" class="settings-section">
            <h2 class="section-title">Privacy & Security</h2>
            
            <div class="setting-group">
              <h3 class="group-title">Privacy Settings</h3>
              <div class="setting-item toggle-item">
                <div class="toggle-content">
                  <label class="setting-label">Public Profile</label>
                  <small class="setting-help">Allow other users to view your profile</small>
                </div>
                <label class="toggle-switch">
                  <input type="checkbox" v-model="settings.privacy.publicProfile">
                  <span class="toggle-slider"></span>
                </label>
              </div>
              
              <div class="setting-item toggle-item">
                <div class="toggle-content">
                  <label class="setting-label">Show Online Status</label>
                  <small class="setting-help">Let buyers see when you're online</small>
                </div>
                <label class="toggle-switch">
                  <input type="checkbox" v-model="settings.privacy.showOnlineStatus">
                  <span class="toggle-slider"></span>
                </label>
              </div>
            </div>

            <div class="setting-group">
              <h3 class="group-title">Security</h3>
              <div class="setting-item">
                <label class="setting-label">Change Password</label>
                <ActionButton
                  variant="secondary"
                  icon="🔒"
                  text="Update Password"
                  @click="changePassword"
                />
              </div>
              
              <div class="setting-item toggle-item">
                <div class="toggle-content">
                  <label class="setting-label">Two-Factor Authentication</label>
                  <small class="setting-help">Add an extra layer of security to your account</small>
                </div>
                <ActionButton
                  variant="info"
                  icon="🔐"
                  text="Enable 2FA"
                  @click="setup2FA"
                />
              </div>
            </div>

            <div class="setting-actions">
              <ActionButton
                variant="primary"
                icon="💾"
                text="Save Privacy Settings"
                :loading="saveLoading.privacy"
                @click="savePrivacySettings"
              />
            </div>
          </div>

          <!-- Payment Settings -->
          <div v-show="activeTab === 'payment'" class="settings-section">
            <h2 class="section-title">Payment Settings</h2>
            
            <div class="coming-soon-card">
              <div class="coming-soon-icon">💳</div>
              <h3>Payment Integration Coming Soon</h3>
              <p>We're working on integrating secure payment processing for your transactions. This will include:</p>
              <ul class="feature-list">
                <li>Multiple payment method support</li>
                <li>Secure transaction processing</li>
                <li>Automatic payout management</li>
                <li>Transaction history and reporting</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Success/Error Messages -->
    <MessageToast
      :show="showMessage"
      :type="messageType"
      :title="messageTitle"
      :message="messageText"
      @close="hideMessage"
    />
  </SellerLayout>
</template>

<script>
import SellerLayout from '@/components/seller/SellerLayout.vue'
import ActionButton from '@/components/seller/shared/ActionButton.vue'
import MessageToast from '@/components/seller/shared/MessageToast.vue'

export default {
  name: 'SellerSettings',
  components: {
    SellerLayout,
    ActionButton,
    MessageToast
  },
  data() {
    return {
      activeTab: 'account',
      settings: {
        account: {
          displayName: 'John Seller',
          email: 'john.seller@example.com',
          phone: '+1 (555) 123-4567',
          shopName: 'John\'s Vintage Store',
          shopDescription: 'Specializing in vintage collectibles and rare items with over 10 years of experience.'
        },
        notifications: {
          newMessages: true,
          itemViews: true,
          priceAlerts: false,
          pushMessages: true,
          orderUpdates: true
        },
        privacy: {
          publicProfile: true,
          showOnlineStatus: true
        }
      },
      saveLoading: {
        account: false,
        notifications: false,
        privacy: false
      },
      showMessage: false,
      messageType: 'info',
      messageTitle: '',
      messageText: ''
    }
  },
  methods: {
    saveAccountSettings() {
      this.saveLoading.account = true;
      
      setTimeout(() => {
        console.log('Saving account settings:', this.settings.account);
        this.showToast('Account settings saved successfully', 'success', 'Settings Saved');
        this.saveLoading.account = false;
      }, 1500);
    },
    
    saveNotificationSettings() {
      this.saveLoading.notifications = true;
      
      setTimeout(() => {
        console.log('Saving notification settings:', this.settings.notifications);
        this.showToast('Notification preferences saved', 'success', 'Preferences Saved');
        this.saveLoading.notifications = false;
      }, 1500);
    },
    
    savePrivacySettings() {
      this.saveLoading.privacy = true;
      
      setTimeout(() => {
        console.log('Saving privacy settings:', this.settings.privacy);
        this.showToast('Privacy settings saved successfully', 'success', 'Settings Saved');
        this.saveLoading.privacy = false;
      }, 1500);
    },
    
    changeEmail() {
      this.showToast('Email change feature coming soon', 'info', 'Coming Soon');
    },
    
    changePassword() {
      this.showToast('Password change feature coming soon', 'info', 'Coming Soon');
    },
    
    setup2FA() {
      this.showToast('Two-factor authentication setup coming soon', 'info', 'Coming Soon');
    },
    
    showToast(message, type = 'info', title = '') {
      this.messageText = message;
      this.messageType = type;
      this.messageTitle = title;
      this.showMessage = true;
    },
    
    hideMessage() {
      this.showMessage = false;
    }
  }
}
</script>

<style scoped>
.seller-settings {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 1px solid #e9ecef;
}

.page-title {
  margin: 0 0 8px 0;
  font-size: 32px;
  font-weight: 700;
  color: #343a40;
}

.page-subtitle {
  margin: 0;
  color: #6c757d;
  font-size: 16px;
}

.settings-container {
  display: grid;
  grid-template-columns: 250px 1fr;
  gap: 32px;
  align-items: start;
}

.settings-nav {
  background: white;
  border-radius: 12px;
  border: 1px solid #e9ecef;
  padding: 8px;
  position: sticky;
  top: 24px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-bottom: 4px;
}

.nav-item:hover {
  background: #f8f9fa;
}

.nav-item.active {
  background: #e3f2fd;
  color: #1976d2;
}

.nav-icon {
  font-size: 18px;
  width: 20px;
  text-align: center;
}

.settings-content {
  background: white;
  border-radius: 12px;
  border: 1px solid #e9ecef;
  padding: 32px;
}

.settings-section {
  max-width: 600px;
}

.section-title {
  margin: 0 0 32px 0;
  font-size: 24px;
  font-weight: 600;
  color: #343a40;
}

.setting-group {
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 1px solid #f1f3f4;
}

.setting-group:last-child {
  margin-bottom: 0;
  padding-bottom: 0;
  border-bottom: none;
}

.group-title {
  margin: 0 0 20px 0;
  font-size: 18px;
  font-weight: 600;
  color: #343a40;
}

.setting-item {
  margin-bottom: 20px;
}

.setting-item:last-child {
  margin-bottom: 0;
}

.setting-label {
  display: block;
  margin-bottom: 6px;
  font-weight: 500;
  color: #495057;
  font-size: 14px;
}

.setting-input,
.setting-textarea {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  font-size: 14px;
  margin-bottom: 8px;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.setting-input:focus,
.setting-textarea:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
}

.setting-textarea {
  resize: vertical;
  font-family: inherit;
}

.setting-help {
  display: block;
  font-size: 12px;
  color: #6c757d;
  margin-top: 4px;
}

.toggle-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 0;
}

.toggle-content {
  flex: 1;
}

.toggle-switch {
  position: relative;
  display: inline-block;
  width: 48px;
  height: 24px;
  margin-left: 16px;
}

.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  border-radius: 24px;
  transition: 0.3s;
}

.toggle-slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  border-radius: 50%;
  transition: 0.3s;
}

.toggle-switch input:checked + .toggle-slider {
  background-color: #007bff;
}

.toggle-switch input:checked + .toggle-slider:before {
  transform: translateX(24px);
}

.setting-actions {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid #e9ecef;
}

.coming-soon-card {
  text-align: center;
  padding: 48px 32px;
  background: #f8f9fa;
  border-radius: 12px;
  border: 1px solid #e9ecef;
}

.coming-soon-icon {
  font-size: 64px;
  margin-bottom: 24px;
}

.coming-soon-card h3 {
  margin: 0 0 16px 0;
  font-size: 24px;
  font-weight: 600;
  color: #343a40;
}

.coming-soon-card p {
  margin: 0 0 20px 0;
  color: #6c757d;
  font-size: 16px;
  line-height: 1.6;
}

.feature-list {
  text-align: left;
  max-width: 300px;
  margin: 0 auto;
  color: #495057;
}

.feature-list li {
  margin-bottom: 8px;
  font-size: 14px;
}

/* Responsive */
@media (max-width: 768px) {
  .settings-container {
    grid-template-columns: 1fr;
    gap: 24px;
  }
  
  .settings-nav {
    position: static;
    display: flex;
    overflow-x: auto;
    padding: 8px;
  }
  
  .nav-item {
    white-space: nowrap;
    margin-right: 8px;
    margin-bottom: 0;
  }
  
  .toggle-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .toggle-switch {
    margin-left: 0;
  }
  
  .coming-soon-card {
    padding: 32px 24px;
  }
}
</style>
