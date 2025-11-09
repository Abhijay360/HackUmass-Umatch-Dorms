#!/bin/bash

# Start the Python backend server
echo "🚀 Starting Python backend on port 8000..."
cd "$(dirname "$0")"

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found. Using default configuration."
    echo "   Create a .env file with GEMINI_API_KEY for production use."
fi

# Start the server
python3 main.py
