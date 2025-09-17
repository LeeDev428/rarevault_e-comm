from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.models import Message, User
from sqlalchemy import or_, and_
from datetime import datetime

messages_bp = Blueprint('messages', __name__)

def convert_to_manila_time(dt):
    """Convert datetime to Manila timezone"""
    if dt is None:
        return None
    
    try:
        import pytz
        # Manila timezone
        manila = pytz.timezone('Asia/Manila')
        
        # If dt is naive (no timezone info), assume it's UTC
        if dt.tzinfo is None:
            utc = pytz.UTC
            dt = utc.localize(dt)
        
        # Convert to Manila time
        manila_time = dt.astimezone(manila)
        # Return in ISO format but more readable
        return manila_time.strftime('%Y-%m-%dT%H:%M:%S+08:00')
    except ImportError:
        # Fallback if pytz is not available - add 8 hours to UTC (Manila is UTC+8)
        if hasattr(dt, 'replace'):
            import datetime
            manila_offset = datetime.timedelta(hours=8)
            manila_time = dt + manila_offset
            return manila_time.strftime('%Y-%m-%dT%H:%M:%S+08:00')
        return dt.isoformat() if dt else None

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
        
        # Simple approach: Get all messages involving current user, then process
        all_messages = Message.query.filter(
            or_(Message.sender_id == current_user_id, Message.receiver_id == current_user_id)
        ).order_by(Message.created_at.desc()).all()
        
        # Group by conversation partner and keep only the latest message
        conversations_dict = {}
        
        for message in all_messages:
            # Determine the partner (the other person in the conversation)
            partner_id = message.receiver_id if message.sender_id == current_user_id else message.sender_id
            
            # Skip if we've already found a more recent message for this partner
            if partner_id in conversations_dict:
                continue
                
            # Get partner information
            partner = User.query.get(partner_id)
            if not partner:
                continue
                
            # Count unread messages for this partner
            if current_user_id == message.receiver_id:
                # I'm the receiver - count unread messages I received
                unread_count = Message.query.filter(
                    Message.sender_id == partner_id,
                    Message.receiver_id == current_user_id,
                    Message.is_receiver_read == False
                ).count()
            else:
                # I'm the sender - count unread messages I sent (sender notifications)
                unread_count = Message.query.filter(
                    Message.sender_id == current_user_id,
                    Message.receiver_id == partner_id,
                    Message.is_sender_read == False
                ).count()
            
            conversations_dict[partner_id] = {
                'partner_id': partner_id,
                'partner_username': partner.username,
                'partner_role': partner.role,
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