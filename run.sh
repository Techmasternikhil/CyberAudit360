#!/usr/bin/env bash
set -e

echo "==================================================="
echo "           CyberAudit360 Launcher (Unix)           "
echo "==================================================="

# 1. Backend setup
if [ ! -d "venv" ]; then
    echo "[*] Creating virtualenv..."
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r backend/requirements.txt -q

# 2. Frontend setup
if [ ! -d "frontend/node_modules" ]; then
    echo "[*] Installing npm dependencies..."
    cd frontend && npm install && cd ..
fi

# 3. Start Backend
echo "[*] Starting Backend..."
cd backend && uvicorn app.main:app --port 8000 &
BACKEND_PID=$!
cd ..

# 4. Start Frontend
echo "[*] Starting Frontend..."
cd frontend && npm run dev &
FRONTEND_PID=$!
cd ..

# Trap to kill both on exit
trap "kill $BACKEND_PID $FRONTEND_PID" EXIT

echo "[*] CyberAudit360 running at http://localhost:5173/"
echo "Press CTRL+C to stop both servers."
wait
