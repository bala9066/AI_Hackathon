@echo off
echo ========================================
echo Testing AI Hardware Pipeline Workflow
echo ========================================
echo.

REM Check if n8n is running
curl -s http://localhost:5678 >nul 2>&1
if errorlevel 1 (
    echo [ERROR] n8n is not running!
    echo Please run start.bat first
    pause
    exit /b 1
)

echo [OK] n8n is running
echo.

echo ========================================
echo Test 1: Simple IoT Device
echo ========================================
echo.

curl -X POST http://localhost:5678/webhook/ai-hardware-pipeline ^
  -H "Content-Type: application/json" ^
  -d "{\"requirements\": \"Design IoT sensor board with ESP32, temperature sensor, battery powered\"}"

echo.
echo.
echo ========================================
echo Test 2: RF/FPGA System (Complex)
echo ========================================
echo.

curl -X POST http://localhost:5678/webhook/ai-hardware-pipeline ^
  -H "Content-Type: application/json" ^
  -d "{\"requirements\": \"Design RF system with Xilinx Artix-7 FPGA, buck-boost converters, 40dBm output power, 5-18GHz frequency range, return loss > 10dB\"}"

echo.
echo.
echo ========================================
echo Tests completed!
echo ========================================
echo.
echo Check the n8n interface for execution results:
echo http://localhost:5678/workflows
echo.
pause
