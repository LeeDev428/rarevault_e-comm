from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, Item

main_bp = Blueprint('main', __name__)

@main_bp.route('/items', methods=['GET'])
def get_items():
    try:
        items = Item.query.filter_by(status='available').all()
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
