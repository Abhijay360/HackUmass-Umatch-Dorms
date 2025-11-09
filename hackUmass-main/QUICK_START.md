# Quick Start Guide 🚀

## Step-by-Step Instructions

### Step 1: Start the Backend (Terminal 1)

Open a terminal and run:

```bash
cd /Users/abhijay/Downloads/hackUmass-main/backend
python3 main.py
```

**You should see:**
```
🚀 Starting UMass Housing Recommender Backend
📡 Server running on: http://0.0.0.0:8000
📝 API Documentation: http://0.0.0.0:8000/docs
🔑 Using Gemini API: ✅ Configured
```

**Keep this terminal open!** The backend must stay running.

---

### Step 2: Start the Frontend (Terminal 2)

Open a **NEW** terminal window and run:

```bash
cd /Users/abhijay/Downloads/hackUmass-main
npm run dev
```

**You should see:**
```
✓ Ready in [time]
○ Local:        http://localhost:3000
```

**Keep this terminal open too!**

---

### Step 3: Open Your Browser

Visit: **http://localhost:3000**

You should see the UMass Housing Recommender homepage.

---

## Quick Test

1. Click "Start Recommender" on the homepage
2. Fill out the questionnaire (5 steps)
3. Submit the form
4. You should see roommate matches with compatibility scores!

---

## Troubleshooting

### "Port 8000 already in use"
```bash
# Find and kill the process
lsof -ti:8000 | xargs kill

# Then restart the backend
cd /Users/abhijay/Downloads/hackUmass-main/backend
python3 main.py
```

### "Port 3000 already in use"
The frontend will automatically use port 3001 or 3002. Check the terminal output for the actual port.

### "Backend not connecting"
- Make sure backend is running (Terminal 1)
- Check http://localhost:8000/health - should return `{"status": "healthy"}`
- Make sure both terminals are open and running

### "Module not found" errors
```bash
# Backend dependencies
cd /Users/abhijay/Downloads/hackUmass-main/backend
pip install -r requirements.txt

# Frontend dependencies
cd /Users/abhijay/Downloads/hackUmass-main
npm install
```

---

## What's Running

- **Backend**: Python FastAPI server on port 8000
- **Frontend**: Next.js app on port 3000 (or 3001/3002)
- **Connection**: Frontend → `/api/match` → Backend → Gemini AI

---

## That's It! 🎉

You're ready to use the UMass Housing Recommender!

