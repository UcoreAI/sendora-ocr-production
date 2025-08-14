@echo off
echo ======================================================
echo SENDORA OCR - AUTOMATIC WKHTMLTOPDF INSTALLER
echo ======================================================
echo.
echo This will install wkhtmltopdf with minimal clicks required.
echo You'll just need to:
echo   1. Click "Yes" when Windows asks for permission
echo   2. Wait for installation to complete
echo.
pause

echo Requesting administrator privileges...
powershell -Command "Start-Process cmd -Verb RunAs -ArgumentList '/c cd /d \"%~dp0\" && AUTO_INSTALL_ADMIN.bat'"
goto :end

:end
echo Installation initiated. Please check the administrator window.
pause