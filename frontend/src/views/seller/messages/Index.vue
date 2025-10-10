<template>
  <SellerLayout>
    <div class="messages-container">
      <!-- Header -->
      <div class="messages-header">
        <h1 class="page-title">Customer Messages</h1>
        <div class="header-stats">
          <div class="stat-item">
            <span class="stat-number">{{ customerConversations.length }}</span>
            <span class="stat-label">Active Conversations</span>
          </div>
          <div class="stat-item" v-if="totalUnreadCount > 0">
            <span class="stat-number unread">{{ totalUnreadCount }}</span>
            <span class="stat-label">Unread Messages</span>
          </div>
        </div>
      </div>

      <!-- Error Message -->
      <div v-if="errorMessage" class="error-banner">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
          <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
        </svg>
        {{ errorMessage }}
        <button @click="errorMessage = ''" class="close-error">×</button>
      </div>

      <!-- Chat Interface -->
      <div class="chat-interface">
        <!-- Conversations Sidebar -->
        <div class="conversations-sidebar">
          <div class="sidebar-header">
            <h3>Customer Inquiries</h3>
            <div class="header-actions">
              <button @click="refreshConversations" class="refresh-btn" :disabled="loading">
                <svg class="refresh-icon" :class="{ spinning: loading }" width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-8 3.58-8 8s3.58 8 8 8c3.74 0 6.85-2.58 7.75-6h-2.08c-.82 2.33-3.04 4-5.67 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/>
                </svg>
              </button>
            </div>
          </div>

          <div class="conversations-list">
            <div 
              v-for="conversation in customerConversations" 
              :key="`${conversation.partner_id}_${conversation.item_id || 'general'}`"
              @click="selectConversation(conversation)"
              :class="['conversation-item', { 
                'active': isActiveConversation(conversation), 
                'has-unread': conversation.unread_count > 0 
              }]"
            >
              <!-- Item Preview (if conversation is about an item) -->
              <div v-if="conversation.item" class="conversation-item-preview">
                <div class="item-thumbnail">
                  <img v-if="conversation.item.images && conversation.item.images.length > 0" 
                       :src="`http://localhost:5000/uploads/${conversation.item.images[0]}`" 
                       :alt="conversation.item.title"
                       class="item-image">
                  <div v-else class="no-image">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z"/>
                    </svg>
                  </div>
                </div>
                <div class="item-info">
                  <div class="item-title">{{ truncateText(conversation.item.title, 25) }}</div>
                  <div class="item-price">${{ conversation.item.price }}</div>
                </div>
              </div>

              <!-- Customer Info -->
              <div class="conversation-details">
                <div class="customer-avatar">
                  <div class="avatar-circle">{{ conversation.partner_username.charAt(0).toUpperCase() }}</div>
                  <span class="customer-badge">Customer</span>
                </div>
                
                <div class="conversation-info">
                  <div class="conversation-header">
                    <span class="customer-name">{{ conversation.partner_username }}</span>
                    <span class="message-time">{{ formatRelativeTime(conversation.last_message_time) }}</span>
                  </div>
                  
                  <div class="last-message-row">
                    <span class="message-preview">{{ truncateText(conversation.last_message, 40) }}</span>
                    <div class="message-indicators">
                      <span v-if="conversation.unread_count > 0" class="unread-badge">{{ conversation.unread_count }}</span>
                      <span v-if="conversation.is_last_message_mine" class="sent-indicator">✓</span>
                    </div>
                  </div>
                  
                  <!-- Order Status (if applicable) -->
                  <div v-if="conversation.order" class="order-status">
                    <span class="order-label">Order #{{ conversation.order.order_number }}</span>
                    <span :class="['status-badge', conversation.order.status]">{{ conversation.order.status }}</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Empty State -->
            <div v-if="customerConversations.length === 0 && !loading" class="empty-conversations">
              <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
                <circle cx="9" cy="9" r="2"/>
                <path d="m13 13l6 6"/>
              </svg>
              <h3>No Customer Messages</h3>
              <p>When customers message you about your items, their conversations will appear here.</p>
            </div>

            <!-- Loading State -->
            <div v-if="loading" class="loading-conversations">
              <div class="loading-spinner"></div>
              <p>Loading conversations...</p>
            </div>
          </div>
        </div>

        <!-- Chat Panel -->
        <div class="chat-panel">
          <!-- No Conversation Selected -->
          <div v-if="!selectedConversation" class="no-conversation-selected">
            <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
            </svg>
            <h3>Select a Customer Conversation</h3>
            <p>Choose a customer from the sidebar to view and respond to their messages</p>
          </div>

          <!-- Active Chat -->
          <div v-else class="active-chat">
            <!-- Item Header (if conversation is about an item) -->
            <div v-if="conversationItem" class="item-header">
              <div class="item-details">
                <div class="item-image-container">
                  <img v-if="conversationItem.images && conversationItem.images.length > 0" 
                       :src="`http://localhost:5000/uploads/${conversationItem.images[0]}`" 
                       :alt="conversationItem.title"
                       class="item-header-image">
                  <div v-else class="no-item-image">
                    <svg width="40" height="40" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z"/>
                    </svg>
                  </div>
                </div>
                <div class="item-info-detailed">
                  <h4 class="item-title-header">{{ conversationItem.title }}</h4>
                  <p class="item-description">{{ truncateText(conversationItem.description || 'No description available', 100) }}</p>
                  <div class="item-meta">
                    <span class="item-price-header">${{ conversationItem.price }}</span>
                    <span :class="['item-status', conversationItem.status]">{{ conversationItem.status }}</span>
                  </div>
                </div>
              </div>
              
              <!-- Order Info (if applicable) -->
              <div v-if="conversationOrder" class="order-header">
                <div class="order-details">
                  <h5>Order #{{ conversationOrder.order_number }}</h5>
                  <div class="order-meta">
                    <span class="order-amount">${{ conversationOrder.total_amount }}</span>
                    <span :class="['order-status-badge', conversationOrder.status]">{{ conversationOrder.status }}</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Chat Header -->
            <div class="chat-header">
              <div class="chat-partner-info">
                <div class="partner-avatar-large">{{ selectedPartnerName.charAt(0).toUpperCase() }}</div>
                <div class="partner-details">
                  <h4>{{ selectedPartnerName }}</h4>
                  <span class="partner-role">Customer</span>
                  <span v-if="conversationItem" class="conversation-context">
                    About: {{ conversationItem.title }}
                  </span>
                </div>
              </div>
              <div class="chat-actions">
                <button @click="refreshMessages" :disabled="messagesLoading" class="action-btn">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-8 3.58-8 8s3.58 8 8 8c3.74 0 6.85-2.58 7.75-6h-2.08c-.82 2.33-3.04 4-5.67 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/>
                  </svg>
                </button>
              </div>
            </div>

            <!-- Messages List -->
            <div class="messages-list" ref="messagesList">
              <div 
                v-for="message in messages" 
                :key="message.id"
                :class="['message-bubble', { 'own-message': parseInt(message.sender_id) === parseInt(currentUserId) }]"
              >
                <div class="message-content">
                  <p class="message-text">{{ message.message }}</p>
                  <div class="message-metadata">
                    <span class="message-timestamp">{{ formatDateTime(message.created_at) }}</span>
                    <span v-if="parseInt(message.sender_id) === parseInt(currentUserId) && message.is_receiver_read" class="read-status">Read</span>
                    <span v-else-if="parseInt(message.sender_id) === parseInt(currentUserId)" class="sent-status">Sent</span>
                  </div>
                </div>
              </div>

              <!-- Empty Messages -->
              <div v-if="messages.length === 0 && !messagesLoading" class="no-messages">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
                </svg>
                <p>No messages yet</p>
                <small>This conversation hasn't started yet</small>
              </div>

              <!-- Loading Messages -->
              <div v-if="messagesLoading" class="loading-messages">
                <div class="loading-spinner small"></div>
                <p>Loading messages...</p>
              </div>
            </div>

            <!-- Message Input -->
            <div class="message-input-container">
              <form @submit.prevent="sendMessage" class="message-form">
                <div class="input-wrapper">
                  <textarea
                    v-model="newMessage"
                    @keydown.enter.exact.prevent="sendMessage"
                    @keydown.enter.shift="newMessage += '\n'"
                    placeholder="Type your response to the customer... (Shift+Enter for new line)"
                    rows="1"
                    ref="messageInput"
                    :disabled="sendingMessage"
                    class="message-input"
                    @input="autoResize"
                  ></textarea>
                  <button 
                    type="submit" 
                    :disabled="!newMessage.trim() || sendingMessage"
                    class="send-button"
                  >
                    <svg v-if="sendingMessage" class="sending-icon" width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                      <circle cx="12" cy="12" r="3" opacity="0.4"/>
                      <path d="M12 1a11 11 0 1 0 11 11A11 11 0 0 0 12 1zm0 19a8 8 0 1 1 8-8 8 8 0 0 1-8 8z" opacity="0.2"/>
                      <path d="M12 4a8 8 0 0 1 8 8" opacity="1"/>
                    </svg>
                    <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
                    </svg>
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </SellerLayout>
</template>

