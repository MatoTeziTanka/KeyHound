@echo off
echo 🚀 KeyHound Enhanced - GitHub Project Setup
echo ================================================

echo.
echo This script will automatically set up your GitHub project with:
echo - All necessary labels
echo - Project milestones  
echo - Issues for completed work
echo - Issues for future priorities
echo.

echo 📋 Prerequisites:
echo 1. GitHub Personal Access Token with repo, project, and issues scopes
echo 2. Python 3.6+ installed
echo 3. requests library installed (pip install requests)
echo.

echo 🔑 To get your GitHub token:
echo 1. Go to: https://github.com/settings/tokens
echo 2. Click "Generate new token (classic)"
echo 3. Select scopes: repo, project, issues
echo 4. Copy the token
echo.

set /p GITHUB_TOKEN="Enter your GitHub token: "

if "%GITHUB_TOKEN%"=="" (
    echo ❌ No token provided. Exiting.
    pause
    exit /b 1
)

echo.
echo 🔧 Setting environment variable...
set GITHUB_TOKEN=%GITHUB_TOKEN%

echo.
echo 🐍 Installing required packages...
pip install requests

echo.
echo 🚀 Running GitHub project setup...
python scripts/setup_github_project.py

echo.
echo ✅ Setup complete! 
echo View your project: https://github.com/sethpizzaboy/KeyHound
echo.

pause
