<template>
  <SellerLayout>
    <div class="seller-dashboard" style="padding: 20px; background: white; margin: 20px; border-radius: 8px;">
      <h1 style="color: #333; font-size: 24px; margin-bottom: 16px;">🎯 Seller Dashboard</h1>
      <p style="color: #666; font-size: 16px; margin-bottom: 20px;">Welcome to your seller dashboard! This content should be visible.</p>
      
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 24px;">
        <div style="background: #f8f9fa; padding: 16px; border-radius: 8px; border: 1px solid #dee2e6;">
          <h3 style="color: #007bff; margin: 0 0 8px 0;">📦 Total Items</h3>
          <p style="font-size: 24px; font-weight: bold; margin: 0; color: #333;">{{ stats.totalItems }}</p>
        </div>
        
        <div style="background: #f8f9fa; padding: 16px; border-radius: 8px; border: 1px solid #dee2e6;">
          <h3 style="color: #28a745; margin: 0 0 8px 0;">✅ Active Items</h3>
          <p style="font-size: 24px; font-weight: bold; margin: 0; color: #333;">{{ stats.activeItems }}</p>
        </div>
        
        <div style="background: #f8f9fa; padding: 16px; border-radius: 8px; border: 1px solid #dee2e6;">
          <h3 style="color: #ffc107; margin: 0 0 8px 0;">⏳ Pending Items</h3>
          <p style="font-size: 24px; font-weight: bold; margin: 0; color: #333;">{{ stats.pendingItems }}</p>
        </div>
        
        <div style="background: #f8f9fa; padding: 16px; border-radius: 8px; border: 1px solid #dee2e6;">
          <h3 style="color: #dc3545; margin: 0 0 8px 0;">💰 Sold Items</h3>
          <p style="font-size: 24px; font-weight: bold; margin: 0; color: #333;">{{ stats.soldItems }}</p>
        </div>
      </div>
      
      <div style="margin-top: 24px;">
        <button 
          @click="goToCreateItem"
          style="background: #007bff; color: white; border: none; padding: 12px 24px; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: 500;"
        >
          ➕ Add New Item
        </button>
      </div>
      
      <div style="margin-top: 24px; padding: 16px; background: #e7f3ff; border-radius: 8px; border: 1px solid #b8daff;">
        <h3 style="color: #0056b3; margin: 0 0 8px 0;">🎉 Content is Working!</h3>
        <p style="color: #0056b3; margin: 0;">If you can see this message, the slot system is working correctly.</p>
      </div>
    </div>
  </SellerLayout>
</template>

<script>
import SellerLayout from '@/components/seller/SellerLayout.vue'

export default {
  name: 'SellerDashboard',
  components: {
    SellerLayout
  },
  data() {
    return {
      stats: {
        totalItems: 12,
        activeItems: 8,
        soldItems: 3,
        pendingItems: 1
      }
    }
  },
  methods: {
    goToCreateItem() {
      this.$router.push('/seller/create-item')
    }
  }
}
</script>