<script>
import SellerLayout from '@/components/seller/SellerLayout.vue'
import axios from 'axios'

export default {
  name: 'SellerMessages',
  components: {
    SellerLayout
  },
  data() {
    return {
      loading: false,
      messagesLoading: false,
      sendingMessage: false,
      conversations: [],
      messages: [],
      selectedConversation: null,
      selectedPartnerId: null,
      selectedPartnerName: '',
      conversationItem: null,
      conversationOrder: null,
      newMessage: '',
      currentUserId: null,
      totalUnreadCount: 0,
      pollingInterval: null,
      conversationPollingInterval: null,
      errorMessage: ''
    }
  },
  computed: {
    customerConversations() {
      // Only show conversations with users (customers)
      return this.conversations.filter(conv => conv.partner_role === 'user')
    }
  },
  async mounted() {
    await this.initializeUser()
    await this.loadConversations()
    this.startPolling()
  },
  beforeUnmount() {
    this.stopPolling()
  },
  methods: {
    async initializeUser() {
      try {
        const token = localStorage.getItem('access_token') || localStorage.getItem('token')
        if (!token) {
          this.$router.push('/login')
          return
        }

        // Decode JWT to get user ID
        const payload = JSON.parse(atob(token.split('.')[1]))
        this.currentUserId = payload.sub

        // Set seller role in localStorage if not already set
        const userRole = localStorage.getItem('user_role')
        if (!userRole) {
          localStorage.setItem('user_role', 'seller')
        }

        // Simple check: if we're in the seller area, assume seller access
        // More sophisticated role checking can be added later if needed
        
      } catch (error) {
        console.error('Error initializing user:', error)
        this.errorMessage = 'Authentication error. Please log in again.'
        setTimeout(() => {
          this.$router.push('/login')
        }, 2000)
      }
    },

    async loadConversations() {
      try {
        this.loading = true
        this.errorMessage = ''
        const token = localStorage.getItem('access_token') || localStorage.getItem('token')
        
        const response = await axios.get('http://localhost:5000/api/messages/conversations', {
          headers: { 'Authorization': `Bearer ${token}` }
        })

        if (response.data.success) {
          this.conversations = response.data.conversations
          this.calculateUnreadCount()
        } else {
          this.errorMessage = 'Failed to load conversations'
        }
      } catch (error) {
        console.error('Error loading conversations:', error)
        this.errorMessage = error.response?.data?.error || 'Failed to load conversations'
        if (error.response?.status === 401) {
          this.$router.push('/login')
        }
      } finally {
        this.loading = false
      }
    },

    async loadMessages(partnerId, itemId = null, silent = false) {
      if (!partnerId) return

      try {
        // Only show loading indicator if not in silent mode (during polling)
        if (!silent) {
          this.messagesLoading = true
          this.errorMessage = ''
        }
        
        const token = localStorage.getItem('access_token') || localStorage.getItem('token')
        
        let url = `http://localhost:5000/api/messages/conversation/${partnerId}`
        if (itemId) {
          url += `?item_id=${itemId}`
        }
        
        const response = await axios.get(url, {
          headers: { 'Authorization': `Bearer ${token}` }
        })

        if (response.data.success) {
          const previousMessageCount = this.messages.length
          this.messages = response.data.messages
          this.selectedPartnerName = response.data.partner.username
          this.conversationItem = response.data.item
          
          // Only scroll to bottom if we're not polling or if there are new messages
          if (!silent || this.messages.length > previousMessageCount) {
            this.$nextTick(() => {
              this.scrollToBottom()
            })
          }

          // Update conversation unread count in local data
          const conversation = this.conversations.find(c => 
            c.partner_id === partnerId && 
            (c.item_id === itemId || (!c.item_id && !itemId))
          )
          if (conversation) {
            conversation.unread_count = 0
            this.calculateUnreadCount()
          }
        }
      } catch (error) {
        console.error('Error loading messages:', error)
        this.errorMessage = error.response?.data?.error || 'Failed to load messages'
        if (error.response?.status === 401) {
          this.$router.push('/login')
        }
      } finally {
        this.messagesLoading = false
      }
    },

    async sendMessage() {
      if (!this.newMessage.trim() || !this.selectedConversation || this.sendingMessage) return

      try {
        this.sendingMessage = true
        this.errorMessage = ''
        const token = localStorage.getItem('access_token') || localStorage.getItem('token')
        
        const messageData = {
          receiver_id: this.selectedConversation.partner_id,
          message: this.newMessage.trim()
        }

        // Add item_id if this conversation is about a specific item
        if (this.selectedConversation.item_id) {
          messageData.item_id = this.selectedConversation.item_id
        }

        // Add order_id if this conversation is about a specific order
        if (this.selectedConversation.order_id) {
          messageData.order_id = this.selectedConversation.order_id
        }
        
        const response = await axios.post('http://localhost:5000/api/messages/send', messageData, {
          headers: { 'Authorization': `Bearer ${token}` }
        })

        if (response.data.success) {
          this.newMessage = ''
          // Add message to current conversation immediately for better UX
          this.messages.push(response.data.data)
          
          // Scroll to bottom
          this.$nextTick(() => {
            this.scrollToBottom()
            this.autoResize() // Reset textarea height
          })

          // Refresh conversations to update last message
          await this.loadConversations()
        }
      } catch (error) {
        console.error('Error sending message:', error)
        this.errorMessage = error.response?.data?.error || 'Failed to send message. Please try again.'
      } finally {
        this.sendingMessage = false
      }
    },

    selectConversation(conversation) {
      this.selectedConversation = conversation
      this.selectedPartnerId = conversation.partner_id
      this.selectedPartnerName = conversation.partner_username
      this.conversationOrder = conversation.order
      this.loadMessages(conversation.partner_id, conversation.item_id)
    },

    isActiveConversation(conversation) {
      return this.selectedConversation && 
             this.selectedConversation.partner_id === conversation.partner_id &&
             this.selectedConversation.item_id === conversation.item_id
    },

    calculateUnreadCount() {
      this.totalUnreadCount = this.customerConversations.reduce((total, conv) => total + conv.unread_count, 0)
    },

    startPolling() {
      // Simple AJAX polling for messages every 10 seconds (reduced frequency to avoid UI issues)
      this.pollingInterval = setInterval(async () => {
        if (this.selectedConversation && !this.messagesLoading) {
          try {
            // Use silent mode to avoid UI flickering during polling
            await this.loadMessages(this.selectedConversation.partner_id, this.selectedConversation.item_id, true)
          } catch (error) {
            console.warn('Failed to refresh messages:', error)
            // Don't show error to user for polling failures
          }
        }
      }, 10000)

      // Simple AJAX polling for conversations every 30 seconds (reduced frequency)
      this.conversationPollingInterval = setInterval(async () => {
        if (!this.loading) {
          try {
            await this.loadConversations()
          } catch (error) {
            console.warn('Failed to refresh conversations:', error)
            // Don't show error to user for polling failures
          }
        }
      }, 30000)
    },

    stopPolling() {
      if (this.pollingInterval) {
        clearInterval(this.pollingInterval)
      }
      if (this.conversationPollingInterval) {
        clearInterval(this.conversationPollingInterval)
      }
    },

    async refreshConversations() {
      await this.loadConversations()
    },

    async refreshMessages() {
      if (this.selectedConversation) {
        await this.loadMessages(this.selectedConversation.partner_id, this.selectedConversation.item_id)
      }
    },

    scrollToBottom() {
      const messagesList = this.$refs.messagesList
      if (messagesList) {
        messagesList.scrollTop = messagesList.scrollHeight
      }
    },

    autoResize() {
      const textarea = this.$refs.messageInput
      if (textarea) {
        textarea.style.height = 'auto'
        textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px'
      }
    },

    formatRelativeTime(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      const now = new Date()
      const diff = now - date
      
      if (diff < 60000) return 'now'
      if (diff < 3600000) return `${Math.floor(diff / 60000)}m ago`
      if (diff < 86400000) return `${Math.floor(diff / 3600000)}h ago`
      if (diff < 2592000000) return `${Math.floor(diff / 86400000)}d ago`
      
      return date.toLocaleDateString()
    },

    formatDateTime(dateString) {
      if (!dateString) return ''
      return new Date(dateString).toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    },

    truncateText(text, maxLength = 50) {
      if (!text || text.length <= maxLength) return text
      return text.substring(0, maxLength) + '...'
    }
  }
}
</script>

