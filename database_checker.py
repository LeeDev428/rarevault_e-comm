#!/usr/bin/env python3
"""
Database checker script to verify table structure
"""
import sys
import os

# Add the backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))

try:
    from app import create_app, db
    from app.models.models import User, Item, ItemImage, Order, Wishlist
except ImportError as e:
    print(f"Import error: {e}")
    print("Please make sure you're running from the project root and the virtual environment is activated")
    sys.exit(1)

def check_database():
    app = create_app()
    
    with app.app_context():
        try:
            # Check if tables exist and have correct columns
            print("Checking database structure...")
            
            # Check items table
            print("\n=== Items Table ===")
            with db.engine.connect() as conn:
                result = conn.execute(db.text("DESCRIBE items"))
                columns = [row[0] for row in result]
                print(f"Columns: {columns}")
                
                required_columns = ['views', 'favorites', 'inquiries', 'engagement', 'isNegotiable', 'isAuthenticated', 'tags']
                missing_columns = [col for col in required_columns if col not in columns]
                
                if missing_columns:
                    print(f"❌ Missing columns: {missing_columns}")
                    print("Please run the safe_migration.sql script!")
                    return False
                else:
                    print("✅ All required columns present")
                
                # Check if ItemImage table exists
                print("\n=== ItemImage Table ===")
                try:
                    result = conn.execute(db.text("DESCRIBE item_images"))
                    img_columns = [row[0] for row in result]
                    print(f"Columns: {img_columns}")
                    print("✅ ItemImage table exists")
                except Exception as e:
                    print(f"❌ ItemImage table missing: {e}")
                    print("Please run the safe_migration.sql script!")
                    return False
            
            # Test creating an item
            print("\n=== Testing Item Creation ===")
            test_item = Item(
                title="Test Item",
                description="Test description",
                price=100.00,
                category="Test",
                condition_status="good",
                seller_id=1,
                views=0,
                favorites=0,
                inquiries=0,
                engagement=0.0,
                isNegotiable=False,
                isAuthenticated=False,
                tags=[]
            )
            
            print(f"✅ Item object created successfully")
            print(f"Item dict keys: {list(test_item.to_dict().keys())}")
            
            return True
            
        except Exception as e:
            print(f"❌ Database check failed: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    success = check_database()
    if success:
        print("\n🎉 Database structure is correct!")
    else:
        print("\n💥 Database structure needs to be updated!")
        print("Run the safe_migration.sql script to fix the issues.")
