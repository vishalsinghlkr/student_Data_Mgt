from flask import Blueprint, request, jsonify, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from functools import wraps
from .models import db, User

auth = Blueprint('auth', __name__)
login_manager = LoginManager()
login_manager.login_view = 'auth.login_users'

# ------------ Role Checker ------------
def role_required(role):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.role != role:
                abort(403)
            return f(*args, **kwargs)
        return wrapped
    return decorator

# ------------ User Loader ------------
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ------------ Register ------------
@auth.route('/register-user', methods=['POST'])
def register_user():
    """
    Register a user
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - role
            - email
            - password_hash
          properties:
            role:
              type: string
              example: admin
            email:
              type: string
              example: admin@example.com
            password_hash:
              type: string
              example: Admin@123
    responses:
      200:
        description: User registered successfully
    """
    data = request.get_json()
    role = data.get('role')
    email = data.get('email')
    password = data.get('password_hash')

    if not all([role, email, password]):
        return jsonify({"error": "Missing required fields"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User already exists"}), 409

    user = User(role=role, email=email, password_hash=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 200

# ------------ Login ------------
@auth.route('/login', methods=['POST'])
def login_users():
    """
    User login
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - role
            - email
            - password_hash
          properties:
            role:
              type: string
              example: admin
            email:
              type: string
              example: admin@example.com
            password_hash:
              type: string
              example: Admin@123
    responses:
      200:
        description: User logged in
      401:
        description: Invalid credentials
    """
    data = request.get_json()
    role = data.get('role')
    email = data.get('email')
    password = data.get('password_hash')

    if not all([role, email, password]):
        return jsonify({"error": "Missing required fields"}), 400

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password_hash, password):
        login_user(user)
        return jsonify({"message": f"{role} logged in successfully"}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

# ------------ Admin Route ------------
@auth.route('/admin', methods=['GET'])
@login_required
@role_required('admin')
def admin_page():
    return jsonify({"message": " Welcome Admin "}), 200

# ------------ Logout ------------
@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200
