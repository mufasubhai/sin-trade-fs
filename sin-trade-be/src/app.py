#!/usr/bin/env python3
from flask import Flask, request, jsonify
from flask_cors import CORS
from src.routes.auth_routes import init_auth_routes
from src.routes.test_routes import init_test_routes
from src.routes.asset_routes import init_asset_routes
from apscheduler.schedulers.background  import BackgroundScheduler
from src.services.amqp_be_subscriber import subscribe_to_queues
from src.services.amqp_be_publisher import declare_queues


# from models.user_model import db
def create_app():
    app = Flask(__name__)
    app.config.from_object("src.config.BackendConfig")
    CORS(app, origins=app.config["CORS_ORIGINS"].split(","))

    print(app.config)

    # Docker container health check
    @app.route("/health")
    def health_check():
        return jsonify({"status": "healthy"}), 200

    init_test_routes(app)
    init_asset_routes(app)
    init_auth_routes(app)

    return app


app = create_app()

# let's think about timing here.
if __name__ == "src.app":
    try:
        scheduler = BackgroundScheduler()
        scheduler.add_executor("processpool")
        declare_queues()
        subscribe_to_queues()
        scheduler.start()
    except Exception as e:
        print(f"Failed to start scheduler: {e}")
    except (KeyboardInterrupt, SystemExit):
        print("Scheduler stopped by user")
        pass

if __name__ == "__main__":
    try:
        scheduler = BackgroundScheduler()
        scheduler.add_executor("processpool")
        declare_queues()
        subscribe_to_queues()
        scheduler.start()
    except Exception as e:
        print(f"Failed to start scheduler: {e}")
    except (KeyboardInterrupt, SystemExit):
        print("Scheduler stopped by user")
        pass
