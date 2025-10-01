# controllers/asset_controller.py
from flask import Blueprint, request, jsonify
from src.services.asset_services import AssetService
from werkzeug.exceptions import HTTPException

asset_controller = Blueprint('asset_controller', __name__)

@asset_controller.route('/asset', methods=['POST', "DELETE", "GET"])
def add_asset():
    try:
        data = request.get_json()
        response_data, status_code = AssetService.addAsset(data)
        
        return response_data, status_code
    except HTTPException as e:
        
        return jsonify({'error': str(e.description)}), e.code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def delete_asset():
    try: 
        data = request.get_json()
        response_data, status_code = AssetService.deleteAsset(data)
        
        return response_data, status_code
    except HTTPException as e:
        
        return jsonify({'error': str(e.description)}), e.code
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
@asset_controller.route('/assets/<user_id>', methods=['GET'])
def list_assets(user_id):
    try: 
        response_data, status_code = AssetService.getActiveAssetsByUserId(user_id)
        return response_data, status_code
    
    except HTTPException as e:
        
        return jsonify({'error': str(e.description)}), e.code
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        