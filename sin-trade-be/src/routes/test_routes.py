from flask import Blueprint, request, jsonify

test_controller = Blueprint('test_controller', __name__)

@test_controller.route('/', methods=['get'])
def main():
    response_data = {
        "status": 200,
        "data": "this has been a success"
    }
    return jsonify(response_data), 200


def init_test_routes(app):
    app.register_blueprint(test_controller)