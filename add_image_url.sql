-- Add image_url column to items table
ALTER TABLE items ADD COLUMN image_url VARCHAR(500) DEFAULT '';

-- Update existing items with default empty string for image_url
UPDATE items SET image_url = '' WHERE image_url IS NULL;
