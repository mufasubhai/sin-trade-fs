# controllers/asset_controller.py
from flask import Blueprint, request, jsonify
from src.services.asset_services import AssetService
from werkzeug.exceptions import HTTPException
from src.middleware.auth_middleware import require_auth

asset_controller = Blueprint('asset_controller', __name__)

@asset_controller.route('/add_asset', methods=['POST'])
@require_auth
def add_asset():
    try:
        data = request.get_json()
        response_data, status_code = AssetService.addAsset(data)
        
        return response_data, status_code
    except HTTPException as e:
        
        return jsonify({'error': str(e.description)}), e.code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# def delete_asset():
#     try: 
#         data = request.get_json()
#         response_data, status_code = AssetService.deleteAsset(data)
        
#         return response_data, status_code
#     except HTTPException as e:
        
#         return jsonify({'error': str(e.description)}), e.code
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
    
    
@asset_controller.route('/assets/<user_id>', methods=['GET'])
@require_auth
def list_assets(user_id):
    try: 
        response_data, status_code = AssetService.getActiveAssetsByUserId(user_id)
        return response_data, status_code
    
    except HTTPException as e:
        
        return jsonify({'error': str(e.description)}), e.code
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        

@asset_controller.route('/history/<ticker_code>', methods=['GET'])
@require_auth
def asset_history(ticker_code):
    try:
        days = request.args.get('days', 14, type=int)
        response_data, status_code = AssetService.getAssetHistory(ticker_code, days)
        return response_data, status_code
    except HTTPException as e:
        return jsonify({'error': str(e.description)}), e.code
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@asset_controller.route('/asset/<asset_id>/<user_id>', methods=['DELETE'])
@require_auth
def single_asset(asset_id, user_id):
    if request.method == 'DELETE':
        return  AssetService.deleteUserAsset(asset_id, user_id)
    else:
        return jsonify({'error': 'Invalid method'}), 405

