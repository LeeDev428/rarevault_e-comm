from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.models import Message, User
from sqlalchemy import or_, and_

messages_bp = Blueprint('messages', __name__)

@messages_bp.route('/send', methods=['POST'])
@jwt_required()
def send_message():
    """Send a new message"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validation
        if not data or not data.get('receiver_id') or not data.get('message'):
            return jsonify({'error': 'Receiver ID and message are required'}), 400
        
        receiver_id = data.get('receiver_id')
        message_text = data.get('message').strip()
        
        if not message_text:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Check if receiver exists
        receiver = User.query.get(receiver_id)
        if not receiver:
            return jsonify({'error': 'Receiver not found'}), 404
        
        # Prevent sending message to yourself
        if current_user_id == receiver_id:
            return jsonify({'error': 'Cannot send message to yourself'}), 400
        
        # Create new message
        new_message = Message(
            sender_id=current_user_id,
            receiver_id=receiver_id,
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
    """Get all conversations for current user"""
    try:
        current_user_id = get_jwt_identity()
        
        # Get all unique conversation partners
        conversations = db.session.query(
            Message.sender_id,
            Message.receiver_id,
            Message.message,
            Message.created_at,
            Message.is_sender_read,
            Message.is_receiver_read,
            User.username.label('partner_username'),
            User.role.label('partner_role')
        ).join(
            User, 
            or_(
                and_(Message.sender_id == current_user_id, User.id == Message.receiver_id),
                and_(Message.receiver_id == current_user_id, User.id == Message.sender_id)
            )
        ).filter(
            or_(Message.sender_id == current_user_id, Message.receiver_id == current_user_id)
        ).order_by(Message.created_at.desc()).all()
        
        # Group conversations by partner
        conversation_dict = {}
        for msg in conversations:
            partner_id = msg.receiver_id if msg.sender_id == current_user_id else msg.sender_id
            
            if partner_id not in conversation_dict:
                conversation_dict[partner_id] = {
                    'partner_id': partner_id,
                    'partner_username': msg.partner_username,
                    'partner_role': msg.partner_role,
                    'last_message': msg.message,
                    'last_message_time': msg.created_at.isoformat(),
                    'unread_count': 0,
                    'is_last_message_mine': msg.sender_id == current_user_id
                }
            
            # Count unread messages based on user role
            if msg.sender_id == current_user_id:
                # I sent this message - check if I've read it (for sent message notifications)
                if not msg.is_sender_read:
                    conversation_dict[partner_id]['unread_count'] += 1
            else:
                # I received this message - check if I've read it
                if not msg.is_receiver_read:
                    conversation_dict[partner_id]['unread_count'] += 1
        
        conversations_list = list(conversation_dict.values())
        conversations_list.sort(key=lambda x: x['last_message_time'], reverse=True)
        
        return jsonify({
            'success': True,
            'conversations': conversations_list
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error getting conversations: {str(e)}")
        return jsonify({'error': 'Failed to get conversations'}), 500

@messages_bp.route('/conversation/<int:partner_id>', methods=['GET'])
@jwt_required()
def get_conversation_messages(partner_id):
    """Get all messages in a conversation with a specific user"""
    try:
        current_user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        
        # Get messages between current user and partner
        messages = Message.query.filter(
            or_(
                and_(Message.sender_id == current_user_id, Message.receiver_id == partner_id),
                and_(Message.sender_id == partner_id, Message.receiver_id == current_user_id)
            )
        ).order_by(Message.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        # Mark messages as read if current user is receiver
        unread_messages = Message.query.filter(
            Message.sender_id == partner_id,
            Message.receiver_id == current_user_id,
            Message.is_receiver_read == False
        ).all()
        
        for msg in unread_messages:
            msg.is_receiver_read = True
        
        if unread_messages:
            db.session.commit()
        
        # Get partner info
        partner = User.query.get(partner_id)
        if not partner:
            return jsonify({'error': 'Partner not found'}), 404
        
        return jsonify({
            'success': True,
            'messages': [msg.to_dict() for msg in reversed(messages.items)],  # Reverse to show oldest first
            'partner': {
                'id': partner.id,
                'username': partner.username,
                'role': partner.role
            },
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