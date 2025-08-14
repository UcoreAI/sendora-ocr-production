"""
Smart Form Filler - Hybrid Approach
Creates fillable-like experience without needing Adobe Acrobat
"""

import fitz  # PyMuPDF
import json
import os
from typing import Dict, Any
from datetime import datetime

class SmartFormFiller:
    """Smart form filling that combines template analysis with precise positioning"""
    
    def __init__(self):
        self.template_paths = {
            'door': r'C:\Users\USER\Desktop\Project management\Sendora\Material\JOB ORDER FORM -DOOR.pdf',
            'frame': r'C:\Users\USER\Desktop\Project management\Sendora\Material\JOB ORDER FORM  - FRAME.pdf',
            'combined': r'C:\Users\USER\Desktop\Project management\Sendora\Material\JOB ORDER FORM.pdf'
        }
        
        # Create smart form specifications based on actual template analysis
        self.create_smart_form_specs()
    
    def create_smart_form_specs(self):
        """Create smart form specifications by analyzing actual template layout"""
        
        print("Creating smart form specifications...")
        
        # Analyze door template to get exact dimensions and positioning
        door_template = self.template_paths['door']
        if os.path.exists(door_template):
            doc = fitz.open(door_template)
            page = doc[0]
            
            # Get actual page dimensions
            rect = page.rect
            page_width = rect.width   # Should be around 842 points (landscape A4)
            page_height = rect.height # Should be around 595 points
            
            print(f"Template dimensions: {page_width} x {page_height}")
            
            # Smart positioning based on actual template analysis
            # These coordinates are measured from the real template structure
            
            smart_spec = {
                'page_size': [page_width, page_height],
                'form_fields': {
                    # Header fields - fine-tuned for perfect alignment
                    'job_order_no': {
                        'x': 140, 'y': 71, 'width': 150, 'height': 20,
                        'font': 'Helvetica', 'size': 10, 'align': 'left'
                    },
                    'job_order_date': {
                        'x': 145, 'y': 91, 'width': 150, 'height': 20,
                        'font': 'Helvetica', 'size': 10, 'align': 'left'
                    },
                    'customer_name': {
                        'x': 750, 'y': 91, 'width': 200, 'height': 20,
                        'font': 'Helvetica', 'size': 10, 'align': 'left'
                    },
                    'po_no': {
                        'x': 100, 'y': 111, 'width': 150, 'height': 20,
                        'font': 'Helvetica', 'size': 10, 'align': 'left'
                    },
                    'delivery_date': {
                        'x': 750, 'y': 71, 'width': 100, 'height': 20,
                        'font': 'Helvetica', 'size': 10, 'align': 'left'
                    },
                    'measure_by': {
                        'x': 700, 'y': 111, 'width': 150, 'height': 20,
                        'font': 'Helvetica', 'size': 10, 'align': 'left'
                    },
                },
                
                # Table row specifications
                'table_rows': [
                    {
                        'row': 1, 'y': 195,
                        'item_x': 40, 'laminate_x': 75, 'thickness_x': 155,
                        'size_x': 240, 'type_x': 340, 'core_x': 390,
                        'edging_x': 470, 'decorative_x': 520, 'design_x': 580,
                        'hole_x': 640, 'remark_x': 700
                    },
                    {
                        'row': 2, 'y': 295,
                        'item_x': 40, 'laminate_x': 75, 'thickness_x': 155,
                        'size_x': 240, 'type_x': 340, 'core_x': 390,
                        'edging_x': 470, 'decorative_x': 520, 'design_x': 580,
                        'hole_x': 640, 'remark_x': 700
                    },
                    {
                        'row': 3, 'y': 395,
                        'item_x': 40, 'laminate_x': 75, 'thickness_x': 155,
                        'size_x': 240, 'type_x': 340, 'core_x': 390,
                        'edging_x': 470, 'decorative_x': 520, 'design_x': 580,
                        'hole_x': 640, 'remark_x': 700
                    },
                    {
                        'row': 4, 'y': 495,
                        'item_x': 40, 'laminate_x': 75, 'thickness_x': 155,
                        'size_x': 240, 'type_x': 340, 'core_x': 390,
                        'edging_x': 470, 'decorative_x': 520, 'design_x': 580,
                        'hole_x': 640, 'remark_x': 700
                    }
                ],
                
                # Checkbox specifications with exact positions
                'checkboxes': {
                    'door_thickness': [
                        {'option': '37mm', 'x': 143, 'y': 207, 'size': 8},
                        {'option': '43mm', 'x': 143, 'y': 225, 'size': 8},
                        {'option': '48mm', 'x': 143, 'y': 242, 'size': 8},
                        {'option': 'Others', 'x': 143, 'y': 260, 'size': 8}
                    ],
                    'door_type': [
                        {'option': 'S/L', 'x': 343, 'y': 207, 'size': 8},
                        {'option': 'D/L', 'x': 343, 'y': 225, 'size': 8},
                        {'option': 'Unequal D/L', 'x': 343, 'y': 242, 'size': 8},
                        {'option': 'Others', 'x': 343, 'y': 260, 'size': 8}
                    ],
                    'door_core': [
                        {'option': 'Honeycomb', 'x': 393, 'y': 207, 'size': 8},
                        {'option': 'Solid Tubular Core', 'x': 393, 'y': 225, 'size': 8},
                        {'option': 'Solid Timber', 'x': 393, 'y': 242, 'size': 8},
                        {'option': 'Metal Skeleton', 'x': 393, 'y': 260, 'size': 8}
                    ],
                    'edging': [
                        {'option': 'NA Lipping', 'x': 473, 'y': 207, 'size': 8},
                        {'option': 'ABS Edging', 'x': 473, 'y': 225, 'size': 8},
                        {'option': 'No Edging', 'x': 473, 'y': 242, 'size': 8}
                    ],
                    'decorative_line': [
                        {'option': 'T-bar', 'x': 523, 'y': 207, 'size': 8},
                        {'option': 'Groove Line', 'x': 523, 'y': 225, 'size': 8}
                    ]
                },
                
                # Footer fields
                'footer_fields': {
                    'prepare_by': {'x': 60, 'y': 545, 'width': 120, 'height': 15},
                    'checked_by': {'x': 350, 'y': 545, 'width': 120, 'height': 15},
                    'verify_by': {'x': 650, 'y': 545, 'width': 120, 'height': 15}
                }
            }
            
            # Save smart specification
            smart_spec_file = 'smart_door_form_spec.json'
            with open(smart_spec_file, 'w', encoding='utf-8') as f:
                json.dump(smart_spec, f, indent=2, ensure_ascii=False)
            
            print(f"Smart form specification created: {smart_spec_file}")
            
            doc.close()
            return smart_spec
        
        return None
    
    def fill_smart_form(self, template_path: str, data: Dict[str, Any], output_path: str) -> bool:
        """Fill form using smart positioning - no Adobe Acrobat needed"""
        
        try:
            # Load smart specification
            spec_file = 'smart_door_form_spec.json'
            if not os.path.exists(spec_file):
                print("Smart form specification not found")
                return False
            
            with open(spec_file, 'r', encoding='utf-8') as f:
                spec = json.load(f)
            
            # Open original template
            original_doc = fitz.open(template_path)
            output_doc = fitz.open()
            
            for page_num in range(len(original_doc)):
                original_page = original_doc[page_num]
                output_page = output_doc.new_page(
                    width=original_page.rect.width, 
                    height=original_page.rect.height
                )
                
                # Copy original template
                output_page.show_pdf_page(original_page.rect, original_doc, page_num)
                
                # Add form field data
                self.add_smart_form_data(output_page, spec, data)
            
            # Save result
            output_doc.save(output_path)
            output_doc.close()
            original_doc.close()
            
            print(f"Smart form filled successfully: {output_path}")
            return True
            
        except Exception as e:
            print(f"Error filling smart form: {e}")
            return False
    
    def add_smart_form_data(self, page, spec: Dict, data: Dict[str, Any]):
        """Add data to form using smart positioning"""
        
        page_height = page.rect.height
        
        # Fill header fields
        for field_name, field_spec in spec['form_fields'].items():
            value = self.get_field_value(field_name, data)
            if value:
                x = field_spec['x']
                y = page_height - field_spec['y']  # Convert to PDF coordinates
                font_size = field_spec['size']
                
                # Add text with proper formatting
                page.insert_text(
                    (x, y), str(value),
                    fontsize=font_size,
                    fontname='helvetica',
                    color=(0, 0, 0)
                )
        
        # Fill table rows
        line_items = self.extract_line_items(data)
        for i, item in enumerate(line_items[:len(spec['table_rows'])]):
            if i < len(spec['table_rows']):
                row_spec = spec['table_rows'][i]
                y = page_height - row_spec['y']
                
                # Item number
                page.insert_text(
                    (row_spec['item_x'], y), str(i + 1),
                    fontsize=9, fontname='helvetica', color=(0, 0, 0)
                )
                
                # Laminate code
                if item['laminate_code']:
                    page.insert_text(
                        (row_spec['laminate_x'], y), item['laminate_code'],
                        fontsize=8, fontname='helvetica', color=(0, 0, 0)
                    )
                
                # Door size
                if item['size']:
                    page.insert_text(
                        (row_spec['size_x'], y), item['size'],
                        fontsize=8, fontname='helvetica', color=(0, 0, 0)
                    )
                
                # Location
                location_y = y + 15
                page.insert_text(
                    (row_spec['laminate_x'], location_y), f"Location: {i+1}",
                    fontsize=7, fontname='helvetica', color=(0, 0, 0)
                )
        
        # Fill checkboxes
        self.fill_smart_checkboxes(page, spec, data, page_height)
        
        # Fill footer
        for field_name, field_spec in spec['footer_fields'].items():
            value = self.get_footer_value(field_name, data)
            if value:
                x = field_spec['x']
                y = page_height - field_spec['y']
                
                page.insert_text(
                    (x, y), str(value),
                    fontsize=9, fontname='helvetica', color=(0, 0, 0)
                )
    
    def fill_smart_checkboxes(self, page, spec: Dict, data: Dict[str, Any], page_height: float):
        """Fill checkboxes with smart positioning"""
        
        checkbox_groups = {
            'door_thickness': data.get('door_thickness', ''),
            'door_type': data.get('door_type', ''),
            'door_core': data.get('door_core', ''),
            'edging': data.get('door_edging', ''),
            'decorative_line': data.get('decorative_line', '')
        }
        
        for group_name, selected_value in checkbox_groups.items():
            if group_name in spec['checkboxes']:
                for checkbox_spec in spec['checkboxes'][group_name]:
                    if self.is_checkbox_selected(checkbox_spec['option'], selected_value):
                        x = checkbox_spec['x']
                        y = page_height - checkbox_spec['y']
                        size = checkbox_spec['size']
                        
                        # Draw X mark
                        self.draw_checkbox_mark(page, x, y, size)
    
    def draw_checkbox_mark(self, page, x: float, y: float, size: float):
        """Draw X mark in checkbox"""
        mark_size = size * 0.8
        page.draw_line((x, y), (x + mark_size, y + mark_size), width=1.5, color=(0, 0, 0))
        page.draw_line((x + mark_size, y), (x, y + mark_size), width=1.5, color=(0, 0, 0))
    
    def is_checkbox_selected(self, option: str, selected_value: str) -> bool:
        """Check if checkbox should be selected"""
        if not selected_value:
            return False
        
        option_lower = option.lower().replace(' ', '').replace('_', '')
        value_lower = selected_value.lower().replace(' ', '').replace('_', '')
        
        # Direct match or partial match
        return option_lower in value_lower or value_lower in option_lower
    
    def extract_line_items(self, data: Dict[str, Any]) -> list:
        """Extract line items from data"""
        line_items = []
        for i in range(10):
            desc_key = f'item_desc_{i}'
            if desc_key in data and data[desc_key]:
                item = {
                    'description': data[desc_key],
                    'size': data.get(f'item_size_{i}', ''),
                    'quantity': data.get(f'item_qty_{i}', '1'),
                    'laminate_code': self.extract_laminate_code(data[desc_key])
                }
                line_items.append(item)
        return line_items
    
    def extract_laminate_code(self, description: str) -> str:
        """Extract laminate code from description"""
        import re
        pattern = r'([0-9]+[A-Z]-[A-Z0-9]+)'
        match = re.search(pattern, description)
        return match.group(1) if match else ""
    
    def get_field_value(self, field_name: str, data: Dict[str, Any]) -> str:
        """Get value for field"""
        mapping = {
            'job_order_no': data.get('invoice_number', ''),
            'job_order_date': data.get('document_date', ''),
            'customer_name': data.get('customer_name', ''),
            'po_no': data.get('po_number', ''),
            'delivery_date': data.get('delivery_date', ''),
            'measure_by': 'Auto Generated'
        }
        return mapping.get(field_name, '')
    
    def get_footer_value(self, field_name: str, data: Dict[str, Any]) -> str:
        """Get footer field value"""
        mapping = {
            'prepare_by': data.get('invoice_number', ''),
            'checked_by': data.get('document_date', ''),
            'verify_by': data.get('customer_name', '')
        }
        return mapping.get(field_name, '')
    
    def generate_smart_jo(self, validated_data: Dict[str, Any], template_type: str = 'door') -> str:
        """Generate JO using smart form filling"""
        
        template_path = self.template_paths[template_type]
        
        # Generate output filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_filename = f"JO_SMART_{template_type.upper()}_{timestamp}.pdf"
        output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'job_orders', output_filename)
        
        if self.fill_smart_form(template_path, validated_data, output_path):
            return output_path
        else:
            return None


# Test the smart form filler
if __name__ == "__main__":
    filler = SmartFormFiller()
    
    print("Smart Form Filler - No Adobe Acrobat Required!")
    print("=" * 60)
    
    # Test with sample data
    sample_data = {
        'invoice_number': 'KDI-2507-003',
        'customer_name': 'SENDORA GROUP SDN BHD',
        'document_date': '2025-08-13',
        'delivery_date': '2025-08-20',
        'po_number': 'PO-2025-001',
        'door_thickness': '43mm',
        'door_type': 'S/L',
        'door_core': 'solid tubular core',
        'door_edging': 'na lipping',
        'decorative_line': 't-bar',
        'item_desc_0': '6S-A057 DOOR 43MM x 850MM x 2100MM',
        'item_size_0': '850MM x 2100MM',
        'item_qty_0': '2',
        'item_type_0': 'door'
    }
    
    print("Generating smart JO with precise positioning...")
    result = filler.generate_smart_jo(sample_data, 'door')
    
    if result:
        print(f"SUCCESS! Generated: {result}")
        print("Smart form filling complete - positioning should be accurate!")
    else:
        print("FAILED: Check template and specifications")