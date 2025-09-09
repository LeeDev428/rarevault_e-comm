#!/usr/bin/env python3
"""
Script to create the item_images table from your schema
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from sqlalchemy import text

def create_images_table():
    app = create_app()
    with app.app_context():
        try:
            print("Creating item_images table...")
            
            # Your exact table creation SQL from complete_database_schema.sql
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS `item_images` (
              `id` int NOT NULL AUTO_INCREMENT,
              `item_id` int NOT NULL,
              `image_url` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL,
              `is_primary` tinyint(1) DEFAULT '0',
              `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
              PRIMARY KEY (`id`),
              KEY `idx_item_id` (`item_id`),
              CONSTRAINT `item_images_ibfk_1` FOREIGN KEY (`item_id`) REFERENCES `items` (`id`) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """
            
            db.engine.execute(text(create_table_sql))
            print("✓ item_images table created successfully")
            
            # Now populate with existing images from file system
            from app.models.models import Item, ItemImage
            
            items = Item.query.all()
            print(f"Found {len(items)} items, checking for image files...")
            
            for item in items:
                upload_dir = f"../uploads/items/{item.id}"
                if os.path.exists(upload_dir):
                    image_files = [f for f in os.listdir(upload_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
                    print(f"Item {item.id}: Found {len(image_files)} image files")
                    
                    for i, image_file in enumerate(image_files):
                        # Check if image record already exists
                        existing = ItemImage.query.filter_by(item_id=item.id, image_url=f"items/{item.id}/{image_file}").first()
                        if not existing:
                            new_image = ItemImage(
                                item_id=item.id,
                                image_url=f"items/{item.id}/{image_file}",
                                is_primary=(i == 0)
                            )
                            db.session.add(new_image)
                            print(f"  Added: {image_file} (primary: {i == 0})")
            
            db.session.commit()
            print("✓ Image records created successfully")
            
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    create_images_table()
