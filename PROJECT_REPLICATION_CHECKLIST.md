# 📋 Sendora OCR Project Replication Checklist

## 🎯 Complete Project Replication Guide

This checklist ensures 100% accurate replication of the Sendora OCR Complete Project with all functionality, configurations, and dependencies.

---

## 📁 Phase 1: Directory Structure & Core Files

### ✅ **Essential Directory Structure**
```bash
# Create base directory
mkdir Sendora-OCR-Complete-Project
cd Sendora-OCR-Complete-Project

# Create all required subdirectories
mkdir backend config frontend uploads job_orders job_orders/pdf temp templates tests docs fillable_templates
```

### ✅ **Core Python Files** (CRITICAL - Must Have)

#### **Backend Core (Priority 1)**
- [ ] `backend/app_v2.py` - ⭐ **MAIN Flask application** (95% OCR accuracy)
- [ ] `backend/google_document_ai.py` - ⭐ **PRIMARY OCR engine** 
- [ ] `backend/simple_working_template.py` - ⭐ **Template generator**
- [ ] `backend/azure_form_recognizer.py` - Fallback OCR (70% accuracy)

#### **Frontend Interface**
- [ ] `frontend/validation.html` - ⭐ **Human validation interface**
- [ ] `frontend/index.html` - File upload interface
- [ ] `frontend/results.html` - Results display

#### **Testing & Debug Scripts**
- [ ] `debug_extraction.py` - ⭐ **Essential testing script**
- [ ] `test_size_extraction.py` - Size conversion testing
- [ ] `verify_setup.py` - System verification script

### ✅ **Configuration Files** (CRITICAL)

#### **Dependencies**
- [ ] `requirements_v2.txt` - ⭐ **CORRECT dependencies** (not requirements.txt)
- [ ] `config/google-credentials.json` - ⭐ **Google Cloud service account key**

#### **Startup Scripts**
- [ ] `start_v2.bat` - ⭐ **Windows startup script**
- [ ] `start_server.py` - Alternative startup
- [ ] `run.py` - Development startup

### ✅ **Documentation Files** (Must Include)
- [ ] `README.md` - ⭐ **Main documentation**
- [ ] `SYSTEM_DOCUMENTATION.md` - Technical deep dive
- [ ] `TOOLS_AND_DEPENDENCIES.md` - Complete tool reference
- [ ] `DATA_FLOW_PIPELINE.md` - Processing pipeline
- [ ] `TEMPLATE_SPECIFICATIONS.md` - Template analysis

---

## 🔧 Phase 2: Critical Configurations

### ✅ **Google Cloud Setup** (ESSENTIAL)
```python
# Google Document AI Configuration
PROJECT_ID = "my-textbee-sms"
LOCATION = "us"
PROCESSORS = {
    'invoice': '1699972f50f6529',        # Invoice Processor
    'purchase_order': '81116d27ff6c4a06', # Form Parser
}

# Service Account JSON Structure
{
  "type": "service_account",
  "project_id": "my-textbee-sms",
  "private_key_id": "[YOUR_KEY_ID]",
  "private_key": "-----BEGIN PRIVATE KEY-----\n[YOUR_PRIVATE_KEY]\n-----END PRIVATE KEY-----\n",
  "client_email": "[YOUR_SERVICE_ACCOUNT_EMAIL]",
  "client_id": "[YOUR_CLIENT_ID]",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "[YOUR_CERT_URL]"
}
```

### ✅ **Dependencies Setup**
```bash
# CRITICAL: Use requirements_v2.txt (not requirements.txt)
pip install -r requirements_v2.txt

# Key dependencies for replication:
google-cloud-documentai>=2.20.0
Flask>=2.3.0
PyPDF2>=3.0.0
```

### ✅ **External Binary Installation**
```bash
# wkhtmltopdf (ESSENTIAL for PDF generation)
# Windows: Download from https://wkhtmltopdf.org/downloads.html
# Install to: C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe

# Verify installation:
"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe" --version
```

---

## 📊 Phase 3: Data & Template Files

### ✅ **Template Specifications** (Reference Files)
- [ ] `complete_jo_template_spec.json` - Original template specification
- [ ] `door_template_spec.json` - Door template specs
- [ ] `frame_template_spec.json` - Frame template specs

### ✅ **Coordinate Files** (Precision Templates)
- [ ] `door_coordinates.json` - Door positioning data
- [ ] `frame_coordinates.json` - Frame positioning data
- [ ] `combined_coordinates.json` - Combined specifications

