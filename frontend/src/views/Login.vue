<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-card">
        <!-- Login Form -->
        <div class="form-header">
          <h2 class="form-title">LOG IN</h2>
        </div>

        <form @submit.prevent="handleLogin" class="login-form">
          <div class="form-group">
            <label class="form-label">Email</label>
            <input
              v-model="formData.email"
              type="email"
              class="form-input"
              required
            />
          </div>

          <div class="form-group">
            <label class="form-label">Password</label>
            <input
              v-model="formData.password"
              type="password"
              class="form-input"
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

          <div class="social-divider">
            <span class="divider-text">OR</span>
          </div>

          <!-- Social Login Buttons -->
          <div class="social-buttons">
            <button type="button" class="social-btn facebook-btn">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
              </svg>
              Facebook
            </button>
            
            <button type="button" class="social-btn google-btn">
              <svg width="20" height="20" viewBox="0 0 24 24">
                <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
                <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
                <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
                <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
              </svg>
              Google
            </button>
          </div>

          <!-- Submit Button -->
          <button 
            type="submit" 
            class="submit-btn"
            :disabled="isLoading"
          >
            <span v-if="isLoading" class="spinner"></span>
            <span v-else>Log in</span>
          </button>

          <!-- Error Message -->
          <div v-if="errorMessage" class="error-message">
            {{ errorMessage }}
          </div>

          <!-- Register Link -->
          <div class="register-link">
            <span>Don't have an account?</span>
            <router-link to="/register" class="link">Register</router-link>
          </div>
        </form>
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
.login-page {
  min-height: 100vh;
  background: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem 1rem;
}

.login-container {
  width: 100%;
  max-width: 475px;
}

.login-card {
  background: white;
  border-radius: 20px;
  padding: 3.5rem 3rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid #e5e7eb;
}

.form-header {
  text-align: center;
  margin-bottom: 2.5rem;
}

.form-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #000000;
  margin: 0;
  letter-spacing: 1px;
}

.login-form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 1.75rem;
}

.form-label {
  display: block;
  font-size: 0.9rem;
  color: #000000;
  margin-bottom: 0.5rem;
  font-weight: 400;
}

.form-input {
  width: 100%;
  padding: 0.75rem 0;
  border: none;
  border-bottom: 1px solid #d1d5db;
  font-size: 0.95rem;
  transition: all 0.2s ease;
  background: transparent;
  color: #000000;
  font-family: inherit;
}

.form-input:focus {
  outline: none;
  border-bottom-color: #000000;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.85rem;
  margin-bottom: 1.5rem;
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
}

.checkbox-label {
  color: #000000;
  font-size: 0.85rem;
}

.forgot-link {
  color: #000000;
  text-decoration: none;
  font-size: 0.85rem;
  transition: opacity 0.2s ease;
}

.forgot-link:hover {
  opacity: 0.7;
}

.social-divider {
  position: relative;
  text-align: center;
  margin: 1.5rem 0;
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
  font-size: 0.8rem;
  font-weight: 500;
  position: relative;
}

.social-buttons {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.social-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.875rem 1rem;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: white;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.facebook-btn {
  color: #1877f2;
}

.facebook-btn:hover {
  background: #f8f9fa;
  border-color: #1877f2;
}

.google-btn {
  color: #000000;
}

.google-btn:hover {
  background: #f8f9fa;
  border-color: #d1d5db;
}

.submit-btn {
  width: 100%;
  padding: 1rem;
  background: #000000;
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.submit-btn:hover:not(:disabled) {
  background: #1a1a1a;
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error-message {
  padding: 0.875rem;
  background: #fef2f2;
  color: #dc2626;
  border: 1px solid #fecaca;
  border-radius: 8px;
  font-size: 0.875rem;
  text-align: center;
  margin-bottom: 1rem;
}

.register-link {
  text-align: center;
  font-size: 0.875rem;
  color: #6b7280;
  margin-top: 1.5rem;
}

.link {
  color: #000000;
  text-decoration: none;
  font-weight: 600;
  margin-left: 0.25rem;
}

.link:hover {
  text-decoration: underline;
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

@media (max-width: 768px) {
  .login-container {
    max-width: 400px;
  }
  
  .login-card {
    padding: 2.5rem 2rem;
  }
  
  .social-buttons {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }
}

@media (max-width: 480px) {
  .login-card {
    padding: 2rem 1.5rem;
  }
}
</style>
