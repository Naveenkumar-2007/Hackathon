#!/usr/bin/env python3
"""
Simple Flask API Server - Guaranteed to work!
This is a simplified version that focuses on getting your API running quickly.
"""

import os
import sys
import json
import requests
from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Create Flask app
app = Flask(__name__)
CORS(app)

# API Configuration
ADZUNA_APP_ID = os.getenv('ADZUNA_APP_ID', '33e2a468')
ADZUNA_API_KEY = os.getenv('ADZUNA_API_KEY', '96ba55c5dca94f6518e12c89b6732bcf')

print("🚀 Starting Simple Flask API Server...")
print(f"📊 Using API ID: {ADZUNA_APP_ID}")
print(f"🔑 Using API Key: {ADZUNA_API_KEY[:8]}...")

# Static internship data as fallback
STATIC_INTERNSHIPS = [
    {
        "title": "Product Management Intern",
        "company": {"display_name": "Microsoft Corporation"},
        "location": {"display_name": "Hyderabad, Telangana"},
        "description": "Product Management internship at Microsoft focusing on user research, market analysis, and product strategy. Work directly with senior PMs on feature development and data-driven decision making.",
        "redirect_url": "https://careers.microsoft.com/product-intern",
        "salary_min": 35000,
        "salary_max": 55000
    },
    {
        "title": "Software Engineering Intern",
        "company": {"display_name": "Flipkart"},
        "location": {"display_name": "Bangalore, Karnataka"},
        "description": "Software Engineering internship focusing on full-stack development, system design, and scalable solutions. Work on real products used by millions of users.",
        "redirect_url": "https://careers.flipkart.com/software-intern",
        "salary_min": 30000,
        "salary_max": 50000
    },
    {
        "title": "Data Analyst Intern",
        "company": {"display_name": "Razorpay"},
        "location": {"display_name": "Bangalore, Karnataka"},
        "description": "Data Analyst internship involving business intelligence, data visualization, and insights generation. Work with large datasets and modern analytics tools.",
        "redirect_url": "https://careers.razorpay.com/data-intern",
        "salary_min": 28000,
        "salary_max": 45000
    },
    {
        "title": "Business Analyst Intern",
        "company": {"display_name": "Wipro"},
        "location": {"display_name": "Pune, Maharashtra"},
        "description": "Business Analyst internship focusing on process improvement, requirements gathering, and stakeholder management. Gain exposure to consulting methodologies.",
        "redirect_url": "https://careers.wipro.com/business-analyst-intern",
        "salary_min": 22000,
        "salary_max": 35000
    },
    {
        "title": "Digital Marketing Intern",
        "company": {"display_name": "Zomato"},
        "location": {"display_name": "Gurgaon, Haryana"},
        "description": "Digital Marketing internship covering social media, content creation, and performance marketing. Work on campaigns reaching millions of users.",
        "redirect_url": "https://careers.zomato.com/marketing-intern",
        "salary_min": 20000,
        "salary_max": 32000
    }
]

def fetch_adzuna_internships(keyword="internship", location="india"):
    """Fetch internships from Adzuna API"""
    try:
        url = "https://api.adzuna.com/v1/api/jobs/in/search/1"
        params = {
            'app_id': ADZUNA_APP_ID,
            'app_key': ADZUNA_API_KEY,
            'what': keyword,
            'where': location,
            'results_per_page': 20,
            'content-type': 'application/json'
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            jobs = data.get('results', [])
            print(f"✅ Fetched {len(jobs)} jobs from Adzuna API")
            return jobs
        else:
            print(f"❌ Adzuna API error: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Error fetching from Adzuna: {e}")
        return []

@app.route('/')
def home():
    """Simple home page to test server"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🚀 Flask API Server - RUNNING!</title>
        <style>
            body { font-family: Arial; padding: 20px; background: #f0f8ff; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .status { background: #d4edda; color: #155724; padding: 15px; border-radius: 5px; margin: 20px 0; }
            .endpoint { background: #f8f9fa; padding: 10px; margin: 10px 0; border-left: 4px solid #007bff; }
            h1 { color: #333; }
            .success { color: #28a745; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎉 Flask API Server is RUNNING!</h1>
            
            <div class="status">
                <strong>✅ Status:</strong> Server is healthy and ready!<br>
                <strong>🔑 API ID:</strong> {{ api_id }}<br>
                <strong>📍 Server:</strong> http://127.0.0.1:5000<br>
                <strong>⏰ Time:</strong> Server started successfully
            </div>
            
            <h2>🔗 Available Endpoints:</h2>
            <div class="endpoint">
                <strong>GET /search_jobs</strong><br>
                Parameters: keyword, location<br>
                Example: <a href="/search_jobs?keyword=product&location=india">/search_jobs?keyword=product&location=india</a>
            </div>
            
            <div class="endpoint">
                <strong>GET /health</strong><br>
                Health check endpoint<br>
                Example: <a href="/health">/health</a>
            </div>
            
            <h2 class="success">🎯 Your API is ready to use!</h2>
            <p>Your frontend can now connect to fetch real internship data.</p>
        </div>
    </body>
    </html>
    """
    return render_template_string(html, api_id=ADZUNA_APP_ID)

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "Flask API server is running",
        "api_configured": bool(ADZUNA_APP_ID and ADZUNA_API_KEY),
        "endpoints": ["/", "/health", "/search_jobs"]
    })

@app.route('/search_jobs')
def search_jobs():
    """Search for internships"""
    keyword = request.args.get('keyword', 'internship')
    location = request.args.get('location', 'india')
    
    print(f"🔍 Searching jobs: keyword='{keyword}', location='{location}'")
    
    # Try to fetch from Adzuna API first
    api_jobs = fetch_adzuna_internships(keyword, location)
    
    # If API fails or returns few results, use static data
    if len(api_jobs) < 3:
        print("📋 Using static internship data as fallback")
        
        # Filter static data based on search terms
        filtered_jobs = []
        for job in STATIC_INTERNSHIPS:
            if (keyword.lower() in job['title'].lower() or 
                keyword.lower() in job['company']['display_name'].lower() or
                keyword.lower() in job['description'].lower()):
                filtered_jobs.append(job)
        
        # If no matches, return all static jobs
        jobs = filtered_jobs if filtered_jobs else STATIC_INTERNSHIPS
        source = "static_data"
    else:
        jobs = api_jobs
        source = "adzuna_api"
    
    print(f"✅ Returning {len(jobs)} jobs from {source}")
    
    return jsonify({
        "success": True,
        "jobs": jobs,
        "count": len(jobs),
        "source": source,
        "keyword": keyword,
        "location": location
    })

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 STARTING FLASK SERVER")
    print("="*50)
    print(f"📍 Server URL: http://127.0.0.1:5000")
    print(f"📍 Server URL: http://localhost:5000")
    print("🌐 Open the URL above to test your server!")
    print("🔄 Press Ctrl+C to stop the server")
    print("="*50 + "\n")
    
    # Run the server
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        threaded=True
    )