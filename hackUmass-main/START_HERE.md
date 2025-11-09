# 🚀 How to Run the Application

## Simple 2-Step Process

You need **TWO terminal windows** - one for the backend, one for the frontend.

---

## Step 1: Start the Backend (Python)

**Open Terminal 1** and run:

```bash
cd /Users/abhijay/Downloads/hackUmass-main/backend
python3 main.py
```

**✅ You should see:**
```
==================================================
🚀 Starting UMass Housing Recommender Backend
==================================================
📡 Server running on: http://0.0.0.0:8000
📝 API Documentation: http://0.0.0.0:8000/docs
==================================================
```

**⚠️ KEEP THIS TERMINAL OPEN!** The backend must keep running.

---

## Step 2: Start the Frontend (Next.js)

**Open Terminal 2** (new terminal window) and run:

```bash
cd /Users/abhijay/Downloads/hackUmass-main
npm run dev
```

**✅ You should see:**
```
- ready started server on 0.0.0.0:3000, url: http://localhost:3000
```

---

## Step 3: Open in Browser

Open your browser and go to:
```
http://localhost:3000
```

Or if your frontend is on a different port (like 3002):
```
http://localhost:3002
```

---

## Quick Commands Summary

### Terminal 1 (Backend):
```bash
cd /Users/abhijay/Downloads/hackUmass-main/backend && python3 main.py
```

### Terminal 2 (Frontend):
```bash
cd /Users/abhijay/Downloads/hackUmass-main && npm run dev
```

---

## Troubleshooting

### "Port 8000 already in use"
```bash
lsof -ti:8000 | xargs kill -9
```
Then restart the backend.

### "Port 3000 already in use"
```bash
lsof -ti:3000 | xargs kill -9
```
Then restart the frontend.

### "Cannot find module" errors
```bash
# In the project root directory
npm install
```

### "Python dependencies not found"
```bash
# In the backend directory
cd /Users/abhijay/Downloads/hackUmass-main/backend
pip3 install -r requirements.txt
```

---

## Verify Everything is Working

1. **Backend Health Check:** Open `http://localhost:8000/health` in browser
   - Should show: `{"status":"healthy"}`

2. **Backend API Docs:** Open `http://localhost:8000/docs` in browser
   - Should show API documentation

3. **Frontend:** Open `http://localhost:3000` in browser
   - Should show the application homepage

---

## Stopping the Servers

- Press `Ctrl+C` in each terminal to stop the servers
- Stop backend first, then frontend

---

## Need Help?

If you see errors:
1. Check that both terminals show the servers are running
2. Make sure ports 8000 and 3000 (or 3002) are not blocked
3. Verify all dependencies are installed (see troubleshooting above)
