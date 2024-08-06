from flask import Blueprint, request, jsonify, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from app.extensions import db, bcrypt

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid input'}), 400

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirm_password')
    role = data.get('role', 'user')  # Default to 'user' if not provided

    if not username or not email or not password or not confirm_password:
        return jsonify({'error': 'Missing required fields'}), 400

    if password != confirm_password:
        return jsonify({'error': 'Passwords do not match'}), 400

    if User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first():
        return jsonify({'error': 'Email or username already exists'}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(
        username=username,
        email=email,
        password_hash=hashed_password,
        role=role
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Registration successful!'}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid input'}), 400

    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        login_user(user)
        print(f"User logged in with role: {user.role}")  # Debug line to print the role
        return jsonify({'message': 'Login successful!', 'role': user.role, 'username': user.username}), 200
    else:
        return jsonify({'error': 'Login failed. Check your email and password.'}), 400

@bp.route('/logout', methods=['POST'])
# @login_required
def logout():
    logout_user()
    return jsonify({'message': 'You have been logged out.'}), 200