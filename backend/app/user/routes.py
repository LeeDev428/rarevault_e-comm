from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import User, Item

user_bp = Blueprint('user', __name__)

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
