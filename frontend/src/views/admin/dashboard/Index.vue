<template>
  <AdminLayout>
    <div class="dashboard-container">
      <!-- Dashboard Header -->
      <div class="dashboard-header">
        <h2>Dashboard</h2>
        <button class="delete-all-btn">Delete all</button>
      </div>

      <!-- Tab Navigation -->
      <div class="tab-navigation">
        <button 
          v-for="tab in tabs" 
          :key="tab.id"
          :class="['tab-btn', { active: activeTab === tab.id }]"
          @click="activeTab = tab.id"
        >
          {{ tab.label }}
        </button>
      </div>

      <!-- Tab Content -->
      <div class="tab-content">
        <TotalUsers v-if="activeTab === 'users'" />
        <ItemsListed v-if="activeTab === 'items'" />
        <AppraisalRequests v-if="activeTab === 'appraisals'" />
      </div>
    </div>
  </AdminLayout>
</template>

<script>
import { ref } from 'vue'
import AdminLayout from '@/components/admin/AdminLayout.vue'
import TotalUsers from './TotalUsers.vue'
import ItemsListed from './ItemsListed.vue'
import AppraisalRequests from './AppraisalRequests.vue'

export default {
  name: 'AdminDashboard',
  components: {
    AdminLayout,
    TotalUsers,
    ItemsListed,
    AppraisalRequests
  },
  setup() {
    const activeTab = ref('users')
    
    const tabs = [
      { id: 'users', label: 'Total Users' },
      { id: 'items', label: 'Items Listed' },
      { id: 'appraisals', label: 'Appraisal Requests' }
    ]

    return {
      activeTab,
      tabs
    }
  }
}
</script>

<style scoped>
.dashboard-container {
  padding: 24px;
  background: #ffffff;
  min-height: 100vh;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
}

.dashboard-header h2 {
  font-size: 24px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0;
}

.delete-all-btn {
  background: #ffffff;
  border: 1px solid #e5e5e5;
  color: #666666;
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.delete-all-btn:hover {
  background: #f5f5f5;
  border-color: #d0d0d0;
}

.tab-navigation {
  display: flex;
  border-bottom: 1px solid #e5e5e5;
  margin-bottom: 24px;
}

.tab-btn {
  background: none;
  border: none;
  padding: 12px 24px;
  font-size: 14px;
  color: #666666;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  transition: all 0.2s ease;
  position: relative;
}

.tab-btn:hover {
  color: #333333;
  background: #f8f9fa;
}

.tab-btn.active {
  color: #1a1a1a;
  border-bottom-color: #1a1a1a;
  font-weight: 500;
}

.tab-content {
  background: #ffffff;
}

/* Clean, minimal styling to match the reference images */
.tab-content > * {
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
