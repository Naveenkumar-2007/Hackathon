# 🚀 AI Resume ATS - Internship Search Platform

A comprehensive AI-powered Resume Application Tracking System (ATS) with real-time internship search capabilities.

## ✨ Features

- **🔍 Real-time Internship Search** - Search thousands of internships using Adzuna API
- **📄 ATS Resume Analysis** - AI-powered resume scoring and optimization
- **👤 Profile Management** - User profile creation and management
- **🎯 Job Matching** - Intelligent job-resume matching with percentage scores
- **📊 Interactive Dashboard** - Clean, modern UI built with React and Tailwind CSS

## 🛠️ Tech Stack

### Frontend
- **React 18** - Modern React with Hooks
- **Vite** - Fast build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **React Router** - Client-side routing
- **Axios** - HTTP client for API calls

### Backend
- **Python Flask** - Lightweight web framework
- **Adzuna API** - Real job data integration
- **scikit-learn** - ML for resume analysis
- **spaCy** - Natural language processing
- **PyPDF2** - PDF text extraction
- **python-docx** - Word document processing

## 🚀 Quick Start

### Prerequisites
- Node.js (v14 or higher)
- Python (v3.8 or higher)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Naveenkumar-2007/Hackathon.git
   cd Hackathon
   ```

2. **Backend Setup**
   ```bash
   cd ai-resume-ats/backend
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your API credentials
   python app.py
   ```

3. **Frontend Setup**
   ```bash
   cd ../frontend
   npm install
   npm run dev
   ```

4. **Access the Application**
   - Frontend: http://localhost:3003
   - Backend API: http://localhost:7000

## 🔧 Configuration

### Environment Variables

Create `.env` files in the backend directory:

```env
# Adzuna API credentials (get from https://developer.adzuna.com/)
ADZUNA_APP_ID=your_app_id
ADZUNA_APP_KEY=your_app_key

# Flask configuration
FLASK_ENV=development
FLASK_DEBUG=True
```

## 📖 API Documentation

### Endpoints

- `GET /health` - Health check
- `GET /search_jobs` - Search internships
- `POST /analyze_resume` - Analyze resume against job description
- `POST /upload_resume` - Upload and parse resume

### Example Usage

```javascript
// Search for internships
fetch('http://localhost:7000/search_jobs?keyword=product%20management&location=india')
  .then(response => response.json())
  .then(data => console.log(data.jobs));
```

## 🎯 Features Overview

### 1. Internship Search
- Real-time search using Adzuna API
- Filter by keywords, location, and salary
- Popular search suggestions
- Detailed job information with apply links

### 2. Resume ATS Analysis
- Upload PDF/DOCX resumes
- AI-powered content analysis
- Keyword matching and scoring
- Improvement suggestions

### 3. Profile Management
- User profile creation
- Skills and experience tracking
- Personalized job recommendations

## 📁 Project Structure

```
ai-resume-ats/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── simple_api.py       # Simple HTTP API server
│   ├── requirements.txt    # Python dependencies
│   └── .env.example       # Environment variables template
├── frontend/
│   ├── src/
│   │   ├── components/    # Reusable React components
│   │   ├── pages/         # Main page components
│   │   ├── App.jsx        # Main App component
│   │   └── main.jsx       # Entry point
│   ├── package.json       # Node.js dependencies
│   └── vite.config.js     # Vite configuration
└── README.md
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Naveen Kumar**
- GitHub: [@Naveenkumar-2007](https://github.com/Naveenkumar-2007)

## 🙏 Acknowledgments

- Adzuna API for providing job data
- React and Flask communities
- Open source contributors

## 📊 Screenshots

### Homepage
![Homepage](./screenshots/homepage.png)

### Job Search
![Job Search](./screenshots/job-search.png)

### Resume Analysis
![Resume Analysis](./screenshots/resume-analysis.png)

---

⭐ **Star this repository if it helped you!**