"""
Template Overlay Generator for Sendora JO
Uses actual Sendora JO template PDFs and overlays parsed data directly onto them
"""

import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen.canvas import Canvas
import io


class SendoraTemplateOverlay:
    """Overlay parsed data directly onto original Sendora JO templates"""
    
    def __init__(self):
        # Base template paths - Use your original templates
        self.templates = {
            'frame': r'C:\Users\USER\Desktop\Project management\Sendora\Material\JOB ORDER FORM  - FRAME.pdf',
            'door': r'C:\Users\USER\Desktop\Project management\Sendora\Material\JOB ORDER FORM -DOOR.pdf',
            'general': r'C:\Users\USER\Desktop\Project management\Sendora\Material\JOB ORDER FORM -DOOR.pdf'
        }
        
        # Field positions on templates (measured from your originals)
        # Coordinates are (x, y) from bottom-left corner in points (1 point = 1/72 inch)
        self.field_positions = {
            'door': {
                'job_order_no': (320, 720),
                'job_order_date': (320, 705),
                'po_no': (320, 690),
                'delivery_date': (600, 720),
                'customer_name': (600, 705),
                'measure_by': (600, 690)
            },
            'frame': {
                'job_order_no': (320, 720),
                'job_order_date': (320, 705),
                'po_no': (320, 690),
                'delivery_date': (600, 720),
                'customer_name': (600, 705),
                'measure_by': (600, 690)
            }
        }
    
    def determine_template_type(self, extracted_data: Dict[str, Any]) -> str:
        """Determine which template to use"""
        
        full_text = ""
        structured = extracted_data.get('structured_data', {})
        
        if 'full_text' in extracted_data:
            full_text = extracted_data['full_text'].lower()
        
        # Score each template type
        scores = {'frame': 0, 'door': 0, 'general': 0}
        
        # Frame indicators
        frame_keywords = ['frame', 'jamb', 'casing', 'bingkai', 'frame width', 'frame size', 'frame profile']
        for keyword in frame_keywords:
            if keyword in full_text:
                scores['frame'] += 2
        
        # Door indicators  
        door_keywords = ['door', 'pintu', 'thickness', 'door size', 'door type', 'door core', 'edging']
        for keyword in door_keywords:
            if keyword in full_text:
                scores['door'] += 2
        
        # Check structured data
        frame_specs = structured.get('frame_specs', {})
        door_specs = structured.get('door_specs', {})
        
        if frame_specs:
            scores['frame'] += 5
        if door_specs:
            scores['door'] += 5
            
        # Products analysis
        products = structured.get('product_specs', [])
        for product in products:
            if 'frame' in str(product).lower():
                scores['frame'] += 3
            elif 'door' in str(product).lower() or product.get('thickness'):
                scores['door'] += 3
        
        # Return best template
        best_template = max(scores, key=scores.get)
        
        # Default to general if no clear winner
        if scores[best_template] < 3:
            best_template = 'general'
            
        return best_template
    
    def generate_job_order(self, extracted_data: Dict[str, Any], template_type: str, output_path: str):
        """Generate JO by overlaying data on original template"""
        
        print(f"DEBUG: Template type selected: {template_type}")
        
        # Get the original template path
        template_path = self.templates.get(template_type)
        
        print(f"DEBUG: Template path: {template_path}")
        print(f"DEBUG: Template exists: {os.path.exists(template_path) if template_path else 'No path'}")
        
        if not template_path or not os.path.exists(template_path):
            print(f"Template not found: {template_path}")
            print("DEBUG: Using fallback JO generation")
            # Fallback to general template or create simple one
            self._create_fallback_jo(extracted_data, output_path)
            return
        
        # Create overlay based on template type
        if template_type == 'frame':
            self._overlay_frame_template(extracted_data, template_path, output_path)
        elif template_type == 'door':
            self._overlay_door_template(extracted_data, template_path, output_path)
        else:
            self._overlay_general_template(extracted_data, template_path, output_path)
    
    def _overlay_frame_template(self, data: Dict[str, Any], template_path: str, output_path: str):
        """Overlay data on FRAME template"""
        
        try:
            # Read the original template
            with open(template_path, 'rb') as template_file:
                reader = PdfReader(template_file)
                writer = PdfWriter()
                
                # Get the first page of the template
                template_page = reader.pages[0]
                
                # Create overlay with data
                overlay_buffer = self._create_frame_overlay(data)
                
                # Read the overlay
                overlay_reader = PdfReader(overlay_buffer)
                overlay_page = overlay_reader.pages[0]
                
                # Merge template with overlay
                template_page.merge_page(overlay_page)
                writer.add_page(template_page)
                
                # Write the result
                with open(output_path, 'wb') as output_file:
                    writer.write(output_file)
                    
                print(f"Frame JO generated: {output_path}")
                
        except Exception as e:
            print(f"Error overlaying frame template: {e}")
            self._create_fallback_jo(data, output_path)
    
    def _create_frame_overlay(self, data: Dict[str, Any]) -> io.BytesIO:
        """Create overlay data for frame template"""
        
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        
        # Extract data
        structured = data.get('structured_data', {})
        doc_info = structured.get('document_info', {})
        company_info = structured.get('company_info', {})
        products = structured.get('product_specs', [])
        frame_specs = structured.get('frame_specs', {})
        
        # Get field positions
        positions = self.field_positions['frame']
        
        # Set font
        c.setFont("Helvetica", 9)
        
        # Fill header fields
        current_date = datetime.now().strftime('%d/%m/%Y')
        
        # Job order info
        c.drawString(positions['job_order_no'][0], positions['job_order_no'][1], 
                    f"JO-{datetime.now().strftime('%Y%m%d')}-001")
        c.drawString(positions['job_order_date'][0], positions['job_order_date'][1], 
                    doc_info.get('date', current_date))
        c.drawString(positions['po_no'][0], positions['po_no'][1], 
                    doc_info.get('po_number', ''))
        
        # Customer info
        c.drawString(positions['delivery_date'][0], positions['delivery_date'][1], current_date)
        c.drawString(positions['customer_name'][0], positions['customer_name'][1], 
                    company_info.get('company_name', ''))
        c.drawString(positions['measure_by'][0], positions['measure_by'][1], 'Auto Generated')
        
        # Fill table data
        for i, product in enumerate(products[:4]):  # Max 4 rows
            if i < len(positions['table_rows']):
                row_y = positions['table_rows'][i]
                
                # Item number
                c.drawString(positions['item_col'], row_y, str(i + 1))
                
                # Frame size
                if product.get('width') and product.get('height'):
                    size_text = f"{product['width']} x {product['height']}"
                    if product.get('thickness'):
                        size_text += f" x {product['thickness']}"
                    c.drawString(positions['frame_size_col'], row_y, size_text)
                
                # Inner/Outer checkboxes
                frame_options = frame_specs.get('frame_options', [])
                
                # Inner checkbox
                if 'inner' in frame_options:
                    checkbox_x = positions['inner_outer_col'] + positions['inner_checkbox'][0]
                    checkbox_y = row_y + positions['inner_checkbox'][1]
                    c.drawString(checkbox_x, checkbox_y, '☑')
                else:
                    checkbox_x = positions['inner_outer_col'] + positions['inner_checkbox'][0]
                    checkbox_y = row_y + positions['inner_checkbox'][1]
                    c.drawString(checkbox_x, checkbox_y, '☐')
                
                # Outer checkbox
                if 'outer' in frame_options:
                    checkbox_x = positions['inner_outer_col'] + positions['outer_checkbox'][0]
                    checkbox_y = row_y + positions['outer_checkbox'][1]
                    c.drawString(checkbox_x, checkbox_y, '☑')
                else:
                    checkbox_x = positions['inner_outer_col'] + positions['outer_checkbox'][0]
                    checkbox_y = row_y + positions['outer_checkbox'][1]
                    c.drawString(checkbox_x, checkbox_y, '☐')
                
                # Location text for rows 2-4
                if i > 0:
                    loc_x = positions['frame_size_col'] + positions['location_text'][0]
                    loc_y = row_y + positions['location_text'][1]
                    c.setFont("Helvetica", 7)
                    c.drawString(loc_x, loc_y, "Location :")
                    c.setFont("Helvetica", 9)
        
        c.save()
        buffer.seek(0)
        return buffer
    
    def _overlay_door_template(self, data: Dict[str, Any], template_path: str, output_path: str):
        """Overlay data on DOOR template"""
        
        try:
            print(f"DEBUG: Opening template file: {template_path}")
            print(f"DEBUG: Template exists: {os.path.exists(template_path)}")
            
            # Read the original template
            with open(template_path, 'rb') as template_file:
                reader = PdfReader(template_file)
                writer = PdfWriter()
                
                # Get the first page
                template_page = reader.pages[0]
                
                # Create overlay with data
                overlay_buffer = self._create_door_overlay(data)
                
                # Save overlay for debugging
                overlay_test_path = output_path.replace('.pdf', '_overlay_only.pdf')
                with open(overlay_test_path, 'wb') as test_file:
                    test_file.write(overlay_buffer.getvalue())
                print(f"DEBUG: Saved overlay test file: {overlay_test_path}")
                
                # Read the overlay
                print(f"DEBUG: Creating overlay with {len(overlay_buffer.getvalue())} bytes")
                overlay_reader = PdfReader(overlay_buffer)
                overlay_page = overlay_reader.pages[0]
                print(f"DEBUG: Overlay page created successfully")
                
                # Merge template with overlay
                print(f"DEBUG: Merging template with overlay...")
                
                # Try alternative merge method
                try:
                    template_page.merge_page(overlay_page)
                    print(f"DEBUG: merge_page() successful")
                except Exception as merge_error:
                    print(f"DEBUG: merge_page() failed: {merge_error}")
                    # Try alternative: overlay on top
                    overlay_page.merge_page(template_page)
                    template_page = overlay_page
                    print(f"DEBUG: Used overlay as base instead")
                
                writer.add_page(template_page)
                print(f"DEBUG: Pages merged successfully")
                
                # Write the result
                with open(output_path, 'wb') as output_file:
                    writer.write(output_file)
                    
                print(f"DEBUG: Final file size: {os.path.getsize(output_path)} bytes")
                    
                print(f"Door JO generated: {output_path}")
                
        except Exception as e:
            print(f"ERROR: Door template overlay failed!")
            print(f"ERROR: Exception details: {e}")
            print(f"ERROR: Template path was: {template_path}")
            import traceback
            traceback.print_exc()
            self._create_fallback_jo(data, output_path)
    
    def _create_door_overlay(self, data: Dict[str, Any]) -> io.BytesIO:
        """Create overlay data for door template"""
        
        # DEBUG: Print extracted data to console
        print("DEBUG: Extracted data structure:")
        print(f"Full data: {data}")
        
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        
        # Extract data
        structured = data.get('structured_data', {})
        doc_info = structured.get('document_info', {})
        company_info = structured.get('company_info', {})
        products = structured.get('product_specs', [])
        door_specs = structured.get('door_specs', {})
        
        # DEBUG: Print individual data sections
        print(f"DEBUG: structured_data: {structured}")
        print(f"DEBUG: doc_info: {doc_info}")
        print(f"DEBUG: company_info: {company_info}")
        print(f"DEBUG: products: {products}")
        print(f"DEBUG: door_specs: {door_specs}")
        
        # Get field positions
        positions = self.field_positions['door']
        
        # Set font - make it larger and bold for visibility
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(colors.black)  # Use black color for production
        
        # Simple, clean overlay
        
        # Fill header fields
        current_date = datetime.now().strftime('%d/%m/%Y')
        
        # Header info
        job_order_no = f"JO-{datetime.now().strftime('%Y%m%d')}-001"
        job_order_date = doc_info.get('date', current_date)
        po_no = doc_info.get('po_number', '')
        delivery_date = current_date
        customer_name = company_info.get('company_name', '')
        
        print(f"DEBUG: Writing header fields:")
        print(f"  Job Order No: '{job_order_no}' at {positions['job_order_no']}")
        print(f"  Job Order Date: '{job_order_date}' at {positions['job_order_date']}")
        print(f"  PO No: '{po_no}' at {positions['po_no']}")
        print(f"  Customer Name: '{customer_name}' at {positions['customer_name']}")
        
        # Set font for header fields
        c.setFont("Helvetica", 9)
        c.setFillColor(colors.black)
        c.drawString(positions['job_order_no'][0], positions['job_order_no'][1], job_order_no)
        c.drawString(positions['job_order_date'][0], positions['job_order_date'][1], job_order_date)
        c.drawString(positions['po_no'][0], positions['po_no'][1], po_no)
        
        # Customer info
        c.drawString(positions['delivery_date'][0], positions['delivery_date'][1], delivery_date)
        c.drawString(positions['customer_name'][0], positions['customer_name'][1], customer_name)
        c.drawString(positions['measure_by'][0], positions['measure_by'][1], 'Auto Generated')
        
        # Simple - just header fields for now
        
        c.save()
        buffer.seek(0)
        return buffer
    
    def _overlay_general_template(self, data: Dict[str, Any], template_path: str, output_path: str):
        """Overlay data on GENERAL template"""
        
        try:
            # For general template, we'll create a simple overlay
            # or copy the original if it's already suitable
            
            with open(template_path, 'rb') as template_file:
                reader = PdfReader(template_file)
                writer = PdfWriter()
                
                # Just copy the original for now, can add overlay later
                for page in reader.pages:
                    writer.add_page(page)
                
                with open(output_path, 'wb') as output_file:
                    writer.write(output_file)
                    
                print(f"General JO generated: {output_path}")
                
        except Exception as e:
            print(f"Error with general template: {e}")
            self._create_fallback_jo(data, output_path)
    
    def _create_fallback_jo(self, data: Dict[str, Any], output_path: str):
        """Create a fallback JO when template overlay fails"""
        
        c = canvas.Canvas(output_path, pagesize=A4)
        
        # Simple fallback JO
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, 800, "SENDORA GROUP SDN BHD (HQ)")
        c.drawString(50, 780, "JOB ORDER")
        
        c.setFont("Helvetica", 10)
        c.drawString(50, 750, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        c.drawString(50, 730, "Template overlay failed - using fallback format")
        
        # Add extracted data
        structured = data.get('structured_data', {})
        y_pos = 700
        
        for key, value in structured.items():
            if isinstance(value, dict):
                c.drawString(50, y_pos, f"{key.upper()}:")
                y_pos -= 15
                for sub_key, sub_value in value.items():
                    c.drawString(70, y_pos, f"  {sub_key}: {sub_value}")
                    y_pos -= 12
            else:
                c.drawString(50, y_pos, f"{key.upper()}: {value}")
                y_pos -= 15
        
        c.save()
        print(f"Fallback JO created: {output_path}")