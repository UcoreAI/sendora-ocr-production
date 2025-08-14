"""
Visual Template Debugger
Shows exactly where fields, lines, and checkboxes are on the template
This will help us get pixel-perfect positioning
"""

import fitz  # PyMuPDF
import os
from typing import Dict, List, Tuple

class VisualTemplateDebugger:
    """Debug and visualize exact positions on template"""
    
    def __init__(self):
        self.door_template = r'C:\Users\USER\Desktop\Project management\Sendora\Material\JOB ORDER FORM -DOOR.pdf'
        
    def create_debug_overlay(self):
        """Create a debug version showing all positions"""
        
        if not os.path.exists(self.door_template):
            print(f"Template not found: {self.door_template}")
            return
        
        # Open template
        doc = fitz.open(self.door_template)
        page = doc[0]
        
        # Get page dimensions
        rect = page.rect
        width = rect.width
        height = rect.height
        
        print(f"Page dimensions: {width} x {height}")
        print(f"Page orientation: {'Landscape' if width > height else 'Portrait'}")
        
        # Create output document with markers
        output_doc = fitz.open()
        output_page = output_doc.new_page(width=width, height=height)
        
        # Copy original template
        output_page.show_pdf_page(rect, doc, 0)
        
        # Add visual markers for debugging
        self.add_coordinate_grid(output_page)
        self.mark_field_positions(output_page)
        self.mark_checkbox_positions(output_page)
        self.mark_table_positions(output_page)
        
        # Save debug version
        debug_file = "debug_template_with_markers.pdf"
        output_doc.save(debug_file)
        output_doc.close()
        doc.close()
        
        print(f"Created debug template: {debug_file}")
        
        # Also extract exact measurements
        self.extract_exact_measurements()
    
    def add_coordinate_grid(self, page):
        """Add coordinate grid for reference"""
        
        width = page.rect.width
        height = page.rect.height
        
        # Add grid lines every 50 points
        for x in range(0, int(width), 50):
            # Vertical lines
            page.draw_line((x, 0), (x, height), width=0.5, color=(0.8, 0.8, 0.8))
            # Add x coordinate
            if x % 100 == 0:
                page.insert_text((x+2, 10), str(x), fontsize=6, color=(0.5, 0.5, 0.5))
        
        for y in range(0, int(height), 50):
            # Horizontal lines
            page.draw_line((0, y), (width, y), width=0.5, color=(0.8, 0.8, 0.8))
            # Add y coordinate
            if y % 100 == 0:
                page.insert_text((2, y+10), str(y), fontsize=6, color=(0.5, 0.5, 0.5))
    
    def mark_field_positions(self, page):
        """Mark where header fields should be"""
        
        # Mark header field positions with red boxes
        header_positions = [
            {'name': 'JO_NO', 'x': 150, 'y': 70, 'width': 150, 'height': 15},
            {'name': 'JO_DATE', 'x': 150, 'y': 92, 'width': 150, 'height': 15},
            {'name': 'PO_NO', 'x': 100, 'y': 114, 'width': 150, 'height': 15},
            {'name': 'DELIVERY', 'x': 700, 'y': 70, 'width': 120, 'height': 15},
            {'name': 'CUSTOMER', 'x': 700, 'y': 92, 'width': 120, 'height': 15},
            {'name': 'MEASURE', 'x': 700, 'y': 114, 'width': 120, 'height': 15}
        ]
        
        for field in header_positions:
            rect = fitz.Rect(field['x'], field['y'], 
                            field['x'] + field['width'], 
                            field['y'] + field['height'])
            page.draw_rect(rect, color=(1, 0, 0), width=1)
            page.insert_text((field['x'], field['y']-2), field['name'], 
                            fontsize=6, color=(1, 0, 0))
    
    def mark_checkbox_positions(self, page):
        """Mark where checkboxes are"""
        
        # Scan for checkbox squares in the template
        # These are typically small squares around 8x8 points
        
        # Known checkbox areas (approximate)
        checkbox_areas = [
            # Door thickness checkboxes (first row)
            {'group': 'thickness', 'row': 0, 'x': 143, 'y': 207},
            {'group': 'thickness', 'row': 0, 'x': 143, 'y': 225},
            {'group': 'thickness', 'row': 0, 'x': 143, 'y': 243},
            
            # Door type checkboxes (first row)
            {'group': 'type', 'row': 0, 'x': 343, 'y': 207},
            {'group': 'type', 'row': 0, 'x': 343, 'y': 225},
            {'group': 'type', 'row': 0, 'x': 343, 'y': 243},
        ]
        
        for cb in checkbox_areas:
            # Draw green circle at checkbox position
            center = (cb['x'] + 4, cb['y'] + 4)
            page.draw_circle(center, 4, color=(0, 1, 0), width=1)
    
    def mark_table_positions(self, page):
        """Mark table row positions"""
        
        # Table rows (approximate)
        table_rows = [
            {'row': 1, 'y': 200, 'height': 80},
            {'row': 2, 'y': 290, 'height': 80},
            {'row': 3, 'y': 380, 'height': 80},
            {'row': 4, 'y': 470, 'height': 80}
        ]
        
        for row in table_rows:
            # Draw blue line at row position
            page.draw_line((30, row['y']), (810, row['y']), 
                          color=(0, 0, 1), width=1)
            page.insert_text((10, row['y']), f"Row {row['row']}", 
                            fontsize=8, color=(0, 0, 1))
    
    def extract_exact_measurements(self):
        """Extract exact measurements by analyzing the template"""
        
        print("\nExtracting exact measurements...")
        
        doc = fitz.open(self.door_template)
        page = doc[0]
        
        # Get all text with exact positions
        text_dict = page.get_text("dict")
        
        measurements = {
            'page_size': [page.rect.width, page.rect.height],
            'header_fields': {},
            'table_cells': [],
            'checkboxes': []
        }
        
        # Find exact positions of key labels
        for block in text_dict.get('blocks', []):
            if 'lines' not in block:
                continue
                
            for line in block['lines']:
                for span in line['spans']:
                    text = span['text'].strip()
                    bbox = span['bbox']
                    
                    # Header labels
                    if 'Job Order No:' in text:
                        measurements['header_fields']['job_order_no'] = {
                            'label_end_x': bbox[2],
                            'label_y': bbox[1],
                            'data_x': bbox[2] + 5,  # Data starts after label
                            'data_y': bbox[1]
                        }
                    elif 'Job Order Date:' in text:
                        measurements['header_fields']['job_order_date'] = {
                            'label_end_x': bbox[2],
                            'label_y': bbox[1],
                            'data_x': bbox[2] + 5,
                            'data_y': bbox[1]
                        }
                    elif 'PO NO:' in text:
                        measurements['header_fields']['po_no'] = {
                            'label_end_x': bbox[2],
                            'label_y': bbox[1],
                            'data_x': bbox[2] + 5,
                            'data_y': bbox[1]
                        }
                    elif 'Delivery Date:' in text:
                        measurements['header_fields']['delivery_date'] = {
                            'label_end_x': bbox[2],
                            'label_y': bbox[1],
                            'data_x': bbox[2] + 5,
                            'data_y': bbox[1]
                        }
                    elif 'Customer Name:' in text:
                        measurements['header_fields']['customer_name'] = {
                            'label_end_x': bbox[2],
                            'label_y': bbox[1],
                            'data_x': bbox[2] + 5,
                            'data_y': bbox[1]
                        }
                    elif 'Measure By :' in text:
                        measurements['header_fields']['measure_by'] = {
                            'label_end_x': bbox[2],
                            'label_y': bbox[1],
                            'data_x': bbox[2] + 5,
                            'data_y': bbox[1]
                        }
                    
                    # Table headers
                    elif 'ITEM' == text:
                        measurements['table_cells'].append({
                            'type': 'header',
                            'text': text,
                            'x': bbox[0],
                            'y': bbox[1],
                            'width': bbox[2] - bbox[0],
                            'height': bbox[3] - bbox[1]
                        })
                    
                    # Checkbox labels
                    elif text in ['37mm', '43mm', '48mm', 'S/L', 'D/L', 'Honeycomb']:
                        measurements['checkboxes'].append({
                            'label': text,
                            'text_x': bbox[0],
                            'text_y': bbox[1],
                            'checkbox_x': bbox[0] - 15,  # Checkbox before text
                            'checkbox_y': bbox[1]
                        })
        
        doc.close()
        
        # Print findings
        print(f"\nFound {len(measurements['header_fields'])} header fields:")
        for field, pos in measurements['header_fields'].items():
            print(f"  {field}: data starts at x={pos['data_x']:.1f}, y={pos['data_y']:.1f}")
        
        print(f"\nFound {len(measurements['checkboxes'])} checkboxes")
        print(f"Found {len(measurements['table_cells'])} table elements")
        
        # Save measurements
        import json
        with open('exact_template_measurements.json', 'w') as f:
            json.dump(measurements, f, indent=2)
        
        print("\nSaved exact measurements to: exact_template_measurements.json")
        
        return measurements


if __name__ == "__main__":
    debugger = VisualTemplateDebugger()
    
    print("Visual Template Debugger")
    print("=" * 60)
    print("This will show exactly where everything should be positioned")
    print()
    
    debugger.create_debug_overlay()
    
    print("\nDone! Check debug_template_with_markers.pdf to see exact positions")
    print("Use the coordinates shown to update the exact_template_filler.py")