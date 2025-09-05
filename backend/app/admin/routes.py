from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import User, Item

admin_bp = Blueprint('admin', __name__)

def require_admin():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return user and user.role == 'admin'

@admin_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def admin_dashboard():
    if not require_admin():
        return jsonify({'error': 'Admin access required'}), 403
    
    try:
        total_users = User.query.count()
        total_items = Item.query.count()
        active_items = Item.query.filter_by(status='available').count()
        
        return jsonify({
            'stats': {
                'total_users': total_users,
                'total_items': total_items,
                'active_items': active_items
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
def get_all_users():
    if not require_admin():
        return jsonify({'error': 'Admin access required'}), 403
    
    try:
        users = User.query.all()
        return jsonify({
            'users': [user.to_dict() for user in users]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/users/<int:user_id>/toggle-status', methods=['PATCH'])
@jwt_required()
def toggle_user_status(user_id):
    if not require_admin():
        return jsonify({'error': 'Admin access required'}), 403
    
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        user.is_active = not user.is_active
        db.session.commit()
        
        return jsonify({
            'message': f'User {"activated" if user.is_active else "deactivated"} successfully',
            'user': user.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
