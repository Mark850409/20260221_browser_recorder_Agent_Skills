@echo off
set CHROME_PATH=C:\Program Files\Google\Chrome\Application\chrome.exe
set PROFILE_DIR=%~dp0..\chrome_profile

echo Closing existing Chrome instances...
taskkill /f /im chrome.exe >nul 2>&1
timeout /t 2 /nobreak >nul

if not exist "%PROFILE_DIR%" mkdir "%PROFILE_DIR%"

echo Starting Chrome with remote debugging on port 9222...
echo Allow Origins: *
start "" "%CHROME_PATH%" --remote-debugging-port=9222 --remote-allow-origins=* --user-data-dir="%PROFILE_DIR%" --no-first-run --no-default-browser-check

echo.
echo Chrome started! 
echo Remote debugging available at http://localhost:9222
echo Please keep this window open while running macros.
timeout /t 5
