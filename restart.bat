@echo off
echo Stopping any running Python servers...
taskkill /f /im python.exe 2>nul
echo.
echo Waiting for processes to terminate...
timeout /t 2 /nobreak > nul
echo.

echo Creating sounds directory if it doesn't exist...
mkdir "static\sounds" 2>nul

echo Starting Exit Management System server...
cd /c/4_EXITECH
start cmd /k "python app.py"
echo.
echo Server restarted! Exit logs will now:
echo - Update in real-time with Socket.IO
echo - Cache to localStorage
echo - Reload from database on refresh
echo. 