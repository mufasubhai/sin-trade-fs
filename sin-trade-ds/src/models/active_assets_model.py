class ActiveAssets:
    def __init__(self, assets_list):
        active_dict = {}
        
        # The line `# if assets_list. > 0:` is a commented-out line in the code. Comments in Python
        # start with the `#` symbol and are used to provide explanations or notes within the code for
        # better understanding.
    # if assets_list. > 0:
        for asset in assets_list:
            active_dict[asset['ticker_name']] = Asset(asset)
            
        self.active_assets = active_dict
        
    def to_dict(self):
        new_dict = {}
        
        for ticker_name, asset in self.active_assets.items():
            new_dict[ticker_name] = asset.to_dict()
        
        return  {'active_assets': new_dict}

class Asset:
    def __init__(self, asset_data):
        self.id = asset_data.get('id')
        self.created_at = asset_data.get('created_at')
        self.ticker_name = asset_data.get('ticker_name')
        self.user_id = asset_data.get('user_id')
        self.asset_id = asset_data.get('asset_id')
        
    def to_dict(self):
        return {
            'id': self.id,
            'created_at': self.created_at,
            'asset_id': self.asset_id,
            'ticker_name': self.ticker_name,
            'user_id': self.user_id,
        }
        
