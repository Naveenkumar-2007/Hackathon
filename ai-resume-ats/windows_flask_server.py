"""
Windows-Compatible Flask Server
This version is specifically configured to work with Windows networking issues
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import socket
import threading
import time
import sys

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "http://localhost:3001", "http://127.0.0.1:3000", "http://127.0.0.1:3001"])

# Sample internship data
internships = [
    {
        "title": "Product Manager Intern",
        "company": {"display_name": "Microsoft"},
        "location": {"display_name": "Bangalore, India"},
        "description": "Exciting product management internship opportunity at Microsoft",
        "salary_min": 35000,
        "salary_max": 55000,
        "redirect_url": "https://careers.microsoft.com"
    },
    {
        "title": "Software Developer Intern", 
        "company": {"display_name": "Flipkart"},
        "location": {"display_name": "Bangalore, India"},
        "description": "Software development internship with cutting-edge technologies",
        "salary_min": 30000,
        "salary_max": 50000,
        "redirect_url": "https://careers.flipkart.com"
    },
    {
        "title": "Data Analyst Intern",
        "company": {"display_name": "Razorpay"}, 
        "location": {"display_name": "Bangalore, India"},
        "description": "Data analysis and business intelligence internship",
        "salary_min": 28000,
        "salary_max": 45000,
        "redirect_url": "https://careers.razorpay.com"
    },
    {
        "title": "Business Analyst Intern",
        "company": {"display_name": "Wipro"},
        "location": {"display_name": "Pune, Maharashtra"},
        "description": "Business process analysis and improvement internship",
        "salary_min": 22000,
        "salary_max": 35000,
        "redirect_url": "https://careers.wipro.com"
    },
    {
        "title": "Digital Marketing Intern",
        "company": {"display_name": "Zomato"},
        "location": {"display_name": "Gurgaon, Haryana"},
        "description": "Digital marketing and social media internship",
        "salary_min": 20000,
        "salary_max": 32000,
        "redirect_url": "https://careers.zomato.com"
    }
]

def check_port_available(port):
    """Check if port is available"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('127.0.0.1', port))
        sock.close()
        return result != 0
    except:
        return False

def find_available_port(start_port=9000):
    """Find an available port starting from start_port"""
    for port in range(start_port, start_port + 100):
        if check_port_available(port):
            return port
    return None

@app.route('/')
def home():
    return jsonify({
        "message": "🎉 Windows-Compatible Flask API Server is RUNNING!",
        "status": "success",
        "server_info": {
            "host": "127.0.0.1",
            "port": "Dynamic",
            "platform": "Windows"
        },
        "endpoints": ["/", "/health", "/search_jobs"],
        "internships_available": len(internships)
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "message": "Windows-compatible server is running perfectly",
        "platform": "Windows",
        "internships_count": len(internships)
    })

@app.route('/search_jobs')
def search_jobs():
    keyword = request.args.get('keyword', '').lower()
    location = request.args.get('location', '').lower()
    
    print(f"🔍 Search request: keyword='{keyword}', location='{location}'")
    
    # Filter internships based on search criteria
    filtered_jobs = internships
    
    if keyword:
        filtered_jobs = [job for job in internships 
                        if keyword in job['title'].lower() or 
                           keyword in job['company']['display_name'].lower() or
                           keyword in job['description'].lower()]
    
    if location and filtered_jobs:
        filtered_jobs = [job for job in filtered_jobs
                        if location in job['location']['display_name'].lower()]
    
    print(f"✅ Returning {len(filtered_jobs)} jobs")
    
    return jsonify({
        "success": True,
        "jobs": filtered_jobs,
        "count": len(filtered_jobs),
        "keyword": keyword,
        "location": location,
        "message": f"Found {len(filtered_jobs)} internship opportunities"
    })

def start_server_safe():
    """Start server with Windows-compatible settings"""
    print("\n" + "="*60)
    print("🖥️  WINDOWS-COMPATIBLE FLASK SERVER")
    print("="*60)
    
    # Find available port
    port = find_available_port(9000)
    if not port:
        print("❌ No available ports found. Trying default 9999...")
        port = 9999
    
    print(f"🔍 Using port: {port}")
    print(f"📍 Server URLs:")
    print(f"   - http://127.0.0.1:{port}")
    print(f"   - http://localhost:{port}")
    print("🔧 Windows networking optimizations enabled")
    print("🌐 CORS configured for frontend")
    print("="*60 + "\n")
    
    try:
        # Windows-specific Flask configuration
        app.run(
            host='127.0.0.1',  # Bind to localhost only (Windows-friendly)
            port=port,
            debug=False,
            threaded=True,
            use_reloader=False,  # Disable reloader (can cause Windows issues)
            processes=1  # Single process (Windows-compatible)
        )
    except Exception as e:
        print(f"❌ Server start failed: {e}")
        print("🔄 Trying alternative configuration...")
        
        try:
            # Alternative configuration
            app.run(
                host='0.0.0.0',
                port=port + 1,
                debug=False,
                threaded=False
            )
        except Exception as e2:
            print(f"❌ Alternative configuration failed: {e2}")
            print("💡 Try running as administrator or check Windows Defender")

if __name__ == '__main__':
    start_server_safe()