<style scoped>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* Main Container */
.messages-container {
  max-width: 1100px;
  margin: 0 auto;
  height: calc(100vh - 0px);
  display: flex;
  flex-direction: column;
  padding: 32px;
  font-family: 'Inter', sans-serif;
}

/* Header */
.messages-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding: 0 0 24px;
  background: transparent;
  border-radius: 0;
  border: none;
  border-bottom: 1px solid #e5e7eb;
  box-shadow: none;
}

.page-title {
  font-family: 'Inter', sans-serif;
  font-size: 28px;
  font-weight: 700;
  color: #000000;
  margin: 0;
  letter-spacing: -0.5px;
  text-shadow: none;
}

.header-stats {
  display: flex;
  gap: 16px;
}

.stat-item {
  text-align: center;
  padding: 12px 16px;
  background: #f9fafb;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
  min-width: 80px;
}

.stat-number {
  display: block;
  font-family: 'Inter', sans-serif;
  font-size: 24px;
  font-weight: 700;
  color: #000000;
  margin-bottom: 4px;
}

.stat-number.unread {
  color: #dc2626;
  animation: pulse 2s infinite;
}

.stat-label {
  font-size: 11px;
  color: #6b7280;
  text-transform: uppercase;
  font-weight: 600;
  letter-spacing: 0.5px;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

/* Error Banner */
.error-banner {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #dc2626;
  padding: 14px 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  position: relative;
  box-shadow: none;
  font-size: 14px;
}

.close-error {
  position: absolute;
  right: 12px;
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #dc2626;
  padding: 4px;
  border-radius: 4px;
  transition: background 0.2s ease;
}

.close-error:hover {
  background: rgba(220, 38, 38, 0.1);
}

/* Chat Interface */
.chat-interface {
  display: flex;
  height: 100%;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  border: 1px solid #e5e7eb;
}

/* Conversations Sidebar */
.conversations-sidebar {
  width: 380px;
  border-right: 1px solid #e5e7eb;
  display: flex;
  flex-direction: column;
  background: #f9fafb;
}

.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: white;
}

