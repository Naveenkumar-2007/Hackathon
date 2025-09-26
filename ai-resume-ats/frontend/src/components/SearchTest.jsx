import React, { useState } from 'react';

const SearchTest = () => {
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);

  const testDirectFetch = async () => {
    setLoading(true);
    setResult('Testing...');
    
    try {
      const url = 'http://127.0.0.1:7000/search_jobs?keyword=product&location=india';
      console.log('Testing URL:', url);
      
      const response = await fetch(url);
      const data = await response.json();
      
      setResult(`✅ Success! Found ${data.jobs?.length || 0} jobs`);
      console.log('Success:', data);
    } catch (error) {
      setResult(`❌ Error: ${error.message}`);
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-8 max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">🧪 Search API Test</h1>
      <button 
        onClick={testDirectFetch}
        disabled={loading}
        className={`px-6 py-3 rounded-lg font-semibold text-white transition-colors ${
          loading 
            ? 'bg-gray-400 cursor-not-allowed' 
            : 'bg-blue-600 hover:bg-blue-700 cursor-pointer'
        }`}
      >
        {loading ? 'Testing...' : 'Test Search API'}
      </button>
      <div className="mt-6 p-4 bg-gray-100 rounded-lg">
        <strong className="text-gray-700">Result:</strong>
        <div className="mt-2 text-gray-800">{result}</div>
      </div>
    </div>
  );
};

export default SearchTest;