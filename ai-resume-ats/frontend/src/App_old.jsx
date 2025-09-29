import React, { useState } from 'react';
import ResumeUpload from './components/ResumeUpload';
import CandidateForm from './components/CandidateForm';
import ATSScore from './components/ATSScore';
import InternshipRecommendations from './components/InternshipRecommendations';
import LoadingSpinner from './components/LoadingSpinner';
import ErrorMessage from './components/ErrorMessage';
import { submitResumeForAnalysis } from './services/api';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [formData, setFormData] = useState({
    skills: '',
    education: '',
    location: 'india'
  });
  const [results, setResults] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!selectedFile) {
      setError('Please upload your resume');
      return;
    }

    if (!formData.skills.trim() || !formData.education.trim()) {
      setError('Please fill in all required fields');
      return;
    }

    setIsLoading(true);
    setError(null);
    setResults(null);

    try {
      const submitData = new FormData();
      submitData.append('resume', selectedFile);
      submitData.append('skills', formData.skills);
      submitData.append('education', formData.education);
      submitData.append('location', formData.location);

      const response = await submitResumeForAnalysis(submitData);
      setResults(response);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    setFormData({
      skills: '',
      education: '',
      location: 'india'
    });
    setResults(null);
    setError(null);
  };

  const handleRetry = () => {
    setError(null);
    handleSubmit({ preventDefault: () => {} });
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                AI Resume ATS
              </h1>
              <p className="text-sm text-gray-600">
                PM Internship Recommendation Engine
              </p>
            </div>
            <div className="hidden sm:flex items-center space-x-2 text-sm text-gray-500">
              <div className="w-2 h-2 bg-green-500 rounded-full"></div>
              <span>Powered by AI</span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="space-y-8">
          
          {/* Introduction */}
          {!results && !isLoading && (
            <div className="text-center">
              <div className="max-w-3xl mx-auto">
                <h2 className="text-3xl font-bold text-gray-900 mb-4">
                  Get Your Resume ATS Score & Find Perfect PM Internships
                </h2>
                <p className="text-lg text-gray-600 mb-8">
                  Upload your resume and get instant ATS compatibility analysis plus personalized 
                  Product Management internship recommendations based on your skills and experience.
                </p>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                  <div className="text-center">
                    <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mx-auto mb-3">
                      <svg className="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                      </svg>
                    </div>
                    <h3 className="font-semibold text-gray-900 mb-1">Upload Resume</h3>
                    <p className="text-sm text-gray-600">PDF or DOCX format</p>
                  </div>
                  <div className="text-center">
                    <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mx-auto mb-3">
                      <svg className="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                      </svg>
                    </div>
                    <h3 className="font-semibold text-gray-900 mb-1">Get ATS Score</h3>
                    <p className="text-sm text-gray-600">0-100% compatibility</p>
                  </div>
                  <div className="text-center">
                    <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mx-auto mb-3">
                      <svg className="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2-2v2m8 0V6a2 2 0 012 2v6.5" />
                      </svg>
                    </div>
                    <h3 className="font-semibold text-gray-900 mb-1">Find Internships</h3>
                    <p className="text-sm text-gray-600">Top 5 matches</p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Form Section */}
          {!results && !isLoading && (
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <ResumeUpload
                  onFileSelect={setSelectedFile}
                  selectedFile={selectedFile}
                  isLoading={isLoading}
                />
                <CandidateForm
                  formData={formData}
                  onChange={setFormData}
                  isLoading={isLoading}
                />
              </div>
              
              <div className="text-center">
                <button
                  type="submit"
                  disabled={isLoading || !selectedFile || !formData.skills.trim() || !formData.education.trim()}
                  className="btn-primary px-8 py-3 text-lg disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Analyze Resume & Get Recommendations
                </button>
              </div>
            </form>
          )}

          {/* Loading State */}
          {isLoading && <LoadingSpinner />}

          {/* Error State */}
          {error && <ErrorMessage error={error} onRetry={handleRetry} />}

          {/* Results */}
          {results && !isLoading && (
            <div className="space-y-6">
              <div className="text-center">
                <h2 className="text-2xl font-bold text-gray-900 mb-2">Analysis Complete!</h2>
                <p className="text-gray-600">Here's your ATS score and personalized internship recommendations</p>
              </div>
              
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="lg:col-span-1">
                  <ATSScore
                    score={results.ats_score}
                    status={results.status}
                    missingKeywords={results.missing_keywords}
                  />
                </div>
                <div className="lg:col-span-2">
                  <InternshipRecommendations recommendations={results.recommendations} />
                </div>
              </div>
              
              <div className="text-center">
                <button
                  onClick={handleReset}
                  className="btn-secondary"
                >
                  Analyze Another Resume
                </button>
              </div>
            </div>
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center space-y-4">
            <div className="flex justify-center items-center space-x-4 text-sm text-gray-500">
              <span>Built with React + Flask</span>
              <span>•</span>
              <span>Powered by RapidAPI (Internships API)</span>
              <span>•</span>
              <span>AI-Driven Analysis</span>
            </div>
            <p className="text-xs text-gray-400">
              © 2024 AI Resume ATS. Helping students find the perfect PM internships.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;