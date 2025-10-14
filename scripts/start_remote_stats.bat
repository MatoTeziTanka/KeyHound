@echo off
echo ============================================================
echo KeyHound Enhanced - Remote Statistics Server
echo ============================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Check if we're in the right directory
if not exist "main.py" (
    echo ERROR: Please run this script from the KeyHound root directory
    echo Current directory: %CD%
    pause
    exit /b 1
)

REM Start the remote stats server
echo Starting Remote Statistics Server...
echo.
echo Dashboard will be available at: http://localhost:8080
echo For external access, use: http://YOUR_IP_ADDRESS:8080
echo.
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

python scripts/start_remote_stats.py --host 0.0.0.0 --port 8080

echo.
echo Server stopped.
pause
