from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from flask_login import login_required, current_user
from app.models.item import Item
from app.extensions import db

bp = Blueprint('upload', __name__, url_prefix='/upload')

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/item/<int:item_id>', methods=['POST'])
# @login_required
def upload_item_image(item_id):
    item = Item.query.get_or_404(item_id)
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        item.image_url = url_for('static', filename=f'uploads/{filename}', _external=True)
        db.session.commit()
        return jsonify({"success": True, "image_url": item.image_url}), 200
    return jsonify({"error": "File not allowed"}), 400

