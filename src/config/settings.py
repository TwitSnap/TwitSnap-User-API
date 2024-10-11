import os
from neomodel import config, db
from dotenv import load_dotenv
from neo4j import GraphDatabase
from utils.logger import Logger

load_dotenv()
HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))
DB_PROTOCOL = os.getenv("DB_PROTOCOL")
DB_URI = os.getenv("DB_HOST_PORT")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
SECRET_KEY = os.getenv("SECRET_KEY")
AUTH_API_URI = os.getenv("AUTH_API_URI")
AUTH_API_REGISTER_PATH = os.getenv("AUTH_API_REGISTER_PATH")
AUTH_API_LOGIN_PATH = os.getenv("AUTH_API_LOGIN_PATH")
DB_TEST_URL = 'bolt://neo4j:testpassword@localhost:7687'
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE  = os.getenv("LOG_FILE", "user_ms.log")

logger = Logger(LOG_LEVEL, LOG_FILE)

def connect_to_database():
    try:
        config.DATABASE_URL = f"{DB_PROTOCOL}://{DB_USERNAME}:{DB_PASSWORD}@{DB_URI}"
        db.set_connection(config.DATABASE_URL)
        config.connection_timeout = 20
        logger.info(f"Connecting to database at {config.DATABASE_URL}")
        db.cypher_query("MATCH (n) DETACH DELETE n")
        logger.info("Successfully connected to the database.")
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        