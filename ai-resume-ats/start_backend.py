#!/usr/bin/env python3
"""
Simple backend starter script to test Flask app
"""

import os
import sys

# Change to the correct directory
backend_dir = r"C:\Users\navee\Cisco Packet Tracer 8.2.2\saves\certificates\genaihack\ai-resume-ats\backend"
os.chdir(backend_dir)

print(f"Starting Flask app from: {os.getcwd()}")

# Check if app.py exists
if not os.path.exists("app.py"):
    print("ERROR: app.py not found in current directory")
    sys.exit(1)

# Check if .env file exists
if not os.path.exists(".env"):
    print("WARNING: .env file not found. Copying from .env.example")
    import shutil
    shutil.copy(".env.example", ".env")

# Test imports
print("Testing imports...")
try:
    import flask
    import flask_cors
    import requests
    import sklearn
    import PyPDF2
    from docx import Document
    from dotenv import load_dotenv
    print("✅ All core modules imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

# Load and run the Flask app
print("Starting Flask server...")
try:
    exec(open("app.py").read())
except Exception as e:
    print(f"Error starting Flask app: {e}")
    import traceback
    traceback.print_exc()