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
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400;1,600;1,700;1,800&family=Inter:wght@300;400;500;600;700&family=Crimson+Text:wght@400;600;700&family=Libre+Baskerville:wght@400;700&display=swap');

.seller-settings {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px;
  font-family: 'Inter', sans-serif;
  background: #ffffff;
}

.page-header {
  margin-bottom: 48px;
  padding: 32px;
  background: #ffffff;
  border-radius: 24px;
  border: 1px solid #e5e7eb;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.page-title {
  margin: 0 0 8px 0;
  font-family: 'Playfair Display', serif;
  font-size: 42px;
  font-weight: 800;
  color: #1f2937;
  letter-spacing: -1px;
  font-style: italic;
}

.page-subtitle {
  margin: 0;
  color: #8b5a3c;
  font-size: 16px;
  opacity: 0.8;
}

.settings-container {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 48px;
  align-items: start;
}

.settings-nav {
  background: #ffffff;
  border-radius: 24px;
  border: 1px solid #e5e7eb;
  padding: 16px;
  position: sticky;
  top: 32px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 20px;
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-bottom: 8px;
  font-weight: 500;
  color: #8b5a3c;
}

.nav-item:hover {
  background: rgba(139, 90, 60, 0.1);
  transform: translateX(4px);
}

.nav-item.active {
  background: linear-gradient(135deg, #8b5a3c 0%, #a06749 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(139, 90, 60, 0.3);
}

.nav-icon {
  font-size: 20px;
  width: 24px;
  text-align: center;
}

.settings-content {
  background: linear-gradient(135deg, #f8f6f1 0%, #e8ddd4 100%);
  border-radius: 24px;
  border: 1px solid #d4af94;
  padding: 48px;
  box-shadow: 0 8px 25px rgba(139, 90, 60, 0.1);
}

.settings-section {
  max-width: 650px;
}

.section-title {
  margin: 0 0 40px 0;
  font-family: 'Playfair Display', serif;
  font-size: 28px;
  font-weight: 600;
  color: #8b5a3c;
}

.setting-group {
  margin-bottom: 40px;
  padding-bottom: 32px;
  border-bottom: 1px solid #d4af94;
}

.setting-group:last-child {
  margin-bottom: 0;
  padding-bottom: 0;
  border-bottom: none;
}

.group-title {
  margin: 0 0 24px 0;
  font-family: 'Playfair Display', serif;
  font-size: 20px;
  font-weight: 600;
  color: #8b5a3c;
}

.setting-item {
  margin-bottom: 24px;
}

.setting-item:last-child {
  margin-bottom: 0;
}

.setting-label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #8b5a3c;
  font-size: 14px;
}

.setting-input,
.setting-textarea {
  width: 100%;
  padding: 16px;
  border: 1px solid #d4af94;
  border-radius: 12px;
  font-size: 14px;
  font-family: 'Inter', sans-serif;
  background: rgba(248, 246, 241, 0.7);
  color: #8b5a3c;
  margin-bottom: 8px;
  transition: all 0.3s ease;
}

.setting-input:focus,
.setting-textarea:focus {
  outline: none;
  border-color: #8b5a3c;
  box-shadow: 0 0 0 3px rgba(139, 90, 60, 0.1);
  background: rgba(248, 246, 241, 1);
}

.setting-input::placeholder,
.setting-textarea::placeholder {
  color: #8b5a3c;
  opacity: 0.6;
}

.setting-textarea {
  resize: vertical;
  min-height: 120px;
}

.setting-help {
  display: block;
  font-size: 12px;
  color: #8b5a3c;
  opacity: 0.7;
  margin-top: 4px;
}

.toggle-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 0;
}

.toggle-content {
  flex: 1;
}

.toggle-switch {
  position: relative;
  display: inline-block;
  width: 56px;
  height: 28px;
  margin-left: 20px;
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
  background: linear-gradient(135deg, #d4af94 0%, #c19a7a 100%);
  border-radius: 28px;
  transition: all 0.3s ease;
  box-shadow: inset 0 2px 4px rgba(139, 90, 60, 0.2);
}

.toggle-slider:before {
  position: absolute;
  content: "";
  height: 22px;
  width: 22px;
  left: 3px;
  bottom: 3px;
  background: white;
  border-radius: 50%;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(139, 90, 60, 0.3);
}

.toggle-switch input:checked + .toggle-slider {
  background: linear-gradient(135deg, #8b5a3c 0%, #a06749 100%);
}

.toggle-switch input:checked + .toggle-slider:before {
  transform: translateX(28px);
}

.setting-actions {
  margin-top: 40px;
  padding-top: 32px;
  border-top: 1px solid #d4af94;
}

.coming-soon-card {
  text-align: center;
  padding: 64px 48px;
  background: linear-gradient(135deg, #f8f6f1 0%, #e8ddd4 100%);
  border-radius: 24px;
  border: 1px solid #d4af94;
  box-shadow: 0 8px 25px rgba(139, 90, 60, 0.1);
}

.coming-soon-icon {
  font-size: 72px;
  margin-bottom: 32px;
  opacity: 0.7;
}

.coming-soon-card h3 {
  margin: 0 0 20px 0;
  font-family: 'Playfair Display', serif;
  font-size: 28px;
  font-weight: 600;
  color: #8b5a3c;
}

.coming-soon-card p {
  margin: 0 0 24px 0;
  color: #8b5a3c;
  font-size: 16px;
  line-height: 1.6;
  opacity: 0.8;
}

.feature-list {
  text-align: left;
  max-width: 320px;
  margin: 0 auto;
  color: #8b5a3c;
}

.feature-list li {
  margin-bottom: 8px;
  font-size: 14px;
  opacity: 0.9;
}

/* Responsive */
@media (max-width: 768px) {
  .seller-settings {
    padding: 24px;
  }
  
  .page-header {
    padding: 24px;
  }
  
  .settings-container {
    grid-template-columns: 1fr;
    gap: 32px;
  }
  
  .settings-nav {
    position: static;
    display: flex;
    overflow-x: auto;
    padding: 12px;
    border-radius: 16px;
  }
  
  .nav-item {
    white-space: nowrap;
    margin-right: 12px;
    margin-bottom: 0;
    padding: 12px 16px;
  }
  
  .nav-item:hover {
    transform: translateX(0);
  }
  
  .settings-content {
    padding: 32px 24px;
  }
  
  .toggle-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
  
  .toggle-switch {
    margin-left: 0;
  }
  
  .coming-soon-card {
    padding: 48px 32px;
  }
  
  .page-title {
    font-size: 28px;
  }
  
  .section-title {
    font-size: 24px;
  }
  
  .group-title {
    font-size: 18px;
  }
}
</style>
