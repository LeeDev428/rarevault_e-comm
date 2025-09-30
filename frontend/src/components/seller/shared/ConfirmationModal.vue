<template>
  <teleport to="body">
    <div v-if="show" class="modal-overlay" @click="handleOverlayClick">
      <div class="confirmation-modal" @click.stop>
        <div class="modal-header">
          <h3 class="modal-title">{{ title }}</h3>
          <button class="close-btn" @click="$emit('cancel')">×</button>
        </div>
        
        <div class="modal-body">
          <div class="icon-container">
            <i class="confirmation-icon" :class="iconClass">{{ icon }}</i>
          </div>
          <p class="message">{{ message }}</p>
        </div>
        
        <div class="modal-footer">
          <button 
            class="btn btn-cancel" 
            @click="$emit('cancel')"
            :disabled="loading"
          >
            {{ cancelText }}
          </button>
          <button 
            class="btn btn-confirm" 
            :class="confirmButtonClass"
            @click="$emit('confirm')"
            :disabled="loading"
          >
            <div v-if="loading" class="spinner"></div>
            <span v-else>{{ confirmText }}</span>
          </button>
        </div>
      </div>
    </div>
  </teleport>
</template>

<script>
export default {
  name: 'ConfirmationModal',
  props: {
    show: {
      type: Boolean,
      default: false
    },
    title: {
      type: String,
      default: 'Confirm Action'
    },
    message: {
      type: String,
      required: true
    },
    type: {
      type: String,
      default: 'warning',
      validator: value => ['warning', 'danger', 'info', 'success'].includes(value)
    },
    confirmText: {
      type: String,
      default: 'Confirm'
    },
    cancelText: {
      type: String,
      default: 'Cancel'
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  emits: ['confirm', 'cancel'],
  computed: {
    icon() {
      const icons = {
        warning: '⚠️',
        danger: '🗑️',
        info: 'ℹ️',
        success: '✅'
      };
      return icons[this.type] || icons.warning;
    },
    iconClass() {
      return `icon-${this.type}`;
    },
    confirmButtonClass() {
      const classes = {
        warning: 'btn-warning',
        danger: 'btn-danger',
        info: 'btn-info',
        success: 'btn-success'
      };
      return classes[this.type] || classes.warning;
    }
  },
  methods: {
    handleOverlayClick() {
      if (!this.loading) {
        this.$emit('cancel');
      }
    }
  },
  mounted() {
    // Prevent body scroll when modal is open
    if (this.show) {
      document.body.style.overflow = 'hidden';
    }
  },
  beforeUnmount() {
    // Restore body scroll
    document.body.style.overflow = '';
  },
  watch: {
    show(newVal) {
      if (newVal) {
        document.body.style.overflow = 'hidden';
      } else {
        document.body.style.overflow = '';
      }
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(139, 90, 60, 0.3);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1060;
  padding: 20px;
}

.confirmation-modal {
  background: linear-gradient(135deg, #ffffff 0%, #fefdfb 100%);
  border-radius: 24px;
  box-shadow: 0 20px 60px rgba(139, 90, 60, 0.25);
  max-width: 480px;
  width: 100%;
  animation: modalSlideIn 0.4s ease;
  border: 2px solid #f5f1eb;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 32px 32px 0;
}

.modal-title {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  color: #5a4a3a;
  font-family: 'Playfair Display', serif;
}

.close-btn {
  background: linear-gradient(135deg, #f8f6f1 0%, #f0ede6 100%);
  border: 2px solid #e8ddd4;
  font-size: 24px;
  cursor: pointer;
  color: #a0958a;
  padding: 8px;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.close-btn:hover {
  background: linear-gradient(135deg, #f0ede6 0%, #e8ddd4 100%);
  color: #8b7968;
  border-color: #d4af94;
}

.modal-body {
  padding: 32px;
  text-align: center;
}

.icon-container {
  margin-bottom: 24px;
}

.confirmation-icon {
  font-size: 64px;
  display: block;
}

.icon-warning {
  color: #d4af94;
}

.icon-danger {
  color: #b8936f;
}

.icon-info {
  color: #8b5a3c;
}

.icon-success {
  color: #8b5a3c;
}

.message {
  font-size: 18px;
  color: #5a4a3a;
  line-height: 1.6;
  margin: 0;
  font-family: 'Inter', sans-serif;
}

.modal-footer {
  display: flex;
  gap: 16px;
  padding: 0 32px 32px;
  justify-content: flex-end;
}

.btn {
  padding: 14px 28px;
  border: 2px solid transparent;
  border-radius: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 100px;
  min-height: 48px;
  font-size: 15px;
  font-family: 'Inter', sans-serif;
  box-shadow: 0 4px 16px rgba(139, 90, 60, 0.1);
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-cancel {
  background: linear-gradient(135deg, #f8f6f1 0%, #f0ede6 100%);
  color: #8b7968;
  border-color: #e8ddd4;
}

.btn-cancel:hover:not(:disabled) {
  background: linear-gradient(135deg, #f0ede6 0%, #e8ddd4 100%);
  border-color: #d4af94;
  color: #5a4a3a;
}

.btn-confirm {
  color: white;
}

.btn-warning {
  background: linear-gradient(135deg, #e8ddd4 0%, #d4af94 100%);
  border-color: #e8ddd4;
  color: #5a4a3a;
}

.btn-warning:hover:not(:disabled) {
  background: linear-gradient(135deg, #d4af94 0%, #b8936f 100%);
  border-color: #d4af94;
  color: white;
}

.btn-danger {
  background: linear-gradient(135deg, #d4af94 0%, #b8936f 100%);
  border-color: #d4af94;
}

.btn-danger:hover:not(:disabled) {
  background: linear-gradient(135deg, #b8936f 0%, #9c7a5a 100%);
  border-color: #b8936f;
}

.btn-info {
  background: linear-gradient(135deg, #8b5a3c 0%, #6d4528 100%);
  border-color: #8b5a3c;
}

.btn-info:hover:not(:disabled) {
  background: linear-gradient(135deg, #6d4528 0%, #5a3621 100%);
  border-color: #6d4528;
}

.btn-success {
  background: linear-gradient(135deg, #8b5a3c 0%, #6d4528 100%);
  border-color: #8b5a3c;
}

.btn-success:hover:not(:disabled) {
  background: linear-gradient(135deg, #6d4528 0%, #5a3621 100%);
  border-color: #6d4528;
}

.spinner {
  width: 18px;
  height: 18px;
  border: 2px solid transparent;
  border-top: 2px solid currentColor;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: scale(0.9) translateY(-30px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
