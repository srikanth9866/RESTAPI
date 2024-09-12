from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

dashboard_blueprint = Blueprint('dashboard', __name__)

# Superadmin/Admin dashboard
@dashboard_blueprint.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    current_user = get_jwt_identity()
    if current_user['role'] == 'Superadmin':
        # Superadmin can see all users
        return jsonify(message="Superadmin Dashboard - View All Users")
    elif current_user['role'] == 'Admin':
        # Admin can see only their users
        return jsonify(message="Admin Dashboard - View Limited Users")
    else:
        return jsonify(message="Access Denied"), 403

