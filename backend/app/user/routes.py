from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.models import User, Item
from sqlalchemy import or_, and_

user_bp = Blueprint('user', __name__)

@user_bp.route('/test-jwt', methods=['GET'])
@jwt_required()
def test_jwt():
    """Simple JWT test endpoint"""
    try:
        user_identity = get_jwt_identity()
        return jsonify({
            'identity': user_identity,
            'identity_type': str(type(user_identity)),
            'message': 'JWT token is valid'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/marketplace', methods=['GET'])
@jwt_required()
def get_marketplace_items():
    """Get all active items from sellers for the marketplace"""
    try:
        # Get user identity from JWT token
        user_identity = get_jwt_identity()
        print(f"JWT Identity: {user_identity}, type: {type(user_identity)}")
        
        if user_identity is None:
            return jsonify({'error': 'Invalid token - no user identity'}), 401
            
        # Handle both string and integer user IDs
        if isinstance(user_identity, str):
            try:
                user_id = int(user_identity)
            except ValueError:
                return jsonify({'error': f'Invalid user ID format: {user_identity}'}), 400
        elif isinstance(user_identity, int):
            user_id = user_identity
        else:
            return jsonify({'error': f'Invalid user ID type: {type(user_identity)}'}), 400
        
        # Verify user exists
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get query parameters for filtering
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        category = request.args.get('category')
        search = request.args.get('search')
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        condition_filter = request.args.get('condition')
        sort_by = request.args.get('sort_by', 'newest')  # newest, oldest, price_low, price_high
        
        # Build query for active items only
        query = Item.query.filter_by(status='active')
        
        # Apply filters
        if category:
            query = query.filter(Item.category == category)
        
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    Item.title.ilike(search_term),
                    Item.description.ilike(search_term),
                    Item.category.ilike(search_term)
                )
            )
        
        if min_price is not None:
            query = query.filter(Item.price >= min_price)
        
        if max_price is not None:
            query = query.filter(Item.price <= max_price)
        
        if condition_filter:
            query = query.filter(Item.condition_status == condition_filter)
        
        # Apply sorting
        if sort_by == 'newest':
            query = query.order_by(Item.created_at.desc())
        elif sort_by == 'oldest':
            query = query.order_by(Item.created_at.asc())
        elif sort_by == 'price_low':
            query = query.order_by(Item.price.asc())
        elif sort_by == 'price_high':
            query = query.order_by(Item.price.desc())
        else:
            query = query.order_by(Item.created_at.desc())
        
        # Paginate results
        items = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        # Get categories for filter dropdown
        categories = db.session.query(Item.category).filter(
            and_(Item.status == 'active', Item.category.isnot(None))
        ).distinct().all()
        categories = [cat[0] for cat in categories if cat[0]]
        
        return jsonify({
            'items': [item.to_dict() for item in items.items],
            'pagination': {
                'page': items.page,
                'pages': items.pages,
                'per_page': items.per_page,
                'total': items.total,
                'has_next': items.has_next,
                'has_prev': items.has_prev
            },
            'filters': {
                'categories': categories,
                'conditions': ['new', 'like_new', 'good', 'fair', 'poor']
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def user_dashboard():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        user_items = Item.query.filter_by(seller_id=user_id).all()
        
        return jsonify({
            'user': user.to_dict(),
            'items': [item.to_dict() for item in user_items]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/items', methods=['POST'])
@jwt_required()
def create_item():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        required_fields = ['title', 'description', 'category', 'price']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        item = Item(
            title=data['title'],
            description=data['description'],
            category=data['category'],
            price=data['price'],
            condition=data.get('condition'),
            year=data.get('year'),
            seller_id=user_id
        )
        
        db.session.add(item)
        db.session.commit()
        
        return jsonify({
            'message': 'Item created successfully',
            'item': item.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_bp.route('/items/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_item(item_id):
    try:
        user_id = get_jwt_identity()
        item = Item.query.filter_by(id=item_id, seller_id=user_id).first()
        
        if not item:
            return jsonify({'error': 'Item not found or unauthorized'}), 404
        
        data = request.get_json()
        
        # Update fields if provided
        updatable_fields = ['title', 'description', 'category', 'price', 'condition', 'year', 'status']
        for field in updatable_fields:
            if field in data:
                setattr(item, field, data[field])
        
        db.session.commit()
        
        return jsonify({
            'message': 'Item updated successfully',
            'item': item.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
