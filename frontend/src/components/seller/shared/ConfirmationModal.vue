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
  z-index: 1060;
  padding: 20px;
}

.confirmation-modal {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  max-width: 400px;
  width: 100%;
  animation: modalSlideIn 0.3s ease;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px 0;
}

.modal-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #343a40;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #6c757d;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
}

.close-btn:hover {
  background: #f8f9fa;
  color: #343a40;
}

.modal-body {
  padding: 24px;
  text-align: center;
}

.icon-container {
  margin-bottom: 16px;
}

.confirmation-icon {
  font-size: 48px;
  display: block;
}

.icon-warning {
  color: #ffc107;
}

.icon-danger {
  color: #dc3545;
}

.icon-info {
  color: #17a2b8;
}

.icon-success {
  color: #28a745;
}

.message {
  font-size: 16px;
  color: #495057;
  line-height: 1.5;
  margin: 0;
}

.modal-footer {
  display: flex;
  gap: 12px;
  padding: 0 24px 24px;
  justify-content: flex-end;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 80px;
  min-height: 40px;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-cancel {
  background: #6c757d;
  color: white;
}

.btn-cancel:hover:not(:disabled) {
  background: #545b62;
}

.btn-confirm {
  color: white;
}

.btn-warning {
  background: #ffc107;
  color: #212529;
}

.btn-warning:hover:not(:disabled) {
  background: #e0a800;
}

.btn-danger {
  background: #dc3545;
}

.btn-danger:hover:not(:disabled) {
  background: #c82333;
}

.btn-info {
  background: #17a2b8;
}

.btn-info:hover:not(:disabled) {
  background: #138496;
}

.btn-success {
  background: #28a745;
}

.btn-success:hover:not(:disabled) {
  background: #1e7e34;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid transparent;
  border-top: 2px solid currentColor;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: scale(0.9) translateY(-20px);
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
