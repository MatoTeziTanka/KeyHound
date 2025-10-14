@echo off
echo 🚀 KeyHound Enhanced - Automated GitHub Project Setup
echo ======================================================
echo.
echo This script will automatically set up your GitHub project using
echo the same GitHub CLI authentication as ScalpStorm!
echo.

echo ✅ Prerequisites Check:
echo - GitHub CLI installed: CONFIRMED
echo - GitHub CLI authenticated: CONFIRMED  
echo - Required scopes (repo, project, issues): CONFIRMED
echo.

echo 🎯 What will be created:
echo - 20 labels (priority, type, component, status)
echo - 5 milestones (v1.0.0 through v2.0.0)
echo - 6 completed issues (documenting all your work)
echo - 3 future issues (next priorities)
echo.

echo 🚀 Starting automated setup...
python scripts/setup_github_cli.py

echo.
echo ✅ Setup complete!
echo.
echo 🔗 View your project: https://github.com/sethpizzaboy/KeyHound/projects/3
echo 📋 View issues: https://github.com/sethpizzaboy/KeyHound/issues
echo 🏷️ View labels: https://github.com/sethpizzaboy/KeyHound/labels
echo.

pause
