# Face Recognition Attendance System - Complete Web App

A modern Flask web application for face recognition-based attendance tracking with user authentication and role-based access control.

## Features

✅ **User Authentication**
- JWT-based authentication with 24-hour token expiration
- Bcrypt password hashing for security
- User registration and login
- Automatic session management

✅ **Role-Based Access Control**
- Student: Mark attendance, view personal records
- Teacher: Create lectures, manage students, view class attendance
- Admin: Full system access, user management, reports

✅ **Modern Web Interface**
- Beautiful, responsive login interface
- Personalized dashboard with role-based actions
- Seamless navigation between pages
- Loading states and error handling

✅ **Face Recognition**
- MTCNN face detection
- FaceNet embeddings for face matching
- Real-time attendance marking

## System Requirements

- Python 3.8+
- MongoDB (local or Atlas)
- Webcam (for face recognition features)

## Installation

### 1. Clone/Setup Project
```bash
cd Face-attendance-system
python -m venv venv
```

### 2. Activate Virtual Environment
**On Windows:**
```bash
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
Create a `.env` file in the project root (copy from `.env.example`):

```bash
cp .env.example .env
```

Then edit `.env` with your settings:
```env
MONGO_URI=mongodb://localhost:27017/face_attendance
SECRET_KEY=your-strong-random-secret-key-here
```

**🔐 Important**: Generate a strong SECRET_KEY for production:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 5. Start MongoDB (if local)
```bash
mongod
```

## Running the Application

### Start the Flask Server
```bash
python app.py
```

The application will be available at: **http://localhost:5000**

### User Navigation

1. **Landing Page** (`/`)
   - Auto-redirects to login if logged out
   - Auto-redirects to dashboard if logged in

2. **Login Page** (`/login`)
   - Login with existing account
   - Register new account
   - Choose role during registration (Student, Teacher, Admin)

3. **Dashboard** (`/dashboard`)
   - View user information
   - Role-based action menu
   - Quick access to features
   - Logout option

## API Endpoints

### Authentication (Public)
```
POST   /api/auth/register    - Create new user
POST   /api/auth/login       - Login and get JWT token
```

### Authentication (Protected)
```
GET    /api/auth/me          - Get current user info
POST   /api/auth/logout      - Logout user
```

### Protected Routes Example
```
GET    /api/student/all      - Get all students (requires teacher/admin)
POST   /api/student/register - Register new student
```

## Testing the Web App

### 1. Test Registration
1. Go to http://localhost:5000
2. Click "Sign up here"
3. Fill in details with role "admin"
4. Click "Sign Up"

### 2. Test Login
1. Click "Login here"
2. Enter registered credentials
3. System redirects to dashboard

### 3. Test Dashboard
1. View user information
2. See role-based quick actions
3. Click logout (top right)
4. Redirected to login page

## Testing with API Client (Postman/Thunder Client)

### Register User
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

### Login
```
POST http://localhost:5000/api/auth/login
Content-Type: application/json

{
  "email": "test@example.com",
  "password": "password123"
}
```

### Use Token
```
GET http://localhost:5000/api/auth/me
Authorization: Bearer <token_from_login>
```

## Project Structure

```
Face-attendance-system/
├── app.py                      # Main Flask app with web routes
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (create from .env.example)
├── .env.example                # Example environment file
├── AUTHENTICATION.md           # Auth system documentation
├── README.md                   # This file
│
├── controllers/                # Business logic
│   ├── auth_controller.py      # Authentication logic
│   ├── student_controller.py
│   ├── attendance_controller.py
│   └── lecture_controller.py
│
├── routes/                     # API endpoints
│   ├── auth_routes.py
│   ├── student_routes.py
│   ├── attendance_routes.py
│   └── lecture_routes.py
│
├── models/                     # Database models
│   ├── auth_model.py          # User model with auth methods
│   ├── student_model.py
│   └── attendance_model.py
│
├── database/                   # Database connection
│   └── db.py
│
├── templates/                  # Web pages (served by Flask)
│   ├── login.html             # Login & Registration page
│   └── dashboard.html         # User dashboard page
│
├── utils/                      # Utilities
│   └── auth_middleware.py     # JWT decorators for route protection
│
└── services/                   # Service layer
    └── face_service.py
```

## Protecting Your Routes

### Add Auth to Existing Routes

In any controller, use decorators from `utils/auth_middleware.py`:

```python
from utils.auth_middleware import admin_only, teacher_or_admin, authenticated_required

# Only admins
@app.route("/api/admin/panel")
@admin_only
def admin_panel():
    ...

# Teachers and admins
@app.route("/api/reports")
@teacher_or_admin
def get_reports():
    ...

# Any authenticated user
@app.route("/api/my-profile")
@authenticated_required
def my_profile():
    ...
```

## Security Features

✅ Passwords hashed with bcrypt (not stored plain text)
✅ JWT tokens with 24-hour expiration
✅ Role-based access control (RBAC)
✅ CORS configured for API access
✅ SQL injection protection via MongoDB
✅ CSRF protection ready (add in production)

⚠️ TODO for Production:
- Implement token blacklisting for logout
- Use HTTPS only
- Add rate limiting to login endpoint
- Implement refresh tokens
- Add 2FA support
- CORS whitelist specific domains

## Troubleshooting

### Port Already in Use
```bash
# Change port in app.py
app.run(debug=True, port=5001)  # Change to different port
```

### MongoDB Connection Failed
```
Error: Connection refused
```
- Ensure MongoDB is running: `mongod`
- Check MONGO_URI in `.env` is correct
- For MongoDB Atlas: Use connection string from Atlas dashboard

### "Invalid Token" Error
- Token may have expired (24 hour limit)
- User needs to login again
- Check `Authorization: Bearer <token>` format

### ImportError for Modules
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Templates Not Found
- Ensure `templates/` folder exists
- Check `app.py` has `template_folder="templates"`
- Restart Flask server

## Environment Variables

| Variable | Required | Example |
|----------|----------|---------|
| MONGO_URI | Yes | `mongodb://localhost:27017/face_attendance` |
| SECRET_KEY | Yes | `your-64-char-random-string` |

## MongoDB Collections

The system automatically uses these collections:
- `users` - Registered users with auth
- `students` - Student records
- `teachers` - Teacher records
- `courses` - Course information
- `lectures` - Lecture sessions
- `attendance` - Attendance records

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source.

## Support

For issues or questions:
1. Check [AUTHENTICATION.md](AUTHENTICATION.md) for API details
2. Review error messages in browser console
3. Check Flask server logs for backend errors

---

**Happy attendance tracking! 🎓📸**