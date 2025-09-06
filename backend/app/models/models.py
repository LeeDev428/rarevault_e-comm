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
    images = db.Column(db.JSON)  # JSON field as in your database
    year = db.Column(db.Integer)  # Year field as in your database
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    seller = db.relationship('User', backref=db.backref('items', lazy=True))
    
    @property
    def condition(self):
        """Handle different condition column names - maps to condition_status"""
        return self.condition_status
    
    @condition.setter
    def condition(self, value):
        """Handle different condition column names - maps to condition_status"""
        self.condition_status = value
    
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
            'images': self.images,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class ItemImage(db.Model):
    __tablename__ = 'item_images'
    
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    is_primary = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    item = db.relationship('Item', backref=db.backref('item_images', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'item_id': self.item_id,
            'image_url': self.image_url,
            'is_primary': self.is_primary,
            'created_at': self.created_at.isoformat() if self.created_at else None
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
