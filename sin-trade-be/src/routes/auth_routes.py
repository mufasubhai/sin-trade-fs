# routes/auth_routes.py
from src.controllers.auth_controller import auth_controller

def init_auth_routes(app):
    app.register_blueprint(auth_controller, url_prefix='/auth')
