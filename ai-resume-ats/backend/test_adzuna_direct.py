#!/usr/bin/env python3
"""
Test Adzuna API directly to verify internship search functionality
"""

import os
import requests
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_adzuna_api():
    """Test Adzuna API with your credentials"""
    
    app_id = os.getenv('ADZUNA_APP_ID')
    app_key = os.getenv('ADZUNA_APP_KEY')
    
    print("🔍 Testing Adzuna API for Internship Opportunities")
    print("=" * 50)
    print(f"App ID: {app_id}")
    print(f"App Key: {app_key[:10]}...")
    print()
    
    if not app_id or not app_key:
        print("❌ API credentials not found in .env file")
        return False
    
    base_url = "https://api.adzuna.com/v1/api/jobs/in/search/1"
    
    # Test different search terms
    search_terms = [
        "internship",
        "graduate trainee", 
        "entry level",
        "product management intern",
        "business analyst intern"
    ]
    
    total_results = 0
    
    for term in search_terms:
        try:
            print(f"🔎 Searching for: '{term}'")
            
            params = {
                'app_id': app_id,
                'app_key': app_key,
                'results_per_page': 10,
                'what': term,
                'where': 'india',
                'sort_by': 'relevance'
            }
            
            response = requests.get(base_url, params=params, timeout=15)
            
            print(f"   Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                count = len(results)
                total_results += count
                
                print(f"   ✅ Found {count} results")
                
                # Show first 3 results
                for i, job in enumerate(results[:3]):
                    title = job.get('title', 'N/A')
                    company = job.get('company', {}).get('display_name', 'N/A')
                    location = job.get('location', {}).get('display_name', 'N/A')
                    print(f"      {i+1}. {title} at {company} - {location}")
                
            elif response.status_code == 429:
                print("   ⚠️ Rate limit hit, waiting...")
                time.sleep(3)
            else:
                print(f"   ❌ Error: {response.status_code}")
                print(f"   Response: {response.text[:200]}")
            
            print()
            time.sleep(1)  # Be nice to the API
            
        except Exception as e:
            print(f"   ❌ Exception: {e}")
            print()
    
    print("=" * 50)
    print(f"🎯 Total Results Found: {total_results}")
    
    if total_results > 0:
        print("✅ API is working! Your Flask app should show real internships now.")
        return True
    else:
        print("❌ No results found. Check API credentials or search terms.")
        return False

def test_specific_internship_search():
    """Test specific internship search that matches what the app does"""
    
    app_id = os.getenv('ADZUNA_APP_ID')
    app_key = os.getenv('ADZUNA_APP_KEY')
    
    print("\n🎯 Testing Specific Internship Search (Like Your App)")
    print("=" * 55)
    
    params = {
        'app_id': app_id,
        'app_key': app_key,
        'results_per_page': 20,
        'what': 'product management internship',
        'where': 'india',
        'sort_by': 'relevance'
    }
    
    try:
        response = requests.get("https://api.adzuna.com/v1/api/jobs/in/search/1", 
                              params=params, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            
            print(f"✅ Found {len(results)} results for 'product management internship'")
            
            # Filter for actual internships
            internships = []
            internship_keywords = ['intern', 'internship', 'trainee', 'graduate', 'entry level']
            
            for job in results:
                title = job.get('title', '').lower()
                description = job.get('description', '').lower()
                
                if any(kw in title or kw in description for kw in internship_keywords):
                    internships.append(job)
            
            print(f"📋 Filtered to {len(internships)} actual internships:")
            
            for i, job in enumerate(internships[:5]):
                title = job.get('title', 'N/A')
                company = job.get('company', {}).get('display_name', 'N/A')
                location = job.get('location', {}).get('display_name', 'N/A')
                salary = job.get('salary_min', 'N/A')
                print(f"   {i+1}. {title}")
                print(f"      Company: {company}")
                print(f"      Location: {location}")
                print(f"      Salary: {salary}")
                print()
            
            return len(internships) > 0
            
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

if __name__ == "__main__":
    success1 = test_adzuna_api()
    success2 = test_specific_internship_search()
    
    if success1 or success2:
        print("\n🎉 API TEST SUCCESSFUL!")
        print("Your Flask app should now show real internship opportunities.")
        print("\nNext steps:")
        print("1. Start your Flask backend: python app.py")
        print("2. Start your React frontend: npm run dev") 
        print("3. Search for internships in the web app")
    else:
        print("\n❌ API TEST FAILED!")
        print("Check your API credentials in the .env file")