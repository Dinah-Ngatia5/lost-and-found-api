from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from app.models.lost_report import LostReport
from app.models.found_report import FoundReport
from app.models.item import Item
from app.models.comment import Comment
from app.models.claim import Claim
from app.extensions import db
from werkzeug.utils import secure_filename
from datetime import datetime
from app.models.reward import Reward
from app.models.user import User
import os

bp = Blueprint('report', __name__, url_prefix='/report')

def handle_image_upload(file, item_id):
    UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER']
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        try:
            file.save(file_path)
            return f'/static/uploads/{filename}'
        except Exception as e:
            print(f"Error saving file: {e}")
            return None
    else:
        print("Invalid file or file type not allowed.")
        return None

@bp.route('/lost', methods=['POST'])
# @login_required
def report_lost_item():
    data = request.json
    file = request.files.get('upload_image')

    try:
        date_lost = datetime.strptime(data['date_lost'], '%Y-%m-%d').date()
        time_lost = datetime.strptime(data['time_lost'], '%H:%M:%S').time()
    except ValueError:
        return jsonify({'error': 'Invalid date or time format. Use YYYY-MM-DD and HH:MM:SS.'}), 400

    item = Item.query.get(data['item_id'])
    if not item:
        return jsonify({'error': 'Item not found.'}), 404

    image_url = handle_image_upload(file, data['item_id']) if file else None

    lost_report = LostReport(
        user_id=current_user.id,
        item_id=data['item_id'],
        item_name=data.get('item_name'),
        date_lost=date_lost,
        time_lost=time_lost,
        place_lost=data['place_lost'],
        contact=data.get('contact'),
        description=data.get('description'),
        primary_color=data.get('primary_color'),
        secondary_color=data.get('secondary_color'),
        upload_image=image_url
    )
    try:
        db.session.add(lost_report)
        db.session.commit()
        
        found_report = FoundReport.query.filter_by(item_id=data['item_id']).first()
        if found_report:
            return jsonify({'message': 'Lost report submitted successfully', 'redirect': 'list_all_found_reports'}), 200
        
        return jsonify({'message': 'Lost report submitted successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error saving lost report: {str(e)}'}), 500

@bp.route('/found', methods=['POST'])
# @login_required
def report_found_item():
    data = request.json
    file = request.files.get('upload_image')

    try:
        date_found = datetime.strptime(data['date_found'], '%Y-%m-%d').date()
        time_found = datetime.strptime(data['time_found'], '%H:%M:%S').time()
    except ValueError:
        return jsonify({'error': 'Invalid date or time format. Use YYYY-MM-DD and HH:MM:SS.'}), 400

    item = Item.query.get(data['item_id'])
    if not item:
        return jsonify({'error': 'Item not found.'}), 404

    image_url = handle_image_upload(file, data['item_id']) if file else None

    found_report = FoundReport(
        user_id=current_user.id,
        item_id=data['item_id'],
        item_name=data.get('item_name'),
        date_found=date_found,
        time_found=time_found,
        place_found=data['place_found'],
        contact=data.get('contact'),
        description=data.get('description'),
        primary_color=data.get('primary_color'),
        secondary_color=data.get('secondary_color'),
        upload_image=image_url
    )
    
    try:
        item.is_recovered = True
        db.session.add(found_report)
        db.session.commit()
        return jsonify({'message': 'Found report submitted successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error saving found report: {str(e)}'}), 500

@bp.route('/comments/<int:item_id>', methods=['GET'])
# @login_required
def get_comments(item_id):
    comments = Comment.query.filter_by(item_id=item_id).all()
    return jsonify([{
        'user_id': comment.user_id,
        'username': comment.user.username,
        'content': comment.content,
        'timestamp': comment.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    } for comment in comments])

@bp.route('/comments/provide/<int:item_id>', methods=['POST'])
# @login_required
def provide_comment(item_id):
    data = request.json
    content = data.get('content')
    if not content:
        return jsonify({'error': 'Content is required'}), 400

    comment = Comment(user_id=current_user.id, item_id=item_id, content=content)
    db.session.add(comment)
    db.session.commit()
    return jsonify({'message': 'Comment added successfully'}), 201

@bp.route('/initiate_claim/<int:found_report_id>', methods=['POST'])
# @login_required
def initiate_claim(found_report_id):
    found_report = FoundReport.query.get_or_404(found_report_id)
    user_lost_report = LostReport.query.filter_by(user_id=current_user.id, item_id=found_report.item_id).first()

    if not user_lost_report:
        return jsonify({'error': 'You need to submit a lost report of the item before claiming it.'}), 400

    data = request.json
    item = found_report.item
    claim = Claim(
        user_id=current_user.id,
        found_report_id=found_report_id,
        description=data.get('description')
    )
    try:
        item.is_claimed = True
        db.session.add(claim)
        db.session.commit()
        return jsonify({'message': 'Claim initiated successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error initiating claim: {str(e)}'}), 500

@bp.route('/offer_reward/<int:found_report_id>', methods=['POST'])
# @login_required
def offer_reward(found_report_id):
    data = request.json
    try:
        amount = float(data['amount'])
        
        if amount <= 0:
            return jsonify({'error': 'Reward amount must be positive.'}), 400

        found_report = FoundReport.query.get(found_report_id)
        if not found_report:
            return jsonify({'error': 'Found report not found.'}), 404

        receiver = found_report.user

        reward = Reward(
            amount=amount,
            receiver_id=receiver.id,
            receiver_username=receiver.username,
            payer_username=current_user.username,
            payer_id=current_user.id,
            found_report_id=found_report_id
        )
        db.session.add(reward)
        db.session.commit()
        return jsonify({'message': 'Reward offered successfully'}), 201
    except ValueError:
        return jsonify({'error': 'Invalid data format. Ensure all fields are correct.'}), 400
    except KeyError as e:
        return jsonify({'error': f'Missing field: {str(e)}'}), 400

