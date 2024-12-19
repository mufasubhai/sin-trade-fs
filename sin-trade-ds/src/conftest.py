## all of our tests have access to this config. We can pass a client as a argument to our tests to expose
import pytest
import os
import sys
# import logging
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.app import create_app  # No

@pytest.fixture(scope='session')
def app():
    app = create_app()
    app.config['TESTING'] = True
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@hostname/test_database'
    
    with app.app_context():
        yield app

@pytest.fixture(scope='session')
def client(app):
    return app.test_client()

@pytest.fixture(scope='session')
def runner(app):
    return app.test_cli_runner()