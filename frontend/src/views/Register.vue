<template>
  <div class="register-page">
    <div class="register-container">
      <div class="register-card">
        <!-- Left Side - Branding -->
        <div class="branding-section">
          <div class="brand-content">
          
            <p class="brand-tagline">Join thousands of collectors and start trading rare treasures today</p>
            <div class="brand-features">
              <div class="feature-item">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M12 2L2 7l10 5 10-5-10-5z"></path>
                  <path d="M2 17l10 5 10-5"></path>
                  <path d="M2 12l10 5 10-5"></path>
                </svg>
                <span>List Your Items Easily</span>
              </div>
              <div class="feature-item">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"></circle>
                  <polyline points="12 6 12 12 16 14"></polyline>
                </svg>
                <span>Quick Account Setup</span>
              </div>
              <div class="feature-item">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
                </svg>
                <span>Build Your Collection</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Side - Register Form -->
        <div class="form-section">
          <div class="form-header">
         <h2 class="logo-text" style="font-size: 32px;">RareVault.</h2>
         <br>
            <p class="form-subtitle">Start your collecting journey</p>
          </div>

          <form @submit.prevent="handleRegister" class="register-form">
            <!-- Error Message -->
            <div v-if="errorMessage" class="error-message">
              {{ errorMessage }}
            </div>

            <!-- Success Message -->
            <div v-if="successMessage" class="success-message">
              {{ successMessage }}
            </div>

            <!-- Name Group -->
            <div class="name-group">
              <div class="form-group">
                <label for="firstName" class="form-label">First Name</label>
                <input
                  id="firstName"
                  v-model="formData.first_name"
                  type="text"
                  class="form-input"
                  placeholder="John"
                  required
                />
              </div>
              
              <div class="form-group">
                <label for="lastName" class="form-label">Last Name</label>
                <input
                  id="lastName"
                  v-model="formData.last_name"
                  type="text"
                  class="form-input"
                  placeholder="Doe"
                  required
                />
              </div>
            </div>

            <!-- Email -->
            <div class="form-group">
              <label for="email" class="form-label">Email Address</label>
              <input
                id="email"
                v-model="formData.email"
                type="email"
                class="form-input"
                placeholder="you@example.com"
                required
              />
            </div>

            <!-- Password -->
            <div class="form-group">
              <label for="password" class="form-label">Password</label>
              <input
                id="password"
                v-model="formData.password"
                type="password"
                class="form-input"
                placeholder="Min. 6 characters"
                required
                minlength="6"
              />
            </div>

            <!-- Confirm Password -->
            <div class="form-group">
              <label for="confirmPassword" class="form-label">Confirm Password</label>
              <input
                id="confirmPassword"
                v-model="formData.confirmPassword"
                type="password"
                class="form-input"
                placeholder="Re-enter password"
                required
              />
            </div>

            <!-- Terms Checkbox -->
            <div class="form-options">
              <label class="checkbox-wrapper">
                <input 
                  v-model="formData.agreeToTerms" 
                  type="checkbox" 
                  class="checkbox"
                  required
                />
                <span class="checkbox-label">
                  I agree to the Terms & Privacy Policy
                </span>
              </label>
            </div>

            <!-- Submit Button -->
            <button 
              type="submit" 
              class="submit-btn"
              :disabled="isLoading || !isFormValid"
            >
              <span v-if="isLoading" class="spinner"></span>
              <span v-else>Create Account</span>
            </button>

            <!-- Login Link -->
            <div class="login-link">
              Already have an account?
              <router-link to="/login" class="link">Sign in</router-link>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Register',
  data() {
    return {
      formData: {
        first_name: '',
        last_name: '',
        email: '',
        password: '',
        confirmPassword: '',
        role: 'user', // Default to 'user' role for security
        agreeToTerms: false
      },
      isLoading: false,
      errorMessage: '',
      successMessage: ''
    }
  },
  computed: {
    isFormValid() {
      return (
        this.formData.first_name &&
        this.formData.last_name &&
        this.formData.email &&
        this.formData.password &&
        this.formData.confirmPassword &&
        this.formData.agreeToTerms &&
        this.formData.password === this.formData.confirmPassword &&
        this.formData.password.length >= 6
      )
    }
  },
  mounted() {
    // Always default to 'user' role for security
    this.formData.role = 'user'
  },
  methods: {
    async handleRegister() {
      this.isLoading = true
      this.errorMessage = ''
      this.successMessage = ''

      // Validate passwords match
      if (this.formData.password !== this.formData.confirmPassword) {
        this.errorMessage = 'Passwords do not match'
        this.isLoading = false
        return
      }

      try {
        const response = await axios.post('/api/auth/register', {
          first_name: this.formData.first_name,
          last_name: this.formData.last_name,
          email: this.formData.email,
          password: this.formData.password,
          role: this.formData.role
        })

        this.successMessage = 'Account created successfully! Redirecting...'

        // Store token and user info
        localStorage.setItem('access_token', response.data.access_token)
        localStorage.setItem('user_role', response.data.user.role)
        localStorage.setItem('user_info', JSON.stringify(response.data.user))

        // Redirect after a short delay
        setTimeout(() => {
          if (response.data.user.role === 'admin') {
            this.$router.push('/admin/dashboard')
          } else {
            this.$router.push('/user/dashboard')
          }
        }, 1500)

      } catch (error) {
        this.errorMessage = error.response?.data?.error || 'Registration failed. Please try again.'
      } finally {
        this.isLoading = false
      }
    }
  }
}
</script>

