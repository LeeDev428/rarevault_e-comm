<template>
  <div class="vintage-item-card">
    <!-- Item Image -->
    <div class="item-image-container">
      <img :src="item.image" :alt="item.title" class="item-image" />
      
      <!-- Overlay Actions on Hover -->
      <div class="item-overlay">
        <div class="item-actions">
          <button 
            class="action-btn contact-btn"
            @click="$emit('contact-seller', item)"
          >
            Contact seller
          </button>
          <button 
            class="action-btn save-btn"
            @click="$emit('save-item', item)"
          >
            Save to wishlist
          </button>
        </div>
      </div>
    </div>

    <!-- Item Details -->
    <div class="item-details">
      <div class="seller-label">
        <span>{{ item.seller }}</span>
      </div>
      
      <h3 class="item-title">{{ item.title }}</h3>
      
      <div class="item-price">
        <span class="price-label">Price</span>
        <span class="price-value">${{ item.price.toFixed(2) }}</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'VintageItemCard',
  props: {
    item: {
      type: Object,
      required: true
    }
  },
  emits: ['contact-seller', 'save-item']
}
</script>

<style scoped>
.vintage-item-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
}

.vintage-item-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

/* Image Container */
.item-image-container {
  position: relative;
  width: 100%;
  height: 240px;
  overflow: hidden;
}

.item-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.vintage-item-card:hover .item-image {
  transform: scale(1.05);
}

/* Overlay */
.item-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.vintage-item-card:hover .item-overlay {
  opacity: 1;
}

.item-actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 20px;
}

.action-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: center;
  min-width: 140px;
}

.contact-btn {
  background: #000000;
  color: white;
}

.contact-btn:hover {
  background: #1f2937;
}

.save-btn {
  background: white;
  color: #374151;
  border: 1px solid #d1d5db;
}

.save-btn:hover {
  background: #f9fafb;
  border-color: #9ca3af;
}

/* Item Details */
.item-details {
  padding: 16px;
}

.seller-label {
  margin-bottom: 8px;
}

.seller-label span {
  font-size: 12px;
  color: #6b7280;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.item-title {
  font-size: 16px;
  font-weight: 600;
  color: #111827;
  margin: 0 0 12px 0;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.item-price {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.price-label {
  font-size: 12px;
  color: #6b7280;
  font-weight: 500;
}

.price-value {
  font-size: 18px;
  font-weight: 700;
  color: #111827;
}

/* Responsive */
@media (max-width: 768px) {
  .item-image-container {
    height: 200px;
  }
  
  .item-actions {
    padding: 16px;
    gap: 10px;
  }
  
  .action-btn {
    padding: 8px 16px;
    font-size: 13px;
    min-width: 120px;
  }
  
  .item-details {
    padding: 12px;
  }
  
  .item-title {
    font-size: 15px;
  }
  
  .price-value {
    font-size: 16px;
  }
}
</style>
