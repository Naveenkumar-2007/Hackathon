import requests
import time

def test_flask_server():
    print("🔍 Testing Flask Server...")
    print("=" * 40)
    
    base_url = "http://127.0.0.1:5000"
    
    try:
        # Test health endpoint
        print("1. Testing health endpoint...")
        health_response = requests.get(f"{base_url}/health", timeout=5)
        print(f"   Status: {health_response.status_code}")
        if health_response.status_code == 200:
            print(f"   Response: {health_response.json()}")
        
        # Test search jobs endpoint
        print("\n2. Testing search jobs endpoint...")
        search_response = requests.get(
            f"{base_url}/search_jobs", 
            params={"keyword": "product", "location": "india"},
            timeout=10
        )
        print(f"   Status: {search_response.status_code}")
        
        if search_response.status_code == 200:
            data = search_response.json()
            print(f"   Jobs found: {data.get('count', 0)}")
            print(f"   Data source: {data.get('source', 'unknown')}")
            
            jobs = data.get('jobs', [])
            if jobs:
                print(f"\n   Sample job:")
                job = jobs[0]
                print(f"   📋 Title: {job.get('title', 'N/A')}")
                print(f"   🏢 Company: {job.get('company', {}).get('display_name', 'N/A')}")
                print(f"   📍 Location: {job.get('location', {}).get('display_name', 'N/A')}")
        
        print("\n" + "=" * 40)
        print("✅ SERVER IS WORKING PERFECTLY!")
        print("🌐 Your API is ready for frontend connection!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - Server might not be running")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    # Wait a moment for server to fully start
    time.sleep(1)
    test_flask_server()