import React, { useState } from 'react';

const SearchDebug = () => {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const testSearch = async () => {
    setLoading(true);
    console.log('🔍 Testing search API...');
    
    try {
      const url = 'http://127.0.0.1:7000/search_jobs?keyword=product%20management%20intern&location=india';
      console.log('📡 Fetching:', url);
      
      const response = await fetch(url);
      console.log('📊 Response status:', response.status);
      
      const data = await response.json();
      console.log('✅ Response data:', data);
      
      setResult({
        success: true,
        status: response.status,
        jobCount: data.jobs?.length || 0,
        jobs: data.jobs || []
      });
    } catch (error) {
      console.error('❌ Error:', error);
      setResult({
        success: false,
        error: error.message
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 bg-white rounded-lg shadow-lg max-w-2xl mx-auto mt-8">
      <h2 className="text-xl font-bold mb-4">🔧 Search API Debug Tool</h2>
      
      <button
        onClick={testSearch}
        disabled={loading}
        className="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 disabled:opacity-50"
      >
        {loading ? 'Testing...' : 'Test Search API'}
      </button>

      {result && (
        <div className="mt-4 p-4 bg-gray-100 rounded-lg">
          <h3 className="font-semibold mb-2">Result:</h3>
          {result.success ? (
            <div>
              <p className="text-green-600">✅ API Call Successful!</p>
              <p>Status: {result.status}</p>
              <p>Jobs Found: {result.jobCount}</p>
              {result.jobs.length > 0 && (
                <div className="mt-2">
                  <p className="font-medium">Sample Job:</p>
                  <pre className="text-xs bg-white p-2 rounded mt-1 overflow-auto">
                    {JSON.stringify(result.jobs[0], null, 2)}
                  </pre>
                </div>
              )}
            </div>
          ) : (
            <div>
              <p className="text-red-600">❌ API Call Failed!</p>
              <p>Error: {result.error}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default SearchDebug;