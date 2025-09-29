import os
import re
import requests
import numpy as np
import time
import random
import csv
import json
from io import BytesIO
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
from docx import Document
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
        # No Adzuna integration - using RapidAPI (internships API)
        # rapidapi key must be provided via environment for production use
        # Read RapidAPI credentials from environment
        self.rapidapi_key = os.getenv('RAPIDAPI_KEY')
        self.rapidapi_host = 'internships-api.p.rapidapi.com'
        # Optional Adzuna credentials (set these in your environment to enable Adzuna)
        self.adzuna_app_id = os.getenv('ADZUNA_APP_ID')
        self.adzuna_app_key = os.getenv('ADZUNA_APP_KEY')
        # Other defaults
        self.default_location = 'india'
        # Demo mode: when true, allow returning static dummy jobs for testing
        self.demo_mode = str(os.getenv('DEMO_MODE', 'false')).lower() in ('1', 'true', 'yes')
        # Domain synonyms to expand queries for better matching
        self.domain_synonyms = {
            'product': ['product', 'product management', 'product manager', 'pm'],
            'data': ['data', 'data science', 'data analyst', 'data engineering', 'machine learning'],
            'marketing': ['marketing', 'digital marketing', 'growth', 'content'],
            'design': ['design', 'ux', 'ui', 'product design'],
            'engineering': ['engineering', 'software', 'developer', 'backend', 'frontend']
        }
        
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
    # Adzuna integration removed. RapidAPI-based fetch_internships implementation exists later in this class.
    
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
    
    def calculate_ats_score(self, resume_text, job_descriptions, required_skills=None, skill_weights=None):
        """Hybrid ATS score: 50% keyword overlap, 50% semantic similarity.

        - keyword overlap: matched required skills / total required skills
        - semantic similarity: cosine similarity between resume and combined job descriptions (TF-IDF)
        Returns (score_percent, missing_keywords_list)
        """
        if not job_descriptions:
            return 0, []

        combined_job_text = " ".join(job_descriptions)

        # Extract required skills from job descriptions if not provided
        if required_skills is None:
            # use simple keyword extractor from combined job text
            required_skills = self.extract_keywords(combined_job_text)

        # Normalize skill lists
        resume_skills = set(self.extract_keywords(resume_text))
        required_skills_set = set(required_skills)

        # Keyword overlap score (0-100)
        if required_skills_set:
            # support optional weights
            if skill_weights:
                total_weight = sum(skill_weights.get(s, 1) for s in required_skills_set)
                matched_weight = sum(skill_weights.get(s, 1) for s in resume_skills & required_skills_set)
                keyword_score = (matched_weight / total_weight) * 100 if total_weight else 0
            else:
                keyword_score = (len(resume_skills & required_skills_set) / len(required_skills_set)) * 100
        else:
            keyword_score = 0

        # Semantic similarity via TF-IDF cosine
        try:
            vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
            tfidf_matrix = vectorizer.fit_transform([resume_text, combined_job_text])
            semantic_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0] * 100
        except Exception as e:
            print(f"Error computing semantic similarity: {e}")
            semantic_sim = 0

        # Hybrid score (50/50)
        ats_score = 0.5 * keyword_score + 0.5 * semantic_sim

        # Missing keywords (present in required_skills but missing in resume_skills)
        missing_keywords = sorted(list(required_skills_set - resume_skills))[:12]

        return round(min(100, max(0, ats_score)), 1), missing_keywords
    
    def calculate_job_match(self, resume_text, job_description):
        """Calculate match percentage for individual job"""
        try:
            vectorizer = TfidfVectorizer(stop_words='english', max_features=500)
            tfidf_matrix = vectorizer.fit_transform([resume_text, job_description])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return min(100, max(0, similarity * 100))
        except:
            return 50  # Default match percentage
    
    def fetch_internships(self, location="india", keyword="", time_filter="week"):
        """Fetch internships from RapidAPI with time filter.

        This function implements retries with exponential backoff + jitter and
        handles 429 rate-limit responses (using Retry-After when provided).
        It also attempts fallback, broader searches when the initial query
        returns no normalized results to increase chances of returning real
        internship recommendations.
        """
        # Read Adzuna credentials at call-time (in case env vars are set after engine construction)
        adzuna_app_id = os.getenv('ADZUNA_APP_ID')
        adzuna_app_key = os.getenv('ADZUNA_APP_KEY')

        # If Adzuna credentials are present, prefer calling Adzuna Jobs API for realtime results
        if adzuna_app_id and adzuna_app_key:
            try:
                # Map location to country code. Prefer India endpoint for common Indian cities/locations.
                loc_lower = (location or '').lower()
                india_tokens = ['india','bangalore','bengaluru','mumbai','delhi','pune','hyderabad','chennai','kolkata','ahmedabad','gurgaon','noida']
                if any(tok in loc_lower for tok in india_tokens):
                    country = 'in'
                else:
                    # If a location was provided and it doesn't look like an Indian city, default to GB;
                    # otherwise default to IN
                    country = 'gb' if location else 'in'

                adzuna_url = f'https://api.adzuna.com/v1/api/jobs/{country}/search/1'
                # Clean keyword: Adzuna performs better when 'intern' is not included in 'what'
                clean_kw = (keyword or 'intern')
                try:
                    import re as _re
                    clean_kw = _re.sub(r'\bintern\b', '', clean_kw, flags=_re.I).strip()
                    if not clean_kw:
                        clean_kw = 'intern'
                except Exception:
                    pass

                params = {
                    'app_id': adzuna_app_id,
                    'app_key': adzuna_app_key,
                    'results_per_page': 50,
                    'what': clean_kw,
                    'where': location or self.default_location,
                    'content-type': 'application/json'
                }
                print(f"[Adzuna] request -> url: {adzuna_url}, params: {{'what': params.get('what'), 'where': params.get('where'), 'results_per_page': params.get('results_per_page')}}")
                # Optionally respect time_filter by filtering with max_days_old if available
                if time_filter == 'day':
                    params['max_days_old'] = 1
                elif time_filter == 'week':
                    params['max_days_old'] = 7
                elif time_filter == 'month':
                    params['max_days_old'] = 30

                resp = requests.get(adzuna_url, params=params, timeout=15)
                # Debug logging for Adzuna response
                try:
                    body_snippet = resp.text[:1000]
                except Exception:
                    body_snippet = '<unable to read body>'

                if resp.status_code != 200:
                    print(f"[Adzuna] API returned status {resp.status_code}. Body snippet: {body_snippet}")
                else:
                    try:
                        data = resp.json()
                    except Exception as e:
                        print(f"Adzuna returned non-JSON response: {e}. Body snippet: {body_snippet}")
                        data = {}

                    results = data.get('results', []) if isinstance(data, dict) else []
                    if not results:
                        # Log the keys and a small sample so we can adjust normalization
                        keys = list(data.keys()) if isinstance(data, dict) else []
                        print(f"[Adzuna] returned no 'results' key. Response keys: {keys}. Body snippet: {body_snippet}")

                    normalized = []
                    for r in results:
                        normalized.append({
                            'title': r.get('title'),
                            'company': {'display_name': r.get('company', {}).get('display_name') if isinstance(r.get('company'), dict) else r.get('company')},
                            'location': {'display_name': r.get('location', {}).get('display_name') if isinstance(r.get('location'), dict) else r.get('location') or r.get('location_area')},
                            'description': r.get('description') or r.get('redirect_url') or r.get('salary_is_predicted',''),
                            'redirect_url': r.get('redirect_url') or r.get('lister_url') or r.get('url')
                        })
                    print(f"[Adzuna] normalized {len(normalized)} items. Sample: {normalized[:1]}")
                    if normalized:
                        return normalized[:15]
            except Exception as e:
                print(f"[Adzuna] request failed: {e}")

        # Select endpoint based on time_filter (RapidAPI internships fallback)
        url = "https://internships-api.p.rapidapi.com/active-jb-7d"
        if time_filter == "24h":
            url = "https://internships-api.p.rapidapi.com/active-jb-1d"
        elif time_filter == "month":
            url = "https://internships-api.p.rapidapi.com/active-jb-30d"

        headers = {
            "x-rapidapi-host": self.rapidapi_host,
            "x-rapidapi-key": self.rapidapi_key
        }

        params = {}
        if keyword:
            params["keyword"] = keyword
        if location:
            params["location"] = location

        if not self.rapidapi_key:
            print("Error: RAPIDAPI_KEY not set in environment")
            # Only return dummy jobs when demo mode is explicitly enabled; otherwise return an empty list
            return self.get_dummy_jobs() if self.demo_mode else []

        # Retry/backoff parameters
        max_retries = 4
        backoff = 1.0

        def normalize_jobs(data):
            raw_jobs = []
            if isinstance(data, list):
                raw_jobs = data
            elif isinstance(data, dict):
                raw_jobs = data.get('jobs') or data.get('results') or data.get('data') or []
                if isinstance(raw_jobs, dict):
                    raw_jobs = raw_jobs.get('items') or list(raw_jobs.values()) or []

            normalized = []
            seen = set()
            for job in raw_jobs:
                title = job.get('title') or job.get('job_title') or job.get('name') or job.get('position') or ''
                company = ''
                if isinstance(job.get('company'), dict):
                    company = job.get('company', {}).get('display_name') or job.get('company', {}).get('name', '')
                else:
                    company = job.get('company') or job.get('company_name') or ''
                location_str = ''
                if isinstance(job.get('location'), dict):
                    location_str = job.get('location', {}).get('display_name') or job.get('location', {}).get('name', '')
                else:
                    location_str = job.get('location') or job.get('city') or ''
                description = job.get('description') or job.get('job_description') or job.get('summary') or ''
                apply_link = job.get('redirect_url') or job.get('url') or job.get('apply_url') or job.get('link') or ''

                dedupe_key = (title.strip().lower(), company.strip().lower(), location_str.strip().lower())
                if dedupe_key in seen:
                    continue
                seen.add(dedupe_key)

                normalized.append({
                    'title': title,
                    'company': {'display_name': company},
                    'location': {'display_name': location_str},
                    'description': description,
                    'redirect_url': apply_link
                })

            return normalized

        # Primary retry loop
        for attempt in range(1, max_retries + 1):
            try:
                response = requests.get(url, headers=headers, params=params, timeout=20)
            except Exception as e:
                wait = backoff + random.uniform(0, 0.5)
                print(f"Request exception (attempt {attempt}/{max_retries}): {e}. Retrying in {wait:.1f}s")
                time.sleep(wait)
                backoff *= 2
                continue

            if response.status_code == 200:
                try:
                    data = response.json()
                except Exception as e:
                    print(f"Failed to decode JSON response: {e}")
                    # If JSON parsing fails, only return dummy data in demo mode
                    return self.get_dummy_jobs() if self.demo_mode else []

                normalized = normalize_jobs(data)
                if normalized:
                    return normalized[:15]
                # If no normalized results, try alternative parameter names
                print("No normalized jobs returned for primary query; will attempt alternative param keys and fallbacks")
                # Try different parameter names that some RapidAPI providers may accept
                alt_param_keys = ['query', 'search', 'title', 'position']
                for alt_key in alt_param_keys:
                    try:
                        alt_params = {'location': location}
                        alt_params[alt_key] = keyword
                        resp = requests.get(url, headers=headers, params=alt_params, timeout=15)
                    except Exception as e:
                        print(f"Alt request exception for key '{alt_key}': {e}")
                        continue

                    if resp.status_code != 200:
                        print(f"Alt RapidAPI status {resp.status_code} for param '{alt_key}'")
                        continue

                    try:
                        alt_data = resp.json()
                    except Exception as e:
                        print(f"Failed to parse alt JSON for '{alt_key}': {e}")
                        continue

                    alt_norm = normalize_jobs(alt_data)
                    if alt_norm:
                        return alt_norm[:15]
                # If alternate keys didn't help, break to fallbacks
                break

            if response.status_code == 429:
                # Rate limited — respect Retry-After if present
                ra = response.headers.get('Retry-After')
                try:
                    wait = int(ra) if ra and ra.isdigit() else backoff
                except:
                    wait = backoff
                jitter = random.uniform(0, 1)
                print(f"RapidAPI 429 rate limit. Waiting {wait + jitter:.1f}s before retry (attempt {attempt})")
                time.sleep(wait + jitter)
                backoff *= 2
                continue

            # Other non-200 responses: log and retry with backoff
            print(f"RapidAPI error: {response.status_code}. Response: {response.text[:200]}")
            wait = backoff + random.uniform(0, 0.5)
            time.sleep(wait)
            backoff *= 2

        # Fallback strategies: try broader or alternative keywords to increase chance of real results
        fallback_keywords = []
        if keyword:
            # try full keyword first
            fallback_keywords.append(keyword)
            # split into tokens (handle commas and whitespace)
            tokens = [t.strip() for t in re.split(r'[,\s]+', keyword) if t.strip()]
            # add tokens (domain, skills) as individual fallbacks
            for t in tokens:
                if len(t) > 2 and t.lower() not in (k.lower() for k in fallback_keywords):
                    fallback_keywords.append(t)
            # try the first token as a broader term
            if tokens:
                first = tokens[0]
                if first and first.lower() not in (k.lower() for k in fallback_keywords):
                    fallback_keywords.append(first)
        # generic fallback
        if 'intern' not in (k.lower() for k in fallback_keywords):
            fallback_keywords.append('intern')

        normalized_all = []
        seen = set()
        for fk in fallback_keywords:
            print(f"Fallback search with keyword: '{fk}'")
            params['keyword'] = fk
            try:
                resp = requests.get(url, headers=headers, params=params, timeout=20)
            except Exception as e:
                print(f"Fallback request error for '{fk}': {e}")
                continue

            if resp.status_code != 200:
                print(f"Fallback RapidAPI status {resp.status_code} for keyword '{fk}'")
                continue

            try:
                data = resp.json()
            except Exception as e:
                print(f"Failed to decode fallback JSON for '{fk}': {e}")
                continue

            temp_norm = normalize_jobs(data)
            for job in temp_norm:
                key = (job.get('title','').strip().lower(), job.get('company',{}).get('display_name','').strip().lower(), job.get('location',{}).get('display_name','').strip().lower())
                if key in seen:
                    continue
                seen.add(key)
                normalized_all.append(job)
            if len(normalized_all) >= 10:
                break

        if normalized_all:
            # filter out results lacking a title which are low-quality
            filtered = [j for j in normalized_all if j.get('title') and j.get('title').strip()]
            if filtered:
                return filtered[:15]
            return normalized_all[:15]

        # If nothing worked, return dummy jobs only in demo mode; otherwise return empty list
        return self.get_dummy_jobs() if self.demo_mode else []


