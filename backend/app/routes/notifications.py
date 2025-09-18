from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.models import db, Order, Item, User

notifications_bp = Blueprint('notifications', __name__)

@notifications_bp.route('/api/notifications/count', methods=['GET'])
@jwt_required()
def get_notification_count():
    """Get count of confirmed orders for the authenticated user"""
    try:
        current_user_id = get_jwt_identity()
        
        # Count confirmed orders where user is the buyer
        confirmed_count = db.session.query(Order).filter(
            Order.buyer_id == current_user_id,
            Order.status == 'confirmed'
        ).count()
        
        return jsonify({
            'success': True,
            'notification_count': confirmed_count
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@notifications_bp.route('/api/notifications', methods=['GET'])
@jwt_required()
def get_notifications():
    """Get list of confirmed orders as notifications for the authenticated user"""
    try:
        current_user_id = get_jwt_identity()
        
        # Get confirmed orders with item and seller details
        notifications = db.session.query(Order, Item, User).join(
            Item, Order.item_id == Item.id
        ).join(
            User, Order.seller_id == User.id
        ).filter(
            Order.buyer_id == current_user_id,
            Order.status == 'confirmed'
        ).order_by(Order.confirmed_at.desc()).limit(20).all()
        
        notification_list = []
        for order, item, seller in notifications:
            notification_list.append({
                'id': order.id,
                'type': 'order_confirmed',
                'title': 'Order Confirmed',
                'message': f'Your order for "{item.title}" has been confirmed by {seller.username}',
                'order_id': order.id,
                'order_number': order.order_number,
                'item_title': item.title,
                'seller_name': seller.username,
                'amount': float(order.total_amount),
                'confirmed_at': order.confirmed_at.isoformat() if order.confirmed_at else None,
                'created_at': order.created_at.isoformat()
            })
        
        return jsonify({
            'success': True,
            'notifications': notification_list,
            'total_count': len(notification_list)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@notifications_bp.route('/api/notifications/mark-seen', methods=['POST'])
@jwt_required()
def mark_notifications_seen():
    """Mark confirmed orders as seen (for future enhancement)"""
    try:
        current_user_id = get_jwt_identity()
        
        # For now, just return success
        # In the future, you could add a 'seen' column to orders table
        # or create a user_notifications_seen table
        
        return jsonify({
            'success': True,
            'message': 'Notifications marked as seen'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500