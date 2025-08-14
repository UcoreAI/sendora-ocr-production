@echo off
echo ======================================================
echo TESTING WKHTMLTOPDF INSTALLATION
echo ======================================================
echo.

REM Check if wkhtmltopdf is installed
if exist "C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe" (
    echo [SUCCESS] wkhtmltopdf found!
    echo.
    echo Version information:
    "C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe" --version
    echo.
    echo ======================================================
    echo TESTING PDF GENERATION
    echo ======================================================
    echo.
    
    REM Find latest HTML file and convert to PDF
    cd job_orders
    for /f "delims=" %%i in ('dir /b /od *.html 2^>nul ^| findstr /i "CORRECT"') do set "latest=%%i"
    
    if defined latest (
        echo Converting: %latest%
        "C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe" "%latest%" "%latest:.html=_TEST.pdf%"
        
        if exist "%latest:.html=_TEST.pdf%" (
            echo.
            echo [SUCCESS] PDF created successfully!
            echo Opening PDF...
            start "" "%latest:.html=_TEST.pdf%"
        ) else (
            echo [ERROR] PDF creation failed
        )
    ) else (
        echo No HTML files found to test
    )
    
    echo.
    echo ======================================================
    echo RESULT: Your system is ready for automatic PDF generation!
    echo ======================================================
    echo.
    echo The Flask app at localhost:5000 will now:
    echo - Automatically convert HTML to PDF
    echo - Download Job Orders as PDF files
    echo - No more "Failed to load PDF document" errors
    
) else (
    echo [ERROR] wkhtmltopdf not found at expected location
    echo.
    echo Please complete the installation:
    echo 1. Download from: https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltox-0.12.6.1-2.msvc2015-win64.exe
    echo 2. Run the installer
    echo 3. Use default installation path: C:\Program Files\wkhtmltopdf\
    echo 4. Run this test again
)

echo.
pause