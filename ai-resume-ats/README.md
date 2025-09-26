# AI Resume ATS + PM Internship Recommendation Engine

A full-stack web application that analyzes resumes using ATS (Applicant Tracking System) algorithms and provides personalized Product Management internship recommendations.

## 🚀 Features

- **Resume Analysis**: Upload PDF/DOCX files and get ATS compatibility scores (0-100%)
- **Keyword Extraction**: AI-powered keyword analysis using spaCy NLP
- **Job Matching**: Real-time internship fetching from Adzuna API
- **Smart Recommendations**: TF-IDF and cosine similarity for job matching
- **Mobile-First Design**: Responsive UI built with React and TailwindCSS
- **Real-time Feedback**: Loading states, error handling, and progress indicators

## 🛠 Tech Stack

### Frontend
- **React 18** with Vite for fast development
- **TailwindCSS** for modern, responsive styling
- **Axios** for API communication
- **React Router** for navigation

### Backend
- **Flask** with Python 3.11
- **spaCy** for natural language processing
- **scikit-learn** for TF-IDF vectorization and similarity matching
- **PyPDF2** and **python-docx** for document parsing
- **Adzuna API** for job data
- **Flask-CORS** for cross-origin requests

## 📁 Project Structure

```
ai-resume-ats/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── requirements.txt       # Python dependencies
│   ├── .env.example          # Environment variables template
│   ├── Procfile              # Render deployment config
│   ├── runtime.txt           # Python version specification
│   └── render-build.sh       # Post-deployment setup script
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   │   ├── ResumeUpload.jsx
│   │   │   ├── CandidateForm.jsx
│   │   │   ├── ATSScore.jsx
│   │   │   ├── InternshipRecommendations.jsx
│   │   │   ├── LoadingSpinner.jsx
│   │   │   └── ErrorMessage.jsx
│   │   ├── services/
│   │   │   └── api.js         # API service functions
│   │   ├── App.jsx           # Main React component
│   │   ├── main.jsx          # React entry point
│   │   └── index.css         # Global styles with TailwindCSS
│   ├── package.json          # Node.js dependencies
│   ├── vite.config.js        # Vite configuration
│   ├── tailwind.config.js    # TailwindCSS configuration
│   ├── vercel.json           # Vercel deployment config
│   └── .env.example          # Frontend environment variables
└── README.md
```

## 🔧 Local Development Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- npm or yarn

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Download spaCy model**:
   ```bash
   python -m spacy download en_core_web_sm
   ```

5. **Setup environment variables**:
   ```bash
   copy .env.example .env  # Windows
   cp .env.example .env    # macOS/Linux
   ```
   
   Edit `.env` file and add your Adzuna API credentials:
   ```
   ADZUNA_APP_ID=your_app_id_here
   ADZUNA_APP_KEY=your_app_key_here
   FLASK_ENV=development
   FLASK_DEBUG=True
   ```

6. **Run the Flask server**:
   ```bash
   python app.py
   ```
   Server will run on `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Setup environment variables**:
   ```bash
   copy .env.example .env  # Windows
   cp .env.example .env    # macOS/Linux
   ```
   
   Edit `.env` file:
   ```
   VITE_API_URL=http://localhost:5000
   ```

4. **Run the development server**:
   ```bash
   npm run dev
   ```
   Frontend will run on `http://localhost:3000`

## 🌐 Getting Adzuna API Credentials

1. Visit [Adzuna Developer Portal](https://developer.adzuna.com/)
2. Sign up for a free developer account
3. Create a new application
4. Copy your `APP_ID` and `APP_KEY`
5. Add them to your `.env` file

**Note**: The application includes fallback dummy data if the Adzuna API is unavailable.

## 📱 How to Use

1. **Upload Resume**: Drag & drop or select a PDF/DOCX resume file
2. **Fill Information**: Enter your skills, education, and preferred location
3. **Analyze**: Click "Analyze Resume & Get Recommendations"
4. **View Results**: 
   - See your ATS compatibility score (0-100%)
   - Review missing keywords to improve your resume
   - Browse personalized PM internship recommendations
   - Click "Apply Now" to visit job listings

## 🚀 Deployment

### Backend Deployment (Render)

1. **Create a new Web Service on Render**
2. **Connect your GitHub repository**
3. **Configure build settings**:
   - **Build Command**: `./render-build.sh`
   - **Start Command**: `gunicorn app:app`
4. **Set environment variables**:
   - `ADZUNA_APP_ID`: Your Adzuna app ID
   - `ADZUNA_APP_KEY`: Your Adzuna app key
5. **Deploy**: Render will automatically build and deploy your app

### Frontend Deployment (Vercel)

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Deploy from frontend directory**:
   ```bash
   cd frontend
   vercel
   ```

3. **Set environment variable**:
   - `VITE_API_URL`: Your deployed backend URL (e.g., `https://your-app.onrender.com`)

4. **Alternative: Deploy via Vercel Dashboard**:
   - Import your GitHub repository
   - Set build settings:
     - **Framework Preset**: Vite
     - **Build Command**: `npm run build`
     - **Output Directory**: `dist`

## 🔍 API Endpoints

### Backend API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check endpoint |
| POST | `/recommend` | Main analysis endpoint |

### POST /recommend

**Request Format**: `multipart/form-data`

**Parameters**:
- `resume`: Resume file (PDF/DOCX)
- `skills`: Candidate skills (string)
- `education`: Educational background (string)
- `location`: Preferred location (string)

**Response Format**:
```json
{
  "ats_score": 72.5,
  "status": "Good chance",
  "missing_keywords": ["SQL", "Tableau", "Analytics"],
  "recommendations": [
    {
      "title": "Product Management Intern",
      "company": "TechCorp India",
      "location": "Bangalore, Karnataka",
      "match_percent": "85%",
      "apply_link": "https://example.com/job/123"
    }
  ]
}
```

## 🔧 Customization

### Adding New Job Sources
Modify `backend/app.py` in the `fetch_internships()` method to integrate additional job APIs.

### Extending ATS Analysis
Enhance the `calculate_ats_score()` method to include more sophisticated matching algorithms.

### UI Themes
Customize TailwindCSS colors in `frontend/tailwind.config.js` to match your brand.

## 🐛 Troubleshooting

### Common Issues

1. **spaCy Model Error**:
   ```bash
   python -m spacy download en_core_web_sm
   ```

2. **CORS Error**:
   - Ensure Flask-CORS is installed and configured
   - Check that frontend API URL matches backend URL

3. **File Upload Issues**:
   - Verify file size is under 10MB
   - Only PDF and DOCX files are supported

4. **API Timeout**:
   - Check Adzuna API credentials
   - Verify internet connection
   - Application will fall back to dummy data if API fails

### Development Tips

- Use browser dev tools to monitor API requests
- Check Flask console for backend errors
- Enable debug mode for detailed error messages
- Use `npm run build` to test production builds locally

## 📊 Performance Considerations

- **File Size Limits**: 10MB maximum for resume uploads
- **API Timeout**: 30-second timeout for job API requests
- **Caching**: Consider implementing Redis for production
- **Rate Limiting**: Implement rate limiting for production use

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🔗 Links

- **Live Demo**: [Deploy your own to see it in action]
- **Backend API**: [Your Render deployment URL]
- **Frontend**: [Your Vercel deployment URL]

---

**Built with ❤️ for helping students find perfect PM internships**