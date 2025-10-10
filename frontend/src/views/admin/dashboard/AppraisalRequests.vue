<template>
  <div class="appraisals-table-container">
    <!-- Sub Navigation -->
    <div class="sub-navigation">
      <button 
        class="sub-tab-btn" 
        :class="{ active: activeSubTab === 'total' }" 
        @click="setActiveSubTab('total')"
      >
        Total Listing
      </button>
      <button 
        class="sub-tab-btn" 
        :class="{ active: activeSubTab === 'sold' }" 
        @click="setActiveSubTab('sold')"
      >
        Items Sold
      </button>
      <button 
        class="sub-tab-btn" 
        :class="{ active: activeSubTab === 'pending' }" 
        @click="setActiveSubTab('pending')"
      >
        Pending Sales
      </button>
      
      <div class="sub-actions">
        <button class="approve-all-btn" @click="approveAll" :disabled="approving || pendingRequests.length === 0">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="20,6 9,17 4,12"></polyline>
          </svg>
          {{ approving ? 'Approving...' : 'Approve All' }}
        </button>
      </div>
    </div>

    <!-- Table Header -->
    <div class="table-header">
      <div class="header-col">Item Title</div>
      <div class="header-col">Posted By</div>
      <div class="header-col">Date requested</div>
      <div class="header-col">Status</div>
      <div class="header-col">View</div>
    </div>

    <!-- Table Body -->
    <div class="table-body">
      <div v-for="request in currentRequests" :key="request.id" class="table-row">
        <div class="table-cell">
          <div class="request-info">
            <input type="radio" :name="'request-' + request.id" class="row-radio">
            <span class="item-title">{{ request.itemTitle }}</span>
          </div>
        </div>
        <div class="table-cell">{{ request.postedBy }}</div>
        <div class="table-cell">{{ request.dateRequested }}</div>
        <div class="table-cell">
          <span class="status-badge" :class="request.status.toLowerCase()">{{ request.status }}</span>
        </div>
        <div class="table-cell">
          <button class="action-btn">View</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AppraisalRequests',
  data() {
    return {
      activeSubTab: 'pending',
      totalRequests: [],
      soldRequests: [],
      pendingRequests: [],
      loading: true,
      error: null,
      approving: false
    }
  },
  async mounted() {
    await this.fetchAllAppraisals()
  },
  watch: {
    activeSubTab() {
      this.fetchAppraisals()
    }
  },
  methods: {
    async fetchAllAppraisals() {
      await this.fetchAppraisals('all')
      await this.fetchAppraisals('approved')
      await this.fetchAppraisals('pending')
    },
    
    async fetchAppraisals(status = null) {
      try {
        this.loading = true
        const token = localStorage.getItem('access_token') || localStorage.getItem('token')
        const statusParam = status || (this.activeSubTab === 'total' ? 'all' : this.activeSubTab === 'sold' ? 'approved' : 'pending')
        
        console.log('Fetching appraisals with status:', statusParam)
        
        if (!token) {
          throw new Error('No authentication token found. Please login again.')
        }
        
        const response = await fetch(`http://localhost:5000/api/admin/appraisals?status=${statusParam}`, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })

        const data = await response.json()
        console.log('Appraisals response:', response.status, data)

        if (!response.ok) {
          throw new Error(data.error || 'Failed to fetch appraisals')
        }

        if (data.appraisals && Array.isArray(data.appraisals)) {
          const appraisals = data.appraisals.map(appraisal => ({
            id: appraisal.id,
            itemTitle: appraisal.title,
            postedBy: appraisal.posted_by || 'Unknown',
            dateRequested: new Date(appraisal.created_at).toLocaleDateString('en-US', { year: 'numeric', month: '2-digit', day: '2-digit' }),
            status: appraisal.appraisal_status.charAt(0).toUpperCase() + appraisal.appraisal_status.slice(1)
          }))

          if (statusParam === 'all') {
            this.totalRequests = appraisals
          } else if (statusParam === 'approved') {
            this.soldRequests = appraisals
          } else if (statusParam === 'pending') {
            this.pendingRequests = appraisals
          }
          
          console.log(`Loaded ${appraisals.length} appraisals for status: ${statusParam}`)
        } else {
          throw new Error('Invalid response format: appraisals array not found')
        }
      } catch (error) {
        console.error('Fetch appraisals error:', error)
        this.error = error.message
        this.totalRequests = []
        this.soldRequests = []
        this.pendingRequests = []
        alert('Failed to fetch appraisals: ' + error.message + '. Check console for details.')
      } finally {
        this.loading = false
      }
    },
    
    async approveItem(itemId) {
      try {
        const token = localStorage.getItem('access_token') || localStorage.getItem('token')
        
        const response = await fetch(`http://localhost:5000/api/admin/appraisals/${itemId}/approve`, {
          method: 'PATCH',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })

        const data = await response.json()

        if (!response.ok) {
          throw new Error(data.error || 'Failed to approve appraisal')
        }

        alert('Appraisal approved successfully')
        await this.fetchAppraisals()
        this.$emit('refresh')
      } catch (error) {
        console.error('Approve appraisal error:', error)
        alert('Failed to approve appraisal: ' + error.message)
      }
    },
    
    async approveAll() {
      if (!confirm('Are you sure you want to approve all pending appraisals?')) {
        return
      }

      try {
        this.approving = true
        const token = localStorage.getItem('access_token') || localStorage.getItem('token')
        
        const response = await fetch('http://localhost:5000/api/admin/appraisals/approve-all', {
          method: 'PATCH',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })

        const data = await response.json()

        if (!response.ok) {
          throw new Error(data.error || 'Failed to approve all appraisals')
        }

        alert(data.message || 'All appraisals approved successfully')
        await this.fetchAllAppraisals()
        this.$emit('refresh')
      } catch (error) {
        console.error('Approve all appraisals error:', error)
        alert('Failed to approve all: ' + error.message)
      } finally {
        this.approving = false
      }
    },
    
    setActiveSubTab(tab) {
      this.activeSubTab = tab
    }
  },
  computed: {
    currentRequests() {
      switch (this.activeSubTab) {
        case 'sold':
          return this.soldRequests
        case 'pending':
          return this.pendingRequests
        default:
          return this.totalRequests
      }
    }
  }
}
</script>

