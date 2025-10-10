<template>
  <div class="users-table-container">
    <!-- Table Header -->
    <div class="table-header">
      <div class="header-col">Name</div>
      <div class="header-col">Shop name</div>
      <div class="header-col">Email</div>
      <div class="header-col">Role</div>
      <div class="header-col">Status</div>
      <div class="header-col">Action</div>
    </div>

    <!-- Table Body -->
    <div class="table-body">
      <div v-for="user in users" :key="user.id" class="table-row">
        <div class="table-cell">
          <div class="user-info">
            <input type="radio" :name="'user-' + user.id" class="row-radio">
            <span class="user-name">{{ user.name }}</span>
          </div>
        </div>
        <div class="table-cell">{{ user.shopName }}</div>
        <div class="table-cell">{{ user.email }}</div>
        <div class="table-cell">{{ user.role }}</div>
        <div class="table-cell">
          <span class="status-badge" :class="user.status.toLowerCase()">{{ user.status }}</span>
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
  name: 'TotalUsers',
  data() {
    return {
      users: [],
      loading: true,
      error: null
    }
  },
  async mounted() {
    await this.fetchUsers()
  },
  methods: {
    async fetchUsers() {
      try {
        this.loading = true
        const token = localStorage.getItem('access_token') || localStorage.getItem('token')
        
        console.log('Fetching users with token:', token ? 'Token exists' : 'No token found')
        
        if (!token) {
          throw new Error('No authentication token found. Please login again.')
        }
        
        const response = await fetch('http://localhost:5000/api/admin/users', {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })

        const data = await response.json()
        
        console.log('Response status:', response.status)
        console.log('Response data:', data)

        if (!response.ok) {
          console.error('API error response:', data)
          throw new Error(data.error || data.message || 'Failed to fetch users')
        }

        if (data.users && Array.isArray(data.users)) {
          // Map API data to component format
          this.users = data.users.map(user => ({
            id: user.id,
            name: user.username,
            shopName: user.shop_name || 'N/A',
            email: user.email,
            role: user.role.charAt(0).toUpperCase() + user.role.slice(1),
            status: user.is_active ? 'Active' : 'Suspended'
          }))
          console.log('Successfully loaded', this.users.length, 'users')
        } else {
          throw new Error('Invalid response format: users array not found')
        }
      } catch (error) {
        console.error('Fetch users error:', error)
        console.error('Error name:', error.name)
        console.error('Error message:', error.message)
        this.error = error.message
        this.users = []
        alert('Failed to fetch users: ' + error.message + '. Check console for details.')
      } finally {
        this.loading = false
      }
    },
    
    async deleteUser(userId) {
      if (!confirm('Are you sure you want to delete this user?')) {
        return
      }

      try {
        const token = localStorage.getItem('access_token') || localStorage.getItem('token')
        
        const response = await fetch(`http://localhost:5000/api/admin/users/${userId}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })

        const data = await response.json()

        if (!response.ok) {
          throw new Error(data.error || 'Failed to delete user')
        }

        alert('User deleted successfully')
        await this.fetchUsers()
        this.$emit('refresh')
      } catch (error) {
        console.error('Delete user error:', error)
        alert('Failed to delete user: ' + error.message)
      }
    }
  }
}
</script>

<style scoped>
.users-table-container {
  width: 100%;
  background: white;
}

/* Table Header */
.table-header {
  display: grid;
  grid-template-columns: 2fr 2fr 2fr 1fr 1fr 1fr;
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
  max-height: 600px;
  overflow-y: auto;
}

.table-row {
  display: grid;
  grid-template-columns: 2fr 2fr 2fr 1fr 1fr 1fr;
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

/* User Info */
.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.row-radio {
  width: 16px;
  height: 16px;
  cursor: pointer;
}

.user-name {
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

.status-badge.active {
  background: #d4edda;
  color: #155724;
}

.status-badge.suspended {
  background: #f8d7da;
  color: #721c24;
}

.status-badge.pending {
  background: #fff3cd;
  color: #856404;
}

.status-badge.review {
  background: #cce7ff;
  color: #004085;
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
    grid-template-columns: 2fr 1.5fr 2fr 1fr 1fr;
  }
  
  .table-cell:nth-child(2) {
    display: none;
  }
  
  .header-col:nth-child(2) {
    display: none;
  }
}

@media (max-width: 768px) {
  .table-header,
  .table-row {
    grid-template-columns: 2fr 1fr 1fr;
  }
  
  .table-cell:nth-child(3),
  .table-cell:nth-child(4) {
    display: none;
  }
  
  .header-col:nth-child(3),
  .header-col:nth-child(4) {
    display: none;
  }
}

@media (max-width: 640px) {
  .users-table-container {
    margin: 0 -24px;
  }
  
  .table-header,
  .table-row {
    padding: 12px 16px;
    grid-template-columns: 1fr 1fr;
  }
  
  .table-cell:nth-child(4),
  .table-cell:nth-child(5) {
    display: none;
  }
  
  .header-col:nth-child(4),
  .header-col:nth-child(5) {
    display: none;
  }
}
</style>
