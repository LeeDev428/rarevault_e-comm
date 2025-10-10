<template>
  <AdminLayout>
    <div class="reports-page">
      <div class="page-header">
        <h1>Reports & Logs</h1>
        <p class="subtitle">Monitor system activity, sales reports, and user actions</p>
      </div>

    <!-- Tabs Navigation -->
    <div class="tabs-navigation">
      <button 
        v-for="tab in tabs" 
        :key="tab.id"
        @click="activeTab = tab.id"
        :class="['tab-btn', { active: activeTab === tab.id }]"
      >
        <component :is="tab.icon" />
        {{ tab.label }}
      </button>
    </div>

    <!-- Sales Reports Tab -->
    <div v-if="activeTab === 'sales'" class="tab-content">
      <div class="reports-header">
        <h2>Sales Overview</h2>
        
        <div class="date-filters">
          <select v-model="salesFilters.period" @change="fetchSalesData" class="filter-select">
            <option value="today">Today</option>
            <option value="week">This Week</option>
            <option value="month">This Month</option>
            <option value="year">This Year</option>
            <option value="custom">Custom Range</option>
          </select>
          
          <div v-if="salesFilters.period === 'custom'" class="date-range">
            <input 
              type="date" 
              v-model="salesFilters.startDate" 
              @change="fetchSalesData"
              class="date-input"
            >
            <span>to</span>
            <input 
              type="date" 
              v-model="salesFilters.endDate" 
              @change="fetchSalesData"
              class="date-input"
            >
          </div>
          
          <button @click="exportSalesReport" class="btn-export">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
              <polyline points="7 10 12 15 17 10"></polyline>
              <line x1="12" y1="15" x2="12" y2="3"></line>
            </svg>
            Export CSV
          </button>
        </div>
      </div>

      <!-- Sales Statistics Cards -->
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon revenue">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="12" y1="1" x2="12" y2="23"></line>
              <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
            </svg>
          </div>
          <div class="stat-content">
            <span class="stat-label">Total Revenue</span>
            <span class="stat-value">₱{{ formatNumber(salesStats.totalRevenue) }}</span>
            <span class="stat-change positive">+{{ salesStats.revenueChange }}%</span>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon orders">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="9" cy="21" r="1"></circle>
              <circle cx="20" cy="21" r="1"></circle>
              <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
            </svg>
          </div>
          <div class="stat-content">
            <span class="stat-label">Total Orders</span>
            <span class="stat-value">{{ salesStats.totalOrders }}</span>
            <span class="stat-change positive">+{{ salesStats.ordersChange }}%</span>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon items">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
            </svg>
          </div>
          <div class="stat-content">
            <span class="stat-label">Items Sold</span>
            <span class="stat-value">{{ salesStats.itemsSold }}</span>
            <span class="stat-change negative">{{ salesStats.itemsChange }}%</span>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon avg">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
            </svg>
          </div>
          <div class="stat-content">
            <span class="stat-label">Avg Order Value</span>
            <span class="stat-value">₱{{ formatNumber(salesStats.avgOrderValue) }}</span>
            <span class="stat-change positive">+{{ salesStats.avgChange }}%</span>
          </div>
        </div>
      </div>

      <!-- Sales Table -->
      <div class="data-table">
        <h3>Recent Sales</h3>
        <table v-if="salesData.length > 0">
          <thead>
            <tr>
              <th>Order ID</th>
              <th>Date</th>
              <th>Customer</th>
              <th>Seller</th>
              <th>Item</th>
              <th>Amount</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="sale in salesData" :key="sale.id">
              <td><span class="order-id">#{{ sale.orderNumber }}</span></td>
              <td>{{ formatDate(sale.date) }}</td>
              <td>{{ sale.customer }}</td>
              <td>{{ sale.seller }}</td>
              <td class="item-title">{{ sale.item }}</td>
              <td class="amount">₱{{ formatNumber(sale.amount) }}</td>
              <td>
                <span class="status-badge" :class="sale.status.toLowerCase()">
                  {{ sale.status }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
        <div v-else class="empty-state">
          <p>No sales data available for the selected period</p>
        </div>
      </div>
    </div>

    <!-- Activity Logs Tab -->
    <div v-if="activeTab === 'activity'" class="tab-content">
      <div class="reports-header">
        <h2>System Activity Logs</h2>
        
        <div class="date-filters">
          <select v-model="activityFilters.action" @change="fetchActivityLogs" class="filter-select">
            <option value="all">All Actions</option>
            <option value="login">Login</option>
            <option value="logout">Logout</option>
            <option value="create">Create</option>
            <option value="update">Update</option>
            <option value="delete">Delete</option>
          </select>
          
          <select v-model="activityFilters.userRole" @change="fetchActivityLogs" class="filter-select">
            <option value="all">All Users</option>
            <option value="admin">Admin</option>
            <option value="seller">Seller</option>
            <option value="user">Buyer</option>
          </select>
          
          <input 
            type="date" 
            v-model="activityFilters.date" 
            @change="fetchActivityLogs"
            class="date-input"
          >
          
          <button @click="exportActivityLogs" class="btn-export">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
              <polyline points="7 10 12 15 17 10"></polyline>
              <line x1="12" y1="15" x2="12" y2="3"></line>
            </svg>
            Export CSV
          </button>
        </div>
      </div>

      <!-- Activity Logs Table -->
      <div class="data-table">
        <table v-if="activityLogs.length > 0">
          <thead>
            <tr>
              <th>Timestamp</th>
              <th>User</th>
              <th>Role</th>
              <th>Action</th>
              <th>Resource</th>
              <th>Details</th>
              <th>IP Address</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="log in activityLogs" :key="log.id">
              <td class="timestamp">{{ formatDateTime(log.timestamp) }}</td>
              <td>{{ log.username }}</td>
              <td>
                <span class="role-badge" :class="log.role">{{ log.role }}</span>
              </td>
              <td>
                <span class="action-badge" :class="log.action">{{ log.action }}</span>
              </td>
              <td>{{ log.resource }}</td>
              <td class="details">{{ log.details }}</td>
              <td class="ip">{{ log.ipAddress }}</td>
            </tr>
          </tbody>
        </table>
        <div v-else class="empty-state">
          <p>No activity logs found</p>
        </div>
      </div>
    </div>

    <!-- User Analytics Tab -->
    <div v-if="activeTab === 'analytics'" class="tab-content">
      <div class="reports-header">
        <h2>User Analytics</h2>
        
        <div class="date-filters">
          <select v-model="analyticsFilters.period" @change="fetchAnalytics" class="filter-select">
            <option value="week">Last 7 Days</option>
            <option value="month">Last 30 Days</option>
            <option value="quarter">Last 3 Months</option>
            <option value="year">Last Year</option>
          </select>
        </div>
      </div>

      <!-- Analytics Stats -->
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon users">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
              <circle cx="9" cy="7" r="4"></circle>
              <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
              <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
            </svg>
          </div>
          <div class="stat-content">
            <span class="stat-label">Total Users</span>
            <span class="stat-value">{{ analyticsStats.totalUsers }}</span>
            <span class="stat-change positive">+{{ analyticsStats.usersGrowth }}%</span>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon active">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M22 12h-4l-3 9L9 3l-3 9H2"></path>
            </svg>
          </div>
          <div class="stat-content">
            <span class="stat-label">Active Users</span>
            <span class="stat-value">{{ analyticsStats.activeUsers }}</span>
            <span class="stat-change positive">+{{ analyticsStats.activeGrowth }}%</span>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon sellers">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"></path>
              <line x1="7" y1="7" x2="7.01" y2="7"></line>
            </svg>
          </div>
          <div class="stat-content">
            <span class="stat-label">Active Sellers</span>
            <span class="stat-value">{{ analyticsStats.activeSellers }}</span>
            <span class="stat-change positive">+{{ analyticsStats.sellersGrowth }}%</span>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon retention">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
              <polyline points="22 4 12 14.01 9 11.01"></polyline>
            </svg>
          </div>
          <div class="stat-content">
            <span class="stat-label">Retention Rate</span>
            <span class="stat-value">{{ analyticsStats.retentionRate }}%</span>
            <span class="stat-change positive">+{{ analyticsStats.retentionChange }}%</span>
          </div>
        </div>
      </div>

      <!-- User Breakdown -->
      <div class="analytics-charts">
        <div class="chart-card">
          <h3>User Registration Trend</h3>
          <div class="chart-placeholder">
            <svg width="100%" height="200" viewBox="0 0 400 200">
              <polyline 
                points="0,180 50,150 100,160 150,120 200,140 250,100 300,110 350,80 400,90"
                fill="none"
                stroke="#0d6efd"
                stroke-width="3"
              />
            </svg>
          </div>
        </div>

        <div class="chart-card">
          <h3>User Distribution by Role</h3>
          <div class="role-distribution">
            <div class="role-item">
              <div class="role-bar">
                <div class="role-fill admin" :style="{ width: analyticsStats.adminPercent + '%' }"></div>
              </div>
              <span class="role-label">Admin ({{ analyticsStats.adminPercent }}%)</span>
            </div>
            <div class="role-item">
              <div class="role-bar">
                <div class="role-fill seller" :style="{ width: analyticsStats.sellerPercent + '%' }"></div>
              </div>
              <span class="role-label">Sellers ({{ analyticsStats.sellerPercent }}%)</span>
            </div>
            <div class="role-item">
              <div class="role-bar">
                <div class="role-fill user" :style="{ width: analyticsStats.userPercent + '%' }"></div>
              </div>
              <span class="role-label">Buyers ({{ analyticsStats.userPercent }}%)</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-overlay">
      <div class="spinner"></div>
      <p>Loading data...</p>
    </div>
    </div>
  </AdminLayout>
</template>

<script>
import AdminLayout from '@/components/admin/AdminLayout.vue'

export default {
  name: 'ReportsPage',
  components: {
    AdminLayout
  },
  data() {
    return {
      activeTab: 'sales',
      loading: false,
      tabs: [
        { id: 'sales', label: 'Sales Reports', icon: 'ChartIcon' },
        { id: 'activity', label: 'Activity Logs', icon: 'ActivityIcon' },
        { id: 'analytics', label: 'User Analytics', icon: 'UsersIcon' }
      ],
      salesFilters: {
        period: 'month',
        startDate: '',
        endDate: ''
      },
      activityFilters: {
        action: 'all',
        userRole: 'all',
        date: ''
      },
      analyticsFilters: {
        period: 'month'
      },
      salesStats: {
        totalRevenue: 0,
        revenueChange: 0,
        totalOrders: 0,
        ordersChange: 0,
        itemsSold: 0,
        itemsChange: 0,
        avgOrderValue: 0,
        avgChange: 0
      },
      salesData: [],
      activityLogs: [],
      analyticsStats: {
        totalUsers: 0,
        usersGrowth: 0,
        activeUsers: 0,
        activeGrowth: 0,
        activeSellers: 0,
        sellersGrowth: 0,
        retentionRate: 0,
        retentionChange: 0,
        adminPercent: 0,
        sellerPercent: 0,
        userPercent: 0
      }
    }
  },
  async mounted() {
    await this.loadTabData()
  },
  watch: {
    activeTab() {
      this.loadTabData()
    }
  },
  methods: {
    async loadTabData() {
      switch (this.activeTab) {
        case 'sales':
          await this.fetchSalesData()
          break
        case 'activity':
          await this.fetchActivityLogs()
          break
        case 'analytics':
          await this.fetchAnalytics()
          break
      }
    },
    
    async fetchSalesData() {
      try {
        this.loading = true
        const token = localStorage.getItem('access_token') || localStorage.getItem('token')
        
        if (!token) {
          throw new Error('No authentication token found')
        }

        // Fetch sales statistics
        const statsResponse = await fetch(`http://localhost:5000/api/admin/reports/sales-stats?period=${this.salesFilters.period}`, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })

        const statsData = await statsResponse.json()
        
        if (!statsResponse.ok) {
          throw new Error(statsData.error || 'Failed to fetch sales statistics')
        }

        // Update stats from backend
        if (statsData.stats) {
          this.salesStats = statsData.stats
        }

        // Fetch recent sales
        const salesResponse = await fetch(`http://localhost:5000/api/admin/reports/recent-sales?period=${this.salesFilters.period}`, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })

        const salesData = await salesResponse.json()
        
        if (!salesResponse.ok) {
          throw new Error(salesData.error || 'Failed to fetch sales data')
        }

        if (salesData.sales && Array.isArray(salesData.sales)) {
          this.salesData = salesData.sales
        } else {
          this.salesData = []
        }

        console.log('Sales data loaded:', this.salesData.length, 'records')
      } catch (error) {
        console.error('Fetch sales data error:', error)
        // Use mock data if API fails
        this.loadMockSalesData()
      } finally {
        this.loading = false
      }
    },
    
    async fetchActivityLogs() {
      try {
        this.loading = true
        const token = localStorage.getItem('access_token') || localStorage.getItem('token')
        
        if (!token) {
          throw new Error('No authentication token found')
        }

        const params = new URLSearchParams({
          action: this.activityFilters.action,
          role: this.activityFilters.userRole,
          date: this.activityFilters.date || ''
        })

        const response = await fetch(`http://localhost:5000/api/admin/reports/activity-logs?${params}`, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })

        const data = await response.json()
        
        if (!response.ok) {
          throw new Error(data.error || 'Failed to fetch activity logs')
        }

        if (data.logs && Array.isArray(data.logs)) {
          this.activityLogs = data.logs
        } else {
          this.activityLogs = []
        }

        console.log('Activity logs loaded:', this.activityLogs.length, 'records')
      } catch (error) {
        console.error('Fetch activity logs error:', error)
        this.loadMockActivityLogs()
      } finally {
        this.loading = false
      }
    },
    
    async fetchAnalytics() {
      try {
        this.loading = true
        const token = localStorage.getItem('access_token') || localStorage.getItem('token')
        
        if (!token) {
          throw new Error('No authentication token found')
        }

        const response = await fetch(`http://localhost:5000/api/admin/reports/user-analytics?period=${this.analyticsFilters.period}`, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })

        const data = await response.json()
        
        if (!response.ok) {
          throw new Error(data.error || 'Failed to fetch analytics')
        }

        if (data.analytics) {
          this.analyticsStats = data.analytics
        }

        console.log('Analytics loaded successfully')
      } catch (error) {
        console.error('Fetch analytics error:', error)
        this.loadMockAnalytics()
      } finally {
        this.loading = false
      }
    },
    
    loadMockSalesData() {
      // Fallback mock data
      this.salesStats = {
        totalRevenue: 125450.75,
        revenueChange: 12.5,
        totalOrders: 342,
        ordersChange: 8.3,
        itemsSold: 567,
        itemsChange: -2.1,
        avgOrderValue: 366.81,
        avgChange: 4.2
      }

      this.salesData = [
        {
          id: 1,
          orderNumber: '2024-001',
          date: new Date().toISOString(),
          customer: 'John Doe',
          seller: 'Vintage Shop',
          item: 'Antique Clock',
          amount: 1250.00,
          status: 'Delivered'
        }
      ]
    },
    
    loadMockActivityLogs() {
      this.activityLogs = [
        {
          id: 1,
          timestamp: new Date().toISOString(),
          username: 'admin',
          role: 'admin',
          action: 'login',
          resource: 'System',
          details: 'Successful login',
          ipAddress: '192.168.1.1'
        }
      ]
    },
    
    loadMockAnalytics() {
      this.analyticsStats = {
        totalUsers: 1245,
        usersGrowth: 15.2,
        activeUsers: 892,
        activeGrowth: 8.7,
        activeSellers: 156,
        sellersGrowth: 12.3,
        retentionRate: 78.5,
        retentionChange: 3.2,
        adminPercent: 2,
        sellerPercent: 28,
        userPercent: 70
      }
    },
    
    exportSalesReport() {
      const csv = this.generateCSV(this.salesData, [
        'orderNumber', 'date', 'customer', 'seller', 'item', 'amount', 'status'
      ])
      this.downloadCSV(csv, 'sales-report.csv')
    },
    
    exportActivityLogs() {
      const csv = this.generateCSV(this.activityLogs, [
        'timestamp', 'username', 'role', 'action', 'resource', 'details', 'ipAddress'
      ])
      this.downloadCSV(csv, 'activity-logs.csv')
    },
    
    generateCSV(data, headers) {
      const csvRows = []
      csvRows.push(headers.join(','))
      
      for (const row of data) {
        const values = headers.map(header => {
          const value = row[header]
          return `"${value}"`
        })
        csvRows.push(values.join(','))
      }
      
      return csvRows.join('\n')
    },
    
    downloadCSV(csv, filename) {
      const blob = new Blob([csv], { type: 'text/csv' })
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.setAttribute('hidden', '')
      a.setAttribute('href', url)
      a.setAttribute('download', filename)
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
    },
    
    formatNumber(num) {
      return parseFloat(num || 0).toLocaleString('en-US', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      })
    },
    
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    },
    
    formatDateTime(dateString) {
      return new Date(dateString).toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
  }
}
</script>

