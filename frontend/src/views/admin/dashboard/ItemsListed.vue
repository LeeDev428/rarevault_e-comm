<template>
  <div class="items-table-container">
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
    </div>

    <!-- Table Header -->
    <div class="table-header">
      <div class="header-col">Photo</div>
      <div class="header-col">Title</div>
      <div class="header-col">Posted By</div>
      <div class="header-col">Category</div>
      <div class="header-col">Date Posted</div>
      <div class="header-col">View</div>
    </div>

    <!-- Table Body -->
    <div class="table-body">
      <div v-for="item in currentItems" :key="item.id" class="table-row">
        <div class="table-cell">
          <div class="item-photo">
            <input type="radio" :name="'item-' + item.id" class="row-radio">
            <div class="photo-placeholder">
              <img v-if="item.photo" :src="item.photo" :alt="item.title" class="item-image">
              <div v-else class="placeholder-icon">📷</div>
            </div>
          </div>
        </div>
        <div class="table-cell">
          <span class="item-title">{{ item.title }}</span>
        </div>
        <div class="table-cell">{{ item.postedBy }}</div>
        <div class="table-cell">{{ item.category }}</div>
        <div class="table-cell">{{ item.datePosted }}</div>
        <div class="table-cell">
          <button class="action-btn">View</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ItemsListed',
  data() {
    return {
      activeSubTab: 'total',
      totalItems: [
        {
          id: 1,
          photo: null,
          title: '1950s Coca-Cola Metal Sign',
          postedBy: 'RetroRelics',
          category: 'Vintage Item',
          datePosted: '2025-05-15'
        },
        {
          id: 2,
          photo: null,
          title: 'Rare Mispinted 1921 Silver Dollar',
          postedBy: 'CoinCollector',
          category: 'Coins & Currency',
          datePosted: '2025-05-14'
        },
        {
          id: 3,
          photo: null,
          title: 'Antique Oak Writing Desk (Circa 1880)',
          postedBy: 'HeritageFinds',
          category: 'Antiques',
          datePosted: '2025-05-14'
        },
        {
          id: 4,
          photo: null,
          title: '1950s Coca-Cola Metal Sign',
          postedBy: 'RetroRelics',
          category: 'Vintage Item',
          datePosted: '2025-05-15'
        },
        {
          id: 5,
          photo: null,
          title: 'Rare Mispinted 1921 Silver Dollar',
          postedBy: 'CoinCollector',
          category: 'Coins & Currency',
          datePosted: '2025-05-14'
        },
        {
          id: 6,
          photo: null,
          title: 'Antique Oak Writing Desk (Circa 1880)',
          postedBy: 'HeritageFinds',
          category: 'Antiques',
          datePosted: '2025-05-14'
        }
      ],
      soldItems: [
        {
          id: 7,
          photo: null,
          title: 'Antique Gold Pocket Watch',
          postedBy: 'Time Traveler',
          category: 'Timepieces',
          datePosted: '2025-05-15'
        },
        {
          id: 8,
          photo: null,
          title: 'Signed First Edition Poetry Book',
          postedBy: 'LiteraryLeopard',
          category: 'Books',
          datePosted: '2025-05-14'
        },
        {
          id: 9,
          photo: null,
          title: 'Vintage Baseball Card Collection',
          postedBy: 'CardShark',
          category: 'Sports Memorabilia',
          datePosted: '2025-05-14'
        },
        {
          id: 10,
          photo: null,
          title: 'Old Oil Painting (Unsigned)',
          postedBy: 'ArtCurious',
          category: 'Art',
          datePosted: '2025-05-13'
        }
      ],
      pendingItems: [
        {
          id: 11,
          photo: null,
          title: 'Ancient Roman Coin',
          postedBy: 'HistoryBuff',
          category: 'Historical Artifacts',
          datePosted: '2025-05-13'
        },
        {
          id: 12,
          photo: null,
          title: 'Retro Gaming Console (Sealed)',
          postedBy: 'PixelPioneer',
          category: 'Electronics',
          datePosted: '2025-05-12'
        }
      ]
    }
  },
  computed: {
    currentItems() {
      switch (this.activeSubTab) {
        case 'sold':
          return this.soldItems
        case 'pending':
          return this.pendingItems
        default:
          return this.totalItems
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
.items-table-container {
  width: 100%;
  background: white;
}

/* Sub Navigation */
.sub-navigation {
  display: flex;
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

/* Table Header */
.table-header {
  display: grid;
  grid-template-columns: 1fr 2fr 1.5fr 1fr 1fr 1fr;
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
  grid-template-columns: 1fr 2fr 1.5fr 1fr 1fr 1fr;
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

/* Item Photo */
.item-photo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.row-radio {
  width: 16px;
  height: 16px;
  cursor: pointer;
}

.photo-placeholder {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.item-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.placeholder-icon {
  font-size: 18px;
  color: #adb5bd;
}

/* Item Title */
.item-title {
  font-weight: 500;
  color: #212529;
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
    grid-template-columns: 1fr 2fr 1.5fr 1fr 1fr;
  }
  
  .table-cell:nth-child(4) {
    display: none;
  }
  
  .header-col:nth-child(4) {
    display: none;
  }
}

@media (max-width: 768px) {
  .table-header,
  .table-row {
    grid-template-columns: 1fr 2fr 1fr;
  }
  
  .table-cell:nth-child(3),
  .table-cell:nth-child(5) {
    display: none;
  }
  
  .header-col:nth-child(3),
  .header-col:nth-child(5) {
    display: none;
  }
}

@media (max-width: 640px) {
  .items-table-container {
    margin: 0 -24px;
  }
  
  .sub-navigation {
    padding: 20px 16px 0;
    flex-wrap: wrap;
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
