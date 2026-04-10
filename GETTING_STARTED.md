# Getting Started - Face Attendance System

## 🚀 Quick Start (5 minutes)

### Prerequisites
- Python 3.8+ installed
- MongoDB running locally or MongoDB Atlas account
- Command line/Terminal access

### Step 1: Install Dependencies
```bash
# Active your virtual environment first
python -m venv venv
venv\Scripts\activate          # Windows
# or
source venv/bin/activate       # macOS/Linux

# Install packages
pip install -r requirements.txt
```

### Step 2: Setup Environment
```bash
# Copy example env file
cp .env.example .env           # macOS/Linux
# or manually copy .env.example to .env on Windows

# Edit .env file with your MongoDB URI
# MONGO_URI=mongodb://localhost:27017/face_attendance
# SECRET_KEY=generate-a-random-string
```

### Step 3: Run Application
```bash
python app.py
```

### Step 4: Access Web App
Open browser: **http://localhost:5000**

---

## 🔑 Creating Your First User

1. **Go to Login Page** - http://localhost:5000
2. **Click "Sign up here"** 
3. **Register with:**
   - Email: `admin@example.com`
   - Password: `password123`
   - Full Name: `Admin User`
   - Role: `admin`
4. **Click "Sign Up"**
5. **Login with same credentials**
6. **View Dashboard** with admin features

---

## 📍 What Each Page Does

### `/` (Home)
- **Auto-redirects** to `/login` if not logged in
- **Auto-redirects** to `/dashboard` if logged in

### `/login`
- Register new users
- Login with email/password
- Beautiful, responsive UI
- Form validation
- Auto-redirect to dashboard on success

### `/dashboard`
- Show logged-in user details
- Display role-based quick actions
- "Quick Actions" menu (Student/Teacher/Admin)
- Logout button

---

## 🔐 Understanding Roles

### 👤 Student
Can:
- Mark attendance using face recognition
- View personal attendance records
- Access limited features

Resources:
```
POST   /api/student/register       - Register as student
GET    /api/student/all            - View student list (requires admin/teacher)
```

### 👨‍🏫 Teacher
Can:
- Create lecture sessions
- Manage student roster
- View class attendance
- Record attendance manually

Resources:
```
POST   /api/lecture/create         - Create new lecture
GET    /api/attendance/class       - Get class attendance
POST   /api/attendance/record      - Record attendance
```

### 👨‍💼 Admin
Can:
- Manage all users
- Create/delete accounts
- View system reports
- Configure settings
- Access audit logs

Resources:
```
GET    /api/admin/users            - List all users
POST   /api/admin/users            - Create user
DELETE /api/admin/users/{id}       - Delete user
```

---

## 🧪 Testing the System

### Test 1: User Registration Flow
```
1. Go to http://localhost:5000
2. Click "Sign up here"
3. Fill form:
   Email: test@sample.com
   Password: test1234
   Name: Test User
   Role: student
4. Click "Sign Up"
5. Should see success message
```

### Test 2: Login Flow
```
1. Click "Login here"
2. Enter credentials:
   Email: test@sample.com
   Password: test1234
3. Click "Login"
4. Redirects to dashboard
5. See user info & student actions
```

### Test 3: Role-Based Dashboard
Create 3 users with different roles and check:
- Student sees "Mark Attendance" action
- Teacher sees "Create Lecture" action
- Admin sees "Manage Users" action

### Test 4: Logout Flow
```
1. Dashboard page
2. Click "Logout" in top-right
3. Confirm logout
4. Redirects to login page
5. Token removed from browser storage
```

---

## 🛠️ API Testing (Advanced)

### Using cURL

**Register:**
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email":"api@test.com",
    "password":"pass1234",
    "full_name":"API Test",
    "role":"student"
  }'
```

**Login:**
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email":"api@test.com",
    "password":"pass1234"
  }'
```

