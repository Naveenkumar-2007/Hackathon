import os
import re
import requests
import numpy as np
import time
from io import BytesIO
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
from docx import Document
# spacy import moved to inside try-catch below

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load spaCy model (download with: python -m spacy download en_core_web_sm)
try:
    import spacy
    nlp = spacy.load("en_core_web_sm")
    print("✅ spaCy model loaded successfully")
except Exception as e:
    print(f"Warning: spaCy issue ({e}). Using fallback NLP processing.")
    nlp = None

class ResumeATSEngine:
    def __init__(self):
        self.adzuna_app_id = os.getenv('ADZUNA_APP_ID')
        self.adzuna_app_key = os.getenv('ADZUNA_APP_KEY')
        self.adzuna_base_url = "https://api.adzuna.com/v1/api/jobs/in/search"
        
    def extract_text_from_pdf(self, file_content):
        """Extract text from PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(BytesIO(file_content))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            print(f"Error extracting PDF text: {e}")
            return ""
    
    def extract_text_from_docx(self, file_content):
        """Extract text from DOCX file"""
        try:
            doc = Document(BytesIO(file_content))
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        except Exception as e:
            print(f"Error extracting DOCX text: {e}")
            return ""
    
    def clean_text(self, text):
        """Clean and normalize text"""
        # Remove extra whitespace and special characters
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s]', ' ', text)
        return text.lower().strip()
    
    def extract_keywords(self, text):
        """Extract keywords using spaCy NLP"""
        if not nlp:
            # Fallback to simple keyword extraction
            words = text.lower().split()
            # Filter out common stop words
            stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should'}
            keywords = [word for word in words if len(word) > 2 and word not in stop_words]
            return list(set(keywords))
        
        doc = nlp(text)
        keywords = []
        
        # Extract nouns, proper nouns, and adjectives
        for token in doc:
            if (token.pos_ in ['NOUN', 'PROPN', 'ADJ'] and 
                not token.is_stop and 
                not token.is_punct and 
                len(token.text) > 2):
                keywords.append(token.lemma_.lower())
        
        # Extract named entities (skills, technologies, etc.)
        for ent in doc.ents:
            if ent.label_ in ['ORG', 'PRODUCT', 'GPE']:
                keywords.append(ent.text.lower())
        
        return list(set(keywords))
    
    def fetch_internships(self, location="india", keyword=""):
        """Fetch internships from Adzuna API with improved search"""
        try:
            if not self.adzuna_app_id or not self.adzuna_app_key:
                print("Warning: Adzuna API credentials not found, using dummy data")
                return self.get_dummy_jobs()
            
            print(f"Using Adzuna API credentials: ID={self.adzuna_app_id[:8]}...")
            
            # Try multiple search strategies to find internships
            search_strategies = [
                # Strategy 1: Direct internship search
                "internship",
                # Strategy 2: Graduate programs
                "graduate trainee",
                # Strategy 3: Entry level positions
                "entry level",
                # Strategy 4: Specific keyword + intern if provided
                f"{keyword} intern" if keyword else "intern"
            ]
            
            all_results = []
            
            for search_term in search_strategies:
                try:
                    params = {
                        'app_id': self.adzuna_app_id,
                        'app_key': self.adzuna_app_key,
                        'results_per_page': 20,
                        'what': search_term,
                        'where': location,
                        'sort_by': 'relevance'
                    }
                    
                    print(f"Searching Adzuna API with term: '{search_term}' in {location}")
                    response = requests.get(f"{self.adzuna_base_url}/1", params=params, timeout=20)
                    
                    print(f"API Response - Status: {response.status_code}")
                    
                    if response.status_code == 200:
                        data = response.json()
                        results = data.get('results', [])
                        print(f"Found {len(results)} results for '{search_term}'")
                        
                        # Add unique results
                        for job in results:
                            job_id = job.get('id', '')
                            if not any(existing.get('id') == job_id for existing in all_results):
                                all_results.append(job)
                        
                        # If we found some results, don't need to try all strategies
                        if len(all_results) >= 10:
                            break
                            
                    elif response.status_code == 429:
                        print("Rate limit hit, waiting...")
                        time.sleep(2)
                    else:
                        print(f"API error for '{search_term}': {response.status_code}")
                        print(f"Response text: {response.text[:200]}...")
                        
                except Exception as e:
                    print(f"Error with search term '{search_term}': {e}")
                    continue
            
            print(f"Total unique results found: {len(all_results)}")
            
            if all_results:
                # Filter and prioritize internship-related results
                internship_results = []
                internship_keywords = ['intern', 'internship', 'trainee', 'graduate', 'entry level', 'student', 'apprentice']
                
                for job in all_results:
                    title = job.get('title', '').lower()
                    description = job.get('description', '').lower()
                    company = job.get('company', {}).get('display_name', '').lower()
                    
                    # Score based on internship relevance
                    score = 0
                    for kw in internship_keywords:
                        if kw in title:
                            score += 3
                        elif kw in description[:300]:  # Check first part of description
                            score += 2
                        elif kw in company:
                            score += 1
                    
                    if score > 0:
                        job['_internship_score'] = score
                        internship_results.append(job)
                
                # Sort by internship relevance score
                internship_results = sorted(internship_results, key=lambda x: x.get('_internship_score', 0), reverse=True)
                
                print(f"Filtered to {len(internship_results)} internship-relevant results")
                
                if internship_results:
                    return internship_results[:15]  # Return top 15 results
                else:
                    print("No internship-relevant results found, returning all results")
                    return all_results[:15]
            else:
                print("No results from API, using dummy data")
                return self.get_dummy_jobs()
                
        except Exception as e:
            print(f"Error fetching internships from API: {e}")
            import traceback
            traceback.print_exc()
            return self.get_dummy_jobs()
    
    def get_dummy_jobs(self):
        """Fallback dummy internship data when API is unavailable"""
        return [
            {
                'title': 'Product Management Summer Intern',
                'company': {'display_name': 'TechCorp India'},
                'location': {'display_name': 'Bangalore, Karnataka'},
                'description': 'Product management summer internship focusing on user research, market analysis, roadmap planning, stakeholder communication, and product strategy. Experience with Agile, Scrum, JIRA, and analytics tools preferred. Duration: 3 months.',
                'redirect_url': 'https://careers.techcorp.com/internships/pm'
            },
            {
                'title': 'Business Analyst Intern - Graduate Program',
                'company': {'display_name': 'ConsultingXYZ'},
                'location': {'display_name': 'Mumbai, Maharashtra'},
                'description': 'Business analysis internship involving requirements gathering, process improvement, data analysis, stakeholder management, and documentation. Knowledge of SQL, Excel, and business intelligence tools required. Full-time conversion opportunity.',
                'redirect_url': 'https://careers.consultingxyz.com/graduate-program'
            },
            {
                'title': 'Digital Marketing Intern',
                'company': {'display_name': 'Digital Solutions Ltd'},
                'location': {'display_name': 'Delhi, NCR'},
                'description': 'Digital marketing internship covering market research, campaign planning, content strategy, social media management, and performance analytics. Experience with Google Analytics and marketing automation tools preferred. Stipend provided.',
                'redirect_url': 'https://careers.digitalsolutions.com/internships'
            },
            {
                'title': 'Operations Management Trainee',
                'company': {'display_name': 'LogisticsPro India'},
                'location': {'display_name': 'Pune, Maharashtra'},
                'description': 'Operations management trainee program focusing on process optimization, supply chain coordination, quality assurance, vendor management, and operational efficiency. Knowledge of Lean Six Sigma and project management methodologies preferred. 6-month program.',
                'redirect_url': 'https://careers.logisticspro.com/trainee-program'
            },
            {
                'title': 'Strategy & Analytics Intern',
                'company': {'display_name': 'DataTech Solutions'},
                'location': {'display_name': 'Hyderabad, Telangana'},
                'description': 'Strategy and analytics internship involving market research, data analysis, business intelligence, dashboard creation, and strategic planning. Experience with SQL, Python, Tableau, and analytical tools required. Remote work options available.',
                'redirect_url': 'https://careers.datatech.com/internships/strategy'
            },
            {
                'title': 'Product Development Intern',
                'company': {'display_name': 'InnovateCorp'},
                'location': {'display_name': 'Chennai, Tamil Nadu'},
                'description': 'Product development internship focusing on user experience design, product testing, market validation, competitive analysis, and product launch strategies. Experience with design thinking and customer research preferred. Mentorship provided.',
                'redirect_url': 'https://careers.innovatecorp.com/product-internship'
            },
            {
                'title': 'Management Consultant Intern',
                'company': {'display_name': 'Strategy Partners'},
                'location': {'display_name': 'Gurgaon, Haryana'},
                'description': 'Management consulting internship involving client engagement, business analysis, strategic recommendations, presentation development, and project management. Strong analytical and communication skills required. PPO opportunity available.',
                'redirect_url': 'https://careers.strategypartners.com/intern-program'
            },
            {
                'title': 'Growth & Strategy Intern',
                'company': {'display_name': 'StartupHub India'},
                'location': {'display_name': 'Bangalore, Karnataka'},
                'description': 'Growth and strategy internship in a fast-paced startup environment. Responsibilities include market expansion, growth hacking, partnership development, and strategic initiatives. Equity participation and flexible work arrangements available.',
                'redirect_url': 'https://careers.startuphub.com/growth-intern'
            }
        ]
    
    def calculate_ats_score(self, resume_text, job_descriptions):
        """Calculate ATS score using TF-IDF and cosine similarity"""
        if not job_descriptions:
            return 0, []
            
        # Combine all job descriptions
        combined_job_text = " ".join(job_descriptions)
        
        # Create TF-IDF vectors
        vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        
        try:
            tfidf_matrix = vectorizer.fit_transform([resume_text, combined_job_text])
            
            # Calculate cosine similarity
            similarity_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            # Convert to percentage (0-100)
            ats_score = min(100, max(0, similarity_score * 100))
            
            # Get feature names (keywords)
            feature_names = vectorizer.get_feature_names_out()
            
            # Get TF-IDF scores for job descriptions
            job_tfidf = tfidf_matrix[1].toarray()[0]
            resume_tfidf = tfidf_matrix[0].toarray()[0]
            
            # Find missing keywords (high in job descriptions, low/missing in resume)
            missing_keywords = []
            for i, score in enumerate(job_tfidf):
                if score > 0.1 and resume_tfidf[i] < 0.05:  # Thresholds for missing keywords
                    missing_keywords.append(feature_names[i])
            
            # Sort by importance and limit to top 10
            missing_keywords = sorted(missing_keywords)[:10]
            
            return round(ats_score, 1), missing_keywords
            
        except Exception as e:
            print(f"Error calculating ATS score: {e}")
            return 0, []
    
    def calculate_job_match(self, resume_text, job_description):
        """Calculate match percentage for individual job"""
        try:
            vectorizer = TfidfVectorizer(stop_words='english', max_features=500)
            tfidf_matrix = vectorizer.fit_transform([resume_text, job_description])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return min(100, max(0, similarity * 100))
        except:
            return 50  # Default match percentage
    
    def get_ats_status(self, score):
        """Get ATS status based on score"""
        if score >= 80:
            return "Excellent chance"
        elif score >= 60:
            return "Good chance"
        elif score >= 40:
            return "Fair chance"
        else:
            return "Low chance, add missing keywords"

# Initialize the ATS engine
ats_engine = ResumeATSEngine()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "AI Resume ATS API is running"})

@app.route('/recommend', methods=['POST'])
def recommend_internships():
    """Main endpoint for resume analysis and internship recommendations"""
    try:
        # Get form data and profile data
        skills = request.form.get('skills', '')
        education = request.form.get('education', '')
        location = request.form.get('location', 'india')
        
        # Get profile data if provided
        profile_data = request.form.get('profile_data', '{}')
        try:
            import json
            profile = json.loads(profile_data) if profile_data != '{}' else {}
        except:
            profile = {}
        
        # Merge profile data with form data
        if profile:
            skills = skills or ', '.join(profile.get('skills', []))
            education = education or profile.get('education', '')
            location = location or profile.get('location', 'india')
        
        # Get uploaded resume file
        resume_file = request.files.get('resume')
        
        if not resume_file:
            return jsonify({"error": "Resume file is required"}), 400
        
        # Extract text from resume
        file_content = resume_file.read()
        filename = resume_file.filename.lower()
        
        if filename.endswith('.pdf'):
            resume_text = ats_engine.extract_text_from_pdf(file_content)
        elif filename.endswith('.docx'):
            resume_text = ats_engine.extract_text_from_docx(file_content)
        else:
            return jsonify({"error": "Only PDF and DOCX files are supported"}), 400
        
        if not resume_text:
            return jsonify({"error": "Could not extract text from resume"}), 400
        
        # Clean and prepare candidate profile
        resume_text = ats_engine.clean_text(resume_text)
        # Combine available information (skills and education are optional)
        profile_parts = [part for part in [skills, education, resume_text] if part.strip()]
        candidate_profile = " ".join(profile_parts).strip()
        
        # Fetch internships with enhanced search using skills as keyword
        jobs = ats_engine.fetch_internships(location=location, keyword=skills)
        
        if not jobs:
            return jsonify({"error": "No internships found"}), 404
        
        # Prepare job descriptions for ATS scoring
        job_descriptions = []
        recommendations = []
        
        for job in jobs[:5]:  # Limit to top 5 jobs
            job_desc = job.get('description', '')
            job_descriptions.append(job_desc)
            
            # Calculate individual job match
            match_percentage = ats_engine.calculate_job_match(candidate_profile, job_desc)
            
            recommendation = {
                "title": job.get('title', 'N/A'),
                "company": job.get('company', {}).get('display_name', 'N/A'),
                "location": job.get('location', {}).get('display_name', 'N/A'),
                "match_percent": f"{round(match_percentage)}%",
                "apply_link": job.get('redirect_url', '#')
            }
            recommendations.append(recommendation)
        
        # Calculate overall ATS score
        ats_score, missing_keywords = ats_engine.calculate_ats_score(candidate_profile, job_descriptions)
        status = ats_engine.get_ats_status(ats_score)
        
        # Sort recommendations by match percentage
        recommendations.sort(key=lambda x: int(x['match_percent'].replace('%', '')), reverse=True)
        
        response = {
            "ats_score": ats_score,
            "status": status,
            "missing_keywords": missing_keywords,
            "recommendations": recommendations
        }
        
        return jsonify(response)
        
    except Exception as e:
        print(f"Error in recommend_internships: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/search_jobs', methods=['GET'])
def search_jobs():
    """Search jobs by keyword and location"""
    try:
        keyword = request.args.get('keyword', 'intern')
        location = request.args.get('location', 'india')
        
        # Use the improved internship fetching method
        jobs = ats_engine.fetch_internships(location=location, keyword=keyword)
        
        # Format jobs for response
        formatted_jobs = []
        for job in jobs[:10]:  # Limit to 10 results
            formatted_job = {
                "title": job.get('title', 'N/A'),
                "company": job.get('company', {}).get('display_name', 'N/A'),
                "location": job.get('location', {}).get('display_name', 'N/A'),
                "description": job.get('description', '')[:200] + '...' if len(job.get('description', '')) > 200 else job.get('description', ''),
                "apply_link": job.get('redirect_url', '#'),
                "match_percent": "85%"  # Default match percentage for search results
            }
            formatted_jobs.append(formatted_job)
        
        return jsonify({
            "jobs": formatted_jobs,
            "total_results": len(formatted_jobs),
            "search_query": f"{keyword} internships in {location}",
            "api_status": "success" if len(formatted_jobs) > 5 else "limited_results"
        })
        
    except Exception as e:
        print(f"Error in search_jobs: {e}")
        return jsonify({"error": "Internal server error"}), 500

# In-memory profile storage (in production, use a database)
profiles = {}

@app.route('/profile', methods=['POST'])
def save_profile():
    """Save user profile"""
    try:
        profile_data = request.get_json()
        
        # Basic validation
        required_fields = ['name', 'email']
        for field in required_fields:
            if not profile_data.get(field):
                return jsonify({"error": f"{field} is required"}), 400
        
        # Generate profile ID (in production, use proper user authentication)
        profile_id = profile_data.get('email', 'default')
        
        # Save profile
        profiles[profile_id] = {
            "name": profile_data.get('name', ''),
            "email": profile_data.get('email', ''),
            "phone": profile_data.get('phone', ''),
            "education": profile_data.get('education', ''),
            "projects": profile_data.get('projects', []),
            "experience": profile_data.get('experience', []),
            "skills": profile_data.get('skills', []),
            "profile_photo": profile_data.get('profile_photo', ''),
            "location": profile_data.get('location', ''),
            "bio": profile_data.get('bio', ''),
            "created_at": profile_data.get('created_at', ''),
            "updated_at": profile_data.get('updated_at', '')
        }
        
        return jsonify({
            "message": "Profile saved successfully",
            "profile_id": profile_id
        })
        
    except Exception as e:
        print(f"Error saving profile: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/profile', methods=['GET'])
def get_profile():
    """Get user profile"""
    try:
        email = request.args.get('email', 'default')
        
        if email in profiles:
            return jsonify(profiles[email])
        else:
            return jsonify({"error": "Profile not found"}), 404
            
    except Exception as e:
        print(f"Error getting profile: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    try:
        print("🚀 Starting Flask API server...")
        print("📍 Server will be available at:")
        print("   - http://127.0.0.1:7000")
        print("   - http://localhost:7000")
        print("🔄 Press Ctrl+C to stop")
        print("-" * 50)
        app.run(debug=False, host='0.0.0.0', port=7000, threaded=True)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        print("🔄 Trying alternative port 7001...")
        app.run(debug=False, host='0.0.0.0', port=7001, threaded=True)