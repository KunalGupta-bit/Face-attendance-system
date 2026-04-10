#!/usr/bin/env python
"""
Quick setup script for Face Attendance System
Initializes the application for first-time use
"""

import os
import sys
from pathlib import Path

def check_python_version():
    """Ensure Python 3.8+"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]}")

def check_env_file():
    """Create .env if it doesn't exist"""
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            with open('.env.example', 'r') as f:
                content = f.read()
            with open('.env', 'w') as f:
                f.write(content)
            print("✅ Created .env from .env.example")
            print("   ⚠️  Please update MONGO_URI and SECRET_KEY in .env")
        else:
            print("❌ .env.example not found")
    else:
        print("✅ .env exists")

def check_venv():
    """Check if virtual environment is activated"""
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    if not in_venv:
        print("⚠️  Virtual environment not activated")
        print("   Run: venv\\Scripts\\activate (Windows)")
        print("   Or:  source venv/bin/activate (macOS/Linux)")
    else:
        print("✅ Virtual environment activated")

def check_requirements():
    """Check if requirements are installed"""
    try:
        import flask
        import pymongo
        import flask_jwt_extended
        import bcrypt
        print("✅ Dependencies installed")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("   Run: pip install -r requirements.txt")

def check_directories():
    """Ensure all required directories exist"""
    dirs = [
        'templates',
        'controllers',
        'routes',
        'models',
        'database',
        'utils',
        'services'
    ]
    
    for d in dirs:
        if os.path.exists(d):
            print(f"✅ {d}/ exists")
        else:
            print(f"❌ {d}/ missing")

def check_mongodb():
    """Check MongoDB connection"""
    try:
        from pymongo import MongoClient
        from config import Config
        
        if not Config.MONGO_URI:
            print("⚠️  MONGO_URI not configured in .env")
            return
        
        client = MongoClient(Config.MONGO_URI, serverSelectionTimeoutMS=2000)
        client.admin.command('ping')
        print("✅ MongoDB connected")
    except Exception as e:
        print(f"⚠️  MongoDB not connected: {e}")
        print("   Start MongoDB: mongod")
        print("   Or configure MongoDB Atlas URI")

def main():
    print("\n" + "="*50)
    print("Face Attendance System - Setup Check")
    print("="*50 + "\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("Environment File", check_env_file),
        ("Virtual Environment", check_venv),
        ("Dependencies", check_requirements),
        ("Directories", check_directories),
        ("MongoDB", check_mongodb),
    ]
    
    for name, check_func in checks:
        print(f"\n🔍 Checking {name}...")
        try:
            check_func()
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "="*50)
    print("Setup check complete!")
    print("="*50)
    print("\n📝 Next steps:")
    print("   1. Update .env with MONGO_URI and SECRET_KEY")
    print("   2. Start MongoDB (if local)")
    print("   3. Run: python app.py")
    print("   4. Open: http://localhost:5000")
    print("\n")

if __name__ == "__main__":
    main()
