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
        <svg class="nav-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
        <span>Account Settings</span>
          </div>
          <div class="nav-item" :class="{ active: activeTab === 'notifications' }" @click="activeTab = 'notifications'">
        <svg class="nav-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/></svg>
        <span>Notifications</span>
          </div>
          <div class="nav-item" :class="{ active: activeTab === 'privacy' }" @click="activeTab = 'privacy'">
        <svg class="nav-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
        <span>Privacy & Security</span>
          </div>
          <div class="nav-item" :class="{ active: activeTab === 'payment' }" @click="activeTab = 'payment'">
        <svg class="nav-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="14" x="2" y="5" rx="2"/><line x1="2" x2="22" y1="10" y2="10"/></svg>
        <span>Payment Settings</span>
          </div>
        </div>

        <!-- Settings Content -->
        <div class="settings-content">
          <!-- Account Settings -->
          <div v-show="activeTab === 'account'" class="settings-section">
        <h2 class="section-title">Account Settings</h2>
        
        <div class="setting-group">
          <h3 class="group-title">Business Address</h3>
          <div class="setting-item">
            <label class="setting-label">Business Address</label>
            <textarea v-model="settings.account.address" class="setting-textarea" rows="3" placeholder="Enter your business address..."></textarea>
            <small class="setting-help">Physical address for your business (optional)</small>
          </div>
        </div>

        <div class="setting-group">
          <h3 class="group-title">Online Presence</h3>
          <div class="setting-item">
            <label class="setting-label">Website URL</label>
            <input v-model="settings.account.website" type="url" class="setting-input" placeholder="https://your-website.com">
            <small class="setting-help">Your business website or online portfolio</small>
          </div>
        </div>

        <div class="setting-group">
          <h3 class="group-title">Social Media Links</h3>
          <div class="setting-item">
            <label class="setting-label">Facebook</label>
            <input v-model="settings.account.socialMedia.facebook" type="url" class="setting-input" placeholder="https://facebook.com/yourpage">
          </div>
          
          <div class="setting-item">
            <label class="setting-label">Instagram</label>
            <input v-model="settings.account.socialMedia.instagram" type="url" class="setting-input" placeholder="https://instagram.com/youraccount">
          </div>
          
          <div class="setting-item">
            <label class="setting-label">Twitter</label>
            <input v-model="settings.account.socialMedia.twitter" type="url" class="setting-input" placeholder="https://twitter.com/youraccount">
          </div>

          <div class="setting-item">
            <label class="setting-label">LinkedIn</label>
            <input v-model="settings.account.socialMedia.linkedin" type="url" class="setting-input" placeholder="https://linkedin.com/in/yourprofile">
          </div>
        </div>

        <div class="setting-group">
          <h3 class="group-title">Account Status</h3>
          <div class="setting-item read-only-item">
            <label class="setting-label">Verification Status</label>
            <div class="status-badge" :class="settings.account.verificationStatus">
          <svg v-if="settings.account.verificationStatus === 'verified'" class="status-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
          <svg v-else-if="settings.account.verificationStatus === 'pending'" class="status-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
          <svg v-else class="status-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="15" x2="9" y1="9" y2="15"/><line x1="9" x2="15" y1="9" y2="15"/></svg>
          <span class="status-text">{{ getVerificationText(settings.account.verificationStatus) }}</span>
            </div>
            <small class="setting-help">Contact support to update your verification status</small>
          </div>
          
          <div class="setting-item read-only-item">
            <label class="setting-label">Seller Rating</label>
            <div class="rating-display">
          <div class="stars">
            <svg v-for="i in 5" :key="i" class="star" :class="{ filled: i <= Math.floor(settings.account.rating) }" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
          </div>
          <span class="rating-value">{{ settings.account.rating.toFixed(1) }}/5.0</span>
            </div>
            <small class="setting-help">Based on buyer reviews and feedback</small>
          </div>
          
          <div class="setting-item read-only-item">
            <label class="setting-label">Total Sales</label>
            <div class="sales-display">
          <span class="sales-number">{{ settings.account.totalSales.toLocaleString() }}</span>
          <span class="sales-text">items sold</span>
            </div>
            <small class="setting-help">Total number of successful sales</small>
          </div>
        </div>

        <div class="setting-actions">
          <ActionButton
            variant="primary"
            icon="save"
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
            icon="save"
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
          icon="lock"
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
          icon="shield"
          text="Enable 2FA"
          @click="setup2FA"
            />
          </div>
        </div>

        <div class="setting-actions">
          <ActionButton
            variant="primary"
            icon="save"
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
          <svg class="coming-soon-icon" xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="14" x="2" y="5" rx="2"/><line x1="2" x2="22" y1="10" y2="10"/></svg>
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
          address: '',
          website: '',
          socialMedia: {
            facebook: '',
            instagram: '',
            twitter: '',
            linkedin: ''
          },
          verificationStatus: 'pending', // pending, verified, rejected
          rating: 0.0,
          totalSales: 0
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
    async saveAccountSettings() {
      this.saveLoading.account = true;
      
      try {
        const token = localStorage.getItem('access_token') || localStorage.getItem('token');
        console.log('Token found:', token ? 'Yes' : 'No', token ? `(${token.substring(0, 20)}...)` : '');
        
        if (!token) {
          this.showToast('Please log in to save settings', 'error', 'Authentication Required');
          this.saveLoading.account = false;
          return;
        }

        // Prepare data for API - only send fields managed by Settings page
        const profileData = {
          address: this.settings.account.address,
          website: this.settings.account.website,
          social_media: this.settings.account.socialMedia
        };

        const response = await fetch('/api/seller/profile', {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify(profileData)
        });

        const data = await response.json();

        if (response.ok) {
          console.log('Settings updated successfully:', data);
          this.showToast('Business settings saved successfully', 'success', 'Settings Saved');
          
          // Update local data with response
          if (data.profile) {
            this.updateLocalProfile(data.profile);
          }
        } else {
          console.error('Failed to save profile:', data);
          this.showToast(data.error || 'Failed to save settings', 'error', 'Save Failed');
        }
      } catch (error) {
        console.error('Error saving account settings:', error);
        this.showToast('Network error. Please try again.', 'error', 'Connection Error');
      }
      
      this.saveLoading.account = false;
    },

    updateLocalProfile(profile) {
      // Update local settings with server response - only fields managed by Settings
      if (profile.address !== undefined) {
        this.settings.account.address = profile.address;
      }
      if (profile.website !== undefined) {
        this.settings.account.website = profile.website;
      }
      if (profile.social_media !== undefined) {
        this.settings.account.socialMedia = profile.social_media || {
          facebook: '',
          instagram: '',
          twitter: '',
          linkedin: ''
        };
      }
      if (profile.verification_status !== undefined) {
        this.settings.account.verificationStatus = profile.verification_status;
      }
      if (profile.rating !== undefined) {
        this.settings.account.rating = profile.rating;
      }
      if (profile.total_sales !== undefined) {
        this.settings.account.totalSales = profile.total_sales;
      }
    },

    async loadProfileData() {
      try {
        const token = localStorage.getItem('access_token') || localStorage.getItem('token');
        console.log('Loading profile - Token found:', token ? 'Yes' : 'No');
        
        if (!token) {
          console.log('No token found for profile loading');
          return;
        }

        const response = await fetch('/api/seller/profile', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        const data = await response.json();

        if (response.ok && data.profile) {
          this.updateLocalProfile(data.profile);
        }
      } catch (error) {
        console.error('Error loading profile data:', error);
      }
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
    },

    getVerificationIcon(status) {
      switch (status) {
        case 'verified':
          return '✅';
        case 'pending':
          return '⏳';
        case 'rejected':
          return '❌';
        default:
          return '❓';
      }
    },

    getVerificationText(status) {
      switch (status) {
        case 'verified':
          return 'Verified Seller';
        case 'pending':
          return 'Verification Pending';
        case 'rejected':
          return 'Verification Rejected';
        default:
          return 'Unknown Status';
      }
    },

    // Debug helper function - can be called from browser console
    debugAuth() {
      console.log('=== Authentication Debug ===');
      console.log('access_token:', localStorage.getItem('access_token'));
      console.log('token:', localStorage.getItem('token'));
      console.log('user_role:', localStorage.getItem('user_role'));
      console.log('user_info:', localStorage.getItem('user_info'));
      
      const token = localStorage.getItem('access_token') || localStorage.getItem('token');
      console.log('Token to use:', token ? token.substring(0, 50) + '...' : 'None');
      
      return {
        hasToken: !!token,
        token: token,
        role: localStorage.getItem('user_role'),
        userInfo: localStorage.getItem('user_info')
      };
    }
  },
  
  mounted() {
    // Debug localStorage contents
    console.log('Settings mounted - localStorage debug:');
    console.log('access_token:', localStorage.getItem('access_token') ? 'Found' : 'Not found');
    console.log('token:', localStorage.getItem('token') ? 'Found' : 'Not found');
    console.log('user_role:', localStorage.getItem('user_role'));
    console.log('user_info:', localStorage.getItem('user_info'));
    
    this.loadProfileData();
  }
}
</script>

