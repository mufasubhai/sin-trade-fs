# services/auth_services.py
from src.models.active_assets_model import ActiveAssets
from src.config import BackendConfig
from src.services.fetching_services.alphavantage_constants import fromToAlpha
from src.services.amqp_be_publisher import publish_message

class AssetService:
    @staticmethod

    def addAsset(data):
        try: 
            if BackendConfig.supabase:
            # may want to change this to a standard Auth Header param
                # BackendConfig.supabase.auth.set_session(data['access_token'], data['refresh_token'])
                
                # only crypto assets are supported at the moment
                if (data['is_crypto'] != True):
                    return {"message": "Only crypto assets are supported at the moment"}, 400
                
                # verify if asset exists in from_to_alpha for initial ffor initial fetching
                if data['ticker_code'].upper() not in fromToAlpha:
                    return {"message": "Asset not supported"}, 400
                
                # check to see if we have a record of this asset in active_assets
                active_asset_response = BackendConfig.supabase.table("active_assets").select('*').eq('ticker_code', data['ticker_code']).execute()
                
                user_asset_response = None
                asset_id = None
                initial_fetch_complete = False
                historical_data = None
                
                try:
                    if len(active_asset_response.data) > 0:
                        asset_id = active_asset_response.data[0]['id']
                        initial_fetch_complete =  active_asset_response.data[0]['initial_fetch_complete']
                    else:
                        add_asset_response = BackendConfig.supabase.table("active_assets").insert(
                            {
                                "ticker_code": data['ticker_code'],
                                ## we can add this later 
                                "ticker_code": "USD" if (data['ticker_code'] == None) else data['ticker_code'],
                                "is_crypto": data['is_crypto'],
                                "initial_fetch_complete": initial_fetch_complete,
                            }
                        ).execute()
                        asset_id = add_asset_response.data[0]['id']
                except Exception as e:
                    print("error", e)
                    return {"message": f"Error: {e}"}, 500

                # add asset to initial fetch queue
                if (initial_fetch_complete == False):
                    if (data["is_crypto"] == True):
                        publish_message("crypto_queue", data['ticker_code'])
                    if (data["is_crypto"] == False):
                        publish_message("stock_queue", data['ticker_code'])


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
                                        "ticker_name" : data["ticker_code"],
                                        "user_id" : data["user_id"],
                                        "asset_id" : asset_id,
                                    }
                                ).execute()
                            except Exception as e:
                                print("error", e)
                    else: 
                        return {"message": "User assets not found"}, 500
                    
                    # in the case of initial fetch being complete, we want to return historical data
                    if (initial_fetch_complete == True):
                        # need to verify whether or not this is actually correct
                        historical_data_response = BackendConfig.supabase.table("asset_prices").select("*").eq("from_asset_code", data['ticker_code']).execute()
                        historical_data = historical_data_response.data
                        
        
                return {
                        "message": "Asset added successfully",
                        "historical_data": historical_data,
                        "status": 200
                        }, 200
            return {"message": "Database connection unsuccessful"}, 500
        except Exception as e:
            return {"message": str(e)}, 401
    
    
    @staticmethod
    def getActiveAssetsByUserId(user_id):
        try:
            if BackendConfig.supabase:
                response = BackendConfig.supabase.table("user_assets").select("*").eq("user_id", user_id).execute()
                return {"data": response.data,"message": "Assets fetched successfully", "status": 200}, 200
            return {"message": "Database connection unsuccessful"}, 500
        except Exception as e:
            return {"message": str(e)}, 401



    # @staticmethod
    def deleteUserAsset(asset_id, user_id):
        try:
            if BackendConfig.supabase:
                response = BackendConfig.supabase.table("user_assets").delete().eq("asset_id", asset_id).eq("user_id", user_id).execute()
                return {"message": "Asset deleted successfully", "status": 200, "data": {"asset_id": asset_id, "user_id": user_id},}, 200
            return {"message": "Database connection unsuccessful", "status": 500}, 500
        except Exception as e:
            return {"message": str(e), "status": 500}, 500
    
    # @staticmethod   
    # def listAssets(data)
