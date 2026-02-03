@echo off
echo ============================================
echo   SYSTEM STATUS CHECK
echo ============================================
echo.

echo [1] Checking Docker...
docker --version 2>nul
if errorlevel 1 (
    echo [X] Docker is NOT installed
    echo     Download from: https://www.docker.com/products/docker-desktop
) else (
    echo [OK] Docker is installed
)
echo.

echo [2] Checking if Docker is running...
docker ps >nul 2>&1
if errorlevel 1 (
    echo [X] Docker is NOT running
    echo     Start Docker Desktop manually
) else (
    echo [OK] Docker is running
)
echo.

echo [3] Checking if n8n is running...
docker ps | findstr n8n >nul 2>&1
if errorlevel 1 (
    echo [X] n8n is NOT running
    echo     Run: setup_and_start.bat
) else (
    echo [OK] n8n container is running
)
echo.

echo [4] Checking configuration files...
if exist ".env" (
    echo [OK] .env file exists
) else (
    echo [X] .env file missing
)

if exist "docker-compose.yml" (
    echo [OK] docker-compose.yml exists
) else (
    echo [X] docker-compose.yml missing
)

if exist "AI_Hardware_Pipeline_Workflow.json" (
    echo [OK] Workflow file exists
) else (
    echo [X] Workflow file missing
)
echo.

echo [5] Testing n8n connection...
curl -s http://localhost:5678 >nul 2>&1
if errorlevel 1 (
    echo [X] Cannot connect to n8n
    echo     n8n might not be running or port 5678 is blocked
) else (
    echo [OK] n8n is accessible at http://localhost:5678
)
echo.

echo ============================================
echo   STATUS CHECK COMPLETE
echo ============================================
echo.
echo If all checks show [OK], you're ready to go!
echo If any show [X], follow the suggestions above.
echo.
pause
