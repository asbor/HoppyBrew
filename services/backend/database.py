# database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import time
from logger_config import get_logger
from config import settings

# Get logger instance

logger = get_logger("Setup")

# Determine if we are in testing mode

IS_TESTING = os.getenv("TESTING", "0") == "1"
logger.info(f"IS_TESTING: {IS_TESTING}")
if IS_TESTING:
    SQLALCHEMY_DATABASE_URL = settings.TEST_DATABASE_URL
else:
    SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Connect to the database

logger.info(f"Connecting to the database: {SQLALCHEMY_DATABASE_URL}")

if IS_TESTING:
    # For SQLite tests, ensure the engine can be shared across threads
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        echo=True,
        connect_args={"check_same_thread": False},
    )
else:
    # For PostgreSQL, wait for it to be ready and create database if needed
    from sqlalchemy_utils import database_exists, create_database
    import psycopg2

    # Wait for PostgreSQL to be ready
    logger.info("Waiting for PostgreSQL to be available")
    max_retries = 30
    for i in range(max_retries):
        try:
            conn = psycopg2.connect(
                host=settings.DATABASE_HOST,
                port=settings.DATABASE_PORT,
                user=settings.DATABASE_USER,
                password=settings.DATABASE_PASSWORD,
                database="postgres",  # Connect to default database first
            )
            conn.close()
            logger.info("PostgreSQL is available")
            break
        except psycopg2.OperationalError:
            if i < max_retries - 1:
                logger.info(f"Waiting for PostgreSQL... ({i+1}/{max_retries})")
                time.sleep(1)
            else:
                raise Exception("Could not connect to PostgreSQL")

    # Create the engine
    engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

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
