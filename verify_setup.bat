@echo off
echo ========================================
echo AI Hardware Pipeline - Setup Verification
echo ========================================
echo.

set ERRORS=0

REM Check Docker
echo [1/5] Checking Docker...
docker --version >nul 2>&1
if errorlevel 1 (
    echo   [X] Docker not found! Please install Docker Desktop
    set /a ERRORS+=1
) else (
    docker --version
    echo   [OK] Docker installed
)
echo.

REM Check Docker running
echo [2/5] Checking if Docker is running...
docker info >nul 2>&1
if errorlevel 1 (
    echo   [X] Docker is not running! Please start Docker Desktop
    set /a ERRORS+=1
) else (
    echo   [OK] Docker is running
)
echo.

REM Check .env file
echo [3/5] Checking environment configuration...
if not exist .env (
    echo   [!] .env file not found
    echo   [INFO] Creating from template...
    copy .env.example .env >nul
    echo   [OK] .env created - Please edit and add your API keys
) else (
    echo   [OK] .env file exists
)
echo.

REM Check required files
echo [4/5] Checking required files...
set FILES_OK=1

if not exist docker-compose.yml (
    echo   [X] docker-compose.yml missing
    set FILES_OK=0
    set /a ERRORS+=1
)

if not exist AI_Hardware_Pipeline_Workflow.json (
    echo   [X] AI_Hardware_Pipeline_Workflow.json missing
    set FILES_OK=0
    set /a ERRORS+=1
)

if not exist README.md (
    echo   [X] README.md missing
    set FILES_OK=0
    set /a ERRORS+=1
)

if %FILES_OK%==1 (
    echo   [OK] All required files present
)
echo.

REM Check directories
echo [5/5] Checking directories...
if not exist workflows (
    echo   [INFO] Creating workflows directory...
    mkdir workflows
)
if not exist output (
    echo   [INFO] Creating output directory...
    mkdir output
)
echo   [OK] Directory structure ready
echo.

REM Summary
echo ========================================
echo Setup Verification Summary
echo ========================================
echo.

if %ERRORS% EQU 0 (
    echo   STATUS: [OK] Ready to start!
    echo.
    echo   Next steps:
    echo   1. Edit .env file and add your OpenAI API key
    echo   2. Run: start.bat
    echo   3. Open: http://localhost:5678
    echo   4. Import workflow: AI_Hardware_Pipeline_Workflow.json
    echo.
) else (
    echo   STATUS: [ERROR] Please fix the issues above
    echo.
)

echo ========================================
pause
