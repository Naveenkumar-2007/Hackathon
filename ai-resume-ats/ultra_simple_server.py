"""
ULTRA SIMPLE FLASK SERVER - GUARANTEED TO WORK
This is the most basic Flask server possible
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# Sample internship data
internships = [
    {
        "title": "Product Manager Intern",
        "company": {"display_name": "Microsoft"},
        "location": {"display_name": "Bangalore, India"},
        "description": "Exciting product management internship opportunity",
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
    }
]

@app.route('/')
def home():
    return jsonify({
        "message": "🎉 Flask API Server is RUNNING!",
        "status": "success",
        "server": "http://127.0.0.1:8000",
        "endpoints": ["/", "/health", "/search_jobs"]
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "message": "Server is running perfectly"
    })

@app.route('/search_jobs')
def search_jobs():
    keyword = request.args.get('keyword', '')
    location = request.args.get('location', '')
    
    # Simple filtering
    filtered_jobs = internships
    if keyword:
        filtered_jobs = [job for job in internships 
                        if keyword.lower() in job['title'].lower() or 
                           keyword.lower() in job['company']['display_name'].lower()]
    
    return jsonify({
        "success": True,
        "jobs": filtered_jobs,
        "count": len(filtered_jobs),
        "keyword": keyword,
        "location": location
    })

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 ULTRA SIMPLE FLASK SERVER STARTING...")
    print(f"📍 URL: http://127.0.0.1:8000")
    print(f"📍 URL: http://localhost:8000") 
    print("🌐 Server is ready!")
    print("="*50 + "\n")
    
    app.run(host='127.0.0.1', port=8000, debug=False)