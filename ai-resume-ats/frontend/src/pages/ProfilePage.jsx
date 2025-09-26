import React, { useState, useEffect } from 'react';

const ProfilePage = () => {
  const [isEditing, setIsEditing] = useState(false);
  const [profile, setProfile] = useState({
    name: '',
    email: '',
    phone: '',
    education: '',
    projects: [],
    experience: [],
    skills: [],
    profile_photo: '',
    location: '',
    bio: '',
    created_at: '',
    updated_at: ''
  });

  const [newProject, setNewProject] = useState({ title: '', description: '', tech: '' });
  const [newExperience, setNewExperience] = useState({ title: '', company: '', duration: '', description: '' });
  const [newSkill, setNewSkill] = useState('');

  // Load profile from localStorage on component mount
  useEffect(() => {
    const savedProfile = localStorage.getItem('userProfile');
    if (savedProfile) {
      const parsedProfile = JSON.parse(savedProfile);
      setProfile(parsedProfile);
    }
  }, []);

  // Save profile to localStorage
  const saveToLocalStorage = (profileData) => {
    localStorage.setItem('userProfile', JSON.stringify(profileData));
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setProfile(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleAddProject = () => {
    if (newProject.title && newProject.description) {
      const updatedProfile = {
        ...profile,
        projects: [...profile.projects, { ...newProject, id: Date.now() }]
      };
      setProfile(updatedProfile);
      setNewProject({ title: '', description: '', tech: '' });
    }
  };

  const handleRemoveProject = (id) => {
    const updatedProfile = {
      ...profile,
      projects: profile.projects.filter(project => project.id !== id)
    };
    setProfile(updatedProfile);
  };

  const handleAddExperience = () => {
    if (newExperience.title && newExperience.company) {
      const updatedProfile = {
        ...profile,
        experience: [...profile.experience, { ...newExperience, id: Date.now() }]
      };
      setProfile(updatedProfile);
      setNewExperience({ title: '', company: '', duration: '', description: '' });
    }
  };

  const handleRemoveExperience = (id) => {
    const updatedProfile = {
      ...profile,
      experience: profile.experience.filter(exp => exp.id !== id)
    };
    setProfile(updatedProfile);
  };

  const handleAddSkill = () => {
    if (newSkill && !profile.skills.includes(newSkill)) {
      const updatedProfile = {
        ...profile,
        skills: [...profile.skills, newSkill]
      };
      setProfile(updatedProfile);
      setNewSkill('');
    }
  };

  const handleRemoveSkill = (skillToRemove) => {
    const updatedProfile = {
      ...profile,
      skills: profile.skills.filter(skill => skill !== skillToRemove)
    };
    setProfile(updatedProfile);
  };

  const handleSaveProfile = () => {
    const updatedProfile = {
      ...profile,
      updated_at: new Date().toISOString(),
      created_at: profile.created_at || new Date().toISOString()
    };
    setProfile(updatedProfile);
    saveToLocalStorage(updatedProfile);
    setIsEditing(false);
    
    // Show success message
    alert('Profile saved successfully!');
  };

  const handlePhotoUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        setProfile(prev => ({
          ...prev,
          profile_photo: e.target.result
        }));
      };
      reader.readAsDataURL(file);
    }
  };

  if (!isEditing && (!profile.name || !profile.email)) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-white rounded-lg shadow-lg p-8 text-center">
            <div className="text-6xl mb-6">👤</div>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Create Your Profile</h2>
            <p className="text-gray-600 mb-8">
              Build your professional profile to get personalized internship recommendations
            </p>
            <button
              onClick={() => setIsEditing(true)}
              className="bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors duration-200"
            >
              Get Started
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">My Profile</h1>
          <div className="flex space-x-4">
            {isEditing ? (
              <>
                <button
                  onClick={handleSaveProfile}
                  className="bg-green-600 text-white px-6 py-2 rounded-lg font-semibold hover:bg-green-700 transition-colors duration-200"
                >
                  Save Profile
                </button>
                <button
                  onClick={() => setIsEditing(false)}
                  className="bg-gray-500 text-white px-6 py-2 rounded-lg font-semibold hover:bg-gray-600 transition-colors duration-200"
                >
                  Cancel
                </button>
              </>
            ) : (
              <button
                onClick={() => setIsEditing(true)}
                className="bg-blue-600 text-white px-6 py-2 rounded-lg font-semibold hover:bg-blue-700 transition-colors duration-200"
              >
                Edit Profile
              </button>
            )}
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Profile Card */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow-lg p-6 sticky top-8">
              <div className="text-center">
                <div className="relative inline-block">
                  {profile.profile_photo ? (
                    <img
                      src={profile.profile_photo}
                      alt="Profile"
                      className="w-32 h-32 rounded-full object-cover mx-auto mb-4"
                    />
                  ) : (
                    <div className="w-32 h-32 bg-gray-200 rounded-full flex items-center justify-center mx-auto mb-4">
                      <span className="text-4xl text-gray-400">👤</span>
                    </div>
                  )}
                  {isEditing && (
                    <label className="absolute bottom-0 right-0 bg-blue-600 text-white p-2 rounded-full cursor-pointer hover:bg-blue-700">
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
                      </svg>
                      <input
                        type="file"
                        accept="image/*"
                        onChange={handlePhotoUpload}
                        className="hidden"
                      />
                    </label>
                  )}
                </div>
                <h2 className="text-2xl font-bold text-gray-900">{profile.name || 'Your Name'}</h2>
                <p className="text-gray-600 mb-2">{profile.email || 'your.email@example.com'}</p>
                <p className="text-gray-600 mb-4">{profile.location || 'Location'}</p>
                {profile.bio && (
                  <p className="text-gray-700 text-sm leading-relaxed">{profile.bio}</p>
                )}
              </div>

              {/* Skills Preview */}
              {profile.skills.length > 0 && (
                <div className="mt-6">
                  <h3 className="font-semibold text-gray-900 mb-3">Skills</h3>
                  <div className="flex flex-wrap gap-2">
                    {profile.skills.slice(0, 6).map((skill, index) => (
                      <span
                        key={index}
                        className="bg-blue-100 text-blue-800 text-xs font-medium px-2.5 py-0.5 rounded"
                      >
                        {skill}
                      </span>
                    ))}
                    {profile.skills.length > 6 && (
                      <span className="text-gray-500 text-xs">+{profile.skills.length - 6} more</span>
                    )}
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Profile Form */}
          <div className="lg:col-span-2">
            <div className="space-y-6">
              {/* Basic Information */}
              <div className="bg-white rounded-lg shadow-lg p-6">
                <h3 className="text-xl font-bold text-gray-900 mb-6">Basic Information</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Name *</label>
                    <input
                      type="text"
                      name="name"
                      value={profile.name}
                      onChange={handleInputChange}
                      disabled={!isEditing}
                      className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-50"
                      placeholder="Your full name"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Email *</label>
                    <input
                      type="email"
                      name="email"
                      value={profile.email}
                      onChange={handleInputChange}
                      disabled={!isEditing}
                      className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-50"
                      placeholder="your.email@example.com"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Phone</label>
                    <input
                      type="tel"
                      name="phone"
                      value={profile.phone}
                      onChange={handleInputChange}
                      disabled={!isEditing}
                      className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-50"
                      placeholder="+91 9876543210"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Location</label>
                    <input
                      type="text"
                      name="location"
                      value={profile.location}
                      onChange={handleInputChange}
                      disabled={!isEditing}
                      className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-50"
                      placeholder="City, State, Country"
                    />
                  </div>
                </div>
                <div className="mt-6">
                  <label className="block text-sm font-medium text-gray-700 mb-2">Education</label>
                  <textarea
                    name="education"
                    value={profile.education}
                    onChange={handleInputChange}
                    disabled={!isEditing}
                    rows="3"
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-50"
                    placeholder="Your educational background (degree, university, year)"
                  />
                </div>
                <div className="mt-6">
                  <label className="block text-sm font-medium text-gray-700 mb-2">Bio</label>
                  <textarea
                    name="bio"
                    value={profile.bio}
                    onChange={handleInputChange}
                    disabled={!isEditing}
                    rows="3"
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-50"
                    placeholder="Tell us about yourself..."
                  />
                </div>
              </div>

              {/* Skills Section */}
              <div className="bg-white rounded-lg shadow-lg p-6">
                <h3 className="text-xl font-bold text-gray-900 mb-6">Skills</h3>
                {isEditing && (
                  <div className="flex gap-2 mb-4">
                    <input
                      type="text"
                      value={newSkill}
                      onChange={(e) => setNewSkill(e.target.value)}
                      className="flex-1 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="Add a skill"
                      onKeyPress={(e) => e.key === 'Enter' && handleAddSkill()}
                    />
                    <button
                      onClick={handleAddSkill}
                      className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
                    >
                      Add
                    </button>
                  </div>
                )}
                <div className="flex flex-wrap gap-2">
                  {profile.skills.map((skill, index) => (
                    <span
                      key={index}
                      className="bg-blue-100 text-blue-800 text-sm font-medium px-3 py-1 rounded-full flex items-center gap-2"
                    >
                      {skill}
                      {isEditing && (
                        <button
                          onClick={() => handleRemoveSkill(skill)}
                          className="text-blue-600 hover:text-blue-800"
                        >
                          ×
                        </button>
                      )}
                    </span>
                  ))}
                </div>
              </div>

              {/* Projects Section */}
              <div className="bg-white rounded-lg shadow-lg p-6">
                <h3 className="text-xl font-bold text-gray-900 mb-6">Projects</h3>
                {isEditing && (
                  <div className="mb-6 p-4 border border-gray-200 rounded-lg">
                    <h4 className="font-medium text-gray-900 mb-3">Add New Project</h4>
                    <div className="space-y-3">
                      <input
                        type="text"
                        value={newProject.title}
                        onChange={(e) => setNewProject({...newProject, title: e.target.value})}
                        className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        placeholder="Project title"
                      />
                      <textarea
                        value={newProject.description}
                        onChange={(e) => setNewProject({...newProject, description: e.target.value})}
                        className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        rows="3"
                        placeholder="Project description"
                      />
                      <input
                        type="text"
                        value={newProject.tech}
                        onChange={(e) => setNewProject({...newProject, tech: e.target.value})}
                        className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        placeholder="Technologies used (e.g., React, Python, etc.)"
                      />
                      <button
                        onClick={handleAddProject}
                        className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700"
                      >
                        Add Project
                      </button>
                    </div>
                  </div>
                )}
                <div className="space-y-4">
                  {profile.projects.map((project, index) => (
                    <div key={project.id || index} className="p-4 border border-gray-200 rounded-lg">
                      <div className="flex justify-between items-start">
                        <div className="flex-1">
                          <h4 className="font-semibold text-gray-900">{project.title}</h4>
                          <p className="text-gray-600 mt-1">{project.description}</p>
                          {project.tech && (
                            <p className="text-sm text-blue-600 mt-2">
                              <strong>Tech:</strong> {project.tech}
                            </p>
                          )}
                        </div>
                        {isEditing && (
                          <button
                            onClick={() => handleRemoveProject(project.id)}
                            className="text-red-600 hover:text-red-800 ml-4"
                          >
                            Remove
                          </button>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Experience Section */}
              <div className="bg-white rounded-lg shadow-lg p-6">
                <h3 className="text-xl font-bold text-gray-900 mb-6">Experience</h3>
                {isEditing && (
                  <div className="mb-6 p-4 border border-gray-200 rounded-lg">
                    <h4 className="font-medium text-gray-900 mb-3">Add New Experience</h4>
                    <div className="space-y-3">
                      <input
                        type="text"
                        value={newExperience.title}
                        onChange={(e) => setNewExperience({...newExperience, title: e.target.value})}
                        className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        placeholder="Job title / Role"
                      />
                      <input
                        type="text"
                        value={newExperience.company}
                        onChange={(e) => setNewExperience({...newExperience, company: e.target.value})}
                        className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        placeholder="Company name"
                      />
                      <input
                        type="text"
                        value={newExperience.duration}
                        onChange={(e) => setNewExperience({...newExperience, duration: e.target.value})}
                        className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        placeholder="Duration (e.g., Jun 2023 - Aug 2023)"
                      />
                      <textarea
                        value={newExperience.description}
                        onChange={(e) => setNewExperience({...newExperience, description: e.target.value})}
                        className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        rows="3"
                        placeholder="Job description and achievements"
                      />
                      <button
                        onClick={handleAddExperience}
                        className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700"
                      >
                        Add Experience
                      </button>
                    </div>
                  </div>
                )}
                <div className="space-y-4">
                  {profile.experience.map((exp, index) => (
                    <div key={exp.id || index} className="p-4 border border-gray-200 rounded-lg">
                      <div className="flex justify-between items-start">
                        <div className="flex-1">
                          <h4 className="font-semibold text-gray-900">{exp.title}</h4>
                          <p className="text-blue-600 font-medium">{exp.company}</p>
                          <p className="text-sm text-gray-500">{exp.duration}</p>
                          {exp.description && (
                            <p className="text-gray-600 mt-2">{exp.description}</p>
                          )}
                        </div>
                        {isEditing && (
                          <button
                            onClick={() => handleRemoveExperience(exp.id)}
                            className="text-red-600 hover:text-red-800 ml-4"
                          >
                            Remove
                          </button>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;