import pytest

def test_main(client):
    response = client.get('/')
    assert response.status_code == 200
    assert "this has been a success" in response.data.decode('utf-8')
