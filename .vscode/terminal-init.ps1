# VSCode Terminal Initialization Script for Windows PowerShell
# This script runs automatically when you open a new terminal in VSCode

# Define helpful functions for Python virtual environment
function setup-venv {
    # Call the batch file which has all the setup logic
    # This keeps the code in one place and easier to maintain
    if (Test-Path "setup.bat") {
        cmd /c setup.bat
        # After setup.bat completes, activate the environment in PowerShell
        if (Test-Path ".venv\Scripts\Activate.ps1") {
            Write-Host ""
            Write-Host "🔄 Activating in PowerShell..." -ForegroundColor Cyan
            .\.venv\Scripts\Activate.ps1
        }
    } else {
        Write-Host "❌ setup.bat not found!" -ForegroundColor Red
        Write-Host "   Make sure you're in the project directory." -ForegroundColor Yellow
    }
}

function activate {
    if (Test-Path ".venv\Scripts\Activate.ps1") {
        .\.venv\Scripts\Activate.ps1
        Write-Host "🐍 Virtual environment activated!" -ForegroundColor Green
        # Auto-install any new packages from requirements.txt
        if (Test-Path "requirements.txt") {
            Write-Host "📦 Checking for new packages..." -ForegroundColor Cyan
            pip install -r requirements.txt --quiet
        }
    } else {
        Write-Host "❌ No virtual environment found." -ForegroundColor Red
        Write-Host "   Run: setup-venv" -ForegroundColor Yellow
    }
}

function install-req {
    if (Test-Path "requirements.txt") {
        Write-Host "📦 Installing packages from requirements.txt..." -ForegroundColor Cyan
        pip install -r requirements.txt
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Packages installed successfully!" -ForegroundColor Green
        }
    } else {
        Write-Host "❌ requirements.txt not found!" -ForegroundColor Red
        Write-Host "   Make sure you're in the project directory." -ForegroundColor Yellow
    }
}

# Check if virtual environment exists and auto-activate
if (Test-Path ".venv\Scripts\Activate.ps1") {
    .\.venv\Scripts\Activate.ps1
    Write-Host "🐍 Virtual environment activated!" -ForegroundColor Green
    Write-Host "   Ready to code! Run: python main.py" -ForegroundColor Yellow
} else {
    Write-Host "💡 Welcome! No virtual environment found yet." -ForegroundColor Cyan
    Write-Host "   Run this command to set up everything: setup-venv" -ForegroundColor Yellow
}

Write-Host ""
