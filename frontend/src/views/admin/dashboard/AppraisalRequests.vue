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
        <button class="approve-all-btn">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <polyline points="20,6 9,17 4,12"></polyline>
          </svg>
          Approved All
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
      totalRequests: [
        {
          id: 1,
          itemTitle: 'Antique Gold Pocket Watch',
          postedBy: 'Time Traveler',
          dateRequested: '2025-05-15',
          status: 'Pending'
        },
        {
          id: 2,
          itemTitle: 'Signed First Edition Poetry Book',
          postedBy: 'LiteraryLeopard',
          dateRequested: '2025-05-14',
          status: 'Approved'
        },
        {
          id: 3,
          itemTitle: 'Vintage Baseball Card Collection',
          postedBy: 'CardShark',
          dateRequested: '2025-05-14',
          status: 'Rejected'
        },
        {
          id: 4,
          itemTitle: 'Old Oil Painting (Unsigned)',
          postedBy: 'ArtCurious',
          dateRequested: '2025-05-13',
          status: 'Rejected'
        },
        {
          id: 5,
          itemTitle: 'Ancient Roman Coin',
          postedBy: 'HistoryBuff',
          dateRequested: '2025-05-13',
          status: 'Pending'
        },
        {
          id: 6,
          itemTitle: 'Retro Gaming Console (Sealed)',
          postedBy: 'PixelPioneer',
          dateRequested: '2025-05-12',
          status: 'Pending'
        }
      ],
      soldRequests: [
        {
          id: 7,
          itemTitle: 'Victorian Silver Tea Set',
          postedBy: 'AntiqueDealer',
          dateRequested: '2025-05-10',
          status: 'Approved'
        },
        {
          id: 8,
          itemTitle: 'Rare Stamp Collection',
          postedBy: 'PhilatelistPro',
          dateRequested: '2025-05-09',
          status: 'Approved'
        }
      ],
      pendingRequests: [
        {
          id: 9,
          itemTitle: 'Antique Gold Pocket Watch',
          postedBy: 'Time Traveler',
          dateRequested: '2025-05-15',
          status: 'Pending'
        },
        {
          id: 10,
          itemTitle: 'Ancient Roman Coin',
          postedBy: 'HistoryBuff',
          dateRequested: '2025-05-13',
          status: 'Pending'
        },
        {
          id: 11,
          itemTitle: 'Retro Gaming Console (Sealed)',
          postedBy: 'PixelPioneer',
          dateRequested: '2025-05-12',
          status: 'Pending'
        }
      ]
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
  },
  methods: {
    setActiveSubTab(tab) {
      this.activeSubTab = tab
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
