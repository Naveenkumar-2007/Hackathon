import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ATSCheckPage = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [formData, setFormData] = useState({
    skills: '',
    education: '',
    location: 'india',
    domain: ''
  });
  const [results, setResults] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const [profile, setProfile] = useState({});

  const API_BASE_URL = 'http://127.0.0.1:5002';

  // Load profile data from localStorage if available
  useEffect(() => {
    const savedProfile = localStorage.getItem('userProfile');
    if (savedProfile) {
      const profileData = JSON.parse(savedProfile);
      setProfile(profileData);
      setFormData({
        skills: Array.isArray(profileData.skills) ? profileData.skills.join(', ') : profileData.skills || '',
        education: profileData.education || '',
        location: profileData.location || 'india',
        domain: ''
      });
    }
  }, []);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      if (file.type === 'application/pdf' || 
          file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document') {
        setSelectedFile(file);
        setError(null);
      } else {
        setError('Please upload a PDF or DOCX file');
      }
    }
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (file.type === 'application/pdf' || 
          file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document') {
        setSelectedFile(file);
        setError(null);
      } else {
        setError('Please upload a PDF or DOCX file');
        setSelectedFile(null);
      }
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!selectedFile) {
      setError('Please upload your resume');
      return;
    }

    // Additional information is optional - no validation required

    setIsLoading(true);
    setError(null);
    setResults(null);

    try {
      const submitData = new FormData();
      submitData.append('resume', selectedFile);
      submitData.append('skills', formData.skills);
      submitData.append('education', formData.education);
      submitData.append('location', formData.location);
  submitData.append('domain', formData.domain);

      // Add profile data if available
      const savedProfile = localStorage.getItem('userProfile');
      if (savedProfile) {
        submitData.append('profile_data', savedProfile);
      }

      const response = await axios.post(`${API_BASE_URL}/recommend`, submitData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setResults(response.data);
    } catch (err) {
      console.error('Error submitting resume:', err);
      setError(err.response?.data?.error || 'An error occurred while analyzing your resume');
    } finally {
      setIsLoading(false);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-blue-600';
    if (score >= 40) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreBackground = (score) => {
    if (score >= 80) return 'bg-green-500';
    if (score >= 60) return 'bg-blue-500';
    if (score >= 40) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  const resetForm = () => {
    setSelectedFile(null);
    setResults(null);
    setError(null);
    document.getElementById('resume-upload').value = '';
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">
            📄 Resume ATS Score Check
            {profile.name && (
              <div className="text-lg font-normal text-blue-600 mt-2">
                Welcome back, {profile.name}! 👋
              </div>
            )}
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Upload your resume to get an AI-powered ATS compatibility score with personalized improvement suggestions and targeted internship recommendations
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Upload and Form Section */}
          <div className="space-y-6">
            {/* File Upload */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h2 className="text-xl font-bold text-gray-900 mb-4">Upload Your Resume</h2>
              
              <div
                className={`relative border-2 border-dashed rounded-lg p-8 text-center transition-colors duration-200 ${
                  dragActive 
                    ? 'border-blue-500 bg-blue-50' 
                    : selectedFile 
                      ? 'border-green-500 bg-green-50' 
                      : 'border-gray-300 hover:border-blue-400 hover:bg-gray-50'
                }`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
              >
                {selectedFile ? (
                  <div className="text-center">
                    <div className="text-4xl mb-4">✅</div>
                    <p className="text-lg font-semibold text-green-700 mb-2">
                      {selectedFile.name}
                    </p>
                    <p className="text-sm text-gray-600 mb-4">
                      File size: {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                    </p>
                    <button
                      onClick={resetForm}
                      className="text-blue-600 hover:text-blue-800 font-medium"
                    >
                      Upload Different File
                    </button>
                  </div>
                ) : (
                  <div>
                    <div className="text-4xl mb-4">📎</div>
                    <p className="text-lg font-semibold text-gray-700 mb-2">
                      Drop your resume here or click to browse
                    </p>
                    <p className="text-sm text-gray-500 mb-4">
                      Supports PDF and DOCX files (max 10MB)
                    </p>
                    <input
                      id="resume-upload"
                      type="file"
                      accept=".pdf,.docx"
                      onChange={handleFileChange}
                      className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                    />
                    <button className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors duration-200">
                      Choose File
                    </button>
                  </div>
                )}
              </div>
            </div>

            {/* Form */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h2 className="text-xl font-bold text-gray-900 mb-4">
                Additional Information 
                <span className="text-sm font-normal text-gray-500 ml-2">(Optional - helps improve recommendations)</span>
              </h2>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Skills <span className="text-gray-400">(Optional)</span>
                  </label>
                  <textarea
                    name="skills"
                    value={formData.skills}
                    onChange={handleInputChange}
                    rows="3"
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="e.g., Product Management, Agile, Scrum, Analytics, Market Research, Strategy"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Education <span className="text-gray-400">(Optional)</span>
                  </label>
                  <textarea
                    name="education"
                    value={formData.education}
                    onChange={handleInputChange}
                    rows="2"
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="e.g., MBA from IIM Bangalore (2024), B.Tech in Computer Science"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Preferred Location
                  </label>
                  <select
                    name="location"
                    value={formData.location}
                    onChange={handleInputChange}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value="india">India</option>
                    <option value="bangalore">Bangalore</option>
                    <option value="mumbai">Mumbai</option>
                    <option value="delhi">Delhi</option>
                    <option value="pune">Pune</option>
                    <option value="hyderabad">Hyderabad</option>
                    <option value="chennai">Chennai</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Internship Domain
                  </label>
                  <select
                    name="domain"
                    value={formData.domain}
                    onChange={handleInputChange}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value="">Select Domain (optional)</option>
                    <option value="product">Product</option>
                    <option value="data">Data</option>
                    <option value="marketing">Marketing</option>
                    <option value="design">Design</option>
                    <option value="engineering">Engineering</option>
                  </select>
                </div>

                <button
                  type="submit"
                  disabled={isLoading || !selectedFile}
                  className="w-full bg-blue-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-blue-700 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isLoading ? (
                    <div className="flex items-center justify-center">
                      <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                      Analyzing Resume...
                    </div>
                  ) : (
                    'Analyze Resume & Get Recommendations'
                  )}
                </button>
              </form>
            </div>
          </div>

          {/* Results Section */}
          <div className="space-y-6">
            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                <div className="flex items-center">
                  <div className="text-red-600 text-xl mr-3">❌</div>
                  <div>
                    <h3 className="text-red-800 font-semibold">Error</h3>
                    <p className="text-red-700">{error}</p>
                  </div>
                </div>
              </div>
            )}

            {isLoading && (
              <div className="bg-white rounded-lg shadow-lg p-8">
                <div className="text-center">
                  <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
                  <h3 className="text-lg font-medium text-gray-900 mb-2">Analyzing Your Resume</h3>
                  <p className="text-gray-600">Please wait while our AI analyzes your resume and finds the best internship matches...</p>
                </div>
              </div>
            )}

            {results && (
              <>
                {/* ATS Score */}
                <div className="bg-white rounded-lg shadow-lg p-6">
                  <h3 className="text-xl font-bold text-gray-900 mb-4">ATS Compatibility Score</h3>
                  <div className="text-center mb-6">
                    <div className="relative w-32 h-32 mx-auto mb-4">
                      <svg className="w-32 h-32 transform -rotate-90" viewBox="0 0 36 36">
                        <path
                          className="text-gray-200"
                          stroke="currentColor"
                          strokeWidth="3"
                          fill="none"
                          d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                        />
                        <path
                          className={getScoreColor(results.ats_score)}
                          stroke="currentColor"
                          strokeWidth="3"
                          fill="none"
                          strokeDasharray={`${results.ats_score}, 100`}
                          d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                        />
                      </svg>
                      <div className="absolute inset-0 flex items-center justify-center">
                        <span className={`text-3xl font-bold ${getScoreColor(results.ats_score)}`}>
                          {Math.round(results.ats_score)}%
                        </span>
                      </div>
                    </div>
                    <p className={`text-lg font-semibold ${getScoreColor(results.ats_score)}`}>
                      {results.status}
                    </p>
                  </div>

                  {/* Missing Keywords */}
                  {results.missing_keywords && results.missing_keywords.length > 0 && (
                    <div className="mb-4">
                      <h4 className="font-semibold text-gray-900 mb-3">💡 Suggested Keywords to Add:</h4>
                      <div className="flex flex-wrap gap-2">
                        {results.missing_keywords.slice(0, 8).map((keyword, index) => (
                          <span
                            key={index}
                            className="bg-yellow-100 text-yellow-800 text-xs font-medium px-2.5 py-1 rounded-full"
                          >
                            {keyword}
                          </span>
                        ))}
                      </div>
                      <p className="text-sm text-gray-600 mt-2">
                        Adding these keywords to your resume may improve your ATS score
                      </p>
                    </div>
                  )}
                </div>

                {/* Internship Recommendations */}
                {results.recommendations && results.recommendations.length > 0 && (
                  <div className="bg-white rounded-lg shadow-lg p-6">
                    <h3 className="text-xl font-bold text-gray-900 mb-4">
                      🎯 Personalized Internship Recommendations
                    </h3>
                    {results.effective_search_keyword && (
                      <p className="text-sm text-gray-500 mb-3">Search used: <span className="font-medium">{results.effective_search_keyword}</span></p>
                    )}
                    <div className="space-y-4">
                      {results.recommendations.slice(0, 5).map((job, index) => (
                        <div key={index} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow duration-200">
                          <div className="flex justify-between items-start mb-3">
                            <div className="flex-1">
                              <h4 className="font-semibold text-gray-900 text-lg mb-1">
                                {job.title}
                              </h4>
                              <p className="text-blue-600 font-medium">{job.company}</p>
                              <p className="text-gray-600 text-sm">{job.location}</p>
                            </div>
                            <div className="text-right">
                              <div className={`px-3 py-1 rounded-full text-sm font-semibold ${
                                parseInt(job.match_percent.replace('%', '')) >= 80 
                                  ? 'bg-green-100 text-green-800'
                                  : parseInt(job.match_percent.replace('%', '')) >= 60
                                    ? 'bg-blue-100 text-blue-800'
                                    : 'bg-yellow-100 text-yellow-800'
                              }`}>
                                {job.match_percent} Match
                              </div>
                            </div>
                          </div>
                          <div className="flex justify-end">
                            <a
                              href={job.apply_link}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors duration-200 inline-flex items-center"
                            >
                              Apply Now
                              <svg className="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                              </svg>
                            </a>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </>
            )}

            {/* Tips */}
            {!results && !isLoading && (
              <div className="bg-blue-50 rounded-lg p-6">
                <h3 className="text-lg font-semibold text-blue-900 mb-4">📊 ATS Score Tips</h3>
                <ul className="text-blue-800 space-y-2 text-sm">
                  <li>• Include keywords from job descriptions</li>
                  <li>• Use standard section headings (Experience, Education, Skills)</li>
                  <li>• Avoid images, tables, and complex formatting</li>
                  <li>• Use industry-specific terminology</li>
                  <li>• Keep formatting simple and clean</li>
                  <li>• Include quantifiable achievements</li>
                </ul>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ATSCheckPage;