import React from 'react';

const CandidateForm = ({ formData, onChange, isLoading }) => {
  const handleInputChange = (field, value) => {
    onChange({ ...formData, [field]: value });
  };

  const locations = [
    'india',
    'bangalore',
    'mumbai',
    'delhi',
    'pune',
    'hyderabad',
    'chennai',
    'kolkata',
    'ahmedabad',
    'noida'
  ];

  return (
    <div className="card">
      <h2 className="text-xl font-semibold text-gray-800 mb-4">Candidate Information</h2>
      
      <div className="space-y-4">
        <div>
          <label htmlFor="skills" className="block text-sm font-medium text-gray-700 mb-2">
            Skills <span className="text-red-500">*</span>
          </label>
          <textarea
            id="skills"
            rows={3}
            placeholder="e.g., Product Management, Market Research, Data Analysis, SQL, Python, Agile, Scrum, JIRA"
            value={formData.skills}
            onChange={(e) => handleInputChange('skills', e.target.value)}
            className="input resize-none"
            disabled={isLoading}
            required
          />
          <p className="text-xs text-gray-500 mt-1">
            List your technical and soft skills relevant to Product Management
          </p>
        </div>

        <div>
          <label htmlFor="education" className="block text-sm font-medium text-gray-700 mb-2">
            Education <span className="text-red-500">*</span>
          </label>
          <textarea
            id="education"
            rows={2}
            placeholder="e.g., MBA Marketing, B.Tech Computer Science, Bachelor's in Business Administration"
            value={formData.education}
            onChange={(e) => handleInputChange('education', e.target.value)}
            className="input resize-none"
            disabled={isLoading}
            required
          />
          <p className="text-xs text-gray-500 mt-1">
            Include your degree, major, and university/institution
          </p>
        </div>

        <div>
          <label htmlFor="location" className="block text-sm font-medium text-gray-700 mb-2">
            Preferred Location
          </label>
          <select
            id="location"
            value={formData.location}
            onChange={(e) => handleInputChange('location', e.target.value)}
            className="input"
            disabled={isLoading}
          >
            {locations.map((location) => (
              <option key={location} value={location}>
                {location.charAt(0).toUpperCase() + location.slice(1)}
              </option>
            ))}
          </select>
          <p className="text-xs text-gray-500 mt-1">
            Select your preferred location for internships
          </p>
        </div>
      </div>
    </div>
  );
};

export default CandidateForm;