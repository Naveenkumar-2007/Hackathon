"""
Minimal HTTP Server for API endpoints
"""
import http.server
import socketserver
import json

class SimpleAPIHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # Enable CORS
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        if self.path == '/health':
            response = {"status": "healthy", "message": "Server running"}
        elif '/search_jobs' in self.path:
            jobs = [
                {
                    "title": "Product Manager Intern",
                    "company": {"display_name": "Microsoft"},
                    "location": {"display_name": "Bangalore"},
                    "description": "Product management internship",
                    "salary_min": 35000,
                    "salary_max": 55000
                },
                {
                    "title": "Software Developer Intern",
                    "company": {"display_name": "Flipkart"},
                    "location": {"display_name": "Bangalore"},
                    "description": "Software development internship",
                    "salary_min": 30000,
                    "salary_max": 50000
                }
            ]
            response = {"success": True, "jobs": jobs, "count": len(jobs)}
        else:
            response = {"message": "API Server Running", "endpoints": ["/health", "/search_jobs"]}
        
        self.wfile.write(json.dumps(response).encode())

PORT = 7000
print(f"🚀 Starting Simple API Server on port {PORT}")
print(f"📍 URL: http://127.0.0.1:{PORT}")

with socketserver.TCPServer(("", PORT), SimpleAPIHandler) as httpd:
    httpd.serve_forever()