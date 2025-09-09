-- Add missing timestamp fields to orders table
ALTER TABLE orders 
ADD COLUMN cancelled_at DATETIME NULL,
ADD COLUMN completed_at DATETIME NULL;

-- Update existing cancelled orders
UPDATE orders SET cancelled_at = updated_at WHERE status = 'cancelled' AND cancelled_at IS NULL;

-- Update existing completed/delivered orders  
UPDATE orders SET completed_at = updated_at WHERE status IN ('completed', 'delivered') AND completed_at IS NULL;
