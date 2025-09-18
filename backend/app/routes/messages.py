from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.models import Message, User, Item, Order
from sqlalchemy import or_, and_
from datetime import datetime

messages_bp = Blueprint('messages', __name__)

def convert_to_manila_time(dt):
    """Convert UTC datetime to Manila timezone for display only"""
    if dt is None:
        return None
    
    try:
        import pytz
        # Manila timezone
        manila = pytz.timezone('Asia/Manila')
        utc = pytz.UTC
        
        # Ensure dt is timezone-aware UTC
        if dt.tzinfo is None:
            dt = utc.localize(dt)
        elif dt.tzinfo != utc:
            dt = dt.astimezone(utc)
        
        # Convert to Manila time for display
        manila_time = dt.astimezone(manila)
        return manila_time.strftime('%Y-%m-%dT%H:%M:%S+08:00')
    except ImportError:
        # Fallback - assume UTC and add 8 hours
        from datetime import timedelta
        manila_offset = timedelta(hours=8)
        manila_time = dt + manila_offset
        return manila_time.strftime('%Y-%m-%dT%H:%M:%S+08:00')

@messages_bp.route('/send', methods=['POST'])
@jwt_required()
def send_message():
    """Send a new message, optionally about a specific item or order"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validation
        if not data or not data.get('receiver_id') or not data.get('message'):
            return jsonify({'error': 'Receiver ID and message are required'}), 400
        
        receiver_id = data.get('receiver_id')
        message_text = data.get('message').strip()
        item_id = data.get('item_id')  # Optional item ID
        order_id = data.get('order_id')  # Optional order ID
        
        if not message_text:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Check if receiver exists
        receiver = User.query.get(receiver_id)
        if not receiver:
            return jsonify({'error': 'Receiver not found'}), 404
        
        # Prevent sending message to yourself
        if current_user_id == receiver_id:
            return jsonify({'error': 'Cannot send message to yourself'}), 400
        
        # Validate item if provided
        item = None
        if item_id:
            item = Item.query.get(item_id)
            if not item:
                return jsonify({'error': 'Item not found'}), 404
        
        # Validate order if provided
        order = None
        if order_id:
            order = Order.query.get(order_id)
            if not order:
                return jsonify({'error': 'Order not found'}), 404
        
        # Create new message
        new_message = Message(
            sender_id=current_user_id,
            receiver_id=receiver_id,
            item_id=item_id,
            order_id=order_id,
            message=message_text,
            is_sender_read=True,  # Sender has "read" their own message by sending it
            is_receiver_read=False  # Receiver hasn't read it yet
        )
        
        db.session.add(new_message)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Message sent successfully',
            'data': new_message.to_dict()
        }), 201
        
    except Exception as e:
        current_app.logger.error(f"Error sending message: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Failed to send message'}), 500

@messages_bp.route('/conversations', methods=['GET'])
@jwt_required()
def get_conversations():
    """Get all conversations for current user, filtered by role compatibility and grouped by item"""
    try:
        current_user_id = get_jwt_identity()
        item_id = request.args.get('item_id')  # Optional filter by item
        
        # Get current user to determine role
        current_user = User.query.get(current_user_id)
        if not current_user:
            return jsonify({'error': 'User not found'}), 404
            
        # Define allowed conversation partners based on role
        allowed_roles = []
        if current_user.role == 'seller':
            allowed_roles = ['user']  # Sellers can only talk to users/customers
        elif current_user.role == 'user':
            allowed_roles = ['seller', 'admin']  # Users can talk to sellers and admins
        elif current_user.role == 'admin':
            allowed_roles = ['user', 'seller']  # Admins can talk to everyone
        
        # Get all messages involving current user
        query = Message.query.filter(
            or_(Message.sender_id == current_user_id, Message.receiver_id == current_user_id)
        )
        
        # Filter by item if specified
        if item_id:
            query = query.filter(Message.item_id == item_id)
            
        all_messages = query.order_by(Message.created_at.desc()).all()
        
        # Group by conversation partner AND item (for item-specific conversations)
        conversations_dict = {}
        
        for message in all_messages:
            # Determine the partner (the other person in the conversation)
            partner_id = message.receiver_id if message.sender_id == current_user_id else message.sender_id
            
            # Create a unique key for each conversation (partner + item)
            conversation_key = f"{partner_id}_{message.item_id or 'general'}"
            
            # Skip if we've already found a more recent message for this conversation
            if conversation_key in conversations_dict:
                continue
                
            # Get partner information
            partner = User.query.get(partner_id)
            if not partner:
                continue
                
            # Filter by allowed roles
            if partner.role not in allowed_roles:
                continue
                
            # Count unread messages FROM this partner TO current user for this item
            unread_query = Message.query.filter(
                Message.sender_id == partner_id,
                Message.receiver_id == current_user_id,
                Message.is_receiver_read == False
            )
            
            if message.item_id:
                unread_query = unread_query.filter(Message.item_id == message.item_id)
            else:
                unread_query = unread_query.filter(Message.item_id.is_(None))
                
            unread_count = unread_query.count()
            
            conversations_dict[conversation_key] = {
                'partner_id': partner_id,
                'partner_username': partner.username,
                'partner_role': partner.role,
                'item_id': message.item_id,
                'item': {
                    'id': message.item.id,
                    'title': message.item.title,
                    'price': float(message.item.price),
                    'status': message.item.status,
                    'images': [img.image_path for img in message.item.images[:1]]
                } if message.item else None,
                'order': {
                    'id': message.order.id,
                    'order_number': message.order.order_number,
                    'status': message.order.status,
                    'total_amount': float(message.order.total_amount)
                } if message.order else None,
                'last_message': message.message,
                'last_message_time': convert_to_manila_time(message.created_at),
                'unread_count': unread_count,
                'is_last_message_mine': message.sender_id == current_user_id
            }
        
        # Convert to list and sort by last message time
        conversations_list = list(conversations_dict.values())
        conversations_list.sort(
            key=lambda x: x['last_message_time'] if x['last_message_time'] else '', 
            reverse=True
        )
        
        return jsonify({
            'success': True,
            'conversations': conversations_list,
            'user_role': current_user.role
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error getting conversations: {str(e)}")
        return jsonify({'error': 'Failed to get conversations'}), 500

@messages_bp.route('/conversation/<int:partner_id>', methods=['GET'])
@jwt_required()
def get_conversation_messages(partner_id):
    """Get all messages in a conversation with a specific user, optionally filtered by item"""
    try:
        current_user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        item_id = request.args.get('item_id', type=int)  # Optional item filter
        
        # Build the query
        query = Message.query.filter(
            or_(
                and_(Message.sender_id == current_user_id, Message.receiver_id == partner_id),
                and_(Message.sender_id == partner_id, Message.receiver_id == current_user_id)
            )
        )
        
        # Filter by item if specified
        if item_id:
            query = query.filter(Message.item_id == item_id)
        
        # Get messages with pagination
        messages = query.order_by(Message.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        # Mark messages as read if current user is receiver
        unread_query = Message.query.filter(
            Message.sender_id == partner_id,
            Message.receiver_id == current_user_id,
            Message.is_receiver_read == False
        )
        
        if item_id:
            unread_query = unread_query.filter(Message.item_id == item_id)
            
        unread_messages = unread_query.all()
        
        for msg in unread_messages:
            msg.is_receiver_read = True
        
        if unread_messages:
            db.session.commit()
        
        # Get partner info
        partner = User.query.get(partner_id)
        if not partner:
            return jsonify({'error': 'Partner not found'}), 404
        
        # Get item info if specified
        item_info = None
        if item_id:
            item = Item.query.get(item_id)
            if item:
                item_info = {
                    'id': item.id,
                    'title': item.title,
                    'description': item.description,
                    'price': float(item.price),
                    'status': item.status,
                    'seller_id': item.seller_id,
                    'images': [img.image_path for img in item.images]
                }
        
        return jsonify({
            'success': True,
            'messages': [msg.to_dict() for msg in reversed(messages.items)],  # Reverse to show oldest first
            'partner': {
                'id': partner.id,
                'username': partner.username,
                'role': partner.role
            },
            'item': item_info,
            'pagination': {
                'page': messages.page,
                'pages': messages.pages,
                'per_page': messages.per_page,
                'total': messages.total,
                'has_next': messages.has_next,
                'has_prev': messages.has_prev
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error getting conversation messages: {str(e)}")
        return jsonify({'error': 'Failed to get messages'}), 500

@messages_bp.route('/mark-read', methods=['PUT'])
@jwt_required()
def mark_messages_read():
    """Mark messages as read"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or not data.get('sender_id'):
            return jsonify({'error': 'Sender ID is required'}), 400
        
        sender_id = data.get('sender_id')
        
        # Mark all unread messages from sender as read
        unread_messages = Message.query.filter(
            Message.sender_id == sender_id,
            Message.receiver_id == current_user_id,
            Message.is_receiver_read == False
        ).all()
        
        for msg in unread_messages:
            msg.is_receiver_read = True
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Marked {len(unread_messages)} messages as read'
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error marking messages as read: {str(e)}")
        return jsonify({'error': 'Failed to mark messages as read'}), 500

