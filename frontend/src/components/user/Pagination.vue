<template>
  <div v-if="totalPages > 1" class="pagination-container">
    <!-- Previous Button -->
    <button 
      @click="goToPage(currentPage - 1)"
      :disabled="!hasPrevious"
      class="pagination-btn"
      :class="{ disabled: !hasPrevious }"
    >
      <span class="btn-icon">←</span>
      <span class="btn-text">Previous</span>
    </button>

    <!-- Page Numbers -->
    <div class="page-numbers">
      <!-- First page -->
      <button
        v-if="showFirstPage"
        @click="goToPage(1)"
        class="page-btn"
        :class="{ active: currentPage === 1 }"
      >
        1
      </button>

      <!-- First ellipsis -->
      <span v-if="showFirstEllipsis" class="ellipsis">...</span>

      <!-- Visible page range -->
      <button
        v-for="page in visiblePages"
        :key="page"
        @click="goToPage(page)"
        class="page-btn"
        :class="{ active: currentPage === page }"
      >
        {{ page }}
      </button>

      <!-- Last ellipsis -->
      <span v-if="showLastEllipsis" class="ellipsis">...</span>

      <!-- Last page -->
      <button
        v-if="showLastPage"
        @click="goToPage(totalPages)"
        class="page-btn"
        :class="{ active: currentPage === totalPages }"
      >
        {{ totalPages }}
      </button>
    </div>

    <!-- Next Button -->
    <button 
      @click="goToPage(currentPage + 1)"
      :disabled="!hasNext"
      class="pagination-btn"
      :class="{ disabled: !hasNext }"
    >
      <span class="btn-text">Next</span>
      <span class="btn-icon">→</span>
    </button>

    <!-- Page Info -->
    <div class="page-info">
      <span class="page-info-text">
        Page {{ currentPage }} of {{ totalPages }}
        <span v-if="totalItems" class="total-items">
          ({{ totalItems }} total {{ itemLabel }})
        </span>
      </span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Pagination',
  props: {
    currentPage: {
      type: Number,
      required: true,
      default: 1
    },
    totalPages: {
      type: Number,
      required: true,
      default: 1
    },
    totalItems: {
      type: Number,
      default: null
    },
    hasPrevious: {
      type: Boolean,
      default: false
    },
    hasNext: {
      type: Boolean,
      default: false
    },
    itemLabel: {
      type: String,
      default: 'items'
    },
    maxVisiblePages: {
      type: Number,
      default: 5
    }
  },
  computed: {
    visiblePages() {
      const pages = [];
      const half = Math.floor(this.maxVisiblePages / 2);
      let start = Math.max(1, this.currentPage - half);
      let end = Math.min(this.totalPages, start + this.maxVisiblePages - 1);
      
      // Adjust start if we're near the end
      if (end - start + 1 < this.maxVisiblePages) {
        start = Math.max(1, end - this.maxVisiblePages + 1);
      }
      
      for (let i = start; i <= end; i++) {
        // Only show pages that aren't already shown as first/last
        if (!this.showFirstPage || i !== 1) {
          if (!this.showLastPage || i !== this.totalPages) {
            pages.push(i);
          }
        }
      }
      
      return pages;
    },
    
    showFirstPage() {
      return this.totalPages > this.maxVisiblePages && this.currentPage > Math.ceil(this.maxVisiblePages / 2) + 1;
    },
    
    showLastPage() {
      return this.totalPages > this.maxVisiblePages && this.currentPage < this.totalPages - Math.ceil(this.maxVisiblePages / 2);
    },
    
    showFirstEllipsis() {
      return this.showFirstPage && this.visiblePages.length > 0 && this.visiblePages[0] > 2;
    },
    
    showLastEllipsis() {
      return this.showLastPage && this.visiblePages.length > 0 && this.visiblePages[this.visiblePages.length - 1] < this.totalPages - 1;
    }
  },
  methods: {
    goToPage(page) {
      if (page >= 1 && page <= this.totalPages && page !== this.currentPage) {
        this.$emit('page-changed', page);
      }
    }
  }
}
</script>

<style scoped>
.pagination-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin: 32px 0;
  flex-wrap: wrap;
}

/* Pagination Buttons */
.pagination-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 16px;
  border: 1px solid #ddd;
  background: white;
  color: #333;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.2s ease;
  min-width: 100px;
  justify-content: center;
}

.pagination-btn:hover:not(.disabled) {
  background: #f8f9fa;
  border-color: #007bff;
  color: #007bff;
}

.pagination-btn.disabled {
  background: #f8f9fa;
  color: #6c757d;
  border-color: #dee2e6;
  cursor: not-allowed;
  opacity: 0.6;
}

.btn-icon {
  font-size: 0.8rem;
  font-weight: bold;
}

.btn-text {
  font-size: 0.9rem;
}

/* Page Numbers */
.page-numbers {
  display: flex;
  align-items: center;
  gap: 4px;
}

.page-btn {
  width: 40px;
  height: 40px;
  border: 1px solid #ddd;
  background: white;
  color: #333;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.page-btn:hover {
  background: #f8f9fa;
  border-color: #007bff;
  color: #007bff;
}

.page-btn.active {
  background: #007bff;
  border-color: #007bff;
  color: white;
  font-weight: 600;
}

.page-btn.active:hover {
  background: #0056b3;
  border-color: #0056b3;
}

/* Ellipsis */
.ellipsis {
  padding: 0 8px;
  color: #6c757d;
  font-weight: 500;
  display: flex;
  align-items: center;
}

/* Page Info */
.page-info {
  margin-left: 16px;
  color: #6c757d;
  font-size: 0.9rem;
}

.page-info-text {
  font-weight: 500;
}

.total-items {
  color: #999;
  font-weight: 400;
}

/* Mobile Responsive */
@media (max-width: 768px) {
  .pagination-container {
    gap: 8px;
    margin: 24px 0;
  }
  
  .pagination-btn {
    min-width: 80px;
    padding: 8px 12px;
    font-size: 0.8rem;
  }
  
  .btn-text {
    display: none;
  }
  
  .page-btn {
    width: 36px;
    height: 36px;
    font-size: 0.8rem;
  }
  
  .page-info {
    width: 100%;
    text-align: center;
    margin-left: 0;
    margin-top: 8px;
    font-size: 0.8rem;
  }
}

@media (max-width: 480px) {
  .page-numbers {
    gap: 2px;
  }
  
  .page-btn {
    width: 32px;
    height: 32px;
    font-size: 0.75rem;
  }
  
  .pagination-btn {
    min-width: 60px;
    padding: 6px 10px;
  }
}
</style>
