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
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'price': float(self.price) if self.price else None,
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
            'images': [image.to_dict() for image in self.images],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class ItemImage(db.Model):
    __tablename__ = 'item_images'
    
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    image_path = db.Column(db.String(500), nullable=False)  # Store file path
    is_primary = db.Column(db.Boolean, default=False)
    display_order = db.Column(db.Integer, default=0)
    original_filename = db.Column(db.String(255))  # Store original filename
    file_size = db.Column(db.Integer)  # Store file size in bytes
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        # Convert file path to URL for frontend
        base_url = "http://localhost:5000/uploads"
        image_url = f"{base_url}/{self.image_path}" if self.image_path else None
        
        return {
            'id': self.id,
            'url': image_url,  # Frontend expects 'url'
            'path': self.image_path,  # Raw path for backend use
            'isPrimary': self.is_primary,
            'displayOrder': self.display_order,
            'originalFilename': self.original_filename,
            'fileSize': self.file_size,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(20), unique=True, nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
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
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    confirmed_at = db.Column(db.DateTime)
    declined_at = db.Column(db.DateTime)
    shipped_at = db.Column(db.DateTime)
    delivered_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
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
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
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
