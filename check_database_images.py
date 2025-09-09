#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app import create_app
from backend.app.models.models import db, Item, ItemImage

app = create_app()

with app.app_context():
    print("=== CHECKING DATABASE IMAGES ===")
    
    # Check all items
    items = Item.query.all()
    print(f"Total items: {len(items)}")
    
    for item in items:
        print(f"\nItem {item.id}: {item.title}")
        
        # Check item images
        item_images = ItemImage.query.filter_by(item_id=item.id).all()
        print(f"  Images count: {len(item_images)}")
        
        for img in item_images:
            print(f"    Image {img.id}: {img.image_url} (primary: {img.is_primary})")
            
            # Check if file exists
            if img.image_url:
                if img.image_url.startswith('items/'):
                    file_path = f"backend/uploads/{img.image_url}"
                else:
                    file_path = f"backend/uploads/items/{img.image_url}"
                
                exists = os.path.exists(file_path)
                print(f"      File exists: {exists} ({file_path})")
        
        # Check item.to_dict() output
        item_dict = item.to_dict()
        print(f"  Primary image from to_dict(): {item_dict.get('primary_image')}")
        print(f"  Images from to_dict(): {len(item_dict.get('images', []))}")
