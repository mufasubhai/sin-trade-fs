import pytest
from tests.test_utils import generate_random_string


from app import create_app
from models.user_model import User

def test_signup(client):
    new_email :str  = "a.apodaca" + "+" + generate_random_string(5) + "@gmail.com"
    response = client.post('/auth/signup', json={'email': new_email, 'password': 'testpass'})
    assert response.status_code == 201


def test_login_fail(client):
    response = client.post('/auth/login', json={'email': 'aapodaca@gmail.com', 'password': 'thisisthewrongpass', })
    assert response.status_code == 401
    
    
def test_login(client):
    response = client.post('/auth/login', json={'email': 'aapodaca@gmail.com', 'password': '6798Akumosan!' })
    assert response.status_code == 200
    
