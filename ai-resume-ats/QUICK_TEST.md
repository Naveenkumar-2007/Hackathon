# 🧪 Quick Testing Checklist

## Before You Start
- [ ] Python 3.11+ installed
- [ ] Node.js 18+ installed
- [ ] Both PowerShell terminals open

## Backend Testing (First Terminal)

### Setup
```powershell
cd "C:\Users\navee\Cisco Packet Tracer 8.2.2\saves\certificates\genaihack\ai-resume-ats\backend"
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m spacy download en_core_web_sm
copy .env.example .env
```

### Start Backend
```powershell
python app.py
```
- [ ] Server starts without errors
- [ ] Shows "Running on http://127.0.0.1:5000"

### Quick Test (New Terminal)
```powershell
cd "C:\Users\navee\Cisco Packet Tracer 8.2.2\saves\certificates\genaihack\ai-resume-ats\test-files"
python test_backend.py
```
- [ ] Health check passes
- [ ] Validation test passes
- [ ] Recommend endpoint works
- [ ] CORS headers present

## Frontend Testing (Second Terminal)

### Setup
```powershell
cd "C:\Users\navee\Cisco Packet Tracer 8.2.2\saves\certificates\genaihack\ai-resume-ats\frontend"
npm install
copy .env.example .env
```

### Start Frontend
```powershell
npm run dev
```
- [ ] Vite server starts
- [ ] Shows "Local: http://localhost:3000/"

## Browser Testing

### Open Application
- [ ] Go to http://localhost:3000
- [ ] Page loads without errors
- [ ] UI looks clean and professional

### Test Upload
- [ ] Try dragging a file to upload area
- [ ] Try clicking to browse files
- [ ] Upload the sample resume (create a simple PDF/DOCX)

### Test Form
- [ ] Fill in skills: "Product Management, Data Analysis, SQL, Python"
- [ ] Fill in education: "MBA Marketing, B.Tech Computer Science"
- [ ] Select location: "bangalore"

### Test Analysis
- [ ] Click "Analyze Resume & Get Recommendations"
- [ ] Loading spinner appears
- [ ] Results appear within 30 seconds
- [ ] ATS score displayed (0-100%)
- [ ] Job recommendations shown
- [ ] "Apply Now" buttons work

### Test Error Handling
- [ ] Try submitting without file → Shows error
- [ ] Try uploading wrong file type → Shows error
- [ ] Try submitting empty form → Shows validation

### Test Responsive Design
- [ ] Resize browser to mobile size
- [ ] All elements still accessible
- [ ] Forms still usable on mobile

## ✅ Success Criteria

### Backend Working If:
- Flask server starts on port 5000
- Health endpoint returns {"status": "healthy"}
- Recommend endpoint accepts file uploads
- Returns JSON with ats_score and recommendations

### Frontend Working If:
- Vite server starts on port 3000
- Application loads in browser
- Can upload files and fill forms
- Can submit and get results
- Mobile responsive design works

### Integration Working If:
- Frontend successfully calls backend API
- File upload and analysis completes
- Results display correctly
- Error handling works properly

## 🐛 Common Issues & Fixes

**Backend won't start:**
```powershell
# Check Python version
python --version
# Reinstall dependencies
pip install -r requirements.txt
# Download spaCy model
python -m spacy download en_core_web_sm
```

**Frontend won't start:**
```powershell
# Clear cache and reinstall
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

**CORS errors:**
- Ensure backend is running first
- Check .env file has correct API URL
- Restart both servers

**File upload fails:**
- Check file size (max 10MB)
- Use PDF or DOCX format only
- Ensure backend has write permissions

## 🚀 Ready for Production?

If all tests pass:
1. Your application is working correctly!
2. You can now deploy to Render (backend) and Vercel (frontend)
3. Follow the deployment instructions in README.md

Need help? Check the full TESTING.md guide!