<template>
  <div class="vintage-item-card">
    <!-- Item Image Container -->
    <div class="item-image-container">
      <!-- Single Image Layout -->
      <div v-if="getItemImages(item).length === 1" class="single-image-layout">
        <img :src="getItemImages(item)[0].url" :alt="item.title" class="item-image single" />
      </div>
      
      <!-- Multiple Images Layout (Facebook style) -->
      <div v-else-if="getItemImages(item).length > 1" class="multiple-images-layout">
        <!-- Primary Image (Left side - bigger) -->
        <div class="primary-image-container">
          <img :src="getPrimaryImage(item).url" :alt="item.title" class="item-image primary" />
        </div>
        
        <!-- Secondary Images (Right side - smaller grid) -->
        <div class="secondary-images-container">
          <div v-for="(image, index) in getSecondaryImages(item)" 
               :key="image.id || index" 
               class="secondary-image-wrapper"
               :class="{ 'has-more': index === 2 && getSecondaryImages(item).length > 3 }">
            <img :src="image.url" :alt="`${item.title} ${index + 2}`" class="item-image secondary" />
            <!-- More images overlay -->
            <div v-if="index === 2 && getSecondaryImages(item).length > 3" class="more-images-overlay">
              <span>+{{ getSecondaryImages(item).length - 3 }}</span>
            </div>
          </div>
        </div>
      </div>
      
      <!-- No Image Layout -->
      <div v-else class="no-image-layout">
        <img :src="'http://localhost:5000/uploads/placeholder.svg'" :alt="item.title" class="item-image placeholder" />
      </div>
      
      <!-- Overlay Actions on Hover -->
      <div class="item-overlay">
        <div class="item-actions">
          <button 
            class="action-btn order-btn"
            @click="$emit('order-item', item)"
          >
            Order Now
          </button>
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
        <span class="price-value">₱{{ item.price.toFixed(2) }}</span>
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
  emits: ['contact-seller', 'save-item', 'order-item'],
  methods: {
    getItemImage(item) {
      // Handle direct image property (already processed)
      if (item?.image && typeof item.image === 'string') {
        return item.image;
      }
      
      // Handle primary image from API
      if (item?.primary_image?.url) {
        return item.primary_image.url;
      }
      
      // Handle primary_image as string (direct URL)
      if (item?.primary_image && typeof item.primary_image === 'string') {
        return item.primary_image;
      }
      
      // Handle images array from API  
      if (item?.images && Array.isArray(item.images) && item.images.length > 0) {
        const primaryImage = item.images.find(img => img.isPrimary);
        if (primaryImage?.url) {
          return primaryImage.url;
        }
        if (item.images[0]?.url) {
          return item.images[0].url;
        }
      }
      
      // Handle image_url property
      if (item?.image_url) {
        return item.image_url;
      }
      
      // Default placeholder
      return 'http://localhost:5000/uploads/placeholder.svg';
    },
    
    getItemImages(item) {
      // Get all images for the item
      let images = [];
      
      // Handle images array from API
      if (item?.images && Array.isArray(item.images) && item.images.length > 0) {
        images = item.images.filter(img => img.url);
      }
      // Handle primary_image as single image
      else if (item?.primary_image?.url) {
        images = [item.primary_image];
      }
      // Handle primary_image as string
      else if (item?.primary_image && typeof item.primary_image === 'string') {
        images = [{ url: item.primary_image, isPrimary: true }];
      }
      // Handle single image property
      else if (item?.image && typeof item.image === 'string') {
        images = [{ url: item.image, isPrimary: true }];
      }
      // Handle image_url property
      else if (item?.image_url) {
        images = [{ url: item.image_url, isPrimary: true }];
      }
      
      return images;
    },
    
    getPrimaryImage(item) {
      const images = this.getItemImages(item);
      // Find primary image or return first image
      return images.find(img => img.isPrimary) || images[0] || { url: 'http://localhost:5000/uploads/placeholder.svg' };
    },
    
    getSecondaryImages(item) {
      const images = this.getItemImages(item);
      // Return non-primary images, limit to 3 for display
      const secondaryImages = images.filter(img => !img.isPrimary);
      return secondaryImages.slice(0, 3);
    }
  }
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

/* Single Image Layout */
.single-image-layout {
  width: 100%;
  height: 100%;
}

.item-image.single,
.item-image.placeholder {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

/* Multiple Images Layout (Facebook style) */
.multiple-images-layout {
  display: flex;
  width: 100%;
  height: 100%;
  gap: 2px;
}

.primary-image-container {
  flex: 1;
  height: 100%;
}

.item-image.primary {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.secondary-images-container {
  flex: 0 0 50%;
  display: flex;
  flex-direction: column;
  gap: 2px;
  height: 100%;
}

.secondary-image-wrapper {
  flex: 1;
  position: relative;
  overflow: hidden;
}

.item-image.secondary {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

/* More images overlay */
.more-images-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 18px;
  font-weight: 600;
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

.order-btn {
  background: #007bff;
  color: white;
}

.order-btn:hover {
  background: #0056b3;
  transform: translateY(-1px);
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
  
  .multiple-images-layout {
    gap: 1px;
  }
  
  .secondary-images-container {
    gap: 1px;
  }
  
  .more-images-overlay {
    font-size: 14px;
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