.sidebar-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #111827;
}

.header-actions {
  display: flex;
  gap: 8px;
}

.refresh-btn {
  background: none;
  border: 1px solid #d1d5db;
  cursor: pointer;
  color: #6b7280;
  padding: 8px;
  border-radius: 6px;
  transition: all 0.2s;
}

.refresh-btn:hover {
  color: #3b82f6;
  border-color: #3b82f6;
  background: #eff6ff;
}

.refresh-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.refresh-icon.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.conversations-list {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}

/* Conversation Item */
.conversation-item {
  background: white;
  border-radius: 12px;
  margin-bottom: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid #e5e7eb;
  overflow: hidden;
}

.conversation-item:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-color: #3b82f6;
}

.conversation-item.active {
  border-color: #3b82f6;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
  background: #eff6ff;
}

.conversation-item.has-unread {
  border-left: 4px solid #ef4444;
}

/* Item Preview */
.conversation-item-preview {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid #f3f4f6;
  background: #f8fafc;
}

.item-thumbnail {
  width: 50px;
  height: 50px;
  border-radius: 8px;
  overflow: hidden;
  margin-right: 12px;
  background: #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: center;
}

.item-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.no-image {
  color: #9ca3af;
}

.item-info {
  flex: 1;
}

.item-title {
  font-weight: 600;
  font-size: 14px;
  color: #111827;
  margin-bottom: 2px;
}

