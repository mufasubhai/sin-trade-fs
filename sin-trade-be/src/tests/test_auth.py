import pytest
from app import create_app
from models.user_model import User
from utils.number_utils import generate_random_number
from utils.string_utils import generate_random_string

    


@pytest.mark.parametrize("title", ["Test login with incorrect credentials"])
def test_login_fail(client, title):
    """Test login with correct credentials"""
    response = client.post(
        '/auth/login', 
        json={
            'email': 'aapodaca+2@gmail.com', 
            'password': '6798Akumosan2!'
        }
    )
    response_data = response.get_json()  # Need to get the JSON data from response
    
    assert response.status_code == 401  # Use response.status_code instead of response[1]

    assert 'message' in response_data
    assert response_data['message'] == 'Invalid login credentials'
    
    
    
    
@pytest.mark.parametrize("title", ["Test login with correct credentials"])
def test_login_success(client, title):
    """Test login with correct credentials"""
    response = client.post(
        '/auth/login', 
        json={
            'email': 'aapodaca+2@gmail.com', 
            'password': '6798Akumosan!'
        }
    )
    response_data = response.get_json()  # Need to get the JSON data from response
    assert response.status_code == 200  # Use response.status_code instead of response[1]

    assert 'access_token' in response_data
    assert 'refresh_token' in response_data
    assert 'aud' in response_data
    assert response_data['aud'] == 'authenticated'
    
    
@pytest.mark.parametrize("title", ["Test login with correct credentials"])
def test_signup_success(client, title):
    """Test signup with success"""
    email = f'aapodaca+{generate_random_number()}@gmail.com'
    username = generate_random_string(10)
    response = client.post(
        '/auth/signup',
        json={
            'email': email,
            'password': '6798Akumosan!',
            'first_name': 'Adrian',
            'last_name': 'Apodaca',
            'username': username
        }
    )
    
    
    assert response.status_code == 200
    response_data = response.get_json()
    assert 'aud' in response_data
    assert response_data['aud'] == 'authenticated'

    
    

#     """Test login with missing required fields"""
#     response = client.post(
#         '/auth/login',
#         json={
#             'email': 'aapodaca@gmail.com'
#         }
#     )
#     assert response.status_code == 400
#     response_data = response.get_json()
#     assert 'error' in response_data

# def test_login_invalid_email_format(client):
#     """Test login with invalid email format"""
#     response = client.post(
#         '/auth/login',
#         json={
#             'email': 'invalid_email',
#             'password': 'somepassword'
#         }
#     )
#     assert response.status_code == 400
#     response_data = response.get_json()
#     assert 'error' in response_data