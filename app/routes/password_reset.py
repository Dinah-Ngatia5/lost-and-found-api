from flask import Blueprint, request, jsonify
from app.models.user import User
from app.models.password_reset import PasswordResetToken
from app.extensions import db, bcrypt, mail
from flask_mail import Message

bp = Blueprint('password_reset', __name__, url_prefix='/password_reset')

@bp.route('/request', methods=['POST'])
def request_password_reset():
    data = request.json
    email = data.get('email')
    
    if not email:
        return jsonify({'error': 'Email is required'}), 400

    user = User.query.filter_by(email=email).first()
    if user:
        token = PasswordResetToken.generate_token(user)
        db.session.add(token)
        db.session.commit()
        
        reset_link = f"/reset-password/{token.token}"  # Frontend route
        msg = Message('Password Reset Request', recipients=[email])
        msg.body = f'Please use the following link to reset your password: {reset_link}'
        mail.send(msg)

    # Always return a success message to prevent email enumeration
    return jsonify({'message': 'If the email is registered, you will receive a password reset link.'}), 200

@bp.route('/reset/<token>', methods=['POST'])
def reset_password(token):
    token_entry = PasswordResetToken.query.filter_by(token=token).first()
    if not token_entry or token_entry.is_expired():
        return jsonify({'error': 'Invalid or expired token'}), 400

    data = request.json
    new_password = data.get('password')
    confirm_password = data.get('confirm_password')

    if not new_password or not confirm_password:
        return jsonify({'error': 'Password and confirmation are required'}), 400

    if new_password != confirm_password:
        return jsonify({'error': 'Passwords do not match'}), 400

    user = User.query.get(token_entry.user_id)
    if user:
        user.password = new_password
        db.session.delete(token_entry)
        db.session.commit()
        return jsonify({'message': 'Password has been reset successfully'}), 200
    else:
        return jsonify({'error': 'User not found'}), 404

@bp.route('/validate/<token>', methods=['GET'])
def validate_token(token):
    token_entry = PasswordResetToken.query.filter_by(token=token).first()
    if token_entry and not token_entry.is_expired():
        return jsonify({'valid': True}), 200
    return jsonify({'valid': False}), 200
