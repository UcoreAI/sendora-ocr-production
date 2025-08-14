@echo off
echo ====================================
echo  Google Document AI Setup Helper
echo ====================================
echo.
echo This script will open the required Google Cloud pages
echo Follow each step and press any key to continue
echo.
pause

echo Step 1: Open Google Cloud Console
echo Create project named: sendora-ocr-project
start https://console.cloud.google.com
echo.
echo - Click project dropdown (top left)
echo - Click "NEW PROJECT"
echo - Name: sendora-ocr-project
echo - Click CREATE
echo.
pause

echo Step 2: Enable billing (get $300 free credit)
start https://console.cloud.google.com/billing
echo.
echo - Click "Link a billing account"
echo - Click "CREATE BILLING ACCOUNT"
echo - Enter payment details (gets $300 free!)
echo.
pause

echo Step 3: Enable Document AI API
start https://console.cloud.google.com/apis/library/documentai.googleapis.com
echo.
echo - Click "ENABLE" button
echo - Wait 1-2 minutes
echo.
pause

echo Step 4: Create service account
start https://console.cloud.google.com/iam-admin/serviceaccounts
echo.
echo - Click "+ CREATE SERVICE ACCOUNT"
echo - Name: sendora-ocr-service
echo - Role: Document AI API User
echo - Click CREATE AND CONTINUE then DONE
echo.
pause

echo Step 5: Download credentials
echo.
echo - Click on sendora-ocr-service account
echo - Go to KEYS tab
echo - Click ADD KEY > Create new key
echo - Select JSON format
echo - Click CREATE (file downloads)
echo.
pause

echo Step 6: Create Document AI processor
start https://console.cloud.google.com/ai/document-ai
echo.
echo - Click "CREATE PROCESSOR"
echo - Choose "Invoice Parser"
echo - Name: sendora-invoice-processor
echo - Region: us or eu
echo - Click CREATE
echo - COPY THE PROCESSOR ID!
echo.
pause

echo Step 7: Move credentials file
echo.
echo Please do the following:
echo 1. Find the downloaded JSON file in your Downloads folder
echo 2. Copy it to: %~dp0config\
echo 3. Rename it to: google-credentials.json
echo.
echo The full path should be:
echo %~dp0config\google-credentials.json
echo.
pause

echo Step 8: Update processor ID in code
echo.
echo Please edit backend\google_document_ai.py
echo Update line 25 with your actual processor ID:
echo self.processors = {'invoice': 'YOUR_PROCESSOR_ID_HERE'}
echo.
pause

echo ====================================
echo Setup complete!
echo ====================================
echo.
echo Test your setup by running:
echo python test_google_ai.py
echo.
echo If you see "Document processed successfully" - you're ready!
echo.
pause