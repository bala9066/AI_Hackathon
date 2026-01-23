@echo off
echo ========================================
echo Stopping AI Hardware Pipeline
echo ========================================
echo.

docker-compose down

echo.
echo [OK] All containers stopped
echo.
echo To restart, run: start.bat
echo.
pause
