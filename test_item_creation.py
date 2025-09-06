#!/usr/bin/env python3
"""
Test script to verify item creation works with the corrected database schema
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app import create_app, db
from app.models.models import User, Item
import json

def test_item_creation():
    """Test creating an item with the correct database schema"""
    app = create_app()
    
    with app.app_context():
        try:
            # Find a seller user
            seller = User.query.filter_by(role='seller').first()
            if not seller:
                print("❌ No seller found in database")
                return False
            
            print(f"✅ Found seller: {seller.username} (ID: {seller.id})")
            
            # Test data matching your database schema
            test_item_data = {
                'title': 'Test Vintage Item',
                'description': 'This is a test vintage collectible item',
                'price': 99.99,
                'category': 'collectibles',
                'condition_status': 'good',  # Using the correct column name
                'seller_id': seller.id,
                'status': 'active',
                'year': 1980,
                'images': ['https://example.com/image1.jpg', 'https://example.com/image2.jpg']  # JSON array
            }
            
            # Create the item
            item = Item(**test_item_data)
            db.session.add(item)
            db.session.commit()
            
            print(f"✅ Item created successfully with ID: {item.id}")
            print(f"   Title: {item.title}")
            print(f"   Condition: {item.condition_status}")
            print(f"   Images: {item.images}")
            print(f"   Year: {item.year}")
            
            # Test the to_dict method
            item_dict = item.to_dict()
            print(f"✅ Item to_dict() works: {json.dumps(item_dict, indent=2)}")
            
            # Clean up - remove the test item
            db.session.delete(item)
            db.session.commit()
            print("✅ Test item cleaned up")
            
            return True
            
        except Exception as e:
            print(f"❌ Error creating item: {str(e)}")
            print(f"   Error type: {type(e).__name__}")
            db.session.rollback()
            return False

if __name__ == '__main__':
    print("🔧 Testing item creation with corrected database schema...")
    success = test_item_creation()
    if success:
        print("\n🎉 All tests passed! Your database schema is properly aligned.")
    else:
        print("\n💥 Tests failed. Check the error messages above.")
