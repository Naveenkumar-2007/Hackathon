import requests
import os

print("🔍 TESTING YOUR NEW API CREDENTIALS")
print("=" * 50)

# Use your provided credentials directly
api_id = "33e2a468"
api_key = "96ba55c5dca94f6518e12c89b6732bcf"

print(f"API ID: {api_id}")
print(f"API Key: {api_key[:8]}...")

# Test the Adzuna API
url = "https://api.adzuna.com/v1/api/jobs/in/search/1"
params = {
    'app_id': api_id,
    'app_key': api_key,
    'what': 'internship',
    'where': 'india',
    'results_per_page': 10
}

try:
    print("\n🚀 Making API request...")
    response = requests.get(url, params=params, timeout=10)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        jobs = data.get('results', [])
        total_count = data.get('count', 0)
        
        print(f"\n✅ SUCCESS! API IS WORKING!")
        print(f"📊 Total internships available: {total_count}")
        print(f"📋 Retrieved: {len(jobs)} internships")
        
        if jobs:
            print(f"\n🔥 REAL INTERNSHIP EXAMPLES:")
            for i, job in enumerate(jobs[:3], 1):
                print(f"\n{i}. {job.get('title', 'N/A')}")
                print(f"   🏢 Company: {job.get('company', {}).get('display_name', 'N/A')}")
                print(f"   📍 Location: {job.get('location', {}).get('display_name', 'N/A')}")
                salary_min = job.get('salary_min')
                salary_max = job.get('salary_max')
                if salary_min and salary_max:
                    print(f"   💰 Salary: ₹{salary_min:,} - ₹{salary_max:,}")
                else:
                    print(f"   💰 Salary: Not specified")
        
        print(f"\n" + "=" * 50)
        print("🎉 FINAL RESULT: YOUR API IS WORKING PERFECTLY!")
        print("✅ Authentication successful")
        print("✅ Real internship data is available")
        print("✅ Your Flask backend can now fetch live data")
        
    else:
        print(f"\n❌ API Error: {response.status_code}")
        print(f"Response: {response.text}")
        print(f"\n❌ RESULT: AUTHENTICATION STILL FAILING")
        
except Exception as e:
    print(f"\n❌ Request failed: {e}")
    print(f"❌ RESULT: CONNECTION ISSUE")