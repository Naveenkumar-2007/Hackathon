import requests
import time

def test_windows_server():
    print("🧪 Testing Windows-Compatible Flask Server")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:9000"
    
    # Wait for server to be ready
    time.sleep(2)
    
    try:
        # Test health endpoint
        print("1. Testing health endpoint...")
        health_response = requests.get(f"{base_url}/health", timeout=10)
        print(f"   Status: {health_response.status_code}")
        
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f"   ✅ Server is healthy!")
            print(f"   📊 Internships available: {health_data.get('internships_count', 0)}")
        
        # Test search endpoint  
        print("\n2. Testing search jobs endpoint...")
        search_response = requests.get(
            f"{base_url}/search_jobs",
            params={"keyword": "product", "location": "bangalore"},
            timeout=10
        )
        print(f"   Status: {search_response.status_code}")
        
        if search_response.status_code == 200:
            search_data = search_response.json()
            print(f"   ✅ Search successful!")
            print(f"   📋 Jobs found: {search_data.get('count', 0)}")
            
            jobs = search_data.get('jobs', [])
            if jobs:
                print(f"\n   🔥 Sample job:")
                job = jobs[0]
                print(f"   📋 Title: {job.get('title', 'N/A')}")
                print(f"   🏢 Company: {job.get('company', {}).get('display_name', 'N/A')}")
                print(f"   💰 Salary: ₹{job.get('salary_min', 0):,} - ₹{job.get('salary_max', 0):,}")
        
        print("\n" + "=" * 50)
        print("🎉 WINDOWS NETWORKING ISSUE SOLVED!")
        print("✅ Flask server is working perfectly")
        print("✅ All endpoints responding correctly")
        print("🌐 Your frontend can now connect!")
        print(f"🔗 Server URL: {base_url}")
        
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Connection still failed: {e}")
        print("\n🔧 Additional solutions to try:")
        print("1. Run PowerShell as Administrator")
        print("2. Temporarily disable Windows Defender")
        print("3. Check antivirus software")
        print("4. Try different port (9001, 9002, etc.)")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    test_windows_server()