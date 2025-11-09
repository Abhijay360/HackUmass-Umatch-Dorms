#!/bin/bash

# Script to start both backend and frontend together

echo "🚀 Starting UMass Housing Recommender..."
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BACKEND_DIR="$SCRIPT_DIR/backend"
FRONTEND_DIR="$SCRIPT_DIR"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit
}

trap cleanup SIGINT SIGTERM

# Start backend
echo "📦 Starting Python backend..."
cd "$BACKEND_DIR"
python3 main.py > /tmp/backend.log 2>&1 &
BACKEND_PID=$!

# Wait for backend to start
sleep 4

# Check if backend is running
if ! ps -p $BACKEND_PID > /dev/null; then
    echo "❌ Backend failed to start. Check /tmp/backend.log for errors"
    cat /tmp/backend.log
    exit 1
fi

echo "✅ Backend started (PID: $BACKEND_PID) - http://localhost:8000"

# Start frontend
echo "🌐 Starting Next.js frontend..."
cd "$FRONTEND_DIR"
npm run dev > /tmp/frontend.log 2>&1 &
FRONTEND_PID=$!

# Wait for frontend to start
sleep 5

echo "✅ Frontend started (PID: $FRONTEND_PID)"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 Both servers are running!"
echo ""
echo "📱 Frontend: http://localhost:3001"
echo "🔧 Backend:   http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop both servers"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Wait for both processes
wait

