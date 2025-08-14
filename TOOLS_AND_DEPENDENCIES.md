# Tools and Dependencies - Complete Reference

## Development Environment

### Operating System
- **Primary**: Windows 10/11 (Development environment)
- **Target**: Windows/Linux (Production ready)
- **Python Version**: 3.11+ (Tested on Python 3.11.4)

## Core Dependencies

### requirements.txt
```txt
# Google Cloud Services
google-cloud-documentai==2.20.1
google-auth==2.22.0
google-auth-oauthlib==1.0.0
google-auth-httplib2==0.1.0
google-api-core==2.11.1
google-oauth2-tool==0.0.3
google-cloud-core==2.3.3

# Azure Services (Legacy Fallback)
azure-ai-formrecognizer==3.3.0
azure-core==1.28.0
azure-identity==1.13.0

# Web Framework
Flask==2.3.2
Flask-CORS==4.0.0
Werkzeug==2.3.6
Jinja2==3.1.2
MarkupSafe==2.1.3
itsdangerous==2.1.2
click==8.1.6

# PDF Processing
PyPDF2==3.0.1
pdfplumber==0.9.0
pypdf==3.0.1

# Data Processing & Analysis
pandas==2.0.3
numpy==1.24.3
openpyxl==3.1.2

# Text Processing
regex==2023.6.3
python-dateutil==2.8.2
python-slugify==8.0.1

# HTTP & Requests
requests==2.31.0
urllib3==2.0.4
certifi==2023.7.22
charset-normalizer==3.2.0
idna==3.4

# Configuration & Environment
python-dotenv==1.0.0
configparser==5.3.0

# Utilities
uuid==1.30
datetime
os
sys
json
re
typing
pathlib
tempfile
shutil
```

### External Binaries Required

#### wkhtmltopdf
**Purpose**: HTML to PDF conversion
**Version**: 0.12.6.1 (with patched qt)
**Installation**:
```bash
# Windows
Download from: https://wkhtmltopdf.org/downloads.html
Install path: C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe

# Linux (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install wkhtmltopdf

# Linux (CentOS/RHEL)
sudo yum install wkhtmltopdf

# macOS
brew install wkhtmltopdf
```

**Configuration Check**:
```python
# In code - path verification
WKHTMLTOPDF_PATH = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
if not os.path.exists(WKHTMLTOPDF_PATH):
    raise FileNotFoundError("wkhtmltopdf not found")
```

## Cloud Services Configuration

### Google Cloud Platform
**Service**: Document AI
**Project ID**: `my-textbee-sms`
**Region**: `us` (United States)

**Required APIs**:
- Document AI API (`documentai.googleapis.com`)
- Cloud Resource Manager API (`cloudresourcemanager.googleapis.com`)
- IAM Service Account Credentials API (`iamcredentials.googleapis.com`)

**Service Account Permissions**:
```json
{
  "roles": [
    "roles/documentai.apiUser",
    "roles/documentai.processor.user",
    "roles/storage.objectViewer"
  ]
}
```

**Processor Configuration**:
```python
processors = {
    'invoice': '1699972f50f6529',        # Invoice Processor
    'purchase_order': '81116d27ff6c4a06', # Form Parser Processor  
    'quote': '81116d27ff6c4a06',         # Form Parser for quotes
    'general': '81116d27ff6c4a06'        # General form parser
}
```

**Authentication Setup**:
```bash
# Service account key file location
config/google-credentials.json

# Environment variable (optional)
export GOOGLE_APPLICATION_CREDENTIALS="config/google-credentials.json"
```

### Azure Form Recognizer (Legacy)
**Service**: Form Recognizer v3.2
**Purpose**: Fallback OCR when Google Document AI unavailable
**Configuration**: `config/azure-config.json`

## Development Tools

### Code Editor & IDE
- **Primary**: Visual Studio Code
- **Extensions**:
  - Python Extension Pack
  - Flask Snippets
  - HTML/CSS/JavaScript support
  - Git integration

### Version Control
- **Git**: Version 2.41.0+
- **Repository**: Local filesystem (ready for GitHub/GitLab)

### Testing Tools
```python
# Built-in testing modules
import unittest
import pytest  # Optional, can be added

# Debug utilities
import pdb
import logging
import traceback
```

### Browser Testing
- **Primary**: Chrome/Chromium (Latest)
- **Secondary**: Firefox, Edge
- **Mobile**: Chrome Mobile, Safari Mobile

## Framework Architecture

### Flask Application Structure
```python
# Application factory pattern
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable cross-origin requests
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
```

### Template Engine
- **Engine**: Jinja2 (Flask default)
- **HTML Generation**: Server-side rendering
- **CSS Framework**: Custom CSS (no external framework)
- **Styling Approach**: Inline styles for PDF compatibility

### Data Processing Pipeline
```python
# Core processing modules
from typing import Dict, List, Any, Optional
from datetime import datetime
import re
import json
import os
from pathlib import Path
```

## File Structure & Organization

