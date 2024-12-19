# controllers/auth_controller.py
from flask import Blueprint, request, jsonify
from src.services.auth_services import AuthService
from werkzeug.exceptions import HTTPException

auth_controller = Blueprint('auth_controller', __name__)

@auth_controller.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        response_data, status_code = AuthService.login(data)
        
        return response_data, status_code
    except HTTPException as e:
        
        return jsonify({'error': str(e.description)}), e.code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_controller.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        response_data, status_code = AuthService.signup(data)
        return response_data, status_code
    except HTTPException as e:
        return jsonify({'error': str(e.description)}), e.code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_controller.route('/logout', methods=['POST'])
def logout():
    try:
        response_data, status_code = AuthService.logout(data)
        return response_data, status_code
        return jsonify({'error': str(e.description)}), e.code
    except Exception as e:
        return jsonify({'error': str(e)}), 500