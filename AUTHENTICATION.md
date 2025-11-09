# Authentication System Documentation

## Overview

HoppyBrew now has a complete JWT-based authentication and authorization system implemented and tested.

## Features

### 1. User Management
- User registration with email validation
- Secure password storage using bcrypt hashing
- User profiles with first name, last name, and username
- User activation/deactivation (is_active flag)
- Email verification support (is_verified flag)

### 2. Role-Based Access Control (RBAC)

Three user roles are supported:
- **viewer**: Read-only access to public endpoints
- **brewer**: Can create and manage recipes, batches, and brewing data
- **admin**: Full system access, can manage users and system configuration

Role hierarchy: admin > brewer > viewer

### 3. Authentication Flow

#### Registration
```bash
POST /auth/register
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword123",
  "first_name": "John",
  "last_name": "Doe",
  "role": "brewer"
}
```

#### Login
```bash
POST /auth/token
Content-Type: application/x-www-form-urlencoded

username=johndoe&password=securepassword123
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### Accessing Protected Endpoints
Include the JWT token in the Authorization header:
```bash
GET /auth/me
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 4. Protected Endpoints

#### Public Endpoints
- POST /auth/register - Register new user
- POST /auth/token - Login

#### User Endpoints (Requires Authentication)
- GET /auth/me - Get current user information
- GET /users/{id} - Get user by ID
- PUT /users/{id} - Update user (own profile or admin)
- DELETE /users/{id} - Delete user (admin only)

#### Admin Endpoints (Requires Admin Role)
- GET /users/ - List all users

## Security Features

### Password Security
- Passwords are hashed using bcrypt with automatic salting
- Plain passwords are never stored in the database
- Minimum password length enforcement recommended (implement in frontend)

### JWT Token Security
- Tokens expire after 30 minutes (configurable via ACCESS_TOKEN_EXPIRE_MINUTES)
- Tokens are signed using HS256 algorithm
- Secret key is configurable via environment variables
- Token payload includes username and expiration time

### Environment Configuration
All security-sensitive settings are configurable via environment variables:

```bash
# Required in production
SECRET_KEY=your-secret-key-at-least-32-characters-long
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database configuration
DATABASE_URL=postgresql://user:pass@localhost:5432/hoppybrew_db

# CORS configuration
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
```

## Database Schema

The `user` table includes:
- `id` (Primary Key)
- `username` (Unique, Indexed)
- `email` (Unique, Indexed)
- `password` (Deprecated, for backwards compatibility)
- `hashed_password` (Bcrypt hash)
- `first_name`
- `last_name`
- `role` (Enum: admin, brewer, viewer)
- `is_active` (Boolean)
- `is_verified` (Boolean)
- `created_at` (Timestamp)
- `updated_at` (Timestamp)

## Migration

The user authentication system is created by migration 0007:
```bash
# Run migrations to create the user table
cd /home/runner/work/HoppyBrew/HoppyBrew
TESTING=1 alembic upgrade head
```

## Testing

All authentication functionality is tested:
- User registration
- User login with JWT token generation
- Protected endpoint access control
- Role-based authorization
- Invalid credentials handling

Run tests:
```bash
cd services/backend
TESTING=1 pytest tests/test_auth.py -v
```

Current test results: **5/5 tests passing** ✅

## Usage Examples

### Python Client Example
```python
import requests

# Register a new user
response = requests.post('http://localhost:8000/auth/register', json={
    'username': 'brewer1',
    'email': 'brewer1@example.com',
    'password': 'securepass123',
    'role': 'brewer'
})
print(f"User created: {response.json()}")

# Login
response = requests.post('http://localhost:8000/auth/token', data={
    'username': 'brewer1',
    'password': 'securepass123'
})
token = response.json()['access_token']

# Access protected endpoint
headers = {'Authorization': f'Bearer {token}'}
response = requests.get('http://localhost:8000/auth/me', headers=headers)
print(f"Current user: {response.json()}")
```

### JavaScript/TypeScript Example
```typescript
// Login
const loginResponse = await fetch('http://localhost:8000/auth/token', {
  method: 'POST',
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  body: new URLSearchParams({
    username: 'brewer1',
    password: 'securepass123'
  })
});
const { access_token } = await loginResponse.json();

// Access protected endpoint
const userResponse = await fetch('http://localhost:8000/auth/me', {
  headers: { 'Authorization': `Bearer ${access_token}` }
});
const user = await userResponse.json();
console.log('Current user:', user);
```

## Production Deployment

### Required Steps

1. **Set SECRET_KEY**
   ```bash
   # Generate a secure random key
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   # Add to .env file
   SECRET_KEY=<generated-key>
   ```

2. **Configure Database**
   ```bash
   DATABASE_URL=postgresql://user:password@host:5432/database
   ```

3. **Run Migrations**
   ```bash
   alembic upgrade head
   ```

4. **Create Admin User**
   ```python
   from auth import get_password_hash
   from Database.Models.users import Users, UserRole
   from database import SessionLocal
   
   db = SessionLocal()
   admin = Users(
       username='admin',
       email='admin@yourdomain.com',
       hashed_password=get_password_hash('your-admin-password'),
       role=UserRole.admin,
       is_active=True,
       is_verified=True
   )
   db.add(admin)
   db.commit()
   ```

5. **Enable HTTPS**
   - Use a reverse proxy (nginx, Apache) with SSL/TLS
   - Set SSL_REDIRECT=true in production

## Security Considerations

### Implemented
✅ Password hashing with bcrypt
✅ JWT token-based authentication
✅ Role-based access control
✅ Environment-based configuration
✅ Token expiration
✅ Secure password storage (never plain text)
✅ SQL injection protection (SQLAlchemy ORM)
✅ CORS configuration

### Recommended Enhancements
- Rate limiting on login endpoint
- Password complexity requirements
- Account lockout after failed attempts
- Two-factor authentication (2FA)
- Password reset via email
- Refresh tokens for long-lived sessions
- Audit logging for authentication events

## Troubleshooting

### Common Issues

**Issue**: "Could not validate credentials" error
- **Solution**: Check if token is expired or SECRET_KEY has changed

**Issue**: "Not enough permissions" error  
- **Solution**: User role doesn't have access to endpoint. Check role requirements.

**Issue**: "SECRET_KEY must be at least 32 characters"
- **Solution**: Generate a proper SECRET_KEY as shown in production deployment section

**Issue**: Tests failing with "no such table: user"
- **Solution**: Ensure Users model is imported in Database/Models/__init__.py
- **Solution**: Check that conftest.py uses StaticPool for SQLite :memory: databases

## Further Reading

- [FastAPI Security Documentation](https://fastapi.tiangolo.com/tutorial/security/)
- [JWT.io](https://jwt.io/) - JWT token debugger
- [Passlib Documentation](https://passlib.readthedocs.io/)
- [OAuth2 Password Flow](https://oauth.net/2/grant-types/password/)