<style scoped>
.reports-page {
  width: 100%;
  padding: 0;
}

/* Page Header */
.page-header {
  margin-bottom: 32px;
}

.page-header h1 {
  font-size: 32px;
  font-weight: 700;
  color: #212529;
  margin: 0 0 8px 0;
}

.subtitle {
  font-size: 16px;
  color: #6c757d;
  margin: 0;
}

/* Tabs Navigation */
.tabs-navigation {
  display: flex;
  gap: 12px;
  margin-bottom: 32px;
  border-bottom: 2px solid #e9ecef;
  padding-bottom: 0;
}

.tab-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: none;
  border: none;
  border-bottom: 3px solid transparent;
  font-size: 15px;
  font-weight: 500;
  color: #6c757d;
  cursor: pointer;
  transition: all 0.2s;
  margin-bottom: -2px;
}

.tab-btn:hover {
  color: #495057;
  background: #f8f9fa;
}

.tab-btn.active {
  color: #0d6efd;
  border-bottom-color: #0d6efd;
  background: white;
}

/* Tab Content */
.tab-content {
  background: white;
  border-radius: 12px;
  padding: 24px;
  border: 1px solid #e9ecef;
}

.reports-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e9ecef;
}

.reports-header h2 {
  font-size: 24px;
  font-weight: 600;
  color: #212529;
  margin: 0;
}

