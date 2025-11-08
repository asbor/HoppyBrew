# database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os
import time
from logger_config import get_logger

# Get logger instance

logger = get_logger("Setup")

# Load environment variables

logger.info("Loading environment variables")
load_dotenv()

# Determine if we are in testing mode

IS_TESTING = os.getenv("TESTING", "0") == "1"
logger.info(f"IS_TESTING: {IS_TESTING}")
if IS_TESTING:
    SQLALCHEMY_DATABASE_URL = os.getenv(
        "TEST_DATABASE_URL", "sqlite:///./test_fermentables.db"
    )
else:
    db_user = os.getenv("DATABASE_USER")
    db_password = os.getenv("DATABASE_PASSWORD")
    db_host = os.getenv("DATABASE_HOST")
    db_port = os.getenv("DATABASE_PORT")
    db_name = os.getenv("DATABASE_NAME")

    # Validate required environment variables
    if not all([db_user, db_password, db_host, db_port, db_name]):
        missing_vars = []
        if not db_user:
            missing_vars.append("DATABASE_USER")
        if not db_password:
            missing_vars.append("DATABASE_PASSWORD")
        if not db_host:
            missing_vars.append("DATABASE_HOST")
        if not db_port:
            missing_vars.append("DATABASE_PORT")
        if not db_name:
            missing_vars.append("DATABASE_NAME")
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing_vars)}"
        )

    SQLALCHEMY_DATABASE_URL = (
        f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    )

# Connect to the database

logger.info(f"Connecting to the database: {SQLALCHEMY_DATABASE_URL}")

# Determine if SQLAlchemy should echo SQL statements
DB_ECHO = os.getenv("DB_ECHO", "false").lower() == "true"

if IS_TESTING:
    # For SQLite tests, ensure the engine can be shared across threads
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        echo=DB_ECHO,
        connect_args={"check_same_thread": False},
    )
else:
    # For PostgreSQL, wait for it to be ready and create database if needed
    from sqlalchemy_utils import database_exists, create_database
    import psycopg2

    # Wait for PostgreSQL to be ready
    logger.info("Waiting for PostgreSQL to be available")
    max_retries = 30
    retry_delay = 1  # seconds

    for i in range(max_retries):
        try:
            conn = psycopg2.connect(
                host=os.getenv("DATABASE_HOST"),
                port=os.getenv("DATABASE_PORT"),
                user=os.getenv("DATABASE_USER"),
                password=os.getenv("DATABASE_PASSWORD"),
                database="postgres",  # Connect to default database first
            )
            conn.close()
            logger.info("PostgreSQL is available")
            break
        except psycopg2.OperationalError as e:
            if i < max_retries - 1:
                logger.info(f"Waiting for PostgreSQL... ({i+1}/{max_retries})")
                time.sleep(retry_delay)
            else:
                logger.error(
                    f"Failed to connect to PostgreSQL after {max_retries} "
                    "attempts"
                )
                raise ConnectionError(
                    f"Could not connect to PostgreSQL at {db_host}:{db_port} "
                    f"after {max_retries} attempts. Last error: {str(e)}"
                )

    # Create the engine
    engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=DB_ECHO)

    # Create database if it doesn't exist
    if not database_exists(engine.url):
        logger.info("Creating the database")
        create_database(engine.url)

# Create a session local

logger.info("Database is available")
logger.info("Creating a session local")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for the models to inherit from (declarative base)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
