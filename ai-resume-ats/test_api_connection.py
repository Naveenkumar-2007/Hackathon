#!/usr/bin/env python3
"""
Simple test to verify API connectivity
"""

import time
import requests
import threading
from flask import Flask

def test_connection():
    """Test connection to Flask server"""
    print("🔄 Testing API connection...")
    
    # Wait for server to start
    time.sleep(3)
    
    try:
        # Test health endpoint
        response = requests.get("http://127.0.0.1:5000/health", timeout=5)
        print(f"✅ Health endpoint: {response.status_code}")
        
        # Test search endpoint
        response = requests.get(
            "http://127.0.0.1:5000/search_jobs",
            params={"keyword": "intern", "location": "india"},
            timeout=10
        )
        print(f"✅ Search endpoint: {response.status_code}")
        if response.status_code == 200:
            jobs = response.json().get('jobs', [])
            print(f"📋 Found {len(jobs)} internships")
            
    except Exception as e:
        print(f"❌ Connection failed: {e}")

if __name__ == "__main__":
    # Start connection test in background
    test_thread = threading.Thread(target=test_connection, daemon=True)
    test_thread.start()
    
    # Import and run Flask app
    try:
        import sys
        import os
        
        # Add backend to path
        backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
        sys.path.insert(0, backend_dir)
        os.chdir(backend_dir)
        
        from app import app
        print("🚀 Starting Flask server...")
        app.run(host='127.0.0.1', port=5000, debug=False, threaded=True)
        
    except Exception as e:
        print(f"❌ Flask error: {e}")
        import traceback
        traceback.print_exc()