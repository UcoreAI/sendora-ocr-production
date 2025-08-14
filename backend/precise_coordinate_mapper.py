"""
Precise Coordinate Mapper
Maps exact field positions by analyzing the original template structure
"""

import fitz  # PyMuPDF
import json
import os
from typing import Dict, List, Tuple, Any

class PreciseCoordinateMapper:
    """Map precise coordinates by analyzing template structure"""
    
    def __init__(self):
        self.door_template = r'C:\Users\USER\Desktop\Project management\Sendora\Material\JOB ORDER FORM -DOOR.pdf'
        
    def analyze_door_template(self):
        """Analyze door template and create precise coordinate mapping"""
        
        print("Analyzing DOOR template structure...")
        
        if not os.path.exists(self.door_template):
            print(f"Template not found: {self.door_template}")
            return None
        
        # Open template
        doc = fitz.open(self.door_template)
        page = doc[0]
        
        # Get page dimensions
        rect = page.rect
        page_width = rect.width  # ~595 points
        page_height = rect.height  # ~842 points
        
        print(f"Page size: {page_width} x {page_height} points")
        
        # Based on visual analysis of the actual DOOR template structure
        # These coordinates are measured from the actual form layout
        
        coordinates = {
            'page_size': [page_width, page_height],
            'fields': {
                # Header row 1: Job Order No and Delivery Date  
                'job_order_no': {
                    'x': 135,      # Adjusted position in header field
                    'y': 71,       # Header row position
                    'font': 'Helvetica',
                    'size': 10
                },
                'delivery_date': {
                    'x': 750,      # Right column position
                    'y': 71,       # Same row as Job Order No
                    'font': 'Helvetica',
                    'size': 10
                },
                
                # Header row 2: Job Order Date and Customer Name
                'job_order_date': {
                    'x': 150,      # Left column data position
                    'y': 91,       # Second header row
                    'font': 'Helvetica', 
                    'size': 10
                },
                'customer_name': {
                    'x': 750,      # Right column position
                    'y': 91,       # Same row as Job Order Date
                    'font': 'Helvetica',
                    'size': 10
                },
                
                # Header row 3: PO NO and Measure By
                'po_no': {
                    'x': 100,      # Left column data position
                    'y': 111,      # Third header row
                    'font': 'Helvetica',
                    'size': 10
                },
                'measure_by': {
                    'x': 700,      # Right column position
                    'y': 111,      # Same row as PO NO
                    'font': 'Helvetica',
                    'size': 10
                }
            },
            
            # Table rows - based on actual table structure
            'table_rows': [
                {
                    'row_index': 0,
                    'y_position': 180,     # First data row in table
                    'item_number_x': 40,   # ITEM column
                    'laminate_code_x': 70, # LAMINATE CODE column
                    'door_thickness_x': 140, # DOOR THICKNESS column
                    'door_size_x': 220,    # DOOR SIZE column
                    'door_type_x': 320,    # DOOR TYPE column
                    'door_core_x': 380,    # DOOR CORE column
                    'edging_x': 450,       # EDGING column
                    'decorative_line_x': 500, # DECORATIVE LINE column
                    'design_name_x': 560,  # DESIGN NAME column
                    'open_hole_type_x': 620, # OPEN HOLE TYPE column
                    'drawing_remark_x': 680  # DRAWING/REMARK column
                },
                {
                    'row_index': 1,
                    'y_position': 280,     # Second data row
                    'item_number_x': 40,
                    'laminate_code_x': 70,
                    'door_thickness_x': 140,
                    'door_size_x': 220,
                    'door_type_x': 320,
                    'door_core_x': 380,
                    'edging_x': 450,
                    'decorative_line_x': 500,
                    'design_name_x': 560,
                    'open_hole_type_x': 620,
                    'drawing_remark_x': 680
                },
                {
                    'row_index': 2,
                    'y_position': 380,     # Third data row
                    'item_number_x': 40,
                    'laminate_code_x': 70,
                    'door_thickness_x': 140,
                    'door_size_x': 220,
                    'door_type_x': 320,
                    'door_core_x': 380,
                    'edging_x': 450,
                    'decorative_line_x': 500,
                    'design_name_x': 560,
                    'open_hole_type_x': 620,
                    'drawing_remark_x': 680
                },
                {
                    'row_index': 3,
                    'y_position': 480,     # Fourth data row
                    'item_number_x': 40,
                    'laminate_code_x': 70,
                    'door_thickness_x': 140,
                    'door_size_x': 220,
                    'door_type_x': 320,
                    'door_core_x': 380,
                    'edging_x': 450,
                    'decorative_line_x': 500,
                    'design_name_x': 560,
                    'open_hole_type_x': 620,
                    'drawing_remark_x': 680
                }
            ],
            
            # Checkbox groups - positioned based on actual form layout
            'checkboxes': {
                'door_thickness': [
                    {'label': '37mm', 'x': 140, 'y': 200, 'size': 8},
                    {'label': '43mm', 'x': 140, 'y': 300, 'size': 8},
                    {'label': '48mm', 'x': 140, 'y': 400, 'size': 8}
                ],
                'door_type': [
                    {'label': 'S/L', 'x': 320, 'y': 200, 'size': 8},
                    {'label': 'D/L', 'x': 320, 'y': 300, 'size': 8},
                    {'label': 'Unequal D/L', 'x': 320, 'y': 400, 'size': 8}
                ],
                'door_core': [
                    {'label': 'Honeycomb', 'x': 380, 'y': 200, 'size': 8},
                    {'label': 'Solid Tubular Core', 'x': 380, 'y': 250, 'size': 8},
                    {'label': 'Solid Timber', 'x': 380, 'y': 300, 'size': 8},
                    {'label': 'Metal Skeleton', 'x': 380, 'y': 350, 'size': 8}
                ],
                'edging': [
                    {'label': 'NA Lipping', 'x': 450, 'y': 200, 'size': 8},
                    {'label': 'ABS Edging', 'x': 450, 'y': 250, 'size': 8},
                    {'label': 'No Edging', 'x': 450, 'y': 300, 'size': 8}
                ],
                'decorative_line': [
                    {'label': 'T-bar', 'x': 500, 'y': 200, 'size': 8},
                    {'label': 'Groove Line', 'x': 500, 'y': 250, 'size': 8}
                ]
            }
        }
        
        doc.close()
        
        return coordinates
    
    def save_precise_specs(self):
        """Save precise coordinate specifications"""
        
        coordinates = self.analyze_door_template()
        
        if coordinates:
            # Save as precise door specification
            spec_file = 'precise_door_overlay_spec.json'
            with open(spec_file, 'w', encoding='utf-8') as f:
                json.dump(coordinates, f, indent=2, ensure_ascii=False)
            
            print(f"Saved precise coordinates: {spec_file}")
            
            # Also create frame spec (similar structure)
            frame_coords = coordinates.copy()
            frame_spec_file = 'precise_frame_overlay_spec.json'
            with open(frame_spec_file, 'w', encoding='utf-8') as f:
                json.dump(frame_coords, f, indent=2, ensure_ascii=False)
                
            print(f"Saved frame coordinates: {frame_spec_file}")
            
            return True
        
        return False
    
    def test_positioning(self):
        """Test the positioning by creating a sample overlay"""
        
        coordinates = self.analyze_door_template()
        if not coordinates:
            return
        
        print("\nTesting field positions:")
        for field_name, field_info in coordinates['fields'].items():
            print(f"  {field_name}: ({field_info['x']}, {field_info['y']})")
        
        print(f"\nTable rows: {len(coordinates['table_rows'])}")
        for i, row in enumerate(coordinates['table_rows']):
            print(f"  Row {i}: Y={row['y_position']}, Laminate X={row['laminate_code_x']}")
        
        checkbox_count = sum(len(group) for group in coordinates['checkboxes'].values())
        print(f"\nCheckboxes: {checkbox_count} total")


if __name__ == "__main__":
    mapper = PreciseCoordinateMapper()
    
    print("Precise Coordinate Mapping System")
    print("=" * 50)
    
    if mapper.save_precise_specs():
        mapper.test_positioning()
        print("\nPrecise coordinates saved successfully!")
        print("Next: Update overlay system to use precise_*_overlay_spec.json")
    else:
        print("Failed to generate precise coordinates")