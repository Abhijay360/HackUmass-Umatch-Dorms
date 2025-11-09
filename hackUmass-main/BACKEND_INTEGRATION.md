# Backend Integration Complete ✅

The new backend file `HackUmass back-end (2).py` has been successfully integrated into the system.

## What Was Done

1. **Backend File Updated**
   - Copied `supabase/HackUmass back-end (2).py` to `backend/HackUmass_back_end.py`
   - Updated to use environment variables for API key
   - All datasets and test profiles are included

2. **FastAPI Integration**
   - `backend/main.py` automatically imports and uses `HackUmass_back_end.py`
   - The `score_and_rank_matches` function is available via the `/api/match` endpoint

3. **Frontend Connection**
   - Frontend connects via `/api/match` route (Next.js API route)
   - Next.js API route proxies to `http://localhost:8000/api/match`
   - All requests go through port 3000 (frontend), which forwards to port 8000 (backend)

4. **Port Configuration**
   - Backend runs on port 8000 (configurable via `PORT` env variable)
   - Frontend runs on port 3000
   - Frontend API route connects to `http://localhost:8000`

## Backend Features

The new backend includes:

- **Academic Zone Mapping**: Maps majors to academic zones (North Science Hub, Central Science, etc.)
- **Proximity Scoring**: Calculates dorm proximity scores based on major
- **First-Year vs Upperclassmen Context**: Different dorm recommendations based on year status
- **100-Point Compatibility Rubric**: 
  - Sleep Habits & Tidiness (40 pts)
  - Noise & Guests (30 pts)
  - Amenities & Logistics (15 pts)
  - Health & Zero-Tolerance (10 pts)
  - Values Alignment (5 pts)
- **Test Suite**: 4 test cases included for validation
- **Simulated Database**: 4 candidate profiles for testing

## How to Run

### 1. Start Backend (Port 8000)
```bash
cd backend
python3 main.py
```

Or use the startup script:
```bash
cd backend
./start.sh
```

### 2. Start Frontend (Port 3000)
```bash
npm run dev
```

### 3. Verify Connection

**Backend Health Check:**
- Visit: http://localhost:8000/health
- Should return: `{"status": "healthy"}`

**API Documentation:**
- Visit: http://localhost:8000/docs
- Interactive Swagger UI

**Frontend:**
- Visit: http://localhost:3000
- Complete the questionnaire
- Results will be fetched from backend via `/api/match`

## Data Flow

```
User fills form → Frontend (port 3000)
                ↓
         /api/match (Next.js API route)
                ↓
         http://localhost:8000/api/match (FastAPI)
                ↓
         HackUmass_back_end.py
                ↓
         Gemini AI API
                ↓
         Results returned to frontend
```

## Backend Endpoints

### POST `/api/match`
Main endpoint for getting dorm recommendations and roommate matches.

**Request Body:**
```json
{
  "yearStatus": "first-year" | "upperclassman",
  "roomType": "single" | "double" | "triple" | "suite" | "apartment",
  "genderType": "co-ed" | "male" | "female",
  "accessible": "yes" | "preferred" | "no",
  "socialLevelType": "...",
  "noiseLevelType": "...",
  // ... other preferences
}
```

**Response:**
```json
{
  "dorm_recommendation": "Northeast",
  "ranked_matches": [
    {
      "compatibilityScore": 85,
      "confidenceLevel": "High",
      "reasoningSummary": "...",
      "matchAdvice": "...",
      "candidateName": "Jane Doe",
      "candidateDorm": "Northeast"
    }
  ]
}
```

## Environment Variables

Create a `.env` file in the `backend/` directory:

```bash
GEMINI_API_KEY=your_api_key_here
PORT=8000
HOST=0.0.0.0
```

## Testing

Run the test suite:
```bash
cd backend
python3 HackUmass_back_end.py
```

This will run 4 test cases and display compatibility scores.

## Troubleshooting

### Backend not starting
- Check Python version: `python3 --version` (needs 3.8+)
- Install dependencies: `pip install -r requirements.txt`
- Check port 8000 is available: `lsof -ti:8000`

### Frontend can't connect
- Verify backend is running on port 8000
- Check browser console for errors
- Verify `/api/match` route exists in `app/api/match/route.ts`

### API errors
- Check Gemini API key is set correctly
- Verify API key has proper permissions
- Check backend logs for detailed error messages

## Files Updated

- ✅ `backend/HackUmass_back_end.py` - New backend logic with all datasets
- ✅ `backend/main.py` - FastAPI server (already configured)
- ✅ `app/api/match/route.ts` - Frontend API proxy (already configured)
- ✅ `app/results/page.tsx` - Updated validation for new fields

## Status

✅ Backend integrated and ready
✅ Frontend connected to backend
✅ Port 8000 configured
✅ All datasets included
✅ Test suite available

The system is ready to use!

