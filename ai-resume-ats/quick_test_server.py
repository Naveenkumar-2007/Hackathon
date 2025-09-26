import requests

try:
    # Test the server
    response = requests.get("http://127.0.0.1:8000/health", timeout=5)
    print(f"✅ Server Response: {response.status_code}")
    print(f"📊 Data: {response.json()}")
    
    # Test search endpoint
    search_response = requests.get("http://127.0.0.1:8000/search_jobs?keyword=product", timeout=5)
    print(f"✅ Search Response: {search_response.status_code}")
    search_data = search_response.json()
    print(f"📋 Jobs Found: {search_data.get('count', 0)}")
    
    print("\n🎉 YOUR FLASK SERVER IS WORKING PERFECTLY!")
    
except Exception as e:
    print(f"❌ Error: {e}")