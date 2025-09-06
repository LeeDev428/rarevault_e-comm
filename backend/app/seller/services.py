"""
Seller Services - Business logic for seller operations
"""
from ..models.models import db, Item, User
from datetime import datetime
from sqlalchemy import func

class SellerService:
    
    @staticmethod
    def get_seller_analytics(seller_id):
        """Get detailed analytics for a seller"""
        try:
            # Basic stats
            total_items = Item.query.filter_by(seller_id=seller_id).count()
            active_items = Item.query.filter_by(seller_id=seller_id, status='available').count()
            sold_items = Item.query.filter_by(seller_id=seller_id, status='sold').count()
            pending_items = Item.query.filter_by(seller_id=seller_id, status='pending').count()
            
            # Revenue calculations
            total_revenue = db.session.query(func.sum(Item.price)).filter_by(
                seller_id=seller_id, status='sold'
            ).scalar() or 0
            
            # Average item price
            avg_price = db.session.query(func.avg(Item.price)).filter_by(
                seller_id=seller_id
            ).scalar() or 0
            
            # Items by category
            category_stats = db.session.query(
                Item.category,
                func.count(Item.id).label('count')
            ).filter_by(seller_id=seller_id).group_by(Item.category).all()
            
            # Recent activity (last 30 days)
            thirty_days_ago = datetime.utcnow().replace(day=1)  # Simplified to current month
            recent_items = Item.query.filter(
                Item.seller_id == seller_id,
                Item.created_at >= thirty_days_ago
            ).count()
            
            return {
                'basic_stats': {
                    'total_items': total_items,
                    'active_items': active_items,
                    'sold_items': sold_items,
                    'pending_items': pending_items
                },
                'financial': {
                    'total_revenue': float(total_revenue),
                    'average_price': float(avg_price)
                },
                'categories': [
                    {'category': cat[0], 'count': cat[1]} 
                    for cat in category_stats
                ],
                'activity': {
                    'recent_items': recent_items
                }
            }
            
        except Exception as e:
            raise Exception(f"Error getting seller analytics: {str(e)}")
    
    @staticmethod
    def validate_item_data(data):
        """Validate item creation/update data"""
        errors = []
        
        # Required fields
        required_fields = ['title', 'category', 'price', 'condition', 'description']
        for field in required_fields:
            if not data.get(field):
                errors.append(f'{field} is required')
        
        # Validate price
        if data.get('price'):
            try:
                price = float(data['price'])
                if price <= 0:
                    errors.append('Price must be greater than 0')
                if price > 1000000:  # Reasonable upper limit
                    errors.append('Price cannot exceed $1,000,000')
            except (ValueError, TypeError):
                errors.append('Invalid price format')
        
        # Validate category
        valid_categories = ['antiques', 'collectibles', 'coins', 'others']
        if data.get('category') and data['category'].lower() not in valid_categories:
            errors.append('Invalid category')
        
        # Validate condition
        valid_conditions = ['excellent', 'good', 'fair', 'poor']
        if data.get('condition') and data['condition'].lower() not in valid_conditions:
            errors.append('Invalid condition')
        
        # Validate year if provided
        if data.get('year'):
            try:
                year = int(data['year'])
                current_year = datetime.now().year
                if year < 1800 or year > current_year:
                    errors.append(f'Year must be between 1800 and {current_year}')
            except (ValueError, TypeError):
                errors.append('Invalid year format')
        
        # Validate title length
        if data.get('title') and len(data['title']) > 200:
            errors.append('Title cannot exceed 200 characters')
        
        # Validate description length
        if data.get('description') and len(data['description']) > 2000:
            errors.append('Description cannot exceed 2000 characters')
        
        return errors
    
    @staticmethod
    def create_item(seller_id, item_data):
        """Create a new item with validation"""
        try:
            # Validate data
            errors = SellerService.validate_item_data(item_data)
            if errors:
                return {'success': False, 'errors': errors}
            
            # Create item
            item = Item(
                title=item_data['title'],
                description=item_data['description'],
                price=float(item_data['price']),
                category=item_data['category'].lower(),
                condition=item_data['condition'].lower(),
                year=int(item_data['year']) if item_data.get('year') else None,
                image_url=item_data.get('image_url', ''),
                seller_id=seller_id,
                status='available'
            )
            
            db.session.add(item)
            db.session.commit()
            
            return {'success': True, 'item': item.to_dict()}
            
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'errors': [str(e)]}
    
    @staticmethod
    def update_item(seller_id, item_id, update_data):
        """Update an existing item with validation"""
        try:
            # Get item
            item = Item.query.filter_by(id=item_id, seller_id=seller_id).first()
            if not item:
                return {'success': False, 'errors': ['Item not found']}
            
            # Validate data
            errors = SellerService.validate_item_data(update_data)
            if errors:
                return {'success': False, 'errors': errors}
            
            # Update fields
            updatable_fields = [
                'title', 'description', 'price', 'category', 
                'condition', 'year', 'image_url', 'status'
            ]
            
            for field in updatable_fields:
                if field in update_data:
                    if field == 'price':
                        setattr(item, field, float(update_data[field]))
                    elif field == 'year' and update_data[field]:
                        setattr(item, field, int(update_data[field]))
                    elif field in ['category', 'condition']:
                        setattr(item, field, update_data[field].lower())
                    else:
                        setattr(item, field, update_data[field])
            
            item.updated_at = datetime.utcnow()
            db.session.commit()
            
            return {'success': True, 'item': item.to_dict()}
            
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'errors': [str(e)]}
    
    @staticmethod
    def delete_item(seller_id, item_id):
        """Delete an item"""
        try:
            item = Item.query.filter_by(id=item_id, seller_id=seller_id).first()
            if not item:
                return {'success': False, 'errors': ['Item not found']}
            
            db.session.delete(item)
            db.session.commit()
            
            return {'success': True, 'message': 'Item deleted successfully'}
            
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'errors': [str(e)]}
    
    @staticmethod
    def get_seller_items_with_filters(seller_id, filters):
        """Get seller items with filtering and pagination"""
        try:
            query = Item.query.filter_by(seller_id=seller_id)
            
            # Apply filters
            if filters.get('status'):
                query = query.filter_by(status=filters['status'])
            
            if filters.get('category'):
                query = query.filter_by(category=filters['category'])
            
            if filters.get('search'):
                search_term = f"%{filters['search']}%"
                query = query.filter(
                    db.or_(
                        Item.title.ilike(search_term),
                        Item.description.ilike(search_term)
                    )
                )
            
            if filters.get('min_price'):
                query = query.filter(Item.price >= float(filters['min_price']))
            
            if filters.get('max_price'):
                query = query.filter(Item.price <= float(filters['max_price']))
            
            if filters.get('condition'):
                query = query.filter_by(condition=filters['condition'])
            
            # Apply sorting
            sort_by = filters.get('sort_by', 'created_at')
            sort_order = filters.get('sort_order', 'desc')
            
            if hasattr(Item, sort_by):
                if sort_order == 'desc':
                    query = query.order_by(getattr(Item, sort_by).desc())
                else:
                    query = query.order_by(getattr(Item, sort_by).asc())
            else:
                query = query.order_by(Item.created_at.desc())
            
            # Pagination
            page = int(filters.get('page', 1))
            per_page = int(filters.get('per_page', 10))
            
            items = query.paginate(
                page=page, per_page=per_page, error_out=False
            )
            
            return {
                'success': True,
                'items': [item.to_dict() for item in items.items],
                'pagination': {
                    'page': items.page,
                    'pages': items.pages,
                    'per_page': items.per_page,
                    'total': items.total,
                    'has_next': items.has_next,
                    'has_prev': items.has_prev
                }
            }
            
        except Exception as e:
            return {'success': False, 'errors': [str(e)]}
    
    @staticmethod
    def verify_seller_access(user):
        """Verify if user has seller access"""
        return user and user.role in ['seller', 'admin']
