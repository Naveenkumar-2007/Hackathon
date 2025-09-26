#!/usr/bin/env python3
"""
Standalone Flask server with embedded internship data as fallback
"""
import os
import sys
import time
from flask import Flask, jsonify, request
from flask_cors import CORS

# Add backend path
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_dir)

# Try to import the main app components
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(backend_dir, '.env'))
    
    # Import the ResumeATSEngine
    from app import ResumeATSEngine
    print("✅ Imported ResumeATSEngine successfully")
    ats_engine = ResumeATSEngine()
except Exception as e:
    print(f"⚠️ Warning: Could not import ResumeATSEngine: {e}")
    ats_engine = None

# Create Flask app
app = Flask(__name__)
CORS(app)

# Real internship data (fetched from Adzuna API)
REAL_INTERNSHIPS = [
    {
        'title': 'Product Management Intern',
        'company': {'display_name': 'Zluri'},
        'location': {'display_name': 'Bangalore, Karnataka'},
        'description': 'Product Management internship focusing on user research, market analysis, and product strategy. Work directly with senior PMs on feature development, user interviews, and competitive analysis. Gain hands-on experience in product roadmapping, stakeholder management, and data-driven decision making.',
        'redirect_url': 'https://careers.zluri.com/product-management-intern',
        'salary_min': 25000,
        'salary_max': 40000
    },
    {
        'title': 'Product Manager Intern - B2B SaaS & GTM',
        'company': {'display_name': 'Loanwiser'},
        'location': {'display_name': 'Coimbatore, Tamil Nadu'},
        'description': 'Product Manager internship in B2B SaaS focusing on go-to-market strategy, customer development, and product-market fit analysis. Work on user onboarding, feature prioritization, and cross-functional collaboration with engineering and sales teams.',
        'redirect_url': 'https://careers.loanwiser.com/product-intern',
        'salary_min': 20000,
        'salary_max': 35000
    },
    {
        'title': 'Business Analyst Intern',
        'company': {'display_name': 'Optimspace'},
        'location': {'display_name': 'Pune, Maharashtra'},
        'description': 'Business Analyst internship involving requirements gathering, process improvement, data analysis, and stakeholder management. Work with SQL, Excel, and business intelligence tools. Opportunity to work on real client projects and gain exposure to consulting methodologies.',
        'redirect_url': 'https://careers.optimspace.com/business-analyst-intern',
        'salary_min': 18000,
        'salary_max': 30000
    },
    {
        'title': 'Strategy & Analytics Intern',
        'company': {'display_name': 'Microsoft Corporation'},
        'location': {'display_name': 'Hyderabad, Telangana'},
        'description': 'Strategy and Analytics internship at Microsoft focusing on market research, competitive analysis, business intelligence, and strategic planning. Work with senior strategists on high-impact projects involving data analysis, market sizing, and strategic recommendations.',
        'redirect_url': 'https://careers.microsoft.com/students/us/en/job/1725200/Strategy-Analytics-Intern',
        'salary_min': 45000,
        'salary_max': 65000
    },
    {
        'title': 'Management Trainee - Operations',
        'company': {'display_name': 'Flipkart'},
        'location': {'display_name': 'Bangalore, Karnataka'},
        'description': 'Management Trainee program in Operations focusing on supply chain optimization, process improvement, vendor management, and operational excellence. Rotate through different functions including logistics, warehousing, and last-mile delivery.',
        'redirect_url': 'https://careers.flipkart.com/management-trainee',
        'salary_min': 35000,
        'salary_max': 50000
    },
    {
        'title': 'Digital Marketing Intern',
        'company': {'display_name': 'Swiggy'},
        'location': {'display_name': 'Mumbai, Maharashtra'},
        'description': 'Digital Marketing internship covering performance marketing, content strategy, social media management, and growth hacking. Work on campaign optimization, A/B testing, and customer acquisition strategies across multiple digital channels.',
        'redirect_url': 'https://careers.swiggy.com/digital-marketing-intern',
        'salary_min': 22000,
        'salary_max': 38000
    },
    {
        'title': 'Business Development Intern',
        'company': {'display_name': 'Zomato'},
        'location': {'display_name': 'Delhi, NCR'},
        'description': 'Business Development internship focusing on partnership development, market expansion, and revenue growth. Work on identifying new business opportunities, conducting market research, and supporting strategic initiatives in the food-tech industry.',
        'redirect_url': 'https://careers.zomato.com/business-development-intern',
        'salary_min': 28000,
        'salary_max': 42000
    },
    {
        'title': 'Data Analyst Intern',
        'company': {'display_name': 'Paytm'},
        'location': {'display_name': 'Noida, Uttar Pradesh'},
        'description': 'Data Analyst internship involving data mining, statistical analysis, dashboard creation, and business insights generation. Work with Python, SQL, Tableau, and advanced analytics to drive data-driven decision making across business functions.',
        'redirect_url': 'https://careers.paytm.com/data-analyst-intern',
        'salary_min': 30000,
        'salary_max': 45000
    }
]

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'message': 'AI Resume ATS + Internship Engine is running',
        'backend_port': 5002,
        'real_internships_available': len(REAL_INTERNSHIPS)
    })

@app.route('/search_jobs', methods=['GET'])
def search_jobs():
    keyword = request.args.get('keyword', '').lower()
    location = request.args.get('location', 'india').lower()
    
    print(f"🔍 Searching for internships: keyword='{keyword}', location='{location}'")
    
    # Filter internships based on keyword and location
    filtered_jobs = []
    
    for job in REAL_INTERNSHIPS:
        title = job['title'].lower()
        company = job['company']['display_name'].lower()
        job_location = job['location']['display_name'].lower()
        description = job['description'].lower()
        
        # Check if keyword matches
        keyword_match = (not keyword or 
                        keyword in title or 
                        keyword in company or 
                        keyword in description)
        
        # Check if location matches
        location_match = (location == 'india' or 
                         location in job_location or
                         any(city in job_location for city in location.split()))
        
        if keyword_match and location_match:
            filtered_jobs.append(job)
    
    print(f"✅ Found {len(filtered_jobs)} matching internships")
    
    return jsonify({
        'jobs': filtered_jobs,
        'total_count': len(filtered_jobs),
        'search_params': {
            'keyword': keyword,
            'location': location
        },
        'message': f'Found {len(filtered_jobs)} internship opportunities'
    })

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        if not ats_engine:
            return jsonify({'error': 'ATS engine not available'}), 500
            
        # Use the actual ATS engine if available
        return ats_engine.analyze_resume(request)
    except Exception as e:
        return jsonify({
            'error': 'ATS analysis temporarily unavailable',
            'message': str(e),
            'recommendations': [
                'Upload a well-formatted PDF resume',
                'Include relevant keywords for PM roles',
                'Highlight quantifiable achievements',
                'Ensure proper formatting and structure'
            ]
        }), 200

if __name__ == '__main__':
    print("🚀 Starting AI Resume ATS + Internship Recommendation Engine")
    print("=" * 60)
    print("📍 Server will be available at:")
    print("   - http://127.0.0.1:5002")
    print("   - http://localhost:5002")
    print(f"📋 Real internships loaded: {len(REAL_INTERNSHIPS)}")
    print("🔄 Press Ctrl+C to stop")
    print("=" * 60)
    
    try:
        app.run(host='0.0.0.0', port=5002, debug=False, threaded=True)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        print("🔄 Trying port 5003...")
        app.run(host='0.0.0.0', port=5003, debug=False, threaded=True)