<template>
  <teleport to="body">
    <transition name="message-fade" appear>
      <div 
        v-if="show" 
        class="message-toast"
        :class="[`message-toast--${type}`, { 'message-toast--auto-dismiss': autoDismiss }]"
      >
        <div class="message-content">
          <i class="message-icon">{{ icon }}</i>
          <div class="message-text">
            <h4 v-if="title" class="message-title">{{ title }}</h4>
            <p class="message-description">{{ message }}</p>
          </div>
          <button 
            v-if="dismissible" 
            class="message-close"
            @click="$emit('close')"
          >
            ×
          </button>
        </div>
        
        <div 
          v-if="autoDismiss && showProgress" 
          class="progress-bar"
          :style="{ animationDuration: `${duration}ms` }"
        ></div>
      </div>
    </transition>
  </teleport>
</template>

<script>
export default {
  name: 'MessageToast',
  props: {
    show: {
      type: Boolean,
      default: false
    },
    type: {
      type: String,
      default: 'info',
      validator: value => ['success', 'error', 'warning', 'info'].includes(value)
    },
    title: {
      type: String,
      default: ''
    },
    message: {
      type: String,
      required: true
    },
    autoDismiss: {
      type: Boolean,
      default: true
    },
    duration: {
      type: Number,
      default: 5000
    },
    dismissible: {
      type: Boolean,
      default: true
    },
    showProgress: {
      type: Boolean,
      default: true
    }
  },
  emits: ['close'],
  computed: {
    icon() {
      const icons = {
        success: '✅',
        error: '❌', 
        warning: '⚠️',
        info: 'ℹ️'
      };
      return icons[this.type] || icons.info;
    }
  },
  mounted() {
    if (this.autoDismiss && this.show) {
      setTimeout(() => {
        this.$emit('close');
      }, this.duration);
    }
  },
  watch: {
    show(newVal) {
      if (newVal && this.autoDismiss) {
        setTimeout(() => {
          this.$emit('close');
        }, this.duration);
      }
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');

.message-toast {
  position: fixed;
  top: 90px;
  right: 32px;
  z-index: 1070;
  max-width: 420px;
  min-width: 350px;
  background: linear-gradient(135deg, #ffffff 0%, #fefdfb 100%);
  border-radius: 20px;
  box-shadow: 0 12px 40px rgba(139, 90, 60, 0.2);
  overflow: hidden;
  border-left: 6px solid;
  border: 2px solid #f5f1eb;
}

.message-toast--success {
  border-left-color: #8b5a3c;
}

.message-toast--error {
  border-left-color: #d4af94;
}

.message-toast--warning {
  border-left-color: #e8ddd4;
}

.message-toast--info {
  border-left-color: #b8936f;
}

.message-content {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 24px;
}

.message-icon {
  font-size: 24px;
  line-height: 1;
  margin-top: 2px;
  flex-shrink: 0;
}

.message-text {
  flex: 1;
}

.message-title {
  margin: 0 0 8px 0;
  font-size: 18px;
  font-weight: 600;
  color: #5a4a3a;
  line-height: 1.3;
  font-family: 'Playfair Display', serif;
}

.message-description {
  margin: 0;
  font-size: 15px;
  color: #8b7968;
  line-height: 1.5;
  font-family: 'Inter', sans-serif;
}

.message-close {
  background: linear-gradient(135deg, #f8f6f1 0%, #f0ede6 100%);
  border: 2px solid #e8ddd4;
  font-size: 20px;
  cursor: pointer;
  color: #a0958a;
  padding: 6px;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  flex-shrink: 0;
  margin-top: -4px;
  transition: all 0.3s ease;
}

.message-close:hover {
  background: linear-gradient(135deg, #f0ede6 0%, #e8ddd4 100%);
  color: #8b7968;
  border-color: #d4af94;
}

.progress-bar {
  height: 4px;
  background: currentColor;
  opacity: 0.4;
  animation: progressShrink linear;
  transform-origin: right;
}

.message-toast--success .progress-bar {
  background: #8b5a3c;
}

.message-toast--error .progress-bar {
  background: #d4af94;
}

.message-toast--warning .progress-bar {
  background: #e8ddd4;
}

.message-toast--info .progress-bar {
  background: #b8936f;
}

/* Transitions */
.message-fade-enter-active,
.message-fade-leave-active {
  transition: all 0.4s ease;
}

.message-fade-enter-from {
  opacity: 0;
  transform: translateX(100%) scale(0.9);
}

.message-fade-leave-to {
  opacity: 0;
  transform: translateX(100%) scale(0.9);
}

@keyframes progressShrink {
  from {
    transform: scaleX(1);
  }
  to {
    transform: scaleX(0);
  }
}

/* Responsive */
@media (max-width: 480px) {
  .message-toast {
    right: 20px;
    left: 20px;
    max-width: none;
    min-width: auto;
  }
  
  .message-content {
    padding: 20px;
  }
  
  .message-title {
    font-size: 16px;
  }
  
  .message-description {
    font-size: 14px;
  }
}
</style>
