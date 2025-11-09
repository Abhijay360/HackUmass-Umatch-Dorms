#!/bin/bash

# Start the Python backend server
cd "$(dirname "$0")/backend"

echo "🚀 Starting UMass Housing Recommender Backend..."
echo "📁 Working directory: $(pwd)"
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 is not installed or not in PATH"
    exit 1
fi

# Check if port 8000 is already in use
if lsof -ti:8000 &> /dev/null; then
    echo "⚠️  Port 8000 is already in use. Attempting to free it..."
    lsof -ti:8000 | xargs kill -9 2>/dev/null
    sleep 2
fi

# Check if requirements are installed
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo "📦 Installing Python dependencies..."
    pip3 install -r requirements.txt
fi

# Start the server
echo "✅ Starting backend server on port 8000..."
python3 main.py

