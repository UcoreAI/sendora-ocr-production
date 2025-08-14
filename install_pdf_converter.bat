@echo off
echo ====================================================
echo SENDORA OCR V2.0 - PDF Converter Installation
echo ====================================================
echo.
echo This will help you install wkhtmltopdf for PDF generation.
echo.
echo Option 1: Manual Download (Recommended)
echo   1. Download from: https://wkhtmltopdf.org/downloads.html
echo   2. Choose: wkhtmltox-0.12.6.1.msvc2015-win64.exe
echo   3. Install with default settings
echo.
echo Option 2: Chocolatey (if you have it)
echo   choco install wkhtmltopdf
echo.
echo Option 3: Use HTML files (Current working method)
echo   - System generates HTML files
echo   - Open in browser and print to PDF (Ctrl+P)
echo.
pause
echo.
echo Testing if wkhtmltopdf is installed...
echo.

REM Test different possible locations
if exist "C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe" (
    echo [SUCCESS] Found wkhtmltopdf at: C:\Program Files\wkhtmltopdf\bin\
    "C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe" --version
    echo.
    echo Your system is ready for automatic PDF generation!
    goto :end
)

if exist "C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe" (
    echo [SUCCESS] Found wkhtmltopdf at: C:\Program Files ^(x86^)\wkhtmltopdf\bin\
    "C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe" --version
    echo.
    echo Your system is ready for automatic PDF generation!
    goto :end
)

wkhtmltopdf --version >nul 2>&1
if %errorlevel% == 0 (
    echo [SUCCESS] wkhtmltopdf is available in PATH
    wkhtmltopdf --version
    echo.
    echo Your system is ready for automatic PDF generation!
    goto :end
)

echo [INFO] wkhtmltopdf not found. 
echo.
echo Please install wkhtmltopdf using one of the options above.
echo The system will continue to work with HTML files until then.
echo.
echo Current status:
echo - HTML generation: WORKING
echo - PDF conversion: NEEDS wkhtmltopdf
echo - Web interface: WORKING at http://localhost:5000

:end
echo.
echo Press any key to continue...
pause >nul