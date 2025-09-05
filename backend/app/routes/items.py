from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.models import db, Item, User
from datetime import datetime

items_bp = Blueprint('items', __name__)

@items_bp.route('/items', methods=['GET'])
@jwt_required()
def get_items():
    try:
        items = Item.query.all()
        return jsonify({
            'items': [item.to_dict() for item in items]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@items_bp.route('/items', methods=['POST'])
@jwt_required()
def create_item():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'category', 'price', 'condition', 'description']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Create new item
        item = Item(
            title=data['title'],
            description=data['description'],
            price=float(data['price']),
            category=data['category'],
            condition=data['condition'],
            image_url=data.get('image_url', ''),
            seller_id=current_user_id,
            status=data.get('status', 'active')
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

@items_bp.route('/items/<int:item_id>', methods=['GET'])
@jwt_required()
def get_item(item_id):
    try:
        item = Item.query.get_or_404(item_id)
        return jsonify({'item': item.to_dict()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@items_bp.route('/items/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_item(item_id):
    try:
        current_user_id = get_jwt_identity()
        item = Item.query.get_or_404(item_id)
        
        # Check if user is the seller or admin
        current_user = User.query.get(current_user_id)
        if item.seller_id != current_user_id and current_user.role != 'admin':
            return jsonify({'error': 'Unauthorized to modify this item'}), 403
        
        data = request.get_json()
        
        # Update item fields
        if 'title' in data:
            item.title = data['title']
        if 'description' in data:
            item.description = data['description']
        if 'price' in data:
            item.price = float(data['price'])
        if 'category' in data:
            item.category = data['category']
        if 'condition' in data:
            item.condition = data['condition']
        if 'image_url' in data:
            item.image_url = data['image_url']
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

@items_bp.route('/items/<int:item_id>', methods=['DELETE'])
@jwt_required()
def delete_item(item_id):
    try:
        current_user_id = get_jwt_identity()
        item = Item.query.get_or_404(item_id)
        
        # Check if user is the seller or admin
        current_user = User.query.get(current_user_id)
        if item.seller_id != current_user_id and current_user.role != 'admin':
            return jsonify({'error': 'Unauthorized to delete this item'}), 403
        
        db.session.delete(item)
        db.session.commit()
        
        return jsonify({'message': 'Item deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@items_bp.route('/admin/users', methods=['GET'])
@jwt_required()
def get_all_users():
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        # Check if user is admin
        if current_user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        
        users = User.query.all()
        return jsonify({
            'users': [user.to_dict() for user in users]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
