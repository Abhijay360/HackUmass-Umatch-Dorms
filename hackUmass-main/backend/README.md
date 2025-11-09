# UMass Housing Recommender Backend

FastAPI backend server for the UMass Housing Recommender application. This backend uses Google's Gemini AI to match students with compatible roommates and recommend ideal dorm areas.

## Features

- **Dorm Recommendation**: AI-powered recommendation of the best UMass dorm area based on student preferences
- **Roommate Matching**: Compatibility scoring between students using a 100-point rubric
- **Academic Proximity**: Considers major/academic zone when recommending dorm locations
- **RESTful API**: Clean FastAPI endpoints for frontend integration

## Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure API Key

Create a `.env` file in the `backend` directory:

```bash
cp .env.example .env
```

Edit `.env` and add your Gemini API key:

```
GEMINI_API_KEY=your_actual_api_key_here
```

**Get your API key from**: https://makersuite.google.com/app/apikey

### 3. Run the Backend

**Option 1: Using Python directly**
```bash
python3 main.py
```

**Option 2: Using the startup script**
```bash
chmod +x start.sh
./start.sh
```

**Option 3: Using uvicorn directly**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The server will start on `http://localhost:8000`

## API Endpoints

### Health Check
```
GET /health
```
Returns server health status.

### Get Matches
```
POST /api/match
```

**Request Body:**
```json
{
  "userId": "user_123",
  "name": "John Doe",
  "major": "Engineering",
  "budgetRange": "800-1200",
  "roomType": "double",
  "genderType": "coed",
  "housingType": "on-campus",
  "socialLevelType": "moderately-social",
  "noiseLevelType": "quiet",
  "yearMix": "mix",
  "sleepSchedule": "early-bird",
  "tidinessLevel": "tidy",
  "communityType": "academic-focused",
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
      "candidateDorm": "Northeast",
      "gradYear": "2026"
    }
  ]
}
```

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Architecture

The backend consists of two main components:

1. **`main.py`**: FastAPI application with REST endpoints
2. **`HackUmass_back_end.py`**: Core matching logic using Gemini AI

### Matching Process

1. **Dorm Recommendation**: Analyzes user profile to recommend the best dorm area
2. **Candidate Filtering**: Filters potential roommates by recommended dorm area
3. **Compatibility Scoring**: Scores each candidate using a 100-point rubric:
   - Sleep Habits & Tidiness (40 pts)
   - Noise & Guests (30 pts)
   - Amenities & Logistics (15 pts)
   - Health & Zero-Tolerance (10 pts)
   - Values Alignment (5 pts)

## Development

### Testing

Run the test suite included in `HackUmass_back_end.py`:

```bash
python3 HackUmass_back_end.py
```

This will run 4 test cases and display compatibility scores.

### Environment Variables

- `GEMINI_API_KEY`: Your Google Gemini API key (required)
- `PORT`: Server port (default: 8000)
- `HOST`: Server host (default: 0.0.0.0)

## Troubleshooting

### API Key Issues
- Ensure your `.env` file exists and contains a valid `GEMINI_API_KEY`
- Check that the API key has proper permissions for Gemini API

### Port Already in Use
- Change the port in `main.py` or set `PORT` environment variable
- Kill the process using port 8000: `lsof -ti:8000 | xargs kill`

### Import Errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check that you're using Python 3.8+

## License

Part of the UMass Housing Recommender project.
