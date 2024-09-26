import os
from neomodel import config, db
from dotenv import load_dotenv
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

SECRET_KEY = "9c41616324b0b9bc4120097e00f161f6faa92e13b7445898861e962857c45b89bed3863f5c52f6e730a2bccbd886bf7f606d794021db48b9c86d9f0376be7bbfea5f8843e985064a1aa2d3712084fea04b7a8f0fc570811c77f8bd0c4942a318722f7c25439f7794e38764df2a77cb79211c46e827a880f8b6916655fe77845ad8157d104a6c9aa83b3140e2389d9369a00ba9802880ed3598c828a9998d54985f0411d64d7a43a5c11af496a69f128d81682c51b2d096afecb5f5ebde43ea2b1d2b1021247ae5f8c84e124ae670c824b7cd6eca6529a005eda46ccbf1fdcc01a00e985ad6f1c88fe672e1b5f6f6f2890094052c50b156aa50b451bdf1f40495"

def get_database_url():
    protocol = os.getenv("NEO4J_PROTOCOL")
    url = os.getenv("NEO4J_HOST_PORT")
    username = os.getenv("NEO4J_USERNAME")
    password = os.getenv("NEO4J_PASSWORD")
    return f"{protocol}://{username}:{password}@{url}"

def connect_to_database():
    try:
        config.DATABASE_URL = get_database_url()
        print(f"Connecting to database at {config.DATABASE_URL}")
        db.cypher_query("MATCH (n) RETURN n LIMIT 1")
        print("Successfully connected to the database.")
    except Exception as e:
        print("Database connection error:", e)
        