<style scoped>
.appraisals-table-container {
  width: 100%;
  background: white;
}

/* Sub Navigation */
.sub-navigation {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 20px;
  padding: 0 24px;
  padding-top: 20px;
}

.sub-tab-btn {
  padding: 8px 16px;
  background: #f8f9fa;
  border: none;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
  color: #6c757d;
  cursor: pointer;
  transition: all 0.2s;
}

.sub-tab-btn:hover {
  background: #e9ecef;
  color: #495057;
}

.sub-tab-btn.active {
  background: #212529;
  color: white;
}

.sub-actions {
  margin-left: auto;
}

.approve-all-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: none;
  border: 1px solid #dee2e6;
  border-radius: 6px;
  font-size: 14px;
  color: #6c757d;
  cursor: pointer;
  transition: all 0.2s;
}

.approve-all-btn:hover {
  background: #f8f9fa;
  border-color: #adb5bd;
  color: #495057;
}

/* Table Header */
.table-header {
  display: grid;
  grid-template-columns: 2fr 1.5fr 1fr 1fr 1fr;
  padding: 16px 24px;
  background: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
  font-weight: 600;
  font-size: 14px;
  color: #495057;
}

.header-col {
  padding: 8px 0;
}

/* Table Body */
.table-body {
  max-height: 500px;
  overflow-y: auto;
}

.table-row {
  display: grid;
  grid-template-columns: 2fr 1.5fr 1fr 1fr 1fr;
  padding: 16px 24px;
  border-bottom: 1px solid #f1f3f4;
  transition: background-color 0.2s;
}

.table-row:hover {
  background: #f8f9fa;
}

.table-cell {
  display: flex;
  align-items: center;
  padding: 8px 0;
  font-size: 14px;
  color: #495057;
}

/* Request Info */
.request-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.row-radio {
  width: 16px;
  height: 16px;
  cursor: pointer;
}

.item-title {
  font-weight: 500;
  color: #212529;
}

/* Status Badge */
.status-badge {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  text-transform: capitalize;
}

.status-badge.pending {
  background: #fff3cd;
  color: #856404;
}

.status-badge.approved {
  background: #d4edda;
  color: #155724;
}

.status-badge.rejected {
  background: #f8d7da;
  color: #721c24;
}

/* Action Button */
.action-btn {
  padding: 6px 16px;
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  font-size: 12px;
  color: #6c757d;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn:hover {
  background: #e9ecef;
  border-color: #adb5bd;
  color: #495057;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .table-header,
  .table-row {
    grid-template-columns: 2fr 1.5fr 1fr 1fr;
  }
  
  .table-cell:nth-child(3) {
    display: none;
  }
  
  .header-col:nth-child(3) {
    display: none;
  }
}

@media (max-width: 768px) {
  .table-header,
  .table-row {
    grid-template-columns: 2fr 1fr 1fr;
  }
  
  .table-cell:nth-child(2) {
    display: none;
  }
  
  .header-col:nth-child(2) {
    display: none;
  }
  
  .sub-navigation {
    flex-wrap: wrap;
    gap: 12px;
  }
  
  .sub-actions {
    margin-left: 0;
    width: 100%;
  }
  
  .approve-all-btn {
    width: 100%;
    justify-content: center;
  }
}

@media (max-width: 640px) {
  .appraisals-table-container {
    margin: 0 -24px;
  }
  
  .sub-navigation {
    padding: 20px 16px 0;
  }
  
  .table-header,
  .table-row {
    padding: 12px 16px;
    grid-template-columns: 1fr 1fr;
  }
  
  .table-cell:nth-child(n+3) {
    display: none;
  }
  
  .header-col:nth-child(n+3) {
    display: none;
  }
}
</style>
