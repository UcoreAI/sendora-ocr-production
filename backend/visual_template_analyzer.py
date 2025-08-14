"""
Visual Template Analyzer
Uses computer vision to precisely detect form fields and table structures
"""

import fitz  # PyMuPDF
import cv2
import numpy as np
import json
import os
from typing import Dict, List, Tuple, Any
import pytesseract
from PIL import Image

class VisualTemplateAnalyzer:
    """Analyze template structure using computer vision"""
    
    def __init__(self):
        self.template_paths = {
            'door': r'C:\Users\USER\Desktop\Project management\Sendora\Material\JOB ORDER FORM -DOOR.pdf',
            'frame': r'C:\Users\USER\Desktop\Project management\Sendora\Material\JOB ORDER FORM  - FRAME.pdf',
            'combined': r'C:\Users\USER\Desktop\Project management\Sendora\Material\JOB ORDER FORM.pdf'
        }
        
    def analyze_all_templates(self):
        """Analyze all templates with computer vision"""
        
        results = {}
        
        for template_name, template_path in self.template_paths.items():
            if os.path.exists(template_path):
                print(f"\n🔍 Analyzing {template_name} template with computer vision...")
                coords = self.analyze_template_visually(template_path, template_name)
                results[template_name] = coords
                
                # Save precise specifications
                spec_file = f"visual_{template_name}_spec.json"
                with open(spec_file, 'w', encoding='utf-8') as f:
                    json.dump(coords, f, indent=2, ensure_ascii=False)
                print(f"✅ Saved: {spec_file}")
            else:
                print(f"❌ Template not found: {template_path}")
        
        return results
    
    def analyze_template_visually(self, pdf_path: str, template_name: str) -> Dict:
        """Analyze template using computer vision"""
        
        # Convert PDF to image for CV analysis
        doc = fitz.open(pdf_path)
        page = doc[0]  # First page
        
        # Get page dimensions
        rect = page.rect
        page_width = rect.width
        page_height = rect.height
        
        # Convert to image
        mat = fitz.Matrix(2, 2)  # 2x zoom for better quality
        pix = page.get_pixmap(matrix=mat)
        img_data = pix.tobytes("png")
        
        # Load with OpenCV
        nparr = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        doc.close()
        
        # Detect form structure
        coordinates = {
            'template_name': template_name,
            'page_size': [page_width, page_height],
            'header_fields': {},
            'table_structure': {},
            'checkbox_groups': {},
            'form_lines': []
        }
        
        # Detect lines and boxes
        self.detect_form_lines(gray, coordinates, 2.0)  # Scale factor for 2x zoom
        
        # Detect text areas and field positions
        self.detect_text_fields(gray, coordinates, 2.0)
        
        # Detect table structure
        self.detect_table_structure(gray, coordinates, 2.0)
        
        # Create overlay specification
        overlay_spec = self.create_visual_overlay_spec(coordinates)
        
        return overlay_spec
    
    def detect_form_lines(self, gray_img: np.ndarray, coordinates: Dict, scale_factor: float):
        """Detect horizontal and vertical lines in the form"""
        
        # Detect horizontal lines
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
        horizontal_lines = cv2.morphologyEx(gray_img, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
        
        # Detect vertical lines  
        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))
        vertical_lines = cv2.morphologyEx(gray_img, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
        
        # Find line coordinates
        h_lines = cv2.HoughLinesP(horizontal_lines, 1, np.pi/180, threshold=100, minLineLength=100, maxLineGap=10)
        v_lines = cv2.HoughLinesP(vertical_lines, 1, np.pi/180, threshold=100, minLineLength=50, maxLineGap=10)
        
        form_lines = []
        
        if h_lines is not None:
            for line in h_lines:
                x1, y1, x2, y2 = line[0]
                form_lines.append({
                    'type': 'horizontal',
                    'x1': x1 / scale_factor, 'y1': y1 / scale_factor,
                    'x2': x2 / scale_factor, 'y2': y2 / scale_factor
                })
        
        if v_lines is not None:
            for line in v_lines:
                x1, y1, x2, y2 = line[0]
                form_lines.append({
                    'type': 'vertical',
                    'x1': x1 / scale_factor, 'y1': y1 / scale_factor,
                    'x2': x2 / scale_factor, 'y2': y2 / scale_factor
                })
        
        coordinates['form_lines'] = form_lines
        print(f"📏 Detected {len(form_lines)} form lines")
    
    def detect_text_fields(self, gray_img: np.ndarray, coordinates: Dict, scale_factor: float):
        """Detect text areas and determine field positions"""
        
        # Use Tesseract to detect text blocks
        try:
            # Get text with bounding boxes
            data = pytesseract.image_to_data(gray_img, output_type=pytesseract.Output.DICT)
            
            header_fields = {}
            
            # Look for header field labels
            field_labels = {
                'job order no': 'job_order_no',
                'job order date': 'job_order_date', 
                'po no': 'po_no',
                'delivery date': 'delivery_date',
                'customer name': 'customer_name',
                'measure by': 'measure_by'
            }
            
            for i, text in enumerate(data['text']):
                if data['conf'][i] > 30:  # Confidence threshold
                    text_lower = text.lower().strip()
                    
                    # Check if this text matches a field label
                    for label, field_name in field_labels.items():
                        if label in text_lower and len(text_lower) > 3:
                            x = data['left'][i] / scale_factor
                            y = data['top'][i] / scale_factor
                            w = data['width'][i] / scale_factor
                            h = data['height'][i] / scale_factor
                            
                            # Position data field to the right of label
                            data_x = x + w + 10
                            data_y = y
                            
                            header_fields[field_name] = {
                                'label_position': {'x': x, 'y': y, 'width': w, 'height': h},
                                'data_position': {'x': data_x, 'y': data_y, 'width': 150, 'height': h},
                                'font_size': max(8, min(h, 12))
                            }
            
            coordinates['header_fields'] = header_fields
            print(f"📝 Detected {len(header_fields)} header fields")
            
        except Exception as e:
            print(f"⚠️ OCR detection failed: {e}")
            # Use geometric analysis as fallback
            self.detect_fields_geometrically(gray_img, coordinates, scale_factor)
    
    def detect_fields_geometrically(self, gray_img: np.ndarray, coordinates: Dict, scale_factor: float):
        """Fallback: detect fields using geometric analysis"""
        
        # Standard positions based on common form layouts
        page_height = coordinates['page_size'][1]
        
        header_fields = {
            'job_order_no': {
                'data_position': {'x': 140, 'y': 50, 'width': 120, 'height': 12},
                'font_size': 10
            },
            'job_order_date': {
                'data_position': {'x': 400, 'y': 50, 'width': 100, 'height': 12},
                'font_size': 10
            },
            'customer_name': {
                'data_position': {'x': 160, 'y': 80, 'width': 300, 'height': 12},
                'font_size': 10
            },
            'po_no': {
                'data_position': {'x': 120, 'y': 110, 'width': 120, 'height': 12},
                'font_size': 10
            },
            'delivery_date': {
                'data_position': {'x': 400, 'y': 80, 'width': 100, 'height': 12},
                'font_size': 10
            },
            'measure_by': {
                'data_position': {'x': 400, 'y': 110, 'width': 150, 'height': 12},
                'font_size': 10
            }
        }
        
        coordinates['header_fields'] = header_fields
        print(f"🔧 Applied geometric positioning: {len(header_fields)} fields")
    
    def detect_table_structure(self, gray_img: np.ndarray, coordinates: Dict, scale_factor: float):
        """Detect table structure and row positions"""
        
        # Find rectangular contours (table cells)
        edges = cv2.Canny(gray_img, 50, 150, apertureSize=3)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        table_cells = []
        for contour in contours:
            # Approximate contour to polygon
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            
            # If it's roughly rectangular and large enough
            if len(approx) == 4:
                x, y, w, h = cv2.boundingRect(contour)
                if w > 50 and h > 20:  # Minimum cell size
                    table_cells.append({
                        'x': x / scale_factor,
                        'y': y / scale_factor,
                        'width': w / scale_factor,
                        'height': h / scale_factor
                    })
        
        # Group cells into rows
        table_rows = []
        if table_cells:
            # Sort by Y position to group rows
            table_cells.sort(key=lambda cell: cell['y'])
            
            current_row = []
            current_y = table_cells[0]['y']
            
            for cell in table_cells:
                if abs(cell['y'] - current_y) < 10:  # Same row
                    current_row.append(cell)
                else:
                    if current_row:
                        table_rows.append(current_row)
                    current_row = [cell]
                    current_y = cell['y']
            
            if current_row:
                table_rows.append(current_row)
        
        coordinates['table_structure'] = {
            'rows': table_rows,
            'total_cells': len(table_cells)
        }
        
        print(f"📊 Detected {len(table_rows)} table rows with {len(table_cells)} cells")
    
    def create_visual_overlay_spec(self, coordinates: Dict) -> Dict:
        """Create overlay specification from visual analysis"""
        
        overlay_spec = {
            'page_size': coordinates['page_size'],
            'fields': {},
            'checkboxes': {},
            'table_rows': []
        }
        
        # Map header fields
        for field_name, field_info in coordinates['header_fields'].items():
            data_pos = field_info['data_position']
            overlay_spec['fields'][field_name] = {
                'x': data_pos['x'],
                'y': data_pos['y'],
                'font': 'Helvetica',
                'size': field_info['font_size']
            }
        
        # Map table structure
        for i, row_cells in enumerate(coordinates['table_structure'].get('rows', [])):
            if row_cells:
                # Use first cell of row as reference
                first_cell = row_cells[0]
                overlay_spec['table_rows'].append({
                    'row_index': i,
                    'y_position': first_cell['y'],
                    'laminate_code_x': first_cell['x'] + 5,  # Slight offset
                    'door_size_x': first_cell['x'] + first_cell['width'] + 10
                })
        
        return overlay_spec


# Main execution
if __name__ == "__main__":
    analyzer = VisualTemplateAnalyzer()
    
    print("🤖 Visual Template Analysis Starting...")
    print("=" * 60)
    
    try:
        results = analyzer.analyze_all_templates()
        
        print("\n" + "=" * 60)
        print("✅ Visual analysis complete!")
        
        for template_name, spec in results.items():
            field_count = len(spec.get('fields', {}))
            table_rows = len(spec.get('table_rows', []))
            print(f"  📋 {template_name}: {field_count} fields, {table_rows} table rows")
        
        print("\n💡 Use visual_*_spec.json files for precise positioning!")
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        import traceback
        traceback.print_exc()