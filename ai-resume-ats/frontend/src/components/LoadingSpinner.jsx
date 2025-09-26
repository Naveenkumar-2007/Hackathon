import React from 'react';

const LoadingSpinner = ({ message = "Analyzing your resume..." }) => {
  return (
    <div className="card text-center">
      <div className="flex flex-col items-center space-y-4">
        <div className="relative">
          <div className="w-16 h-16 border-4 border-primary-200 border-t-primary-600 rounded-full animate-spin"></div>
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="w-8 h-8 border-2 border-primary-300 border-t-transparent rounded-full animate-spin" style={{ animationDirection: 'reverse', animationDuration: '1s' }}></div>
          </div>
        </div>
        
        <div className="space-y-2">
          <h3 className="text-lg font-semibold text-gray-800">Processing Your Request</h3>
          <p className="text-gray-600">{message}</p>
        </div>
        
        <div className="w-full max-w-xs">
          <div className="bg-gray-200 rounded-full h-2 overflow-hidden">
            <div className="h-full bg-gradient-to-r from-primary-500 to-blue-600 rounded-full animate-pulse"></div>
          </div>
        </div>
        
        <div className="text-sm text-gray-500 space-y-1">
          <p>• Extracting resume content</p>
          <p>• Analyzing skills and keywords</p>
          <p>• Fetching relevant internships</p>
          <p>• Calculating ATS compatibility</p>
        </div>
      </div>
    </div>
  );
};

export default LoadingSpinner;