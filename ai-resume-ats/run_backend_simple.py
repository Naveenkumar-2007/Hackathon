#!/usr/bin/env python3
"""
Simple Flask backend runner with better error handling
"""

import os
import sys
from pathlib import Path

# Ensure we're in the right directory
backend_dir = Path(__file__).parent / "backend"
if backend_dir.exists():
    os.chdir(backend_dir)
    sys.path.insert(0, str(backend_dir))

print(f"Starting Flask server from: {os.getcwd()}")

try:
    # Import and run the app
    from app import app
    print("✅ Flask app imported successfully")
    
    print("🚀 Starting Flask server on http://127.0.0.1:5000")
    print("📱 Frontend running on http://localhost:3001")
    print("Press Ctrl+C to stop")
    print("-" * 50)
    
    app.run(host='127.0.0.1', port=5000, debug=False, threaded=True)
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're in the correct directory and all dependencies are installed")
except Exception as e:
    print(f"❌ Error starting Flask server: {e}")
    import traceback
    traceback.print_exc()