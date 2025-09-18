from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.models import db, Order, Message, Item, User

seller_notifications_bp = Blueprint('seller_notifications', __name__)

@seller_notifications_bp.route('/api/seller/notifications/count', methods=['GET'])
@jwt_required()
def get_seller_notification_count():
    """Get count of pending and delivered orders for seller"""
    try:
        current_user_id = get_jwt_identity()
        
        # Count orders where seller is current user and status is pending or delivered
        order_count = db.session.query(Order).filter(
            Order.seller_id == current_user_id,
            Order.status.in_(['pending', 'delivered'])
        ).count()
        
        return jsonify({
            'success': True,
            'notification_count': order_count
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@seller_notifications_bp.route('/api/seller/notifications', methods=['GET'])
@jwt_required()
def get_seller_notifications():
    """Get list of pending and delivered orders as notifications for seller"""
    try:
        current_user_id = get_jwt_identity()
        
        # Get pending and delivered orders with item and buyer details
        notifications = db.session.query(Order, Item, User).join(
            Item, Order.item_id == Item.id
        ).join(
            User, Order.buyer_id == User.id
        ).filter(
            Order.seller_id == current_user_id,
            Order.status.in_(['pending', 'delivered'])
        ).order_by(Order.created_at.desc()).limit(20).all()
        
        notification_list = []
        for order, item, buyer in notifications:
            if order.status == 'pending':
                title = 'New Order Received'
                message = f'You have a new order from {buyer.username} for "{item.title}"'
            else:  # delivered
                title = 'Order Delivered'
                message = f'Order #{order.order_number} for "{item.title}" has been delivered'
            
            notification_list.append({
                'id': order.id,
                'type': f'order_{order.status}',
                'title': title,
                'message': message,
                'order_id': order.id,
                'order_number': order.order_number,
                'item_title': item.title,
                'buyer_name': buyer.username,
                'amount': float(order.total_amount),
                'status': order.status,
                'created_at': order.created_at.isoformat(),
                'delivered_at': order.delivered_at.isoformat() if order.delivered_at else None
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

@seller_notifications_bp.route('/api/seller/messages/unread-count', methods=['GET'])
@jwt_required()
def get_seller_unread_message_count():
    """Get count of unread messages for seller"""
    try:
        current_user_id = get_jwt_identity()
        
        # Count messages where seller is receiver and message is unread
        unread_count = db.session.query(Message).filter(
            Message.receiver_id == current_user_id,
            Message.is_receiver_read == False
        ).count()
        
        return jsonify({
            'success': True,
            'unread_count': unread_count
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500