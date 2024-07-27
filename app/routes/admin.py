from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models.item import Item
from app.models.lost_report import LostReport
from app.models.found_report import FoundReport
from app.models.claim import Claim
from app.models.reward import Reward
from app.extensions import db
from app.utils.image_utils import handle_image_upload
from app.utils.decorators import admin_required
import os

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    try:
        lost_reports = LostReport.query.all()
        found_reports = FoundReport.query.all()
        claims = Claim.query.all()
        rewards = Reward.query.all()
        return render_template('admin_dashboard.html', lost_reports=lost_reports, found_reports=found_reports, claims=claims, rewards=rewards)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


        



@bp.route('/items', methods=['GET', 'POST'])
@login_required
@admin_required
def add_item():
    if request.method == 'POST':
        try:
            data = request.form
            image_url = handle_image_upload(request.files.get('image'), None)  # Upload image if provided
            item = Item(name=data['name'], description=data.get('description'), image_url=image_url)
            db.session.add(item)
            db.session.commit()
            return jsonify({'message': 'Item added successfully'}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return render_template('add_item.html')

@bp.route('/list_items', methods=['GET'])
@login_required
@admin_required
def list_items():
    try:
        items = Item.query.all()
        return render_template('list_items.html', items=items)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/items/<int:item_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def update_item(item_id):
    item = Item.query.get_or_404(item_id)
    
    if request.method == 'POST':
        try:
            data = request.form
            image_url = handle_image_upload(request.files.get('image'), item_id)  # Update image if provided
            item.name = data['name']
            item.description = data.get('description')
            if image_url:
                item.image_url = image_url
            db.session.commit()
            return redirect(url_for('admin.list_items'))
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return render_template('update_item.html', item=item)


@bp.route('/items/<int:item_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_item(item_id):
    try:
        item = Item.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': 'Item deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@bp.route('/reports/lost', methods=['GET'])
@login_required
@admin_required
def view_lost_reports():
    try:
        lost_reports = LostReport.query.all()
        return render_template('list_lost_reports.html', lost_reports=lost_reports)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/reports/found', methods=['GET'])
@login_required
@admin_required
def view_found_reports():
    try:
        found_reports = FoundReport.query.all()
        return render_template('list_found_reports.html', found_reports=found_reports)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/claims', methods=['GET'])
@login_required
@admin_required
def view_claims():
    try:
        claims = Claim.query.all()
        return render_template('list_claims.html', claims=claims)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/rewards', methods=['GET'])
@login_required
@admin_required
def view_rewards():
    try:
        rewards = Reward.query.all()
        return render_template('list_rewards.html', rewards=rewards)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/reports/lost/<int:report_id>/approve', methods=['POST'])
@login_required
@admin_required
def approve_lost_report(report_id):
    try:
        report = LostReport.query.get_or_404(report_id)
        report.approved = True
        db.session.commit()
        return redirect(url_for('admin.view_lost_reports'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500
