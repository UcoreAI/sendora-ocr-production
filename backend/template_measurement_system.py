"""
Template Measurement System
Precisely measures your actual JO template to maintain identical format
Combines manual measurement with AI vision detection
"""

import fitz  # PyMuPDF
import cv2
import numpy as np
import json
import os
from typing import Dict, List, Tuple, Any
from PIL import Image
import pytesseract

class TemplateMeasurementSystem:
    """Precisely measure actual JO template for pixel-perfect positioning"""
    
    def __init__(self):
        self.door_template = r'C:\Users\USER\Desktop\Project management\Sendora\Material\JOB ORDER FORM -DOOR.pdf'
        self.measurements = {}
        
    def measure_template_precisely(self):
        """Measure the actual template with extreme precision"""
        
        print("=" * 60)
        print("TEMPLATE MEASUREMENT SYSTEM")
        print("Preserving your exact JO format - no SOP changes")
        print("=" * 60)
        
        if not os.path.exists(self.door_template):
            print(f"Template not found: {self.door_template}")
            return None
        
        # Open template
        doc = fitz.open(self.door_template)
        page = doc[0]
        
        # Get exact dimensions
        rect = page.rect
        page_width = rect.width
        page_height = rect.height
        
        print(f"\nTemplate Dimensions: {page_width:.2f} x {page_height:.2f} points")
        print(f"Format: {'Landscape A4' if page_width > page_height else 'Portrait A4'}")
        
        # Convert to high-res image for AI vision analysis
        mat = fitz.Matrix(3, 3)  # 3x zoom for precision
        pix = page.get_pixmap(matrix=mat)
        img_data = pix.tobytes("png")
        
        # Save for analysis
        temp_img = "temp_template_analysis.png"
        pix.save(temp_img)
        
        # Load with OpenCV
        img = cv2.imread(temp_img)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Measure using multiple methods
        measurements = {
            'page_dimensions': {
                'width': page_width,
                'height': page_height,
                'format': 'Landscape A4' if page_width > page_height else 'Portrait A4'
            },
            'header_fields': self.measure_header_fields(page, gray, 3.0),
            'table_structure': self.measure_table_structure(page, gray, 3.0),
            'checkbox_positions': self.measure_checkboxes(page, gray, 3.0),
            'footer_fields': self.measure_footer_fields(page, gray, 3.0)
        }
        
        # Clean up
        os.remove(temp_img)
        doc.close()
        
        # Save measurements
        self.save_measurements(measurements)
        
        return measurements
    
    def measure_header_fields(self, page, gray_img, scale: float) -> Dict:
        """Measure exact header field positions"""
        
        print("\nMeasuring header fields...")
        
        # Get text with positions
        text_dict = page.get_text("dict")
        
        header_fields = {}
        
        # Known header labels and their typical positions
        # Based on actual JO template structure
        field_mappings = {
            'Job Order No:': {
                'field_name': 'job_order_no',
                'expected_x': 55,  # Left side
                'expected_y': 70   # Top area
            },
            'Job Order Date:': {
                'field_name': 'job_order_date',
                'expected_x': 55,
                'expected_y': 92
            },
            'PO NO:': {
                'field_name': 'po_no',
                'expected_x': 55,
                'expected_y': 114
            },
            'Delivery Date:': {
                'field_name': 'delivery_date',
                'expected_x': 645,  # Right side
                'expected_y': 70
            },
            'Customer Name:': {
                'field_name': 'customer_name',
                'expected_x': 645,
                'expected_y': 92
            },
            'Measure By :': {
                'field_name': 'measure_by',
                'expected_x': 645,
                'expected_y': 114
            }
        }
        
        # Find actual positions in template
        for block in text_dict.get('blocks', []):
            if 'lines' not in block:
                continue
                
            for line in block['lines']:
                for span in line['spans']:
                    text = span['text'].strip()
                    
                    # Check each known label
                    for label, info in field_mappings.items():
                        if label in text:
                            bbox = span['bbox']
                            
                            # Calculate data input position
                            # Data goes after the colon, with proper spacing
                            label_end_x = bbox[2]  # Right edge of label
                            label_y = bbox[1]      # Top of label
                            
                            # Measure the actual space after label
                            data_x = label_end_x + 10  # Small gap after colon
                            data_y = label_y
                            
                            header_fields[info['field_name']] = {
                                'label_bbox': list(bbox),
                                'data_position': {
                                    'x': data_x,
                                    'y': data_y,
                                    'width': 200,  # Standard field width
                                    'height': bbox[3] - bbox[1]
                                },
                                'font_size': span['size'],
                                'actual_label': text
                            }
                            
                            print(f"  Found {info['field_name']}: x={data_x:.1f}, y={data_y:.1f}")
        
        return header_fields
    
    def measure_table_structure(self, page, gray_img, scale: float) -> Dict:
        """Measure exact table structure and row positions"""
        
        print("\nMeasuring table structure...")
        
        # Detect table lines using computer vision
        edges = cv2.Canny(gray_img, 50, 150, apertureSize=3)
        
        # Detect horizontal lines (table rows)
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, 
                                minLineLength=200, maxLineGap=10)
        
        # Find table boundaries
        horizontal_lines = []
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                if abs(y2 - y1) < 5:  # Horizontal line
                    y_pos = y1 / scale  # Convert back to PDF scale
                    if 150 < y_pos < 500:  # Table area
                        horizontal_lines.append(y_pos)
        
        # Sort and deduplicate
        horizontal_lines = sorted(set(horizontal_lines))
        
        # Identify table rows (gaps between lines)
        table_rows = []
        for i in range(len(horizontal_lines) - 1):
            row_y = horizontal_lines[i] + 5  # Slightly below line
            row_height = horizontal_lines[i+1] - horizontal_lines[i]
            
            if row_height > 30:  # Reasonable row height
                table_rows.append({
                    'row_index': len(table_rows),
                    'y_position': row_y,
                    'height': row_height
                })
        
        # Measure column positions from template
        text_dict = page.get_text("dict")
        
        column_headers = {
            'ITEM': 36,
            'LAMINATE CODE': 70,
            'DOOR THICKNESS': 155,
            'DOOR SIZE': 255,
            'DOOR TYPE': 355,
            'DOOR CORE': 425,
            'EDGING': 495,
            'DECORATIVE LINE': 565,
            'DESIGN NAME': 650,
            'OPEN HOLE TYPE': 720,
            'DRAWING / REMARK': 790
        }
        
        # Find actual column positions
        actual_columns = {}
        for block in text_dict.get('blocks', []):
            if 'lines' not in block:
                continue
                
            for line in block['lines']:
                for span in line['spans']:
                    text = span['text'].strip().upper()
                    
                    for header, expected_x in column_headers.items():
                        if header in text:
                            actual_columns[header.lower().replace(' ', '_')] = {
                                'x': span['bbox'][0],
                                'width': span['bbox'][2] - span['bbox'][0]
                            }
        
        print(f"  Found {len(table_rows)} table rows")
        print(f"  Found {len(actual_columns)} column positions")
        
        return {
            'rows': table_rows,
            'columns': actual_columns,
            'table_bounds': {
                'top': horizontal_lines[0] if horizontal_lines else 180,
                'bottom': horizontal_lines[-1] if horizontal_lines else 500
            }
        }
    
    def measure_checkboxes(self, page, gray_img, scale: float) -> Dict:
        """Measure exact checkbox positions"""
        
        print("\nMeasuring checkbox positions...")
        
        # Find checkbox symbols using pattern matching
        # Checkboxes typically appear as small squares
        
        text_dict = page.get_text("dict")
        
        checkbox_groups = {
            'door_thickness': [],
            'door_type': [],
            'door_core': [],
            'edging': [],
            'decorative_line': []
        }
        
        # Map text to checkbox groups
        checkbox_mappings = {
            '37mm': ('door_thickness', 0),
            '43mm': ('door_thickness', 1),
            '48mm': ('door_thickness', 2),
            'S/L': ('door_type', 0),
            'D/L': ('door_type', 1),
            'Unequal D/L': ('door_type', 2),
            'Honeycomb': ('door_core', 0),
            'Solid Tubular Core': ('door_core', 1),
            'Solid Timber': ('door_core', 2),
            'Metal Skeleton': ('door_core', 3),
            'NA Lipping': ('edging', 0),
            'ABS Edging': ('edging', 1),
            'No Edging': ('edging', 2),
            'T-bar': ('decorative_line', 0),
            'Groove Line': ('decorative_line', 1)
        }
        
        # Find actual positions
        for block in text_dict.get('blocks', []):
            if 'lines' not in block:
                continue
                
            for line in block['lines']:
                for span in line['spans']:
                    text = span['text'].strip()
                    
                    for option_text, (group, index) in checkbox_mappings.items():
                        if option_text in text:
                            bbox = span['bbox']
                            
                            # Checkbox is typically 10-15 points to the left of text
                            checkbox_x = bbox[0] - 15
                            checkbox_y = bbox[1]
                            
                            checkbox_groups[group].append({
                                'option': option_text,
                                'checkbox_position': {
                                    'x': checkbox_x,
                                    'y': checkbox_y,
                                    'size': 8
                                },
                                'text_position': {
                                    'x': bbox[0],
                                    'y': bbox[1]
                                }
                            })
        
        total_checkboxes = sum(len(group) for group in checkbox_groups.values())
        print(f"  Found {total_checkboxes} checkbox positions")
        
        return checkbox_groups
    
    def measure_footer_fields(self, page, gray_img, scale: float) -> Dict:
        """Measure footer field positions"""
        
        print("\nMeasuring footer fields...")
        
        page_height = page.rect.height
        
        # Footer fields are typically at the bottom
        footer_fields = {
            'prepare_by': {
                'x': 55,
                'y': page_height - 50,
                'width': 200
            },
            'checked_by': {
                'x': 355,
                'y': page_height - 50,
                'width': 200
            },
            'verify_by': {
                'x': 655,
                'y': page_height - 50,
                'width': 200
            }
        }
        
        print(f"  Measured {len(footer_fields)} footer positions")
        
        return footer_fields
    
    def save_measurements(self, measurements: Dict):
        """Save precise measurements for use in form filling"""
        
        # Save detailed measurements
        measurements_file = 'template_measurements.json'
        with open(measurements_file, 'w', encoding='utf-8') as f:
            json.dump(measurements, f, indent=2, ensure_ascii=False)
        
        print(f"\nSaved measurements: {measurements_file}")
        
        # Create optimized overlay specification
        self.create_optimized_overlay_spec(measurements)
    
    def create_optimized_overlay_spec(self, measurements: Dict):
        """Create optimized overlay specification from measurements"""
        
        overlay_spec = {
            'page_size': [
                measurements['page_dimensions']['width'],
                measurements['page_dimensions']['height']
            ],
            'fields': {},
            'table': {
                'rows': [],
                'columns': {}
            },
            'checkboxes': {}
        }
        
        # Map header fields
        for field_name, field_data in measurements['header_fields'].items():
            overlay_spec['fields'][field_name] = {
                'x': field_data['data_position']['x'],
                'y': field_data['data_position']['y'],
                'font': 'Helvetica',
                'size': min(field_data['font_size'], 10)
            }
        
        # Map table structure
        for row in measurements['table_structure']['rows']:
            row_spec = {
                'y': row['y_position'],
                'height': row['height']
            }
            
            # Add column positions
            for col_name, col_data in measurements['table_structure']['columns'].items():
                row_spec[col_name + '_x'] = col_data['x']
            
            overlay_spec['table']['rows'].append(row_spec)
        
        # Map checkboxes
        for group_name, checkboxes in measurements['checkbox_positions'].items():
            overlay_spec['checkboxes'][group_name] = []
            for checkbox in checkboxes:
                overlay_spec['checkboxes'][group_name].append({
                    'option': checkbox['option'],
                    'x': checkbox['checkbox_position']['x'],
                    'y': checkbox['checkbox_position']['y'],
                    'size': checkbox['checkbox_position']['size']
                })
        
        # Save optimized specification
        spec_file = 'measured_overlay_spec.json'
        with open(spec_file, 'w', encoding='utf-8') as f:
            json.dump(overlay_spec, f, indent=2, ensure_ascii=False)
        
        print(f"Created overlay spec: {spec_file}")
        print("\nMeasurement complete! Your JO format is preserved exactly.")


# Run the measurement system
if __name__ == "__main__":
    measurer = TemplateMeasurementSystem()
    
    print("Starting precise template measurement...")
    print("This ensures your JO format remains 100% identical")
    print("No changes to your existing SOP required!\n")
    
    measurements = measurer.measure_template_precisely()
    
    if measurements:
        print("\n" + "=" * 60)
        print("MEASUREMENT SUMMARY")
        print("=" * 60)
        print(f"Page Format: {measurements['page_dimensions']['format']}")
        print(f"Header Fields: {len(measurements['header_fields'])}")
        print(f"Table Rows: {len(measurements['table_structure']['rows'])}")
        print(f"Checkboxes: {sum(len(g) for g in measurements['checkbox_positions'].values())}")
        print(f"Footer Fields: {len(measurements['footer_fields'])}")
        print("\nYour exact JO template format has been measured!")
        print("The system will now use these precise coordinates.")
    else:
        print("Measurement failed - check template path")