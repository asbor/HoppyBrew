from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated, List
from sqlalchemy.orm import Session
from database import get_db
from Database.Models.users import Users, UserRole
from Database.Schemas.auth import UserCreate, UserResponse, UserUpdate, Token, LoginRequest
from auth import (
    get_password_hash, authenticate_user, create_access_token, get_current_active_user,
    require_admin, require_brewer, ACCESS_TOKEN_EXPIRE_MINUTES
)
from datetime import timedelta

router = APIRouter()

# Use dependency injection instead of module-level database session
db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: db_dependency):
    """Register a new user"""
    # Check if user already exists
    if db.query(Users).filter(Users.username == user.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    if db.query(Users).filter(Users.email == user.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = Users(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        role=user.role,
        is_active=user.is_active
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.post("/auth/token", response_model=Token)
def login_for_access_token(db: db_dependency, form_data: OAuth2PasswordRequestForm = Depends()):
    """Login and get access token"""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/auth/me", response_model=UserResponse)
def read_current_user(current_user: Users = Depends(get_current_active_user)):
    """Get current user information"""
    return current_user


@router.get("/users/", response_model=List[UserResponse])
def list_users(db: db_dependency, current_user: Users = Depends(require_admin)):
    """List all users (admin only)"""
    return db.query(Users).all()


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: db_dependency, current_user: Users = Depends(get_current_active_user)):
    """Get user by ID"""
    # Users can only see their own profile unless they're admin
    if current_user.role != UserRole.admin and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate, db: db_dependency,
                current_user: Users = Depends(get_current_active_user)):
    """Update user information"""
    # Users can only update their own profile unless they're admin
    if current_user.role != UserRole.admin and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Update fields that were provided
    update_data = user_update.model_dump(exclude_unset=True)

    # Hash password if provided
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(
            update_data.pop("password"))

    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: db_dependency, current_user: Users = Depends(require_admin)):
    """Delete user (admin only)"""
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    db.delete(user)
    db.commit()

# Protected endpoint examples


@router.get("/admin/test")
def admin_only_endpoint(current_user: Users = Depends(require_admin)):
    """Test endpoint that requires admin role"""
    return {"message": "Hello admin!", "user": current_user.username}


@router.get("/brewer/test")
def brewer_endpoint(current_user: Users = Depends(require_brewer)):
    """Test endpoint that requires brewer role"""
    return {"message": "Hello brewer!", "user": current_user.username}
