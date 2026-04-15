import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_hello_world_status(client):
    response = client.get("/")
    assert response.status_code == 200


def test_hello_world_content(client):
    response = client.get("/")
    assert b"Hello World" in response.data
