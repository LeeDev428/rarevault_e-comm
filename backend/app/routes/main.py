from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.models import db, User, Item, Order
from datetime import datetime
import uuid

main_bp = Blueprint('main', __name__)

@main_bp.route('/items', methods=['GET'])
def get_items():
    try:
        # Get all active items (not sold, pending, or removed)
        items = Item.query.filter_by(status='active').all()
        return jsonify({
            'items': [item.to_dict() for item in items]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main_bp.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    try:
        item = Item.query.get(item_id)
        if not item:
            return jsonify({'error': 'Item not found'}), 404
        
        return jsonify({'item': item.to_dict()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# DISABLED - Use /api/user/orders instead to prevent duplication
# @main_bp.route('/orders', methods=['POST'])
# @jwt_required()
# def create_order():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # Get basic required data
        item_id = data.get('item_id')
        if not item_id:
            return jsonify({'error': 'item_id is required'}), 400
        
        # Get the item
        item = Item.query.get(item_id)
        if not item:
            return jsonify({'error': 'Item not found'}), 404
        
        # Check if item is available
        if item.status != 'active':
            return jsonify({'error': 'Item is not available for purchase'}), 400
        
        # Check stock availability
        if data['quantity'] > item.stock:
            return jsonify({'error': 'Insufficient stock available'}), 400
        
        # Prevent self-purchase
        if item.seller_id == current_user_id:
            return jsonify({'error': 'You cannot order your own item'}), 400
        
        # Generate unique order number
        order_number = f"ORD-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"
        
        # Calculate total amount
        price_per_item = item.price
        total_amount = price_per_item * data['quantity']
        
        # Create the order
        order = Order(
            order_number=order_number,
            buyer_id=current_user_id,
            seller_id=item.seller_id,
            item_id=item.id,
            quantity=data['quantity'],
            price_per_item=price_per_item,
            total_amount=total_amount,
            shipping_address=data['shipping_address'],
            customer_name=data['customer_name'],
            customer_phone=data['customer_phone'],
            customer_email=data.get('customer_email', ''),
            payment_method=data.get('payment_method', 'cash_on_delivery'),
            customer_notes=data.get('customer_notes', ''),
            status='pending'
        )
        
        db.session.add(order)
        db.session.commit()
        
        return jsonify({
            'message': 'Order created successfully',
            'order': order.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"Error creating order: {e}")
        return jsonify({'error': str(e)}), 500
