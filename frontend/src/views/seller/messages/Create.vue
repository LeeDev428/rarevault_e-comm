<template>
  <SellerLayout>
    <div class="create-message-container">
      <div class="page-header">
        <button @click="$router.go(-1)" class="back-btn">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
            <path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.42-1.41L7.83 13H20v-2z"/>
          </svg>
          Back
        </button>
        <h1 class="page-title">Reply to Customer</h1>
      </div>

      <div class="message-form-container">
        <form @submit.prevent="sendMessage" class="message-form">
          <div class="form-group">
            <label for="recipient">To Customer:</label>
            <input 
              type="text" 
              id="recipient"
              v-model="recipientName"
              :disabled="true"
              class="form-input"
            />
          </div>

          <div class="form-group">
            <label for="subject">Subject (Optional):</label>
            <input 
              type="text" 
              id="subject"
              v-model="subject"
              placeholder="What's this about?"
              class="form-input"
            />
          </div>

          <div class="form-group">
            <label for="message">Message:</label>
            <textarea 
              id="message"
              v-model="messageText"
              placeholder="Type your response here..."
              rows="8"
              required
              class="form-textarea"
            ></textarea>
          </div>

          <div class="form-actions">
            <button 
              type="button" 
              @click="$router.go(-1)"
              class="btn-secondary"
            >
              Cancel
            </button>
            <button 
              type="submit" 
              :disabled="!messageText.trim() || sending"
              class="btn-primary seller"
            >
              <span v-if="sending">Sending...</span>
              <span v-else>Send Reply</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </SellerLayout>
</template>

<script>
import SellerLayout from '@/components/seller/SellerLayout.vue'
import axios from 'axios'

export default {
  name: 'SellerCreateMessage',
  components: {
    SellerLayout
  },
  data() {
    return {
      recipientId: null,
      recipientName: '',
      subject: '',
      messageText: '',
      sending: false
    }
  },
  mounted() {
    this.initializeFromRoute()
    this.verifySellerAccess()
  },
  methods: {
    verifySellerAccess() {
      try {
        const token = localStorage.getItem('access_token') || localStorage.getItem('token')
        if (!token) {
          this.$router.push('/login')
          return
        }

        // Decode JWT to verify user is a seller
        const payload = JSON.parse(atob(token.split('.')[1]))
        if (payload.role !== 'seller') {
          this.$router.push('/user/dashboard')
          return
        }
      } catch (error) {
        console.error('Error verifying seller access:', error)
        this.$router.push('/login')
      }
    },

    initializeFromRoute() {
      // Get recipient info from route query
      this.recipientId = this.$route.query.customerId || this.$route.query.recipientId
      this.recipientName = this.$route.query.customerName || this.$route.query.recipientName || 'Customer'
      
      if (!this.recipientId) {
        this.$router.push('/seller/messages')
        return
      }

      // Pre-fill subject if provided
      if (this.$route.query.subject) {
        this.subject = this.$route.query.subject
      }

      // Pre-fill message if provided
      if (this.$route.query.message) {
        this.messageText = this.$route.query.message
      }

      // Default subject for order-related messages
      if (this.$route.query.orderId) {
        this.subject = `Re: Order #${this.$route.query.orderId}`
      }
    },

    async sendMessage() {
      if (!this.messageText.trim() || !this.recipientId || this.sending) return

      try {
        this.sending = true
        const token = localStorage.getItem('access_token') || localStorage.getItem('token')
        
        if (!token) {
          this.$router.push('/login')
          return
        }

        let finalMessage = this.messageText.trim()
        
        // Add subject to message if provided
        if (this.subject.trim()) {
          finalMessage = `Subject: ${this.subject.trim()}\n\n${finalMessage}`
        }

        const response = await axios.post('http://localhost:5000/api/messages/send', {
          receiver_id: this.recipientId,
          message: finalMessage
        }, {
          headers: { 'Authorization': `Bearer ${token}` }
        })

        if (response.data.success) {
          alert('Reply sent successfully!')
          
          // Navigate to seller messages page with the customer selected
          this.$router.push({
            path: '/seller/messages',
            query: { 
              customerId: this.recipientId,
              customerName: this.recipientName
            }
          })
        } else {
          throw new Error(response.data.error || 'Failed to send message')
        }
      } catch (error) {
        console.error('Error sending message:', error)
        const errorMessage = error.response?.data?.error || error.message || 'Failed to send reply'
        alert(`Error: ${errorMessage}`)
      } finally {
        this.sending = false
      }
    }
  }
}
</script>

<style scoped>
.create-message-container {
  max-width: 800px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 32px;
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: #f3f4f6;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  color: #374151;
  font-weight: 500;
  transition: background 0.2s ease;
}

.back-btn:hover {
  background: #e5e7eb;
}

.page-title {
  font-size: 28px;
  font-weight: 700;
  color: #111827;
  margin: 0;
}

.message-form-container {
  background: white;
  padding: 32px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.message-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-weight: 600;
  color: #374151;
}

.form-input,
.form-textarea {
  padding: 12px 16px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 14px;
  font-family: inherit;
  transition: border-color 0.2s ease;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: #f59e0b;
  box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.1);
}

.form-input:disabled {
  background: #f9fafb;
  color: #6b7280;
  cursor: not-allowed;
}

.form-textarea {
  resize: vertical;
  min-height: 120px;
  line-height: 1.5;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 8px;
}

.btn-secondary,
.btn-primary {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-secondary {
  background: #f3f4f6;
  color: #374151;
}

.btn-secondary:hover {
  background: #e5e7eb;
}

.btn-primary {
  background: #3b82f6;
  color: white;
}

.btn-primary.seller {
  background: #f59e0b;
}

.btn-primary:hover:not(:disabled) {
  background: #2563eb;
}

.btn-primary.seller:hover:not(:disabled) {
  background: #d97706;
}

.btn-primary:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

/* Responsive */
@media (max-width: 768px) {
  .create-message-container {
    padding: 0 16px;
  }
  
  .message-form-container {
    padding: 24px 20px;
  }
  
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .form-actions {
    flex-direction: column-reverse;
  }
  
  .btn-secondary,
  .btn-primary {
    width: 100%;
  }
}
</style>
