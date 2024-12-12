import pytest

def test_main(client):
    response = client.get('/')
    assert response.status_code == 200
    assert "we've made a successful call" in response.data.decode('utf-8')