@messages_bp.route('/unread-count', methods=['GET'])
@jwt_required()
def get_unread_count():
    """Get total unread message count for current user"""
    try:
        current_user_id = get_jwt_identity()
        
        unread_count = Message.query.filter(
            Message.receiver_id == current_user_id,
            Message.is_receiver_read == False
        ).count()
        
        return jsonify({
            'success': True,
            'unread_count': unread_count
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error getting unread count: {str(e)}")
        return jsonify({'error': 'Failed to get unread count'}), 500

@messages_bp.route('/sellers', methods=['GET'])
@jwt_required()
def get_sellers():
    """Get list of sellers that users can message"""
    try:
        current_user_id = get_jwt_identity()
        
        # Get current user to verify they're allowed to message sellers
        current_user = User.query.get(current_user_id)
        if not current_user:
            return jsonify({'error': 'User not found'}), 404
            
        # Only users can use this endpoint
        if current_user.role not in ['user', 'admin']:
            return jsonify({'error': 'Access denied'}), 403
        
        # Get all sellers
        sellers = User.query.filter_by(role='seller').all()
        
        sellers_data = []
        for seller in sellers:
            # Check if there's an existing conversation
            existing_conversation = Message.query.filter(
                or_(
                    and_(Message.sender_id == current_user_id, Message.receiver_id == seller.id),
                    and_(Message.sender_id == seller.id, Message.receiver_id == current_user_id)
                )
            ).first()
            
            sellers_data.append({
                'id': seller.id,
                'username': seller.username,
                'email': seller.email,
                'has_conversation': existing_conversation is not None
            })
        
        return jsonify({
            'success': True,
            'sellers': sellers_data
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error getting sellers: {str(e)}")
        return jsonify({'error': 'Failed to get sellers'}), 500

@messages_bp.route('/start-conversation', methods=['POST'])
@jwt_required()
def start_conversation():
    """Start a new conversation with a seller about a specific item"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or not data.get('seller_id') or not data.get('message'):
            return jsonify({'error': 'Seller ID and initial message are required'}), 400
        
        seller_id = data.get('seller_id')
        message_text = data.get('message').strip()
        item_id = data.get('item_id')  # Optional item ID
        order_id = data.get('order_id')  # Optional order ID
        
        if not message_text:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Get current user
        current_user = User.query.get(current_user_id)
        if not current_user:
            return jsonify({'error': 'User not found'}), 404
            
        # Verify user role
        if current_user.role not in ['user', 'admin']:
            return jsonify({'error': 'Only users can start conversations with sellers'}), 403
        
        # Check if seller exists and is actually a seller
        seller = User.query.get(seller_id)
        if not seller:
            return jsonify({'error': 'Seller not found'}), 404
            
        if seller.role != 'seller':
            return jsonify({'error': 'Target user is not a seller'}), 400
        
        # Prevent messaging yourself
        if current_user_id == seller_id:
            return jsonify({'error': 'Cannot send message to yourself'}), 400
        
        # Validate item if provided
        item = None
        if item_id:
            item = Item.query.get(item_id)
            if not item:
                return jsonify({'error': 'Item not found'}), 404
            # Verify the item belongs to the seller
            if item.seller_id != seller_id:
                return jsonify({'error': 'Item does not belong to this seller'}), 400
        
        # Validate order if provided
        order = None
        if order_id:
            order = Order.query.get(order_id)
            if not order:
                return jsonify({'error': 'Order not found'}), 404
        
        # Create the first message
        new_message = Message(
            sender_id=current_user_id,
            receiver_id=seller_id,
            item_id=item_id,
            order_id=order_id,
            message=message_text,
            is_sender_read=True,
            is_receiver_read=False
        )
        
        db.session.add(new_message)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Conversation started successfully',
            'data': new_message.to_dict()
        }), 201
        
    except Exception as e:
        current_app.logger.error(f"Error starting conversation: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Failed to start conversation'}), 500

@messages_bp.route('/item/<int:item_id>/start-conversation', methods=['POST'])
@jwt_required()
def start_item_conversation(item_id):
    """Start a conversation about a specific item with its seller"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or not data.get('message'):
            return jsonify({'error': 'Message is required'}), 400
        
        message_text = data.get('message').strip()
        
        if not message_text:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Get the item
        item = Item.query.get(item_id)
        if not item:
            return jsonify({'error': 'Item not found'}), 404
        
        # Get current user
        current_user = User.query.get(current_user_id)
        if not current_user:
            return jsonify({'error': 'User not found'}), 404
        
        # Prevent messaging yourself (if you're the seller)
        if current_user_id == item.seller_id:
            return jsonify({'error': 'Cannot message yourself about your own item'}), 400
        
        # Verify user can message sellers
        if current_user.role not in ['user', 'admin']:
            return jsonify({'error': 'Only users can message sellers about items'}), 403
        
        # Create the message
        new_message = Message(
            sender_id=current_user_id,
            receiver_id=item.seller_id,
            item_id=item_id,
            message=message_text,
            is_sender_read=True,
            is_receiver_read=False
        )
        
        db.session.add(new_message)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Message sent to seller successfully',
            'data': new_message.to_dict()
        }), 201
        
    except Exception as e:
        current_app.logger.error(f"Error starting item conversation: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Failed to send message'}), 500