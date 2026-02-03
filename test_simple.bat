@echo off
echo ============================================
echo   TESTING AI HARDWARE PIPELINE
echo ============================================
echo.

echo Sending test request to workflow...
echo.
echo Test: Simple IoT Sensor Design
echo.

curl -X POST http://localhost:5678/webhook/ai-hardware-pipeline ^
  -H "Content-Type: application/json" ^
  -d "{\"requirements\": \"Design simple IoT temperature sensor with ESP32, DHT22 sensor, battery powered, WiFi enabled, MQTT protocol\"}"

echo.
echo.
echo ============================================
echo   TEST COMPLETE
echo ============================================
echo.
echo Check the n8n UI to see workflow execution:
echo http://localhost:5678
echo.
echo Click "Executions" to see the results.
echo.
echo The workflow will generate:
echo - Component BOM with prices
echo - Block diagram  
echo - Hardware Requirements Document (HRS)
echo - Compliance report
echo - And more!
echo.
pause
