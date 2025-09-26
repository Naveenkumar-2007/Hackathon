import requests
import time

print("Testing Flask server locally...")

# Wait a moment
time.sleep(2)

try:
    response = requests.get("http://127.0.0.1:5000/health", timeout=5)
    print(f"✅ Health endpoint works! Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"❌ Error: {e}")

try:
    response = requests.get("http://127.0.0.1:5000/search_jobs?keyword=product+management&location=india", timeout=10)
    print(f"✅ Search endpoint works! Status: {response.status_code}")
    data = response.json()
    print(f"Found {len(data.get('jobs', []))} jobs")
except Exception as e:
    print(f"❌ Search error: {e}")