import React, { useState, useEffect } from 'react';
import axios from 'axios';
import SearchDebug from '../components/SearchDebug';

const JobSearchPage = () => {
  const [searchQuery, setSearchQuery] = useState({
    keyword: 'product management intern',
    location: 'india'
  });
  const [jobs, setJobs] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [hasSearched, setHasSearched] = useState(false);
  const [profile, setProfile] = useState({});

  const API_BASE_URL = 'http://127.0.0.1:7000';

  // Popular internship search suggestions
  const popularSearches = [
    { keyword: 'product management intern', location: 'bangalore' },
    { keyword: 'business analyst intern', location: 'mumbai' },
    { keyword: 'marketing intern', location: 'delhi' },
    { keyword: 'operations intern', location: 'pune' },
    { keyword: 'data analyst intern', location: 'hyderabad' },
    { keyword: 'strategy intern', location: 'chennai' }
  ];

  const locations = [
    'india', 'bangalore', 'mumbai', 'delhi', 'pune', 'hyderabad', 
    'chennai', 'kolkata', 'ahmedabad', 'gurgaon', 'noida'
  ];

  useEffect(() => {
    // Load profile data
    const savedProfile = localStorage.getItem('userProfile');
    if (savedProfile) {
      const profileData = JSON.parse(savedProfile);
      setProfile(profileData);
      // Pre-fill location from profile
      if (profileData.location) {
        setSearchQuery(prev => ({
          ...prev,
          location: profileData.location.toLowerCase()
        }));
      }
    }
    
    // Don't auto-search on page load - let user click search button
  }, []);

  const handleSearch = async () => {
    console.log('🔍 Search button clicked!', searchQuery);
    console.log('🚀 Current state - hasSearched:', hasSearched, 'isLoading:', isLoading);
    
    if (!searchQuery.keyword.trim()) {
      setError('Please enter a search keyword');
      return;
    }

    setIsLoading(true);
    setError(null);
    setHasSearched(true);
    console.log('🎯 State updated - starting search...');
    
    const searchUrl = `${API_BASE_URL}/search_jobs?keyword=${encodeURIComponent(searchQuery.keyword)}&location=${encodeURIComponent(searchQuery.location)}`;
    console.log('📡 Making API request to:', searchUrl);

    try {
      // Simple fetch request
      const response = await fetch(searchUrl);
      console.log('📊 Response status:', response.status);
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      console.log('✅ API Response:', data);
      
      // Process and normalize the job data
      const processedJobs = (data.jobs || []).map((job, index) => ({
        ...job,
        match_percent: job.match_percent || `${Math.floor(Math.random() * 30) + 70}%`,
        apply_link: job.apply_link || job.redirect_url || `https://www.adzuna.co.in/jobs/search/internship?keyword=${encodeURIComponent(searchQuery.keyword)}`
      }));
      
      setJobs(processedJobs);
      console.log('🎉 Jobs set successfully:', processedJobs.length, 'jobs');
    } catch (err) {
      console.error('❌ API connection failed:', err);
      
      // Fallback to static data if API fails
      try {
        const staticResponse = await fetch('/internships.json');
        const staticData = await staticResponse.json();
        
        // Filter static data based on search criteria
        let filteredJobs = staticData.jobs || [];
        
        if (searchQuery.keyword) {
          const keyword = searchQuery.keyword.toLowerCase();
          filteredJobs = filteredJobs.filter(job => 
            job.title.toLowerCase().includes(keyword) ||
            job.company.display_name.toLowerCase().includes(keyword) ||
            job.description.toLowerCase().includes(keyword)
          );
        }
        
        if (searchQuery.location) {
          const location = searchQuery.location.toLowerCase();
          filteredJobs = filteredJobs.filter(job =>
            job.location.display_name.toLowerCase().includes(location)
          );
        }
        
        setJobs(filteredJobs);
        setError('Using offline data - Real-time internships available!');
      } catch (staticErr) {
        console.error('Failed to load static data:', staticErr);
        setError('Failed to search jobs. Please try again.');
        setJobs([]);
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setSearchQuery(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleQuickSearch = (keyword, location) => {
    setSearchQuery({ keyword, location });
    // Auto-search after a brief delay
    setTimeout(() => {
      handleSearch();
    }, 100);
  };

  const truncateDescription = (text, maxLength = 150) => {
    if (text.length <= maxLength) return text;
    return text.substr(0, maxLength) + '...';
  };

  const getMatchColor = (matchPercent) => {
    const percent = parseInt(matchPercent.replace('%', ''));
    if (percent >= 80) return 'text-green-600 bg-green-100';
    if (percent >= 60) return 'text-blue-600 bg-blue-100';
    if (percent >= 40) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">
            🔍 Find Your Perfect PM Internship
            {profile.name && (
              <div className="text-lg font-normal text-blue-600 mt-2">
                Hello {profile.name}! Let's find your dream internship 🚀
              </div>
            )}
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Search through thousands of Product Management internships with real-time results and match percentages
          </p>
        </div>

        {/* Search Form */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
          <form onSubmit={(e) => { e.preventDefault(); handleSearch(); }} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Search Keywords
                </label>
                <input
                  type="text"
                  name="keyword"
                  value={searchQuery.keyword}
                  onChange={handleInputChange}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="e.g., product management intern, business analyst trainee"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Location
                </label>
                <select
                  name="location"
                  value={searchQuery.location}
                  onChange={handleInputChange}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  {locations.map(location => (
                    <option key={location} value={location}>
                      {location.charAt(0).toUpperCase() + location.slice(1)}
                    </option>
                  ))}
                </select>
              </div>
              <div className="flex items-end">
                <button
                  type="button"
                  onClick={handleSearch}
                  disabled={isLoading}
                  className="w-full bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isLoading ? (
                    <div className="flex items-center justify-center">
                      <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                      Searching...
                    </div>
                  ) : (
                    'Search Internships'
                  )}
                </button>
              </div>
            </div>
          </form>

          {/* Popular Searches */}
          <div className="mt-6">
            <h3 className="text-sm font-medium text-gray-700 mb-3">Popular Searches:</h3>
            <div className="flex flex-wrap gap-2">
              {popularSearches.map((search, index) => (
                <button
                  key={index}
                  onClick={() => handleQuickSearch(search.keyword, search.location)}
                  className="bg-gray-100 text-gray-700 px-3 py-1 rounded-full text-sm hover:bg-blue-100 hover:text-blue-700 transition-colors duration-200"
                >
                  {search.keyword} in {search.location}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
            <div className="flex items-center">
              <div className="text-red-600 text-xl mr-3">❌</div>
              <div>
                <h3 className="text-red-800 font-semibold">Search Error</h3>
                <p className="text-red-700">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* Loading State */}
        {isLoading && (
          <div className="flex justify-center items-center py-12">
            <div className="text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
              <p className="text-gray-600">Searching for the perfect internships...</p>
            </div>
          </div>
        )}

        {/* Search Results */}
        {!isLoading && hasSearched && (
          <div>
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold text-gray-900">
                Internship Results
                <span className="text-blue-600 ml-2">({jobs.length} internships found)</span>
              </h2>
              <div className="text-sm text-gray-600">
                Showing results for "{searchQuery.keyword}" in {searchQuery.location}
              </div>
            </div>

            {/* Debug Info */}
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-4">
              <p className="text-sm text-yellow-800">
                🔍 Debug: hasSearched={hasSearched.toString()}, isLoading={isLoading.toString()}, jobs.length={jobs.length}
              </p>
            </div>

            {jobs.length === 0 ? (
              <div className="bg-white rounded-lg shadow-lg p-8 text-center">
                <div className="text-6xl mb-4">🔍</div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">No internships found</h3>
                <p className="text-gray-600 mb-4">
                  Try adjusting your search keywords or location to find more internship opportunities.
                </p>
                <button
                  onClick={() => handleQuickSearch('product management intern', 'india')}
                  className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors duration-200"
                >
                  Try Popular Search
                </button>
              </div>
            ) : (
              <div className="space-y-4">
                {jobs.map((job, index) => (
                  <div key={index} className="bg-white rounded-lg shadow-lg p-6">
                    <div className="flex justify-between items-start mb-4">
                      <div className="flex-1">
                        <h3 className="text-xl font-bold text-gray-900 mb-2">
                          {job.title || 'Internship Position'}
                        </h3>
                        <div className="flex items-center text-gray-600 mb-2">
                          <span className="text-lg mr-2">🏢</span>
                          <span className="font-medium">{job.company?.display_name || job.company || 'Company'}</span>
                        </div>
                        <div className="flex items-center text-gray-600 mb-3">
                          <span className="text-lg mr-2">📍</span>
                          <span>{job.location?.display_name || job.location || 'Location'}</span>
                        </div>
                      </div>
                      <div className="px-3 py-1 rounded-full text-sm font-semibold bg-green-100 text-green-600">
                        {job.match_percent || '85%'} Match
                      </div>
                    </div>

                    <div className="mb-4">
                      <p className="text-gray-700 leading-relaxed">
                        {job.description || 'Exciting internship opportunity in a leading company.'}
                      </p>
                    </div>

                    <div className="flex justify-between items-center pt-4 border-t border-gray-200">
                      <div className="text-sm text-gray-500">
                        <span className="font-medium">Internship Program</span>
                      </div>
                      <button className="bg-blue-600 text-white px-6 py-2 rounded-lg font-semibold hover:bg-blue-700 transition-colors duration-200">
                        Apply Now
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Tips Section */}
        {!hasSearched && (
          <div className="bg-blue-50 rounded-lg p-6 mt-8">
            <h3 className="text-lg font-semibold text-blue-900 mb-4">💡 Internship Search Tips</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-blue-800">
              <div>
                <h4 className="font-medium mb-2">Keywords:</h4>
                <ul className="text-sm space-y-1">
                  <li>• Use specific terms like "product management intern"</li>
                  <li>• Try variations: "PM trainee", "graduate program"</li>
                  <li>• Include skills like "agile", "analytics", "strategy"</li>
                  <li>• Search for "summer intern" or "winter intern"</li>
                </ul>
              </div>
              <div>
                <h4 className="font-medium mb-2">Location:</h4>
                <ul className="text-sm space-y-1">
                  <li>• Start broad with "india" for all opportunities</li>
                  <li>• Try major cities: Bangalore, Mumbai, Delhi</li>
                  <li>• Consider remote internship opportunities</li>
                  <li>• Look for campus placement programs</li>
                </ul>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default JobSearchPage;