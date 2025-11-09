# UMass Housing Recommender - Full Stack Setup

This project consists of:
- **Frontend**: Next.js application (runs on port 3000/3001)
- **Backend**: FastAPI Python server (runs on port 8000)

## Quick Start

### 1. Start the Python Backend

Open a terminal and run:

```bash
cd backend
pip install -r requirements.txt
python main.py
```

The backend will start on `http://localhost:8000`

### 2. Start the Next.js Frontend

Open another terminal and run:

```bash
npm run dev
```

The frontend will start on `http://localhost:3000` (or 3001 if 3000 is taken)

### 3. Use the Application

1. Go to `http://localhost:3000` (or 3001)
2. Click "Start Recommender"
3. Complete the 6-step questionnaire
4. View your roommate matches!

## Environment Variables (Optional)

Create a `.env.local` file in the root directory:

```env
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

If not set, it defaults to `http://localhost:8000`

## Troubleshooting

### Backend not connecting?
- Make sure the Python backend is running on port 8000
- Check that all dependencies are installed: `pip install -r backend/requirements.txt`
- Verify the API key in `supabase/HackUmass back-end.py` is set

### Frontend errors?
- Make sure both servers are running
- Check browser console for errors
- Verify CORS is configured correctly in `backend/main.py`

## Project Structure

```
hackUmass-main/
├── app/                    # Next.js frontend pages
├── components/             # React components
├── backend/               # Python FastAPI backend
│   ├── main.py           # FastAPI server
│   └── requirements.txt  # Python dependencies
└── supabase/
    └── HackUmass back-end.py  # Original Python matching logic
```

