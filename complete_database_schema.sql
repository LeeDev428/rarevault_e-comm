-- Complete database schema for RareVault
-- Drop existing tables if they exist (in correct order due to foreign keys)
DROP TABLE IF EXISTS wishlists;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS item_images;
DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS seller_profiles;

-- Create items table with all necessary columns
CREATE TABLE items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    seller_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    category VARCHAR(100),
    condition_status ENUM('new', 'like_new', 'good', 'fair', 'poor') DEFAULT 'good',
    status ENUM('active', 'sold', 'pending', 'removed') DEFAULT 'active',
    year INT,
    views INT DEFAULT 0,
    favorites INT DEFAULT 0,
    inquiries INT DEFAULT 0,
    engagement DECIMAL(5,2) DEFAULT 0.0,
    isNegotiable BOOLEAN DEFAULT FALSE,
    isAuthenticated BOOLEAN DEFAULT FALSE,
    tags JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (seller_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_seller (seller_id),
    INDEX idx_category (category),
    INDEX idx_status (status),
    INDEX idx_created (created_at)
);

-- Create item_images table to store image file paths
CREATE TABLE item_images (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_id INT NOT NULL,
    image_path VARCHAR(500) NOT NULL,  -- Store file path like 'uploads/items/123/image1.jpg'
    is_primary BOOLEAN DEFAULT FALSE,
    display_order INT DEFAULT 0,
    original_filename VARCHAR(255),  -- Store original filename
    file_size INT,  -- Store file size in bytes
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE,
    INDEX idx_item_id (item_id),
    INDEX idx_primary (item_id, is_primary)
);

-- Create seller_profiles table
CREATE TABLE seller_profiles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    business_name VARCHAR(255),
    description TEXT,
    phone VARCHAR(20),
    address TEXT,
    website VARCHAR(255),
    social_media JSON,  -- Store social media links as JSON
    verification_status ENUM('pending', 'verified', 'rejected') DEFAULT 'pending',
    rating DECIMAL(3,2) DEFAULT 0.0,
    total_sales INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user (user_id)
);

-- Create orders table
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_number VARCHAR(20) UNIQUE NOT NULL,
    buyer_id INT NOT NULL,
    seller_id INT NOT NULL,
    item_id INT NOT NULL,
    quantity INT DEFAULT 1,
    price_per_item DECIMAL(10,2) NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    status ENUM('pending', 'confirmed', 'declined', 'shipped', 'delivered', 'cancelled') DEFAULT 'pending',
    
    -- Customer information
    shipping_address TEXT NOT NULL,
    customer_name VARCHAR(255) NOT NULL,
    customer_phone VARCHAR(20),
    customer_email VARCHAR(255),
    
    -- Payment information
    payment_method VARCHAR(50) DEFAULT 'cash_on_delivery',
    payment_status ENUM('pending', 'paid', 'failed', 'refunded') DEFAULT 'pending',
    
    -- Order management
    customer_notes TEXT,
    seller_notes TEXT,
    decline_reason TEXT,
    tracking_number VARCHAR(100),
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    confirmed_at TIMESTAMP NULL,
    declined_at TIMESTAMP NULL,
    shipped_at TIMESTAMP NULL,
    delivered_at TIMESTAMP NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (buyer_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (seller_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE,
    INDEX idx_buyer_orders (buyer_id),
    INDEX idx_seller_orders (seller_id),
    INDEX idx_item_orders (item_id),
    INDEX idx_status (status),
    INDEX idx_order_number (order_number)
);

-- Create wishlists table (for save functionality)
CREATE TABLE wishlists (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    item_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_item (user_id, item_id),
    INDEX idx_user_wishlist (user_id)
);

-- Insert sample data for testing
INSERT INTO items (seller_id, title, description, price, category, condition_status, year, tags) VALUES
(1, 'Vintage Rolex Submariner', 'Authentic 1965 Rolex Submariner in excellent condition', 8500.00, 'Watches', 'good', 1965, '["vintage", "rolex", "luxury", "collectible"]'),
(1, 'Antique Victorian Vase', 'Beautiful hand-painted Victorian era vase', 350.00, 'Antiques', 'fair', 1880, '["antique", "victorian", "pottery", "collectible"]'),
(1, 'Rare Baseball Card Collection', 'Complete set of 1952 Topps baseball cards', 2500.00, 'Collectibles', 'good', 1952, '["baseball", "cards", "sports", "vintage"]');

-- Insert sample images (you'll need to create these folders and files)
INSERT INTO item_images (item_id, image_path, is_primary, display_order, original_filename) VALUES
(1, 'uploads/items/1/rolex_main.jpg', TRUE, 0, 'rolex_submariner_front.jpg'),
(1, 'uploads/items/1/rolex_side.jpg', FALSE, 1, 'rolex_submariner_side.jpg'),
(2, 'uploads/items/2/vase_main.jpg', TRUE, 0, 'victorian_vase.jpg'),
(3, 'uploads/items/3/cards_main.jpg', TRUE, 0, 'baseball_cards_collection.jpg');

-- Create indexes for better performance
CREATE INDEX idx_items_search ON items (title, category, status);
CREATE INDEX idx_items_price ON items (price);
CREATE INDEX idx_orders_date ON orders (created_at);

-- Show the table structures
SHOW CREATE TABLE items;
SHOW CREATE TABLE item_images;
SHOW CREATE TABLE orders;
SHOW CREATE TABLE wishlists;
