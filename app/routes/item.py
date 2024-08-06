from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models.item import Item
from app.extensions import db

bp = Blueprint('item', __name__, url_prefix='/item')

@bp.route('/<int:item_id>', methods=['GET'])
# @login_required
def get_item(item_id):
    item = Item.query.get_or_404(item_id)
    return jsonify(item.to_dict()), 200

@bp.route('/all', methods=['GET'])
# @login_required
def get_all_items():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    items = Item.query.paginate(page=page, per_page=per_page, error_out=False)
    
    items_dict = [item.to_dict() for item in items.items]
    
    return jsonify({
        'items': items_dict,
        'total': items.total,
        'pages': items.pages,
        'current_page': items.page
    }), 200

