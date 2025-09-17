<template><template>

  <div class="flex items-center justify-between bg-white p-6 border-t border-gray-200">  <div class="flex items-center justify-between bg-white p-6 border-t border-gray-200">

    <!-- Items info -->    <!-- Items info -->

    <div class="flex-1 flex justify-between items-center sm:hidden">    <div class="flex-1 flex justify-between items-center sm:hidden">

      <p class="text-sm text-gray-700">      <p class="text-sm text-gray-700">

        Showing {{ itemsPerPage * (currentPage - 1) + 1 }} to {{ Math.min(itemsPerPage * currentPage, totalItems) }} of {{ totalItems }} {{ itemLabel }}        Showing {{ itemsPerPage * (currentPage - 1) + 1 }} to {{ Math.min(itemsPerPage * currentPage, totalItems) }} of {{ totalItems }} {{ itemLabel }}

      </p>      </p>

      <div class="flex space-x-2">      <div class="flex space-x-2">

        <button         <button 

          @click="previousPage"           @click="previousPage" 

          :disabled="!hasPrevious"          :disabled="!hasPrevious"

          class="relative inline-flex items-center px-2 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"          class="relative inline-flex items-center px-2 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"

        >        >

          <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">          <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">

            <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />            <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />

          </svg>          </svg>

        </button>        </button>

        <button         <button 

          @click="nextPage"           @click="nextPage" 

          :disabled="!hasNext"          :disabled="!hasNext"

          class="relative inline-flex items-center px-2 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"          class="relative inline-flex items-center px-2 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"

        >        >

          <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">          <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">

            <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />            <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />

          </svg>          </svg>

        </button>        </button>

      </div>      </div>

    </div>    </div>



    <!-- Desktop pagination -->    <!-- Desktop pagination -->

    <div class="hidden sm:flex sm:flex-1 sm:items-center sm:justify-between">    <div class="hidden sm:flex sm:flex-1 sm:items-center sm:justify-between">

      <div>      <div>

        <p class="text-sm text-gray-700">        <p class="text-sm text-gray-700">

          Showing <span class="font-medium">{{ itemsPerPage * (currentPage - 1) + 1 }}</span> to <span class="font-medium">{{ Math.min(itemsPerPage * currentPage, totalItems) }}</span> of <span class="font-medium">{{ totalItems }}</span> {{ itemLabel }}          Showing <span class="font-medium">{{ itemsPerPage * (currentPage - 1) + 1 }}</span> to <span class="font-medium">{{ Math.min(itemsPerPage * currentPage, totalItems) }}</span> of <span class="font-medium">{{ totalItems }}</span> {{ itemLabel }}

        </p>        </p>

      </div>      </div>

      <div>      <div>

        <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">        <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">

          <!-- Previous button -->          <!-- Previous button -->

          <button          <button

            @click="previousPage"            @click="previousPage"

            :disabled="!hasPrevious"            :disabled="!hasPrevious"

            class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"            class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"

          >          >

            <span class="sr-only">Previous</span>            <span class="sr-only">Previous</span>

            <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">            <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">

              <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />              <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />

            </svg>            </svg>

          </button>          </button>



          <!-- Page numbers -->          <!-- Page numbers -->

          <button          <button

            v-for="page in visiblePages"            v-for="page in visiblePages"

            :key="page"            :key="page"

            @click="goToPage(page)"            @click="goToPage(page)"

            :class="[            :class="[

              page === currentPage              page === currentPage

                ? 'z-10 bg-blue-50 border-blue-500 text-blue-600'                ? 'z-10 bg-blue-50 border-blue-500 text-blue-600'

                : 'bg-white border-gray-300 text-gray-500 hover:bg-gray-50',                : 'bg-white border-gray-300 text-gray-500 hover:bg-gray-50',

              'relative inline-flex items-center px-4 py-2 border text-sm font-medium'              'relative inline-flex items-center px-4 py-2 border text-sm font-medium'

            ]"            ]"

          >          >

            {{ page }}            {{ page }}

          </button>          </button>



          <!-- Next button -->          <!-- Next button -->

          <button          <button

            @click="nextPage"            @click="nextPage"

            :disabled="!hasNext"            :disabled="!hasNext"

            class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"            class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"

          >          >

            <span class="sr-only">Next</span>            <span class="sr-only">Next</span>

            <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">            <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">

              <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />              <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />

            </svg>            </svg>

          </button>          </button>

        </nav>        </nav>

      </div>      </div>

    </div>    </div>

  </div>  </div>

</template></template>



<script><script>

import { computed } from 'vue'import { computed } from 'vue'



export default {export default {

  name: 'Pagination',  name: 'Pagination',

  props: {  props: {

    currentPage: {    currentPage: {

      type: Number,      type: Number,

      required: true      required: true

    },    },

    totalPages: {    totalPages: {

      type: Number,      type: Number,

      required: true      required: true

    },    },

    totalItems: {    totalItems: {

      type: Number,      type: Number,

      required: true      required: true

    },    },

    itemsPerPage: {    itemsPerPage: {

      type: Number,      type: Number,

      default: 9      default: 9

    },    },

    itemLabel: {    itemLabel: {

      type: String,      type: String,

      default: 'items'      default: 'items'

    },    },

    hasPrevious: {    hasPrevious: {

      type: Boolean,      type: Boolean,

      default: false      default: false

    },    },

    hasNext: {    hasNext: {

      type: Boolean,      type: Boolean,

      default: false      default: false

    }    }

  },  },

  emits: ['page-changed'],  emits: ['page-changed'],

  setup(props, { emit }) {  setup(props, { emit }) {

    const visiblePages = computed(() => {    const visiblePages = computed(() => {

      const pages = []      const pages = []

      const start = Math.max(1, props.currentPage - 2)      const start = Math.max(1, props.currentPage - 2)

      const end = Math.min(props.totalPages, props.currentPage + 2)      const end = Math.min(props.totalPages, props.currentPage + 2)

            

      for (let i = start; i <= end; i++) {      for (let i = start; i <= end; i++) {

        pages.push(i)        pages.push(i)

      }      }

            

      return pages      return pages

    })    })



    const previousPage = () => {    const previousPage = () => {

      if (props.hasPrevious) {      if (props.hasPrevious) {

        emit('page-changed', props.currentPage - 1)        emit('page-changed', props.currentPage - 1)

      }      }

    }    }



    const nextPage = () => {    const nextPage = () => {

      if (props.hasNext) {      if (props.hasNext) {

        emit('page-changed', props.currentPage + 1)        emit('page-changed', props.currentPage + 1)

      }      }

    }    }



    const goToPage = (page) => {    const goToPage = (page) => {

      emit('page-changed', page)      emit('page-changed', page)

    }    }



    return {    return {

      visiblePages,      visiblePages,

      previousPage,      previousPage,

      nextPage,      nextPage,

      goToPage      goToPage

    }    }

  }  }

}}

</script></script>



<style scoped><style scoped>

/* Additional custom styles if needed *//* Additional custom styles if needed */

</style></style>
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
