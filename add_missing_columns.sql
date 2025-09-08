-- Add missing columns to items table
-- These columns are needed for the marketplace functionality

-- Add views column (track how many times item was viewed)
ALTER TABLE items 
ADD COLUMN views INT DEFAULT 0;

-- Add favorites column (track how many users favorited this item)
ALTER TABLE items 
ADD COLUMN favorites INT DEFAULT 0;

-- Add inquiries column (track how many inquiries were made)
ALTER TABLE items 
ADD COLUMN inquiries INT DEFAULT 0;

-- Add engagement column (engagement rate as percentage)
ALTER TABLE items 
ADD COLUMN engagement DECIMAL(5,2) DEFAULT 0.0;

-- Add isNegotiable column (whether price is negotiable)
ALTER TABLE items 
ADD COLUMN isNegotiable BOOLEAN DEFAULT FALSE;

-- Add isAuthenticated column (whether item is authenticated)
ALTER TABLE items 
ADD COLUMN isAuthenticated BOOLEAN DEFAULT FALSE;

-- Add tags column (JSON field for item tags)
ALTER TABLE items 
ADD COLUMN tags JSON;

-- Update existing items with default values
UPDATE items 
SET 
    views = 0,
    favorites = 0,
    inquiries = 0,
    engagement = 0.0,
    isNegotiable = FALSE,
    isAuthenticated = FALSE,
    tags = JSON_ARRAY()
WHERE views IS NULL;

-- Verify the new structure
DESCRIBE items;

-- Show sample data
SELECT id, title, views, favorites, inquiries, engagement, isNegotiable, isAuthenticated, tags
FROM items 
LIMIT 5;
