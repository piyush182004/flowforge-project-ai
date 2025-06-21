@echo off
echo Starting FlowForge Backend Server...
echo.
echo The server will run continuously.
echo Press Ctrl+C to stop the server.
echo.
echo Backend will be available at: http://localhost:5000
echo Health check: http://localhost:5000/api/health
echo.
python app.py
pause 