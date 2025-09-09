#!/usr/bin/env python3

import sys
import os

# Add the backend directory to the Python path
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_dir)

from app import create_app
from app.models.models import Item, ItemImage, db

app = create_app()

with app.app_context():
    print("=== DEBUG: Checking Items and Images ===")
    
    # Get all items
    items = Item.query.all()
    print(f"Total items in database: {len(items)}")
    
    for item in items:
        print(f"\nItem ID: {item.id}, Title: {item.title}")
        images = ItemImage.query.filter_by(item_id=item.id).all()
        print(f"  Images count: {len(images)}")
        
        for img in images:
            print(f"    Image ID: {img.id}")
            print(f"    Path: {img.image_path}")
            print(f"    Is Primary: {img.is_primary}")
            print(f"    Full URL: http://localhost:5000/uploads/{img.image_path}")
            
            # Check if file exists
            full_path = os.path.join("uploads", img.image_path)
            file_exists = os.path.exists(full_path)
            print(f"    File exists: {file_exists}")
            
        # Test to_dict method
        item_dict = item.to_dict()
        print(f"  Primary image from to_dict(): {item_dict.get('primary_image')}")
        print(f"  Images array length: {len(item_dict.get('images', []))}")
