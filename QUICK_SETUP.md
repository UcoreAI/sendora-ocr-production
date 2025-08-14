# 🚀 Sendora OCR - Quick Setup Guide

## ⚡ 5-Minute Setup

### Step 1: Install Python Dependencies
```bash
cd "C:\Users\USER\Desktop\Sendora-OCR-Complete-Project"
pip install -r requirements.txt
```

### Step 2: Copy Environment Configuration
```bash
copy "config\.env" ".env"
```

### Step 3: Start the Application
```bash
python run.py
```
**OR** double-click `start.bat`

### Step 4: Access Web Interface
- Open browser: **http://localhost:5000**
- Upload any Malaysian business document
- Download the generated Job Order

---

## 🔧 Template Path Configuration

**IMPORTANT**: Update template paths if your JO templates are in a different location.

Edit `backend/template_overlay_generator.py` line 23-27:

```python
self.templates = {
    'frame': r'C:\Users\USER\Desktop\Project management\Sendora\Material\JOB ORDER FORM  - FRAME.pdf',
    'door': r'C:\Users\USER\Desktop\Project management\Sendora\Material\JOB ORDER FORM -DOOR.pdf',
    'general': r'C:\Users\USER\Desktop\Project management\Sendora\Material\JOB ORDER.pdf'
}
```

---

## 🧪 Quick Test

Run the template overlay test:
```bash
cd tests/
python test_template_overlay.py
```

Expected output:
```
Testing Sendora Template Overlay System...
[OK] FRAME template found: JOB ORDER FORM  - FRAME.pdf
[OK] DOOR template found: JOB ORDER FORM -DOOR.pdf
[SUCCESS] Generated: overlay_frame_jo.pdf (108,061 bytes)
[SUCCESS] Generated: overlay_door_jo.pdf (143,315 bytes)
```

---

## 📋 Dependencies Required

```
Flask>=2.3.0
azure-cognitiveservices-vision-computervision>=0.9.0
Pillow>=10.0.0
pandas>=2.0.0
python-dotenv>=1.0.0
reportlab>=4.0.0
PyPDF2>=3.0.0
```

---

## 🔑 API Credentials

Your Azure Form Recognizer is already configured:
- **Endpoint**: https://sendoraformparser.cognitiveservices.azure.com/
- **Key**: Stored in `.env` file

---

## ✅ System Status

- **Template Overlay**: ✅ Uses your actual JO templates
- **Azure OCR**: ✅ Real API integration
- **Web Interface**: ✅ Upload/Process/Download workflow
- **Malaysian Patterns**: ✅ Optimized for local documents

---

## 🆘 Troubleshooting

### Issue: Template files not found
**Solution**: Update template paths in `backend/template_overlay_generator.py`

### Issue: Port already in use
**Solution**: Change port in `run.py` or kill existing process

### Issue: Missing dependencies
**Solution**: Run `pip install -r requirements.txt`

---

**Ready to use! Upload your documents and get perfect Job Orders! 🎯**