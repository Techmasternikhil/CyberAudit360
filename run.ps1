Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "           CyberAudit360 Launcher (PowerShell)      " -ForegroundColor Cyan
Write-Host "===================================================" -ForegroundColor Cyan

# 1. Setup Backend
Write-Host "[*] Checking Python Virtual Environment..." -ForegroundColor Yellow
if (-not (Test-Path "venv")) {
    python -m venv venv
}
& .\venv\Scripts\Activate.ps1

Write-Host "[*] Ensuring dependencies..." -ForegroundColor Yellow
pip install -r backend\requirements.txt -q

if (-not (Test-Path "frontend\node_modules")) {
    Write-Host "[*] Installing Frontend packages..." -ForegroundColor Yellow
    Push-Location frontend
    npm install
    Pop-Location
}

# 2. Launch Backend
Write-Host "[*] Launching Backend on http://127.0.0.1:8000 ..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; ..\venv\Scripts\Activate.ps1; uvicorn app.main:app --port 8000"

# 3. Launch Frontend
Write-Host "[*] Launching Frontend on http://localhost:5173 ..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"

# 4. Open Browser
Start-Sleep -Seconds 3
Start-Process "http://localhost:5173/"

Write-Host "CyberAudit360 is successfully launched!" -ForegroundColor Cyan
