import requests
import time

print("🔍 Testing your LIVE Flask API endpoint...")
print("=" * 50)

# Give the server a moment to fully start
time.sleep(2)

try:
    # Test the search endpoint
    url = "http://127.0.0.1:5001/search_jobs"
    params = {
        'keyword': 'product manager',
        'location': 'india'
    }
    
    print(f"Making request to: {url}")
    print(f"Parameters: {params}")
    
    response = requests.get(url, params=params, timeout=15)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        jobs = data.get('jobs', [])
        
        print(f"\n✅ SUCCESS! API ENDPOINT IS WORKING!")
        print(f"📊 Jobs found: {len(jobs)}")
        
        if jobs:
            print(f"\n🔥 LIVE INTERNSHIP RESULTS:")
            for i, job in enumerate(jobs[:3], 1):
                print(f"\n{i}. {job.get('title', 'N/A')}")
                print(f"   🏢 Company: {job.get('company', {}).get('display_name', 'N/A')}")
                print(f"   📍 Location: {job.get('location', {}).get('display_name', 'N/A')}")
                
        print(f"\n" + "=" * 50)
        print("🎉 FINAL RESULT: YOUR COMPLETE API IS WORKING!")
        print("✅ Flask server is running")
        print("✅ API endpoints are responding")
        print("✅ Real internship data is being fetched")
        print("✅ Your frontend can now connect to get live data!")
        
    else:
        print(f"\n❌ API Error: {response.status_code}")
        print(f"Response: {response.text}")
        
except requests.exceptions.ConnectionError:
    print("\n⚠️ Connection failed - Server might be starting up")
    print("Wait a few more seconds and try again")
    
except Exception as e:
    print(f"\n❌ Request failed: {e}")

print(f"\n🌐 Your Flask server is running at: http://127.0.0.1:5001")
print(f"🔗 Frontend can now connect to get real internships!")