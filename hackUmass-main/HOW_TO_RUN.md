# How to Run the UMass Housing Recommender Application

This guide will help you run both the frontend (Next.js) and backend (Python FastAPI) servers.

## Prerequisites

- **Node.js** (v18 or higher)
- **Python** (v3.8 or higher)
- **npm** or **yarn** package manager

## Step 1: Install Frontend Dependencies

```bash
cd /Users/abhijay/Downloads/hackUmass-main
npm install
```

## Step 2: Install Backend Dependencies

```bash
cd backend
python3 -m pip install -r requirements.txt
```

**Note:** If you encounter issues, try:
```bash
pip3 install -r requirements.txt
```

## Step 3: Set Up Environment Variables

### Backend Environment Variables

Create a `.env` file in the `backend` directory:

```bash
cd backend
touch .env
```

Add your Gemini API key to the `.env` file:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

**Note:** You can get a Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

### Frontend Environment Variables (Optional)

If you're using Supabase, create a `.env.local` file in the root directory:

```bash
cd /Users/abhijay/Downloads/hackUmass-main
touch .env.local
```

Add your Supabase credentials:
```
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
```

**Note:** The app will work without Supabase - it uses a Python backend for matching.

## Step 4: Start the Backend Server

Open a **new terminal window** and run:

```bash
cd /Users/abhijay/Downloads/hackUmass-main/backend
python3 main.py
```

You should see:
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

The backend will be running on **http://localhost:8000**

## Step 5: Start the Frontend Server

Open a **new terminal window** and run:

```bash
cd /Users/abhijay/Downloads/hackUmass-main
npm run dev
```

You should see:
```
✓ Ready in X seconds
○ Local:        http://localhost:3000
```

The frontend will be running on **http://localhost:3000**

## Step 6: Access the Application

1. Open your browser and go to: **http://localhost:3000**
2. Click on "Recommender" to start the questionnaire
3. Fill out the housing preferences form
4. Submit to get dorm and roommate recommendations

## Quick Start (All in One)

If you want to run both servers quickly, use these commands in separate terminals:

**Terminal 1 (Backend):**
```bash
cd /Users/abhijay/Downloads/hackUmass-main/backend && python3 main.py
```

**Terminal 2 (Frontend):**
```bash
cd /Users/abhijay/Downloads/hackUmass-main && npm run dev
```

## Troubleshooting

### Backend Issues

1. **Port 8000 already in use:**
   ```bash
   # Find and kill the process using port 8000
   lsof -ti:8000 | xargs kill -9
   ```

2. **Python module not found:**
   ```bash
   # Make sure you installed requirements
   pip3 install -r backend/requirements.txt
   ```

3. **Gemini API Key missing:**
   - Make sure you created `backend/.env` with `GEMINI_API_KEY=your_key`

### Frontend Issues

1. **Port 3000 already in use:**
   ```bash
   # Find and kill the process using port 3000
   lsof -ti:3000 | xargs kill -9
   ```

2. **Module resolution errors:**
   - These are IDE warnings and won't prevent the app from running
   - Restart your TypeScript server in your IDE if needed

3. **Build errors:**
   ```bash
   # Clear Next.js cache
   rm -rf .next
   npm run dev
   ```

### Connection Issues

- Make sure both servers are running
- Check that backend is on port 8000 and frontend is on port 3000
- Verify the backend is accessible: `curl http://localhost:8000/healthz`

## Testing the Application

1. **Test Backend Health:**
   ```bash
   curl http://localhost:8000/healthz
   ```
   Should return: `{"status":"healthy"}`

2. **Test Frontend:**
   - Open http://localhost:3000 in your browser
   - Navigate to the Recommender page
   - Complete the questionnaire

## Stopping the Servers

- **Backend:** Press `Ctrl+C` in the backend terminal
- **Frontend:** Press `Ctrl+C` in the frontend terminal

## Production Build

To create a production build:

```bash
# Frontend
npm run build
npm start

# Backend
# Use a production WSGI server like gunicorn
pip install gunicorn
gunicorn main:app --host 0.0.0.0 --port 8000
```
