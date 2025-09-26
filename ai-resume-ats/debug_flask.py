import sys
import os

# Add the backend directory to the path
backend_dir = r"C:\Users\navee\Cisco Packet Tracer 8.2.2\saves\certificates\genaihack\ai-resume-ats\backend"
sys.path.insert(0, backend_dir)
os.chdir(backend_dir)

print("Testing Flask app imports and basic functionality...")

try:
    from flask import Flask
    print("✅ Flask imported successfully")
    
    from flask_cors import CORS
    print("✅ Flask-CORS imported successfully")
    
    import requests
    print("✅ Requests imported successfully")
    
    # Import and test the main app
    import app as flask_app
    print("✅ Main app module imported successfully")
    print(f"✅ Flask app object: {flask_app.app}")
    
    # Test the API endpoints
    print("\n🔍 Testing API endpoints...")
    
    # Test if we can call the search_jobs function directly
    from app import fetch_internships
    print("✅ fetch_internships function imported")
    
    # Test API call
    print("Testing Adzuna API call...")
    internships = fetch_internships("product manager", "india")
    print(f"✅ API returned {len(internships)} internships")
    
    if internships:
        print("Sample internship:")
        sample = internships[0]
        print(f"  Title: {sample.get('title', 'N/A')}")
        print(f"  Company: {sample.get('company', {}).get('display_name', 'N/A')}")
        print(f"  Location: {sample.get('location', {}).get('display_name', 'N/A')}")
    
    print("\n✅ API is working correctly!")
    print("Your Adzuna API integration is functional.")
    
except Exception as e:
    print(f"❌ Error during import or startup: {e}")
    import traceback
    traceback.print_exc()