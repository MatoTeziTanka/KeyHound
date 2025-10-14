# KeyHound Enhanced - GitHub Project Setup Script
Write-Host "🚀 KeyHound Enhanced - GitHub Project Setup" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "This script will automatically set up your GitHub project with:" -ForegroundColor Yellow
Write-Host "- All necessary labels" -ForegroundColor White
Write-Host "- Project milestones" -ForegroundColor White  
Write-Host "- Issues for completed work" -ForegroundColor White
Write-Host "- Issues for future priorities" -ForegroundColor White
Write-Host ""

Write-Host "📋 Prerequisites:" -ForegroundColor Yellow
Write-Host "1. GitHub Personal Access Token with repo, project, and issues scopes" -ForegroundColor White
Write-Host "2. Python 3.6+ installed" -ForegroundColor White
Write-Host "3. requests library installed" -ForegroundColor White
Write-Host ""

Write-Host "🔑 To get your GitHub token:" -ForegroundColor Yellow
Write-Host "1. Go to: https://github.com/settings/tokens" -ForegroundColor White
Write-Host "2. Click 'Generate new token (classic)'" -ForegroundColor White
Write-Host "3. Select scopes: repo, project, issues" -ForegroundColor White
Write-Host "4. Copy the token" -ForegroundColor White
Write-Host ""

# Get GitHub token
$token = Read-Host "Enter your GitHub token"

if ([string]::IsNullOrEmpty($token)) {
    Write-Host "❌ No token provided. Exiting." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "🔧 Setting environment variable..." -ForegroundColor Yellow
$env:GITHUB_TOKEN = $token

Write-Host ""
Write-Host "🐍 Installing required packages..." -ForegroundColor Yellow
try {
    pip install requests
    Write-Host "✅ requests library installed" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to install requests library" -ForegroundColor Red
    Write-Host "Please install manually: pip install requests" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "🚀 Running GitHub project setup..." -ForegroundColor Yellow
try {
    python scripts/setup_github_project.py
    Write-Host ""
    Write-Host "✅ Setup complete!" -ForegroundColor Green
    Write-Host "View your project: https://github.com/sethpizzaboy/KeyHound" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Setup failed. Check the error messages above." -ForegroundColor Red
}

Write-Host ""
Read-Host "Press Enter to exit"
