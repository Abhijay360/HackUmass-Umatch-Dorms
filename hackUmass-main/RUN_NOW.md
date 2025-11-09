# 🚀 How to Run the UMass Housing Recommender

## Quick Start Guide

### Prerequisites
- Python 3.8+ installed
- Node.js 18+ installed
- npm or yarn installed

---

## Step 1: Set Up Backend (Python)

### 1.1 Navigate to backend directory
```bash
cd backend
```

### 1.2 Install Python dependencies
```bash
pip3 install -r requirements.txt
```

**Note:** If you get permission errors, use:
```bash
pip3 install --user -r requirements.txt
```

### 1.3 (Optional) Set up environment variables
Create a `.env` file in the `backend` directory:
```bash
GEMINI_API_KEY=your_api_key_here
```

**Note:** The backend will use a default key if not provided, but it's recommended to set your own.

### 1.4 Start the backend server
```bash
python3 main.py
```

You should see:
```
==================================================
🚀 Starting UMass Housing Recommender Backend
==================================================
📡 Server running on: http://0.0.0.0:8000
📝 API Documentation: http://0.0.0.0:8000/docs
🔑 Using Gemini API: ✅ Configured
==================================================
```

**Keep this terminal window open!** The backend must be running for the frontend to work.

---

## Step 2: Set Up Frontend (Next.js)

### 2.1 Open a NEW terminal window
Keep the backend running in the first terminal, and open a second terminal.

### 2.2 Navigate to project root
```bash
cd /Users/abhijay/Downloads/hackUmass-main
```

### 2.3 Install Node.js dependencies (if not already done)
```bash
npm install
```

### 2.4 Start the frontend development server
```bash
npm run dev
```

You should see:
```
- ready started server on 0.0.0.0:3000, url: http://localhost:3000
```

---

## Step 3: Access the Application

1. **Frontend:** Open your browser and go to:
   ```
   http://localhost:3000
   ```

2. **Backend API Docs (optional):** View the API documentation at:
   ```
   http://localhost:8000/docs
   ```

3. **Backend Health Check:**
   ```
   http://localhost:8000/health
   ```

---

## Troubleshooting

### Backend Issues

**Port 8000 already in use:**
```bash
# Find and kill the process using port 8000
lsof -ti:8000 | xargs kill -9

# Then restart the backend
python3 main.py
```

**Python dependencies not found:**
```bash
# Make sure you're in the backend directory
cd backend

# Reinstall dependencies
pip3 install -r requirements.txt
```

**API Key errors:**
- The backend will work with the default key, but for production, set `GEMINI_API_KEY` in a `.env` file

### Frontend Issues

**Port 3000 already in use:**
```bash
# Find and kill the process using port 3000
lsof -ti:3000 | xargs kill -9

# Then restart the frontend
npm run dev
```

**Module not found errors:**
```bash
# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Cannot connect to backend:**
- Make sure the backend is running on port 8000
- Check that you see the backend startup message
- Try accessing `http://localhost:8000/health` in your browser

---

## Running Both Servers (Quick Commands)

### Terminal 1 (Backend):
```bash
cd /Users/abhijay/Downloads/hackUmass-main/backend
python3 main.py
```

### Terminal 2 (Frontend):
```bash
cd /Users/abhijay/Downloads/hackUmass-main
npm run dev
```

---

## Testing the Application

1. Go to `http://localhost:3000`
2. Click "Start Quiz" or navigate to the recommender page
3. Fill out the questionnaire
4. Submit and wait for matches (may take 30-60 seconds for LLM processing)
5. View your dorm recommendations and roommate matches

---

## Stopping the Servers

- **Backend:** Press `Ctrl+C` in the backend terminal
- **Frontend:** Press `Ctrl+C` in the frontend terminal

---

## Need Help?

If you encounter errors:
1. Check that both servers are running
2. Check the terminal output for error messages
3. Verify ports 3000 and 8000 are not in use by other applications
4. Make sure all dependencies are installed correctly

