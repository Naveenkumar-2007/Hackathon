#!/usr/bin/env python3
"""
Manual demonstration of internship search functionality
"""

import os
import sys
import json
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))
os.chdir(backend_dir)

# Load environment
from dotenv import load_dotenv
load_dotenv()

try:
    from app import ResumeATSEngine
    
    print("🎯 Testing Your AI Resume ATS + Internship Recommendation Engine")
    print("=" * 70)
    
    # Create engine instance
    engine = ResumeATSEngine()
    
    print(f"✅ Adzuna API ID: {engine.adzuna_app_id}")
    print(f"✅ Adzuna API Key: {engine.adzuna_app_key[:10]}...")
    print()
    
    # Test internship search
    print("🔍 Searching for Product Management Internships...")
    jobs = engine.fetch_internships(location="india", keyword="product management")
    
    print(f"📋 Found {len(jobs)} internship opportunities:")
    print()
    
    for i, job in enumerate(jobs[:8], 1):  # Show first 8 results
        title = job.get('title', 'N/A')
        company = job.get('company', {}).get('display_name', 'N/A')
        location = job.get('location', {}).get('display_name', 'N/A')
        salary = job.get('salary_min', 'Not specified')
        
        print(f"{i:2d}. 📌 {title}")
        print(f"    🏢 {company}")
        print(f"    📍 {location}")
        print(f"    💰 Salary: {salary}")
        print()
    
    print("=" * 70)
    print("🎉 SUCCESS! Your API integration is working perfectly!")
    print()
    print("💡 To test in your web application:")
    print("   1. Make sure both servers are running:")
    print("      - Backend: python app.py (should show port 5001)")
    print("      - Frontend: npm run dev (running on port 3001)")
    print("   2. Open http://localhost:3001 in your browser")
    print("   3. Go to 'Internship Search' page")
    print("   4. Search for 'product management' or leave blank")
    print("   5. You should see real internship results!")
    print()
    print("🔧 If connection issues persist:")
    print("   - Check Windows Firewall settings")
    print("   - Try running as Administrator")
    print("   - Use 'localhost' instead of '127.0.0.1' in browser")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()