"""
Sendora OCR V2.0 - Enhanced Flask Application
With Google Document AI and HITL Validation
"""

from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
import os
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename
import json
import tempfile
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

# Import our processors
from google_document_ai import GoogleDocumentProcessor
from sendora_template_filler import SendoraTemplateFiller
from precise_template_overlay import PreciseTemplateOverlay
from smart_form_filler import SmartFormFiller
from exact_template_filler import ExactTemplateFiller
from html_to_pdf_converter import HTMLJobOrderGenerator
from simple_html_generator import SimpleHTMLJobOrderGenerator
from fixed_html_generator import FixedHTMLJobOrderGenerator
from correct_template_generator import CorrectTemplateGenerator
from fixed_coordinate_template import FixedCoordinateTemplate
from clean_template_generator import CleanTemplateGenerator
from exact_replica_template import ExactReplicaTemplate
from simple_working_template import SimpleWorkingTemplate

# Configuration
app = Flask(__name__, 
           template_folder=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend'),
           static_folder=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static'))

app.secret_key = 'sendora-ocr-v2-secret-key'

def convert_html_to_pdf_for_download(html_path):
    """Convert HTML to PDF using various methods"""
    import subprocess
    from pathlib import Path
    
    if not html_path or not os.path.exists(html_path):
        return None
    
    # Create PDF directory if it doesn't exist
    pdf_dir = os.path.join(os.path.dirname(html_path), 'pdf')
    os.makedirs(pdf_dir, exist_ok=True)
    
    # Generate PDF filename
    html_name = Path(html_path).stem
    pdf_path = os.path.join(pdf_dir, f"{html_name}.pdf")
    
    # Try wkhtmltopdf first (most reliable)
    wkhtmltopdf_paths = [
        'wkhtmltopdf',  # If in PATH
        r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe',  # Default install
        r'C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe',  # 32-bit install
    ]
    
    for wkhtmltopdf_path in wkhtmltopdf_paths:
        try:
            result = subprocess.run([wkhtmltopdf_path, '--version'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                # wkhtmltopdf is available
                cmd = [
                    wkhtmltopdf_path,
                    '--page-size', 'A4',
                    '--margin-top', '10mm',
                    '--margin-bottom', '10mm',
                    '--margin-left', '10mm',
                    '--margin-right', '10mm',
                    '--encoding', 'UTF-8',
                    '--enable-local-file-access',
                    '--quiet',  # Suppress output
                    html_path,
                    pdf_path
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0 and os.path.exists(pdf_path):
                    print(f"PDF generated with wkhtmltopdf: {pdf_path}")
                    return pdf_path
        except:
            continue
    
    # Try weasyprint as second option
    try:
        from weasyprint import HTML
        HTML(filename=html_path).write_pdf(pdf_path)
        
        if os.path.exists(pdf_path):
            print(f"PDF generated with WeasyPrint: {pdf_path}")
            return pdf_path
    except:
        pass
    
    # Try pdfkit as third option
    try:
        import pdfkit
        
        options = {
            'page-size': 'A4',
            'margin-top': '10mm',
            'margin-right': '10mm',
            'margin-bottom': '10mm',
            'margin-left': '10mm',
            'encoding': "UTF-8",
            'no-outline': None,
            'enable-local-file-access': None,
            'quiet': ''
        }
        
        pdfkit.from_file(html_path, pdf_path, options=options)
        
        if os.path.exists(pdf_path):
            print(f"PDF generated with pdfkit: {pdf_path}")
            return pdf_path
    except:
        pass
    
    print("No PDF converter available, will send HTML instead")
    return None

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
JO_FOLDER = os.path.join(BASE_DIR, 'job_orders')
TEMP_FOLDER = os.path.join(BASE_DIR, 'temp')

# Configuration
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'tiff'}

app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Ensure directories exist
for folder in [UPLOAD_FOLDER, JO_FOLDER, TEMP_FOLDER]:
    os.makedirs(folder, exist_ok=True)

# In-memory session storage (use Redis in production)
validation_sessions = {}

# Initialize processors
document_processor = GoogleDocumentProcessor()
template_filler = SendoraTemplateFiller()
precise_overlay = PreciseTemplateOverlay()
smart_filler = SmartFormFiller()
exact_filler = ExactTemplateFiller()
html_jo_generator = HTMLJobOrderGenerator()
simple_html_generator = SimpleHTMLJobOrderGenerator()
fixed_html_generator = FixedHTMLJobOrderGenerator()
correct_template_generator = CorrectTemplateGenerator()
fixed_coordinate_template = FixedCoordinateTemplate()
clean_template_generator = CleanTemplateGenerator()
exact_replica_template = ExactReplicaTemplate()
simple_working_template = SimpleWorkingTemplate()

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Main upload page"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle document upload and start processing"""
    
    if 'document' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['document']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Use PDF, PNG, JPG, JPEG, or TIFF'}), 400
    
    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Process with Google Document AI
        print(f"Processing file: {filename}")
        extracted_data = document_processor.process_document(filepath)
        
        # Create validation session
        session_id = str(uuid.uuid4())
        validation_sessions[session_id] = {
            'original_file': filepath,
            'filename': filename,
            'extracted_data': extracted_data,
            'validated_data': None,
            'timestamp': datetime.now()
        }
        
        print(f"Created session: {session_id}")
        
        # Return success with redirect to validation
        return jsonify({
            'status': 'success',
            'session_id': session_id,
            'redirect': f'/validate?session={session_id}',
            'message': 'Document processed successfully'
        })
        
    except Exception as e:
        print(f"Error processing upload: {e}")
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500

@app.route('/validate')
def validate():
    """Validation interface"""
    session_id = request.args.get('session')
    
    if not session_id or session_id not in validation_sessions:
        return redirect(url_for('index'))
    
    return render_template('validation.html')

@app.route('/api/get-extracted-data/<session_id>')
def get_extracted_data(session_id):
    """Get extracted data for validation"""
    
    if session_id not in validation_sessions:
        return jsonify({'error': 'Session not found'}), 404
    
    return jsonify(validation_sessions[session_id]['extracted_data'])

@app.route('/api/get-document/<session_id>')
def get_document(session_id):
    """Get original document for preview"""
    
    if session_id not in validation_sessions:
        return jsonify({'error': 'Session not found'}), 404
    
    session_data = validation_sessions[session_id]
    filepath = session_data['original_file']
    
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=False)
    else:
        return jsonify({'error': 'Document not found'}), 404

@app.route('/api/save-validation', methods=['POST'])
def save_validation():
    """Save validated data"""
    
    session_id = request.form.get('session_id')
    
    if not session_id or session_id not in validation_sessions:
        return jsonify({'error': 'Session not found'}), 404
    
    # Save validated form data
    validated_data = {}
    for key, value in request.form.items():
        if key != 'session_id':
            validated_data[key] = value
    
    validation_sessions[session_id]['validated_data'] = validated_data
    validation_sessions[session_id]['validation_timestamp'] = datetime.now()
    
    print(f"Saved validation for session: {session_id}")
    
    return jsonify({'status': 'saved', 'message': 'Progress saved successfully'})

@app.route('/api/generate-jo', methods=['POST'])
def generate_jo():
    """Generate Job Order from validated data"""
    
    session_id = request.form.get('session_id')
    
    if not session_id or session_id not in validation_sessions:
        return jsonify({'error': 'Session not found'}), 404
    
    try:
        # Get original extracted data from session
        original_extracted_data = validation_sessions[session_id]['extracted_data']
        
        # Get validated data from form
        validated_data = {}
        for key, value in request.form.items():
            if key != 'session_id':
                validated_data[key] = value
        
        # Merge original extracted specifications with validated data
        # This ensures we don't lose the Google Document AI extracted specifications
        specifications_to_preserve = [
            'door_thickness', 'door_type', 'door_core', 'door_edging', 
            'decorative_line', 'frame_type', 'line_items', 'door_size', 
            'item_size_0', 'item_desc_0'
        ]
        
        for spec in specifications_to_preserve:
            if spec in original_extracted_data and original_extracted_data[spec]:
                # Only use original data if validated data doesn't have this field or it's empty
                if spec not in validated_data or not validated_data[spec]:
                    validated_data[spec] = original_extracted_data[spec]
                    print(f"PRESERVED from original extraction: {spec} = {original_extracted_data[spec]}")
        
        print(f"MERGED DATA: door_thickness = '{validated_data.get('door_thickness', '')}'")
        print(f"MERGED DATA: door_type = '{validated_data.get('door_type', '')}'")
        print(f"MERGED DATA: door_core = '{validated_data.get('door_core', '')}'")
        print(f"MERGED DATA: door_size = '{validated_data.get('door_size', '')}'")
        print(f"MERGED DATA: item_size_0 = '{validated_data.get('item_size_0', '')}'")
        print(f"MERGED DATA: item_desc_0 = '{validated_data.get('item_desc_0', '')}')")
        
        # Generate JO using SIMPLE WORKING template approach (clean and functional)
        print("Attempting to generate JO using SIMPLE WORKING template approach...")
        
        # DEBUG: Print validated_data keys and values
        print("=== WEB APP DEBUG: Validated Data ===")
        for key, value in validated_data.items():
            if not key.startswith('full_text'):
                print(f"WEB APP - {key}: {value}")
        print("=====================================")
        
        html_path = simple_working_template.generate_working_jo(validated_data)
        print(f"Simple working template generator result: {html_path}")
        
        if not html_path:
            # Fallback to exact template filler
            html_path = exact_filler.generate_exact_jo(validated_data)
            if not html_path:
                # Fallback to smart filler if exact filler fails
                html_path = smart_filler.generate_smart_jo(validated_data)
                if not html_path:
                    # Final fallback to precise overlay
                    html_path = precise_overlay.generate_precise_jo(validated_data)
        
        # Convert HTML to PDF for download
        pdf_path = convert_html_to_pdf_for_download(html_path)
        
        if pdf_path and os.path.exists(pdf_path):
            # Send PDF file
            pdf_filename = os.path.basename(pdf_path)
            print(f"Generated PDF JO: {pdf_filename}")
            return send_file(pdf_path, as_attachment=True, download_name=pdf_filename, mimetype='application/pdf')
        else:
            # If PDF conversion fails, send HTML with proper mimetype
            html_filename = os.path.basename(html_path)
            print(f"PDF conversion failed, sending HTML: {html_filename}")
            # Change extension to .html for clarity
            download_name = html_filename.replace('.html', '_VIEW_IN_BROWSER.html')
            return send_file(html_path, as_attachment=True, download_name=download_name, mimetype='text/html')
        
    except Exception as e:
        print(f"Error generating JO: {e}")
        return jsonify({'error': f'JO generation failed: {str(e)}'}), 500

def generate_jo_pdf(validated_data, output_path):
    """Generate Job Order as PDF using ReportLab"""
    
    try:
        # Create PDF document
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontSize=18,
            textColor=colors.darkblue,
            alignment=TA_CENTER,
            spaceAfter=20
        )
        
        header_style = ParagraphStyle(
            'CustomHeader',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.darkblue,
            spaceBefore=12,
            spaceAfter=6
        )
        
        normal_style = styles['Normal']
        
        # Title
        story.append(Paragraph("SENDORA JOB ORDER", title_style))
        story.append(Spacer(1, 12))
        
        # Generation info
        gen_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        story.append(Paragraph(f"<b>Generated:</b> {gen_time}", normal_style))
        story.append(Spacer(1, 12))
        
        # Document Information Section
        story.append(Paragraph("DOCUMENT INFORMATION", header_style))
        
        doc_info = [
            ['Invoice/PO Number:', validated_data.get('invoice_number', 'N/A')],
            ['Customer Name:', validated_data.get('customer_name', 'N/A')],
            ['Document Date:', validated_data.get('document_date', 'N/A')],
            ['Delivery Date:', validated_data.get('delivery_date', 'N/A')],
            ['Template Type:', validated_data.get('template_type', 'N/A')]
        ]
        
        doc_table = Table(doc_info, colWidths=[120, 300])
        doc_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ]))
        
        story.append(doc_table)
        story.append(Spacer(1, 12))
        
        # Door Specifications Section
        story.append(Paragraph("DOOR SPECIFICATIONS", header_style))
        
        door_specs = [
            ['Door Thickness:', validated_data.get('door_thickness', 'Not Specified')],
            ['Door Type:', validated_data.get('door_type', 'Not Specified')],
            ['Door Core:', validated_data.get('door_core', 'Not Specified')],
            ['Edging:', validated_data.get('door_edging', 'Not Specified')]
        ]
        
        door_table = Table(door_specs, colWidths=[120, 300])
        door_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ]))
        
        story.append(door_table)
        story.append(Spacer(1, 12))
        
        # Frame Specifications Section
        story.append(Paragraph("FRAME SPECIFICATIONS", header_style))
        
        frame_specs = [
            ['Frame Type:', validated_data.get('frame_type', 'Not Specified')],
            ['Frame Profile:', validated_data.get('frame_profile', 'Not Specified')]
        ]
        
        frame_table = Table(frame_specs, colWidths=[120, 300])
        frame_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ]))
        
        story.append(frame_table)
        story.append(Spacer(1, 12))
        
        # Line Items Section
        story.append(Paragraph("LINE ITEMS", header_style))
        
        # Collect line items
        line_items = []
        item_count = 0
        
        for key, value in validated_data.items():
            if key.startswith('item_desc_') and value:
                item_num = key.split('_')[-1]
                desc = validated_data.get(f'item_desc_{item_num}', '')
                size = validated_data.get(f'item_size_{item_num}', '')
                qty = validated_data.get(f'item_qty_{item_num}', '')
                item_type = validated_data.get(f'item_type_{item_num}', '')
                
                item_count += 1
                line_items.append([
                    str(item_count),
                    desc[:50] + ('...' if len(desc) > 50 else ''),
                    size or 'N/A',
                    qty or '1',
                    item_type or 'N/A'
                ])
        
        if line_items:
            # Create line items table
            line_items.insert(0, ['#', 'Description', 'Size', 'Qty', 'Type'])  # Header
            
            items_table = Table(line_items, colWidths=[25, 250, 80, 40, 60])
            items_table.setStyle(TableStyle([
                # Header row
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                
                # Data rows
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('ALIGN', (0, 1), (0, -1), 'CENTER'),  # Item numbers centered
                ('ALIGN', (2, 1), (-1, -1), 'CENTER'),  # Size, Qty, Type centered
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                
                # Grid
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            
            story.append(items_table)
        else:
            story.append(Paragraph("No line items specified.", normal_style))
        
        story.append(Spacer(1, 20))
        
        # Summary
        summary_data = [
            ['Total Items:', str(item_count)],
            ['Status:', 'Ready for Production'],
            ['System:', 'Sendora OCR V2.0 with Google Document AI']
        ]
        
        summary_table = Table(summary_data, colWidths=[120, 300])
        summary_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
        ]))
        
        story.append(summary_table)
        
        # Build PDF
        doc.build(story)
        print(f"PDF Job Order generated: {output_path}")
        
    except Exception as e:
        print(f"Error generating PDF: {e}")
        # Fallback to text file
        with open(output_path.replace('.pdf', '.txt'), 'w', encoding='utf-8') as f:
            f.write(f"JO Generation Error: {e}\n\nPlease contact support.")

@app.route('/api/sessions')
def list_sessions():
    """List all validation sessions (for debugging)"""
    
    sessions = []
    for session_id, data in validation_sessions.items():
        sessions.append({
            'session_id': session_id,
            'filename': data.get('filename'),
            'timestamp': data.get('timestamp').isoformat() if data.get('timestamp') else None,
            'has_validation': data.get('validated_data') is not None
        })
    
    return jsonify(sessions)

@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': 'File too large. Maximum size is 16MB.'}), 413

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Page not found'}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("SENDORA OCR V2.0 - Enhanced System Starting...")
    print("=" * 60)
    print("Google Document AI: Ready")
    print("HITL Validation: Ready") 
    print("File Upload: Ready")
    print("Session Management: Ready")
    print("HTML Template Generator: Ready")
    print("=" * 60)
    print("Server: http://localhost:5000")
    print("Upload: http://localhost:5000")
    print("Validate: http://localhost:5000/validate")
    print("Sessions: http://localhost:5000/api/sessions")
    print("=" * 60)
    print("Ready for document processing!")
    print()
    
    app.run(debug=True, host='0.0.0.0', port=5000)