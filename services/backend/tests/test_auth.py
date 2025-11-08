"""
Test authentication endpoints
"""

from auth import get_password_hash
from Database.Models.users import Users, UserRole


def test_user_registration(client):
    """Test user registration"""
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123",
        "first_name": "Test",
        "last_name": "User",
        "role": "viewer",
    }

    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "password" not in data  # Password should not be returned


def test_user_login(client, db_session):
    """Test user login"""
    # Create a test user first
    hashed_password = get_password_hash("testpassword123")
    user = Users(
        username="loginuser",
        email="login@example.com",
        hashed_password=hashed_password,
        role=UserRole.viewer,
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()

    # Test login
    response = client.post(
        "/auth/token", data={"username": "loginuser", "password": "testpassword123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_get_current_user(client, db_session):
    """Test getting current user information"""
    # Create and login user
    hashed_password = get_password_hash("testpassword123")
    user = Users(
        username="currentuser",
        email="current@example.com",
        hashed_password=hashed_password,
        role=UserRole.brewer,
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()

    # Login to get token
    response = client.post(
        "/auth/token", data={"username": "currentuser", "password": "testpassword123"}
    )
    token = response.json()["access_token"]

    # Test getting current user
    response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "currentuser"
    assert data["role"] == "brewer"


def test_protected_endpoint_without_token(client):
    """Test that protected endpoints require authentication"""
    response = client.get("/auth/me")
    assert response.status_code == 401


def test_admin_endpoint_requires_admin_role(client, db_session):
    """Test that admin endpoints require admin role"""
    # Create a regular user
    hashed_password = get_password_hash("testpassword123")
    user = Users(
        username="regularuser",
        email="regular@example.com",
        hashed_password=hashed_password,
        role=UserRole.viewer,
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()

    # Login as regular user
    response = client.post(
        "/auth/token", data={"username": "regularuser", "password": "testpassword123"}
    )
    token = response.json()["access_token"]

    # Try to access admin endpoint
    response = client.get("/admin/test", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403
