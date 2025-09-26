#!/usr/bin/env python3
"""
Minimal Flask server for testing
"""

from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'message': 'API is working!'})

@app.route('/test')
def test():
    return jsonify({'test': 'success', 'server': 'running'})

if __name__ == '__main__':
    print("🚀 Starting minimal Flask server for testing...")
    print("💡 Testing URLs:")
    print("   - http://127.0.0.1:5001/health")
    print("   - http://127.0.0.1:5001/test")
    
    try:
        app.run(host='127.0.0.1', port=5001, debug=False)
    except Exception as e:
        print(f"❌ Error: {e}")
        # Try a different port
        print("🔄 Trying port 5002...")
        app.run(host='127.0.0.1', port=5002, debug=False)