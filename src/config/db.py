# db/database.py
import os
from dotenv import load_dotenv
from neomodel import config, db
from authlib.integrations.starlette_client import OAuth, OAuthError

load_dotenv()

oauth = OAuth()
oauth.register(
    name = 'google',
    server_metadata_url = 'https://accounts.google.com/.well-known/openid-configuration',
    authorize_url = 'https://accounts.google.com/o/oauth2/auth',
    client_id = os.getenv('CLIENT_ID'),
    client_secret = os.getenv('CLIENT_SECRET'),
    client_kwargs = {'scope': 'email openid profile',})

def get_database_url():
    protocol = os.getenv("NEO4J_PROTOCOL")
    url = os.getenv("NEO4J_HOST_PORT")
    username = os.getenv("NEO4J_USERNAME")
    password = os.getenv("NEO4J_PASSWORD")
    return f"{protocol}://{username}:{password}@{url}"

def connect_to_database():
    config.DATABASE_URL = get_database_url()
    try:
        db.cypher_query("MATCH (n) RETURN n LIMIT 1")
        print("Conexión exitosa a la base de datos.")
    except Exception as e:
        print("Error de conexión:", e)

