import React from 'react';

const InternshipRecommendations = ({ recommendations }) => {
  const getMatchColor = (matchPercent) => {
    const percent = parseInt(matchPercent.replace('%', ''));
    if (percent >= 80) return 'text-success-600 bg-success-100';
    if (percent >= 60) return 'text-primary-600 bg-primary-100';
    if (percent >= 40) return 'text-warning-600 bg-warning-100';
    return 'text-danger-600 bg-danger-100';
  };

  if (!recommendations || recommendations.length === 0) {
    return (
      <div className="card">
        <h2 className="text-xl font-semibold text-gray-800 mb-4">Internship Recommendations</h2>
        <div className="text-center py-8">
          <div className="text-gray-400 mb-4">
            <svg className="mx-auto h-12 w-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2-2v2m8 0V6a2 2 0 012 2v6.5" />
            </svg>
          </div>
          <p className="text-gray-500">No internship recommendations available</p>
        </div>
      </div>
    );
  }

  return (
    <div className="card">
      <h2 className="text-xl font-semibold text-gray-800 mb-4">
        Recommended PM Internships ({recommendations.length})
      </h2>
      
      <div className="space-y-4">
        {recommendations.map((job, index) => (
          <div
            key={index}
            className="bg-gray-50 rounded-lg p-4 border border-gray-200 hover:border-primary-300 transition-colors duration-200"
          >
            <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-3">
              <div className="flex-grow">
                <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-2">
                  <h3 className="text-lg font-semibold text-gray-900 mb-1 sm:mb-0">
                    {job.title}
                  </h3>
                  <div className={`inline-flex items-center px-2.5 py-1 rounded-full text-sm font-medium ${getMatchColor(job.match_percent)}`}>
                    <div className="w-2 h-2 rounded-full bg-current mr-1.5"></div>
                    {job.match_percent} Match
                  </div>
                </div>
                
                <div className="space-y-1 text-sm text-gray-600 mb-3">
                  <div className="flex items-center">
                    <svg className="h-4 w-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                    </svg>
                    {job.company}
                  </div>
                  <div className="flex items-center">
                    <svg className="h-4 w-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                    {job.location}
                  </div>
                </div>
              </div>
            </div>
            
            <div className="flex flex-col sm:flex-row gap-2 sm:justify-end">
              <a
                href={job.apply_link}
                target="_blank"
                rel="noopener noreferrer"
                className="btn-primary text-center inline-flex items-center justify-center"
              >
                <svg className="h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                </svg>
                Apply Now
              </a>
            </div>
          </div>
        ))}
      </div>
      
      <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
        <div className="flex items-start">
          <div className="flex-shrink-0">
            <svg className="h-5 w-5 text-blue-400" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
            </svg>
          </div>
          <div className="ml-3">
            <p className="text-sm text-blue-800">
              <strong>Pro Tip:</strong> These recommendations are ranked by compatibility with your resume. 
              Focus on roles with higher match percentages for better chances of success.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default InternshipRecommendations;