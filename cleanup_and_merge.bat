@echo off
echo ============================================
echo   CLEANUP - Merge and Remove Files
echo ============================================
echo.
echo This will:
echo 1. Move ALL redundant documentation to backup folder
echo 2. Keep only 3 essential guide files
echo 3. Keep only essential scripts
echo.
echo BEFORE: 25+ files
echo AFTER: ~12 essential files
echo.
echo Files to KEEP:
echo.
echo GUIDES (3 files):
echo   - START_HERE.md (master guide - everything in one file)
echo   - WORKFLOW_GUIDE.md (workflow details)
echo   - README.md (technical reference)
echo.
echo SCRIPTS (5 files):
echo   - setup_and_start.bat
echo   - check_status.bat
echo   - test_simple.bat
echo   - start.bat
echo   - stop.bat
echo.
echo CORE (4 files):
echo   - AI_Hardware_Pipeline_Workflow.json
echo   - docker-compose.yml
echo   - .env
echo   - .env.example
echo.
echo All other files will be moved to backup folder.
echo.
pause
echo.

echo Creating backup folder...
if not exist "backup" mkdir backup

echo.
echo Moving redundant files to backup folder...

REM Move all redundant guides
if exist "INDEX.md" move "INDEX.md" "backup\" >nul && echo [MOVED] INDEX.md
if exist "INSTANT_START.md" move "INSTANT_START.md" "backup\" >nul && echo [MOVED] INSTANT_START.md
if exist "SIMPLE_START_GUIDE.md" move "SIMPLE_START_GUIDE.md" "backup\" >nul && echo [MOVED] SIMPLE_START_GUIDE.md
if exist "COMPLETE_GUIDE.md" move "COMPLETE_GUIDE.md" "backup\" >nul && echo [MOVED] COMPLETE_GUIDE.md
if exist "README_FIRST.md" move "README_FIRST.md" "backup\" >nul && echo [MOVED] README_FIRST.md
if exist "FILE_GUIDE.md" move "FILE_GUIDE.md" "backup\" >nul && echo [MOVED] FILE_GUIDE.md
if exist "QUICKSTART.md" move "QUICKSTART.md" "backup\" >nul && echo [MOVED] QUICKSTART.md

REM Move dev/advanced files
if exist "CHATBOT_UPDATE.md" move "CHATBOT_UPDATE.md" "backup\" >nul && echo [MOVED] CHATBOT_UPDATE.md
if exist "GITHUB_DEPLOYMENT.md" move "GITHUB_DEPLOYMENT.md" "backup\" >nul && echo [MOVED] GITHUB_DEPLOYMENT.md
if exist "workflow_steps.txt" move "workflow_steps.txt" "backup\" >nul && echo [MOVED] workflow_steps.txt

REM Move redundant scripts
if exist "verify_setup.bat" move "verify_setup.bat" "backup\" >nul && echo [MOVED] verify_setup.bat
if exist "test_workflow.bat" move "test_workflow.bat" "backup\" >nul && echo [MOVED] test_workflow.bat

REM Move this cleanup script to backup too
move "cleanup_files.bat" "backup\" >nul 2>&1 && echo [MOVED] cleanup_files.bat

echo.
echo ============================================
echo   CLEANUP COMPLETE!
echo ============================================
echo.
echo Your project is now clean and organized!
echo.
echo ESSENTIAL FILES (12 total):
echo.
echo [START HERE]
echo   START_HERE.md          - Everything you need in ONE file!
echo.
echo [Additional Guides]
echo   WORKFLOW_GUIDE.md      - Phase-by-phase workflow details
echo   README.md              - Technical reference
echo.
echo [Scripts]
echo   setup_and_start.bat    - One-click setup
echo   check_status.bat       - Verify setup
echo   test_simple.bat        - Test workflow
echo   start.bat              - Start n8n
echo   stop.bat               - Stop n8n
echo.
echo [Core Files]
echo   AI_Hardware_Pipeline_Workflow.json
echo   docker-compose.yml
echo   .env
echo   .env.example
echo.
echo [Directories]
echo   workflows/
echo   output/
echo   backup/  (redundant files here - can delete later)
echo.
echo.
echo Next Steps:
echo   1. Open START_HERE.md
echo   2. Follow the Quick Start section
echo   3. Win your hackathon!
echo.
pause