### Project Directory Structure
```
C:\Users\USER\Desktop\Sendora-OCR-Complete-Project\
├── backend/                    # Core application logic
│   ├── google_document_ai.py   # Google Document AI processor
│   ├── app_v2.py              # Flask web application
│   ├── simple_working_template.py  # Template generator
│   └── azure_form_recognizer.py    # Legacy Azure OCR
├── frontend/                   # Web interface
│   └── validation.html         # Human validation interface
├── config/                     # Configuration files
│   ├── google-credentials.json # Google service account key
│   └── azure-config.json      # Azure configuration (optional)
├── uploads/                    # Input PDF storage
├── job_orders/                 # Generated JO output
│   ├── *.html                 # HTML templates
│   └── pdf/                   # PDF output directory
├── templates/                  # Jinja2 templates (if used)
├── static/                     # Static assets (CSS, JS, images)
├── debug_extraction.py         # Development testing script
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (optional)
├── .gitignore                # Git ignore file
└── README.md                 # Project documentation
```

### File Naming Conventions
```python
# Generated Job Orders
JO_WORKING_YYYYMMDD_HHMMSS.html
JO_WORKING_YYYYMMDD_HHMMSS.pdf

# Uploaded Invoices
YYYYMMDD_HHMMSS_INVOICE.pdf

# Configuration Files
*-config.json
*-credentials.json
```

## Security & Authentication

### API Keys Management
```python
# Google Cloud credentials
GOOGLE_CREDENTIALS_PATH = "config/google-credentials.json"

# Azure credentials (optional)
AZURE_ENDPOINT = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
AZURE_KEY = os.getenv("AZURE_FORM_RECOGNIZER_KEY")

# Environment variables
from dotenv import load_dotenv
load_dotenv()
```

### File Security
```python
# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

# File size limits
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

# Upload directory security
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
```

## Performance Optimization

### Caching Strategy
- **Session storage**: In-memory dictionary for validation sessions
- **Template caching**: Generated HTML templates cached temporarily
- **API response caching**: Google Document AI responses (15-minute self-cleaning cache)

### Resource Management
```python
# Memory management
import gc
gc.collect()  # Called after large file processing

# File cleanup
import tempfile
import shutil
# Temporary files auto-cleaned

# Connection pooling
# Google Cloud client uses automatic connection pooling
```

## Monitoring & Logging

### Application Logging
```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sendora_ocr.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

### Error Handling
```python
# Exception handling patterns
try:
    result = process_document(file_path)
except Exception as e:
    logger.error(f"Document processing failed: {e}")
    return fallback_processing(file_path)
```

## Deployment Configuration

### Production Environment
```python
# Flask production settings
if os.getenv('FLASK_ENV') == 'production':
    app.config['DEBUG'] = False
    app.config['TESTING'] = False
else:
    app.config['DEBUG'] = True
```

### Environment Variables
```bash
# Production environment variables
FLASK_ENV=production
FLASK_APP=backend/app_v2.py
GOOGLE_APPLICATION_CREDENTIALS=config/google-credentials.json
UPLOAD_FOLDER=uploads
OUTPUT_FOLDER=job_orders
MAX_FILE_SIZE=16777216
ALLOWED_EXTENSIONS=pdf,png,jpg,jpeg
```

### Docker Configuration (Future)
```dockerfile
# Example Dockerfile structure
FROM python:3.11-slim

# Install wkhtmltopdf
RUN apt-get update && apt-get install -y wkhtmltopdf

# Copy requirements and install
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application
COPY . /app
WORKDIR /app

# Expose port
EXPOSE 5000

# Run application
CMD ["python", "backend/app_v2.py"]
```

## Testing & Quality Assurance

### Unit Testing Framework
```python
# Test structure (can be implemented)
import unittest
from backend.google_document_ai import GoogleDocumentProcessor

class TestOCRProcessing(unittest.TestCase):
    def setUp(self):
        self.processor = GoogleDocumentProcessor()
    
    def test_size_extraction(self):
        text = "DOOR SIZE: 43MM X 3FT X 8FT"
        result = self.processor.extract_size(text)
        self.assertEqual(result, "915MM x 2440MM")
```

### Integration Testing
```bash
# Manual testing script
python debug_extraction.py

# Web application testing
curl -X POST http://localhost:5000/upload \
  -F "file=@test_invoice.pdf"
```

## Documentation Tools

### Documentation Generation
- **Markdown**: GitHub-flavored markdown for documentation
- **Inline Documentation**: Python docstrings following PEP 257
- **API Documentation**: Can be generated with Sphinx

### Code Quality
```python
# Code formatting (can be added)
pip install black flake8 mypy

# Usage
black backend/
flake8 backend/
mypy backend/
```

## Development Workflow

### Local Development Setup
```bash
# 1. Clone/download project
# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate.bat  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install wkhtmltopdf binary

# 5. Configure Google Cloud credentials
# Place google-credentials.json in config/

# 6. Run application
python backend/app_v2.py

# 7. Test with debug script
python debug_extraction.py
```

### Build & Deployment Process
1. **Development**: Local testing with debug scripts
2. **Validation**: Manual testing with validation interface
3. **Integration**: Test full pipeline with real invoices
4. **Deployment**: Copy to production server
5. **Monitoring**: Check logs and performance metrics

---

*Complete tools and dependencies reference for Sendora OCR Complete Project*