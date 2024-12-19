#!/usr/bin/env python3
from flask import Flask, request
from flask_cors import CORS
import logging
# from routes.auth_routes import init_auth_routes
from src.routes.test_routes import init_test_routes

# from models.user_model import db

def create_app():
    app = Flask(__name__)
    app.config.from_object('src.config.DSConfig') 
    CORS(app, origins=app.config["CORS_ORIGINS"].split(','))
    
    logging.info(app.config) 
    
    @app.route('/health')
    def health_check():
        return jsonify({"status": "healthy"}), 200

    # add routes
    # init_auth_routes(app)
    init_test_routes(app)
    
    return app    # 

app = create_app()

if __name__ == '__main__':
    app.run()