/* Filters */
.date-filters {
  display: flex;
  gap: 12px;
  align-items: center;
}

.filter-select,
.date-input {
  padding: 8px 14px;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  font-size: 14px;
  color: #495057;
  background: white;
}

.date-range {
  display: flex;
  gap: 8px;
  align-items: center;
}

.btn-export {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: #198754;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-export:hover {
  background: #157347;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

.stat-card {
  display: flex;
  gap: 16px;
  padding: 24px;
  background: linear-gradient(135deg, #f8f9fa 0%, white 100%);
  border-radius: 12px;
  border: 1px solid #e9ecef;
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-icon.revenue { background: linear-gradient(135deg, #0d6efd 0%, #0a58ca 100%); color: white; }
.stat-icon.orders { background: linear-gradient(135deg, #198754 0%, #146c43 100%); color: white; }
.stat-icon.items { background: linear-gradient(135deg, #ffc107 0%, #ff9800 100%); color: white; }
.stat-icon.avg { background: linear-gradient(135deg, #6f42c1 0%, #5a32a3 100%); color: white; }
.stat-icon.users { background: linear-gradient(135deg, #0dcaf0 0%, #0aa2c0 100%); color: white; }
.stat-icon.active { background: linear-gradient(135deg, #20c997 0%, #198754 100%); color: white; }
.stat-icon.sellers { background: linear-gradient(135deg, #fd7e14 0%, #e8590c 100%); color: white; }
.stat-icon.retention { background: linear-gradient(135deg, #d63384 0%, #ab296a 100%); color: white; }

.stat-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-label {
  font-size: 13px;
  color: #6c757d;
  font-weight: 500;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #212529;
}

.stat-change {
  font-size: 13px;
  font-weight: 600;
}

.stat-change.positive {
  color: #198754;
}

.stat-change.negative {
  color: #dc3545;
}

/* Data Table */
.data-table {
  margin-top: 32px;
}

.data-table h3 {
  font-size: 18px;
  font-weight: 600;
  color: #212529;
  margin: 0 0 16px 0;
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background: #f8f9fa;
  border-bottom: 2px solid #dee2e6;
}

th {
  padding: 12px 16px;
  text-align: left;
  font-size: 13px;
  font-weight: 600;
  color: #495057;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

tbody tr {
  border-bottom: 1px solid #f1f3f4;
  transition: background-color 0.2s;
}

tbody tr:hover {
  background: #f8f9fa;
}

td {
  padding: 14px 16px;
  font-size: 14px;
  color: #495057;
}

.order-id {
  font-family: monospace;
  font-weight: 600;
  color: #0d6efd;
}

.item-title {
  font-weight: 500;
  color: #212529;
}

.amount {
  font-weight: 600;
  color: #198754;
}

.timestamp {
  font-size: 13px;
  color: #6c757d;
}

.ip {
  font-family: monospace;
  font-size: 13px;
}

.details {
  max-width: 300px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Badges */
.status-badge,
.role-badge,
.action-badge {
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  text-transform: capitalize;
}

.status-badge.delivered { background: #d4edda; color: #155724; }
.status-badge.shipped { background: #d1ecf1; color: #0c5460; }
.status-badge.pending { background: #fff3cd; color: #856404; }
.status-badge.cancelled { background: #f8d7da; color: #721c24; }

.role-badge.admin { background: #e7f1ff; color: #0d6efd; }
.role-badge.seller { background: #fff3cd; color: #856404; }
.role-badge.user { background: #d4edda; color: #155724; }

.action-badge.login { background: #d1ecf1; color: #0c5460; }
.action-badge.logout { background: #f8d7da; color: #721c24; }
.action-badge.create { background: #d4edda; color: #155724; }
.action-badge.update { background: #fff3cd; color: #856404; }
.action-badge.delete { background: #f8d7da; color: #721c24; }

/* Analytics Charts */
.analytics-charts {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 24px;
  margin-top: 32px;
}

.chart-card {
  padding: 24px;
  background: white;
  border-radius: 12px;
  border: 1px solid #e9ecef;
}

.chart-card h3 {
  font-size: 16px;
  font-weight: 600;
  color: #212529;
  margin: 0 0 20px 0;
}

.chart-placeholder {
  width: 100%;
  height: 200px;
  background: #f8f9fa;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.role-distribution {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.role-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.role-bar {
  width: 100%;
  height: 32px;
  background: #f1f3f4;
  border-radius: 8px;
  overflow: hidden;
}

.role-fill {
  height: 100%;
  transition: width 0.3s ease;
}

.role-fill.admin { background: #0d6efd; }
.role-fill.seller { background: #ffc107; }
.role-fill.user { background: #198754; }

.role-label {
  font-size: 14px;
  font-weight: 500;
  color: #495057;
}

/* Empty State */
.empty-state {
  padding: 60px 20px;
  text-align: center;
  color: #6c757d;
}

.empty-state p {
  font-size: 16px;
  margin: 0;
}

/* Loading Overlay */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.9);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #f1f3f4;
  border-top-color: #0d6efd;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-overlay p {
  margin-top: 16px;
  font-size: 16px;
  color: #6c757d;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .analytics-charts {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .reports-page {
    padding: 24px 16px;
  }

  .reports-header {
    flex-direction: column;
    align-items: stretch;
    gap: 16px;
  }

  .date-filters {
    flex-wrap: wrap;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .tabs-navigation {
    overflow-x: auto;
  }

  table {
    display: block;
    overflow-x: auto;
    white-space: nowrap;
  }
}
</style>
