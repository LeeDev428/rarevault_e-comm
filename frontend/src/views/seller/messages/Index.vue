<template>
  <SellerLayout>
    <div class="messages-container">
      <!-- Header -->
      <div class="messages-header">
        <h1 class="page-title">Customer Messages</h1>
        <div class="header-stats">
          <div class="stat-item">
            <span class="stat-number">{{ conversations.length }}</span>
            <span class="stat-label">Conversations</span>
          </div>
          <div class="stat-item" v-if="totalUnreadCount > 0">
            <span class="stat-number unread">{{ totalUnreadCount }}</span>
            <span class="stat-label">Unread</span>
          </div>
        </div>
      </div>

      <!-- Chat Interface -->
      <div class="chat-interface">
        <!-- Conversations List (Left Sidebar) -->
        <div class="conversations-sidebar">
          <div class="sidebar-header">
            <h3>Customer Conversations</h3>
            <button @click="refreshConversations" class="refresh-btn" :disabled="loading">
              <svg class="refresh-icon" :class="{ spinning: loading }" width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                <path d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-8 3.58-8 8s3.58 8 8 8c3.74 0 6.85-2.58 7.75-6h-2.08c-.82 2.33-3.04 4-5.67 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/>
              </svg>
            </button>
          </div>

          <div class="conversations-list">
            <div 
              v-for="conversation in conversations" 
              :key="conversation.partner_id"
              @click="selectConversation(conversation)"
              :class="['conversation-item', { 'active': selectedPartnerId === conversation.partner_id, 'has-unread': conversation.unread_count > 0 }]"
            >
              <div class="conversation-avatar">
                <div class="avatar-circle customer">{{ conversation.partner_username.charAt(0).toUpperCase() }}</div>
                <span class="role-badge user">Customer</span>
              </div>
              <div class="conversation-info">
                <div class="conversation-header">
                  <span class="partner-name">{{ conversation.partner_username }}</span>
                  <span class="message-time">{{ formatTime(conversation.last_message_time) }}</span>
                </div>
                <div class="last-message">
                  <span class="message-preview">{{ truncateMessage(conversation.last_message) }}</span>
                  <div class="message-indicators">
                    <span v-if="conversation.unread_count > 0" class="unread-badge">{{ conversation.unread_count }}</span>
                    <span v-if="conversation.is_last_message_mine" class="sent-indicator">✓</span>
                  </div>
                </div>
              </div>
            </div>

            <div v-if="conversations.length === 0 && !loading" class="empty-conversations">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
                <circle cx="9" cy="9" r="2"/>
                <path d="m13 13l6 6"/>
              </svg>
              <p>No customer messages yet</p>
              <small>Customer messages will appear here when they contact you</small>
            </div>
          </div>
        </div>

        <!-- Chat Area (Right Panel) -->
        <div class="chat-panel">
          <div v-if="!selectedPartnerId" class="no-conversation-selected">
            <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
            </svg>
            <h3>Select a customer conversation</h3>
            <p>Choose a customer from the sidebar to view and respond to their messages</p>
          </div>

          <div v-else class="active-chat">
            <!-- Chat Header -->
            <div class="chat-header">
              <div class="chat-partner-info">
                <div class="partner-avatar customer">{{ selectedPartnerName.charAt(0).toUpperCase() }}</div>
                <div>
                  <h4>{{ selectedPartnerName }}</h4>
                  <span class="partner-role">Customer</span>
                </div>
              </div>
              <div class="chat-actions">
                <button @click="refreshMessages" :disabled="messagesLoading" class="action-btn secondary">
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
                :class="['message-item', { 'own-message': message.sender_id === currentUserId }]"
              >
                <div class="message-content">
                  <p>{{ message.message }}</p>
                  <div class="message-meta">
                    <span class="message-time">{{ formatDateTime(message.created_at) }}</span>
                    <span v-if="message.sender_id === currentUserId && message.is_receiver_read" class="read-indicator">✓✓</span>
                    <span v-else-if="message.sender_id === currentUserId" class="sent-indicator">✓</span>
                  </div>
                </div>
              </div>

              <div v-if="messages.length === 0 && !messagesLoading" class="no-messages">
                <p>No messages yet</p>
                <small>This customer hasn't sent any messages</small>
              </div>
            </div>

            <!-- Message Input -->
            <div class="message-input-container">
              <form @submit.prevent="sendMessage" class="message-form">
                <div class="input-group">
                  <textarea
                    v-model="newMessage"
                    @keydown.enter.exact.prevent="sendMessage"
                    @keydown.enter.shift="newMessage += '\n'"
                    placeholder="Type your response... (Shift+Enter for new line)"
                    rows="1"
                    ref="messageInput"
                    :disabled="sendingMessage"
                    class="message-textarea"
                  ></textarea>
                  <button 
                    type="submit" 
                    :disabled="!newMessage.trim() || sendingMessage"
                    class="send-btn"
                  >
                    <svg v-if="sendingMessage" class="sending-spinner" width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
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
      selectedPartnerId: null,
      selectedPartnerName: '',
      selectedPartnerRole: '',
      newMessage: '',
      currentUserId: null,
      totalUnreadCount: 0,
      pollingInterval: null,
      conversationPollingInterval: null
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

        // Decode JWT to get user ID (basic decode, in production use proper JWT library)
        const payload = JSON.parse(atob(token.split('.')[1]))
        this.currentUserId = payload.sub

        // Verify user is a seller
        if (payload.role !== 'seller') {
          this.$router.push('/user/dashboard')
          return
        }
      } catch (error) {
        console.error('Error initializing user:', error)
        this.$router.push('/login')
      }
    },

    async loadConversations() {
      try {
        this.loading = true
        const token = localStorage.getItem('access_token') || localStorage.getItem('token')
        
        const response = await axios.get('http://localhost:5000/api/messages/conversations', {
          headers: { 'Authorization': `Bearer ${token}` }
        })

        if (response.data.success) {
          // Filter to only show conversations with users (customers)
          this.conversations = response.data.conversations.filter(conv => 
            conv.partner_role === 'user'
          )
          this.calculateUnreadCount()
        }
      } catch (error) {
        console.error('Error loading conversations:', error)
        if (error.response?.status === 401) {
          this.$router.push('/login')
        }
      } finally {
        this.loading = false
      }
    },

    async loadMessages(partnerId) {
      if (!partnerId) return

      try {
        this.messagesLoading = true
        const token = localStorage.getItem('access_token') || localStorage.getItem('token')
        
        const response = await axios.get(`http://localhost:5000/api/messages/conversation/${partnerId}`, {
          headers: { 'Authorization': `Bearer ${token}` }
        })

        if (response.data.success) {
          this.messages = response.data.messages
          this.selectedPartnerName = response.data.partner.username
          this.selectedPartnerRole = response.data.partner.role
          
          // Scroll to bottom after loading messages
          this.$nextTick(() => {
            this.scrollToBottom()
          })

          // Mark as read
          await this.markMessagesAsRead(partnerId)
        }
      } catch (error) {
        console.error('Error loading messages:', error)
        if (error.response?.status === 401) {
          this.$router.push('/login')
        }
      } finally {
        this.messagesLoading = false
      }
    },

    async sendMessage() {
      if (!this.newMessage.trim() || !this.selectedPartnerId || this.sendingMessage) return

      try {
        this.sendingMessage = true
        const token = localStorage.getItem('access_token') || localStorage.getItem('token')
        
        const response = await axios.post('http://localhost:5000/api/messages/send', {
          receiver_id: this.selectedPartnerId,
          message: this.newMessage.trim()
        }, {
          headers: { 'Authorization': `Bearer ${token}` }
        })

        if (response.data.success) {
          this.newMessage = ''
          // Add message to current conversation immediately for better UX
          this.messages.push(response.data.data)
          
          // Scroll to bottom
          this.$nextTick(() => {
            this.scrollToBottom()
          })

          // Refresh conversations to update last message
          await this.loadConversations()
        }
      } catch (error) {
        console.error('Error sending message:', error)
        alert('Failed to send message. Please try again.')
      } finally {
        this.sendingMessage = false
      }
    },

    async markMessagesAsRead(senderId) {
      try {
        const token = localStorage.getItem('access_token') || localStorage.getItem('token')
        
        await axios.put('http://localhost:5000/api/messages/mark-read', {
          sender_id: senderId
        }, {
          headers: { 'Authorization': `Bearer ${token}` }
        })

        // Update local conversation data
        const conversation = this.conversations.find(c => c.partner_id === senderId)
        if (conversation) {
          conversation.unread_count = 0
          this.calculateUnreadCount()
        }
      } catch (error) {
        console.error('Error marking messages as read:', error)
      }
    },

    selectConversation(conversation) {
      this.selectedPartnerId = conversation.partner_id
      this.selectedPartnerName = conversation.partner_username
      this.selectedPartnerRole = conversation.partner_role
      this.loadMessages(conversation.partner_id)
    },

    calculateUnreadCount() {
      this.totalUnreadCount = this.conversations.reduce((total, conv) => total + conv.unread_count, 0)
    },

    startPolling() {
      // Poll messages every 3 seconds when a conversation is selected
      this.pollingInterval = setInterval(() => {
        if (this.selectedPartnerId && !this.messagesLoading) {
          this.loadMessages(this.selectedPartnerId)
        }
      }, 3000)

      // Poll conversations every 10 seconds
      this.conversationPollingInterval = setInterval(() => {
        if (!this.loading) {
          this.loadConversations()
        }
      }, 10000)
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
      if (this.selectedPartnerId) {
        await this.loadMessages(this.selectedPartnerId)
      }
    },

    scrollToBottom() {
      const messagesList = this.$refs.messagesList
      if (messagesList) {
        messagesList.scrollTop = messagesList.scrollHeight
      }
    },

    formatTime(dateString) {
      const date = new Date(dateString)
      const now = new Date()
      const diff = now - date
      
      if (diff < 60000) return 'now'
      if (diff < 3600000) return `${Math.floor(diff / 60000)}m`
      if (diff < 86400000) return `${Math.floor(diff / 3600000)}h`
      if (diff < 2592000000) return `${Math.floor(diff / 86400000)}d`
      
      return date.toLocaleDateString()
    },

    formatDateTime(dateString) {
      return new Date(dateString).toLocaleString()
    },

    truncateMessage(message, maxLength = 50) {
      if (message.length <= maxLength) return message
      return message.substring(0, maxLength) + '...'
    }
  }
}
</script>

