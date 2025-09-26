# Testing Guide for AI Resume ATS Application

## 🧪 Complete Testing Instructions

### Prerequisites
- Python 3.11+ installed
- Node.js 18+ installed
- Git (optional, for cloning)

## Step 1: Backend Testing

### 1.1 Setup Backend Environment

Open PowerShell and navigate to the backend directory:
```powershell
cd "C:\Users\navee\Cisco Packet Tracer 8.2.2\saves\certificates\genaihack\ai-resume-ats\backend"
```

Create and activate virtual environment:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If you get execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
```

Install dependencies:
```powershell
pip install -r requirements.txt
```

Download spaCy model:
```powershell
python -m spacy download en_core_web_sm
```

### 1.2 Configure Environment Variables

Create `.env` file from example:
```powershell
copy .env.example .env
```

Edit the `.env` file and add your Adzuna API credentials:
```
ADZUNA_APP_ID=your_app_id_here
ADZUNA_APP_KEY=your_app_key_here
FLASK_ENV=development
FLASK_DEBUG=True
```

**Note**: If you don't have Adzuna API credentials yet, the app will use dummy data for testing.

### 1.3 Run Backend Server

Start the Flask server:
```powershell
python app.py
```

You should see:
```
* Running on http://127.0.0.1:5000
* Debug mode: on
```

### 1.4 Test Backend API

Open a new PowerShell window and test the health endpoint:
```powershell
curl http://localhost:5000/health
```

Expected response:
```json
{"status": "healthy", "message": "AI Resume ATS API is running"}
```

## Step 2: Frontend Testing

### 2.1 Setup Frontend Environment

Open a new PowerShell window and navigate to frontend:
```powershell
cd "C:\Users\navee\Cisco Packet Tracer 8.2.2\saves\certificates\genaihack\ai-resume-ats\frontend"
```

Install dependencies:
```powershell
npm install
```

Create environment file:
```powershell
copy .env.example .env
```

The `.env` file should contain:
```
VITE_API_URL=http://localhost:5000
```

### 2.2 Run Frontend Server

Start the Vite development server:
```powershell
npm run dev
```

You should see:
```
  Local:   http://localhost:3000/
  Network: use --host to expose
```

## Step 3: End-to-End Testing

### 3.1 Open the Application

1. Open your browser and go to `http://localhost:3000`
2. You should see the AI Resume ATS homepage

### 3.2 Test with Sample Resume

I'll create a sample resume for testing:

### 3.3 Testing Scenarios

#### Scenario 1: Basic Functionality Test
1. **Upload Resume**: Use the sample resume file
2. **Fill Form**: 
   - Skills: "Product Management, Market Research, Data Analysis, SQL, Python, Agile, Scrum"
   - Education: "MBA Marketing, B.Tech Computer Science"
   - Location: "bangalore"
3. **Submit**: Click "Analyze Resume & Get Recommendations"
4. **Verify Results**: Should show ATS score and internship recommendations

#### Scenario 2: Error Handling Test
1. Try uploading without a file - should show error
2. Try uploading a text file - should show format error
3. Try submitting without skills - should show validation error

#### Scenario 3: Different File Formats
1. Test with PDF resume
2. Test with DOCX resume
3. Test with large file (should handle up to 10MB)

#### Scenario 4: Mobile Responsiveness
1. Resize browser window to mobile size
2. Test all functionality on mobile view
3. Verify responsive design works properly

## Step 4: API Testing with Postman/curl

### Test Resume Analysis Endpoint

Create a test request:
```powershell
# Test with curl (if available)
curl -X POST http://localhost:5000/recommend `
  -F "resume=@sample_resume.pdf" `
  -F "skills=Product Management, Data Analysis, SQL" `
  -F "education=MBA Marketing" `
  -F "location=bangalore"
```

## Step 5: Browser Developer Tools Testing

1. **Open Developer Tools** (F12)
2. **Network Tab**: Monitor API requests
3. **Console Tab**: Check for JavaScript errors
4. **Application Tab**: Check for any storage issues

## Common Issues and Solutions

### Backend Issues

**Issue**: `ModuleNotFoundError: No module named 'spacy'`
**Solution**: 
```powershell
pip install spacy
python -m spacy download en_core_web_sm
```

**Issue**: `CORS error`
**Solution**: Ensure Flask-CORS is installed and backend is running

**Issue**: `Adzuna API error`
**Solution**: Check API credentials or use dummy data fallback

### Frontend Issues

**Issue**: `Cannot connect to backend`
**Solution**: 
1. Ensure backend is running on port 5000
2. Check VITE_API_URL in .env file
3. Verify no firewall blocking

**Issue**: `npm install fails`
**Solution**: 
```powershell
npm cache clean --force
npm install
```

**Issue**: `Tailwind styles not working`
**Solution**: Restart the dev server after installing

## Performance Testing

### Load Testing
1. Upload multiple files simultaneously
2. Test with large resume files (up to 10MB)
3. Monitor response times

### Browser Compatibility
Test on:
- Chrome (latest)
- Firefox (latest)
- Edge (latest)
- Safari (if available)

## Automated Testing (Optional)

For more advanced testing, you can add:

### Backend Unit Tests
```python
# test_app.py
import pytest
from app import app

def test_health_endpoint():
    with app.test_client() as client:
        response = client.get('/health')
        assert response.status_code == 200
```

### Frontend Testing
```javascript
// Add to package.json
"scripts": {
  "test": "vitest"
}
```

## Success Criteria

✅ **Backend Tests Pass**:
- Health endpoint returns 200
- Resume upload works
- ATS analysis completes
- Job recommendations returned

✅ **Frontend Tests Pass**:
- Application loads without errors
- File upload interface works
- Form validation works
- Results display correctly
- Mobile responsive design works

✅ **Integration Tests Pass**:
- Frontend successfully calls backend API
- Error handling works properly
- Loading states display correctly
- Complete user flow works end-to-end

## Next Steps After Testing

1. **Fix any issues** found during testing
2. **Optimize performance** if needed
3. **Deploy to production** (Render + Vercel)
4. **Set up monitoring** for production environment

Need help with any specific testing scenario or encountering issues? Let me know!