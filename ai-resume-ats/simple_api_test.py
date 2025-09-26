import sys
import os

# Add the backend directory to the path
backend_dir = r"C:\Users\navee\Cisco Packet Tracer 8.2.2\saves\certificates\genaihack\ai-resume-ats\backend"
sys.path.insert(0, backend_dir)
os.chdir(backend_dir)

print("🔍 TESTING YOUR API STATUS")
print("=" * 50)

try:
    # Test 1: Basic imports
    print("1. Testing imports...")
    from flask import Flask
    print("   ✅ Flask imported")
    
    import requests
    print("   ✅ Requests imported")
    
    # Test 2: Import your app
    print("\n2. Testing your app...")
    import app as flask_app
    print("   ✅ Your Flask app imported successfully")
    
    # Test 3: Test Adzuna API directly
    print("\n3. Testing Adzuna API connection...")
    
    # Get your API credentials
    from dotenv import load_dotenv
    load_dotenv()
    
    api_id = os.getenv('ADZUNA_APP_ID', '33e2a468')
    api_key = os.getenv('ADZUNA_API_KEY', 'b7b5dae8f8b9b5e5a1f2c3d4e5f6g7h8')
    
    print(f"   API ID: {api_id}")
    print(f"   API Key: {api_key[:8]}...")
    
    # Direct API test
    url = f"https://api.adzuna.com/v1/api/jobs/in/search/1"
    params = {
        'app_id': api_id,
        'app_key': api_key,
        'what': 'internship',
        'where': 'india',
        'results_per_page': 5
    }
    
    response = requests.get(url, params=params, timeout=10)
    print(f"   API Response Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        jobs = data.get('results', [])
        print(f"   ✅ API WORKING! Found {len(jobs)} internships")
        
        if jobs:
            print(f"\n   Sample internship:")
            job = jobs[0]
            print(f"   📋 Title: {job.get('title', 'N/A')}")
            print(f"   🏢 Company: {job.get('company', {}).get('display_name', 'N/A')}")
            print(f"   📍 Location: {job.get('location', {}).get('display_name', 'N/A')}")
            print(f"   💰 Salary: {job.get('salary_min', 'N/A')} - {job.get('salary_max', 'N/A')}")
    else:
        print(f"   ❌ API Error: {response.status_code}")
        print(f"   Response: {response.text}")
    
    print("\n" + "=" * 50)
    if response.status_code == 200:
        print("🎉 RESULT: YOUR API IS WORKING PERFECTLY!")
        print("✅ The Adzuna API connection is functional")
        print("✅ You can fetch real internship data")
        print("\n💡 The issue is likely with Flask server connectivity,")
        print("   not with the API itself.")
    else:
        print("❌ RESULT: API CONNECTION ISSUE")
        print("🔧 Check your API credentials in the .env file")

except Exception as e:
    print(f"\n❌ Error during API test: {e}")
    import traceback
    traceback.print_exc()
    
    print("\n" + "=" * 50)
    print("❌ RESULT: SETUP ISSUE DETECTED")
    print("🔧 Check your backend setup and dependencies")