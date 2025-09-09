from flask import Blueprint, jsonify
from app.models.models import Item, ItemImage, db

debug_bp = Blueprint('debug', __name__)

@debug_bp.route('/debug/items-images', methods=['GET'])
def debug_items_images():
    try:
        items = Item.query.all()
        result = []
        
        for item in items:
            images = ItemImage.query.filter_by(item_id=item.id).all()
            item_data = {
                'item_id': item.id,
                'title': item.title,
                'images_count': len(images),
                'images': [
                    {
                        'id': img.id,
                        'path': img.image_url,
                        'is_primary': img.is_primary,
                        'url': f"http://localhost:5000/uploads/{img.image_url}"
                    } for img in images
                ],
                'to_dict_result': item.to_dict()
            }
            result.append(item_data)
            
        return jsonify({
            'total_items': len(items),
            'items': result
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
