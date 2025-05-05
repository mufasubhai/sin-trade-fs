# services/auth_services.py
from src.models.user_model import User, ProfileResponse
from src.models.active_assets_model import ActiveAssets
from src.config import BackendConfig
from flask import jsonify


class AssetService:
    @staticmethod
    def addAsset(data):
        try: 
            if BackendConfig.supabase:
            # may wan tto change this to a standard Auth Header param
                BackendConfig.supabase.auth.set_session(data['access_token'], data['refresh_token'])
                
                active_asset_response = BackendConfig.supabase.table("active_assets").upsert(
                    {
                        "ticker_code" : data["ticker_code"],
                        "is_crypto": data["is_crypto"]
                    }
                )
                
                # here we need to get the asset id from the active asset response
                asset_id = active_asset_response.data[0]['id']
                
            
                BackendConfig.supabase.table("user_assets").upsert(
                    {
                        "user_id": data["user_id"],
                        "asset_id": asset_id
                    }
                )
                return {"message": "Asset added successfully"}, 200
            return {"message": "Database connection unsuccessful"}, 500
        except Exception as e:
            return {"message": str(e)}, 401
    
    # @staticmethod
    # def deleteAsset(data):
    
    # @staticmethod   
    # def listAssets(data)