.item-price {
  font-weight: 700;
  color: #059669;
  font-size: 14px;
}

/* Conversation Details */
.conversation-details {
  display: flex;
  align-items: center;
  padding: 16px;
  gap: 12px;
}

.customer-avatar {
  position: relative;
  flex-shrink: 0;
}

.avatar-circle {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 16px;
}

.customer-badge {
  position: absolute;
  bottom: -6px;
  left: 50%;
  transform: translateX(-50%);
  background: #10b981;
  color: white;
  font-size: 10px;
  padding: 2px 6px;
  border-radius: 8px;
  text-transform: uppercase;
  font-weight: 600;
  letter-spacing: 0.5px;
  white-space: nowrap;
}

.conversation-info {
  flex: 1;
  min-width: 0;
}

.conversation-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.customer-name {
  font-weight: 600;
  color: #111827;
  font-size: 15px;
}

.message-time {
  font-size: 12px;
  color: #6b7280;
  font-weight: 500;
}

.last-message-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.message-preview {
  font-size: 13px;
  color: #6b7280;
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-right: 8px;
}

.message-indicators {
  display: flex;
  align-items: center;
  gap: 6px;
}

.unread-badge {
  background: #ef4444;
  color: white;
  font-size: 11px;
  font-weight: 600;
  padding: 3px 7px;
  border-radius: 12px;
  min-width: 20px;
  text-align: center;
}

