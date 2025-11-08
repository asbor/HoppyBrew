from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from database import Base
import enum


class UserRole(enum.Enum):
    """User role enumeration for role-based access control"""
    admin = "admin"
    brewer = "brewer"
    viewer = "viewer"


class Users(Base):
    """
    Description:

    This class represents the User table in the database.

    The user is also referred to as the brewer.

    Relationships:

    - ONE user/brewer can have ZERO or MANY recipes
    - ONE user/brewer can have ZERO or MANY equipment_profiles
    - ONE user/brewer can have ZERO or MANY fermentation_profiles
    - ONE user/brewer can have ZERO or MANY mash_profiles
    - ONE user/brewer can have ZERO or MANY water_profiles

    Notes:
    - The relationship between the User and Recipe tables is defined in the
    Recipe table

    - The relationship between the User and EquipmentProfile tables is defined
    in the EquipmentProfile table

    - The relationship between the User and FermentationProfile tables is
    defined in the FermentationProfile table

    - The relationship between the User and MashProfile tables is defined in
    the MashProfile table

    - The relationship between the User and WaterProfile tables is defined in
    the WaterProfile table

    """

    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    # Kept for backwards compatibility
    password = Column(String, nullable=True)
    # New secure password field
    hashed_password = Column(String(255), nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)

    # New authentication and authorization fields
    role = Column(Enum(UserRole), default=UserRole.viewer, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        server_default=func.now(), onupdate=func.now())

    @property
    def full_name(self):
        """Get user's full name"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name or self.last_name or self.username

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}', role='{self.role}')>"
