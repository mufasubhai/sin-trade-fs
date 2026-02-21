import pytest
import json


class TestRoutes:
    def test_main_route(self, client):
        response = client.get('/')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 200
        assert "we've made a successful call" in data['data']

    def test_health_route(self, client):
        response = client.get('/health')
        assert response.status_code == 200
        assert b"up 1" in response.data

    def test_health_route_prometheus_metrics(self, client):
        response = client.get('/health')
        assert response.status_code == 200
        assert b"up 1" in response.data

    def test_404_route(self, client):
        response = client.get('/nonexistent')
        assert response.status_code == 404
