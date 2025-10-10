<template>
  <UserLayout>
    <div class="messages-container">
      <!-- Header -->
      <div class="messages-header">
        <h1 class="page-title">Messages</h1>
        <div class="header-actions">
         
          <div class="unread-count" v-if="totalUnreadCount > 0">
            {{ totalUnreadCount }} unread message{{ totalUnreadCount > 1 ? 's' : '' }}
          </div>
        </div>
      </div>

      <!-- Chat Interface -->
      <div class="chat-interface">
        <!-- Conversations List (Left Sidebar) -->
        <div class="conversations-sidebar">
          <div class="sidebar-header">
            <h3>Conversations</h3>
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
              :class="['conversation-item', { 'active': selectedPartnerId === conversation.partner_id }]"
            >
              <div class="conversation-avatar">
                <div class="avatar-circle" :class="conversation.partner_role">{{ conversation.partner_username.charAt(0).toUpperCase() }}</div>
                <span class="role-badge" :class="conversation.partner_role">{{ conversation.partner_role === 'seller' ? 'Seller' : conversation.partner_role }}</span>
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
              </svg>
              <p>No conversations yet</p>
              <small>Start messaging with sellers!</small>
            </div>
          </div>
        </div>

        <!-- Chat Area (Right Panel) -->
        <div class="chat-panel">
          <div v-if="!selectedPartnerId" class="no-conversation-selected">
            <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
            </svg>
            <h3>Select a conversation</h3>
            <p>Choose a conversation from the sidebar to start messaging</p>
          </div>

          <div v-else class="active-chat">
            <!-- Chat Header -->
            <div class="chat-header">
              <div class="chat-partner-info">
              <div>
                  <h4>{{ selectedPartnerName }}</h4>
                  <span class="partner-role">{{ selectedPartnerRole === 'seller' ? 'Seller' : selectedPartnerRole }}</span>
                </div>
              </div>
              <div class="chat-actions">
                
              </div>
            </div>

            <!-- Messages List -->
            <div class="messages-list" ref="messagesList">
              <div 
                v-for="message in messages" 
                :key="message.id"
                :class="['message-item', { 'own-message': parseInt(message.sender_id) === parseInt(currentUserId) }]"
              >
                <div class="message-content">
                  <p>{{ message.message }}</p>
                  <div class="message-meta">
                    <span class="message-time">{{ formatDateTime(message.created_at) }}</span>
                    <span v-if="parseInt(message.sender_id) === parseInt(currentUserId) && message.is_receiver_read" class="read-indicator">✓✓</span>
                    <span v-else-if="parseInt(message.sender_id) === parseInt(currentUserId)" class="sent-indicator">✓</span>
                  </div>
                </div>
              </div>

              <div v-if="messages.length === 0 && !messagesLoading" class="no-messages">
                <p>No messages yet</p>
                <small>Start the conversation!</small>
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
                    placeholder="Type your message... (Shift+Enter for new line)"
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

      <!-- Sellers Modal -->
      <div v-if="showSellersModal" class="modal-overlay" @click="showSellersModal = false">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h3>Message a Seller</h3>
            <button @click="showSellersModal = false" class="close-btn">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
              </svg>
            </button>
          </div>
          <div class="modal-body">
            <div v-if="loadingSellers" class="loading-sellers">
              <div class="loading-spinner"></div>
              <p>Loading sellers...</p>
            </div>
            <div v-else class="sellers-list">
              <div 
                v-for="seller in sellers" 
                :key="seller.id"
                @click="startConversationWithSeller(seller)"
                class="seller-item"
                :class="{ 'has-conversation': seller.has_conversation }"
              >
                <div class="seller-avatar">{{ seller.username.charAt(0).toUpperCase() }}</div>
                <div class="seller-info">
                  <div class="seller-name">{{ seller.username }}</div>
                  <div class="seller-status">
                    <span v-if="seller.has_conversation" class="existing">Existing conversation</span>
                    <span v-else class="new">Click to start conversation</span>
                  </div>
                </div>
                <div class="seller-action">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                  </svg>
                </div>
              </div>
              <div v-if="sellers.length === 0" class="no-sellers">
                <p>No sellers available</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Start Conversation Modal -->
      <div v-if="showStartConversationModal" class="modal-overlay" @click="closeStartConversationModal">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h3>Message {{ selectedSellerForConversation?.username }}</h3>
            <button @click="closeStartConversationModal" class="close-btn">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
              </svg>
            </button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="sendInitialMessage" class="start-conversation-form">
              <div class="form-group">
                <label for="initialMessage">Your message:</label>
                <textarea
                  id="initialMessage"
                  v-model="initialMessage"
                  placeholder="Hi! I'm interested in your items..."
                  rows="4"
                  required
                  class="initial-message-textarea"
                ></textarea>
              </div>
              <div class="form-actions">
                <button type="button" @click="closeStartConversationModal" class="btn secondary">Cancel</button>
                <button type="submit" :disabled="!initialMessage.trim() || startingConversation" class="btn primary">
                  <span v-if="startingConversation">Sending...</span>
                  <span v-else>Send Message</span>
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </UserLayout>
</template>

