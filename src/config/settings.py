import os
from neomodel import config, db
from dotenv import load_dotenv
from neo4j import GraphDatabase
from utils.logger import Logger
import json
import redis
from firebase_admin import credentials, initialize_app

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
FIREBASE_CREDENTIALS = os.getenv("FIREBASE_CREDENTIALS")
FIREBASE_STORAGE_BUCKET = os.getenv("FIREBASE_STORAGE_BUCKET")
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_USERNAME = os.getenv("REDIS_USERNAME")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
REGISTER_PIN_LENGHT = int(os.getenv("REGISTER_PIN_LENGHT"))
REGISTER_PIN_TTL = os.getenv("REGISTER_PIN_TTL")
NOTIFICATION_API_URI = os.getenv("NOTIFICATION_API_URI")
NOTIFICATION_API_SEND_PATH = os.getenv("NOTIFICATION_API_SEND_PATH")
logger = Logger(LOG_LEVEL, LOG_FILE)

def init_database():
    try:
        config.DATABASE_URL = f"{DB_PROTOCOL}://{DB_USERNAME}:{DB_PASSWORD}@{DB_URI}"
        db.set_connection(config.DATABASE_URL)
        config.connection_timeout = 20
        logger.info(f"Connecting to database at {config.DATABASE_URL}")
        # db.cypher_query("MATCH (n) DETACH DELETE n")
        logger.info("Successfully connected to the database.")
    except Exception as e:
        logger.error(f"Database connection error: {e}")

def init_firebase():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__)) 
        logger.info(f"Initializing Firebase with credentials from {current_dir}")
        firebase_credentials_path = os.path.join(current_dir, '..', '..', 'twitsnap-82671-firebase-adminsdk-q3c3c-7613007f9d.json')
        cred = credentials.Certificate(firebase_credentials_path)
        initialize_app(cred, {
            'storageBucket': FIREBASE_STORAGE_BUCKET
        })
        logger.info("Firebase initialized successfully.")
    except Exception as e:
        logger.error(f"Firebase initialization error: {e}")

def init_redis():
    try:
        logger.info(f"Initializing Redis connection at {REDIS_HOST}:{REDIS_PORT} - username: {REDIS_USERNAME} - password: {REDIS_PASSWORD}")
        conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, username=REDIS_USERNAME,password=REDIS_PASSWORD)
        conn.ping()
        logger.info("Redis connection initialized successfully.")
        return conn
    except Exception as e:
        logger.error(f"Redis initialization error: {e}")

redis_conn = init_redis()