"""Test database configuration logic to ensure correct database is used."""

import os
import sys
from unittest.mock import patch, MagicMock


def test_database_url_with_testing_enabled():
    """Test that SQLite is used when TESTING=1."""
    # We need to reload the database module with TESTING=1
    # First remove it from sys.modules if already loaded
    if "database" in sys.modules:
        del sys.modules["database"]

    with patch.dict(os.environ, {"TESTING": "1"}):
        # Import database module
        import database

        assert database.IS_TESTING is True
        assert database.SQLALCHEMY_DATABASE_URL.startswith("sqlite://")


def test_database_url_with_testing_disabled():
    """Test that PostgreSQL is used when TESTING=0."""
    # Remove database module from cache
    if "database" in sys.modules:
        del sys.modules["database"]

    # Set environment variables for PostgreSQL
    env_vars = {
        "TESTING": "0",
        "DATABASE_USER": "testuser",
        "DATABASE_PASSWORD": "testpass",
        "DATABASE_HOST": "testhost",
        "DATABASE_PORT": "5432",
        "DATABASE_NAME": "testdb",
    }

    # Mock psycopg2 connection to avoid actual database connection
    with patch.dict(os.environ, env_vars), \
         patch("psycopg2.connect") as mock_connect, \
         patch("sqlalchemy_utils.database_exists") as mock_exists:

        # Setup mocks
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        mock_exists.return_value = True

        # Import database module
        import database

        assert database.IS_TESTING is False
        expected_url = "postgresql://testuser:testpass@testhost:5432/testdb"
        assert database.SQLALCHEMY_DATABASE_URL == expected_url


def test_testing_env_var_string_0_is_falsy():
    """Test string '0' in TESTING env var is correctly evaluated as False."""
    # This is the key test - ensuring "0" is not truthy
    if "database" in sys.modules:
        del sys.modules["database"]

    env_vars = {
        "TESTING": "0",
        "DATABASE_USER": "postgres",
        "DATABASE_PASSWORD": "postgres",
        "DATABASE_HOST": "localhost",
        "DATABASE_PORT": "5432",
        "DATABASE_NAME": "hoppybrew_db",
    }

    with patch.dict(os.environ, env_vars), \
         patch("psycopg2.connect") as mock_connect, \
         patch("sqlalchemy_utils.database_exists") as mock_exists:

        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        mock_exists.return_value = True

        import database

        # The key assertion: TESTING="0" should result in IS_TESTING=False
        assert database.IS_TESTING is False
        # And therefore should use PostgreSQL, not SQLite
        assert not database.SQLALCHEMY_DATABASE_URL.startswith("sqlite://")
        assert database.SQLALCHEMY_DATABASE_URL.startswith("postgresql://")


def test_testing_env_var_string_1_is_truthy():
    """Test string '1' in TESTING env var is correctly evaluated as True."""
    if "database" in sys.modules:
        del sys.modules["database"]

    with patch.dict(os.environ, {"TESTING": "1"}):
        import database

        # TESTING="1" should result in IS_TESTING=True
        assert database.IS_TESTING is True
        # And therefore should use SQLite
        assert database.SQLALCHEMY_DATABASE_URL.startswith("sqlite://")


def test_testing_env_var_not_set():
    """Test when TESTING not set, defaults to production (PostgreSQL)."""
    if "database" in sys.modules:
        del sys.modules["database"]

    # Ensure TESTING is not in environment
    env_vars = {
        "DATABASE_USER": "postgres",
        "DATABASE_PASSWORD": "postgres",
        "DATABASE_HOST": "localhost",
        "DATABASE_PORT": "5432",
        "DATABASE_NAME": "hoppybrew_db",
    }

    # Remove TESTING if it exists
    env_copy = os.environ.copy()
    if "TESTING" in env_copy:
        del env_copy["TESTING"]
    env_copy.update(env_vars)

    with patch.dict(os.environ, env_copy, clear=True), \
         patch("psycopg2.connect") as mock_connect, \
         patch("sqlalchemy_utils.database_exists") as mock_exists:

        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        mock_exists.return_value = True

        import database

        # When not set, should default to False (production/PostgreSQL)
        assert database.IS_TESTING is False
        assert database.SQLALCHEMY_DATABASE_URL.startswith("postgresql://")
