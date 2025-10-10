<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-card">
        <!-- Left Side - Branding -->
        <div class="branding-section">
          <div class="brand-content">
           
            <p class="brand-tagline">Discover rare treasures and connect with collectors worldwide</p>
            <div class="brand-features">
              <div class="feature-item">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                  <polyline points="22 4 12 14.01 9 11.01"></polyline>
                </svg>
                <span>Verified Sellers</span>
              </div>
              <div class="feature-item">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                  <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                </svg>
                <span>Secure Transactions</span>
              </div>
              <div class="feature-item">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                  <circle cx="9" cy="7" r="4"></circle>
                  <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                  <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                </svg>
                <span>Collector Community</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Side - Login Form -->
        <div class="form-section">
          <div class="form-header">
            <h2 class="logo-text" style="font-size: 32px;">RareVault.</h2>
            <br>
            <p class="form-subtitle">Sign in to your account</p>
          </div>

          <form @submit.prevent="handleLogin" class="login-form">
            <!-- Error Message -->
            <div v-if="errorMessage" class="error-message">
              {{ errorMessage }}
            </div>

            <div class="form-group">
              <label class="form-label">Email Address</label>
              <input
                v-model="formData.email"
                type="email"
                class="form-input"
                placeholder="you@example.com"
                required
              />
            </div>

            <div class="form-group">
              <label class="form-label">Password</label>
              <input
                v-model="formData.password"
                type="password"
                class="form-input"
                placeholder="Enter your password"
                required
              />
            </div>

            <div class="form-options">
              <label class="checkbox-wrapper">
                <input 
                  v-model="formData.rememberMe" 
                  type="checkbox" 
                  class="checkbox"
                />
                <span class="checkbox-label">Remember me</span>
              </label>
              <a href="#" class="forgot-link">Forgot password?</a>
            </div>

            <!-- Submit Button -->
            <button 
              type="submit" 
              class="submit-btn"
              :disabled="isLoading"
            >
              <span v-if="isLoading" class="spinner"></span>
              <span v-else>Sign In</span>
            </button>


            <!-- Register Link -->
            <div class="register-link">
              Don't have an account?
              <router-link to="/register" class="link">Create one</router-link>
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
  name: 'Login',
  data() {
    return {
      formData: {
        email: '',
        password: '',
        rememberMe: false
      },
      isLoading: false,
      errorMessage: ''
    }
  },
  methods: {
    async handleLogin() {
      this.isLoading = true
      this.errorMessage = ''

      try {
        const response = await axios.post('/api/auth/login', {
          email: this.formData.email,
          password: this.formData.password
        })

        // Store token and user info
        localStorage.setItem('access_token', response.data.access_token)
        localStorage.setItem('user_role', response.data.user.role)
        localStorage.setItem('user_info', JSON.stringify(response.data.user))

        // Redirect based on role
        if (response.data.user.role === 'admin') {
          this.$router.push('/admin/dashboard')
        } else if (response.data.user.role === 'seller') {
          this.$router.push('/seller/dashboard')
        } else {
          this.$router.push('/user/dashboard')
        }
      } catch (error) {
        this.errorMessage = error.response?.data?.error || 'Login failed. Please try again.'
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

.login-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #e8ecef 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.5rem;
}

.login-container {
  width: 100%;
  max-width: 1000px;
  max-height: 90vh;
}

.login-card {
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
  margin-bottom: 1.5rem;
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

.login-form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 1.125rem;
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
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.813rem;
  margin-bottom: 1.25rem;
}

.checkbox-wrapper {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.checkbox {
  width: 17px;
  height: 17px;
  cursor: pointer;
  accent-color: #000000;
}

.checkbox-label {
  color: #374151;
  font-size: 0.813rem;
  font-weight: 500;
}

.forgot-link {
  color: #000000;
  text-decoration: none;
  font-size: 0.813rem;
  font-weight: 600;
  transition: color 0.2s ease;
}

.forgot-link:hover {
  color: #4b5563;
}

.social-divider {
  position: relative;
  text-align: center;
  margin: 0.875rem 0 1rem;
}

.social-divider::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
  background: #e5e7eb;
}

.divider-text {
  background: white;
  color: #9ca3af;
  padding: 0 1rem;
  font-size: 0.813rem;
  font-weight: 500;
  position: relative;
}

.social-buttons {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
  margin-bottom: 1.125rem;
}

.social-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.625rem 0.875rem;
  border: 1.5px solid #e5e7eb;
  border-radius: 8px;
  background: white;
  font-size: 0.813rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.facebook-btn {
  color: #1877f2;
}

.facebook-btn:hover {
  background: #f0f7ff;
  border-color: #1877f2;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(24, 119, 242, 0.15);
}

.google-btn {
  color: #4b5563;
}

.google-btn:hover {
  background: #f9fafb;
  border-color: #d1d5db;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
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

.register-link {
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
  .login-card {
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
  .login-page {
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
  
  .social-buttons {
    grid-template-columns: 1fr;
    gap: 0.75rem;
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
