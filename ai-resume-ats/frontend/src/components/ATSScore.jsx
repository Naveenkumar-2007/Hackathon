import React from 'react';

const ATSScore = ({ score, status, missingKeywords }) => {
  const getScoreColor = (score) => {
    if (score >= 80) return 'text-success-600';
    if (score >= 60) return 'text-primary-600';
    if (score >= 40) return 'text-warning-600';
    return 'text-danger-600';
  };

  const getProgressBarColor = (score) => {
    if (score >= 80) return 'bg-success-500';
    if (score >= 60) return 'bg-primary-500';
    if (score >= 40) return 'bg-warning-500';
    return 'bg-danger-500';
  };

  const getProgressBarBg = (score) => {
    if (score >= 80) return 'bg-success-100';
    if (score >= 60) return 'bg-primary-100';
    if (score >= 40) return 'bg-warning-100';
    return 'bg-danger-100';
  };

  return (
    <div className="card">
      <h2 className="text-xl font-semibold text-gray-800 mb-4">ATS Score Analysis</h2>
      
      <div className="space-y-4">
        {/* Score Circle and Progress Bar */}
        <div className="flex items-center space-x-6">
          {/* Circular Score Display */}
          <div className="flex-shrink-0">
            <div className="relative w-20 h-20">
              <svg className="w-20 h-20 transform -rotate-90" viewBox="0 0 36 36">
                <path
                  className="text-gray-200"
                  stroke="currentColor"
                  strokeWidth="3"
                  fill="transparent"
                  d="M18 2.0845
                    a 15.9155 15.9155 0 0 1 0 31.831
                    a 15.9155 15.9155 0 0 1 0 -31.831"
                />
                <path
                  className={getScoreColor(score)}
                  stroke="currentColor"
                  strokeWidth="3"
                  strokeDasharray={`${score}, 100`}
                  strokeLinecap="round"
                  fill="transparent"
                  d="M18 2.0845
                    a 15.9155 15.9155 0 0 1 0 31.831
                    a 15.9155 15.9155 0 0 1 0 -31.831"
                />
              </svg>
              <div className="absolute inset-0 flex items-center justify-center">
                <span className={`text-lg font-bold ${getScoreColor(score)}`}>
                  {Math.round(score)}%
                </span>
              </div>
            </div>
          </div>

          {/* Progress Bar */}
          <div className="flex-grow">
            <div className="flex justify-between items-center mb-2">
              <span className="text-sm font-medium text-gray-700">ATS Compatibility</span>
              <span className={`text-sm font-semibold ${getScoreColor(score)}`}>
                {Math.round(score)}%
              </span>
            </div>
            <div className={`w-full ${getProgressBarBg(score)} rounded-full h-2.5`}>
              <div 
                className={`${getProgressBarColor(score)} h-2.5 rounded-full transition-all duration-1000 ease-out`}
                style={{ width: `${score}%` }}
              ></div>
            </div>
          </div>
        </div>

        {/* Status */}
        <div className="text-center">
          <p className={`text-lg font-semibold ${getScoreColor(score)}`}>
            {status}
          </p>
        </div>

        {/* Missing Keywords */}
        {missingKeywords && missingKeywords.length > 0 && (
          <div className="mt-4">
            <h3 className="text-sm font-medium text-gray-700 mb-2">
              Suggested Keywords to Improve Score:
            </h3>
            <div className="flex flex-wrap gap-2">
              {missingKeywords.slice(0, 8).map((keyword, index) => (
                <span
                  key={index}
                  className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-100 text-primary-800"
                >
                  {keyword}
                </span>
              ))}
            </div>
            {missingKeywords.length > 8 && (
              <p className="text-xs text-gray-500 mt-2">
                +{missingKeywords.length - 8} more keywords
              </p>
            )}
          </div>
        )}

        {/* Low Score Warning */}
        {score < 60 && (
          <div className="mt-4 p-3 bg-warning-50 border border-warning-200 rounded-md">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-warning-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <p className="text-sm text-warning-800">
                  <strong>Low ATS Score:</strong> Consider adding the suggested keywords to your resume to improve your chances of getting selected.
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ATSScore;