@app.route('/recommend', methods=['POST'])
def recommend():
    """Main endpoint: accepts resume file + optional fields and returns ATS score + recommendations"""
    try:
        # Read form fields
        if 'resume' not in request.files:
            return jsonify({'error': 'Resume file is required'}), 400

        resume_file = request.files['resume']
        skills = request.form.get('skills', '')
        education = request.form.get('education', '')
        location = request.form.get('location', 'india')
        time_filter = request.form.get('time_filter', 'week')
        # Optional domain parameter (e.g., product, marketing, data)
        domain = request.form.get('domain', '').strip()

        # Read file bytes
        content = resume_file.read()

        # Extract text based on file type
        filename = resume_file.filename.lower()
        if filename.endswith('.pdf'):
            resume_text = ats_engine.extract_text_from_pdf(content)
        elif filename.endswith('.docx'):
            resume_text = ats_engine.extract_text_from_docx(content)
        else:
            # Try to decode as text
            try:
                resume_text = content.decode('utf-8', errors='ignore')
            except:
                resume_text = ''

        resume_text = ats_engine.clean_text(resume_text + ' ' + skills + ' ' + education)

        # Build a search keyword: prefer domain (if provided) then include skills
        search_trace = []
        effective_search_keyword = ''

        if domain:
            dkey = domain.lower()
            synonyms = ats_engine.domain_synonyms.get(dkey, [domain])
            # join synonyms with skills to make stronger queries
            for syn in synonyms:
                candidate = f"{syn} {skills}".strip()
                search_trace.append(candidate)
            # fallback: domain + first skill token
            if skills:
                first_skill = skills.split(',')[0].split()[0]
                search_trace.append(f"{domain} {first_skill}")
        else:
            # no domain supplied: tokenized skills as candidates
            tokens = [t.strip() for t in re.split(r'[,\s]+', skills) if t.strip()]
            for t in tokens:
                search_trace.append(t)

        # Add generic fallbacks
        search_trace.append(skills.strip())
        search_trace.append('intern')

        # Try successive search_trace items until we get results
        jobs = []
        for q in search_trace:
            if not q:
                continue
            effective_search_keyword = q
            print(f"Attempting RapidAPI search with: '{q}' and location '{location}'")
            jobs = ats_engine.fetch_internships(location=location, keyword=q, time_filter=time_filter)
            if jobs and len(jobs) > 0:
                break

        # If still empty, final fallback to generic interns: use dummy jobs so
        # we can still compute an ATS score for the user even when provider
        # APIs returned no results. We keep demo_mode behavior for returning
        # live search results, but ensure scoring can continue by using
        # built-in dummy jobs as a fallback for scoring only.
        used_dummy_for_scoring = False
        if not jobs:
            print("No jobs found from providers; using built-in dummy jobs for ATS scoring fallback.")
            jobs = ats_engine.get_dummy_jobs()
            used_dummy_for_scoring = True

        # Filter and prioritize jobs by domain tokens and location to improve relevance
        domain_tokens = []
        if domain:
            dkey = domain.lower()
            domain_tokens = [t.lower() for t in ats_engine.domain_synonyms.get(dkey, [domain])]
        else:
            # Try to extract token from skills
            domain_tokens = [t.lower() for t in re.split(r'[,\s]+', skills) if t]

        loc_tokens = [t.lower() for t in re.split(r'[,\s]+', (location or '').strip()) if t]

        def job_contains_tokens(job, tokens):
            txt = ' '.join([str(job.get('title','')), str(job.get('company',{}).get('display_name','') if isinstance(job.get('company',{}), dict) else job.get('company','')), str(job.get('location',{}).get('display_name','') if isinstance(job.get('location',{}), dict) else job.get('location','')), str(job.get('description',''))]).lower()
            return any(tok in txt for tok in tokens if tok)

        # apply domain filter if it yields reasonable matches
        filtered_jobs = jobs
        if domain_tokens:
            domain_matched = [j for j in jobs if job_contains_tokens(j, domain_tokens)]
            if len(domain_matched) >= 3:
                filtered_jobs = domain_matched
            elif len(domain_matched) > 0:
                # if some matches, use them but still keep others for fallback
                filtered_jobs = domain_matched + [j for j in jobs if j not in domain_matched]

        # Prioritize location matches by sorting
        def loc_score_job(job):
            txt = ' '.join([str(job.get('title','')), str(job.get('company',{}).get('display_name','') if isinstance(job.get('company',{}), dict) else job.get('company','')), str(job.get('location',{}).get('display_name','') if isinstance(job.get('location',{}), dict) else job.get('location','')), str(job.get('description',''))]).lower()
            score = 0
            for tok in loc_tokens:
                if tok and tok in txt:
                    score += 1
            return score

        filtered_jobs.sort(key=loc_score_job, reverse=True)

        # Prepare job descriptions for ATS scoring
        job_texts = []
        formatted_recs = []
        for job in filtered_jobs:
            title = job.get('title') or job.get('job_title') or job.get('name') or 'Internship'
            company = (job.get('company', {}) if isinstance(job.get('company', {}), dict) else {}).get('display_name') if isinstance(job.get('company', {}), dict) else job.get('company') if isinstance(job.get('company', str)) else job.get('company_name') if job.get('company_name') else 'Company'
            location_str = (job.get('location', {}) .get('display_name') ) if isinstance(job.get('location', {}), dict) else job.get('location') or job.get('city') or 'Location'
            description = job.get('description') or job.get('job_description') or job.get('summary') or ''
            apply_link = job.get('redirect_url') or job.get('url') or job.get('apply_url') or job.get('link') or '#'
            # mark domain/location match flags for later boosting
            domain_match = False
            location_match = False
            txt_fields = f"{title} {company} {location_str} {description}".lower()
            if domain_tokens and any(tok in txt_fields for tok in domain_tokens):
                domain_match = True
            if loc_tokens and any(tok in txt_fields for tok in loc_tokens):
                location_match = True

            combined = f"{title} {company} {location_str} {description}"
            job_texts.append(ats_engine.clean_text(combined))

            formatted_recs.append({
                'title': title,
                'company': company,
                'location': location_str,
                'description': description,
                'apply_link': apply_link,
                'domain_match': domain_match,
                'location_match': location_match
            })

        # Compute ATS score using hybrid approach across the returned internships
        ats_score, missing_keywords = ats_engine.calculate_ats_score(resume_text, job_texts)

        # Compute match percent per recommendation
        recs_with_score = []
        for rec, job_text in zip(formatted_recs, job_texts):
            match = ats_engine.calculate_job_match(resume_text, job_text)
            recs_with_score.append({
                'title': rec['title'],
                'company': rec['company'],
                'location': rec['location'],
                'description': rec['description'],
                'apply_link': rec['apply_link'],
                'match_percent': int(round(match)),
                'raw_job_text': job_text
            })

        # Compute a final score combining semantic match, domain and location boosts
        domain_tokens = [t.lower() for t in (domain or '').split() if t]
        loc_tokens = [t.lower() for t in re.split(r'[,\s]+', (location or '').strip()) if t]

        def compute_final_score(entry):
            base = entry.get('match_percent', 0)
            boost = 0
            text = (entry.get('raw_job_text','') or '').lower()
            # domain boost
            for tok in domain_tokens:
                if tok and tok in text:
                    boost += 25
            # location boost
            for tok in loc_tokens:
                if tok and tok in text:
                    boost += 20
            # keyword overlap boost (small)
            boost += 5 if any(k in text for k in ([s.strip().lower() for s in skills.split(',')] if skills else [])) else 0
            return base + boost

        # Calculate final_score for each entry and filter out very low-quality items
        for e in recs_with_score:
            e['final_score'] = int(round(compute_final_score(e)))

        # Remove items with extremely low final score (e.g., <5)
        recs_with_score = [e for e in recs_with_score if e.get('final_score', 0) >= 5]

        # Sort by final_score desc, then by match_percent desc
        recs_with_score.sort(key=lambda x: (x.get('final_score', 0), int(str(x.get('match_percent','0')).replace('%','') if isinstance(x.get('match_percent'), str) else x.get('match_percent',0))), reverse=True)

        # Format match_percent as percent string and drop raw_job_text and final_score before returning
        for e in recs_with_score:
            e['match_percent'] = f"{int(e.get('match_percent',0))}%"
            e.pop('raw_job_text', None)
            e.pop('final_score', None)

        # Determine status
        status = 'Unknown'
        if ats_score >= 80:
            status = 'Excellent'
        elif ats_score >= 60:
            status = 'Good'
        elif ats_score >= 40:
            status = 'Fair'
        else:
            status = 'Needs Improvement'

        # Location relevance boosting: prefer job entries containing location tokens
        loc_tokens = [t.lower() for t in re.split(r'[,\s]+', (location or '').strip()) if t]
        def location_score(entry):
            txt = ' '.join([str(entry.get('title','')), str(entry.get('company','')), str(entry.get('location','')), str(entry.get('description',''))]).lower()
            score = 0
            for tok in loc_tokens:
                if tok and tok in txt:
                    score += 30
            return score

        # Final sort: already sorted by domain-boosted match; now boost by location
        recs_with_score.sort(key=lambda e: (int(e['match_percent'].replace('%','')), ) , reverse=True)
        recs_with_score.sort(key=lambda e: location_score(e), reverse=True)

        # Include effective search keyword and trace for debugging/tuning
        response_payload = {
            'ats_score': ats_score,
            'status': status,
            'missing_keywords': missing_keywords,
            'recommendations': recs_with_score,
            'effective_search_keyword': effective_search_keyword,
            'search_trace': search_trace,
            'used_dummy_jobs_for_scoring': used_dummy_for_scoring
        }

        return jsonify(response_payload)

    except Exception as e:
        print(f"Error in /recommend: {e}")
        return jsonify({'error': 'Internal server error'}), 500

