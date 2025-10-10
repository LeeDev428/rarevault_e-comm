<template>
  <SellerLayout>
    <div class="seller-profile">
      <!-- Page Header -->
      <div class="page-header">
        <div class="header-content">
          <h1 class="page-title">My Profile</h1>
          <p class="page-subtitle">Manage and protect your account</p>
        </div>
      </div>

      <div class="profile-container">
        <!-- Profile Form -->
        <div class="profile-form">
          <div class="form-section">
            <h2 class="section-title">Profile Information</h2>
            
            <div class="form-group">
              <label class="form-label">Username</label>
              <input 
                v-model="profile.username"
                type="text" 
                class="form-input"
                placeholder="Username can only be changed once"
              >
              <small class="form-help">Username can only be changed once</small>
            </div>

            <div class="form-group">
              <label class="form-label">Name</label>
              <input 
                v-model="profile.name"
                type="text" 
                class="form-input"
                placeholder="Enter your full name"
              >
            </div>

            <div class="form-group">
              <label class="form-label">Email</label>
              <div class="email-input-group">
                <input 
                  v-model="profile.email"
                  type="email" 
                  class="form-input"
                  placeholder="Enter your email"
                >
                <button class="change-btn">Change</button>
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">Phone Number</label>
              <div class="phone-input-group">
                <input 
                  v-model="profile.phone"
                  type="tel" 
                  class="form-input"
                  placeholder="Enter your phone number"
                >
                <button class="add-btn">Add</button>
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">Gender</label>
              <div class="radio-group">
                <label class="radio-option">
                  <input type="radio" v-model="profile.gender" value="male">
                  <span class="radio-label">Male</span>
                </label>
                <label class="radio-option">
                  <input type="radio" v-model="profile.gender" value="female">
                  <span class="radio-label">Female</span>
                </label>
                <label class="radio-option">
                  <input type="radio" v-model="profile.gender" value="other">
                  <span class="radio-label">Other</span>
                </label>
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">Date of Birth</label>
              <div class="date-group">
                <select v-model="profile.birthDate" class="date-select">
                  <option value="">Date</option>
                  <option v-for="day in 31" :key="day" :value="day">{{ day }}</option>
                </select>
                <select v-model="profile.birthMonth" class="date-select">
                  <option value="">Month</option>
                  <option v-for="(month, index) in months" :key="index" :value="index + 1">{{ month }}</option>
                </select>
                <select v-model="profile.birthYear" class="date-select">
                  <option value="">Year</option>
                  <option v-for="year in years" :key="year" :value="year">{{ year }}</option>
                </select>
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">Shop Name</label>
              <input 
                v-model="profile.shopName"
                type="text" 
                class="form-input"
                placeholder="Enter your shop name"
              >
            </div>

            <div class="form-group">
              <label class="form-label">Shop Description</label>
              <textarea 
                v-model="profile.shopDescription"
                class="form-textarea"
                rows="4"
                placeholder="Describe your shop and what you sell..."
              ></textarea>
            </div>

            <div class="form-actions">
              <ActionButton
                variant="primary"
                icon="💾"
                text="Save"
                :loading="saveLoading"
                @click="saveProfile"
              />
            </div>
          </div>
        </div>

        <!-- Profile Photo and Meetup Preferences -->
        <div class="profile-sidebar">
          <!-- Profile Photo -->
          <div class="photo-section">
            <div class="photo-container">
              <div class="profile-photo">
                <div v-if="!profile.photo" class="photo-placeholder">
                    <svg class="photo-icon" xmlns="http://www.w3.org/2000/svg" width="52" height="52" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/>
                    <circle cx="12" cy="7" r="4"/>
                    </svg>
                </div>
                <img v-else :src="profile.photo" alt="Profile Photo" class="photo-image">
              </div>
              <button class="select-image-btn" @click="selectImage">
                Select Image
              </button>
            </div>
            <div class="photo-info">
              <p class="info-text">File size: maximum 1 MB</p>
              <p class="info-text">File extension: .JPEG, .PNG</p>
            </div>
          </div>

          <!-- Meetup Preferences -->
          <div class="meetup-section">
            <h3 class="meetup-title">Meetup preferences</h3>
            <p class="meetup-subtitle">Mark your way how you deal with clients on rare items</p>

            <div class="meetup-options">
              <label class="meetup-option">
                <input 
                  type="checkbox" 
                  v-model="meetupPreferences.publicMeetup"
                  class="meetup-checkbox"
                >
                <div class="option-content">
                  <svg class="option-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M6 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18Z"/>
                  <path d="M6 12H4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h2"/>
                  <path d="M18 9h2a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-2"/>
                  <path d="M10 6h4"/>
                  <path d="M10 10h4"/>
                  <path d="M10 14h4"/>
                  <path d="M10 18h4"/>
                  </svg>
                  <span class="option-text">Public meetup</span>
                </div>
                </label>

                <label class="meetup-option">
                <input 
                  type="checkbox" 
                  v-model="meetupPreferences.doorPickup"
                  class="meetup-checkbox"
                >
                <div class="option-content">
                  <svg class="option-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M13 4h3a2 2 0 0 1 2 2v14"/>
                  <path d="M2 20h3"/>
                  <path d="M13 20h9"/>
                  <path d="M10 12v.01"/>
                  <path d="M13 4.562v16.157a1 1 0 0 1-1.242.97L5 20V5.562a2 2 0 0 1 1.515-1.94l4-1A2 2 0 0 1 13 4.561Z"/>
                  </svg>
                  <span class="option-text">Door pickup</span>
                </div>
                </label>

                <label class="meetup-option">
                <input 
                  type="checkbox" 
                  v-model="meetupPreferences.doorDelivery"
                  class="meetup-checkbox"
                >
                <div class="option-content">
                  <svg class="option-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2"/>
                  <path d="M15 18H9"/>
                  <path d="M19 18h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.624l-3.48-4.35A1 1 0 0 0 17.52 8H14"/>
                  <circle cx="17" cy="18" r="2"/>
                  <circle cx="7" cy="18" r="2"/>
                  </svg>
                  <span class="option-text">Door delivery</span>
                </div>
              </label>
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
  name: 'SellerProfile',
  components: {
    SellerLayout,
    ActionButton,
    MessageToast
  },
  data() {
    return {
      profile: {
        username: 'johnseller',
        name: 'John Seller',
        email: 'j***********@gmail.com',
        phone: '',
        gender: 'male',
        birthDate: '',
        birthMonth: '',
        birthYear: '',
        shopName: 'John\'s Vintage Store',
        shopDescription: 'Specializing in vintage collectibles and rare items with over 10 years of experience.',
        photo: null
      },
      meetupPreferences: {
        publicMeetup: true,
        doorPickup: false,
        doorDelivery: true
      },
      months: [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
      ],
      saveLoading: false,
      showMessage: false,
      messageType: 'info',
      messageTitle: '',
      messageText: ''
    }
  },
  computed: {
    years() {
      const currentYear = new Date().getFullYear();
      const years = [];
      for (let year = currentYear; year >= currentYear - 100; year--) {
        years.push(year);
      }
      return years;
    }
  },
  methods: {
    selectImage() {
      // Create file input
      const input = document.createElement('input');
      input.type = 'file';
      input.accept = '.jpeg,.jpg,.png';
      input.onchange = (event) => {
        const file = event.target.files[0];
        if (file) {
          // Check file size (1MB = 1024 * 1024 bytes)
          if (file.size > 1024 * 1024) {
            this.showToast('File size must be less than 1 MB', 'error', 'File Too Large');
            return;
          }
          
          // Check file type
          const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png'];
          if (!allowedTypes.includes(file.type)) {
            this.showToast('Only JPEG and PNG files are allowed', 'error', 'Invalid File Type');
            return;
          }
          
          // Create preview
          const reader = new FileReader();
          reader.onload = (e) => {
            this.profile.photo = e.target.result;
            this.showToast('Profile photo selected successfully', 'success', 'Photo Selected');
          };
          reader.readAsDataURL(file);
        }
      };
      input.click();
    },
    
    saveProfile() {
      this.saveLoading = true;
      
      // Simulate API call
      setTimeout(() => {
        // Validate required fields
        if (!this.profile.name || !this.profile.shopName) {
          this.showToast('Please fill in all required fields', 'error', 'Validation Error');
          this.saveLoading = false;
          return;
        }
        
        // Save profile data (in real app, this would be an API call)
        console.log('Saving profile:', this.profile);
        console.log('Saving meetup preferences:', this.meetupPreferences);
        
        this.showToast('Your profile has been updated successfully', 'success', 'Profile Saved');
        this.saveLoading = false;
      }, 2000);
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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

.seller-profile {
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

.profile-container {
  display: grid;
  grid-template-columns: 1fr 350px;
  gap: 32px;
  align-items: start;
}

.profile-form {
  background: #ffffff;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  padding: 32px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.section-title {
  margin: 0 0 24px 0;
  font-family: 'Inter', sans-serif;
  font-size: 18px;
  font-weight: 600;
  color: #000000;
}

.form-group {
  margin-bottom: 20px;
}

.form-label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #000000;
  font-size: 14px;
}

.form-input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  background: #ffffff;
  color: #111827;
  transition: all 0.2s ease;
  font-family: 'Inter', sans-serif;
}

.form-input:focus {
  outline: none;
  border-color: #000000;
  box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.05);
  background: #ffffff;
}

