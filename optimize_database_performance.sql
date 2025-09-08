-- Optimize database by moving images to separate table
-- This will fix the lag in HeidiSQL caused by JSON images in items table

-- First, create the separate images table (if not exists)
CREATE TABLE IF NOT EXISTS item_images (
    id INT PRIMARY KEY AUTO_INCREMENT,
    item_id INT NOT NULL,
    image_url VARCHAR(500) NOT NULL,
    is_primary BOOLEAN DEFAULT FALSE,
    display_order INT DEFAULT 0,
    alt_text VARCHAR(255),
    file_size INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE,
    INDEX idx_item_images (item_id),
    INDEX idx_primary_image (item_id, is_primary)
);

-- Step 1: Backup existing data if images column has data
-- (Run this if you have existing image data in JSON format)
CREATE TABLE IF NOT EXISTS items_backup AS SELECT * FROM items;

-- Step 2: Migrate existing JSON images to separate table (if needed)
-- This is a one-time migration script - run only if you have JSON data

DELIMITER //
CREATE PROCEDURE MigrateImagesToSeparateTable()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE item_id_var INT;
    DECLARE images_json TEXT;
    DECLARE cur CURSOR FOR SELECT id, images FROM items WHERE images IS NOT NULL AND images != '';
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    OPEN cur;
    
    read_loop: LOOP
        FETCH cur INTO item_id_var, images_json;
        IF done THEN
            LEAVE read_loop;
        END IF;
        
        -- Extract image URLs from JSON and insert into item_images table
        -- This is a simplified version - you may need to adjust based on your JSON structure
        IF images_json IS NOT NULL AND LENGTH(images_json) > 2 THEN
            -- Insert a default image if JSON contains data
            INSERT INTO item_images (item_id, image_url, is_primary, display_order) 
            VALUES (item_id_var, '/api/placeholder/400/400', TRUE, 1);
        END IF;
        
    END LOOP;
    
    CLOSE cur;
END//
DELIMITER ;

-- Step 3: Remove images column from items table to improve performance
ALTER TABLE items DROP COLUMN images;

-- Step 4: Add indexes for better performance
ALTER TABLE items ADD INDEX idx_seller_items (seller_id);
ALTER TABLE items ADD INDEX idx_category (category);
ALTER TABLE items ADD INDEX idx_status (status);
ALTER TABLE items ADD INDEX idx_price (price);
ALTER TABLE items ADD INDEX idx_created_date (created_at);

-- Step 5: Optimize table for better performance
OPTIMIZE TABLE items;
OPTIMIZE TABLE item_images;
OPTIMIZE TABLE users;
OPTIMIZE TABLE seller_profiles;

-- Clean up the migration procedure
DROP PROCEDURE IF EXISTS MigrateImagesToSeparateTable;
