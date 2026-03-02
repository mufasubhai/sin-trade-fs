#!/usr/bin/env python3
from flask import Flask, request, jsonify, Response
from flask_cors import CORS

from src.routes.test_routes import init_test_routes
from apscheduler.schedulers.background  import BackgroundScheduler

from src.services.ds_job_scheduler import  check_targets, run_ml_trading_cron, compute_ticker_stats
from src.services.amqp_ds_subscriber import subscribe_to_queues
from src.services.amqp_ds_publisher import declare_queues


def create_app():
    app = Flask(__name__)
    app.config.from_object("src.config.DSConfig")
    CORS(app, origins=app.config["CORS_ORIGINS"].split(","))

    print(app.config)

    # Docker container health check (Prometheus-compatible)
    @app.route("/health")
    def health_check():
        metrics = """# HELP up Service health status
# TYPE up gauge
up 1
"""
        return Response(metrics, mimetype="text/plain")

    init_test_routes(app)

    return app  #


app = create_app()


if __name__ == "src.app":
    try:
        scheduler = BackgroundScheduler()
        scheduler.add_executor("processpool")
        # scheduler.add_job(check_targets, "interval", minutes=5)
        # scheduler.add_job(run_ml_trading_cron, "interval", seconds=30)
        # scheduler.add_job(compute_ticker_stats, "interval", minutes=5)
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
        scheduler.add_job(check_targets, "interval", minutes=5)
        scheduler.add_job(run_ml_trading_cron, "interval", hours=1)
        scheduler.add_job(compute_ticker_stats, "interval", hours=1)
        declare_queues()
        subscribe_to_queues()
        scheduler.start()
    except Exception as e:
        print(f"Failed to start scheduler: {e}")
    except (KeyboardInterrupt, SystemExit):
        print("Scheduler stopped by user")
        pass
