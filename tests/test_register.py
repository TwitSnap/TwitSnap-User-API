import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
import pytest
from fastapi.testclient import TestClient
from neomodel import config, db
from main import create_app
from models.user import User 
from exceptions.conflict_exception import ConflictException

app = create_app()
client = TestClient(app)
config.DATABASE_URL ='bolt://neo4j:testpassword@localhost:7687'
@pytest.fixture(autouse=True)
def clear_db():
    db.cypher_query("MATCH (n) DETACH DELETE n")

def test_register_user():
    data = {"register_type": "email",
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "stringst",
            "phone": "string",
            "country": "string"}

    response = client.post("/api/v1/register", json=data)
    
    assert response.status_code == 201
    assert response.json()["username"] == "testuser"
    
    user = User.nodes.get(username="testuser")
    assert user is not None
    assert user.email == "testuser@example.com"

def test_register_user_with_existing_email():

    data = {"register_type": "email",
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "stringst",
            "phone": "string",
            "country": "string"}

    response = client.post("/api/v1/register", json=data)
    
    assert response.status_code == 201
    assert response.json()["username"] == "testuser"
    
    response = client.post("/api/v1/register", json=data)
    assert response.status_code == 409