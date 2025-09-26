import requests
import json

# Test the internship search API
try:
    print("Testing Internship Search API...")
    response = requests.get("http://127.0.0.1:5000/search_jobs", 
                          params={"keyword": "product management", "location": "india"})
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ API working! Found {data.get('total_results', 0)} internships")
        print(f"Search query: {data.get('search_query', 'N/A')}")
        
        jobs = data.get("jobs", [])
        for i, job in enumerate(jobs[:3]):  # Show first 3 internships
            print(f"\n{i+1}. {job.get('title', 'N/A')}")
            print(f"   Company: {job.get('company', 'N/A')}")
            print(f"   Location: {job.get('location', 'N/A')}")
    else:
        print(f"❌ API Error: {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"❌ Connection Error: {e}")

# Test the health endpoint
try:
    print("\n\nTesting Health Endpoint...")
    response = requests.get("http://127.0.0.1:5000/health")
    if response.status_code == 200:
        print("✅ Backend is healthy!")
        print(response.json())
    else:
        print(f"❌ Health check failed: {response.status_code}")
except Exception as e:
    print(f"❌ Health check error: {e}")