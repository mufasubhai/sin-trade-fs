## all of our tests have access to this config. We can pass a client as a argument to our tests to expose
import pytest
from .app import create_app

@pytest.fixture(scope='module')
def app():
    app = create_app()
    app.config['TESTING'] = True
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@hostname/test_database'
    
    with app.app_context():
        yield app

@pytest.fixture(scope='module')
def client(app):
    return app.test_client()

@pytest.fixture(scope='module')
def runner(app):
    return app.test_cli_runner()