# PowerShell script to install wkhtmltopdf
Write-Host "======================================================"
Write-Host "SENDORA OCR V2.0 - Installing wkhtmltopdf"
Write-Host "======================================================"

$downloadUrl = "https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-3/wkhtmltox-0.12.6.1.msvc2015-win64.exe"
$installerPath = "$env:TEMP\wkhtmltopdf_installer.exe"

try {
    Write-Host "Downloading wkhtmltopdf installer..."
    Invoke-WebRequest -Uri $downloadUrl -OutFile $installerPath -UseBasicParsing
    
    Write-Host "Running installer..."
    Start-Process -FilePath $installerPath -ArgumentList "/S" -Wait -NoNewWindow
    
    Write-Host "Cleaning up..."
    Remove-Item $installerPath -Force -ErrorAction SilentlyContinue
    
    Write-Host "Testing installation..."
    $wkhtmltopdfPath = "C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
    
    if (Test-Path $wkhtmltopdfPath) {
        Write-Host "SUCCESS! wkhtmltopdf installed successfully" -ForegroundColor Green
        & $wkhtmltopdfPath --version
        Write-Host ""
        Write-Host "Your system is now ready for automatic PDF generation!" -ForegroundColor Green
        Write-Host "Restart your Flask app to use the new PDF converter." -ForegroundColor Yellow
    } else {
        Write-Host "Installation completed but wkhtmltopdf not found at expected location" -ForegroundColor Yellow
        Write-Host "Please restart your command prompt and try again" -ForegroundColor Yellow
    }
    
} catch {
    Write-Host "Error during installation: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Manual installation steps:" -ForegroundColor Yellow
    Write-Host "1. Visit: https://wkhtmltopdf.org/downloads.html"
    Write-Host "2. Download: wkhtmltox-0.12.6.1.msvc2015-win64.exe"
    Write-Host "3. Run the installer with default settings"
}

Write-Host ""
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")