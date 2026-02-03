@echo off
echo ============================================
echo   AI HARDWARE PIPELINE - SETUP AND START
echo ============================================
echo.

REM Check if Docker is installed
echo [1/4] Checking Docker installation...
docker --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not installed!
    echo.
    echo Please install Docker Desktop from:
    echo https://www.docker.com/products/docker-desktop
    echo.
    pause
    exit /b 1
)
echo [OK] Docker is installed.
echo.

REM Check if Docker is running
echo [2/4] Checking if Docker is running...
docker ps >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Docker is not running.
    echo [ACTION] Starting Docker Desktop...
    start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    echo Waiting 30 seconds for Docker to start...
    timeout /t 30 /nobreak >nul
    
    REM Check again
    docker ps >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] Docker failed to start. Please start Docker Desktop manually.
        echo After Docker is running, run this script again.
        pause
        exit /b 1
    )
)
echo [OK] Docker is running.
echo.

REM Check if .env file exists
echo [3/4] Checking configuration...
if not exist ".env" (
    echo [WARNING] .env file not found!
    if exist ".env.example" (
        echo [ACTION] Creating .env from .env.example...
        copy .env.example .env >nul
        echo.
        echo [IMPORTANT] Please edit .env file and add your OpenAI API key!
        echo Opening .env in Notepad...
        notepad .env
        echo.
        echo After adding your API key, press any key to continue...
        pause >nul
    ) else (
        echo [ERROR] .env.example not found. Cannot create .env file.
        pause
        exit /b 1
    )
)
echo [OK] Configuration file exists.
echo.

REM Start n8n
echo [4/4] Starting n8n...
echo This may take 30-60 seconds...
echo.
docker-compose up -d

if errorlevel 1 (
    echo [ERROR] Failed to start n8n!
    echo.
    echo Troubleshooting:
    echo 1. Make sure Docker Desktop is running
    echo 2. Check docker-compose.yml exists
    echo 3. Run: docker-compose logs -f
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================
echo   SUCCESS! n8n is starting...
echo ============================================
echo.
echo Waiting for n8n to be ready (30 seconds)...
timeout /t 30 /nobreak >nul

echo.
echo n8n should now be running at: http://localhost:5678
echo.
echo Login credentials:
echo   Username: admin
echo   Password: admin123
echo.
echo Opening browser...
start http://localhost:5678

echo.
echo [NEXT STEPS]
echo 1. Login to n8n
echo 2. Import AI_Hardware_Pipeline_Workflow.json
echo 3. Add your OpenAI API key in credentials
echo 4. Activate the workflow
echo 5. Run test_workflow.bat
echo.
echo Press any key to exit...
pause >nul