# Create a single engine instance for route handlers
ats_engine = ResumeATSEngine()
@app.route('/search_jobs', methods=['GET'])
def search_jobs():
    """Search jobs by keyword and location"""
    try:
        keyword = request.args.get('keyword', 'intern')
        location = request.args.get('location', 'india')
        time_filter = request.args.get('time_filter', 'week')

        # Use the improved internship fetching method
        jobs = ats_engine.fetch_internships(location=location, keyword=keyword, time_filter=time_filter)

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

        api_status = 'success' if len(formatted_jobs) > 0 else ('demo_mode' if ats_engine.demo_mode else 'no_results')
        return jsonify({
            "jobs": formatted_jobs,
            "total_results": len(formatted_jobs),
            "search_query": f"{keyword} internships in {location}",
            "api_status": api_status
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


def parse_jobs_file(file_storage):
    """Parse uploaded CSV or JSON file containing job listings.
    Expected CSV columns: title,company,location,description,apply_link
    Expected JSON: list of objects with the same keys.
    Returns list of job dicts.
    """
    try:
        filename = (file_storage.filename or '').lower()
        content = file_storage.read()
        # Reset pointer for potential re-read by caller
        try:
            file_storage.stream.seek(0)
        except Exception:
            pass

        # Try JSON first
        if filename.endswith('.json') or (content.strip().startswith(b'[') or content.strip().startswith(b'{')):
            try:
                data = json.loads(content.decode('utf-8', errors='ignore'))
                if isinstance(data, dict):
                    # If single object, wrap into list
                    data = [data]
                jobs = []
                for it in data:
                    jobs.append({
                        'title': it.get('title') or it.get('job_title') or it.get('name') or 'Internship',
                        'company': {'display_name': it.get('company') or it.get('company_name') or ''},
                        'location': {'display_name': it.get('location') or it.get('city') or ''},
                        'description': it.get('description') or it.get('job_description') or it.get('summary') or '',
                        'redirect_url': it.get('apply_link') or it.get('apply_url') or it.get('link') or ''
                    })
                return jobs
            except Exception as e:
                print(f"Failed to parse JSON jobs file: {e}")

        # Fallback: parse as CSV
        try:
            text = content.decode('utf-8', errors='ignore')
            reader = csv.DictReader(text.splitlines())
            jobs = []
            for row in reader:
                jobs.append({
                    'title': row.get('title') or row.get('job_title') or row.get('name') or 'Internship',
                    'company': {'display_name': row.get('company') or row.get('company_name') or ''},
                    'location': {'display_name': row.get('location') or row.get('city') or ''},
                    'description': row.get('description') or row.get('job_description') or row.get('summary') or '',
                    'redirect_url': row.get('apply_link') or row.get('apply_url') or row.get('link') or ''
                })
            return jobs
        except Exception as e:
            print(f"Failed to parse CSV jobs file: {e}")
            return []
    except Exception as e:
        print(f"Error reading jobs file: {e}")
        return []


@app.route('/recommend_from_jobs', methods=['POST'])
def recommend_from_jobs():
    """Accepts a resume file and a jobs CSV/JSON file, returns ATS recommendations."""
    try:
        if 'resume' not in request.files:
            return jsonify({'error': 'Resume file is required'}), 400
        if 'jobs_file' not in request.files:
            return jsonify({'error': 'jobs_file (CSV or JSON) is required'}), 400

        resume_file = request.files['resume']
        jobs_file = request.files['jobs_file']

        # Read resume text
        content = resume_file.read()
        filename = resume_file.filename.lower()
        if filename.endswith('.pdf'):
            resume_text = ats_engine.extract_text_from_pdf(content)
        elif filename.endswith('.docx'):
            resume_text = ats_engine.extract_text_from_docx(content)
        else:
            try:
                resume_text = content.decode('utf-8', errors='ignore')
            except:
                resume_text = ''

        # Clean resume text and include education if provided in form
        education = request.form.get('education', '')
        skills = request.form.get('skills', '')
        location = request.form.get('location', '')
        domain = request.form.get('domain', '')

        resume_text = ats_engine.clean_text(resume_text + ' ' + skills + ' ' + education)

        # Parse jobs
        jobs = parse_jobs_file(jobs_file)
        if not jobs:
            return jsonify({'error': 'No jobs parsed from the provided file', 'parsed_count': 0}), 400

        # Reuse existing recommend logic but operate on provided jobs
        # We'll replicate the core scoring parts here to avoid duplicating HTTP calls
        # Prepare job_texts and formatted_recs
        job_texts = []
        formatted_recs = []
        for job in jobs:
            title = job.get('title') or 'Internship'
            company = (job.get('company', {}) if isinstance(job.get('company', {}), dict) else {}).get('display_name') if isinstance(job.get('company', {}), dict) else job.get('company') if isinstance(job.get('company', str)) else job.get('company_name') if job.get('company_name') else 'Company'
            location_str = (job.get('location', {}) .get('display_name') ) if isinstance(job.get('location', {}), dict) else job.get('location') or job.get('city') or 'Location'
            description = job.get('description') or job.get('job_description') or job.get('summary') or ''
            apply_link = job.get('redirect_url') or job.get('url') or job.get('apply_url') or job.get('link') or job.get('apply_link') or '#'
            combined = f"{title} {company} {location_str} {description}"
            job_texts.append(ats_engine.clean_text(combined))
            formatted_recs.append({
                'title': title,
                'company': company,
                'location': location_str,
                'description': description,
                'apply_link': apply_link
            })

        ats_score, missing_keywords = ats_engine.calculate_ats_score(resume_text, job_texts)

        recs_with_score = []
        for rec, job_text in zip(formatted_recs, job_texts):
            match = ats_engine.calculate_job_match(resume_text, job_text)
            recs_with_score.append({
                'title': rec['title'],
                'company': rec['company'],
                'location': rec['location'],
                'description': rec['description'],
                'apply_link': rec['apply_link'],
                'match_percent': int(round(match))
            })

        # Simple final scoring: prioritize by match_percent and optionally by location/domain
        # Apply location/domain boosts if provided
        domain_tokens = [t.lower() for t in (domain or '').split() if t]
        loc_tokens = [t.lower() for t in re.split(r'[,\s]+', (location or '').strip()) if t]

        def compute_final_score_local(entry):
            base = entry.get('match_percent', 0)
            boost = 0
            text = (entry.get('title','') + ' ' + entry.get('company','') + ' ' + entry.get('location','') + ' ' + entry.get('description','')).lower()
            for tok in domain_tokens:
                if tok and tok in text:
                    boost += 25
            for tok in loc_tokens:
                if tok and tok in text:
                    boost += 20
            return base + boost

        for e in recs_with_score:
            e['final_score'] = int(round(compute_final_score_local(e)))

        recs_with_score = [e for e in recs_with_score if e.get('final_score',0) >= 5]
        recs_with_score.sort(key=lambda x: (x.get('final_score',0), x.get('match_percent',0)), reverse=True)

        for e in recs_with_score:
            e['match_percent'] = f"{int(e.get('match_percent',0))}%"
            e.pop('final_score', None)

        status = 'Unknown'
        if ats_score >= 80:
            status = 'Excellent'
        elif ats_score >= 60:
            status = 'Good'
        elif ats_score >= 40:
            status = 'Fair'
        else:
            status = 'Needs Improvement'

        return jsonify({
            'ats_score': ats_score,
            'status': status,
            'missing_keywords': missing_keywords,
            'recommendations': recs_with_score,
            'parsed_count': len(jobs)
        })

    except Exception as e:
        print(f"Error in /recommend_from_jobs: {e}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    try:
        print("Starting Flask API server...")
        print("Server will be available at:")
        print("   - http://127.0.0.1:5002")
        print("   - http://localhost:5002")
        print("Press Ctrl+C to stop")
        print("-" * 50)
        app.run(debug=False, host='0.0.0.0', port=5002, threaded=True)
    except Exception as e:
        print(f"Error starting server: {e}")
        print("Trying alternative port 7001...")
        app.run(debug=False, host='0.0.0.0', port=5003, threaded=True)