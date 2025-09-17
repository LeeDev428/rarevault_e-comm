from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Numeric

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50))  # Match your DB schema
    last_name = db.Column(db.String(50))   # Match your DB schema
    role = db.Column(db.Enum('user', 'admin', 'seller'), default='user')  # Match your enum
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Item(db.Model):
    __tablename__ = 'items'
    
    id = db.Column(db.Integer, primary_key=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=1)
    category = db.Column(db.String(100))
    condition_status = db.Column(db.Enum('new', 'like_new', 'good', 'fair', 'poor'), default='good')
    status = db.Column(db.Enum('active', 'sold', 'pending', 'removed'), default='active')
    year = db.Column(db.Integer)  # Year field as in your database
    views = db.Column(db.Integer, default=0)
    favorites = db.Column(db.Integer, default=0)
    inquiries = db.Column(db.Integer, default=0)
    engagement = db.Column(Numeric(5, 2), default=0.0)
    isNegotiable = db.Column(db.Boolean, default=False)
    isAuthenticated = db.Column(db.Boolean, default=False)
    tags = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    images = db.relationship('ItemImage', backref='item', lazy='dynamic', cascade='all, delete-orphan')
    seller = db.relationship('User', backref='items')
    
    def to_dict(self):
        # Try to get images, but handle the case where table doesn't exist
        images_list = []
        primary_image = None
        
        try:
            # First, ensure the item_images table exists
            from sqlalchemy import text
            # Check if item_images table exists and create it if not
            try:
                db.engine.execute(text("SELECT 1 FROM item_images LIMIT 1"))
            except Exception as table_error:
                # Table doesn't exist, create it
                print(f"Creating item_images table...")
                db.engine.execute(text("""
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
                """))
                
            # Now try to get images from the relationship
            images_list = [image.to_dict() for image in self.images.all()]
            # Find primary image or use first image
            if images_list:
                primary_image = next((img for img in images_list if img.get('isPrimary')), images_list[0])
        except Exception as e:
            # If still can't access images, check file system
            print(f"Warning: Could not load images for item {self.id}: {e}")
            
            # Check if there are images in the uploads directory
            import os
            upload_dir = f"uploads/items/{self.id}"
            if os.path.exists(upload_dir):
                image_files = [f for f in os.listdir(upload_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
                if image_files:
                    # Create image objects from files
                    for i, image_file in enumerate(image_files):
                        image_url = f"http://localhost:5000/uploads/items/{self.id}/{image_file}"
                        images_list.append({
                            'id': i + 1,
                            'url': image_url,
                            'isPrimary': i == 0,
                            'created_at': None
                        })
                    primary_image = images_list[0] if images_list else None
        
        # Calculate real sales data from orders table
        from sqlalchemy import func
        sold_count = 0
        total_sales_quantity = 0
        
        try:
            # Get total quantity sold for this item from delivered orders
            sales_data = db.session.query(
                func.sum(Order.quantity).label('total_quantity'),
                func.count(Order.id).label('order_count')
            ).filter(
                Order.item_id == self.id,
                Order.status == 'delivered'
            ).first()
            
            if sales_data and sales_data.total_quantity:
                total_sales_quantity = int(sales_data.total_quantity)
                sold_count = int(sales_data.order_count)
        except Exception as e:
            print(f"Error calculating sales data: {e}")
        
        # Calculate real ratings data
        rating = 0.0
        rating_count = 0
        
        try:
            # Get average rating and count for this item
            rating_data = db.session.query(
                func.avg(Rating.rating).label('avg_rating'),
                func.count(Rating.id).label('rating_count')
            ).filter(Rating.item_id == self.id).first()
            
            if rating_data and rating_data.avg_rating:
                rating = float(rating_data.avg_rating)
                rating_count = int(rating_data.rating_count)
        except Exception as e:
            print(f"Error calculating rating data: {e}")
        
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'price': float(self.price) if self.price else None,
            'stock': self.stock,
            'condition': self.condition_status,
            'year': self.year,
            'seller_id': self.seller_id,
            'status': self.status,
            'views': self.views,
            'favorites': self.favorites,
            'inquiries': self.inquiries,
            'engagement': float(self.engagement) if self.engagement else 0.0,
            'isNegotiable': self.isNegotiable,
            'isAuthenticated': self.isAuthenticated,
            'tags': self.tags or [],
            'images': images_list,
            'primary_image': primary_image,
            # Real sales and ratings data
            'soldCount': total_sales_quantity,
            'totalOrders': sold_count,
            'rating': rating,
            'ratingCount': rating_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class ItemImage(db.Model):
    __tablename__ = 'item_images'
    
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    image_path = db.Column(db.String(500), nullable=False)
    is_primary = db.Column(db.Boolean, default=False)
    display_order = db.Column(db.Integer, default=0)
    original_filename = db.Column(db.String(255))
    file_size = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        # Construct the proper image URL
        if self.image_path:
            # If it's already a full URL, use it as is
            if self.image_path.startswith('http'):
                full_url = self.image_path
            # If it starts with 'items/', prepend the uploads path
            elif self.image_path.startswith('items/'):
                full_url = f"http://localhost:5000/uploads/{self.image_path}"
            # Otherwise, assume it's a filename and construct the full path
            else:
                full_url = f"http://localhost:5000/uploads/items/{self.item_id}/{self.image_path}"
        else:
            full_url = None
        
        return {
            'id': self.id,
            'url': full_url,
            'image_url': full_url,  # For backward compatibility
            'isPrimary': self.is_primary,
            'is_primary': self.is_primary,  # For backward compatibility
            'display_order': self.display_order,
            'original_filename': self.original_filename,
            'file_size': self.file_size,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(20), unique=True, nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    price_per_item = db.Column(Numeric(10, 2), nullable=False)
    total_amount = db.Column(Numeric(10, 2), nullable=False)
    status = db.Column(db.Enum('pending', 'confirmed', 'declined', 'shipped', 'delivered', 'cancelled'), default='pending')
    
    # Customer information
    shipping_address = db.Column(db.Text, nullable=False)
    customer_name = db.Column(db.String(255), nullable=False)
    customer_phone = db.Column(db.String(20))
    customer_email = db.Column(db.String(255))
    
    # Payment information
    payment_method = db.Column(db.String(50), default='cash_on_delivery')
    payment_status = db.Column(db.Enum('pending', 'paid', 'failed', 'refunded'), default='pending')
    
    # Order management
    customer_notes = db.Column(db.Text)
    seller_notes = db.Column(db.Text)
    decline_reason = db.Column(db.Text)
    tracking_number = db.Column(db.String(100))
    
    # Timestamps - exact match to your database schema
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    confirmed_at = db.Column(db.DateTime)
    declined_at = db.Column(db.DateTime)
    shipped_at = db.Column(db.DateTime)
    delivered_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    cancelled_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    
    # Relationships
    buyer = db.relationship('User', foreign_keys=[buyer_id], backref='purchases')
    seller = db.relationship('User', foreign_keys=[seller_id], backref='sales')
    item = db.relationship('Item', backref='orders')
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_number': self.order_number,
            'buyer_id': self.buyer_id,
            'seller_id': self.seller_id,
            'item_id': self.item_id,
            'quantity': self.quantity,
            'price_per_item': float(self.price_per_item) if self.price_per_item else None,
            'total_amount': float(self.total_amount) if self.total_amount else None,
            'status': self.status,
            
            # Customer information
            'shipping_address': self.shipping_address,
            'customer_name': self.customer_name,
            'customer_phone': self.customer_phone,
            'customer_email': self.customer_email,
            
            # Payment information
            'payment_method': self.payment_method,
            'payment_status': self.payment_status,
            
            # Order management
            'customer_notes': self.customer_notes,
            'seller_notes': self.seller_notes,
            'decline_reason': self.decline_reason,
            'tracking_number': self.tracking_number,
            
            # Timestamps
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'confirmed_at': self.confirmed_at.isoformat() if self.confirmed_at else None,
            'declined_at': self.declined_at.isoformat() if self.declined_at else None,
            'shipped_at': self.shipped_at.isoformat() if self.shipped_at else None,
            'delivered_at': self.delivered_at.isoformat() if self.delivered_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'cancelled_at': self.cancelled_at.isoformat() if self.cancelled_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

class Wishlist(db.Model):
    __tablename__ = 'wishlists'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='wishlist_items')
    item = db.relationship('Item', backref='wishlisted_by')
    
    # Ensure unique combination of user_id and item_id
    __table_args__ = (db.UniqueConstraint('user_id', 'item_id', name='unique_user_item'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'item_id': self.item_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    # Relationships
    user = db.relationship('User', backref='wishlist_items')
    item = db.relationship('Item', backref='wishlisted_by')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'item_id': self.item_id,
            'added_at': self.added_at.isoformat() if self.added_at else None
        }


class SellerProfile(db.Model):
    __tablename__ = 'seller_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    shop_name = db.Column(db.String(255))
    shop_description = db.Column(db.Text)
    meetup_preferences = db.Column(db.JSON)
    verification_status = db.Column(db.Enum('pending', 'verified', 'rejected'), default='pending')
    rating = db.Column(Numeric(3, 2), default=0.00)
    total_sales = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('seller_profile', uselist=False))
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'shop_name': self.shop_name,
            'shop_description': self.shop_description,
            'meetup_preferences': self.meetup_preferences,
            'verification_status': self.verification_status,
            'rating': float(self.rating) if self.rating else 0.00,
            'total_sales': self.total_sales,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Rating(db.Model):
    __tablename__ = 'ratings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    review = db.Column(db.Text, nullable=True)
    photo = db.Column(db.String(255), nullable=True)  # Single photo path/URL
    is_anonymous = db.Column(db.Boolean, default=False)
    helpful_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id], backref='ratings')
    item = db.relationship('Item', backref='ratings')
    order = db.relationship('Order', backref='ratings')
    seller = db.relationship('User', foreign_keys=[seller_id], backref='received_ratings')
    
    # Ensure unique combination of user_id and item_id
    __table_args__ = (db.UniqueConstraint('user_id', 'item_id', name='unique_user_item_rating'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'item_id': self.item_id,
            'order_id': self.order_id,
            'seller_id': self.seller_id,
            'rating': self.rating,
            'review': self.review,
            'photo': self.photo,
            'is_anonymous': self.is_anonymous,
            'helpful_count': self.helpful_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'user': self.user.to_dict() if self.user else None,
            'item': {
                'id': self.item.id,
                'title': self.item.title,
                'price': float(self.item.price)
            } if self.item else None
        }

class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages')
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref='received_messages')
    
    def to_dict(self):
        return {
            'id': self.id,
            'sender_id': self.sender_id,
            'receiver_id': self.receiver_id,
            'message': self.message,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'sender': {
                'id': self.sender.id,
                'username': self.sender.username,
                'role': self.sender.role
            } if self.sender else None,
            'receiver': {
                'id': self.receiver.id,
                'username': self.receiver.username,
                'role': self.receiver.role
            } if self.receiver else None
        }
