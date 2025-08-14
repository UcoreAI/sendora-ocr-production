"""
Precise Template Overlay System
Uses extracted coordinates for pixel-perfect positioning
"""

import fitz  # PyMuPDF
import json
import os
from datetime import datetime
from typing import Dict, Any

class PreciseTemplateOverlay:
    """Overlay data on original templates with pixel-perfect positioning"""
    
    def __init__(self):
        self.template_paths = {
            'door': r'C:\Users\USER\Desktop\Project management\Sendora\Material\JOB ORDER FORM -DOOR.pdf',
            'frame': r'C:\Users\USER\Desktop\Project management\Sendora\Material\JOB ORDER FORM  - FRAME.pdf',
            'combined': r'C:\Users\USER\Desktop\Project management\Sendora\Material\JOB ORDER FORM.pdf'
        }
        
        # Load precise coordinates first, then fallback to others
        self.specs = {}
        for template_name in self.template_paths.keys():
            spec_loaded = False
            
            # Try precise coordinates first (highest priority)
            precise_spec_file = os.path.join(os.path.dirname(__file__), f"precise_{template_name}_overlay_spec.json")
            
            if os.path.exists(precise_spec_file):
                with open(precise_spec_file, 'r', encoding='utf-8') as f:
                    self.specs[template_name] = json.load(f)
                print(f"Loaded PRECISE spec: {precise_spec_file}")
                spec_loaded = True
            
            if not spec_loaded:
                # Try AI-learned specs second
                ai_spec_file = os.path.join(os.path.dirname(__file__), f"ai_{template_name}_overlay_spec.json")
                
                if os.path.exists(ai_spec_file):
                    with open(ai_spec_file, 'r', encoding='utf-8') as f:
                        self.specs[template_name] = json.load(f)
                    print(f"Loaded AI-learned spec: {ai_spec_file}")
                    spec_loaded = True
            
            if not spec_loaded:
                # Fallback to extracted specs
                spec_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), f"{template_name}_overlay_spec.json")
                if os.path.exists(spec_file):
                    with open(spec_file, 'r', encoding='utf-8') as f:
                        self.specs[template_name] = json.load(f)
                    print(f"Loaded extracted spec: {spec_file}")
                    spec_loaded = True
            
            if not spec_loaded:
                print(f"No spec file found for {template_name}")
    
    def generate_precise_jo(self, validated_data: Dict[str, Any], template_type: str = 'auto') -> str:
        """Generate JO with precise overlay positioning"""
        
        # Auto-detect template type
        if template_type == 'auto':
            template_type = self.detect_template_type(validated_data)
        
        # Check if we have the template and spec
        if template_type not in self.template_paths:
            raise ValueError(f"Unknown template type: {template_type}")
        
        template_path = self.template_paths[template_type]
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template not found: {template_path}")
        
        if template_type not in self.specs:
            raise ValueError(f"No specification found for template: {template_type}")
        
        # Generate output filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_filename = f"JO_PRECISE_{template_type.upper()}_{timestamp}.pdf"
        output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'job_orders', output_filename)
        
        # Create precise overlay
        self.create_precise_overlay(template_path, self.specs[template_type], validated_data, output_path)
        
        return os.path.abspath(output_path)
    
    def detect_template_type(self, data: Dict[str, Any]) -> str:
        """Auto-detect which template to use"""
        
        # Count door vs frame items
        door_count = 0
        frame_count = 0
        
        for key, value in data.items():
            if key.startswith('item_') and value:
                item_type = data.get(key.replace('desc', 'type'), '').lower()
                if 'door' in item_type or 'door' in value.lower():
                    door_count += 1
                elif 'frame' in item_type or 'frame' in value.lower():
                    frame_count += 1
        
        # Check specifications
        has_door_specs = any(data.get(key) for key in ['door_thickness', 'door_type', 'door_core'])
        has_frame_specs = any(data.get(key) for key in ['frame_type', 'frame_profile'])
        
        # Determine template
        if has_door_specs and has_frame_specs:
            return 'combined'
        elif frame_count > door_count or has_frame_specs:
            return 'frame'
        else:
            return 'door'
    
    def create_precise_overlay(self, template_path: str, spec: Dict, data: Dict[str, Any], output_path: str):
        """Create PDF with precise data overlay"""
        
        # Open original template
        original_doc = fitz.open(template_path)
        
        # Create new document for output
        output_doc = fitz.open()
        
        for page_num in range(len(original_doc)):
            # Copy original page
            original_page = original_doc[page_num]
            
            # Create new page with same dimensions
            output_page = output_doc.new_page(width=original_page.rect.width, height=original_page.rect.height)
            
            # Copy original content
            output_page.show_pdf_page(original_page.rect, original_doc, page_num)
            
            # Add data overlay
            self.add_data_overlay(output_page, spec, data, page_num)
        
        # Save result
        output_doc.save(output_path)
        output_doc.close()
        original_doc.close()
        
        print(f"Precise JO created: {output_path}")
    
    def add_data_overlay(self, page, spec: Dict, data: Dict[str, Any], page_num: int):
        """Add data overlay with precise positioning"""
        
        page_height = page.rect.height
        
        # Add header fields
        for field_name, field_spec in spec.get('fields', {}).items():
            value = self.get_field_value(field_name, data)
            if value:
                # Convert coordinates (PDF coordinates are from bottom-left)
                x = field_spec['x']
                y = page_height - field_spec['y']  # Flip Y coordinate
                font_size = field_spec.get('size', 10)
                
                # Insert text at precise position
                page.insert_text(
                    (x, y),
                    str(value),
                    fontsize=font_size,
                    fontname="helvetica",
                    color=(0, 0, 0)  # Black text
                )
        
        # Add checkboxes
        for group_name, checkbox_list in spec.get('checkboxes', {}).items():
            selected_value = self.get_checkbox_value(group_name, data)
            
            for checkbox_spec in checkbox_list:
                if self.is_checkbox_selected(checkbox_spec['label'], selected_value):
                    # Draw checkbox mark
                    x = checkbox_spec['x']
                    y = page_height - checkbox_spec['y']
                    size = checkbox_spec.get('size', 8)
                    
                    # Draw X mark
                    self.draw_checkbox_mark(page, x, y, size)
        
        # Add line items (if on door/frame template)
        if page_num == 0:  # First page typically has items
            self.add_line_items(page, spec, data, page_height)
    
    def get_field_value(self, field_name: str, data: Dict[str, Any]) -> str:
        """Get value for field from data"""
        
        # Direct mapping
        if field_name in data:
            return str(data[field_name])
        
        # Field name mapping
        field_mappings = {
            'job_order_no': data.get('invoice_number', ''),
            'job_order_date': data.get('document_date', ''),
            'po_no': data.get('po_number', ''),
            'delivery_date': data.get('delivery_date', ''),
            'customer_name': data.get('customer_name', ''),
            'measure_by': 'Auto Generated'
        }
        
        return field_mappings.get(field_name, '')
    
    def get_checkbox_value(self, group_name: str, data: Dict[str, Any]) -> str:
        """Get checkbox value for group"""
        
        # Group name mapping
        group_mappings = {
            'door_thickness': data.get('door_thickness', ''),
            'door_type': data.get('door_type', ''),
            'door_core': data.get('door_core', ''),
            'edging': data.get('door_edging', ''),
            'decorative_line': data.get('decorative_line', ''),
            'frame_type': data.get('frame_type', '')
        }
        
        return group_mappings.get(group_name, '')
    
    def is_checkbox_selected(self, checkbox_label: str, selected_value: str) -> bool:
        """Check if checkbox should be marked"""
        
        if not selected_value:
            return False
        
        # Normalize for comparison
        label_lower = checkbox_label.lower().replace(' ', '').replace('_', '')
        value_lower = selected_value.lower().replace(' ', '').replace('_', '')
        
        # Direct match
        if label_lower == value_lower:
            return True
        
        # Partial match for common variations
        if label_lower in value_lower or value_lower in label_lower:
            return True
        
        # Special cases
        if checkbox_label == '43mm' and ('43' in selected_value):
            return True
        if checkbox_label == 'S/L' and ('single' in selected_value.lower() or 's/l' in selected_value.lower()):
            return True
        if checkbox_label == 'Honeycomb' and 'honeycomb' in selected_value.lower():
            return True
        
        return False
    
    def draw_checkbox_mark(self, page, x: float, y: float, size: float):
        """Draw X mark in checkbox"""
        
        # Create small X mark
        mark_size = size * 0.6
        
        # Draw X lines
        page.draw_line((x, y), (x + mark_size, y + mark_size), width=1, color=(0, 0, 0))
        page.draw_line((x + mark_size, y), (x, y + mark_size), width=1, color=(0, 0, 0))
    
    def add_line_items(self, page, spec: Dict, data: Dict[str, Any], page_height: float):
        """Add line items to precise table positions"""
        
        # Extract line items from data
        line_items = []
        for i in range(10):  # Check up to 10 items
            desc_key = f'item_desc_{i}'
            if desc_key in data and data[desc_key]:
                item = {
                    'description': data[desc_key],
                    'size': data.get(f'item_size_{i}', ''),
                    'quantity': data.get(f'item_qty_{i}', '1'),
                    'type': data.get(f'item_type_{i}', 'door'),
                    'laminate_code': self.extract_laminate_code(data[desc_key])
                }
                line_items.append(item)
        
        # Use precise table row coordinates
        table_rows = spec.get('table_rows', [])
        
        for i, item in enumerate(line_items[:len(table_rows)]):  # Use available table rows
            if i < len(table_rows):
                row = table_rows[i]
                y_pos = page_height - row['y_position']  # Convert PDF coordinates
                
                # Item number
                if 'item_number_x' in row:
                    page.insert_text((row['item_number_x'], y_pos), str(i + 1), 
                                    fontsize=9, fontname="helvetica", color=(0, 0, 0))
                
                # Laminate code
                if 'laminate_code_x' in row and item['laminate_code']:
                    page.insert_text((row['laminate_code_x'], y_pos), item['laminate_code'], 
                                    fontsize=8, fontname="helvetica", color=(0, 0, 0))
                
                # Door size
                if 'door_size_x' in row and item['size']:
                    page.insert_text((row['door_size_x'], y_pos), item['size'], 
                                    fontsize=8, fontname="helvetica", color=(0, 0, 0))
                
                # Location field (if available)
                location_text = f"Location: {i+1}"
                if 'laminate_code_x' in row:
                    location_y = y_pos + 15  # Below the main row
                    page.insert_text((row['laminate_code_x'], location_y), location_text, 
                                    fontsize=7, fontname="helvetica", color=(0, 0, 0))
    
    def extract_laminate_code(self, description: str) -> str:
        """Extract laminate code from item description"""
        import re
        # Look for patterns like "6S-A057" in the description
        pattern = r'([0-9]+[A-Z]-[A-Z0-9]+)'
        match = re.search(pattern, description)
        return match.group(1) if match else ""


# Test function
def test_precise_overlay():
    """Test the precise overlay system"""
    
    overlay = PreciseTemplateOverlay()
    
    # Test data
    test_data = {
        'invoice_number': 'KDI-2507-003',
        'customer_name': 'SENDORA GROUP SDN BHD',
        'document_date': '2025-08-13',
        'delivery_date': '2025-08-20',
        'door_thickness': '43mm',
        'door_type': 'S/L',
        'door_core': 'solid tubular',
        'door_edging': 'na lipping',
        'item_desc_0': '6S-A057 DOOR 43MM x 850MM x 2100MM',
        'item_size_0': '850MM x 2100MM',
        'item_qty_0': '2',
        'item_type_0': 'door'
    }
    
    try:
        output_path = overlay.generate_precise_jo(test_data, 'door')
        print(f"Test successful! Generated: {output_path}")
        return output_path
    except Exception as e:
        print(f"Test failed: {e}")
        return None

if __name__ == "__main__":
    test_precise_overlay()