#!/usr/bin/env python3
from flask import Flask, request, jsonify
from flask_cors import CORS

from src.routes.test_routes import init_test_routes

from src.services.ds_job_scheduler import  check_history
from apscheduler.schedulers.background import BackgroundScheduler
from src.services.amqp_ds_subscriber import subscribe_to_queues
from src.services.amqp_ds_publisher import declare_queues


def create_app():
    app = Flask(__name__)
    app.config.from_object("src.config.DSConfig")
    CORS(app, origins=app.config["CORS_ORIGINS"].split(","))

    print(app.config)

    @app.route("/health")
    def health_check():
        return jsonify({"status": "healthy"}), 200

    init_test_routes(app)

    return app  #


app = create_app()


if __name__ == "src.app":
    try:
        scheduler = BackgroundScheduler()
        scheduler.add_executor("processpool")
        scheduler.add_job(check_history, "interval", minutes=1)
        scheduler.add_job(check_history, "interval", minutes=5)
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
        scheduler.add_job(check_history, "interval", minutes=1)
        scheduler.add_job(check_history, "interval", minutes=5)
        declare_queues()
        subscribe_to_queues()
        scheduler.start()
    except Exception as e:
        print(f"Failed to start scheduler: {e}")
    except (KeyboardInterrupt, SystemExit):
        print("Scheduler stopped by user")
        pass
