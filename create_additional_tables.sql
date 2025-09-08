-- Create item_images table (separate from items table for better performance)
CREATE TABLE IF NOT EXISTS item_images (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_id INT NOT NULL,
    image_url VARCHAR(500) NOT NULL,
    is_primary BOOLEAN DEFAULT FALSE,
    display_order INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE,
    INDEX idx_item_id (item_id),
    INDEX idx_primary (item_id, is_primary)
);

-- Create orders table
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

-- Create wishlists table (for save functionality)
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

-- Migrate existing image data from items.images JSON column to item_images table
-- (This is a one-time migration script)
INSERT INTO item_images (item_id, image_url, is_primary, display_order)
SELECT 
    i.id as item_id,
    JSON_UNQUOTE(JSON_EXTRACT(img.value, '$.url')) as image_url,
    CASE 
        WHEN JSON_EXTRACT(img.value, '$.isPrimary') = 'true' THEN TRUE 
        ELSE FALSE 
    END as is_primary,
    (img.index_pos) as display_order
FROM items i
CROSS JOIN JSON_TABLE(
    COALESCE(i.images, '[]'),
    '$[*]' COLUMNS (
        index_pos FOR ORDINALITY,
        value JSON PATH '$'
    )
) AS img
WHERE i.images IS NOT NULL 
  AND JSON_LENGTH(i.images) > 0;

-- After migration, you can optionally remove the images column from items table
-- ALTER TABLE items DROP COLUMN images;

-- Verify the migration
SELECT 
    i.id,
    i.title,
    COUNT(img.id) as image_count,
    GROUP_CONCAT(img.image_url ORDER BY img.display_order) as image_urls
FROM items i
LEFT JOIN item_images img ON i.id = img.item_id
GROUP BY i.id, i.title
LIMIT 10;