.sent-indicator {
  color: #10b981;
  font-size: 12px;
  font-weight: 600;
}

/* Order Status */
.order-status {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 4px;
}

.order-label {
  font-size: 12px;
  color: #6b7280;
  font-weight: 500;
}

.status-badge {
  font-size: 10px;
  padding: 2px 6px;
  border-radius: 6px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-badge.pending { background: #fef3c7; color: #d97706; }
.status-badge.confirmed { background: #dcfce7; color: #16a34a; }
.status-badge.shipped { background: #dbeafe; color: #2563eb; }
.status-badge.delivered { background: #f0fdf4; color: #15803d; }
.status-badge.cancelled { background: #fee2e2; color: #dc2626; }

/* Empty States */
.empty-conversations, .loading-conversations {
  padding: 60px 20px;
  text-align: center;
  color: #6b7280;
}

.empty-conversations svg, .loading-conversations svg {
  margin-bottom: 20px;
  color: #d1d5db;
}

.empty-conversations h3 {
  color: #374151;
  margin: 0 0 8px;
  font-size: 18px;
}

.empty-conversations p {
  margin: 0;
  font-size: 14px;
  line-height: 1.5;
}

.loading-spinner {
  width: 32px;
  height: 32px;
  border: 3px solid #e5e7eb;
  border-top: 3px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 16px;
}

.loading-spinner.small {
  width: 20px;
  height: 20px;
  border-width: 2px;
}

/* Chat Panel */
.chat-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: white;
}

.no-conversation-selected {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #6b7280;
  text-align: center;
  padding: 40px;
}

.no-conversation-selected svg {
  margin-bottom: 24px;
  color: #d1d5db;
}

.no-conversation-selected h3 {
  margin: 0 0 8px;
  color: #374151;
  font-size: 20px;
}

.no-conversation-selected p {
  margin: 0;
  font-size: 14px;
  max-width: 300px;
}

/* Active Chat */
.active-chat {
  height: 100%;
  display: flex;
  flex-direction: column;
}

/* Item Header */
.item-header {
  background: #f9fafb;
  border-bottom: 1px solid #e5e7eb;
  padding: 16px 20px;
}

.item-details {
  display: flex;
  align-items: center;
  gap: 16px;
}

.item-image-container {
  width: 80px;
  height: 80px;
  border-radius: 12px;
  overflow: hidden;
  background: #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: center;
}

.item-header-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.no-item-image {
  color: #9ca3af;
}

.item-info-detailed {
  flex: 1;
}

.item-title-header {
  margin: 0 0 8px;
  font-size: 18px;
  font-weight: 600;
  color: #111827;
}

.item-description {
  margin: 0 0 8px;
  font-size: 14px;
  color: #6b7280;
  line-height: 1.4;
}

.item-meta {
  display: flex;
  align-items: center;
  gap: 12px;
}

.item-price-header {
  font-size: 18px;
  font-weight: 700;
  color: #059669;
}

.item-status {
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
}

.item-status.active { background: #dcfce7; color: #16a34a; }
.item-status.sold { background: #fee2e2; color: #dc2626; }
.item-status.pending { background: #fef3c7; color: #d97706; }

/* Order Header */
.order-header {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #e5e7eb;
}

.order-details h5 {
  margin: 0 0 6px;
  font-size: 14px;
  font-weight: 600;
  color: #111827;
}

.order-meta {
  display: flex;
  align-items: center;
  gap: 12px;
}

.order-amount {
  font-size: 16px;
  font-weight: 700;
  color: #059669;
}

.order-status-badge {
  padding: 3px 8px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
}

.order-status-badge.pending { background: #fef3c7; color: #d97706; }
.order-status-badge.confirmed { background: #dcfce7; color: #16a34a; }
.order-status-badge.shipped { background: #dbeafe; color: #2563eb; }
.order-status-badge.delivered { background: #f0fdf4; color: #15803d; }

/* Chat Header */
.chat-header {
  padding: 20px;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: white;
}

.chat-partner-info {
  display: flex;
  align-items: center;
  gap: 16px;
}

.partner-avatar-large {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 18px;
}

.partner-details h4 {
  margin: 0 0 4px;
  font-size: 18px;
  color: #111827;
}

.partner-role {
  font-size: 12px;
  color: #6b7280;
  text-transform: uppercase;
  font-weight: 600;
  letter-spacing: 0.5px;
  display: block;
  margin-bottom: 2px;
}

.conversation-context {
  font-size: 13px;
  color: #3b82f6;
  font-weight: 500;
}

.chat-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  background: none;
  border: 1px solid #d1d5db;
  padding: 8px;
  border-radius: 6px;
  cursor: pointer;
  color: #6b7280;
  transition: all 0.2s;
}

.action-btn:hover {
  color: #3b82f6;
  border-color: #3b82f6;
  background: #eff6ff;
}

.action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Messages List */
.messages-list {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  background: #ffffff;
}

.message-bubble {
  display: flex;
  max-width: 75%;
  animation: fadeIn 0.3s ease-out;
  margin-bottom: 16px;
}

.message-bubble.own-message {
  align-self: flex-end;
  margin-left: auto;
  margin-right: 0;
}

.message-bubble:not(.own-message) {
  align-self: flex-start;
  margin-left: 0;
  margin-right: auto;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.message-content {
  background: #f3f4f6;
  padding: 12px 16px;
  border-radius: 18px;
  position: relative;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.own-message .message-content {
  background: #000000;
  color: white;
}

.message-text {
  margin: 0 0 8px;
  font-size: 14px;
  line-height: 1.4;
  word-wrap: break-word;
}

.message-metadata {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 11px;
  opacity: 0.7;
}

.own-message .message-metadata {
  color: rgba(255, 255, 255, 0.8);
}

.message-timestamp {
  font-weight: 500;
}

.read-status {
  color: #10b981;
  font-weight: 600;
}

.sent-status {
  color: #6b7280;
  font-weight: 500;
}

.own-message .sent-status {
  color: rgba(255, 255, 255, 0.8);
}

.no-messages, .loading-messages {
  text-align: center;
  color: #6b7280;
  padding: 60px 20px;
}

.no-messages svg, .loading-messages svg {
  margin-bottom: 16px;
  color: #d1d5db;
}

/* Message Input */
.message-input-container {
  padding: 20px;
  border-top: 1px solid #e5e7eb;
  background: white;
}

.message-form {
  max-width: 100%;
}

.input-wrapper {
  display: flex;
  gap: 12px;
  align-items: flex-end;
}

.message-input {
  flex: 1;
  min-height: 44px;
  max-height: 120px;
  padding: 12px 16px;
  border: 1px solid #d1d5db;
  border-radius: 22px;
  font-size: 14px;
  font-family: inherit;
  resize: none;
  background: #f9fafb;
  transition: all 0.2s;
  outline: none;
}

.message-input:focus {
  border-color: #000000;
  background: white;
  box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.05);
}

.message-input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.send-button {
  width: 44px;
  height: 44px;
  border: none;
  background: #000000;
  color: white;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.send-button:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.send-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.sending-icon {
  animation: spin 1s linear infinite;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .conversations-sidebar {
    width: 320px;
  }
  
  .item-header {
    padding: 12px 16px;
  }
  
  .item-details {
    gap: 12px;
  }
  
  .item-image-container {
    width: 60px;
    height: 60px;
  }
}

@media (max-width: 768px) {
  .messages-container {
    height: calc(100vh - 80px);
    padding: 0 8px;
  }
  
  .chat-interface {
    flex-direction: column;
    border-radius: 12px;
  }
  
  .conversations-sidebar {
    width: 100%;
    max-height: 40vh;
  }
  
  .messages-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .header-stats {
    gap: 20px;
  }
  
  .page-title {
    font-size: 24px;
  }
  
  .message-bubble {
    max-width: 90%;
  }
  
  .conversation-item-preview {
    padding: 8px 12px;
  }
  
  .item-thumbnail {
    width: 40px;
    height: 40px;
  }
  
  .conversation-details {
    padding: 12px;
  }
}
</style>
