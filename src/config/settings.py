import os
from neomodel import config, db
from dotenv import load_dotenv
from utils.logger import Logger
from models.interest import Interest
import redis

load_dotenv()
HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))
DB_PROTOCOL = os.getenv("DB_PROTOCOL")
DB_URI = os.getenv("DB_HOST_PORT")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
AUTH_API_URI = os.getenv("AUTH_API_URI")
ENV = os.getenv("ENV")
AUTH_API_REGISTER_PATH = os.getenv("AUTH_API_REGISTER_PATH")
AUTH_API_LOGIN_PATH = os.getenv("AUTH_API_LOGIN_PATH")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "user_ms.log")
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
DEFAULT_PROFILE_PHOTO = os.getenv("DEFAULT_PROFILE_PHOTO")
NOTIFICATION_SENDER = os.getenv("NOTIFICATION_SENDER")
FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")
NOTIFICATION_DESTINATION_COPY = os.getenv("NOTIFICATION_DESTINATION_COPY")
SERVICE_REGISTRY_URI = os.getenv("SERVICE_REGISTRY_URI")
SERVICE_REGISTRY_VERIFY_PATH = os.getenv("SERVICE_REGISTRY_VERIFY_PATH")
INTERESTS = [
    "entretenimiento",
    "videojuegos",
    "música",
    "noticias",
    "deportes",
    "tecnología",
    "comida",
    "salud",
]
API_KEY = os.getenv("API_KEY")
if ENV == "dev":
    DB_PASSWORD = os.getenv("DB_PASSWORD_TEST")
    DB_URI = os.getenv("DB_HOST_PORT_TEST")
else:
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_URI = os.getenv("DB_HOST_PORT")

logger = Logger(LOG_LEVEL, LOG_FILE)


def init_database():
    try:
        config.DATABASE_URL = f"{DB_PROTOCOL}://{DB_USERNAME}:{DB_PASSWORD}@{DB_URI}"
        db.set_connection(config.DATABASE_URL)
        config.connection_timeout = 60
        config.AUTO_RECONNECT = True
        logger.info(f"Connecting to database at {config.DATABASE_URL}")

        for interest in INTERESTS:
            i = Interest.nodes.get_or_none(name=interest)
            if i is None:
                Interest(name=interest).save()
                logger.debug(f"Interest {interest} created.")
            else:
                logger.debug(f"Interest {interest} already exists.")

        logger.info("Successfully connected to the database.")
    except Exception as e:
        logger.error(f"Database connection error: {e}")


def init_redis():
    try:
        logger.info(
            f"Initializing Redis connection at {REDIS_HOST}:{REDIS_PORT} - username: {REDIS_USERNAME} - password: {REDIS_PASSWORD}"
        )
        conn = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            username=REDIS_USERNAME,
            password=REDIS_PASSWORD,
        )
        conn.ping()
        logger.info("Redis connection initialized successfully.")
        return conn
    except Exception as e:
        logger.error(f"Redis initialization error: {e}")


redis_conn = init_redis()
