<template>
  <div class="flex items-center justify-between bg-white p-6 border-t border-gray-200">
    <div class="flex flex-1 items-center justify-between">
      <div v-if="variant !== 'dots'">
        <p class="text-sm text-gray-700">
          Showing <span class="font-medium">{{ itemsPerPage * (currentPage - 1) + 1 }}</span> to <span class="font-medium">{{ Math.min(itemsPerPage * currentPage, totalItems) }}</span> of <span class="font-medium">{{ totalItems }}</span> {{ itemLabel }}
        </p>
      </div>
      <div>
        <nav v-if="variant !== 'dots'" class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px">
          <button @click="previousPage" :disabled="!hasPrevious" class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50">
            <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
            </svg>
          </button>
          <button v-for="page in visiblePages" :key="page" @click="goToPage(page)" :class="[page === currentPage ? 'z-10 bg-blue-50 border-blue-500 text-blue-600' : 'bg-white border-gray-300 text-gray-500 hover:bg-gray-50', 'relative inline-flex items-center px-4 py-2 border text-sm font-medium']">{{ page }}</button>
          <button @click="nextPage" :disabled="!hasNext" class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50">
            <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
            </svg>
          </button>
        </nav>

        <!-- Dots variant -->
        <nav v-else class="dots-pagination flex items-center gap-3 justify-center">
          <button v-for="page in totalPages" :key="page" @click="goToPage(page)" :class="['dot', { 'active': page === currentPage }]" aria-label="Go to page">
          </button>
        </nav>
      </div>
    </div>
  </div>
</template>
<script>
import { computed } from 'vue'
export default {
  name: 'Pagination',
  props: {
    currentPage: { type: Number, required: true },
    totalPages: { type: Number, required: true },
    totalItems: { type: Number, required: true },
    itemsPerPage: { type: Number, default: 9 },
    itemLabel: { type: String, default: 'items' },
    hasPrevious: { type: Boolean, default: false },
    hasNext: { type: Boolean, default: false },
    variant: { type: String, default: 'default' } // 'default' or 'dots'
  },
  emits: ['page-changed'],
  setup(props, { emit }) {
    const visiblePages = computed(() => {
      const pages = []
      const start = Math.max(1, props.currentPage - 2)
      const end = Math.min(props.totalPages, props.currentPage + 2)
      for (let i = start; i <= end; i++) { pages.push(i) }
      return pages
    })
    const previousPage = () => { if (props.hasPrevious) { emit('page-changed', props.currentPage - 1) } }
    const nextPage = () => { if (props.hasNext) { emit('page-changed', props.currentPage + 1) } }
    const goToPage = (page) => { emit('page-changed', page) }
    return { visiblePages, previousPage, nextPage, goToPage }
  }
}
</script>

<style scoped>
.dots-pagination .dot {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  border: 2px solid #d1d5db; /* light gray */
  background: transparent;
  cursor: pointer;
  transition: all 0.18s ease;
}
.dots-pagination .dot:hover { transform: translateY(-3px); border-color: #9ca3af; }
.dots-pagination .dot.active { background: #111827; border-color: #111827; }
</style>
