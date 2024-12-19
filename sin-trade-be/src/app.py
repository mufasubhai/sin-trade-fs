#!/usr/bin/env python3
from flask import Flask, request
from flask_cors import CORS
import logging
from src.routes.auth_routes import init_auth_routes
from src.routes.test_routes import init_test_routes

# from models.user_model import db

def create_app():
    app = Flask(__name__)
    app.config.from_object('src.config.BackendConfig') 
    CORS(app, origins=app.config["CORS_ORIGINS"].split(','))
    
    logging.info(app.config) 

    init_test_routes(app)
    # add routes
    # The line `init_auth_routes(app)` is likely a function call that initializes the authentication
    # routes for the Flask application. This function is expected to be defined elsewhere in the
    # codebase and is responsible for setting up the routes related to user authentication, such as
    # login, registration, password reset, etc.
    init_auth_routes(app)
    # init_test_routes(app)
    
    return app    # 

app = create_app()

if __name__ == '__main__':
    app.run()