<style scoped>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

.seller-settings {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px;
  font-family: 'Inter', sans-serif;
  background: #ffffff;
}

.page-header {
  margin-bottom: 32px;
  padding: 0 0 24px;
  background: transparent;
  border-radius: 0;
  border: none;
  border-bottom: 1px solid #e5e7eb;
  box-shadow: none;
}

.page-title {
  margin: 0 0 4px 0;
  font-family: 'Inter', sans-serif;
  font-size: 28px;
  font-weight: 700;
  color: #000000;
  letter-spacing: -0.5px;
  font-style: normal;
}

.page-subtitle {
  margin: 0;
  color: #6b7280;
  font-size: 14px;
  font-weight: 400;
}

.settings-container {
  display: grid;
  grid-template-columns: 240px 1fr;
  gap: 32px;
  align-items: start;
}

.settings-nav {
  background: #ffffff;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  padding: 12px;
  position: sticky;
  top: 32px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
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
  font-weight: 500;
  color: #374151;
  font-size: 14px;
}

.nav-item:hover {
  background: #f9fafb;
}

.nav-item.active {
  background: #000000;
  color: white;
}

.nav-icon {
  font-size: 18px;
  width: 20px;
  text-align: center;
}

.settings-content {
  background: #ffffff;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  padding: 32px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.settings-section {
  max-width: 650px;
}

