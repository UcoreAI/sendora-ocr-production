@echo off
echo Opening latest Job Order in browser...
cd job_orders
for /f "delims=" %%i in ('dir /b /od *.html 2^>nul ^| findstr /i "JO_CORRECT"') do set "latest=%%i"
if defined latest (
    echo Opening %latest%...
    start "" "%latest%"
) else (
    echo No Job Order HTML files found.
)
pause