from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models.item import Item
from app.models.lost_report import LostReport
from app.models.found_report import FoundReport
from app.models.claim import Claim
from app.models.reward import Reward
from app.extensions import db
from app.utils.image_utils import handle_image_upload
from app.utils.decorators import admin_required

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/dashboard')
# @login_required
# @admin_required
def dashboard():
    try:
        lost_reports = LostReport.query.all()
        found_reports = FoundReport.query.all()
        claims = Claim.query.all()
        rewards = Reward.query.all()
        
        lost_reports_dict = []
        found_reports_dict = []
        claims_dict = []
        rewards_dict = []
        
        for report in lost_reports:
            try:
                lost_reports_dict.append(report.to_dict())
            except Exception as e:
                print(f"Error in LostReport.to_dict(): {str(e)}")
        
        for report in found_reports:
            try:
                found_reports_dict.append(report.to_dict())
            except Exception as e:
                print(f"Error in FoundReport.to_dict(): {str(e)}")
        
        for claim in claims:
            try:
                claims_dict.append(claim.to_dict())
            except Exception as e:
                print(f"Error in Claim.to_dict(): {str(e)}")
        
        for reward in rewards:
            try:
                rewards_dict.append(reward.to_dict())
            except Exception as e:
                print(f"Error in Reward.to_dict(): {str(e)}")
        
        return jsonify({
            'lost_reports': lost_reports_dict,
            'found_reports': found_reports_dict,
            'claims': claims_dict,
            'rewards': rewards_dict
        }), 200
    except Exception as e:
        print(f"Error in dashboard route: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/items', methods=['GET', 'POST'])
# @login_required
# @admin_required
def add_item():
    if request.method == 'POST':
        try:
            data = request.json
            item_name = data['name']
            
            existing_item = Item.query.filter_by(name=item_name).first()
            if existing_item:
                return jsonify({'error': 'Item with this name already exists'}), 400
            
            image_url = handle_image_upload(request.files.get('image'), None) 
            item = Item(name=item_name, description=data.get('description'), image_url=image_url)
            db.session.add(item)
            db.session.commit()
            
            return jsonify({'message': 'Item added successfully', 'item': item.to_dict()}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Method not allowed'}), 405

@bp.route('/list_items', methods=['GET'])
# @login_required
# @admin_required
def list_items():
    try:
        page = request.args.get('page', 1, type=int)
        items_per_page = 5
        
        items_query = Item.query.paginate(page=page, per_page=items_per_page)
        
        return jsonify({
            'items': [item.to_dict() for item in items_query.items],
            'current_page': items_query.page,
            'total_pages': items_query.pages,
            'total_items': items_query.total
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/items/<int:item_id>', methods=['GET', 'PUT', 'DELETE'])
# @login_required
# @admin_required
def manage_item(item_id):
    item = Item.query.get_or_404(item_id)
    
    if request.method == 'GET':
        return jsonify(item.to_dict()), 200
    
    elif request.method == 'PUT':
        try:
            data = request.json
            image_url = handle_image_upload(request.files.get('image'), item_id)
            item.name = data['name']
            item.description = data.get('description')
            if image_url:
                item.image_url = image_url
            db.session.commit()
            return jsonify({'message': 'Item updated successfully', 'item': item.to_dict()}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'DELETE':
        try:
            db.session.delete(item)
            db.session.commit()
            return jsonify({'message': 'Item deleted successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@bp.route('/reports/lost', methods=['GET'])
# @login_required
# @admin_required
def view_lost_reports():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 2
        
        lost_reports_paginated = LostReport.query.paginate(page=page, per_page=per_page)
        
        return jsonify({
            'lost_reports': [report.to_dict() for report in lost_reports_paginated.items],
            'current_page': lost_reports_paginated.page,
            'total_pages': lost_reports_paginated.pages,
            'total_reports': lost_reports_paginated.total
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/reports/found', methods=['GET'])
# @login_required
# @admin_required
def view_found_reports():
    try:
        found_reports = FoundReport.query.all()
        return jsonify({'found_reports': [report.to_dict() for report in found_reports]}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/claims', methods=['GET'])
# @login_required
# @admin_required
def view_claims():
    try:
        claims = Claim.query.all()
        return jsonify({'claims': [claim.to_dict() for claim in claims]}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/rewards', methods=['GET'])
# @login_required
# @admin_required
def view_rewards():
    try:
        rewards = Reward.query.all()
        return jsonify({'rewards': [reward.to_dict() for reward in rewards]}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/reports/lost/<int:lost_report_id>/approve', methods=['POST'])
# @login_required
# @admin_required
def approve_lost_report(lost_report_id):
    try:
        report = LostReport.query.get_or_404(lost_report_id)
        if report.approved:
            return jsonify({'error': 'Lost report already approved'}), 400
        
        report.approved = True
        db.session.commit()
        return jsonify({'message': 'Lost report approved successfully', 'report': report.to_dict()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/list_recovered_items', methods=['GET'])
# @login_required
# @admin_required
def list_recovered_items():
    try:
        recovered_items = Item.query.join(FoundReport).filter(FoundReport.item_id == Item.id).all()
        return jsonify({'recovered_items': [item.to_dict() for item in recovered_items]}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/list_returned_items', methods=['GET'])
# @login_required
# @admin_required
def list_returned_items():
    try:
        returned_items = Item.query.filter_by(is_returned=True).all()
        return jsonify({'returned_items': [item.to_dict() for item in returned_items]}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
