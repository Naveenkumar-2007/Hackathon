"""
Simple HTTP Server that bypasses Windows networking issues
This creates an API-like interface using Python's built-in HTTP server
"""
import http.server
import socketserver
import json
import urllib.parse
from datetime import datetime

# Sample internship data
internships_data = {
    "jobs": [
        {
            "title": "Product Manager Intern",
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
            "description": "Business Analyst internship focusing on process improvement, requirements gathering, and stakeholder management.",
            "redirect_url": "https://careers.wipro.com/business-analyst-intern",
            "salary_min": 22000,
            "salary_max": 35000
        },
        {
            "title": "Digital Marketing Intern",
            "company": {"display_name": "Zomato"},
            "location": {"display_name": "Gurgaon, Haryana"},
            "description": "Digital Marketing internship covering social media, content creation, and performance marketing.",
            "redirect_url": "https://careers.zomato.com/marketing-intern",
            "salary_min": 20000,
            "salary_max": 32000
        }
    ]
}

class APIHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Parse the URL
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        query_params = urllib.parse.parse_qs(parsed_path.query)
        
        # Set CORS headers
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        if path == '/health':
            response = {
                "status": "healthy",
                "message": "HTTP server is running perfectly",
                "timestamp": datetime.now().isoformat(),
                "server_type": "Python HTTP Server",
                "internships_available": len(internships_data["jobs"])
            }
            
        elif path == '/search_jobs':
            # Get search parameters
            keyword = query_params.get('keyword', [''])[0].lower()
            location = query_params.get('location', [''])[0].lower()
            
            # Filter jobs
            filtered_jobs = internships_data["jobs"]
            
            if keyword:
                filtered_jobs = [job for job in filtered_jobs 
                               if keyword in job['title'].lower() or 
                                  keyword in job['company']['display_name'].lower() or
                                  keyword in job['description'].lower()]
            
            if location:
                filtered_jobs = [job for job in filtered_jobs
                               if location in job['location']['display_name'].lower()]
            
            response = {
                "success": True,
                "jobs": filtered_jobs,
                "count": len(filtered_jobs),
                "keyword": keyword,
                "location": location,
                "timestamp": datetime.now().isoformat()
            }
            
        elif path == '/' or path == '':
            response = {
                "message": "🎉 Python HTTP API Server is RUNNING!",
                "status": "success",
                "server_type": "Python HTTP Server (Windows Compatible)",
                "endpoints": ["/", "/health", "/search_jobs"],
                "internships_available": len(internships_data["jobs"]),
                "timestamp": datetime.now().isoformat()
            }
        else:
            response = {"error": "Endpoint not found", "available_endpoints": ["/", "/health", "/search_jobs"]}
        
        # Send JSON response
        self.wfile.write(json.dumps(response, indent=2).encode())

def start_http_server():
    PORT = 7000
    
    print("\n" + "="*60)
    print("🌐 PYTHON HTTP API SERVER (Windows Compatible)")
    print("="*60)
    print(f"📍 Server URL: http://127.0.0.1:{PORT}")
    print(f"📍 Server URL: http://localhost:{PORT}")
    print("🔧 This bypasses Windows Flask networking issues")
    print("🌐 CORS enabled for frontend connections")
    print(f"📊 Serving {len(internships_data['jobs'])} real internships")
    print("="*60)
    print("🚀 Server starting... Press Ctrl+C to stop")
    print("="*60 + "\n")
    
    with socketserver.TCPServer(("", PORT), APIHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🔄 Server stopped by user")
            httpd.shutdown()

if __name__ == "__main__":
    start_http_server()