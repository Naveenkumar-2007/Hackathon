import React, { useState } from 'react';

const SimpleSearchPage = () => {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [keyword, setKeyword] = useState('product');
  const [location, setLocation] = useState('india');

  const searchJobs = async () => {
    console.log('🚀 Starting search...', { keyword, location });
    setLoading(true);
    setError('');
    
    try {
      const url = `http://127.0.0.1:7000/search_jobs?keyword=${keyword}&location=${location}`;
      console.log('🌐 Fetching:', url);
      
      const response = await fetch(url);
      console.log('📡 Response status:', response.status);
      
      const data = await response.json();
      console.log('✅ Data received:', data);
      
      setJobs(data.jobs || []);
      
    } catch (err) {
      console.error('❌ Error:', err);
      setError('Failed to fetch jobs: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>🔍 Simple Job Search Test</h1>
      
      <div style={{ marginBottom: '20px' }}>
        <input
          type="text"
          value={keyword}
          onChange={(e) => setKeyword(e.target.value)}
          placeholder="Keyword"
          style={{ padding: '10px', marginRight: '10px', border: '1px solid #ccc', borderRadius: '4px' }}
        />
        <input
          type="text"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
          placeholder="Location"
          style={{ padding: '10px', marginRight: '10px', border: '1px solid #ccc', borderRadius: '4px' }}
        />
        <button
          onClick={searchJobs}
          disabled={loading}
          style={{
            padding: '10px 20px',
            backgroundColor: loading ? '#ccc' : '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: loading ? 'not-allowed' : 'pointer'
          }}
        >
          {loading ? 'Searching...' : 'Search Jobs'}
        </button>
      </div>

      {error && (
        <div style={{ color: 'red', marginBottom: '20px' }}>
          {error}
        </div>
      )}

      <div>
        <h2>Results: {jobs.length} jobs found</h2>
        {jobs.map((job, index) => (
          <div key={index} style={{ 
            border: '1px solid #ddd', 
            padding: '15px', 
            margin: '10px 0', 
            borderRadius: '5px',
            backgroundColor: '#f9f9f9'
          }}>
            <h3 style={{ color: '#007bff' }}>{job.title}</h3>
            <p><strong>Company:</strong> {job.company?.display_name || 'N/A'}</p>
            <p><strong>Location:</strong> {job.location?.display_name || 'N/A'}</p>
            <p><strong>Description:</strong> {job.description?.substring(0, 200)}...</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SimpleSearchPage;