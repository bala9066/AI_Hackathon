@echo off
echo Copying output files from n8n container...
if not exist "output" mkdir output

docker cp n8n_ai_hardware_pipeline:/home/node/.n8n/block_diagram.json ./output/ 2>nul
docker cp n8n_ai_hardware_pipeline:/home/node/.n8n/block_diagram.md ./output/ 2>nul
docker cp n8n_ai_hardware_pipeline:/home/node/.n8n/component_options.csv ./output/ 2>nul
docker cp n8n_ai_hardware_pipeline:/home/node/.n8n/BOM.csv ./output/ 2>nul
docker cp n8n_ai_hardware_pipeline:/home/node/.n8n/Power_Budget.csv ./output/ 2>nul
docker cp n8n_ai_hardware_pipeline:/home/node/.n8n/RF_Analysis.csv ./output/ 2>nul

echo.
echo Files copied to AG/output/ folder!
dir output
pause
