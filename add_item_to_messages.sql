-- Add item_id column to messages table for item-specific conversations
-- This allows messages to be linked to specific items for context

ALTER TABLE `messages` 
ADD COLUMN `item_id` int DEFAULT NULL AFTER `receiver_id`,
ADD COLUMN `order_id` int DEFAULT NULL AFTER `item_id`;

-- Add foreign key constraints
ALTER TABLE `messages` 
ADD CONSTRAINT `messages_ibfk_3` FOREIGN KEY (`item_id`) REFERENCES `items` (`id`) ON DELETE SET NULL,
ADD CONSTRAINT `messages_ibfk_4` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE SET NULL;

-- Add indexes for better performance
ALTER TABLE `messages` 
ADD INDEX `idx_item` (`item_id`),
ADD INDEX `idx_order` (`order_id`),
ADD INDEX `idx_item_conversation` (`item_id`, `sender_id`, `receiver_id`);

-- Update the conversation index to include item_id for better grouping
ALTER TABLE `messages` 
DROP INDEX `idx_conversation`,
ADD INDEX `idx_conversation` (`sender_id`, `receiver_id`, `item_id`);