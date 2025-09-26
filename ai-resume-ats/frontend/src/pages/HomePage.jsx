import React from 'react';
import { Link } from 'react-router-dom';

const HomePage = () => {
  const features = [
    {
      icon: '👤',
      title: 'Build Your Profile',
      description: 'Create a comprehensive professional profile similar to LinkedIn with your education, skills, projects, and experience.',
      link: '/profile',
      buttonText: 'Create Profile',
      color: 'blue'
    },
    {
      icon: '📄',
      title: 'Resume ATS Score Check',
      description: 'Upload your resume and get an AI-powered ATS score with personalized improvement suggestions and missing keywords.',
      link: '/ats-check',
      buttonText: 'Check ATS Score',
      color: 'green'
    },
    {
      icon: '🔍',
      title: 'Internship Search',
      description: 'Search for PM internships using keywords and location. Get real-time results from top job boards with match percentages.',
      link: '/job-search',
      buttonText: 'Search Internships',
      color: 'purple'
    },
    {
      icon: '🎯',
      title: 'Personalized Recommendations',
      description: 'Get AI-powered internship recommendations based on your profile, resume, and career preferences.',
      link: '/ats-check',
      buttonText: 'Get Recommendations',
      color: 'orange'
    }
  ];

  const getColorClasses = (color) => {
    const colorMap = {
      blue: 'bg-blue-50 text-blue-600 border-blue-200 hover:bg-blue-100',
      green: 'bg-green-50 text-green-600 border-green-200 hover:bg-green-100',
      purple: 'bg-purple-50 text-purple-600 border-purple-200 hover:bg-purple-100',
      orange: 'bg-orange-50 text-orange-600 border-orange-200 hover:bg-orange-100'
    };
    return colorMap[color] || colorMap.blue;
  };

  const getButtonClasses = (color) => {
    const buttonMap = {
      blue: 'bg-blue-600 hover:bg-blue-700 text-white',
      green: 'bg-green-600 hover:bg-green-700 text-white',
      purple: 'bg-purple-600 hover:bg-purple-700 text-white',
      orange: 'bg-orange-600 hover:bg-orange-700 text-white'
    };
    return buttonMap[color] || buttonMap.blue;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <div className="text-center">
            <h1 className="text-4xl sm:text-5xl md:text-6xl font-bold text-gray-900 mb-6">
              <span className="block">AI-Based Internship</span>
              <span className="block text-blue-600">Recommendation Engine</span>
              <span className="block text-lg sm:text-xl md:text-2xl font-normal text-gray-600 mt-4">
                for PM Internship Scheme
              </span>
            </h1>
            <p className="max-w-3xl mx-auto text-xl text-gray-600 mb-8">
              Revolutionize your internship search with AI-powered recommendations, 
              ATS score analysis, and personalized career guidance designed specifically 
              for Product Management roles.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <Link
                to="/profile"
                className="bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors duration-200 shadow-lg hover:shadow-xl"
              >
                🚀 Get Started
              </Link>
              <Link
                to="/ats-check"
                className="bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold border-2 border-blue-600 hover:bg-blue-50 transition-colors duration-200"
              >
                📊 Quick ATS Check
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center mb-12">
          <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">
            Powerful Features for Your Success
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Everything you need to land your dream PM internship, powered by cutting-edge AI technology
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature, index) => (
            <div
              key={index}
              className={`p-6 rounded-xl border-2 transition-all duration-300 hover:shadow-lg hover:scale-105 ${getColorClasses(feature.color)}`}
            >
              <div className="text-4xl mb-4 text-center">{feature.icon}</div>
              <h3 className="text-xl font-bold mb-3 text-center">{feature.title}</h3>
              <p className="text-gray-700 mb-6 text-center leading-relaxed">
                {feature.description}
              </p>
              <div className="text-center">
                <Link
                  to={feature.link}
                  className={`inline-block px-6 py-2 rounded-lg font-semibold transition-colors duration-200 ${getButtonClasses(feature.color)}`}
                >
                  {feature.buttonText}
                </Link>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Stats Section */}
      <div className="bg-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
            <div className="p-6">
              <div className="text-4xl font-bold text-blue-600 mb-2">95%</div>
              <div className="text-xl font-semibold text-gray-900 mb-2">ATS Compatibility</div>
              <div className="text-gray-600">Our AI ensures your resume passes through ATS systems</div>
            </div>
            <div className="p-6">
              <div className="text-4xl font-bold text-green-600 mb-2">1000+</div>
              <div className="text-xl font-semibold text-gray-900 mb-2">Active Internships</div>
              <div className="text-gray-600">Real-time access to PM internship opportunities</div>
            </div>
            <div className="p-6">
              <div className="text-4xl font-bold text-purple-600 mb-2">85%</div>
              <div className="text-xl font-semibold text-gray-900 mb-2">Match Accuracy</div>
              <div className="text-gray-600">Personalized recommendations based on your profile</div>
            </div>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-gradient-to-r from-blue-600 to-indigo-700 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
            Ready to Launch Your PM Career?
          </h2>
          <p className="text-xl text-blue-100 mb-8 max-w-2xl mx-auto">
            Join thousands of students who have successfully landed their dream PM internships with our AI-powered platform.
          </p>
          <Link
            to="/profile"
            className="bg-white text-blue-600 px-8 py-4 rounded-lg font-bold text-lg hover:bg-gray-100 transition-colors duration-200 shadow-lg hover:shadow-xl inline-block"
          >
            Start Your Journey Today 🚀
          </Link>
        </div>
      </div>
    </div>
  );
};

export default HomePage;