.form-input::placeholder {
  color: #9ca3af;
}

.form-textarea {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  font-family: 'Inter', sans-serif;
  resize: vertical;
  min-height: 120px;
  background: #ffffff;
  color: #111827;
  transition: all 0.2s ease;
}

.form-textarea:focus {
  outline: none;
  border-color: #000000;
  box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.05);
  background: #ffffff;
}

.form-textarea::placeholder {
  color: #9ca3af;
}

.form-help {
  display: block;
  margin-top: 6px;
  font-size: 12px;
  color: #6b7280;
}

.email-input-group,
.phone-input-group {
  display: flex;
  gap: 12px;
}

.email-input-group .form-input,
.phone-input-group .form-input {
  flex: 1;
}

.change-btn,
.add-btn {
  padding: 10px 20px;
  border: none;
  background: #000000;
  color: white;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: 'Inter', sans-serif;
}

.change-btn:hover,
.add-btn:hover {
  background: #111827;
}

.radio-group {
  display: flex;
  gap: 24px;
}

.radio-option {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 8px;
  transition: background 0.3s ease;
}

.radio-option:hover {
  background: #f9fafb;
}

.radio-option input[type="radio"] {
  margin: 0;
  accent-color: #000000;
}

.radio-label {
  font-size: 14px;
  color: #111827;
  font-weight: 500;
}

