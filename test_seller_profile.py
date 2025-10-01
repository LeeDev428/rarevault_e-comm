#!/usr/bin/env python3
"""
Test script to verify seller_profiles table and API functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app import create_app, db
from backend.app.models.models import User, SellerProfile

def test_seller_profile_model():
    """Test that the SellerProfile model matches the database schema"""
    app = create_app()
    
    with app.app_context():
        try:
            # Test creating a seller profile
            print("Testing SellerProfile model...")
            
            # Create a test user
            test_user = User(
                username='testsellerx',
                email='testsellerx@example.com',
                role='seller'
            )
            test_user.set_password('password123')
            
            db.session.add(test_user)
            db.session.commit()
            
            print(f"✅ Created test user: {test_user.id}")
            
            # Create a seller profile
            seller_profile = SellerProfile(
                user_id=test_user.id,
                business_name='Test Business',
                description='Test description for the business',
                phone='+1234567890',
                address='123 Test Street\nTest City, TC 12345',
                website='https://testbusiness.com',
                social_media={
                    'facebook': 'https://facebook.com/testbusiness',
                    'instagram': 'https://instagram.com/testbusiness',
                    'twitter': 'https://twitter.com/testbusiness',
                    'linkedin': 'https://linkedin.com/company/testbusiness'
                }
            )
            
            db.session.add(seller_profile)
            db.session.commit()
            
            print(f"✅ Created seller profile: {seller_profile.id}")
            
            # Test the to_dict method
            profile_dict = seller_profile.to_dict()
            print("✅ Profile to_dict output:")
            for key, value in profile_dict.items():
                print(f"   {key}: {value}")
            
            # Verify all expected fields are present
            expected_fields = [
                'id', 'user_id', 'business_name', 'description', 'phone', 
                'address', 'website', 'social_media', 'verification_status', 
                'rating', 'total_sales', 'created_at', 'updated_at'
            ]
            
            missing_fields = [field for field in expected_fields if field not in profile_dict]
            if missing_fields:
                print(f"❌ Missing fields: {missing_fields}")
            else:
                print("✅ All expected fields present in model")
            
            # Clean up
            db.session.delete(seller_profile)
            db.session.delete(test_user)
            db.session.commit()
            
            print("✅ Test completed successfully!")
            
        except Exception as e:
            print(f"❌ Error during test: {str(e)}")
            db.session.rollback()
            
            # Try to clean up anyway
            try:
                test_users = User.query.filter_by(username='testsellerx').all()
                for user in test_users:
                    # Delete associated profiles first
                    profiles = SellerProfile.query.filter_by(user_id=user.id).all()
                    for profile in profiles:
                        db.session.delete(profile)
                    db.session.delete(user)
                db.session.commit()
                print("🧹 Cleaned up test data")
            except:
                pass

if __name__ == "__main__":
    test_seller_profile_model()