<style scoped>
.messages-container {
  max-width: 1200px;
  margin: 0 auto;
  height: calc(100vh - 120px);
  display: flex;
  flex-direction: column;
}

.messages-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.page-title {
  font-size: 28px;
  font-weight: 700;
  color: #111827;
  margin: 0;
}

.header-stats {
  display: flex;
  gap: 24px;
}

.stat-item {
  text-align: center;
}

.stat-number {
  display: block;
  font-size: 24px;
  font-weight: 700;
  color: #3b82f6;
  margin-bottom: 4px;
}

.stat-number.unread {
  color: #ef4444;
}

.stat-label {
  font-size: 12px;
  color: #6b7280;
  text-transform: uppercase;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.chat-interface {
  display: flex;
  height: 100%;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

/* Conversations Sidebar */
.conversations-sidebar {
  width: 320px;
  border-right: 1px solid #e5e7eb;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.sidebar-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

.refresh-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: #6b7280;
  padding: 4px;
  border-radius: 4px;
}

.refresh-btn:hover {
  background: #f3f4f6;
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
}

.conversation-item {
  display: flex;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #f3f4f6;
  cursor: pointer;
  transition: background 0.2s ease;
  position: relative;
}

.conversation-item:hover {
  background: #f9fafb;
}

.conversation-item.active {
  background: #eff6ff;
  border-right: 3px solid #3b82f6;
}

.conversation-item.has-unread {
  background: #fef7ff;
}

.conversation-item.has-unread.active {
  background: #eff6ff;
}

.conversation-avatar {
  position: relative;
  margin-right: 12px;
}

.avatar-circle {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #3b82f6;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
}

.avatar-circle.customer {
  background: #10b981;
}

.role-badge {
  position: absolute;
  bottom: -2px;
  right: -2px;
  background: #10b981;
  color: white;
  font-size: 10px;
  padding: 2px 6px;
  border-radius: 8px;
  text-transform: uppercase;
  font-weight: 600;
}

.role-badge.user {
  background: #10b981;
}

.conversation-info {
  flex: 1;
  min-width: 0;
}

.conversation-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.partner-name {
  font-weight: 600;
  color: #111827;
}

.message-time {
  font-size: 12px;
  color: #6b7280;
}

.last-message {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.message-preview {
  color: #6b7280;
  font-size: 14px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.message-indicators {
  display: flex;
  align-items: center;
  gap: 4px;
}

.unread-badge {
  background: #ef4444;
  color: white;
  font-size: 11px;
  padding: 2px 6px;
  border-radius: 10px;
  min-width: 18px;
  text-align: center;
}

.sent-indicator {
  color: #10b981;
  font-size: 12px;
}

.empty-conversations {
  text-align: center;
  padding: 40px 20px;
  color: #6b7280;
}

/* Chat Panel - Same as user messages but with seller branding */
.chat-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.no-conversation-selected {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: #6b7280;
  text-align: center;
}

.no-conversation-selected h3 {
  margin: 16px 0 8px 0;
  color: #374151;
}

.active-chat {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.chat-header {
  padding: 20px;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chat-partner-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.partner-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #10b981;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
}

.chat-partner-info h4 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #111827;
}

.partner-role {
  font-size: 12px;
  color: #6b7280;
  text-transform: uppercase;
}

.action-btn {
  background: #f3f4f6;
  border: none;
  padding: 8px;
  border-radius: 6px;
  cursor: pointer;
  color: #6b7280;
}

.action-btn:hover {
  background: #e5e7eb;
}

/* Messages List */
.messages-list {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.message-item {
  display: flex;
  max-width: 70%;
}

.message-item.own-message {
  align-self: flex-end;
  flex-direction: row-reverse;
}

.message-content {
  background: #f3f4f6;
  padding: 12px 16px;
  border-radius: 18px;
  max-width: 100%;
}

.own-message .message-content {
  background: #f59e0b;
  color: white;
}

.message-content p {
  margin: 0 0 8px 0;
  line-height: 1.4;
  word-wrap: break-word;
}

.message-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 4px;
}

.message-time {
  font-size: 11px;
  opacity: 0.7;
}

.read-indicator {
  color: #10b981;
  font-size: 12px;
}

.sent-indicator {
  color: #6b7280;
  font-size: 12px;
}

.own-message .sent-indicator,
.own-message .read-indicator {
  color: rgba(255, 255, 255, 0.8);
}

.no-messages {
  text-align: center;
  color: #6b7280;
  padding: 40px 20px;
}

/* Message Input */
.message-input-container {
  padding: 20px;
  border-top: 1px solid #e5e7eb;
}

.message-form {
  display: flex;
  gap: 12px;
}

.input-group {
  flex: 1;
  display: flex;
  gap: 8px;
}

.message-textarea {
  flex: 1;
  padding: 12px 16px;
  border: 1px solid #d1d5db;
  border-radius: 20px;
  resize: none;
  font-family: inherit;
  font-size: 14px;
  line-height: 1.4;
  max-height: 120px;
  min-height: 44px;
}

.message-textarea:focus {
  outline: none;
  border-color: #f59e0b;
  box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.1);
}

.send-btn {
  width: 44px;
  height: 44px;
  border: none;
  border-radius: 50%;
  background: #f59e0b;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.send-btn:hover:not(:disabled) {
  background: #d97706;
}

.send-btn:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

.sending-spinner {
  animation: spin 1s linear infinite;
}

/* Responsive */
@media (max-width: 768px) {
  .messages-container {
    height: calc(100vh - 80px);
  }
  
  .conversations-sidebar {
    width: 280px;
  }
  
  .chat-interface {
    flex-direction: column;
  }
  
  .messages-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .header-stats {
    align-self: stretch;
    justify-content: space-around;
  }
}
</style>
