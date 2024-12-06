import sys
import os
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
from services.user_service import user_service
from repositories.user_repository import UserRepository
from config.settings import init_database, REGISTER_PIN_TTL, redis_conn
from fastapi.testclient import TestClient
from neomodel import db
from main import create_app
from models.user import User 

init_database()
app = create_app()
user_repository = UserRepository(db)
client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_db():
    db.cypher_query("MATCH (n) DETACH DELETE n")

def test_register_user():
    data = {"username": "testuser",
            "email": "testuser@example.com",
            "password": "stringst",
            "phone": "string",
            "country": "AR",
            "interests": ["entretenimiento"]}

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
def test_register_user_with_invalid_interests():
    data = {"username": "testuser",
            "email": "testuser@example.com",
            "password": "stringst",
            "phone": "string",
            "country": "AR",
            "interests": ["random"]}

    response = client.post("/api/v1/register", json=data)
    assert response.status_code == 422

def test_register_with_invalid_email():
    data = {"username": "testuser",
            "email": ""}
    response = client.post("/api/v1/register", json=data)
    assert response.status_code == 422

def test_refresh_pin_register():
    user = create_user()
    response = client.post(f"/api/v1/users/{user.uid}/pin")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_verify_pin_register():
    user = create_user()
    pin = user_service.generate_pin()
    # await user_service.generate_register_pin(user.uid, pin) falla notis
    redis_conn.setex(f"{user.uid}", REGISTER_PIN_TTL, pin)

    json = {
        "id": user.uid,
        "pin": pin
    }
    response = client.post(f"/api/v1/users/confirmation", json = json)
    user = user_repository.find_user_by_id(user.uid)
    assert response.status_code == 200
    assert user.verified == True

# utils
def create_user(username="testuser", email="testuser@example.com", phone="1234567890", country="AR"):
    user = User(username=username, email=email, phone=phone,country=country)
    user_repository.save(user)
    return user