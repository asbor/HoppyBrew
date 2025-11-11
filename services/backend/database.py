"""
Database configuration module with lazy initialization.

This module provides database connectivity using SQLAlchemy with proper
connection pooling and lazy initialization. The database engine is only
created when first accessed, avoiding repeated initialization on module import.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy.engine import Engine
import os
import time
from typing import Generator, Optional
from logger_config import get_logger
from config import settings


class _DatabaseManager:
    """
    Singleton database manager that handles lazy initialization.
    """

    def __init__(self):
        self._engine: Optional[Engine] = None
        self._SessionLocal: Optional[sessionmaker] = None
        self._initialized: bool = False

    def _wait_for_postgresql(self, max_retries: int = 30, retry_delay: int = 1) -> None:
        """
        Wait for PostgreSQL to become available.

        Args:
            max_retries: Maximum number of connection attempts
            retry_delay: Delay in seconds between retries

        Raises:
            Exception: If PostgreSQL is not available after max_retries
        """
        import psycopg

        logger = get_logger("database")
        logger.info("Waiting for PostgreSQL to be available")

        for i in range(max_retries):
            try:
                conn = psycopg.connect(
                    host=settings.DATABASE_HOST,
                    port=settings.DATABASE_PORT,
                    user=settings.DATABASE_USER,
                    password=settings.DATABASE_PASSWORD,
                    dbname="postgres",  # Connect to default database first
                )
                conn.close()
                logger.info("PostgreSQL is available")
                return
            except psycopg.OperationalError:
                if i < max_retries - 1:
                    logger.debug(f"Waiting for PostgreSQL... ({i + 1}/{max_retries})")
                    time.sleep(retry_delay)
                else:
                    logger.error("Could not connect to PostgreSQL after maximum retries")
                    raise Exception("Could not connect to PostgreSQL")

    def _create_database_if_not_exists(self, engine: Engine) -> None:
        """
        Create the database if it doesn't exist.

        Args:
            engine: SQLAlchemy engine instance
        """
        from sqlalchemy_utils import database_exists, create_database

        logger = get_logger("database")

        if not database_exists(engine.url):
            logger.info("Creating database")
            create_database(engine.url)
        else:
            logger.debug("Database already exists")

    def initialize(self) -> Engine:
        """
        Initialize the database engine and session factory.
        This function is called lazily on first access.

        Returns:
            Engine: SQLAlchemy engine instance
        """
        if self._initialized:
            return self._engine

        logger = get_logger("database")

        # Determine if we are in testing mode
        is_testing = os.getenv("TESTING", "0") == "1"

        if is_testing:
            database_url = settings.TEST_DATABASE_URL
            logger.debug(f"Using test database: {database_url}")
            # For SQLite tests, ensure the engine can be shared across threads
            self._engine = create_engine(
                database_url,
                echo=False,  # Disable echo in tests to reduce noise
                connect_args={"check_same_thread": False},
                pool_pre_ping=True,  # Verify connections before using
            )
        else:
            database_url = settings.DATABASE_URL
            logger.info("Initializing database connection")
            
            # Check if using SQLite or PostgreSQL
            if database_url.startswith('sqlite'):
                logger.info("Using SQLite database")
                # For SQLite, enable foreign keys and WAL mode for better performance
                self._engine = create_engine(
                    database_url,
                    echo=False,
                    connect_args={"check_same_thread": False},
                    pool_pre_ping=True,
                )
            else:
                logger.info("Using PostgreSQL database")
                # Wait for PostgreSQL to be ready
                self._wait_for_postgresql()

                # Create the engine with connection pooling
                self._engine = create_engine(
                    database_url,
                    echo=False,  # Disable SQLAlchemy echo to reduce log noise
                    pool_pre_ping=True,  # Verify connections before using
                    pool_size=5,  # Connection pool size
                    max_overflow=10,  # Maximum overflow connections
                )

                # Create database if it doesn't exist
                self._create_database_if_not_exists(self._engine)
        # Create session factory
        self._SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self._engine)

        self._initialized = True
        logger.info("Database initialized successfully")

        return self._engine

    @property
    def engine(self) -> Engine:
        """Get the database engine, initializing if necessary."""
        if not self._initialized:
            self.initialize()
        return self._engine

    @property
    def SessionLocal(self) -> sessionmaker:
        """Get the session factory, initializing if necessary."""
        if not self._initialized:
            self.initialize()
        return self._SessionLocal


# Create singleton instance
_db_manager = _DatabaseManager()

# Create a base class for the models to inherit from (declarative base)
Base = declarative_base()


# Use __getattr__ to provide lazy access to engine and SessionLocal
def __getattr__(name):
    """
    Module-level attribute access with lazy initialization.
    This allows importing engine and SessionLocal without triggering initialization.
    """
    if name == "engine":
        return _db_manager.engine
    elif name == "SessionLocal":
        return _db_manager.SessionLocal
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


def initialize_database() -> Engine:
    """
    Explicitly initialize the database.
    Can be called to ensure database is ready before use.

    Returns:
        Engine: SQLAlchemy engine instance
    """
    return _db_manager.initialize()


def get_engine() -> Engine:
    """
    Get the database engine, initializing it if necessary.

    Returns:
        Engine: SQLAlchemy engine instance
    """
    return _db_manager.engine


def get_session_local() -> sessionmaker:
    """
    Get the session factory, initializing the database if necessary.

    Returns:
        sessionmaker: SQLAlchemy session factory
    """
    return _db_manager.SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    Dependency injection function for FastAPI endpoints.
    Provides a database session and ensures it's closed after use.

    Yields:
        Session: SQLAlchemy database session
    """
    session_factory = get_session_local()
    db = session_factory()
    try:
        yield db
    finally:
        db.close()
