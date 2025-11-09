# 🔧 Quick Fix for Connection Error

## The Problem
The error "Unable to connect to the matching service. Please make sure the Python backend is running on port 8000" means the frontend cannot reach the backend.

## ✅ Solution

### Step 1: Make sure the backend is running

Open a terminal and run:
```bash
cd /Users/abhijay/Downloads/hackUmass-main/backend
python3 main.py
```

You should see:
```
🚀 Starting UMass Housing Recommender Backend
📡 Server running on: http://0.0.0.0:8000
```

**Keep this terminal open!**

### Step 2: Verify backend is working

In another terminal, test the backend:
```bash
curl http://localhost:8000/health
```

You should see: `{"status":"healthy"}`

### Step 3: Restart the frontend

If the frontend is already running, restart it:
1. Stop it (Ctrl+C in the frontend terminal)
2. Start it again:
```bash
cd /Users/abhijay/Downloads/hackUmass-main
npm run dev
```

### Step 4: Try again

Go to `http://localhost:3000` (or `http://localhost:3002` if that's where your frontend is running) and try the quiz again.

---

## Common Issues

### Port 8000 is already in use
```bash
# Kill the process using port 8000
lsof -ti:8000 | xargs kill -9

# Then restart the backend
cd /Users/abhijay/Downloads/hackUmass-main/backend
python3 main.py
```

### Backend crashes on startup
- Check that all dependencies are installed: `pip3 install -r requirements.txt`
- Check the error message in the terminal
- Make sure Python 3.8+ is installed

### Frontend still can't connect
- Make sure the backend terminal shows "Server running on: http://0.0.0.0:8000"
- Try accessing `http://localhost:8000/health` in your browser
- Check that no firewall is blocking port 8000

---

## Quick Start Script

I've created a helper script. You can use it to start the backend:

```bash
cd /Users/abhijay/Downloads/hackUmass-main
./start_backend.sh
```

This script will:
- Check if Python 3 is installed
- Free port 8000 if it's in use
- Install dependencies if needed
- Start the backend server
