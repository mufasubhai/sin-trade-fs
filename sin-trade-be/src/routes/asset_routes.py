# routes/auth_routes.py
from src.controllers.asset_controller import asset_controller

def init_asset_routes(app):
    app.register_blueprint(asset_controller, url_prefix='/assets')
