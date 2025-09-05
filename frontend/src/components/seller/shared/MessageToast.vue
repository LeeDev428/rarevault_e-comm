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
.message-toast {
  position: fixed;
  top: 80px;
  right: 24px;
  z-index: 1070;
  max-width: 400px;
  min-width: 300px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
  overflow: hidden;
  border-left: 4px solid;
}

.message-toast--success {
  border-left-color: #28a745;
}

.message-toast--error {
  border-left-color: #dc3545;
}

.message-toast--warning {
  border-left-color: #ffc107;
}

.message-toast--info {
  border-left-color: #17a2b8;
}

.message-content {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px;
}

.message-icon {
  font-size: 20px;
  line-height: 1;
  margin-top: 2px;
  flex-shrink: 0;
}

.message-text {
  flex: 1;
}

.message-title {
  margin: 0 0 4px 0;
  font-size: 16px;
  font-weight: 600;
  color: #343a40;
  line-height: 1.2;
}

.message-description {
  margin: 0;
  font-size: 14px;
  color: #6c757d;
  line-height: 1.4;
}

.message-close {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #6c757d;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  flex-shrink: 0;
  margin-top: -2px;
}

.message-close:hover {
  background: #f8f9fa;
  color: #343a40;
}

.progress-bar {
  height: 3px;
  background: currentColor;
  opacity: 0.3;
  animation: progressShrink linear;
  transform-origin: right;
}

.message-toast--success .progress-bar {
  background: #28a745;
}

.message-toast--error .progress-bar {
  background: #dc3545;
}

.message-toast--warning .progress-bar {
  background: #ffc107;
}

.message-toast--info .progress-bar {
  background: #17a2b8;
}

/* Transitions */
.message-fade-enter-active,
.message-fade-leave-active {
  transition: all 0.3s ease;
}

.message-fade-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.message-fade-leave-to {
  opacity: 0;
  transform: translateX(100%);
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
    right: 16px;
    left: 16px;
    max-width: none;
    min-width: auto;
  }
}
</style>
