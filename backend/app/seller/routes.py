from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.models import db, Item, User, ItemImage, Order, Rating
from datetime import datetime
import os
import base64
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
        
        # Add rating information and sold count to each item
        items_with_ratings = []
        for item in items.items:
            item_data = item.to_dict()
            
            # Get rating statistics for this item
            ratings = Rating.query.filter_by(item_id=item.id).all()
            if ratings:
                avg_rating = sum(r.rating for r in ratings) / len(ratings)
                item_data['average_rating'] = round(avg_rating, 1)
                item_data['rating_count'] = len(ratings)
            else:
                item_data['average_rating'] = None
                item_data['rating_count'] = 0
            
            # Get sold count for this item (orders with delivered status)
            sold_count = Order.query.filter_by(
                item_id=item.id, 
                status='delivered'
            ).count()
            item_data['sold_count'] = sold_count
            
            items_with_ratings.append(item_data)
        
        return jsonify({
            'items': items_with_ratings,
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
        required_fields = ['title', 'category', 'price', 'condition', 'description', 'stock']
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
            
        # Validate stock
        try:
            stock = int(data['stock'])
            if stock < 0:
                return jsonify({'error': 'Stock must be 0 or greater'}), 400
        except ValueError:
            return jsonify({'error': 'Invalid stock format'}), 400
        
        # Create new item with all the new columns
        item_data = {
            'title': data['title'],
            'description': data['description'],
            'price': price,
            'stock': stock,
            'category': data['category'],
            'seller_id': current_user_id,
            'status': 'active',
            'condition_status': data['condition'],
            'views': 0,
            'favorites': 0,
            'inquiries': 0,
            'engagement': 0.0,
            'isNegotiable': data.get('isNegotiable', False),
            'isAuthenticated': data.get('isAuthenticated', False),
            'tags': data.get('tags', [])
        }
        
        # Handle optional fields
        if data.get('year'):
            try:
                item_data['year'] = int(data['year'])
            except (ValueError, TypeError):
                pass
        
        # Create the item first
        item = Item(**item_data)
        db.session.add(item)
        db.session.flush()  # Flush to get the item ID
        
        # Handle images - store in separate ItemImage table
        if data.get('images'):
            for idx, image_data in enumerate(data['images']):
                if isinstance(image_data, dict) and 'url' in image_data:
                    image_url = image_data['url']
                    
                    # Handle base64 images
                    if image_url.startswith('data:image/'):
                        try:
                            # Extract base64 data
                            header, base64_data = image_url.split(',', 1)
                            image_format = header.split('/')[1].split(';')[0]
                            
                            # Create directory for item images
                            item_dir = os.path.join(UPLOAD_FOLDER, str(item.id))
                            os.makedirs(item_dir, exist_ok=True)
                            
                            # Generate filename
                            filename = f"image_{idx}.{image_format}"
                            file_path = os.path.join(item_dir, filename)
                            
                            # Decode and save image
                            import base64
                            with open(file_path, 'wb') as f:
                                f.write(base64.b64decode(base64_data))
                            
                            # Store relative path for database
                            relative_path = f"{item.id}/{filename}"
                            
                            item_image = ItemImage(
                                item_id=item.id,
                                image_path=relative_path,
                                is_primary=image_data.get('isPrimary', idx == 0),
                                display_order=idx,
                                original_filename=filename
                            )
                            db.session.add(item_image)
                            
                        except Exception as e:
                            print(f"Error processing image {idx}: {str(e)}")
                            continue
                    else:
                        # Handle regular URL (if uploading from URL)
                        item_image = ItemImage(
                            item_id=item.id,
                            image_path=image_url,
                            is_primary=image_data.get('isPrimary', idx == 0),
                            display_order=idx
                        )
                        db.session.add(item_image)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Item created successfully',
            'item': item.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"Error creating item: {str(e)}")  # Debug logging
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
        if 'stock' in data:
            try:
                stock = int(data['stock'])
                if stock < 0:
                    return jsonify({'error': 'Stock must be 0 or greater'}), 400
                item.stock = stock
            except ValueError:
                return jsonify({'error': 'Invalid stock format'}), 400
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

# ORDER MANAGEMENT ENDPOINTS
@seller_bp.route('/seller/orders', methods=['GET'])
@jwt_required()
def get_seller_orders():
    """Get orders for the seller"""
    try:
        current_user_id = int(get_jwt_identity())
        
        # Verify user is a seller
        user = User.query.get(current_user_id)
        if not user or user.role not in ['seller', 'admin']:
            return jsonify({'error': 'Access denied. Seller role required.'}), 403

        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 50)
        status_filter = request.args.get('status', '')
        
        # Build query using your database schema
        try:
            query = Order.query.filter_by(seller_id=current_user_id)
            
            if status_filter:
                query = query.filter_by(status=status_filter)
            
            query = query.order_by(Order.created_at.desc())  # Use created_at to match schema
            
            total = query.count()
            orders = query.offset((page - 1) * per_page).limit(per_page).all()
            
            print(f"Found {total} orders for seller {current_user_id}")
            
        except Exception as query_error:
            print(f"Error querying orders: {query_error}")
            # If query fails, return empty result
            return jsonify({
                'orders': [],
                'pagination': {
                    'page': 1,
                    'pages': 0,
                    'per_page': 20,
                    'total': 0,
                    'has_next': False,
                    'has_prev': False
                }
            }), 200
        
        # Format response with item and buyer details
        orders_data = []
        for order in orders:
            order_data = order.to_dict()
            
            # Get item details
            item = Item.query.get(order.item_id)
            if item:
                order_data['item'] = item.to_dict()
                # The item.to_dict() method already handles image loading safely
                # including primary image, so we don't need to query ItemImage separately
            
            # Get buyer details (limited info for privacy)
            buyer = User.query.get(order.buyer_id)
            if buyer:
                order_data['buyer'] = {
                    'id': buyer.id,
                    'username': buyer.username,
                    'first_name': buyer.first_name,
                    'last_name': buyer.last_name
                }
            
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

