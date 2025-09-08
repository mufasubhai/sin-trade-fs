# services/auth_services.py
from src.models.active_assets_model import ActiveAssets
from src.config import BackendConfig
from flask import jsonify


class AssetService:
    @staticmethod

    def addAsset(data):
        try: 
            if BackendConfig.supabase:
            # may wan tto change this to a standard Auth Header param
                # BackendConfig.supabase.auth.set_session(data['access_token'], data['refresh_token'])
                
                active_asset_response = BackendConfig.supabase.table("active_assets").select('*').eq('ticker_code', data['ticker_code']).execute()
                
                user_asset_response = None;
                asset_id = None
                
                try:
                    if len(active_asset_response.data) > 0:
                        asset_id = active_asset_response.data[0]['id']
                    else:
                        add_asset_response = BackendConfig.supabase.table("active_assets").insert(
                            {
                                "ticker_code": data['ticker_code'],
                                "is_crypto": data['is_crypto']
                            }
                        ).execute()
                        asset_id = add_asset_response.data[0]['id']
                except Exception as e:
                    print("error", e)
                    return {"message": f"Error: {e}"}, 500
                        

                # print("ticker code", data['ticker_code'])

                if asset_id is None:
                    return {"message": "Something went wrong"}, 500
                else: 
                    try: 
                        user_asset_response = BackendConfig.supabase.table("user_assets").select("*").eq("id", asset_id).execute()
                    except Exception as e:
                        print("error", e)
                        return {"message": f"Error: {e}"}, 500
                
                    if user_asset_response:
                        if len(user_asset_response.data) > 0:
                            return {"message": "Asset already exists"}, 500
                        else: 
                            try: 
                                BackendConfig.supabase.table("user_assets").insert(
                                    {
                                        "ticker_name": data["ticker_code"],
                                        "user_id": data["user_id"].to_Int(),
                                        "asset_id": asset_id
                                        
                                    }
                                ).execute()
                            except Exception as e:
                                print("error", e)
                    else: 
                        return {"message": "User assets not found"}, 500
        
                return {"message": "Asset added successfully"}, 200
            return {"message": "Database connection unsuccessful"}, 500
        except Exception as e:
            return {"message": str(e)}, 401
    
    # @staticmethod
    # def deleteAsset(data):
    
    # @staticmethod   
    # def listAssets(data)