.date-group {
  display: flex;
  gap: 12px;
}

.date-select {
  flex: 1;
  padding: 12px 16px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  background: #ffffff;
  color: #111827;
  transition: all 0.2s ease;
  font-family: 'Inter', sans-serif;
}

.date-select:focus {
  outline: none;
  border-color: #000000;
  box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.05);
  background: #ffffff;
}

.form-actions {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid #f3f4f6;
}

/* Profile Sidebar */
.profile-sidebar {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.photo-section {
  background: #ffffff;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.photo-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  margin-bottom: 20px;
}

.profile-photo {
  width: 140px;
  height: 140px;
  border-radius: 50%;
  overflow: hidden;
  border: 4px solid #e5e7eb;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.photo-placeholder {
  width: 100%;
  height: 100%;
  background: #f3f4f6;
  display: flex;
  align-items: center;
  justify-content: center;
}

.photo-icon {
  font-size: 52px;
  color: #9ca3af;
  opacity: 1;
}

.photo-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.select-image-btn {
  padding: 10px 20px;
  border: 1px solid #e5e7eb;
  background: #f9fafb;
  color: #000000;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: 'Inter', sans-serif;
}

.select-image-btn:hover {
  background: #ffffff;
  border-color: #000000;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.photo-info {
  text-align: center;
}

.info-text {
  margin: 4px 0;
  font-size: 12px;
  color: #6b7280;
  opacity: 1;
}

.meetup-section {
  background: #ffffff;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.meetup-title {
  margin: 0 0 8px 0;
  font-family: 'Inter', sans-serif;
  font-size: 18px;
  font-weight: 600;
  color: #111827;
}

.meetup-subtitle {
  margin: 0 0 20px 0;
  font-size: 14px;
  color: #6b7280;
  opacity: 1;
  line-height: 1.5;
}

.meetup-options {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.meetup-option {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  padding: 12px;
  border-radius: 8px;
  transition: all 0.2s ease;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
}

.meetup-option:hover {
  background: #ffffff;
  border-color: #d1d5db;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.meetup-checkbox {
  margin: 0;
  accent-color: #000000;
}

.option-content {
  display: flex;
  align-items: center;
  gap: 12px;
}

.option-icon {
  font-size: 18px;
  color: #374151;
}

.option-text {
  font-size: 14px;
  color: #111827;
  font-weight: 500;
}

/* Responsive */
@media (max-width: 768px) {
  .seller-profile {
    padding: 24px;
  }
  
  .profile-container {
    grid-template-columns: 1fr;
    gap: 32px;
  }
  
  .page-header,
  .profile-form,
  .photo-section,
  .meetup-section {
    padding: 24px;
  }
  
  .radio-group {
    flex-direction: column;
    gap: 12px;
  }
  
  .date-group {
    flex-direction: column;
  }
  
  .email-input-group,
  .phone-input-group {
    flex-direction: column;
  }
  
  .page-title {
    font-size: 28px;
  }
  
  .section-title {
    font-size: 20px;
  }
}
</style>
