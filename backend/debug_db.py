from app import create_app
from app.models.models import Item, ItemImage, db
import os

app = create_app()

with app.app_context():
    print("=== DEBUG: Checking Items and Images ===")
    
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
            url = f"http://localhost:5000/uploads/{img.image_path}"
            print(f"    Full URL: {url}")
            
            full_path = os.path.join("uploads", img.image_path)
            file_exists = os.path.exists(full_path)
            print(f"    File exists: {file_exists}")
            
        item_dict = item.to_dict()
        primary_img = item_dict.get("primary_image")
        print(f"  Primary image from to_dict(): {primary_img}")
        images_count = len(item_dict.get("images", []))
        print(f"  Images array length: {images_count}")
