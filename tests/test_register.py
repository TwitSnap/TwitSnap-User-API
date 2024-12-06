import sys
import os
import pytest



sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
from repositories import user_repository
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

def test_refresh_pin_register():
    user = create_user()
    response = client.post(f"/api/v1/user/{user.uid}/pin")
    assert response.status_code == 200

def test_register_confirmation():


# utils
def create_user(username="testuser", email="testuser@example.com", phone="1234567890", country="AR"):
    user = User(username=username, email=email, phone=phone,country=country)
    user_repository.save(user)
    return user