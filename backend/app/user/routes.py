from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.models import User, Item, Wishlist, Order, ItemImage
from sqlalchemy import or_, and_
import uuid
from datetime import datetime

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

# WISHLIST ENDPOINTS
@user_bp.route('/wishlist', methods=['GET'])
@jwt_required()
def get_user_wishlist():
    """Get user's wishlist items"""
    try:
        user_id = get_jwt_identity()
        if isinstance(user_id, str):
            user_id = int(user_id)
        
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 50)
        
        # Get user's wishlist items with pagination
        wishlist_query = db.session.query(Wishlist, Item).join(
            Item, Wishlist.item_id == Item.id
        ).filter(
            Wishlist.user_id == user_id,
            Item.status == 'active'
        ).order_by(Wishlist.created_at.desc())
        
        total = wishlist_query.count()
        wishlist_items = wishlist_query.offset((page - 1) * per_page).limit(per_page).all()
        
        # Format response
        items = []
        for wishlist, item in wishlist_items:
            item_data = item.to_dict()
            item_data['added_to_wishlist'] = wishlist.created_at.isoformat()
            item_data['wishlist_id'] = wishlist.id
            
            # Get primary image
            primary_image = ItemImage.query.filter_by(
                item_id=item.id, 
                is_primary=True
            ).first()
            
            if primary_image:
                item_data['primary_image'] = primary_image.to_dict()
            
            items.append(item_data)
        
        return jsonify({
            'items': items,
            'pagination': {
                'page': page,
                'pages': (total + per_page - 1) // per_page,
                'per_page': per_page,
                'total': total,
                'has_next': page * per_page < total,
                'has_prev': page > 1
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/wishlist/<int:item_id>', methods=['POST'])
@jwt_required()
def add_to_wishlist(item_id):
    """Add item to user's wishlist"""
    try:
        user_id = get_jwt_identity()
        if isinstance(user_id, str):
            user_id = int(user_id)
        
        # Check if item exists and is active
        item = Item.query.filter_by(id=item_id, status='active').first()
        if not item:
            return jsonify({'error': 'Item not found or not available'}), 404
        
        # Check if user is trying to save their own item
        if item.seller_id == user_id:
            return jsonify({'error': 'Cannot save your own item'}), 400
        
        # Check if already in wishlist
        existing = Wishlist.query.filter_by(user_id=user_id, item_id=item_id).first()
        if existing:
            return jsonify({'message': 'Item already in wishlist', 'wishlisted': True}), 200
        
        # Add to wishlist
        wishlist_item = Wishlist(
            user_id=user_id,
            item_id=item_id
        )
        
        db.session.add(wishlist_item)
        db.session.commit()
        
        return jsonify({
            'message': 'Item added to wishlist successfully',
            'wishlisted': True,
            'wishlist_id': wishlist_item.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_bp.route('/wishlist/<int:item_id>', methods=['DELETE'])
@jwt_required()
def remove_from_wishlist(item_id):
    """Remove item from user's wishlist"""
    try:
        user_id = get_jwt_identity()
        if isinstance(user_id, str):
            user_id = int(user_id)
        
        # Find and remove wishlist item
        wishlist_item = Wishlist.query.filter_by(user_id=user_id, item_id=item_id).first()
        if not wishlist_item:
            return jsonify({'error': 'Item not in wishlist'}), 404
        
        db.session.delete(wishlist_item)
        db.session.commit()
        
        return jsonify({
            'message': 'Item removed from wishlist successfully',
            'wishlisted': False
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ORDER ENDPOINTS
@user_bp.route('/orders', methods=['GET'])
@jwt_required()
def get_user_orders():
    """Get user's orders"""
    try:
        user_id = get_jwt_identity()
        if isinstance(user_id, str):
            user_id = int(user_id)
        
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 50)
        status_filter = request.args.get('status', '')
        
        # Build query
        query = Order.query.filter_by(buyer_id=user_id)
        
        if status_filter:
            query = query.filter_by(status=status_filter)
        
        query = query.order_by(Order.created_at.desc())
        
        total = query.count()
        orders = query.offset((page - 1) * per_page).limit(per_page).all()
        
        # Format response with item details
        orders_data = []
        for order in orders:
            order_data = order.to_dict()
            
            # Get item details
            item = Item.query.get(order.item_id)
            if item:
                order_data['item'] = item.to_dict()
                
                # Get primary image
                primary_image = ItemImage.query.filter_by(
                    item_id=item.id, 
                    is_primary=True
                ).first()
                
                if primary_image:
                    order_data['item']['primary_image'] = primary_image.to_dict()
            
            orders_data.append(order_data)
        
        return jsonify({
            'orders': orders_data,
            'pagination': {
                'page': page,
                'pages': (total + per_page - 1) // per_page,
                'per_page': per_page,
                'total': total,
                'has_next': page * per_page < total,
                'has_prev': page > 1
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/orders', methods=['POST'])
@jwt_required()
def create_order():
    """Create a new order"""
    try:
        user_id = get_jwt_identity()
        if isinstance(user_id, str):
            user_id = int(user_id)
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['item_id', 'shipping_address', 'customer_name']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        item_id = data['item_id']
        
        # Check if item exists and is available
        item = Item.query.filter_by(id=item_id, status='active').first()
        if not item:
            return jsonify({'error': 'Item not found or not available'}), 404
        
        # Check if user is trying to buy their own item
        if item.seller_id == user_id:
            return jsonify({'error': 'Cannot order your own item'}), 400
        
        # Generate unique order number
        order_number = f"ORD{datetime.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:8].upper()}"
        
        # Create order
        order = Order(
            order_number=order_number,
            buyer_id=user_id,
            seller_id=item.seller_id,
            item_id=item_id,
            quantity=data.get('quantity', 1),
            price_per_item=item.price,
            total_amount=item.price * data.get('quantity', 1),
            status='pending',
            
            # Customer information
            shipping_address=data['shipping_address'],
            customer_name=data['customer_name'],
            customer_phone=data.get('customer_phone', ''),
            customer_email=data.get('customer_email', ''),
            
            # Payment and notes
            payment_method=data.get('payment_method', 'cash_on_delivery'),
            customer_notes=data.get('customer_notes', '')
        )
        
        db.session.add(order)
        db.session.commit()
        
        return jsonify({
            'message': 'Order created successfully',
            'order': order.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
