@echo off
echo ========================================
echo AI Hardware Pipeline - Quick Start
echo ========================================
echo.

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not running!
    echo Please start Docker Desktop and try again.
    pause
    exit /b 1
)

echo [OK] Docker is running
echo.

REM Check if .env file exists
if not exist .env (
    echo [INFO] Creating .env file from template...
    copy .env.example .env
    echo.
    echo [ACTION REQUIRED] Please edit .env file and add your API keys:
    echo   - OPENAI_API_KEY
    echo   - DIGIKEY_API_KEY (optional)
    echo   - MOUSER_API_KEY (optional)
    echo.
    echo Press any key to open .env file...
    pause >nul
    notepad .env
)

echo [INFO] Starting n8n with Docker Compose...
docker-compose up -d

if errorlevel 1 (
    echo [ERROR] Failed to start containers
    pause
    exit /b 1
)

echo.
echo ========================================
echo  n8n is now running!
echo ========================================
echo.
echo  URL: http://localhost:5678
echo  Username: admin
echo  Password: admin123
echo.
echo  Next steps:
echo  1. Open http://localhost:5678 in your browser
echo  2. Import the workflow: AI_Hardware_Pipeline_Workflow.json
echo  3. Configure OpenAI credentials
echo  4. Activate the workflow
echo  5. Test with example requirements
echo.
echo ========================================

REM Wait a few seconds for n8n to start
timeout /t 5 /nobreak >nul

REM Try to open browser
start http://localhost:5678

echo.
echo Press any key to view logs (Ctrl+C to exit logs)...
pause >nul
docker-compose logs -f n8n
