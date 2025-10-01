<template>
  <UserLayout>
    <div class="live-streaming-page">
      <div class="live-container">
        <!-- Main Video Area -->
        <div class="video-section">
          <div class="video-player">
            <div class="video-content">
              <!-- Live Video Background -->
              <div class="video-background">
                <div class="stream-video-placeholder">
                  <div class="video-placeholder-content">
                    <div class="play-icon">▶</div>
                    <p>Live Stream</p>
                  </div>
                </div>
                <!-- Live Indicator -->
                <div class="live-indicator">
                  <span class="live-dot"></span>
                  <span class="live-text">LIVE</span>
                </div>
                
                <!-- Stream Title Overlay -->
                <div class="stream-overlay">
                  <h2 class="stream-title">Luxury Livesale! SALE! SALE! SALE!</h2>
                </div>
              </div>
            </div>
            
            <!-- Stream Info Bar -->
            <div class="stream-info">
              <div class="streamer-info">
                <div class="streamer-avatar">
                  <div class="avatar-placeholder">LS</div>
                </div>
                <div class="streamer-details">
                  <h3 class="streamer-name">LemyShop</h3>
                  <div class="stream-stats">
                    <span class="viewers">🔴 3.1K watching</span>
                    <span class="rating">⭐ 4.8</span>
                  </div>
                </div>
              </div>
              
              <div class="action-buttons">
                <button class="follow-btn">+ Follow</button>
                <button class="share-btn">Share</button>
              </div>
            </div>
          </div>
        </div>

        <!-- Chat and Interaction Section -->
        <div class="chat-section">
          <div class="chat-container">
            <!-- Chat Header -->
            <div class="chat-header">
              <h3>Live Chat</h3>
              <div class="chat-stats">
                <span>3,142 viewers</span>
              </div>
            </div>

            <!-- Chat Messages -->
            <div class="chat-messages">
              <div class="chat-message">
                <div class="user-avatar">
                  <div class="user-avatar-placeholder">J</div>
                </div>
                <div class="message-content">
                  <span class="username">jeff123</span>
                  <span class="message-text">nice items</span>
                  <div class="message-actions">
                    <button class="reply-btn">Reply</button>
                    <button class="heart-btn">♥ 1 reply</button>
                  </div>
                </div>
              </div>

              <div class="chat-message">
                <div class="user-avatar">
                  <div class="user-avatar-placeholder">J</div>
                </div>
                <div class="message-content">
                  <span class="username">jeff123</span>
                  <span class="message-text">hi nice colection</span>
                  <div class="message-actions">
                    <button class="reply-btn">Reply</button>
                    <button class="heart-btn">♥ 1 reply</button>
                  </div>
                </div>
              </div>

              <div class="chat-message">
                <div class="user-avatar">
                  <div class="user-avatar-placeholder">J</div>
                </div>
                <div class="message-content">
                  <span class="username">jeff123</span>
                  <span class="message-text">niceeeeeeeeee</span>
                  <div class="message-actions">
                    <button class="reply-btn">Reply</button>
                    <button class="heart-btn">♥ 1 reply</button>
                  </div>
                </div>
              </div>

              <div class="chat-message">
                <div class="user-avatar">
                  <div class="user-avatar-placeholder">J</div>
                </div>
                <div class="message-content">
                  <span class="username">jeff123</span>
                  <span class="message-text">wohooooooo</span>
                  <div class="message-actions">
                    <button class="reply-btn">Reply</button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Chat Input -->
            <div class="chat-input-section">
              <div class="chat-input-container">
                <input 
                  type="text" 
                  placeholder="Add a comment..." 
                  class="chat-input"
                  v-model="newMessage"
                  @keyup.enter="sendMessage"
                />
                <button class="send-btn" @click="sendMessage">Send</button>
              </div>
            </div>
          </div>
        </div>

        <!-- Live Viewers Sidebar -->
        <div class="viewers-sidebar">
          <div class="sidebar-header">
            <h4>Live Users</h4>
            <span class="viewer-count">{{ liveViewers.length }}</span>
          </div>
          
          <div class="viewers-list">
            <div 
              v-for="viewer in liveViewers" 
              :key="viewer.id"
              class="viewer-item"
            >
              <div class="viewer-avatar">
                <div class="viewer-avatar-placeholder">{{ viewer.name.charAt(0) }}</div>
                <div class="live-status"></div>
              </div>
              <div class="viewer-info">
                <span class="viewer-name">{{ viewer.name }}</span>
                <span class="viewer-status">{{ viewer.status }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </UserLayout>
</template>

<script>
import UserLayout from '@/components/user/UserLayout.vue'

export default {
  name: 'LiveStreaming',
  components: {
    UserLayout
  },
  data() {
    return {
      newMessage: '',
      chatMessages: [
        {
          id: 1,
          username: 'jeff123',
          message: 'nice items',
          timestamp: new Date(),
          avatar: 'placeholder'
        }
      ],
      liveViewers: [
        {
          id: 1,
          name: 'LIVE NOW',
          status: 'VINTAGE UPDATES',
          avatar: 'placeholder'
        },
        {
          id: 2,
          name: 'LIVE NOW',
          status: 'VINTAGE UPDATES',
          avatar: 'placeholder'
        },
        {
          id: 3,
          name: 'LIVE NOW',
          status: 'VINTAGE UPDATES',
          avatar: 'placeholder'
        },
        {
          id: 4,
          name: 'LIVE NOW',
          status: 'VINTAGE UPDATES',
          avatar: 'placeholder'
        }
      ]
    }
  },
  methods: {
    sendMessage() {
      if (this.newMessage.trim()) {
        this.chatMessages.push({
          id: Date.now(),
          username: 'You',
          message: this.newMessage,
          timestamp: new Date(),
          avatar: 'placeholder'
        })
        this.newMessage = ''
      }
    }
  },
  mounted() {
    // Simulate live chat updates
    setInterval(() => {
      const messages = [
        'Amazing collection!',
        'How much for this?',
        'Beautiful items',
        'Love this stream!',
        'Where can I buy?'
      ]
      
      if (Math.random() > 0.7) {
        this.chatMessages.push({
          id: Date.now(),
          username: `user${Math.floor(Math.random() * 1000)}`,
          message: messages[Math.floor(Math.random() * messages.length)],
          timestamp: new Date(),
          avatar: 'placeholder'
        })
        
        // Keep only last 10 messages
        if (this.chatMessages.length > 10) {
          this.chatMessages = this.chatMessages.slice(-10)
        }
      }
    }, 3000)
  }
}
</script>

<style scoped>
.live-streaming-page {
  background: #f8f9fa;
  min-height: 100vh;
  padding: 20px;
}

.live-container {
  display: grid;
  grid-template-columns: 1fr 350px 250px;
  gap: 20px;
  max-width: 1400px;
  margin: 0 auto;
}

/* Video Section */
.video-section {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.video-player {
  position: relative;
}

.video-content {
  position: relative;
  width: 100%;
  height: 450px;
  background: #000;
}

.video-background {
  position: relative;
  width: 100%;
  height: 100%;
}

.stream-video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Video Placeholder */
.stream-video-placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(45deg, #333, #555);
  display: flex;
  align-items: center;
  justify-content: center;
}

.video-placeholder-content {
  text-align: center;
  color: white;
}

.play-icon {
  font-size: 48px;
  margin-bottom: 10px;
  opacity: 0.8;
}

.video-placeholder-content p {
  font-size: 18px;
  margin: 0;
  opacity: 0.8;
}

/* Avatar Placeholders */
.avatar-placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(45deg, #8B4513, #A0522D);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: 16px;
}

.user-avatar-placeholder {
  width: 24px;
  height: 24px;
  background: linear-gradient(45deg, #007bff, #0056b3);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: 10px;
}

.viewer-avatar-placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(45deg, #28a745, #20c997);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: 12px;
}

.live-indicator {
  position: absolute;
  top: 15px;
  left: 15px;
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(255, 0, 0, 0.9);
  color: white;
  padding: 6px 12px;
  border-radius: 20px;
  font-weight: bold;
  font-size: 12px;
}

.live-dot {
  width: 8px;
  height: 8px;
  background: white;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.stream-overlay {
  position: absolute;
  bottom: 20px;
  left: 20px;
  right: 20px;
}

.stream-title {
  color: white;
  font-size: 24px;
  font-weight: bold;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
  margin: 0;
}

.stream-info {
  padding: 15px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: white;
  border-top: 1px solid #eee;
}

.streamer-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.streamer-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  overflow: hidden;
}

.streamer-name {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 4px 0;
  color: #333;
}

.stream-stats {
  display: flex;
  gap: 15px;
  font-size: 12px;
  color: #666;
}

.action-buttons {
  display: flex;
  gap: 10px;
}

.follow-btn, .share-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.follow-btn {
  background: #007bff;
  color: white;
}

.share-btn {
  background: #f8f9fa;
  color: #333;
  border: 1px solid #ddd;
}

.follow-btn:hover {
  background: #0056b3;
}

.share-btn:hover {
  background: #e9ecef;
}

/* Chat Section */
.chat-section {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  height: fit-content;
}

.chat-header {
  padding: 15px 20px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chat-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
}

.chat-stats {
  font-size: 12px;
  color: #666;
}

.chat-messages {
  padding: 15px 20px;
  max-height: 400px;
  overflow-y: auto;
  flex-grow: 1;
}

.chat-message {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
}

.user-avatar {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
}

.message-content {
  flex-grow: 1;
}

.username {
  font-weight: 600;
  font-size: 12px;
  color: #333;
  margin-right: 8px;
}

.message-text {
  font-size: 14px;
  color: #333;
}

.message-actions {
  margin-top: 4px;
  display: flex;
  gap: 10px;
}

.reply-btn, .heart-btn {
  background: none;
  border: none;
  font-size: 11px;
  color: #666;
  cursor: pointer;
  padding: 0;
}

.reply-btn:hover, .heart-btn:hover {
  color: #007bff;
}

.chat-input-section {
  padding: 15px 20px;
  border-top: 1px solid #eee;
}

.chat-input-container {
  display: flex;
  gap: 10px;
}

.chat-input {
  flex-grow: 1;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 20px;
  font-size: 14px;
  outline: none;
}

.chat-input:focus {
  border-color: #007bff;
}

.send-btn {
  padding: 8px 16px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 20px;
  font-size: 14px;
  cursor: pointer;
}

.send-btn:hover {
  background: #0056b3;
}

/* Viewers Sidebar */
.viewers-sidebar {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  height: fit-content;
}

.sidebar-header {
  padding: 15px 20px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.sidebar-header h4 {
  margin: 0;
  font-size: 14px;
  font-weight: 600;
}

.viewer-count {
  background: #007bff;
  color: white;
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 11px;
  font-weight: 600;
}

.viewers-list {
  padding: 15px 20px;
}

.viewer-item {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
}

.viewer-avatar {
  position: relative;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  overflow: hidden;
}

.live-status {
  position: absolute;
  bottom: -2px;
  right: -2px;
  width: 10px;
  height: 10px;
  background: #28a745;
  border: 2px solid white;
  border-radius: 50%;
}

.viewer-info {
  flex-grow: 1;
}

.viewer-name {
  display: block;
  font-size: 12px;
  font-weight: 600;
  color: #333;
}

.viewer-status {
  display: block;
  font-size: 10px;
  color: #666;
  text-transform: uppercase;
}

/* Responsive Design */
@media (max-width: 1200px) {
  .live-container {
    grid-template-columns: 1fr 300px;
    grid-template-rows: auto auto;
  }
  
  .viewers-sidebar {
    grid-column: 1 / -1;
    grid-row: 2;
  }
  
  .viewers-list {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 10px;
  }
}

@media (max-width: 768px) {
  .live-container {
    grid-template-columns: 1fr;
    gap: 15px;
  }
  
  .video-content {
    height: 300px;
  }
  
  .stream-title {
    font-size: 18px;
  }
  
  .stream-info {
    flex-direction: column;
    gap: 10px;
    align-items: flex-start;
  }
}
</style>