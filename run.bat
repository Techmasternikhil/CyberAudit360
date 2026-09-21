@echo off
title CyberAudit360 Launcher
echo ===================================================
echo           CyberAudit360 Launcher
echo ===================================================
echo.

:: 1. Check Python
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Python is not installed or not in PATH!
    pause
    exit /b 1
)

:: 2. Check Node
where npm >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Node.js/npm is not installed or not in PATH!
    pause
    exit /b 1
)

:: 3. Setup Backend
echo [*] Checking Backend Virtual Environment...
if not exist "venv\" (
    echo [*] Creating virtual environment...
    python -m venv venv
)
call .\venv\Scripts\activate.bat

echo [*] Installing backend dependencies...
pip install -r backend\requirements.txt -q

:: 4. Setup Frontend
echo [*] Checking Frontend Dependencies...
if not exist "frontend\node_modules\" (
    echo [*] Installing npm packages (first-time setup)...
    cd frontend && npm install && cd ..
)

:: 5. Launch Backend Server in separate window
echo [*] Starting Backend API Server on http://127.0.0.1:8000 ...
start "CyberAudit360 Backend" cmd /k "cd backend && ..\venv\Scripts\activate.bat && uvicorn app.main:app --port 8000"

:: 6. Launch Frontend Dev Server in separate window
echo [*] Starting Frontend Server on http://localhost:5173 ...
start "CyberAudit360 Frontend" cmd /k "cd frontend && npm run dev"

:: 7. Wait 3 seconds and open browser
timeout /t 3 /nobreak >nul
echo [*] Opening Dashboard in browser...
start http://localhost:5173/

echo.
echo ===================================================
echo CyberAudit360 is running!
echo Dashboard: http://localhost:5173/
echo API Docs:  http://127.0.0.1:8000/docs
echo ===================================================
pause
