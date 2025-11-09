# 🚀 How to Run the UMass Housing Recommender

## Quick Start Guide

### Prerequisites
- Python 3.x installed
- Node.js and npm installed
- Backend dependencies installed
- Frontend dependencies installed

---

## Step 1: Start the Backend Server (Terminal 1)

Open a terminal window and run:

```bash
cd /Users/abhijay/Downloads/hackUmass-main/backend
python3 main.py
```

**Expected Output:**
```
🚀 Starting UMass Housing Recommender Backend
📡 Server running on: http://0.0.0.0:8000
📝 API Documentation: http://0.0.0.0:8000/docs
🔑 Using Gemini API: ✅ Configured
```

**⚠️ Keep this terminal open!** The backend must stay running.

---

## Step 2: Start the Frontend Server (Terminal 2)

Open a **NEW** terminal window and run:

```bash
cd /Users/abhijay/Downloads/hackUmass-main
npm run dev
```

**Expected Output:**
```
✓ Ready in [time]
○ Local:        http://localhost:3000
```

**⚠️ Keep this terminal open too!**

---

## Step 3: Open Your Browser

Visit: **http://localhost:3000**

You should see the UMass Housing Recommender homepage.

---

## Testing the Application

1. Click **"Start Recommender"** on the homepage
2. Fill out the questionnaire:
   - Select year status (first-year or upperclassman)
   - Select your major
   - Select room type
   - Select your gender
   - Answer all other questions
3. Submit the form
4. Wait for results (may take 30-60 seconds)
5. View your roommate matches (only matches with 75%+ compatibility)

---

## Troubleshooting

### Backend Not Starting?

**Check if port 8000 is already in use:**
```bash
lsof -ti:8000 | xargs kill
```

**Install backend dependencies:**
```bash
cd /Users/abhijay/Downloads/hackUmass-main/backend
pip install -r requirements.txt
```

**Check if Python backend file exists:**
```bash
ls /Users/abhijay/Downloads/hackUmass-main/backend/main.py
```

### Frontend Not Starting?

**Install frontend dependencies:**
```bash
cd /Users/abhijay/Downloads/hackUmass-main
npm install
```

**Check if port 3000 is in use:**
The frontend will automatically use port 3001 or 3002. Check the terminal output for the actual port.

### "Request Timed Out" Error?

1. Make sure the backend is running (Terminal 1)
2. Check backend is accessible: http://localhost:8000/health
3. Wait up to 60 seconds for processing (timeout is set to 60s)

### Backend Connection Error?

**Test backend directly:**
```bash
curl http://localhost:8000/health
```

Should return: `{"status": "healthy"}`

**Check backend logs** in Terminal 1 for error messages.

---

## What's Running?

- **Backend**: Python FastAPI server on port 8000
  - Handles dorm recommendations
  - Scores roommate compatibility
  - Uses Gemini AI for matching

- **Frontend**: Next.js app on port 3000 (or 3001/3002)
  - Questionnaire UI
  - Results display
  - Connects to backend via `/api/match`

---

## Stopping the Application

1. **Stop Frontend**: In Terminal 2, press `Ctrl+C`
2. **Stop Backend**: In Terminal 1, press `Ctrl+C`

---

## That's It! 🎉

You're ready to use the UMass Housing Recommender!

For issues or questions, check the terminal logs for error messages.

