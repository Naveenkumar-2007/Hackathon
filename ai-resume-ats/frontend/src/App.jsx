import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navigation from './components/Navigation';
import SearchTest from './components/SearchTest';
import SimpleSearchPage from './pages/SimpleSearchPage';
import HomePage from './pages/HomePage';
import ProfilePage from './pages/ProfilePage';
import ATSCheckPage from './pages/ATSCheckPage';
import JobSearchPage from './pages/JobSearchPage';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Navigation />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/profile" element={<ProfilePage />} />
          <Route path="/ats-check" element={<ATSCheckPage />} />
          <Route path="/job-search" element={<JobSearchPage />} />
          <Route path="/simple" element={<SimpleSearchPage />} />
          <Route path="/test" element={<SearchTest />} />
        </Routes>
        
        {/* Footer */}
        <footer className="bg-gray-900 text-white py-12 mt-16">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
              {/* Brand */}
              <div className="col-span-1 md:col-span-2">
                <h3 className="text-2xl font-bold text-white mb-4">
                  🚀 AI Internship Engine
                </h3>
                <p className="text-gray-400 text-lg mb-4">
                  Revolutionizing PM internship search with AI-powered recommendations, 
                  ATS optimization, and personalized career guidance.
                </p>
                <div className="flex space-x-4 text-sm text-gray-400">
                  <span>✅ ATS Optimization</span>
                  <span>🎯 Smart Matching</span>
                  <span>📊 Real-time Analysis</span>
                </div>
              </div>

              {/* Features */}
              <div>
                <h4 className="text-lg font-semibold text-white mb-4">Features</h4>
                <ul className="space-y-2 text-gray-400">
                  <li>Profile Builder</li>
                  <li>Resume ATS Check</li>
                  <li>Job Search</li>
                  <li>AI Recommendations</li>
                  <li>Match Scoring</li>
                </ul>
              </div>

              {/* Support */}
              <div>
                <h4 className="text-lg font-semibold text-white mb-4">Support</h4>
                <ul className="space-y-2 text-gray-400">
                  <li>Help Center</li>
                  <li>Contact Us</li>
                  <li>Privacy Policy</li>
                  <li>Terms of Service</li>
                  <li>About</li>
                </ul>
              </div>
            </div>
            
            <div className="border-t border-gray-800 mt-8 pt-8 text-center">
              <p className="text-gray-400 mb-2">
                © 2025 AI-Based Internship Recommendation Engine. Built for PM Internship Success.
              </p>
              <p className="text-gray-500 text-sm mb-2">
                Developed by <span className="text-blue-400 font-semibold">Delta Force Team</span>
              </p>
              <p className="text-gray-500 text-sm">
                Facing any issues? 📧 Message us: <a href="mailto:naveenkumarchapala123@gmail.com" className="text-blue-400 hover:text-blue-300">naveenkumarchapala123@gmail.com</a>
              </p>
            </div>
          </div>
        </footer>
      </div>
    </Router>
  );
}

export default App;