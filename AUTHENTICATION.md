# Authentication System Guide

## Overview

Your Face Attendance System now has a complete JWT-based authentication system with support for role-based access control (RBAC).

### Supported Roles
- **Student**: Can mark attendance and view their own records
- **Teacher**: Can create lectures, manage students, and view attendance
- **Admin**: Full system access, user management, and system configuration

---

## API Endpoints

### 1. Register New User
**Endpoint**: `POST /api/auth/register`

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "password123",
  "full_name": "John Doe",
  "role": "student"
}
```

**Response (Success - 201)**:
```json
{
  "message": "User registered successfully",
  "user": {
    "id": "507f1f77bcf86cd799439011",
    "email": "user@example.com",
    "full_name": "John Doe",
    "role": "student"
  }
}
```

**Response (Error - 400)**:
```json
{
  "error": "User with this email already exists"
}
```

---

### 2. Login User
**Endpoint**: `POST /api/auth/login`

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response (Success - 200)**:
```json
{
  "message": "Login successful",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "507f1f77bcf86cd799439011",
    "email": "user@example.com",
    "full_name": "John Doe",
    "role": "student"
  }
}
```

**Response (Error - 401)**:
```json
{
  "error": "Invalid email or password"
}
```

---

### 3. Get Current User
**Endpoint**: `GET /api/auth/me`

**Headers**:
```
Authorization: Bearer <access_token>
```

**Response (Success - 200)**:
```json
{
  "id": "507f1f77bcf86cd799439011",
  "email": "user@example.com",
  "full_name": "John Doe",
  "role": "student"
}
```

**Response (Error - 401)**:
```json
{
  "error": "Unauthorized - Invalid or missing token"
}
```

---

### 4. Logout User
**Endpoint**: `POST /api/auth/logout`

**Headers**:
```
Authorization: Bearer <access_token>
```

**Response (Success - 200)**:
```json
{
  "message": "Logout successful"
}
```

---

## Using the Frontend

### 1. Login Page
**URL**: `http://localhost:5000/login.html`

- Switch between "Login" and "Sign Up" tabs
- Enter credentials and submit
- On successful login, token is saved to localStorage and user is redirected to dashboard

### 2. Dashboard Page
**URL**: `http://localhost:5000/dashboard.html`

- Displays logged-in user information
- Shows role-based quick actions
- Requires valid JWT token (redirects to login if missing)
- Can logout from the navbar

---

## Using JWT Tokens in API Calls

### JavaScript Example
```javascript
const token = localStorage.getItem('access_token');

const response = await fetch('http://localhost:5000/api/student/all', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  }
});
```

### cURL Example
```bash
curl -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  http://localhost:5000/api/student/all
```

---

## Protecting Routes with Decorators

### In Your Controllers

Use the authentication decorators from `utils/auth_middleware.py`:

#### 1. Require Any Authenticated User
```python
from utils.auth_middleware import authenticated_required

@app.route('/api/student/all', methods=['GET'])
@authenticated_required
def get_students():
    return get_all_students()
```

#### 2. Specific Role Required
```python
from utils.auth_middleware import admin_only, teacher_or_admin

@app.route('/api/admin/users', methods=['GET'])
@admin_only
def get_all_users():
    # Only admins can access
    ...

@app.route('/api/teacher/lectures', methods=['GET'])
@teacher_or_admin
def get_lectures():
    # Teachers and admins can access
    ...
```

#### 3. Multiple Roles
```python
from utils.auth_middleware import require_role

@app.route('/api/attendance/report', methods=['GET'])
@require_role('admin', 'teacher')
def get_attendance_report():
    # Admins and teachers can access
    ...
```

---

## Updating Existing Routes

To add authentication to your existing endpoints, follow this pattern:

### Before
```python
@student_bp.route("/all", methods=["GET"])
def get_students():
    return get_all_students()
```

### After
```python
from utils.auth_middleware import teacher_or_admin

@student_bp.route("/all", methods=["GET"])
@teacher_or_admin
def get_students():
    return get_all_students()
```

---

## Environment Configuration

### Required Environment Variables

Create a `.env` file in your project root:

```
MONGO_URI=mongodb://localhost:27017/face_attendance
SECRET_KEY=your-super-secret-key-change-this-in-production
```

### Important
- **SECRET_KEY** is used for JWT token signing
- In production, use a strong, randomly generated secret key
- Never commit `.env` to version control

---

## Database Schema

### Users Collection
```json
{
  "_id": ObjectId,
  "email": "user@example.com",
  "password_hash": "bcrypt_hashed_password",
  "full_name": "John Doe",
  "role": "student",
  "is_active": true,
  "created_at": ISODate,
  "last_login": ISODate
}
```

---

## JWT Token Structure

The JWT token contains:
- **Header**: Algorithm (HS256) and token type
- **Payload**: 
  - `identity`: User ID
  - `email`: User email
  - `role`: User role
  - `full_name`: User full name
  - `exp`: Token expiration (24 hours)
- **Signature**: Signed with SECRET_KEY

---

## Error Handling

### Common Error Responses

| Status | Error | Cause |
|--------|-------|-------|
| 400 | Missing email/password | Incomplete login request |
| 401 | Invalid email or password | Wrong credentials |
| 401 | Unauthorized - Invalid or missing token | Missing/expired JWT |
| 403 | Insufficient permissions | User role not allowed |
| 500 | Server error | Backend issue |

---

## Testing the Authentication

### Using Thunder Client / Postman

1. **Register**
   ```
   POST http://localhost:5000/api/auth/register
   Content-Type: application/json

   {
     "email": "test@example.com",
     "password": "password123",
     "full_name": "Test User",
     "role": "student"
   }
   ```

2. **Login**
   ```
   POST http://localhost:5000/api/auth/login
   Content-Type: application/json

   {
     "email": "test@example.com",
     "password": "password123"
   }
   ```

3. **Use Token**
   ```
   GET http://localhost:5000/api/auth/me
   Authorization: Bearer <token_from_login_response>
   ```

---

## Next Steps

1. Update your existing route controllers to use authentication decorators
2. Store the JWT token securely on the client (localStorage for now, consider httpOnly cookies in production)
3. Test all endpoints with the provided frontend
4. Deploy to production with a strong SECRET_KEY
5. Consider implementing token refresh for better security

---

## Security Best Practices

1. ✅ Passwords hashed with bcrypt (not stored in plain text)
2. ✅ JWT tokens expire after 24 hours
3. ✅ Role-based access control (RBAC)
4. ✅ CORS enabled only from your frontend
5. ⚠️ TODO: Implement token blacklisting for logout
6. ⚠️ TODO: Use HTTPS in production
7. ⚠️ TODO: Add rate limiting to login endpoint
8. ⚠️ TODO: Implement refresh tokens for better UX

---

## Troubleshooting

### "Token has expired"
- User needs to login again
- Token expires after 24 hours

### "Invalid token"
- Check if token is being sent correctly
- Format: `Authorization: Bearer <token>`

### "Insufficient permissions"
- User role doesn't have access to this endpoint
- Check the role decorator on the route

### Port Already in Use
- Flask default port is 5000
- Change in `app.run(port=5000)` to another port if needed
