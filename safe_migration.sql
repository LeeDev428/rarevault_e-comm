-- Simple migration to add missing columns without dropping tables
-- This will work with your existing data

-- Add missing columns to items table if they don't exist
SET @sql = '';
SELECT COUNT(*) INTO @col_count
FROM information_schema.columns 
WHERE table_schema = DATABASE() 
  AND table_name = 'items' 
  AND column_name = 'views';

SET @sql = IF(@col_count = 0, 'ALTER TABLE items ADD COLUMN views INT DEFAULT 0;', '');
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SELECT COUNT(*) INTO @col_count
FROM information_schema.columns 
WHERE table_schema = DATABASE() 
  AND table_name = 'items' 
  AND column_name = 'favorites';

SET @sql = IF(@col_count = 0, 'ALTER TABLE items ADD COLUMN favorites INT DEFAULT 0;', '');
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SELECT COUNT(*) INTO @col_count
FROM information_schema.columns 
WHERE table_schema = DATABASE() 
  AND table_name = 'items' 
  AND column_name = 'inquiries';

SET @sql = IF(@col_count = 0, 'ALTER TABLE items ADD COLUMN inquiries INT DEFAULT 0;', '');
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SELECT COUNT(*) INTO @col_count
FROM information_schema.columns 
WHERE table_schema = DATABASE() 
  AND table_name = 'items' 
  AND column_name = 'engagement';

SET @sql = IF(@col_count = 0, 'ALTER TABLE items ADD COLUMN engagement DECIMAL(5,2) DEFAULT 0.0;', '');
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SELECT COUNT(*) INTO @col_count
FROM information_schema.columns 
WHERE table_schema = DATABASE() 
  AND table_name = 'items' 
  AND column_name = 'isNegotiable';

SET @sql = IF(@col_count = 0, 'ALTER TABLE items ADD COLUMN isNegotiable BOOLEAN DEFAULT FALSE;', '');
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SELECT COUNT(*) INTO @col_count
FROM information_schema.columns 
WHERE table_schema = DATABASE() 
  AND table_name = 'items' 
  AND column_name = 'isAuthenticated';

SET @sql = IF(@col_count = 0, 'ALTER TABLE items ADD COLUMN isAuthenticated BOOLEAN DEFAULT FALSE;', '');
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SELECT COUNT(*) INTO @col_count
FROM information_schema.columns 
WHERE table_schema = DATABASE() 
  AND table_name = 'items' 
  AND column_name = 'tags';

SET @sql = IF(@col_count = 0, 'ALTER TABLE items ADD COLUMN tags JSON;', '');
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Create item_images table if it doesn't exist
CREATE TABLE IF NOT EXISTS item_images (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_id INT NOT NULL,
    image_path VARCHAR(500) NOT NULL,
    is_primary BOOLEAN DEFAULT FALSE,
    display_order INT DEFAULT 0,
    original_filename VARCHAR(255),
    file_size INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE,
    INDEX idx_item_id (item_id),
    INDEX idx_primary (item_id, is_primary)
);

-- Create orders table if it doesn't exist
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    item_id INT NOT NULL,
    seller_id INT NOT NULL,
    quantity INT DEFAULT 1,
    price_at_order DECIMAL(10,2) NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    status ENUM('pending', 'confirmed', 'shipped', 'delivered', 'cancelled') DEFAULT 'pending',
    shipping_address TEXT,
    payment_method VARCHAR(50),
    payment_status ENUM('pending', 'paid', 'failed', 'refunded') DEFAULT 'pending',
    notes TEXT,
    tracking_number VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE,
    FOREIGN KEY (seller_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_orders (user_id),
    INDEX idx_seller_orders (seller_id),
    INDEX idx_item_orders (item_id),
    INDEX idx_status (status)
);

-- Create wishlists table if it doesn't exist
CREATE TABLE IF NOT EXISTS wishlists (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    item_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_item (user_id, item_id),
    INDEX idx_user_wishlist (user_id)
);

-- Update existing items with default values for new columns
UPDATE items 
SET 
    views = COALESCE(views, 0),
    favorites = COALESCE(favorites, 0),
    inquiries = COALESCE(inquiries, 0),
    engagement = COALESCE(engagement, 0.0),
    isNegotiable = COALESCE(isNegotiable, FALSE),
    isAuthenticated = COALESCE(isAuthenticated, FALSE),
    tags = COALESCE(tags, JSON_ARRAY())
WHERE id IS NOT NULL;

-- Add some sample placeholder images for existing items (you can remove this if not needed)
INSERT IGNORE INTO item_images (item_id, image_path, is_primary, display_order, original_filename)
SELECT 
    id,
    CONCAT('items/', id, '/placeholder.jpg'),
    TRUE,
    0,
    'placeholder.jpg'
FROM items 
WHERE NOT EXISTS (
    SELECT 1 FROM item_images WHERE item_images.item_id = items.id
);

-- Show final structure
DESCRIBE items;
SELECT COUNT(*) as item_count FROM items;
SELECT COUNT(*) as image_count FROM item_images;
SELECT COUNT(*) as order_count FROM orders;
SELECT COUNT(*) as wishlist_count FROM wishlists;