@seller_bp.route('/seller/orders/<int:order_id>/status', methods=['PUT'])
@jwt_required()
def update_order_status(order_id):
    """Update order status (confirm/decline/ship/etc.)"""
    try:
        current_user_id = int(get_jwt_identity())
        
        # Verify user is a seller
        user = User.query.get(current_user_id)
        if not user or user.role not in ['seller', 'admin']:
            return jsonify({'error': 'Access denied. Seller role required.'}), 403
        
        data = request.get_json()
        new_status = data.get('status')
        seller_notes = data.get('seller_notes', '')
        decline_reason = data.get('decline_reason', '')
        
        if new_status not in ['pending', 'confirmed', 'declined', 'shipped', 'delivered', 'cancelled']:
            return jsonify({'error': 'Invalid status'}), 400
        
        # Find order
        order = Order.query.filter_by(id=order_id, seller_id=current_user_id).first()
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        # Update order status and timestamps
        order.status = new_status
        order.seller_notes = seller_notes
        order.updated_at = datetime.utcnow()
        
        if new_status == 'confirmed':
            order.confirmed_at = datetime.utcnow()
        elif new_status == 'declined':
            order.declined_at = datetime.utcnow()
            order.decline_reason = decline_reason
        elif new_status == 'shipped':
            order.shipped_at = datetime.utcnow()
        elif new_status == 'delivered':
            order.delivered_at = datetime.utcnow()
        
        # Update item status based on order status and handle stock changes
        item = Item.query.get(order.item_id)
        if item:
            if new_status in ['confirmed', 'shipped']:
                item.status = 'sold' if new_status == 'shipped' else 'pending'
            elif new_status in ['declined', 'cancelled']:
                # Restore stock when order is declined or cancelled
                item.stock += order.quantity
                item.status = 'active'
            elif new_status == 'delivered':
                item.status = 'sold'
        
        db.session.commit()
        
        return jsonify({
            'message': f'Order status updated to {new_status}',
            'order': order.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@seller_bp.route('/seller/orders/<int:order_id>/confirm', methods=['PUT'])
@jwt_required()
def confirm_order(order_id):
    """Confirm an order"""
    try:
        current_user_id = int(get_jwt_identity())
        
        # Verify user is a seller
        user = User.query.get(current_user_id)
        if not user or user.role not in ['seller', 'admin']:
            return jsonify({'error': 'Access denied. Seller role required.'}), 403
        
        # Find order
        order = Order.query.filter_by(id=order_id, seller_id=current_user_id).first()
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        if order.status != 'pending':
            return jsonify({'error': 'Only pending orders can be confirmed'}), 400
        
        # Update order status
        order.status = 'confirmed'
        order.confirmed_at = datetime.utcnow()
        order.updated_at = datetime.utcnow()
        
        # Note: Item status should remain 'active' to allow other customers to order
        # Only the order status changes, not the item status
        
        db.session.commit()
        
        return jsonify({
            'message': 'Order confirmed successfully',
            'order': order.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@seller_bp.route('/seller/orders/<int:order_id>/cancel', methods=['PUT'])
@jwt_required()
def cancel_order(order_id):
    """Cancel an order"""
    try:
        current_user_id = int(get_jwt_identity())
        
        # Verify user is a seller
        user = User.query.get(current_user_id)
        if not user or user.role not in ['seller', 'admin']:
            return jsonify({'error': 'Access denied. Seller role required.'}), 403
        
        data = request.get_json() or {}
        cancel_reason = data.get('reason', '')
        
        # Find order
        order = Order.query.filter_by(id=order_id, seller_id=current_user_id).first()
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        if order.status not in ['pending', 'confirmed']:
            return jsonify({'error': 'Only pending or confirmed orders can be cancelled'}), 400
        
        # Update order status
        order.status = 'cancelled'
        order.cancelled_at = datetime.utcnow()
        order.updated_at = datetime.utcnow()
        order.seller_notes = cancel_reason
        
        # Restore stock when order is cancelled
        item = Item.query.get(order.item_id)
        if item:
            item.stock += order.quantity
            item.status = 'active'  # Make item available again
        
        db.session.commit()
        
        return jsonify({
            'message': 'Order cancelled successfully',
            'order': order.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@seller_bp.route('/seller/orders/<int:order_id>/complete', methods=['PUT'])
@jwt_required()
def complete_order(order_id):
    """Mark an order as completed"""
    try:
        current_user_id = int(get_jwt_identity())
        
        # Verify user is a seller
        user = User.query.get(current_user_id)
        if not user or user.role not in ['seller', 'admin']:
            return jsonify({'error': 'Access denied. Seller role required.'}), 403
        
        # Find order
        order = Order.query.filter_by(id=order_id, seller_id=current_user_id).first()
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        if order.status != 'confirmed':
            return jsonify({'error': 'Only confirmed orders can be completed'}), 400
        
        # Update order status
        order.status = 'completed'
        order.completed_at = datetime.utcnow()
        order.updated_at = datetime.utcnow()
        
        # Note: Item status should remain 'active' unless stock is depleted
        # Only the order status changes, not the item status
        # Item stock was already decremented when the order was placed
        
        db.session.commit()
        
        return jsonify({
            'message': 'Order completed successfully',
            'order': order.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@seller_bp.route('/ratings', methods=['GET'])
@jwt_required()
def get_seller_ratings():
    """Get all ratings for items sold by the seller"""
    try:
        current_user_id = int(get_jwt_identity())
        
        # Verify user is a seller
        user = User.query.get(current_user_id)
        if not user or user.role not in ['seller', 'admin']:
            return jsonify({'error': 'Access denied. Seller role required.'}), 403
        
        # Get ratings for all items sold by this seller
        ratings = db.session.query(Rating).join(Item, Rating.item_id == Item.id).filter(
            Item.seller_id == current_user_id
        ).order_by(Rating.created_at.desc()).all()
        
        # Calculate statistics
        total_ratings = len(ratings)
        if total_ratings > 0:
            average_rating = sum(r.rating for r in ratings) / total_ratings
            rating_distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
            for r in ratings:
                rating_distribution[r.rating] += 1
        else:
            average_rating = 0
            rating_distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        
        return jsonify({
            'ratings': [rating.to_dict() for rating in ratings],
            'statistics': {
                'total_ratings': total_ratings,
                'average_rating': round(average_rating, 2),
                'rating_distribution': rating_distribution
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
