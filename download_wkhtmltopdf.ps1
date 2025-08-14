# PowerShell script to download and install wkhtmltopdf
Write-Host "======================================================"
Write-Host "DOWNLOADING WKHTMLTOPDF INSTALLER"
Write-Host "======================================================"

$downloadUrl = "https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltox-0.12.6.1-2.msvc2015-win64.exe"
$installerPath = "$env:USERPROFILE\Desktop\wkhtmltopdf_installer.exe"

try {
    Write-Host "Downloading from GitHub..."
    Write-Host "This may take a minute..."
    
    # Use .NET WebClient for more reliable download
    $webClient = New-Object System.Net.WebClient
    $webClient.DownloadFile($downloadUrl, $installerPath)
    
    if (Test-Path $installerPath) {
        $fileSize = (Get-Item $installerPath).Length / 1MB
        Write-Host "SUCCESS! Downloaded wkhtmltopdf installer" -ForegroundColor Green
        Write-Host "File size: $([math]::Round($fileSize, 2)) MB"
        Write-Host "Location: $installerPath"
        Write-Host ""
        Write-Host "Starting installation..." -ForegroundColor Yellow
        Write-Host "Please follow the installer prompts"
        
        # Start the installer
        Start-Process -FilePath $installerPath -Wait
        
        # Check if installation succeeded
        $installPath = "C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
        if (Test-Path $installPath) {
            Write-Host ""
            Write-Host "SUCCESS! wkhtmltopdf installed successfully!" -ForegroundColor Green
            & $installPath --version
            Write-Host ""
            Write-Host "Your system is now ready for automatic PDF generation!" -ForegroundColor Green
            Write-Host "The Flask app will now generate PDFs automatically." -ForegroundColor Green
        } else {
            Write-Host "Installation completed. Please verify installation manually." -ForegroundColor Yellow
        }
    } else {
        Write-Host "Download failed. File not found at expected location." -ForegroundColor Red
    }
    
} catch {
    Write-Host "Error during download: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Alternative: Manual download" -ForegroundColor Yellow
    Write-Host "Opening download page in browser..."
    Start-Process "https://github.com/wkhtmltopdf/packaging/releases/tag/0.12.6.1-2"
}

Write-Host ""
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")