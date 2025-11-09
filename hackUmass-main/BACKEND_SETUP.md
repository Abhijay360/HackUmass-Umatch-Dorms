# Backend Setup Guide

This guide will help you set up and run the UMass Housing Recommender backend.

## Quick Start

### 1. Navigate to Backend Directory
```bash
cd backend
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API Key (Optional but Recommended)

Create a `.env` file:
```bash
cp .env.example .env
```

Edit `.env` and add your Gemini API key:
```
GEMINI_API_KEY=your_actual_api_key_here
```

**Get your API key from**: https://makersuite.google.com/app/apikey

> **Note**: If you don't set up a `.env` file, the backend will use a default API key (for development only).

### 4. Start the Backend

**Option 1: Using the startup script**
```bash
./start.sh
```

**Option 2: Using Python directly**
```bash
python3 main.py
```

**Option 3: Using uvicorn**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The server will start on `http://localhost:8000`

## Verify Backend is Running

1. **Health Check**: Visit http://localhost:8000/health
   - Should return: `{"status": "healthy"}`

2. **API Documentation**: Visit http://localhost:8000/docs
   - Interactive Swagger UI for testing endpoints

3. **Test Endpoint**: Visit http://localhost:8000/
   - Should return: `{"message": "UMass Housing Recommender API", "status": "running"}`

## Backend Architecture

```
backend/
├── main.py                    # FastAPI application & REST endpoints
├── HackUmass_back_end.py      # Core matching logic (Gemini AI)
├── requirements.txt           # Python dependencies
├── start.sh                   # Startup script
├── .env.example              # Environment variables template
└── README.md                 # Detailed documentation
```

## Key Files

### `main.py`
- FastAPI application
- REST API endpoints (`/api/match`, `/health`)
- CORS configuration for Next.js frontend
- Field name normalization between frontend and backend

### `HackUmass_back_end.py`
- Gemini AI integration
- Dorm recommendation logic
- Roommate compatibility scoring (100-point rubric)
- Academic proximity calculations

## API Endpoints

### POST `/api/match`
Main endpoint for getting dorm recommendations and roommate matches.

**Request**: User profile with preferences
**Response**: Dorm recommendation + ranked list of roommate matches

See `backend/README.md` for detailed API documentation.

## Troubleshooting

### Port 8000 Already in Use
```bash
# Find process using port 8000
lsof -ti:8000

# Kill the process
lsof -ti:8000 | xargs kill
```

Or change the port in `main.py`:
```python
port = int(os.getenv("PORT", 8001))  # Change to 8001
```

### Module Not Found Errors
```bash
# Ensure you're in the backend directory
cd backend

# Reinstall dependencies
pip install -r requirements.txt
```

### API Key Issues
- Check that `.env` file exists in `backend/` directory
- Verify `GEMINI_API_KEY` is set correctly
- Test API key at: https://makersuite.google.com/app/apikey

### Import Errors
- Ensure Python 3.8+ is installed: `python3 --version`
- Install all dependencies: `pip install -r requirements.txt`

## Development

### Running Tests
The backend includes a test suite:
```bash
python3 HackUmass_back_end.py
```

This runs 4 test cases and displays compatibility scores.

### Hot Reload (Development)
Use uvicorn with `--reload` flag:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Next Steps

1. ✅ Backend is running on port 8000
2. ✅ Start the Next.js frontend (see main README)
3. ✅ Test the full flow: Frontend → API → Gemini AI → Results

## Support

For issues or questions, check:
- `backend/README.md` - Detailed API documentation
- API docs at http://localhost:8000/docs (when running)

