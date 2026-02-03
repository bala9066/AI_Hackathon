@echo off
echo ============================================
echo   FILE CLEANUP - Remove Redundant Files
echo ============================================
echo.
echo This will remove duplicate documentation files
echo and keep only the essential ones.
echo.
echo FILES TO REMOVE (redundant documentation):
echo - CHATBOT_UPDATE.md (dev notes)
echo - GITHUB_DEPLOYMENT.md (advanced, not needed for basic use)
echo - workflow_steps.txt (raw notes, info is in guides)
echo - verify_setup.bat (duplicate of check_status.bat)
echo - test_workflow.bat (duplicate of test_simple.bat)
echo.
echo FILES TO KEEP (essential):
echo - INDEX.md (master navigation)
echo - INSTANT_START.md (quick start)
echo - SIMPLE_START_GUIDE.md (detailed guide)
echo - COMPLETE_GUIDE.md (full reference)
echo - WORKFLOW_GUIDE.md (workflow details)
echo - README.md (full documentation)
echo.
echo - All .bat scripts (setup, start, stop, check, test)
echo - AI_Hardware_Pipeline_Workflow.json (the workflow!)
echo - docker-compose.yml, .env, .env.example
echo.
pause
echo.

echo Creating backup folder...
if not exist "backup" mkdir backup

echo.
echo Moving redundant files to backup folder...

if exist "CHATBOT_UPDATE.md" (
    move "CHATBOT_UPDATE.md" "backup\" >nul
    echo [MOVED] CHATBOT_UPDATE.md
)

if exist "GITHUB_DEPLOYMENT.md" (
    move "GITHUB_DEPLOYMENT.md" "backup\" >nul
    echo [MOVED] GITHUB_DEPLOYMENT.md
)

if exist "workflow_steps.txt" (
    move "workflow_steps.txt" "backup\" >nul
    echo [MOVED] workflow_steps.txt
)

if exist "verify_setup.bat" (
    move "verify_setup.bat" "backup\" >nul
    echo [MOVED] verify_setup.bat
)

if exist "test_workflow.bat" (
    move "test_workflow.bat" "backup\" >nul
    echo [MOVED] test_workflow.bat
)

REM Remove some of the redundant new guides (keep the best ones)
if exist "README_FIRST.md" (
    move "README_FIRST.md" "backup\" >nul
    echo [MOVED] README_FIRST.md (redundant with INDEX.md)
)

if exist "FILE_GUIDE.md" (
    move "FILE_GUIDE.md" "backup\" >nul
    echo [MOVED] FILE_GUIDE.md (info is in COMPLETE_GUIDE.md)
)

if exist "QUICKSTART.md" (
    move "QUICKSTART.md" "backup\" >nul
    echo [MOVED] QUICKSTART.md (redundant with SIMPLE_START_GUIDE.md)
)

if exist "START_HERE.md" (
    move "START_HERE.md" "backup\" >nul
    echo [MOVED] START_HERE.md (redundant with COMPLETE_GUIDE.md)
)

echo.
echo ============================================
echo   CLEANUP COMPLETE!
echo ============================================
echo.
echo Removed/moved files are in the 'backup' folder.
echo You can delete the backup folder later if you want.
echo.
echo ESSENTIAL FILES REMAINING:
echo.
echo START HERE:
echo   - INDEX.md (read this first)
echo.
echo GUIDES (pick one):
echo   - INSTANT_START.md (fastest)
echo   - SIMPLE_START_GUIDE.md (recommended)
echo   - COMPLETE_GUIDE.md (comprehensive)
echo   - WORKFLOW_GUIDE.md (workflow phases)
echo   - README.md (full reference)
echo.
echo SCRIPTS:
echo   - setup_and_start.bat (setup and start n8n)
echo   - check_status.bat (verify setup)
echo   - test_simple.bat (test workflow)
echo   - start.bat (start n8n)
echo   - stop.bat (stop n8n)
echo.
echo WORKFLOW:
echo   - AI_Hardware_Pipeline_Workflow.json
echo.
echo CONFIG:
echo   - docker-compose.yml
echo   - .env
echo.
pause
