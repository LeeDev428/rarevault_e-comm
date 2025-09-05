-- Add seller role to users table and create necessary tables for seller functionality

-- 1. Update users table to include 'seller' role (if using ENUM)
-- If your role column is ENUM, you need to modify it:
ALTER TABLE users MODIFY COLUMN role ENUM('user', 'admin', 'seller') NOT NULL DEFAULT 'user';

-- Or if using VARCHAR, this should already work:
-- ALTER TABLE users MODIFY COLUMN role VARCHAR(20) NOT NULL DEFAULT 'user';

-- 2. Create items table for sellers to manage their items
CREATE TABLE IF NOT EXISTS items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    seller_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    category VARCHAR(100),
    condition_status ENUM('new', 'like_new', 'good', 'fair', 'poor') DEFAULT 'good',
    status ENUM('active', 'sold', 'pending', 'removed') DEFAULT 'active',
    images JSON, -- Store image URLs as JSON array
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (seller_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_seller_id (seller_id),
    INDEX idx_status (status),
    INDEX idx_category (category)
);

-- 3. Create seller_profiles table for additional seller information
CREATE TABLE IF NOT EXISTS seller_profiles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    shop_name VARCHAR(255),
    shop_description TEXT,
    meetup_preferences JSON, -- Store meetup preferences as JSON
    verification_status ENUM('pending', 'verified', 'rejected') DEFAULT 'pending',
    rating DECIMAL(3, 2) DEFAULT 0.00,
    total_sales INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 4. Create item_images table for better image management
CREATE TABLE IF NOT EXISTS item_images (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_id INT NOT NULL,
    image_url VARCHAR(500) NOT NULL,
    is_primary BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE,
    INDEX idx_item_id (item_id)
);

-- 5. Insert sample seller users
INSERT INTO users (name, email, password, role) VALUES 
('John Seller', 'seller1@example.com', '$2b$12$hashedpassword1', 'seller'),
('Jane Merchant', 'seller2@example.com', '$2b$12$hashedpassword2', 'seller'),
('Mike Trader', 'seller3@example.com', '$2b$12$hashedpassword3', 'seller');

-- 6. Insert sample seller profiles
INSERT INTO seller_profiles (user_id, shop_name, shop_description, meetup_preferences) VALUES 
(
    (SELECT id FROM users WHERE email = 'seller1@example.com'),
    'John\'s Vintage Store',
    'Specializing in vintage collectibles and rare items',
    '{"public_meetup": true, "door_pickup": false, "door_delivery": true}'
),
(
    (SELECT id FROM users WHERE email = 'seller2@example.com'),
    'Jane\'s Antiques',
    'Quality antiques and vintage items',
    '{"public_meetup": true, "door_pickup": true, "door_delivery": false}'
),
(
    (SELECT id FROM users WHERE email = 'seller3@example.com'),
    'Mike\'s Rare Finds',
    'Rare and unique collectible items',
    '{"public_meetup": false, "door_pickup": true, "door_delivery": true}'
);

-- 7. Insert sample items
INSERT INTO items (seller_id, title, description, price, category, condition_status) VALUES 
(
    (SELECT id FROM users WHERE email = 'seller1@example.com'),
    'Vintage Watch',
    'Beautiful vintage watch from the 1950s',
    299.99,
    'Watches',
    'good'
),
(
    (SELECT id FROM users WHERE email = 'seller2@example.com'),
    'Antique Vase',
    'Rare Ming dynasty inspired vase',
    599.99,
    'Antiques',
    'like_new'
),
(
    (SELECT id FROM users WHERE email = 'seller3@example.com'),
    'Collectible Coin',
    'Rare 1932 silver dollar',
    199.99,
    'Coins',
    'good'
);