.section-title {
  margin: 0 0 32px 0;
  font-family: 'Inter', sans-serif;
  font-size: 20px;
  font-weight: 600;
  color: #000000;
}

.setting-group {
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 1px solid #f3f4f6;
}

.setting-group:last-child {
  margin-bottom: 0;
  padding-bottom: 0;
  border-bottom: none;
}

.group-title {
  margin: 0 0 20px 0;
  font-family: 'Inter', sans-serif;
  font-size: 16px;
  font-weight: 600;
  color: #000000;
}

.setting-item {
  margin-bottom: 20px;
}

.setting-item:last-child {
  margin-bottom: 0;
}

.setting-label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #000000;
  font-size: 14px;
}

.setting-input,
.setting-textarea {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  font-family: 'Inter', sans-serif;
  background: #ffffff;
  color: #000000;
  margin-bottom: 8px;
  transition: all 0.2s ease;
}

.setting-input:focus,
.setting-textarea:focus {
  outline: none;
  border-color: #000000;
  box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.05);
  background: #ffffff;
}

.setting-input::placeholder,
.setting-textarea::placeholder {
  color: #9ca3af;
  opacity: 1;
}

.setting-textarea {
  resize: vertical;
  min-height: 120px;
}

.setting-help {
  display: block;
  font-size: 12px;
  color: #6b7280;
  opacity: 1;
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
  background: #d1d5db;
  border-radius: 28px;
  transition: all 0.2s ease;
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
  transition: all 0.2s ease;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.toggle-switch input:checked + .toggle-slider {
  background: #000000;
}

.toggle-switch input:checked + .toggle-slider:before {
  transform: translateX(28px);
}

.setting-actions {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid #f3f4f6;
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

.coming-soon-card {
  text-align: center;
  padding: 48px 32px;
  background: #ffffff;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.coming-soon-icon {
  font-size: 64px;
  margin-bottom: 24px;
  opacity: 0.5;
}

.coming-soon-card h3 {
  margin: 0 0 16px 0;
  font-family: 'Inter', sans-serif;
  font-size: 20px;
  font-weight: 600;
  color: #000000;
}

.coming-soon-card p {
  margin: 0 0 20px 0;
  color: #6b7280;
  font-size: 14px;
  line-height: 1.6;
  opacity: 1;
}

.feature-list {
  text-align: left;
  max-width: 320px;
  margin: 0 auto;
  color: #374151;
}

.feature-list li {
  margin-bottom: 8px;
  font-size: 14px;
  opacity: 1;
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

/* New styles for seller profile fields */
.read-only-item {
  background: #f9fafb;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 20px;
}

.read-only-item .setting-label {
  color: #374151;
  font-weight: 600;
  margin-bottom: 8px;
}

.status-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 20px;
  font-weight: 600;
  font-size: 14px;
}

.status-badge.verified {
  background: #d1fae5;
  color: #065f46;
  border: 1px solid #a7f3d0;
}

.status-badge.pending {
  background: #fef3c7;
  color: #92400e;
  border: 1px solid #fde68a;
}

.status-badge.rejected {
  background: #fee2e2;
  color: #991b1b;
  border: 1px solid #fecaca;
}

.rating-display {
  display: flex;
  align-items: center;
  gap: 12px;
}

.stars {
  display: flex;
  gap: 2px;
}

.star {
  font-size: 16px;
  opacity: 0.3;
  transition: opacity 0.2s;
}

.star.filled {
  opacity: 1;
}

.rating-value {
  font-weight: 600;
  color: #374151;
  font-size: 16px;
}

.sales-display {
  display: flex;
  align-items: baseline;
  gap: 8px;
}

.sales-number {
  font-size: 24px;
  font-weight: 700;
  color: #000000;
}

.sales-text {
  color: #6b7280;
  font-size: 14px;
}

/* Enhanced styles for social media inputs */
.setting-item input[type="url"] {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  transition: all 0.2s ease;
}

.setting-item input[type="url"]:focus {
  background: #ffffff;
  border-color: #000000;
  box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.05);
}

/* Textarea enhancements */
.setting-textarea {
  min-height: 100px;
  resize: vertical;
  line-height: 1.6;
}

/* Status icons styling */
.status-icon {
  font-size: 16px;
  display: flex;
  align-items: center;
}

.status-text {
  font-weight: 600;
  letter-spacing: 0.025em;
}
</style>
