from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import User, db

auth_blueprint = Blueprint('auth', __name__)

# Registration route
@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.json
    new_user = User(username=data['username'], role=data['role'])
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(message="User registered"), 201

# Login route
@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity={"username": user.username, "role": user.role})
        return jsonify(access_token=access_token), 200
    return jsonify(message="Invalid credentials"), 401

# Route to access users (only for Superadmin and Admin roles)
@auth_blueprint.route('/users', methods=['GET'])
@jwt_required()  # Requires a valid JWT token
def get_users():
    current_user = get_jwt_identity()  # Get the logged-in user from the token
    role = current_user['role']

    # Restrict access to only Superadmin and Admin roles
    if role in ['Superadmin', 'Admin']:
        users = User.query.all()  # Fetch all users from the database
        result = []
        for user in users:
            result.append({
                'username': user.username,
                'role': user.role
            })
        return jsonify(users=result), 200
    return jsonify(message="Access forbidden: Admins or Superadmins only"), 403