@bp.route('/receive_reward/<int:found_report_id>', methods=['POST'])
# @login_required
def receive_reward(found_report_id):
    found_report = FoundReport.query.get_or_404(found_report_id)
    
    data = request.json
    try:
        amount = float(data['amount'])
        date_paid = datetime.strptime(data['date_paid'], '%Y-%m-%d').date()
        payer_username = data['payer_username']
        
        if amount <= 0:
            return jsonify({'error': 'Reward amount must be positive.'}), 400
        
        payer = User.query.filter_by(username=payer_username).first()
        if not payer:
            return jsonify({'error': 'Payer not found.'}), 404

        reward = Reward.query.filter_by(found_report_id=found_report_id).first()
        if not reward:
            return jsonify({'error': 'No reward offered for this found report.'}), 404

        if found_report.user_id != current_user.id:
            return jsonify({'error': 'You are not authorized to receive this reward.'}), 403

        if reward.payer_id != payer.id or reward.amount <= 0:
            return jsonify({'error': 'Invalid reward or reward has already been processed.'}), 400

        reward.amount = amount
        reward.date_paid = date_paid
        reward.payer_username = payer_username
        reward.payer_id = payer.id
        db.session.commit()
        return jsonify({'message': 'Reward received successfully'}), 200
    except ValueError:
        return jsonify({'error': 'Invalid data format. Ensure all fields are correct.'}), 400
    except KeyError as e:
        return jsonify({'error': f'Missing field: {str(e)}'}), 400

@bp.route('/list_found_reports', methods=['GET'])
# @login_required
def list_all_found_reports():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 4

        found_reports_paginated = FoundReport.query.paginate(page=page, per_page=per_page)
        
        found_reports = [{
            'id': report.id,
            'item_name': report.item_name,
            'date_found': report.date_found.strftime('%Y-%m-%d'),
            'place_found': report.place_found,
            'description': report.description,
            'upload_image': report.upload_image
        } for report in found_reports_paginated.items]

        return jsonify({
            'found_reports': found_reports,
            'total_pages': found_reports_paginated.pages,
            'current_page': found_reports_paginated.page,
            'total_reports': found_reports_paginated.total
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/list_lost_reports', methods=['GET'])
# @login_required
def list_all_lost_reports():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 2

        lost_reports_paginated = LostReport.query.paginate(page=page, per_page=per_page)
        
        lost_reports = [{
            'id': report.id,
            'item_name': report.item_name,
            'date_lost': report.date_lost.strftime('%Y-%m-%d'),
            'place_lost': report.place_lost,
            'description': report.description,
            'upload_image': report.upload_image
        } for report in lost_reports_paginated.items]

        return jsonify({
            'lost_reports': lost_reports,
            'total_pages': lost_reports_paginated.pages,
            'current_page': lost_reports_paginated.page,
            'total_reports': lost_reports_paginated.total
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/pay_reward/<int:found_report_id>', methods=['POST'])
# @login_required
def pay_reward(found_report_id):
    found_report = FoundReport.query.get_or_404(found_report_id)

    reward = Reward.query.filter_by(found_report_id=found_report_id).first()
    if not reward:
        return jsonify({'error': 'No reward offered for this found report. Please offer a reward first.'}), 404

    data = request.json
    try:
        amount = float(data['amount'])
        date_paid = datetime.strptime(data['date_paid'], '%Y-%m-%d').date()

        if amount <= 0:
            return jsonify({'error': 'Reward amount must be positive.'}), 400

        reward.date_paid = date_paid
        db.session.commit()
        return jsonify({'message': 'Reward paid successfully'}), 200
    except ValueError:
        return jsonify({'error': 'Invalid data format. Ensure all fields are correct.'}), 400
    except KeyError as e:
        return jsonify({'error': f'Missing field: {str(e)}'}), 400

@bp.route('/return_item/<int:found_report_id>', methods=['POST'])
# @login_required
def return_item(found_report_id):
    found_report = FoundReport.query.get_or_404(found_report_id)
    item = found_report.item

    data = request.json
    user_id = data.get('user_id')

    if found_report.user_id != current_user.id:
        return jsonify({'error': 'You are not authorized to return this item.'}), 403

    if not item.is_claimed:
        return jsonify({'error': 'Item must be claimed before it can be returned.'}), 400

    if item.is_returned:
        return jsonify({'error': 'Item is already returned.'}), 400

    claim = Claim.query.filter_by(found_report_id=found_report_id, user_id=user_id).first()
    if not claim:
        return jsonify({'error': 'Invalid user ID or no claim found for this item.'}), 404

    try:
        item.is_returned = True
        db.session.commit()
        return jsonify({'message': 'Item returned successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error returning item: {str(e)}'}), 500

@bp.route('/my_rewards', methods=['GET'])
# @login_required
def view_my_rewards():
    rewards_received = Reward.query.filter_by(receiver_id=current_user.id).all()
    rewards_paid = Reward.query.filter_by(payer_id=current_user.id).all()
    
    return jsonify({
        'rewards_received': [reward.to_dict() for reward in rewards_received],
        'rewards_paid': [reward.to_dict() for reward in rewards_paid]
    }), 200

