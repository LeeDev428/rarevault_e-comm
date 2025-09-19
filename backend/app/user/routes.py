from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.models import User, Item, Wishlist, Order, ItemImage, Rating
from sqlalchemy import or_, and_, text
import uuid
import os
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename

user_bp = Blueprint('user', __name__)

def ensure_item_images_table():
    """Ensure item_images table exists"""
    try:
        # Try to create the table if it doesn't exist
        create_table_sql = text("""
        CREATE TABLE IF NOT EXISTS `item_images` (
          `id` int NOT NULL AUTO_INCREMENT,
          `item_id` int NOT NULL,
          `image_path` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL,
          `is_primary` tinyint(1) DEFAULT '0',
          `display_order` int DEFAULT '0',
          `original_filename` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
          `file_size` int DEFAULT NULL,
          `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
          PRIMARY KEY (`id`),
          KEY `idx_item_id` (`item_id`),
          KEY `idx_primary` (`item_id`,`is_primary`),
          CONSTRAINT `item_images_ibfk_1` FOREIGN KEY (`item_id`) REFERENCES `items` (`id`) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """)
        db.engine.execute(create_table_sql)
        print("✓ item_images table ensured")
    except Exception as e:
        print(f"Warning: Could not ensure item_images table: {e}")

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
        
        # Format items with seller information and rating data
        items_data = []
        for item in items.items:
            item_data = item.to_dict()
            
            # Get seller information
            seller = User.query.get(item.seller_id)
            if seller:
                item_data['seller'] = {
                    'id': seller.id,
                    'username': seller.username,
                    'first_name': seller.first_name,
                    'last_name': seller.last_name
                }
                item_data['seller_name'] = seller.username
            
            # Get rating statistics for this item
            ratings = Rating.query.filter_by(item_id=item.id).all()
            if ratings:
                avg_rating = sum(r.rating for r in ratings) / len(ratings)
                item_data['rating'] = round(avg_rating, 1)
                item_data['ratingCount'] = len(ratings)
            else:
                item_data['rating'] = 0
                item_data['ratingCount'] = 0
            
            # Get sold count for this item (sum of quantities from delivered orders)
            sold_count = db.session.query(db.func.sum(Order.quantity)).filter_by(
                item_id=item.id, 
                status='delivered'
            ).scalar() or 0
            item_data['soldCount'] = sold_count
            
            items_data.append(item_data)
        
        return jsonify({
            'items': items_data,
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
def get_wishlist():
    """Get user's wishlist items"""
    try:
        ensure_item_images_table()  # Ensure table exists
        
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
            
            # Get primary image safely
            try:
                primary_image = ItemImage.query.filter_by(
                    item_id=item.id, 
                    is_primary=True
                ).first()
                
                if primary_image:
                    item_data['primary_image'] = primary_image.to_dict()
            except Exception as img_error:
                print(f"Warning: Could not load primary image for item {item.id}: {img_error}")
                # Continue without images
            
            # Get seller information
            seller = User.query.get(item.seller_id)
            if seller:
                item_data['seller'] = {
                    'id': seller.id,
                    'username': seller.username,
                    'first_name': seller.first_name,
                    'last_name': seller.last_name
                }
                item_data['seller_name'] = seller.username
            
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
    """Remove item from wishlist"""
    try:
        user_id = get_jwt_identity()
        if isinstance(user_id, str):
            user_id = int(user_id)
        
        # Find wishlist item by user_id and item_id
        wishlist_item = Wishlist.query.filter_by(user_id=user_id, item_id=item_id).first()
        if not wishlist_item:
            return jsonify({'error': 'Wishlist item not found'}), 404
        
        db.session.delete(wishlist_item)
        db.session.commit()
        
        return jsonify({'message': 'Item removed from wishlist successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ORDER ENDPOINTS
@user_bp.route('/orders', methods=['GET'])
@jwt_required()
def get_orders():
    """Get user's orders"""
    try:
        ensure_item_images_table()  # Ensure table exists
        
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
                
                # Get primary image safely
                try:
                    primary_image = ItemImage.query.filter_by(
                        item_id=item.id, 
                        is_primary=True
                    ).first()
                    
                    if primary_image:
                        order_data['item']['primary_image'] = primary_image.to_dict()
                except Exception as img_error:
                    print(f"Warning: Could not load primary image for item {item.id}: {img_error}")
                    # Continue without images
                
                # Get seller information
                seller = User.query.get(order.seller_id)
                if seller:
                    order_data['item']['seller'] = {
                        'id': seller.id,
                        'username': seller.username,
                        'first_name': seller.first_name,
                        'last_name': seller.last_name
                    }
                    order_data['item']['seller_name'] = seller.username
            
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
        
        # Get data
        item_id = data.get('item_id')
        if not item_id:
            return jsonify({'error': 'item_id is required'}), 400
        
        # Check if item exists and is available
        item = Item.query.filter_by(id=item_id, status='active').first()
        if not item:
            return jsonify({'error': 'Item not found or not available'}), 404

        # Check if user is trying to buy their own item
        if item.seller_id == user_id:
            return jsonify({'error': 'Cannot order your own item'}), 400
        
        # Validate quantity and check stock
        quantity = data.get('quantity', 1)
        if quantity <= 0:
            return jsonify({'error': 'Quantity must be greater than 0'}), 400
        
        # Check for recent duplicate orders (prevent double-clicking)
        recent_order = Order.query.filter_by(
            buyer_id=user_id,
            item_id=item_id
        ).filter(
            Order.created_at > datetime.now() - timedelta(minutes=1)
        ).first()
        
        if recent_order:
            return jsonify({
                'message': 'Order already created',
                'order': recent_order.to_dict()
            }), 200
        
        # Generate unique order number
        order_number = f"ORD{datetime.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:8].upper()}"
        
        # Create order with transaction safety
        try:
            # Create order
            order = Order(
                order_number=order_number,
                buyer_id=user_id,
                seller_id=item.seller_id,
                item_id=item_id,
                quantity=quantity,
                price_per_item=item.price,
                total_amount=item.price * quantity,
                status='pending',
                
                # Customer information - use defaults if empty
                shipping_address=data.get('shipping_address') or 'Not provided',
                customer_name=data.get('customer_name') or 'Not provided',
                customer_phone=data.get('customer_phone') or '',
                customer_email=data.get('customer_email') or '',
                
                # Payment and notes
                payment_method=data.get('payment_method', 'cash_on_delivery'),
                customer_notes=data.get('customer_notes', '')
            )
            
            # Reserve stock (deduct from available stock)
            item.stock -= quantity
            
            # If stock reaches 0, set item status to out_of_stock
            if item.stock <= 0:
                item.status = 'out_of_stock'
            
            db.session.add(order)
            db.session.commit()
            
            return jsonify({
                'message': 'Order created successfully',
                'order': order.to_dict()
            }), 201
            
        except Exception as e:
            db.session.rollback()
            print(f"Order creation error: {e}")
            return jsonify({'error': 'Failed to create order'}), 500
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@user_bp.route('/orders/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order_details(order_id):
    """Get details of a specific order"""
    try:
        current_user_id = get_jwt_identity()
        
        # Find the order and verify it belongs to the current user
        order = Order.query.filter_by(id=order_id, buyer_id=current_user_id).first()
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        # Get the order data with item details
        order_data = order.to_dict()
        
        # Ensure we have item details
        if order.item:
            item_data = order.item.to_dict()
            # Get item images
            try:
                images = ItemImage.query.filter_by(item_id=order.item.id).all()
                if images:
                    item_data['images'] = [img.to_dict() for img in images]
                    # Find primary image
                    primary_image = next((img for img in images if img.is_primary), images[0] if images else None)
                    if primary_image:
                        item_data['primary_image'] = primary_image.to_dict()
            except Exception as img_error:
                print(f"Error loading images for item {order.item.id}: {img_error}")
                item_data['images'] = []
            
            order_data['item'] = item_data
        
        return jsonify({'order': order_data}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user_bp.route('/orders/<int:order_id>/received', methods=['PUT'])
@jwt_required()
def mark_order_received(order_id):
    """Mark an order as received (delivered)"""
    try:
        current_user_id = get_jwt_identity()
        
        # Find the order and verify it belongs to the current user
        order = Order.query.filter_by(id=order_id, buyer_id=current_user_id).first()
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        # Check if order status is confirmed
        if order.status != 'confirmed':
            return jsonify({'error': 'Order must be confirmed to mark as received'}), 400
        
        # Update order status to delivered
        order.status = 'delivered'
        order.delivered_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Order marked as received successfully',
            'order': order.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@user_bp.route('/ratings', methods=['POST'])
@jwt_required()
def submit_rating():
    """Submit a rating and review for an item"""
    try:
        current_user_id = get_jwt_identity()
        
        # Get form data
        item_id = request.form.get('item_id')
        order_id = request.form.get('order_id')
        rating = request.form.get('rating')
        review = request.form.get('review')
        
        if not all([item_id, rating]):
            return jsonify({'error': 'Item ID and rating are required'}), 400
        
        # Validate rating is between 1-5
        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                return jsonify({'error': 'Rating must be between 1 and 5'}), 400
        except ValueError:
            return jsonify({'error': 'Rating must be a valid number'}), 400
        
        # Verify the item exists and get seller_id
        item = Item.query.get(item_id)
        if not item:
            return jsonify({'error': 'Item not found'}), 404
        
        seller_id = item.seller_id
        
        # If order_id is provided, verify the order exists and belongs to the user
        if order_id:
            order = Order.query.filter_by(id=order_id, buyer_id=current_user_id).first()
            if not order:
                return jsonify({'error': 'Order not found'}), 404
            # Also verify that the order's seller matches the item's seller
            if order.seller_id != seller_id:
                return jsonify({'error': 'Order and item seller mismatch'}), 400
        
        # Check if user already rated this item
        existing_rating = Rating.query.filter_by(
            user_id=current_user_id,
            item_id=item_id
        ).first()
        
        if existing_rating:
            return jsonify({'error': 'You have already rated this item'}), 400
        
        # Handle single photo upload (based on database schema)
        photo_url = None
        if 'photos' in request.files:
            photos = request.files.getlist('photos')
            if photos and photos[0].filename:  # Take only the first photo
                photo = photos[0]
                upload_folder = os.path.join('uploads', 'ratings', str(current_user_id))
                os.makedirs(upload_folder, exist_ok=True)
                
                filename = secure_filename(f"rating_{item_id}_{photo.filename}")
                filepath = os.path.join(upload_folder, filename)
                photo.save(filepath)
                photo_url = f'/uploads/ratings/{current_user_id}/{filename}'
        
        # Create new rating
        new_rating = Rating(
            user_id=current_user_id,
            item_id=item_id,
            order_id=order_id if order_id else None,
            seller_id=seller_id,
            rating=rating,
            review=review,
            photo=photo_url
        )
        
        db.session.add(new_rating)
        db.session.commit()
        
        return jsonify({
            'message': 'Rating submitted successfully',
            'rating': new_rating.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@user_bp.route('/ratings', methods=['GET'])
@jwt_required()
def get_user_ratings():
    """Get all ratings by the current user"""
    try:
        current_user_id = get_jwt_identity()
        
        ratings = Rating.query.filter_by(user_id=current_user_id).order_by(Rating.created_at.desc()).all()
        
        return jsonify({
            'ratings': [rating.to_dict() for rating in ratings]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user_bp.route('/items/<int:item_id>/ratings', methods=['GET'])
@jwt_required()
def get_item_ratings(item_id):
    """Get all ratings for a specific item"""
    try:
        # Verify the item exists
        item = Item.query.get(item_id)
        if not item:
            return jsonify({'error': 'Item not found'}), 404
        
        ratings = Rating.query.filter_by(item_id=item_id).order_by(Rating.created_at.desc()).all()
        
        # Calculate average rating
        if ratings:
            average_rating = sum(r.rating for r in ratings) / len(ratings)
        else:
            average_rating = 0
        
        return jsonify({
            'ratings': [rating.to_dict() for rating in ratings],
            'average_rating': round(average_rating, 2),
            'total_ratings': len(ratings)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user_bp.route('/ratings/check/<int:item_id>', methods=['GET'])
@jwt_required()
def check_rating_status(item_id):
    """Check if the current user has already rated a specific item"""
    try:
        current_user_id = get_jwt_identity()
        
        # Verify the item exists
        item = Item.query.get(item_id)
        if not item:
            return jsonify({'error': 'Item not found'}), 404
        
        # Check if user has already rated this item
        existing_rating = Rating.query.filter_by(
            user_id=current_user_id,
            item_id=item_id
        ).first()
        
        return jsonify({
            'is_rated': existing_rating is not None,
            'rating': existing_rating.to_dict() if existing_rating else None
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
