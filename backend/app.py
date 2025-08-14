from flask import Flask, request, render_template, jsonify, send_file, redirect, url_for, flash
import os
import cv2
from PIL import Image
import pandas as pd
import numpy as np
from werkzeug.utils import secure_filename
from datetime import datetime
import json
import re
from dotenv import load_dotenv
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch

# Import our enhanced OCR providers
from azure_form_recognizer import SendoraFormRecognizer
from template_overlay_generator import SendoraTemplateOverlay

# Load environment variables
load_dotenv()

# Configuration - Use absolute paths
# Get the project root directory (parent of backend directory)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__, 
           template_folder=os.path.join(BASE_DIR, 'frontend'), 
           static_folder=os.path.join(BASE_DIR, 'static'))
app.secret_key = os.getenv('SECRET_KEY', 'dev-key')

# Use absolute paths for all folders
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
TEMP_FOLDER = os.path.join(BASE_DIR, 'temp') 
JO_FOLDER = os.path.join(BASE_DIR, 'job_orders')
MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', 16777216))  # 16MB
ALLOWED_EXTENSIONS = set(os.getenv('ALLOWED_EXTENSIONS', 'pdf,png,jpg,jpeg,tiff').split(','))

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Ensure directories exist
for folder in [UPLOAD_FOLDER, TEMP_FOLDER, JO_FOLDER]:
    os.makedirs(folder, exist_ok=True)

# Enhanced OCR and JO Generation Classes are imported above

# Initialize enhanced processors
ocr_processor = SendoraFormRecognizer()
jo_generator = SendoraTemplateOverlay()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file selected')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        filename = timestamp + filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process the file
        return redirect(url_for('process_document', filename=filename))
    
    flash('Invalid file type')
    return redirect(request.url)

@app.route('/process/<filename>')
def process_document(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if not os.path.exists(filepath):
        flash('File not found')
        return redirect(url_for('index'))
    
    # Process document with Azure Form Recognizer
    ocr_result = ocr_processor.analyze_document(filepath)
    
    if 'error' in ocr_result:
        flash(f'OCR Error: {ocr_result["error"]}')
        return redirect(url_for('index'))
    
    # Determine JO template based on extracted data
    template_type = jo_generator.determine_template_type(ocr_result)
    
    # Generate Job Order
    jo_filename = f"JO_{filename.split('.')[0]}.pdf"
    jo_path = os.path.join(JO_FOLDER, jo_filename)
    
    try:
        print(f"DEBUG: About to call generate_job_order with template_type: {template_type}")
        print(f"DEBUG: Output path: {jo_path}")
        jo_generator.generate_job_order(ocr_result, template_type, jo_path)
        print(f"DEBUG: generate_job_order completed")
    except Exception as e:
        print(f"DEBUG: Exception in generate_job_order: {e}")
        import traceback
        traceback.print_exc()
        flash(f'Error generating Job Order: {e}')
        return redirect(url_for('index'))
    
    result = {
        'filename': filename,
        'ocr_result': ocr_result,
        'extracted_data': ocr_result.get('structured_data', {}),
        'template_type': template_type,
        'jo_filename': jo_filename,
        'processing_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    return render_template('results.html', result=result)

@app.route('/download_jo/<filename>')
def download_jo(filename):
    jo_path = os.path.join(JO_FOLDER, filename)
    
    if os.path.exists(jo_path):
        return send_file(jo_path, as_attachment=True)
    else:
        flash(f'Job Order file not found: {filename}')
        return redirect(url_for('index'))

@app.route('/api/status')
def api_status():
    return jsonify({
        'status': 'active',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/approve/<jo_filename>')
def approve_jo(jo_filename):
    """Mock approval workflow"""
    flash(f'Job Order {jo_filename} approved! (Mock WhatsApp notification sent)')
    return redirect(url_for('index'))

@app.route('/reject/<jo_filename>')
def reject_jo(jo_filename):
    """Mock rejection workflow"""
    flash(f'Job Order {jo_filename} rejected! (Mock WhatsApp notification sent)')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)