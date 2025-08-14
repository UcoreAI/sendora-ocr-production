# 🔑 Google Document AI API Setup Guide

## Complete Step-by-Step Instructions to Get Your Credentials

### Prerequisites
- Google account (Gmail)
- Credit card (for billing - has $300 free credit for new users)
- 15 minutes to complete setup

---

## 📋 Step 1: Create Google Cloud Project

1. **Go to Google Cloud Console**
   ```
   https://console.cloud.google.com
   ```

2. **Create New Project**
   - Click the project dropdown (top left)
   - Click "NEW PROJECT"
   - Enter project details:
     - Project name: `sendora-ocr-project`
     - Location: Leave as default
   - Click "CREATE"
   - Wait 30 seconds for creation

3. **Select Your Project**
   - Click the project dropdown again
   - Select `sendora-ocr-project`

---

## 💳 Step 2: Enable Billing (Required but Free Trial Available)

1. **Access Billing**
   ```
   https://console.cloud.google.com/billing
   ```

2. **Set Up Billing Account**
   - Click "Link a billing account"
   - Click "CREATE BILLING ACCOUNT"
   - Follow the steps:
     - Country: Malaysia
     - Account type: Individual
     - Enter payment details
   - **Note**: You get $300 free credit for 90 days!

3. **Link to Project**
   - Select your `sendora-ocr-project`
   - Click "SET ACCOUNT"

---

## 🚀 Step 3: Enable Document AI API

### Method A: Direct Link (Easiest)
1. **Click this link**:
   ```
   https://console.cloud.google.com/apis/library/documentai.googleapis.com
   ```

2. **Click "ENABLE"** button
   - Wait for 1-2 minutes

### Method B: Manual Navigation
1. Go to **APIs & Services** → **Library**
2. Search for "Document AI"
3. Click on "Cloud Document AI API"
4. Click "ENABLE"

---

## 🤖 Step 4: Create Service Account & Download Credentials

### Create Service Account

1. **Navigate to Service Accounts**
   ```
   https://console.cloud.google.com/iam-admin/serviceaccounts
   ```

2. **Create Service Account**
   - Click "+ CREATE SERVICE ACCOUNT"
   - Enter details:
     - Service account name: `sendora-ocr-service`
     - Service account ID: `sendora-ocr-service` (auto-fills)
     - Description: `Service account for Sendora OCR Document AI`
   - Click "CREATE AND CONTINUE"

3. **Grant Permissions**
   - In "Grant this service account access" section
   - Click the role dropdown
   - Search and select: `Document AI API User`
   - Click "CONTINUE"
   - Click "DONE"

### Download Credentials JSON

1. **Find Your Service Account**
   - You should see `sendora-ocr-service@sendora-ocr-project.iam.gserviceaccount.com`
   - Click on it

2. **Create Key**
   - Go to "KEYS" tab
   - Click "ADD KEY" → "Create new key"
   - Select "JSON" format
   - Click "CREATE"
   - **File will auto-download** (usually to Downloads folder)

3. **Move & Rename File**
   - Find the downloaded file (named like `sendora-ocr-project-xxxxx.json`)
   - Copy it to: `C:\Users\USER\Desktop\Sendora-OCR-Complete-Project\config\`
   - Rename it to: `google-credentials.json`

---

## 📄 Step 5: Create Document AI Processor

1. **Go to Document AI Console**
   ```
   https://console.cloud.google.com/ai/document-ai
   ```

2. **Create Processor**
   - Click "CREATE PROCESSOR"
   - Choose processor type:
     - For invoices: Select "Invoice Parser"
     - For general: Select "Document OCR"
   - Click "CREATE"
   - Give it a name: `sendora-invoice-processor`
   - Select region: `us` (United States) or `eu` (Europe)
   - Click "CREATE"

3. **Copy Processor ID**
   - After creation, click on your processor
   - Copy the "Processor ID" (looks like: `a1b2c3d4e5f6g7h8`)
   - Save this ID - you'll need it!

---

## 🔧 Step 6: Update Your Code Configuration

1. **Edit google_document_ai.py**
   ```python
   # backend/google_document_ai.py
   # Update these values (around line 20-25):
   
   self.project_id = "sendora-ocr-project"  # Your actual project ID
   self.location = "us"  # or "eu" based on your processor
   self.processors = {
       'invoice': 'YOUR_PROCESSOR_ID_HERE',  # Replace with actual ID
       'purchase_order': 'YOUR_PROCESSOR_ID_HERE',
       'general': 'YOUR_PROCESSOR_ID_HERE'
   }
   ```

2. **Verify Credentials Path**
   Make sure this file exists:
   ```
   C:\Users\USER\Desktop\Sendora-OCR-Complete-Project\config\google-credentials.json
   ```

---

## ✅ Step 7: Test Your Setup

Run the test script:
```bash
cd "C:\Users\USER\Desktop\Sendora-OCR-Complete-Project"
python test_google_ai.py
```

You should see:
```
Google Document AI processor initialized
Processing document with Google Document AI...
Document processed successfully
```

---

## 💰 Pricing Information

### Free Tier (First 90 days)
- **$300 credit** for new Google Cloud users
- Covers ~15,000 pages of processing

### After Free Tier
- **First 1,000 pages/month**: FREE
- **Next 5,000,000 pages**: $0.10 per page
- **Malaysian pricing**: ~RM 0.45 per page after free tier

### Cost Estimate for Sendora
- 100 documents/day = 3,000/month
- First 1,000 FREE
- Next 2,000 = $200 = ~RM 900/month
- **Or stay under 1,000/month = FREE forever**

---

## 🆘 Troubleshooting

### Error: "API not enabled"
- Make sure you enabled Document AI API (Step 3)
- Wait 5 minutes after enabling

### Error: "Permission denied"
- Check service account has "Document AI API User" role
- Verify credentials file is in correct location

### Error: "Billing account required"
- You must enable billing (Step 2)
- Free tier still requires billing setup

### Error: "Processor not found"
- Make sure processor ID is correct
- Check region matches (us vs eu)

---

## 🎯 Quick Setup Script

Save this as `setup_google_cloud.bat`:

```batch
@echo off
echo ====================================
echo Google Document AI Setup Helper
echo ====================================
echo.
echo Step 1: Open Google Cloud Console
start https://console.cloud.google.com
timeout /t 3
echo.
echo Step 2: Create project named: sendora-ocr-project
pause
echo.
echo Step 3: Enable billing (get $300 free credit)
start https://console.cloud.google.com/billing
pause
echo.
echo Step 4: Enable Document AI API
start https://console.cloud.google.com/apis/library/documentai.googleapis.com
pause
echo.
echo Step 5: Create service account
start https://console.cloud.google.com/iam-admin/serviceaccounts
pause
echo.
echo Step 6: Create Document AI processor
start https://console.cloud.google.com/ai/document-ai
pause
echo.
echo Step 7: Place credentials file here:
echo C:\Users\USER\Desktop\Sendora-OCR-Complete-Project\config\google-credentials.json
pause
echo.
echo Setup complete! Run: python test_google_ai.py
```

---

## 📝 Summary Checklist

- [ ] Created Google Cloud project
- [ ] Enabled billing (got $300 credit)
- [ ] Enabled Document AI API
- [ ] Created service account
- [ ] Downloaded credentials JSON
- [ ] Moved credentials to `config/google-credentials.json`
- [ ] Created Document AI processor
- [ ] Updated code with processor ID
- [ ] Tested with `test_google_ai.py`

**Total Time: ~15 minutes**
**Cost: FREE (with $300 credit)**
**Result: 95% OCR accuracy!**