<script>
import UserLayout from '@/components/user/UserLayout.vue'
import axios from 'axios'

export default {
  name: 'UserMessages',
  components: {
    UserLayout
  },
  data() {
    return {
      loading: false,
      messagesLoading: false,
      sendingMessage: false,
      loadingSellers: false,
      startingConversation: false,
      conversations: [],
      messages: [],
      sellers: [],
      selectedPartnerId: null,
      selectedPartnerName: '',
      selectedPartnerRole: '',
      selectedSellerForConversation: null,
      newMessage: '',
      initialMessage: '',
      currentUserId: null,
      totalUnreadCount: 0,
      pollingInterval: null,
      conversationPollingInterval: null,
      showSellersModal: false,
      showStartConversationModal: false,
      errorMessage: ''
    }
  },
  async mounted() {
    await this.initializeUser()
    await this.loadConversations()
    this.handleRouteQuery()
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
          this.conversations = response.data.conversations
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

    async loadMessages(partnerId, silent = false) {
      if (!partnerId) return

      try {
        // Only show loading indicator if not in silent mode (during polling)
        if (!silent) {
          this.messagesLoading = true
        }
        
        const token = localStorage.getItem('access_token') || localStorage.getItem('token')
        
        const response = await axios.get(`http://localhost:5000/api/messages/conversation/${partnerId}`, {
          headers: { 'Authorization': `Bearer ${token}` }
        })

        if (response.data.success) {
          const previousMessageCount = this.messages.length
          this.messages = response.data.messages
          this.selectedPartnerName = response.data.partner.username
          this.selectedPartnerRole = response.data.partner.role
          
          // Only scroll to bottom if we're not polling or if there are new messages
          if (!silent || this.messages.length > previousMessageCount) {
            this.$nextTick(() => {
              this.scrollToBottom()
            })
          }

          // Mark as read (but only if not silent mode to avoid excessive API calls)
          if (!silent) {
            await this.markMessagesAsRead(partnerId)
          }
        }
      } catch (error) {
        console.error('Error loading messages:', error)
        if (error.response?.status === 401) {
          this.$router.push('/login')
        }
      } finally {
        if (!silent) {
          this.messagesLoading = false
        }
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

    handleRouteQuery() {
      // Handle navigation from Orders page
      const sellerId = this.$route.query.sellerId
      const sellerName = this.$route.query.sellerName
      
      if (sellerId) {
        this.selectedPartnerId = parseInt(sellerId)
        
        // Check if conversation exists
        let conversation = this.conversations.find(c => c.partner_id === this.selectedPartnerId)
        
        if (!conversation && sellerName) {
          // Create a temporary conversation object for UI
          conversation = {
            partner_id: this.selectedPartnerId,
            partner_username: sellerName,
            partner_role: 'seller',
            last_message: '',
            last_message_time: new Date().toISOString(),
            unread_count: 0,
            is_last_message_mine: false
          }
          this.conversations.unshift(conversation)
        }
        
        if (conversation) {
          this.selectConversation(conversation)
        }
      }
    },

    calculateUnreadCount() {
      this.totalUnreadCount = this.conversations.reduce((total, conv) => total + conv.unread_count, 0)
    },

    startPolling() {
      // Simple AJAX polling for messages every 10 seconds (reduced frequency to avoid UI issues)
      this.pollingInterval = setInterval(async () => {
        if (this.selectedPartnerId && !this.messagesLoading) {
          try {
            // Use silent mode to avoid UI flickering during polling
            await this.loadMessages(this.selectedPartnerId, true)
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
    },

    async loadSellers() {
      try {
        this.loadingSellers = true
        const token = localStorage.getItem('access_token') || localStorage.getItem('token')
        
        const response = await axios.get('http://localhost:5000/api/messages/sellers', {
          headers: { 'Authorization': `Bearer ${token}` }
        })

        if (response.data.success) {
          this.sellers = response.data.sellers
        }
      } catch (error) {
        console.error('Error loading sellers:', error)
        this.errorMessage = 'Failed to load sellers'
      } finally {
        this.loadingSellers = false
      }
    },

    async startConversationWithSeller(seller) {
      if (seller.has_conversation) {
        // If conversation exists, find and select it
        const existingConversation = this.conversations.find(conv => 
          conv.partner_id === seller.id && conv.partner_role === 'seller'
        )
        if (existingConversation) {
          this.selectConversation(existingConversation)
          this.showSellersModal = false
        }
      } else {
        // Start new conversation
        this.selectedSellerForConversation = seller
        this.showSellersModal = false
        this.showStartConversationModal = true
      }
    },

    async sendInitialMessage() {
      if (!this.initialMessage.trim() || !this.selectedSellerForConversation || this.startingConversation) return

      try {
        this.startingConversation = true
        const token = localStorage.getItem('access_token') || localStorage.getItem('token')
        
        const response = await axios.post('http://localhost:5000/api/messages/start-conversation', {
          seller_id: this.selectedSellerForConversation.id,
          message: this.initialMessage.trim()
        }, {
          headers: { 'Authorization': `Bearer ${token}` }
        })

        if (response.data.success) {
          this.closeStartConversationModal()
          // Refresh conversations and select the new one
          await this.loadConversations()
          const newConversation = this.conversations.find(conv => 
            conv.partner_id === this.selectedSellerForConversation.id
          )
          if (newConversation) {
            this.selectConversation(newConversation)
          }
        }
      } catch (error) {
        console.error('Error starting conversation:', error)
        this.errorMessage = 'Failed to start conversation. Please try again.'
      } finally {
        this.startingConversation = false
      }
    },

    closeStartConversationModal() {
      this.showStartConversationModal = false
      this.selectedSellerForConversation = null
      this.initialMessage = ''
    },

    async openSellersModal() {
      this.showSellersModal = true
      await this.loadSellers()
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400;1,500;1,600;1,700;1,800&family=Inter:wght@300;400;500;600;700&display=swap');

.page-title {

  font-weight: 700;
  font-size: 2.5rem;
  letter-spacing: -1px;
  color: #1f2937;
}

h3 {

  font-weight: 600;
  font-size: 1.25rem;
  letter-spacing: -0.5px;
  color: #1f2937;
}

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

.unread-count {
  background: #ef4444;
  color: white;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
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
}

.conversation-item:hover {
  background: #f9fafb;
}

.conversation-item.active {
  background: #eff6ff;
  border-right: 3px solid #3b82f6;
}

.conversation-avatar {
  position: relative;
  margin-right: 12px;
}

.avatar-circle {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #000000;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
}

.avatar-circle.seller {
  background: linear-gradient(135deg, #b05151 0%, #b05151 100%);
}

.avatar-circle.admin {
  background: linear-gradient(135deg, #4e62b0 0%, #4e62b0 100%);
}

.avatar-circle.user {
  background: linear-gradient(135deg, #000000 0%, #000000 100%);
}

.role-badge {
  position: absolute;
  bottom: -6px;
  left: 50%;
  transform: translateX(-50%);
  background: #000000;
  color: white;
  font-size: 7px;
  padding: 2px 6px;
  border-radius: 8px;
  text-transform: uppercase;
  font-weight: 600;
  white-space: nowrap;
}

.role-badge.seller {
  background: #f59e0b;
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
  color: #000000;
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

/* Chat Panel */
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
  background: #000000;
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
  margin-bottom: 16px;
}

.message-item.own-message {
  align-self: flex-end;
  margin-left: auto;
  margin-right: 0;
}

.message-item:not(.own-message) {
  align-self: flex-start;
  margin-left: 0;
  margin-right: auto;
}

.message-content {
  background: #f3f4f6;
  padding: 12px 16px;
  border-radius: 18px;
  max-width: 100%;
}

.own-message .message-content {
  background: #3b82f6;
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
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.send-btn {
  width: 44px;
  height: 44px;
  border: none;
  border-radius: 50%;
  background: #3b82f6;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.send-btn:hover:not(:disabled) {
  background: #2563eb;
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
}

/* Header Styles */
.messages-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
  font-size: 14px;
}

.action-btn.primary {
  background: #3b82f6;
  color: white;
}

.action-btn.primary:hover {
  background: #2563eb;
}

.action-btn.secondary {
  background: #f3f4f6;
  color: #374151;
  border: 1px solid #d1d5db;
}

.action-btn.secondary:hover {
  background: #e5e7eb;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 12px;
  max-width: 500px;
  width: 90%;
  max-height: 80vh;
  overflow: hidden;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
}

.modal-header {
  padding: 20px;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #111827;
}

.close-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: #6b7280;
  padding: 4px;
  border-radius: 4px;
  transition: all 0.2s;
}

.close-btn:hover {
  color: #374151;
  background: #f3f4f6;
}

.modal-body {
  padding: 20px;
  max-height: 60vh;
  overflow-y: auto;
}

/* Sellers List Styles */
.loading-sellers {
  text-align: center;
  padding: 40px;
  color: #6b7280;
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

.sellers-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.seller-item {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.seller-item:hover {
  background: #f9fafb;
  border-color: #3b82f6;
}

.seller-item.has-conversation {
  background: #eff6ff;
  border-color: #3b82f6;
}

.seller-avatar {
  width: 40px;
  height: 40px;
  background: #000000;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  margin-right: 12px;
}

.seller-info {
  flex: 1;
}

.seller-name {
  font-weight: 600;
  color: #111827;
  margin-bottom: 4px;
}

.seller-status {
  font-size: 12px;
  color: #6b7280;
}

.seller-status .existing {
  color: #3b82f6;
}

.seller-status .new {
  color: #059669;
}

.seller-action {
  color: #3b82f6;
}

.no-sellers {
  text-align: center;
  color: #6b7280;
  padding: 40px;
}

/* Start Conversation Form */
.start-conversation-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-weight: 500;
  color: #374151;
}

.initial-message-textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 14px;
  font-family: inherit;
  resize: vertical;
  min-height: 100px;
}

.initial-message-textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.btn {
  padding: 10px 16px;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
  font-size: 14px;
}

.btn.primary {
  background: #3b82f6;
  color: white;
}

.btn.primary:hover:not(:disabled) {
  background: #2563eb;
}

.btn.primary:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

.btn.secondary {
  background: #f3f4f6;
  color: #374151;
  border: 1px solid #d1d5db;
}

.btn.secondary:hover {
  background: #e5e7eb;
}
</style>