### ✅ **Sample Data** (For Testing)
```bash
# Include at least 1-2 sample invoices in uploads/
# File format: YYYYMMDD_HHMMSS_INVOICE.pdf
uploads/20250815_120000_INVOICE.pdf  # Sample invoice for testing
```

---

## 🔍 Phase 4: Critical Settings Verification

### ✅ **File Path Validations**
```python
# Verify these paths exist and are correct:
WKHTMLTOPDF_PATH = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
GOOGLE_CREDENTIALS = "config/google-credentials.json"
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "job_orders"
```

### ✅ **Google Document AI Configuration**
```python
# In backend/google_document_ai.py - verify these settings:
self.project_id = "my-textbee-sms"
self.location = "us"
self.processors = {
    'invoice': '1699972f50f6529',
    'purchase_order': '81116d27ff6c4a06',
}
```

### ✅ **Critical Code Fixes** (Must Include)
```python
# In backend/app_v2.py - ESSENTIAL fix for door size display:
specifications_to_preserve = [
    'door_thickness', 'door_type', 'door_core', 'door_edging',
    'decorative_line', 'frame_type', 'line_items', 'door_size',
    'item_size_0', 'item_desc_0'  # These fix the door size issue
]
```

---

## 🚀 Phase 5: Installation & Testing Sequence

### ✅ **Step-by-Step Installation**
```bash
# 1. Environment Setup
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux

# 2. Dependencies (CRITICAL: Use v2 requirements)
pip install -r requirements_v2.txt

# 3. External Tools
# Install wkhtmltopdf binary (see Phase 2)

# 4. Google Cloud Setup
# Place google-credentials.json in config/
# Verify processors are created in Google Cloud Console

# 5. Directory Permissions
# Ensure uploads/ and job_orders/ are writable

# 6. Test Installation
python verify_setup.py
```

### ✅ **Functional Testing Sequence**
```bash
# 1. Basic OCR Test
python debug_extraction.py

# 2. Size Conversion Test  
python test_size_extraction.py

# 3. Template Generation Test
python backend/simple_working_template.py

# 4. Full System Test
python backend/app_v2.py
# Open http://localhost:5000
# Upload test invoice
# Verify JO generation
```

### ✅ **Success Criteria Checklist**
- [ ] ✅ Flask app starts without errors on port 5000
- [ ] ✅ Google Document AI processes test invoice successfully  
- [ ] ✅ Door size conversion works: "43MM X 3FT X 8FT" → "915MM x 2440MM"
- [ ] ✅ Checkbox selection works: 43mm thickness → ✅ 43mm checked
- [ ] ✅ PDF generation works: HTML → PDF via wkhtmltopdf
- [ ] ✅ Confidence scores above 80% for test invoices
- [ ] ✅ Door size displays correctly (not empty or "1,2,3,4")

---

## ⚠️ Phase 6: Common Replication Issues

### ❌ **Most Common Issues & Solutions**

#### **Issue 1: Door Size Shows Empty**
```python
# CAUSE: Missing door_size in specifications_to_preserve
# FIX: Ensure backend/app_v2.py lines 304-308 include:
specifications_to_preserve = [
    # ... other specs ...
    'door_size', 'item_size_0', 'item_desc_0'  # CRITICAL
]
```

#### **Issue 2: Wrong Requirements File**
```bash
# CAUSE: Using requirements.txt instead of requirements_v2.txt
# FIX: Use the correct file:
pip install -r requirements_v2.txt  # NOT requirements.txt
```

#### **Issue 3: Google Credentials Not Found**
```python
# CAUSE: google-credentials.json in wrong location
# FIX: Must be in config/google-credentials.json (exact path)
config/google-credentials.json  # Correct location
```

#### **Issue 4: wkhtmltopdf Not Found**
```bash
# CAUSE: wkhtmltopdf not installed or wrong path
# FIX: Install to exact path:
C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe
```

#### **Issue 5: Import Errors**
```python
# CAUSE: Missing google-cloud-documentai package
# FIX: Install correct version:
pip install google-cloud-documentai>=2.20.0
```

### ✅ **Verification Commands**
```bash
# Test each component individually:

# 1. Google Cloud Connection
python -c "from backend.google_document_ai import GoogleDocumentProcessor; print('Google AI: OK')"

# 2. Flask App
python -c "from backend.app_v2 import app; print('Flask: OK')"

# 3. Template Generator  
python -c "from backend.simple_working_template import SimpleWorkingTemplate; print('Template: OK')"

# 4. PDF Converter
"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe" --version

# 5. Full Pipeline Test
python debug_extraction.py
```

---

