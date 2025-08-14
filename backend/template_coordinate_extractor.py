"""
Template Coordinate Extractor
Extracts precise coordinates from your original Sendora JO templates
"""

import fitz  # PyMuPDF
import pdfplumber
import json
import os
from typing import Dict, List, Tuple

class TemplateCoordinateExtractor:
    """Extract exact coordinates from original Sendora templates"""
    
    def __init__(self):
        self.template_paths = {
            'door': r'C:\Users\USER\Desktop\Project management\Sendora\Material\JOB ORDER FORM -DOOR.pdf',
            'frame': r'C:\Users\USER\Desktop\Project management\Sendora\Material\JOB ORDER FORM  - FRAME.pdf',
            'combined': r'C:\Users\USER\Desktop\Project management\Sendora\Material\JOB ORDER FORM.pdf'
        }
        
    def extract_all_templates(self):
        """Extract coordinates from all templates"""
        
        results = {}
        
        for template_name, template_path in self.template_paths.items():
            if os.path.exists(template_path):
                print(f"\nAnalyzing {template_name} template...")
                coords = self.extract_template_coordinates(template_path)
                results[template_name] = coords
                
                # Save individual spec file
                spec_file = f"{template_name}_template_spec.json"
                with open(spec_file, 'w', encoding='utf-8') as f:
                    json.dump(coords, f, indent=2, ensure_ascii=False)
                print(f"Saved: {spec_file}")
            else:
                print(f"Template not found: {template_path}")
        
        return results
    
    def extract_template_coordinates(self, pdf_path: str) -> Dict:
        """Extract precise coordinates from template PDF"""
        
        coordinates = {
            'template_path': pdf_path,
            'page_size': None,
            'header_fields': {},
            'text_elements': {},
            'form_fields': {},
            'table_structure': {},
            'checkbox_groups': {},
            'signature_areas': {}
        }
        
        # Use PyMuPDF for precise extraction
        doc = fitz.open(pdf_path)
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # Get page size
            if coordinates['page_size'] is None:
                rect = page.rect
                coordinates['page_size'] = [rect.width, rect.height]
            
            # Extract text with exact positions
            text_dict = page.get_text("dict")
            self.parse_text_blocks(text_dict, coordinates, page_num)
            
            # Extract form fields
            if page.first_widget:
                self.extract_form_fields(page, coordinates, page_num)
        
        doc.close()
        
        # Use pdfplumber for additional analysis
        self.analyze_with_pdfplumber(pdf_path, coordinates)
        
        return coordinates
    
    def parse_text_blocks(self, text_dict: Dict, coordinates: Dict, page_num: int):
        """Parse text blocks and identify field positions"""
        
        page_key = f"page_{page_num}"
        if page_key not in coordinates['text_elements']:
            coordinates['text_elements'][page_key] = {}
        
        for block in text_dict.get('blocks', []):
            if 'lines' not in block:
                continue
                
            for line in block['lines']:
                for span in line['spans']:
                    text = span['text'].strip()
                    if not text:
                        continue
                    
                    # Identify field labels and positions
                    field_info = {
                        'text': text,
                        'x': span['bbox'][0],
                        'y': span['bbox'][1],
                        'width': span['bbox'][2] - span['bbox'][0],
                        'height': span['bbox'][3] - span['bbox'][1],
                        'font': span['font'],
                        'size': span['size'],
                        'flags': span['flags']
                    }
                    
                    # Categorize based on content
                    if self.is_field_label(text):
                        field_name = self.normalize_field_name(text)
                        coordinates['header_fields'][field_name] = field_info
                    elif self.is_checkbox_option(text):
                        self.add_checkbox_option(text, field_info, coordinates)
                    else:
                        coordinates['text_elements'][page_key][text] = field_info
    
    def extract_form_fields(self, page, coordinates: Dict, page_num: int):
        """Extract interactive form fields"""
        
        widget = page.first_widget
        while widget:
            field_info = {
                'field_name': widget.field_name or 'unnamed',
                'field_type': widget.field_type_string,
                'rect': list(widget.rect),
                'x': widget.rect.x0,
                'y': widget.rect.y0,
                'width': widget.rect.width,
                'height': widget.rect.height
            }
            
            coordinates['form_fields'][f"field_{len(coordinates['form_fields'])}"] = field_info
            widget = widget.next
    
    def analyze_with_pdfplumber(self, pdf_path: str, coordinates: Dict):
        """Use pdfplumber for table and structure analysis"""
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    # Find tables
                    tables = page.find_tables()
                    if tables:
                        coordinates['table_structure'][f"page_{page_num}"] = []
                        for i, table in enumerate(tables):
                            table_info = {
                                'table_id': i,
                                'bbox': table.bbox,
                                'rows': len(table.rows) if table.rows else 0,
                                'columns': len(table.rows[0]) if table.rows and table.rows[0] else 0
                            }
                            coordinates['table_structure'][f"page_{page_num}"].append(table_info)
                    
                    # Extract lines for form structure
                    lines = page.lines
                    if lines:
                        coordinates[f"lines_page_{page_num}"] = [
                            {
                                'x0': line['x0'],
                                'y0': line['y0'], 
                                'x1': line['x1'],
                                'y1': line['y1'],
                                'width': line.get('width', 1)
                            } for line in lines
                        ]
        except Exception as e:
            print(f"pdfplumber analysis failed: {e}")
    
    def is_field_label(self, text: str) -> bool:
        """Check if text is a field label"""
        field_labels = [
            'job order no', 'job order date', 'po no', 'delivery date',
            'customer name', 'measure by', 'laminate code', 'door thickness',
            'door size', 'door type', 'door core', 'edging', 'decorative line',
            'design name', 'open hole type', 'drawing', 'remark',
            'frame width', 'rebated', 'frame size', 'inner or outer',
            'frame profile', 'frame laminate code'
        ]
        return any(label in text.lower() for label in field_labels)
    
    def is_checkbox_option(self, text: str) -> bool:
        """Check if text is a checkbox option"""
        checkbox_options = [
            '37mm', '43mm', '48mm', 's/l', 'd/l', 'unequal d/l',
            'honeycomb', 'solid tubular core', 'solid timber', 'metal skeleton',
            'na lipping', 'abs edging', 'no edging', 't-bar', 'groove line',
            'inner', 'outer'
        ]
        return text.lower() in checkbox_options
    
    def add_checkbox_option(self, text: str, field_info: Dict, coordinates: Dict):
        """Add checkbox option to appropriate group"""
        
        # Determine checkbox group
        text_lower = text.lower()
        
        if text_lower in ['37mm', '43mm', '48mm']:
            group = 'door_thickness'
        elif text_lower in ['s/l', 'd/l', 'unequal d/l']:
            group = 'door_type'
        elif text_lower in ['honeycomb', 'solid tubular core', 'solid timber', 'metal skeleton']:
            group = 'door_core'
        elif text_lower in ['na lipping', 'abs edging', 'no edging']:
            group = 'edging'
        elif text_lower in ['t-bar', 'groove line']:
            group = 'decorative_line'
        elif text_lower in ['inner', 'outer']:
            group = 'frame_type'
        else:
            group = 'other'
        
        if group not in coordinates['checkbox_groups']:
            coordinates['checkbox_groups'][group] = {}
        
        coordinates['checkbox_groups'][group][text] = field_info
    
    def normalize_field_name(self, text: str) -> str:
        """Normalize field name for consistent mapping"""
        
        text_lower = text.lower().replace(':', '').strip()
        
        mapping = {
            'job order no': 'job_order_no',
            'job order date': 'job_order_date',
            'po no': 'po_no',
            'delivery date': 'delivery_date',
            'customer name': 'customer_name',
            'measure by': 'measure_by'
        }
        
        return mapping.get(text_lower, text_lower.replace(' ', '_'))
    
    def create_overlay_specification(self, coordinates: Dict) -> Dict:
        """Create specification for overlay positioning"""
        
        overlay_spec = {
            'page_size': coordinates['page_size'],
            'fields': {},
            'checkboxes': {},
            'tables': {}
        }
        
        # Map header fields for data input
        for field_name, field_info in coordinates['header_fields'].items():
            # Position data input slightly to the right of label
            overlay_spec['fields'][field_name] = {
                'x': field_info['x'] + field_info['width'] + 10,
                'y': field_info['y'],
                'font': 'Helvetica',
                'size': min(field_info['size'], 10)
            }
        
        # Map checkbox positions
        for group_name, checkboxes in coordinates['checkbox_groups'].items():
            overlay_spec['checkboxes'][group_name] = []
            for option_text, option_info in checkboxes.items():
                overlay_spec['checkboxes'][group_name].append({
                    'label': option_text,
                    'x': option_info['x'] - 15,  # Position checkbox before text
                    'y': option_info['y'] + option_info['height'] / 2,
                    'size': 8
                })
        
        return overlay_spec
    
    def save_specifications(self, results: Dict):
        """Save all specifications as JSON files"""
        
        for template_name, coordinates in results.items():
            # Save detailed coordinates
            coord_file = f"{template_name}_coordinates.json"
            with open(coord_file, 'w', encoding='utf-8') as f:
                json.dump(coordinates, f, indent=2, ensure_ascii=False)
            
            # Create overlay specification
            overlay_spec = self.create_overlay_specification(coordinates)
            spec_file = f"{template_name}_overlay_spec.json"
            with open(spec_file, 'w', encoding='utf-8') as f:
                json.dump(overlay_spec, f, indent=2, ensure_ascii=False)
            
            print(f"Created: {coord_file} and {spec_file}")


# Test and extract coordinates
if __name__ == "__main__":
    extractor = TemplateCoordinateExtractor()
    
    print("Extracting coordinates from Sendora JO templates...")
    print("=" * 60)
    
    results = extractor.extract_all_templates()
    extractor.save_specifications(results)
    
    print("\n" + "=" * 60)
    print("Coordinate extraction complete!")
    print("\nFiles created:")
    for template_name in results.keys():
        print(f"  - {template_name}_coordinates.json")
        print(f"  - {template_name}_overlay_spec.json")
    
    print("\nSummary:")
    for template_name, coords in results.items():
        header_count = len(coords.get('header_fields', {}))
        checkbox_count = sum(len(group) for group in coords.get('checkbox_groups', {}).values())
        print(f"  {template_name}: {header_count} header fields, {checkbox_count} checkboxes")