Response includes `access_token`:
```json
{
  "message": "Login successful",
  "access_token": "eyJhbGc...",
  "user": {...}
}
```

**Use Token:**
```bash
curl -X GET http://localhost:5000/api/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Using Postman/Thunder Client

1. **POST** `http://localhost:5000/api/auth/register`
   - Header: `Content-Type: application/json`
   - Body (JSON):
     ```json
     {
       "email": "postman@test.com",
       "password": "password123",
       "full_name": "Postman User",
       "role": "admin"
     }
     ```

2. **POST** `http://localhost:5000/api/auth/login`
   - Same headers and format
   - Copy the `access_token` from response

3. **GET** `http://localhost:5000/api/auth/me`
   - Header: `Authorization: Bearer <paste_token_here>`
   - See current user info

---

## 📂 Project Structure Overview

```
app.py
├─ Main Flask app with web routes
├─ Serves login.html, dashboard.html
├─ Provides /api/auth endpoints
└─ Handles JWT configuration

templates/
├─ login.html      ← Login & registration UI
└─ dashboard.html  ← User dashboard UI

models/
├─ auth_model.py   ← User database operations
└─ Other models...

controllers/
├─ auth_controller.py ← Authentication logic
└─ Other controllers...

routes/
├─ auth_routes.py  ← /api/auth endpoints
└─ Other routes...

utils/
└─ auth_middleware.py ← JWT decorators

database/
└─ db.py          ← MongoDB connection
```

---

## ❌ Troubleshooting

### Problem: "Address already in use"
**Solution:** Port 5000 is occupied
```bash
# Use different port
# Edit app.py, change: app.run(debug=True, port=5001)
```

### Problem: "Cannot connect to MongoDB"
**Solution:** MongoDB not running
```bash
# Start MongoDB locally
mongod

# Or configure MongoDB Atlas
# Update MONGO_URI in .env with Atlas connection string
```

### Problem: "ModuleNotFoundError"
**Solution:** Dependencies not installed
```bash
pip install -r requirements.txt
```

### Problem: "Template not found"
**Solution:** Missing templates folder
```bash
# Ensure templates/ folder exists with login.html & dashboard.html
# Restart Flask app
```

### Problem: "CORS error" in browser console
**Solution:** Usually just browser security, not real issue
- CORS is configured for `/api/*` endpoints
- Web pages are served from same origin

---

## 🔐 Security Notes

✅ **What's Protected:**
- Passwords hashed with bcrypt
- Tokens expire after 24 hours
- Role-based access control
- CORS configured

⚠️ **For Production:**
- Change SECRET_KEY to strong random value
  ```bash
  python -c "import secrets; print(secrets.token_hex(32))"
  ```
- Use HTTPS only
- Configure CORS to specific domains
- Add rate limiting
- Implement refresh tokens
- Set up audit logging

---

## 📚 Next Steps

1. **Customize Dashboard**
   - Edit `templates/dashboard.html`
   - Add more quick actions
   - Integrate attendance marking UI

2. **Implement Features**
   - Add face recognition in attendance marking
   - Create admin user management panel
   - Build attendance reports

3. **Deploy**
   - Move to production server
   - Configure environment variables
   - Set up SSL/HTTPS
   - Setup database backups

---

## 📖 Documentation

- **[README.md](README.md)** - Full project documentation
- **[AUTHENTICATION.md](AUTHENTICATION.md)** - Complete API reference
- **Flask Docs** - https://flask.palletsprojects.com/
- **PyJWT Docs** - https://pyjwt.readthedocs.io/

---

## 💡 Tips

- Keep browser console open (F12) to see any errors
- Check Flask terminal for server-side errors
- localStorage stores JWT token (visible in DevTools → Application)
- Clear localStorage if having auth issues: localStorage.clear()
- Use `http://localhost:5000/api` to see API info

---

**Need help? Check the error messages - they usually explain what's wrong!** 

🎯 Happy coding! 

