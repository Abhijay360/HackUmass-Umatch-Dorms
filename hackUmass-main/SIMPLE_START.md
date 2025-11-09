# 🚀 Simple Start Guide

## Option 1: One Command (Easiest!) ⭐

Run this single command to start everything:

```bash
cd "/Users/abhijay/Downloads/hackUmass-main"
./start-all.sh
```

This starts both backend and frontend automatically!

Then open: **http://localhost:3001**

---

## Option 2: Manual Start (Two Terminals)

### Terminal 1 - Backend:
```bash
cd "/Users/abhijay/Downloads/hackUmass-main/backend"
pip3 install -r requirements.txt
python3 main.py
```

### Terminal 2 - Frontend:
```bash
cd "/Users/abhijay/Downloads/hackUmass-main"
npm run dev
```

Then open: **http://localhost:3001**

---

## ✅ How to Know It's Working

**Backend is running if you see:**
```
🚀 Starting UMass Housing Recommender Backend
📡 Server running on: http://localhost:8000
```

**Frontend is running if you see:**
```
▲ Next.js 13.5.1
- Local:        http://localhost:3001
✓ Ready
```

---

## 🔗 Important Notes

- **You only need to open ONE URL**: `http://localhost:3001`
- The frontend automatically connects to the backend
- Both servers must be running for the app to work
- The frontend runs on port 3001, backend on 8000 (but you don't need to visit 8000 directly)

---

## ❌ Troubleshooting

### "python3: command not found"
- Try: `python main.py` instead of `python3 main.py`

### "Module not found" errors
```bash
cd backend
pip3 install -r requirements.txt
```

### Backend won't start
- Check that port 8000 is not in use
- Make sure `backend/HackUmass_back_end.py` exists
- Check the terminal for error messages

### Frontend can't connect
- Make sure backend is running first!
- Wait a few seconds after starting backend before starting frontend

