import pytest
import os

from app.main import app
from hamcrest import assert_that, equal_to, has_entries, has_item

TEST_DB = "db/integration_test.db"

os.makedirs("db", exist_ok=True)

@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()


def test_hello_default(client):
    response = client.get('/hello')
    assert response.status_code == 200
    assert b"Hello, mysterious visitor" in response.data

def test_hello_with_name(client):
    response = client.get('/hello?name=Yasin')
    assert response.status_code == 200
    assert b"Hello, Yasin" in response.data

def test_hello_form(client):
    response = client.get('/hello-form')
    assert response.status_code == 200
    assert b"Say Hello" in response.data
    assert b"Your name:" in response.data
