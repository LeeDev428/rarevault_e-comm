from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.models import db, Item, User
from datetime import datetime
import os
from werkzeug.utils import secure_filename

seller_bp = Blueprint('seller', __name__)

# Configure upload settings
UPLOAD_FOLDER = 'uploads/items'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@seller_bp.route('/seller/dashboard/stats', methods=['GET'])
@jwt_required()
def get_seller_stats():
    try:
        current_user_id = int(get_jwt_identity())
        
        # Verify user is a seller
        user = User.query.get(current_user_id)
        if not user or user.role not in ['seller', 'admin']:
            return jsonify({'error': 'Access denied. Seller role required.'}), 403
        
        # Get seller statistics
        total_items = Item.query.filter_by(seller_id=current_user_id).count()
        active_items = Item.query.filter_by(seller_id=current_user_id, status='active').count()
        sold_items = Item.query.filter_by(seller_id=current_user_id, status='sold').count()
        pending_items = Item.query.filter_by(seller_id=current_user_id, status='pending').count()
        
        # Calculate total revenue from sold items
        sold_items_revenue = db.session.query(db.func.sum(Item.price)).filter_by(
            seller_id=current_user_id, status='sold'
        ).scalar() or 0
        
        return jsonify({
            'stats': {
                'total_items': total_items,
                'active_items': active_items,
                'sold_items': sold_items,
                'pending_items': pending_items,
                'total_revenue': float(sold_items_revenue)
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@seller_bp.route('/seller/items', methods=['GET'])
@jwt_required()
def get_seller_items():
    try:
        current_user_id = int(get_jwt_identity())
        
        # Verify user is a seller
        user = User.query.get(current_user_id)
        if not user or user.role not in ['seller', 'admin']:
            return jsonify({'error': 'Access denied. Seller role required.'}), 403
        
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status = request.args.get('status')
        category = request.args.get('category')
        search = request.args.get('search')
        
        # Build query
        query = Item.query.filter_by(seller_id=current_user_id)
        
        if status:
            query = query.filter_by(status=status)
        if category:
            query = query.filter_by(category=category)
        if search:
            query = query.filter(Item.title.contains(search))
        
        # Order by most recent first
        query = query.order_by(Item.created_at.desc())
        
        # Paginate
        items = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'items': [item.to_dict() for item in items.items],
            'pagination': {
                'page': items.page,
                'pages': items.pages,
                'per_page': items.per_page,
                'total': items.total
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Create new item
@seller_bp.route('/seller/items', methods=['POST'])
@jwt_required()
def create_seller_item():
    try:
        current_user_id = int(get_jwt_identity())  # Convert to int since it's stored as string
        
        # Verify user is a seller
        user = User.query.get(current_user_id)
        if not user or user.role not in ['seller', 'admin']:
            return jsonify({'error': 'Access denied. Seller role required.'}), 403
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'category', 'price', 'condition', 'description']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Validate price
        try:
            price = float(data['price'])
            if price <= 0:
                return jsonify({'error': 'Price must be greater than 0'}), 400
        except ValueError:
            return jsonify({'error': 'Invalid price format'}), 400
        
        # Create new item - dynamically handle different column names
        item_data = {
            'title': data['title'],
            'description': data['description'],
            'price': price,
            'category': data['category'],
            'seller_id': current_user_id,
            'status': 'active'
        }
        
        # Handle condition field (maps to condition_status column)
        item_data['condition_status'] = data['condition']
        
        # Handle optional fields
        if data.get('year'):
            try:
                item_data['year'] = int(data['year'])
            except (ValueError, TypeError):
                pass
        
        # Handle images as JSON field (matching your database schema)
        if data.get('images'):
            item_data['images'] = data['images']  # Store as JSON
        elif data.get('image_url'):
            # If single image_url provided, store as JSON array
            item_data['images'] = [data['image_url']]
        
        item = Item(**item_data)
        db.session.add(item)
        db.session.commit()
        
        return jsonify({
            'message': 'Item created successfully',
            'item': item.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@seller_bp.route('/seller/items/<int:item_id>', methods=['GET'])
@jwt_required()
def get_seller_item(item_id):
    try:
        current_user_id = int(get_jwt_identity())
        
        # Verify user is a seller
        user = User.query.get(current_user_id)
        if not user or user.role not in ['seller', 'admin']:
            return jsonify({'error': 'Access denied. Seller role required.'}), 403
        
        item = Item.query.filter_by(id=item_id, seller_id=current_user_id).first()
        if not item:
            return jsonify({'error': 'Item not found'}), 404
        
        return jsonify({'item': item.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Update item
@seller_bp.route('/seller/items/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_seller_item(item_id):
    try:
        current_user_id = int(get_jwt_identity())
        
        # Verify user is a seller
        user = User.query.get(current_user_id)
        if not user or user.role not in ['seller', 'admin']:
            return jsonify({'error': 'Access denied. Seller role required.'}), 403
        
        item = Item.query.filter_by(id=item_id, seller_id=current_user_id).first()
        if not item:
            return jsonify({'error': 'Item not found'}), 404
        
        data = request.get_json()
        
        # Update fields if provided
        if 'title' in data:
            item.title = data['title']
        if 'description' in data:
            item.description = data['description']
        if 'price' in data:
            try:
                price = float(data['price'])
                if price <= 0:
                    return jsonify({'error': 'Price must be greater than 0'}), 400
                item.price = price
            except ValueError:
                return jsonify({'error': 'Invalid price format'}), 400
        if 'category' in data:
            item.category = data['category']
        if 'condition' in data:
            item.condition = data['condition']
        if 'year' in data:
            item.year = data['year']
        if 'images' in data:
            item.images = data['images']
        if 'status' in data:
            item.status = data['status']
        
        item.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Item updated successfully',
            'item': item.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@seller_bp.route('/seller/items/<int:item_id>', methods=['DELETE'])
@jwt_required()
def delete_seller_item(item_id):
    try:
        current_user_id = int(get_jwt_identity())
        
        # Verify user is a seller
        user = User.query.get(current_user_id)
        if not user or user.role not in ['seller', 'admin']:
            return jsonify({'error': 'Access denied. Seller role required.'}), 403
        
        item = Item.query.filter_by(id=item_id, seller_id=current_user_id).first()
        if not item:
            return jsonify({'error': 'Item not found'}), 404
        
        db.session.delete(item)
        db.session.commit()
        
        return jsonify({'message': 'Item deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Upload item image
@seller_bp.route('/seller/items/upload-image', methods=['POST'])
@jwt_required()
def upload_item_image():
    try:
        current_user_id = int(get_jwt_identity())
        
        # Verify user is a seller
        user = User.query.get(current_user_id)
        if not user or user.role not in ['seller', 'admin']:
            return jsonify({'error': 'Access denied. Seller role required.'}), 403
        
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            # Create upload directory if it doesn't exist
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            
            # Generate secure filename
            filename = secure_filename(file.filename)
            timestamp = str(int(datetime.now().timestamp()))
            filename = f"{current_user_id}_{timestamp}_{filename}"
            
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            
            # Return the URL path
            images = f"/uploads/items/{filename}"
            
            return jsonify({
                'message': 'Image uploaded successfully',
                'images': images
            }), 200
        else:
            return jsonify({'error': 'Invalid file type'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@seller_bp.route('/seller/profile', methods=['GET'])
@jwt_required()
def get_seller_profile():
    try:
        current_user_id = int(get_jwt_identity())
        
        user = User.query.get(current_user_id)
        if not user or user.role not in ['seller', 'admin']:
            return jsonify({'error': 'Access denied. Seller role required.'}), 403
        
        return jsonify({'profile': user.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@seller_bp.route('/seller/profile', methods=['PUT'])
@jwt_required()
def update_seller_profile():
    try:
        current_user_id = int(get_jwt_identity())
        
        user = User.query.get(current_user_id)
        if not user or user.role not in ['seller', 'admin']:
            return jsonify({'error': 'Access denied. Seller role required.'}), 403
        
        data = request.get_json()
        
        # Update profile fields
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'email' in data:
            # Check if email is already taken
            existing_user = User.query.filter_by(email=data['email']).first()
            if existing_user and existing_user.id != current_user_id:
                return jsonify({'error': 'Email already in use'}), 400
            user.email = data['email']
        
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Profile updated successfully',
            'profile': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
