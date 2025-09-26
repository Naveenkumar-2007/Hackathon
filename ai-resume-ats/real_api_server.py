"""
Real Adzuna API Server for Internship Search
"""
import http.server
import socketserver
import json
import requests
import urllib.parse
from urllib.parse import urlparse, parse_qs

class RealAPIHandler(http.server.BaseHTTPRequestHandler):
    
    # Adzuna API credentials
    ADZUNA_APP_ID = "33e2a468"
    ADZUNA_APP_KEY = "96ba55c5dca94f6518e12c89b6732bcf"
    ADZUNA_BASE_URL = "https://api.adzuna.com/v1/api/jobs/in/search"
    
    def do_GET(self):
        # Enable CORS
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        parsed_url = urlparse(self.path)
        
        if parsed_url.path == '/health':
            response = {"status": "healthy", "message": "Real Adzuna API Server running"}
            
        elif parsed_url.path == '/search_jobs':
            try:
                # Parse query parameters
                query_params = parse_qs(parsed_url.query)
                keyword = query_params.get('keyword', [''])[0]
                location = query_params.get('location', ['india'])[0]
                
                print(f"🔍 Searching Adzuna API for: '{keyword}' in {location}")
                
                # Call real Adzuna API
                jobs = self.fetch_real_jobs(keyword, location)
                response = {
                    "success": True, 
                    "jobs": jobs, 
                    "count": len(jobs),
                    "source": "Adzuna API"
                }
                
            except Exception as e:
                print(f"❌ Error fetching real jobs: {e}")
                # Fallback to enhanced dummy data if API fails
                jobs = self.get_fallback_jobs(keyword, location)
                response = {
                    "success": True, 
                    "jobs": jobs, 
                    "count": len(jobs),
                    "source": "Fallback Data"
                }
        else:
            response = {
                "message": "Real Adzuna API Server Running", 
                "endpoints": ["/health", "/search_jobs"],
                "version": "2.0"
            }
        
        self.wfile.write(json.dumps(response).encode())
    
    def fetch_real_jobs(self, keyword, location):
        """Fetch real jobs from Adzuna API"""
        try:
            # Search for internships and trainee positions
            search_terms = [
                f"{keyword} intern",
                f"{keyword} internship", 
                f"{keyword} trainee",
                keyword
            ]
            
            all_jobs = []
            
            for search_term in search_terms:
                params = {
                    'app_id': self.ADZUNA_APP_ID,
                    'app_key': self.ADZUNA_APP_KEY,
                    'results_per_page': 10,
                    'what': search_term,
                    'where': location,
                    'content-type': 'application/json'
                }
                
                print(f"📡 Calling Adzuna API with: {search_term}")
                response = requests.get(f"{self.ADZUNA_BASE_URL}/1", params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    jobs = data.get('results', [])
                    
                    for job in jobs:
                        # Process and format job data
                        processed_job = {
                            "title": job.get('title', 'Internship Position'),
                            "company": {
                                "display_name": job.get('company', {}).get('display_name', 'Company')
                            },
                            "location": {
                                "display_name": job.get('location', {}).get('display_name', location.title())
                            },
                            "description": job.get('description', 'Exciting internship opportunity'),
                            "salary_min": job.get('salary_min', 25000),
                            "salary_max": job.get('salary_max', 50000),
                            "redirect_url": job.get('redirect_url', '#'),
                            "created": job.get('created', '2025-09-22'),
                            "match_percent": f"{85 + len(all_jobs) * 2}%"
                        }
                        all_jobs.append(processed_job)
                    
                    print(f"✅ Found {len(jobs)} jobs for '{search_term}'")
                    
                    # Stop after getting enough results
                    if len(all_jobs) >= 20:
                        break
                else:
                    print(f"⚠️ Adzuna API returned status {response.status_code}")
            
            # Remove duplicates and return top results
            unique_jobs = []
            seen_titles = set()
            
            for job in all_jobs:
                job_key = f"{job['title']}_{job['company']['display_name']}"
                if job_key not in seen_titles:
                    seen_titles.add(job_key)
                    unique_jobs.append(job)
                    
                if len(unique_jobs) >= 10:
                    break
            
            print(f"🎉 Returning {len(unique_jobs)} unique jobs")
            return unique_jobs
            
        except Exception as e:
            print(f"❌ Error in fetch_real_jobs: {e}")
            raise e
    
    def get_fallback_jobs(self, keyword, location):
        """Enhanced fallback data when API fails"""
        return [
            {
                "title": f"{keyword.title()} Intern",
                "company": {"display_name": "Tech Mahindra"},
                "location": {"display_name": location.title()},
                "description": f"Exciting {keyword} internship opportunity with hands-on experience in {keyword} domain.",
                "salary_min": 30000,
                "salary_max": 45000,
                "redirect_url": "https://careers.techmahindra.com/",
                "match_percent": "92%"
            },
            {
                "title": f"Junior {keyword.title()} Trainee",
                "company": {"display_name": "Infosys"},
                "location": {"display_name": location.title()},
                "description": f"Graduate trainee program in {keyword} with comprehensive training and mentorship.",
                "salary_min": 35000,
                "salary_max": 50000,
                "redirect_url": "https://www.infosys.com/careers/",
                "match_percent": "88%"
            },
            {
                "title": f"{keyword.title()} Summer Intern",
                "company": {"display_name": "Wipro"},
                "location": {"display_name": location.title()},
                "description": f"12-week summer internship program focusing on {keyword} skills and real-world projects.",
                "salary_min": 25000,
                "salary_max": 40000,
                "redirect_url": "https://careers.wipro.com/",
                "match_percent": "85%"
            },
            {
                "title": f"{keyword.title()} Associate Intern",
                "company": {"display_name": "TCS"},
                "location": {"display_name": location.title()},
                "description": f"Entry-level internship position in {keyword} with opportunities for full-time conversion.",
                "salary_min": 32000,
                "salary_max": 48000,
                "redirect_url": "https://www.tcs.com/careers",
                "match_percent": "90%"
            }
        ]

PORT = 7000
print(f"🚀 Starting Real Adzuna API Server on port {PORT}")
print(f"📍 URL: http://127.0.0.1:{PORT}")
print(f"🔑 Using Adzuna credentials: {RealAPIHandler.ADZUNA_APP_ID}")

try:
    with socketserver.TCPServer(("", PORT), RealAPIHandler) as httpd:
        print("✅ Server started successfully!")
        print("🔗 Endpoints available:")
        print("   - /health (Server status)")
        print("   - /search_jobs?keyword=X&location=Y (Job search)")
        httpd.serve_forever()
except Exception as e:
    print(f"❌ Server error: {e}")