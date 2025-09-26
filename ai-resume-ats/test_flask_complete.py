import requests
import json

def test_flask_internship_search():
    """Test the Flask app's internship search endpoint"""
    
    print("🧪 Testing Flask App Internship Search")
    print("=" * 40)
    
    try:
        # Test 1: Product Management search
        print("🔍 Testing Product Management internship search...")
        response = requests.get(
            "http://127.0.0.1:5000/search_jobs",
            params={"keyword": "product management", "location": "india"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            jobs = data.get('jobs', [])
            print(f"✅ SUCCESS: Found {len(jobs)} internships")
            
            # Show first 3 results
            for i, job in enumerate(jobs[:3]):
                title = job.get('title', 'N/A')
                company = job.get('company', {}).get('display_name', 'N/A')
                location = job.get('location', {}).get('display_name', 'N/A')
                print(f"   {i+1}. {title} at {company} - {location}")
        else:
            print(f"❌ ERROR: Status {response.status_code}")
            print(f"Response: {response.text}")
        
        print()
        
        # Test 2: General internship search
        print("🔍 Testing general internship search...")
        response = requests.get(
            "http://127.0.0.1:5000/search_jobs", 
            params={"keyword": "", "location": "india"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            jobs = data.get('jobs', [])
            print(f"✅ SUCCESS: Found {len(jobs)} internships")
            
            # Show first 3 results
            for i, job in enumerate(jobs[:3]):
                title = job.get('title', 'N/A')
                company = job.get('company', {}).get('display_name', 'N/A')
                location = job.get('location', {}).get('display_name', 'N/A')
                print(f"   {i+1}. {title} at {company} - {location}")
        else:
            print(f"❌ ERROR: Status {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")

def test_health_endpoint():
    """Test the health endpoint"""
    print("\n🏥 Testing Health Endpoint...")
    
    try:
        response = requests.get("http://127.0.0.1:5000/health", timeout=10)
        
        if response.status_code == 200:
            print("✅ Health check passed!")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Health check failed: Status {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")

if __name__ == "__main__":
    test_health_endpoint()
    test_flask_internship_search()
    
    print("\n" + "=" * 50)
    print("🎯 If tests passed, your app is ready!")
    print("Open your React frontend and search for internships.")
    print("You should now see REAL internship opportunities from Adzuna API!")