<style scoped>

 .logo {
  text-decoration: none;
  color: #1f2937;
}

.logo-text {
  font-family: 'Playfair Display', serif;
  font-style: normal;
  font-weight: 400;
  font-size: 32px;
  letter-spacing: 0;
  color: #000000;
  margin: 0;
  transition: color 0.2s ease;
}

.register-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #e8ecef 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.5rem;
}

.register-container {
  width: 100%;
  max-width: 1000px;
  max-height: 90vh;
}

.register-card {
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.12);
  overflow: hidden;
  display: grid;
  grid-template-columns: 1fr 1fr;
  max-height: 90vh;
}

/* Branding Section */
.branding-section {
  background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
  padding: 2.5rem 2.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.branding-section::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
  pointer-events: none;
}

.brand-content {
  position: relative;
  z-index: 1;
}

.brand-logo {
  font-family: 'Playfair Display', serif;
  font-size: 2.25rem;
  font-weight: 700;
  color: white;
  margin: 0 0 0.75rem 0;
  letter-spacing: -0.5px;
}

.brand-tagline {
  color: rgba(255, 255, 255, 0.85);
  font-size: 0.95rem;
  line-height: 1.5;
  margin: 0 0 2rem 0;
  max-width: 90%;
}

.brand-features {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.875rem;
}

.feature-item svg {
  flex-shrink: 0;
  opacity: 0.9;
  width: 18px;
  height: 18px;
}

/* Form Section */
.form-section {
  padding: 2.5rem 2.5rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  overflow-y: auto;
}

.form-header {
  margin-bottom: 1.25rem;
}

.form-title {
  font-size: 1.625rem;
  font-weight: 700;
  color: #000000;
  margin: 0 0 0.375rem 0;
  letter-spacing: -0.5px;
}

.form-subtitle {
  color: #6b7280;
  font-size: 0.875rem;
  margin: 0;
}

.register-form {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.name-group {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
  margin-bottom: 0;
}

.name-group .form-group {
  margin-bottom: 0.875rem;
}

.form-group {
  margin-bottom: 0.875rem;
}

.form-label {
  display: block;
  font-size: 0.813rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.375rem;
  letter-spacing: 0.3px;
}

.form-input {
  width: 100%;
  padding: 0.75rem 0.875rem;
  border: 1.5px solid #e5e7eb;
  border-radius: 8px;
  font-size: 0.875rem;
  transition: all 0.3s ease;
  background: #f9fafb;
  color: #000000;
  font-family: inherit;
}

.form-input::placeholder {
  color: #9ca3af;
}

.form-input:focus {
  outline: none;
  border-color: #000000;
  background: white;
  box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.05);
}

.form-options {
  margin-bottom: 1.125rem;
}

.checkbox-wrapper {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.checkbox {
  width: 16px;
  height: 16px;
  cursor: pointer;
  accent-color: #000000;
}

.checkbox-label {
  color: #374151;
  font-size: 0.813rem;
  font-weight: 500;
}

.submit-btn {
  width: 100%;
  padding: 0.813rem 1.25rem;
  background: #000000;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 0.938rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-bottom: 1.125rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.submit-btn:hover:not(:disabled) {
  background: #1a1a1a;
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
}

.submit-btn:active:not(:disabled) {
  transform: translateY(0);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.error-message {
  padding: 0.75rem 0.875rem;
  background: #fef2f2;
  color: #dc2626;
  border: 1px solid #fecaca;
  border-radius: 8px;
  font-size: 0.813rem;
  text-align: center;
  margin-bottom: 1rem;
  font-weight: 500;
}

.success-message {
  padding: 0.75rem 0.875rem;
  background: #f0fdf4;
  color: #166534;
  border: 1px solid #bbf7d0;
  border-radius: 8px;
  font-size: 0.813rem;
  text-align: center;
  margin-bottom: 1rem;
  font-weight: 500;
}

.login-link {
  text-align: center;
  font-size: 0.813rem;
  color: #6b7280;
  font-weight: 500;
}

.link {
  color: #000000;
  text-decoration: none;
  font-weight: 700;
  margin-left: 0.25rem;
  transition: color 0.2s ease;
}

.link:hover {
  color: #4b5563;
}

.spinner {
  width: 1rem;
  height: 1rem;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@media (max-width: 1024px) {
  .register-card {
    grid-template-columns: 1fr;
    max-width: 550px;
    margin: 0 auto;
  }

  .branding-section {
    padding: 3rem 2rem;
    min-height: auto;
  }

  .brand-logo {
    font-size: 2.5rem;
  }

  .brand-tagline {
    font-size: 1rem;
    margin-bottom: 2rem;
  }

  .form-section {
    padding: 3rem 2.5rem;
  }
}

@media (max-width: 768px) {
  .register-page {
    padding: 1.5rem 1rem;
  }

  .branding-section {
    padding: 2.5rem 2rem;
  }

  .brand-logo {
    font-size: 2rem;
  }

  .form-section {
    padding: 2.5rem 2rem;
  }

  .form-title {
    font-size: 1.75rem;
  }
  
  .name-group {
    grid-template-columns: 1fr;
    gap: 0;
  }
}

@media (max-width: 480px) {
  .branding-section {
    padding: 2rem 1.5rem;
  }

  .form-section {
    padding: 2rem 1.5rem;
  }

  .form-title {
    font-size: 1.5rem;
  }
}
</style>
