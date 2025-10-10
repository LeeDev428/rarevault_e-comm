from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import User, Item, Order
from sqlalchemy import func, and_

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
        # Total Users
        total_users = User.query.count()
        buyers = User.query.filter_by(role='user').count()
        sellers = User.query.filter_by(role='seller').count()
        
        # Items Statistics
        total_items = Item.query.count()
        active_items = Item.query.filter_by(status='active').count()
        sold_items = Item.query.filter_by(status='sold').count()
        pending_items = Item.query.filter_by(status='pending').count()
        
        # Appraisal Statistics (using items with pending status)
        total_appraisals = Item.query.filter(Item.status.in_(['pending', 'active'])).count()
        approved_appraisals = Item.query.filter_by(status='active').count()
        pending_appraisals = Item.query.filter_by(status='pending').count()
        
        return jsonify({
            'stats': {
                'total_users': total_users,
                'buyers': buyers,
                'sellers': sellers,
                'total_items': total_items,
                'active_items': active_items,
                'sold_items': sold_items,
                'pending_items': pending_items,
                'total_appraisals': total_appraisals,
                'approved_appraisals': approved_appraisals,
                'pending_appraisals': pending_appraisals
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
        users_data = []
        for user in users:
            user_dict = user.to_dict()
            # Get shop name if seller
            if user.role == 'seller':
                user_dict['shop_name'] = user.shop_name if hasattr(user, 'shop_name') else 'N/A'
            else:
                user_dict['shop_name'] = 'N/A'
            users_data.append(user_dict)
            
        return jsonify({
            'success': True,
            'users': users_data,
            'total': len(users_data)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    if not require_admin():
        return jsonify({'error': 'Admin access required'}), 403
    
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'User deleted successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/users/delete-all', methods=['DELETE'])
@jwt_required()
def delete_all_users():
    if not require_admin():
        return jsonify({'error': 'Admin access required'}), 403
    
    try:
        # Don't delete admin users
        deleted_count = User.query.filter(User.role != 'admin').delete()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{deleted_count} users deleted successfully',
            'deleted_count': deleted_count
        }), 200
    except Exception as e:
        db.session.rollback()
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

@admin_bp.route('/items', methods=['GET'])
@jwt_required()
def get_all_items():
    if not require_admin():
        return jsonify({'error': 'Admin access required'}), 403
    
    try:
        status_filter = request.args.get('status', 'all')
        
        if status_filter == 'sold':
            items = Item.query.filter_by(status='sold').all()
        elif status_filter == 'pending':
            items = Item.query.filter_by(status='pending').all()
        elif status_filter == 'active':
            items = Item.query.filter_by(status='active').all()
        else:
            items = Item.query.all()
        
        items_data = []
        for item in items:
            item_dict = item.to_dict()
            # Get seller info
            seller = User.query.get(item.seller_id)
            item_dict['posted_by'] = seller.username if seller else 'Unknown'
            items_data.append(item_dict)
            
        return jsonify({
            'success': True,
            'items': items_data,
            'total': len(items_data)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/items/<int:item_id>', methods=['DELETE'])
@jwt_required()
def delete_item(item_id):
    if not require_admin():
        return jsonify({'error': 'Admin access required'}), 403
    
    try:
        item = Item.query.get(item_id)
        if not item:
            return jsonify({'error': 'Item not found'}), 404
        
        db.session.delete(item)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Item deleted successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/items/delete-all', methods=['DELETE'])
@jwt_required()
def delete_all_items():
    if not require_admin():
        return jsonify({'error': 'Admin access required'}), 403
    
    try:
        status_filter = request.args.get('status', 'all')
        
        if status_filter == 'sold':
            deleted_count = Item.query.filter_by(status='sold').delete()
        elif status_filter == 'pending':
            deleted_count = Item.query.filter_by(status='pending').delete()
        elif status_filter == 'active':
            deleted_count = Item.query.filter_by(status='active').delete()
        else:
            deleted_count = Item.query.delete()
            
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{deleted_count} items deleted successfully',
            'deleted_count': deleted_count
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/appraisals', methods=['GET'])
@jwt_required()
def get_appraisals():
    if not require_admin():
        return jsonify({'error': 'Admin access required'}), 403
    
    try:
        status_filter = request.args.get('status', 'pending')
        
        if status_filter == 'approved':
            items = Item.query.filter_by(status='active').all()
        elif status_filter == 'rejected':
            items = Item.query.filter_by(status='removed').all()
        elif status_filter == 'pending':
            items = Item.query.filter_by(status='pending').all()
        else:
            items = Item.query.filter(Item.status.in_(['pending', 'active', 'removed'])).all()
        
        appraisals_data = []
        for item in items:
            item_dict = item.to_dict()
            seller = User.query.get(item.seller_id)
            item_dict['posted_by'] = seller.username if seller else 'Unknown'
            item_dict['appraisal_status'] = 'approved' if item.status == 'active' else ('rejected' if item.status == 'removed' else 'pending')
            appraisals_data.append(item_dict)
            
        return jsonify({
            'success': True,
            'appraisals': appraisals_data,
            'total': len(appraisals_data)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/appraisals/<int:item_id>/approve', methods=['PATCH'])
@jwt_required()
def approve_appraisal(item_id):
    if not require_admin():
        return jsonify({'error': 'Admin access required'}), 403
    
    try:
        item = Item.query.get(item_id)
        if not item:
            return jsonify({'error': 'Item not found'}), 404
        
        item.status = 'active'
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Appraisal approved successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/appraisals/approve-all', methods=['PATCH'])
@jwt_required()
def approve_all_appraisals():
    if not require_admin():
        return jsonify({'error': 'Admin access required'}), 403
    
    try:
        pending_items = Item.query.filter_by(status='pending').all()
        approved_count = 0
        
        for item in pending_items:
            item.status = 'active'
            approved_count += 1
            
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{approved_count} appraisals approved successfully',
            'approved_count': approved_count
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/appraisals/delete-all', methods=['DELETE'])
@jwt_required()
def delete_all_appraisals():
    if not require_admin():
        return jsonify({'error': 'Admin access required'}), 403
    
    try:
        status_filter = request.args.get('status', 'all')
        
        if status_filter == 'approved':
            deleted_count = Item.query.filter_by(status='active').delete()
        elif status_filter == 'pending':
            deleted_count = Item.query.filter_by(status='pending').delete()
        else:
            deleted_count = Item.query.filter(Item.status.in_(['pending', 'active'])).delete()
            
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{deleted_count} appraisals deleted successfully',
            'deleted_count': deleted_count
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Reports & Analytics Routes
@admin_bp.route('/reports/sales-stats', methods=['GET'])
@jwt_required()
def get_sales_stats():
    if not require_admin():
        return jsonify({'error': 'Admin access required'}), 403
    
    try:
        period = request.args.get('period', 'month')
        
        # Calculate date range based on period
        from datetime import datetime, timedelta
        end_date = datetime.now()
        
        if period == 'today':
            start_date = end_date.replace(hour=0, minute=0, second=0)
        elif period == 'week':
            start_date = end_date - timedelta(days=7)
        elif period == 'month':
            start_date = end_date - timedelta(days=30)
        elif period == 'year':
            start_date = end_date - timedelta(days=365)
        else:
            start_date = end_date - timedelta(days=30)
        
        # Get orders in date range
        orders = Order.query.filter(
            Order.created_at >= start_date,
            Order.status.in_(['delivered', 'shipped'])
        ).all()
        
        total_revenue = sum(float(order.total_amount) for order in orders)
        total_orders = len(orders)
        items_sold = sum(order.quantity for order in orders)
        avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
        
        # Calculate previous period for comparison
        prev_start = start_date - (end_date - start_date)
        prev_orders = Order.query.filter(
            Order.created_at >= prev_start,
            Order.created_at < start_date,
            Order.status.in_(['delivered', 'shipped'])
        ).all()
        
        prev_revenue = sum(float(order.total_amount) for order in prev_orders)
        prev_count = len(prev_orders)
        
        revenue_change = ((total_revenue - prev_revenue) / prev_revenue * 100) if prev_revenue > 0 else 0
        orders_change = ((total_orders - prev_count) / prev_count * 100) if prev_count > 0 else 0
        
        return jsonify({
            'stats': {
                'totalRevenue': total_revenue,
                'revenueChange': round(revenue_change, 1),
                'totalOrders': total_orders,
                'ordersChange': round(orders_change, 1),
                'itemsSold': items_sold,
                'itemsChange': 0,
                'avgOrderValue': avg_order_value,
                'avgChange': 0
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/reports/recent-sales', methods=['GET'])
@jwt_required()
def get_recent_sales():
    if not require_admin():
        return jsonify({'error': 'Admin access required'}), 403
    
    try:
        period = request.args.get('period', 'month')
        
        from datetime import datetime, timedelta
        end_date = datetime.now()
        
        if period == 'today':
            start_date = end_date.replace(hour=0, minute=0, second=0)
        elif period == 'week':
            start_date = end_date - timedelta(days=7)
        elif period == 'month':
            start_date = end_date - timedelta(days=30)
        else:
            start_date = end_date - timedelta(days=30)
        
        orders = Order.query.filter(
            Order.created_at >= start_date
        ).order_by(Order.created_at.desc()).limit(50).all()
        
        sales_data = []
        for order in orders:
            buyer = User.query.get(order.buyer_id)
            seller = User.query.get(order.seller_id)
            item = Item.query.get(order.item_id)
            
            sales_data.append({
                'id': order.id,
                'orderNumber': order.order_number,
                'date': order.created_at.isoformat() if order.created_at else None,
                'customer': buyer.username if buyer else 'Unknown',
                'seller': seller.username if seller else 'Unknown',
                'item': item.title if item else 'Item not found',
                'amount': float(order.total_amount),
                'status': order.status.capitalize()
            })
        
        return jsonify({
            'sales': sales_data,
            'total': len(sales_data)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/reports/activity-logs', methods=['GET'])
@jwt_required()
def get_activity_logs():
    if not require_admin():
        return jsonify({'error': 'Admin access required'}), 403
    
    try:
        # This would require an activity_logs table in your database
        # For now, return mock structure
        return jsonify({
            'logs': [],
            'message': 'Activity logging feature requires database migration'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/reports/user-analytics', methods=['GET'])
@jwt_required()
def get_user_analytics():
    if not require_admin():
        return jsonify({'error': 'Admin access required'}), 403
    
    try:
        period = request.args.get('period', 'month')
        
        # Get user counts
        total_users = User.query.count()
        active_users = User.query.filter_by(is_active=True).count()
        active_sellers = User.query.filter_by(role='seller', is_active=True).count()
        
        # Calculate percentages
        admin_count = User.query.filter_by(role='admin').count()
        seller_count = User.query.filter_by(role='seller').count()
        user_count = User.query.filter_by(role='user').count()
        
        admin_percent = round((admin_count / total_users * 100) if total_users > 0 else 0, 1)
        seller_percent = round((seller_count / total_users * 100) if total_users > 0 else 0, 1)
        user_percent = round((user_count / total_users * 100) if total_users > 0 else 0, 1)
        
        return jsonify({
            'analytics': {
                'totalUsers': total_users,
                'usersGrowth': 0,
                'activeUsers': active_users,
                'activeGrowth': 0,
                'activeSellers': active_sellers,
                'sellersGrowth': 0,
                'retentionRate': 0,
                'retentionChange': 0,
                'adminPercent': admin_percent,
                'sellerPercent': seller_percent,
                'userPercent': user_percent
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
