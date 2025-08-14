@echo off
echo ========================================
echo    SENDORA OCR SYSTEM STARTUP
echo ========================================
echo.

cd /d "%~dp0"

echo 🔍 Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found! Please install Python 3.8+
    pause
    exit /b 1
)

echo ✅ Python found

echo 🔍 Checking dependencies...
pip show flask >nul 2>&1
if %errorlevel% neq 0 (
    echo 📦 Installing dependencies...
    pip install -r requirements.txt
)

echo ✅ Dependencies ready

echo 🔧 Setting up environment...
if not exist ".env" (
    copy "config\.env" ".env"
    echo ✅ Environment file copied
)

echo.
echo 🚀 Starting Sendora OCR System...
echo 📁 Template Overlay: ACTIVE
echo 🔑 Azure OCR: CONFIGURED
echo 🌐 Opening: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo ========================================

python start_server.py

pause