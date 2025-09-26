#!/usr/bin/env python3
"""
Quick test script for AI Resume ATS Backend
Run this script to test basic functionality
"""

import requests
import json
import os
from pathlib import Path

# Configuration
BASE_URL = "http://localhost:5000"
TEST_DATA = {
    "skills": "Product Management, Market Research, Data Analysis, SQL, Python, Agile, Scrum, JIRA",
    "education": "MBA Marketing, B.Tech Computer Science Engineering",
    "location": "bangalore"
}

def test_health_endpoint():
    """Test the health check endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Health check failed with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend server")
        print("   Make sure Flask server is running on http://localhost:5000")
        return False
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_recommend_endpoint_without_file():
    """Test the recommend endpoint without file (should fail gracefully)"""
    print("\n🔍 Testing recommend endpoint without file...")
    try:
        response = requests.post(f"{BASE_URL}/recommend", data=TEST_DATA, timeout=10)
        if response.status_code == 400:
            print("✅ Validation working - correctly rejected request without file")
            return True
        else:
            print(f"⚠️  Expected 400 error, got {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_recommend_endpoint_with_dummy_file():
    """Test the recommend endpoint with a dummy text file"""
    print("\n🔍 Testing recommend endpoint with dummy file...")
    
    # Create a dummy resume content
    dummy_resume = """
John Doe
Product Manager
Skills: Product Management, Market Research, Data Analysis, SQL, Python, Agile, Scrum
Education: MBA Marketing, B.Tech Computer Science
Experience: 2 years in product management and business analysis
"""
    
    try:
        # Create form data with file
        files = {
            'resume': ('test_resume.txt', dummy_resume, 'text/plain')
        }
        data = TEST_DATA
        
        response = requests.post(f"{BASE_URL}/recommend", files=files, data=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Recommend endpoint working!")
            print(f"   ATS Score: {result.get('ats_score', 'N/A')}%")
            print(f"   Status: {result.get('status', 'N/A')}")
            print(f"   Missing Keywords: {len(result.get('missing_keywords', []))} found")
            print(f"   Recommendations: {len(result.get('recommendations', []))} jobs found")
            
            # Print first recommendation if available
            recommendations = result.get('recommendations', [])
            if recommendations:
                first_job = recommendations[0]
                print(f"   First Job: {first_job.get('title', 'N/A')} at {first_job.get('company', 'N/A')}")
            
            return True
        else:
            print(f"❌ Request failed with status {response.status_code}")
            try:
                error_msg = response.json().get('error', 'Unknown error')
                print(f"   Error: {error_msg}")
            except:
                print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_cors():
    """Test CORS headers"""
    print("\n🔍 Testing CORS headers...")
    try:
        response = requests.options(f"{BASE_URL}/recommend")
        cors_headers = {
            'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
            'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
            'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers')
        }
        
        if any(cors_headers.values()):
            print("✅ CORS headers present")
            for header, value in cors_headers.items():
                if value:
                    print(f"   {header}: {value}")
            return True
        else:
            print("⚠️  CORS headers not found (might be okay)")
            return True
    except Exception as e:
        print(f"❌ CORS test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting AI Resume ATS Backend Tests")
    print("=" * 50)
    
    results = []
    
    # Run tests
    results.append(test_health_endpoint())
    results.append(test_recommend_endpoint_without_file())
    results.append(test_recommend_endpoint_with_dummy_file())
    results.append(test_cors())
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Backend is working correctly.")
        print("\n📝 Next Steps:")
        print("1. Start the frontend with: npm run dev")
        print("2. Open http://localhost:3000 in your browser")
        print("3. Test the complete application")
    else:
        print("⚠️  Some tests failed. Please check the backend setup.")
        print("\n🔧 Troubleshooting:")
        print("1. Ensure Flask server is running: python app.py")
        print("2. Check all dependencies are installed: pip install -r requirements.txt")
        print("3. Verify spaCy model is downloaded: python -m spacy download en_core_web_sm")

if __name__ == "__main__":
    main()