## 📝 Phase 7: Essential Files Manifest

### ✅ **Must-Have Files for 95% OCR Accuracy**
```
✅ CRITICAL FILES (Cannot work without):
├── backend/app_v2.py                    # Main Flask app (95% accuracy)
├── backend/google_document_ai.py        # Primary OCR engine  
├── backend/simple_working_template.py   # Template generator
├── frontend/validation.html             # HITL validation interface
├── config/google-credentials.json       # Google Cloud credentials
├── requirements_v2.txt                  # Correct dependencies
├── debug_extraction.py                  # Testing script
└── start_v2.bat                        # Windows startup

✅ IMPORTANT FILES (Recommended):
├── backend/azure_form_recognizer.py     # Fallback OCR (70%)
├── test_size_extraction.py              # Size conversion testing
├── verify_setup.py                     # System verification
├── complete_jo_template_spec.json       # Original template spec
└── PROJECT_REPLICATION_CHECKLIST.md    # This file

✅ OPTIONAL FILES (Nice to have):
├── All other backend/*.py files         # Legacy/experimental
├── All coordinate JSON files            # Precision template specs
├── All sample invoices in uploads/      # Testing data
└── All documentation MD files           # Reference docs
```

---

## 🎯 Phase 8: Production Deployment Checklist

### ✅ **Pre-Deployment Verification**
- [ ] All files copied to production server
- [ ] Python 3.11+ installed on target system
- [ ] wkhtmltopdf installed on target system
- [ ] Google Cloud credentials valid and accessible
- [ ] All directories have proper permissions
- [ ] Port 5000 available or configured differently

### ✅ **Production Configuration**
```python
# Update paths for production environment
WKHTMLTOPDF_PATH = "/usr/bin/wkhtmltopdf"  # Linux
# or
WKHTMLTOPDF_PATH = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"  # Windows

# Set production environment
FLASK_ENV = "production"
DEBUG = False
```

### ✅ **Final Verification Steps**
1. **Start System**: `python backend/app_v2.py`
2. **Test Upload**: Upload sample invoice
3. **Check OCR**: Verify 95% accuracy on extraction
4. **Validate Output**: Confirm door size shows "915MM x 2440MM"
5. **PDF Generation**: Ensure PDF generates correctly
6. **Performance**: Processing time should be 5-8 seconds

---

## 🎉 Success Confirmation

### ✅ **System is Successfully Replicated When:**
- [ ] ✅ **95% OCR accuracy** achieved (vs 70% with Azure)
- [ ] ✅ **Door size displays correctly** ("915MM x 2440MM")
- [ ] ✅ **Checkboxes work** (43mm thickness selected)
- [ ] ✅ **Feet conversion works** (3FT × 8FT → 915MM × 2440MM)
- [ ] ✅ **PDF generation successful** (HTML → PDF)
- [ ] ✅ **End-to-end processing** under 10 seconds
- [ ] ✅ **Human validation interface** functional
- [ ] ✅ **Error handling works** (fallback to Azure if needed)

### 📊 **Performance Benchmarks**
- **OCR Processing**: 3-5 seconds
- **Template Generation**: <1 second  
- **PDF Conversion**: 2-3 seconds
- **Total Pipeline**: 5-8 seconds
- **Success Rate**: >95% for typical invoices

---

## 🔒 **Security & Credentials**

### ⚠️ **Critical Security Notes**
- **Never commit** `config/google-credentials.json` to version control
- **Secure the private key** in google-credentials.json
- **Limit Google Cloud permissions** to Document AI only
- **Regular key rotation** recommended (quarterly)
- **Monitor API usage** to prevent unexpected charges

### 🔑 **Required Credentials**
1. **Google Cloud Service Account** with Document AI API access
2. **Document AI Processors** (Invoice + Form Parser created)
3. **Valid payment method** in Google Cloud (for API calls)

---

## 📞 **Support & Troubleshooting**

### 🆘 **If Replication Fails**
1. **Check this checklist** step by step
2. **Run verification scripts** to identify issues
3. **Check Google Cloud Console** for API status
4. **Review error logs** in console output
5. **Test individual components** before full system

### 📋 **Common Support Requests**
- **"Door size is empty"** → Check specifications_to_preserve in app_v2.py
- **"Google AI not working"** → Verify credentials and processor IDs
- **"PDF not generating"** → Check wkhtmltopdf installation
- **"Import errors"** → Use requirements_v2.txt, not requirements.txt

---

*This checklist ensures 100% accurate replication of the Sendora OCR Complete Project with all 95% accuracy features and critical fixes included.*