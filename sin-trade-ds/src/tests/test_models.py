import pytest
from src.models.active_assets_model import ActiveAssets, Asset


class TestModels:
    def test_asset_init(self):
        asset_data = {
            "id": 1,
            "created_at": "2024-01-01",
            "ticker_name": "BTC",
            "user_id": "user123",
            "asset_id": 100
        }
        
        asset = Asset(asset_data)
        
        assert asset.id == 1
        assert asset.ticker_name == "BTC"
        assert asset.user_id == "user123"
        assert asset.asset_id == 100

    def test_asset_init_with_missing_fields(self):
        asset_data = {"id": 1}
        
        asset = Asset(asset_data)
        
        assert asset.id == 1
        assert asset.ticker_name is None
        assert asset.user_id is None

    def test_asset_to_dict(self):
        asset_data = {
            "id": 1,
            "created_at": "2024-01-01",
            "ticker_name": "BTC",
            "user_id": "user123",
            "asset_id": 100
        }
        
        asset = Asset(asset_data)
        result = asset.to_dict()
        
        assert result["id"] == 1
        assert result["ticker_name"] == "BTC"
        assert result["user_id"] == "user123"
        assert result["asset_id"] == 100
        assert result["created_at"] == "2024-01-01"

    def test_active_assets_init(self):
        assets_list = [
            {
                "ticker_name": "BTC",
                "id": 1,
                "created_at": "2024-01-01",
                "user_id": "user123",
                "asset_id": 100
            },
            {
                "ticker_name": "ETH",
                "id": 2,
                "created_at": "2024-01-01",
                "user_id": "user123",
                "asset_id": 101
            }
        ]
        
        active_assets = ActiveAssets(assets_list)
        
        assert "BTC" in active_assets.active_assets
        assert "ETH" in active_assets.active_assets

    def test_active_assets_init_empty(self):
        assets_list = []
        
        active_assets = ActiveAssets(assets_list)
        
        assert active_assets.active_assets == {}

    def test_active_assets_to_dict(self):
        assets_list = [
            {
                "ticker_name": "BTC",
                "id": 1,
                "created_at": "2024-01-01",
                "user_id": "user123",
                "asset_id": 100
            }
        ]
        
        active_assets = ActiveAssets(assets_list)
        result = active_assets.to_dict()
        
        assert "active_assets" in result
        assert "BTC" in result["active_assets"]
