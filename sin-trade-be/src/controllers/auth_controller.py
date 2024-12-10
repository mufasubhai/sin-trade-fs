# controllers/auth_controller.py
from flask import Blueprint, request, jsonify
from services.auth_services import AuthService

auth_controller = Blueprint('auth_controller', __name__)

@auth_controller.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = AuthService.login(data)
    return jsonify(user), 200

@auth_controller.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    user = AuthService.signup(data)
    return jsonify(user), 201

@auth_controller.route('/logout', methods=['POST'])
def logout():
    AuthService.logout()
    return jsonify({"message": "Logged out successfully"}), 200
