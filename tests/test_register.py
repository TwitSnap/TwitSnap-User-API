import sys
import os
import pytest
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
from config.settings import init_database
from fastapi.testclient import TestClient
from neomodel import config, db
from main import create_app
from models.user import User 

init_database()
app = create_app()
client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_db():
    db.cypher_query("MATCH (n) DETACH DELETE n")

def test_register_user():
    data = {"username": "testuser",
            "email": "testuser@example.com",
            "password": "stringst",
            "phone": "string",
            "country": "AR"}

    response = client.post("/api/v1/register", json=data)
    
    assert response.status_code == 201
    assert response.json()["username"] == "testuser"
    
    user = User.nodes.get(username="testuser")
    assert user is not None
    assert user.email == "testuser@example.com"

def test_register_user_with_existing_email():

    data = {"username": "testuser",
            "email": "testuser@example.com",
            "password": "stringst",
            "phone": "string",
            "country": "AR"}

    response = client.post("/api/v1/register", json=data)
    
    assert response.status_code == 201
    assert response.json()["username"] == "testuser"
    
    response = client.post("/api/v1/register", json=data)
    assert response.status_code == 409

def test_register_with_invalid_email():
    data = {"username": "testuser",
            "email": ""}
    response = client.post("/api/v1/register", json=data)
    assert response.status_code == 422
