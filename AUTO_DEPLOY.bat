@echo off
echo ========================================
echo    SENDORA OCR AUTO DEPLOYMENT HELPER
echo ========================================
echo.

echo Step 1: Preparing GitHub repository...
echo.
echo 1. Go to: https://github.com/new
echo 2. Repository name: sendora-ocr-production
echo 3. Description: Sendora OCR V2.0 - 95%% accuracy automated Job Order generation
echo 4. Make it PUBLIC
echo 5. DO NOT check "Initialize with README"
echo 6. Click "Create repository"
echo.
echo After creation, GitHub will show commands like:
echo git remote add origin https://github.com/YOURUSERNAME/sendora-ocr-production.git
echo.
set /p username="Enter your GitHub username: "

echo.
echo Step 2: Pushing to GitHub...
echo.
cd "%~dp0"
echo Current directory: %cd%

echo Adding remote repository...
git remote add origin https://github.com/%username%/sendora-ocr-production.git

echo Pushing to main branch...
git branch -M main
git push -u origin main

if %errorlevel% equ 0 (
    echo ✅ SUCCESS: Code pushed to GitHub!
    echo.
    echo Your repository: https://github.com/%username%/sendora-ocr-production
) else (
    echo ❌ ERROR: Git push failed. Please check:
    echo 1. GitHub repository exists and is public
    echo 2. Your GitHub username is correct
    echo 3. You have push permissions
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo    NEXT: CREATE ELESTIO SERVICE
echo ========================================
echo.
echo 1. Go to: https://elestio.com/register
echo 2. Sign up and verify email
echo 3. Add payment method
echo 4. Click "Create New Service"
echo 5. Select "Docker"
echo 6. Configure:
echo    - Service Name: sendora-ocr-demo
echo    - Plan: Standard (2GB RAM, 2 CPU) - $14/month
echo    - Region: Choose closest to you
echo 7. Click "Create Service"
echo.
echo After service is created:
echo 1. Note your service domain (e.g., sendora-ocr-u123.vm.elestio.app)
echo 2. Note SSH credentials from dashboard
echo 3. Use SSH to connect to your VPS
echo 4. Run these commands on your VPS:
echo.
echo cd /opt
echo git clone https://github.com/%username%/sendora-ocr-production.git
echo cd sendora-ocr-production
echo mkdir -p config uploads job_orders temp logs
echo chmod 755 uploads job_orders temp logs
echo.
echo 5. Upload google-credentials.json to config/ folder
echo 6. Run: chmod +x deploy.sh
echo 7. Run: export ELESTIO_DOMAIN="your-actual-domain.vm.elestio.app"
echo 8. Run: ./deploy.sh
echo.
echo ========================================
echo    DEPLOYMENT READY!
echo ========================================
echo.
echo Your GitHub repository: https://github.com/%username%/sendora-ocr-production
echo Next step: Create Elestio account and service
echo Full guide: Open ELESTIO_DEPLOYMENT_GUIDE.md
echo Quick commands: Open QUICK_DEPLOY_COMMANDS.md
echo.
pause