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
  </div>

  <!-- Pagination Info -->
  <div v-if="totalItems > 0" class="pagination-info">
    Showing {{ startItem }}-{{ endItem }} of {{ totalItems }} {{ itemLabel }}
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
      required: true,
      default: 0
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
    },
    itemsPerPage: {
      type: Number,
      default: 9
    }
  },
  computed: {
    startItem() {
      return (this.currentPage - 1) * this.itemsPerPage + 1;
    },
    endItem() {
      return Math.min(this.currentPage * this.itemsPerPage, this.totalItems);
    },
    visiblePages() {
      const pages = [];
      let start = Math.max(2, this.currentPage - Math.floor(this.maxVisiblePages / 2));
      let end = Math.min(this.totalPages - 1, start + this.maxVisiblePages - 1);
      
      // Adjust start if we're near the end
      if (end - start + 1 < this.maxVisiblePages) {
        start = Math.max(2, end - this.maxVisiblePages + 1);
      }
      
      for (let i = start; i <= end; i++) {
        if (i > 1 && i < this.totalPages) {
          pages.push(i);
        }
      }
      return pages;
    },
    showFirstPage() {
      return this.totalPages > 1;
    },
    showLastPage() {
      return this.totalPages > 1 && this.currentPage !== this.totalPages;
    },
    showFirstEllipsis() {
      return this.visiblePages.length > 0 && this.visiblePages[0] > 2;
    },
    showLastEllipsis() {
      return this.visiblePages.length > 0 && 
             this.visiblePages[this.visiblePages.length - 1] < this.totalPages - 1;
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
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
  margin: 2rem 0;
  flex-wrap: wrap;
}

.pagination-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  color: #374151;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.pagination-btn:hover:not(.disabled) {
  background: #f3f4f6;
  border-color: #d1d5db;
}

.pagination-btn.disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background: #f9fafb;
}

.page-numbers {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.page-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  height: 2.5rem;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  color: #374151;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.page-btn:hover {
  background: #f3f4f6;
  border-color: #d1d5db;
}

.page-btn.active {
  background: var(--primary-color, #8b5a3c);
  border-color: var(--primary-color, #8b5a3c);
  color: white;
}

.ellipsis {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  height: 2.5rem;
  color: #6b7280;
  font-weight: 500;
}

.btn-icon {
  font-size: 1.1rem;
}

.btn-text {
  display: none;
}

.pagination-info {
  text-align: center;
  color: #6b7280;
  font-size: 0.875rem;
  margin-top: 1rem;
}

/* Responsive Design */
@media (min-width: 640px) {
  .btn-text {
    display: inline;
  }
  
  .pagination-container {
    gap: 1rem;
  }
  
  .page-numbers {
    gap: 0.5rem;
  }
}

@media (max-width: 480px) {
  .pagination-container {
    gap: 0.25rem;
  }
  
  .pagination-btn {
    padding: 0.5rem 0.75rem;
    font-size: 0.875rem;
  }
  
  .page-btn {
    width: 2rem;
    height: 2rem;
    font-size: 0.875rem;
  }
  
  .ellipsis {
    width: 2rem;
    height: 2rem;
  }
}
</style>
