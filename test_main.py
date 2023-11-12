from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_add_story():
    params = {
        'author': 'test',
        'title': 'test',
        'story': 'test',
    }
    response = client.post("/api/add_story", json=params)
    assert response.status_code == 201
    assert 'author' in response.json()


def test_get_stories():
    response = client.get("/api/get_five_stories")
    assert response.status_code == 200


def test_get_stories_by_title():
    params = {
        'query_str': 'test'
    }
    response = client.get("/api/get_stories_search", params=params)
    assert response.status_code == 200
