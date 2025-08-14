@echo off
echo ======================================================
echo INSTALLING WKHTMLTOPDF (ADMINISTRATOR MODE)
echo ======================================================
echo.

REM Check if already installed
if exist "C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe" (
    echo wkhtmltopdf is already installed!
    goto :test
)

echo Method 1: Trying winget...
winget install wkhtmltopdf.wkhtmltopdf --accept-source-agreements --accept-package-agreements --silent
if exist "C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe" goto :success

echo.
echo Method 2: Trying chocolatey...
where choco >nul 2>nul
if errorlevel 1 (
    echo Installing chocolatey first...
    powershell -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))"
    SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"
)

choco install wkhtmltopdf -y
if exist "C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe" goto :success

echo.
echo Method 3: Direct download and install...
powershell -Command "$ProgressPreference = 'SilentlyContinue'; Invoke-WebRequest -Uri 'https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltox-0.12.6.1-2.msvc2015-win64.exe' -OutFile '$env:TEMP\wkhtmltopdf.exe'; Start-Process '$env:TEMP\wkhtmltopdf.exe' -ArgumentList '/S' -Wait; Remove-Item '$env:TEMP\wkhtmltopdf.exe' -Force"

timeout /t 5 /nobreak
if exist "C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe" goto :success

echo.
echo Manual installation required. Opening download page...
start https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltox-0.12.6.1-2.msvc2015-win64.exe
goto :end

:success
echo.
echo ======================================================
echo SUCCESS! WKHTMLTOPDF INSTALLED
echo ======================================================

:test
echo Testing installation...
"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe" --version
echo.

REM Test with actual HTML file
cd "%~dp0"
if exist "job_orders" (
    cd job_orders
    for /f "delims=" %%i in ('dir /b /od *.html 2^>nul ^| findstr /i "CORRECT"') do set "latest=%%i"
    
    if defined latest (
        echo Testing PDF conversion with: !latest!
        "C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe" "!latest!" "TEST_PDF_OUTPUT.pdf"
        
        if exist "TEST_PDF_OUTPUT.pdf" (
            echo.
            echo SUCCESS! PDF created and opening...
            start "" "TEST_PDF_OUTPUT.pdf"
        )
    )
)

echo.
echo ======================================================
echo INSTALLATION COMPLETE!
echo ======================================================
echo.
echo Your Flask app will now automatically generate PDFs!
echo Restart the Flask server to enable PDF generation.
echo.

:end
echo.
pause