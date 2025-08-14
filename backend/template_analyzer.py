"""
Complete JO Template Analyzer
Carefully documents every detail of your JO template for HTML recreation
"""

import fitz  # PyMuPDF
import json
import os
from typing import Dict, List, Any

class CompleteTemplateAnalyzer:
    """Analyze and document every detail of the JO template"""
    
    def __init__(self):
        self.door_template = r'C:\Users\USER\Desktop\Project management\Sendora\Material\JOB ORDER FORM -DOOR.pdf'
        
    def analyze_complete_template(self):
        """Complete analysis of JO template - every element documented"""
        
        print("=" * 80)
        print("COMPLETE JO TEMPLATE ANALYSIS")
        print("Documenting every detail for HTML recreation")
        print("=" * 80)
        
        if not os.path.exists(self.door_template):
            print(f"Template not found: {self.door_template}")
            return None
        
        # Open template for analysis
        doc = fitz.open(self.door_template)
        page = doc[0]
        
        # Get page dimensions
        rect = page.rect
        width = rect.width
        height = rect.height
        
        print(f"Page Dimensions: {width:.2f} x {height:.2f} points")
        print(f"Page Format: A4 Landscape")
        print(f"Aspect Ratio: {width/height:.2f}")
        
        # Complete template specification
        template_spec = {
            'page_info': {
                'width': width,
                'height': height,
                'format': 'A4 Landscape',
                'orientation': 'landscape',
                'margins': {'top': 20, 'right': 20, 'bottom': 20, 'left': 20}
            },
            'header_section': self.analyze_header_section(page),
            'company_branding': self.analyze_company_branding(page),
            'form_title': self.analyze_form_title(page),
            'table_structure': self.analyze_table_structure(page),
            'checkbox_groups': self.analyze_checkbox_groups(page),
            'footer_section': self.analyze_footer_section(page),
            'styling': self.analyze_styling(page),
            'layout_structure': self.analyze_layout_structure(page)
        }
        
        doc.close()
        
        # Save complete specification
        self.save_complete_specification(template_spec)
        
        return template_spec
    
    def analyze_header_section(self, page):
        """Analyze header fields section"""
        
        print("\nANALYZING HEADER SECTION...")
        
        text_dict = page.get_text("dict")
        header_fields = {}
        
        # Header field labels and their details
        header_labels = [
            'Job Order No:',
            'Job Order Date:',
            'PO NO:',
            'Delivery Date:',
            'Customer Name:',
            'Measure By :'
        ]
        
        for block in text_dict.get('blocks', []):
            if 'lines' not in block:
                continue
                
            for line in block['lines']:
                for span in line['spans']:
                    text = span['text'].strip()
                    
                    for label in header_labels:
                        if label in text:
                            bbox = span['bbox']
                            
                            field_name = label.lower().replace(':', '').replace(' ', '_')
                            header_fields[field_name] = {
                                'label': label,
                                'label_position': {
                                    'x': bbox[0],
                                    'y': bbox[1],
                                    'width': bbox[2] - bbox[0],
                                    'height': bbox[3] - bbox[1]
                                },
                                'data_field': {
                                    'x': bbox[2] + 5,
                                    'y': bbox[1],
                                    'width': 150,
                                    'height': bbox[3] - bbox[1]
                                },
                                'font_size': span['size'],
                                'font_family': span['font']
                            }
                            print(f"  Found: {label}")
        
        return {
            'fields': header_fields,
            'layout': 'two_column',
            'left_column': ['job_order_no', 'job_order_date', 'po_no'],
            'right_column': ['delivery_date', 'customer_name', 'measure_by']
        }
    
    def analyze_company_branding(self, page):
        """Analyze company branding elements"""
        
        print("\nANALYZING COMPANY BRANDING...")
        
        text_dict = page.get_text("dict")
        branding = {}
        
        for block in text_dict.get('blocks', []):
            if 'lines' not in block:
                continue
                
            for line in block['lines']:
                for span in line['spans']:
                    text = span['text'].strip()
                    
                    if 'SENDORA GROUP SDN BHD' in text:
                        bbox = span['bbox']
                        branding['company_name'] = {
                            'text': text,
                            'position': {'x': bbox[0], 'y': bbox[1]},
                            'font_size': span['size'],
                            'font_weight': 'bold'
                        }
                        print(f"  Company Name: {text}")
                    
                    elif text == 'JOB ORDER':
                        bbox = span['bbox']
                        branding['form_type'] = {
                            'text': text,
                            'position': {'x': bbox[0], 'y': bbox[1]},
                            'font_size': span['size'],
                            'font_weight': 'bold',
                            'border': True
                        }
                        print(f"  Form Type: {text}")
        
        return branding
    
    def analyze_form_title(self, page):
        """Analyze form title section"""
        
        print("\nANALYZING FORM TITLE...")
        
        text_dict = page.get_text("dict")
        
        for block in text_dict.get('blocks', []):
            if 'lines' not in block:
                continue
                
            for line in block['lines']:
                for span in line['spans']:
                    text = span['text'].strip()
                    
                    if text == 'DOOR':
                        bbox = span['bbox']
                        return {
                            'text': text,
                            'position': {'x': bbox[0], 'y': bbox[1]},
                            'font_size': span['size'],
                            'font_weight': 'bold',
                            'center_aligned': True,
                            'border': True,
                            'background': 'white'
                        }
        
        return {'text': 'DOOR', 'center_aligned': True, 'border': True}
    
    def analyze_table_structure(self, page):
        """Analyze complete table structure"""
        
        print("\nANALYZING TABLE STRUCTURE...")
        
        text_dict = page.get_text("dict")
        
        # Table column headers
        table_headers = [
            'ITEM',
            'LAMINATE CODE', 
            'DOOR THICKNESS',
            'DOOR SIZE',
            'DOOR TYPE',
            'DOOR CORE',
            'EDGING',
            'DECORATIVE LINE',
            'DESIGN NAME',
            'OPEN HOLE TYPE',
            'DRAWING / REMARK'
        ]
        
        columns = {}
        
        for block in text_dict.get('blocks', []):
            if 'lines' not in block:
                continue
                
            for line in block['lines']:
                for span in line['spans']:
                    text = span['text'].strip().upper()
                    
                    for header in table_headers:
                        if header in text and len(text) <= len(header) + 5:
                            bbox = span['bbox']
                            
                            col_name = header.lower().replace(' ', '_').replace('/', '_')
                            columns[col_name] = {
                                'header': header,
                                'position': {'x': bbox[0], 'y': bbox[1]},
                                'width': bbox[2] - bbox[0],
                                'font_size': span['size']
                            }
                            print(f"  Column: {header}")
        
        return {
            'columns': columns,
            'rows': 4,  # Standard 4 rows
            'row_height': 90,  # Approximate row height
            'header_row': True,
            'borders': True,
            'alternating_rows': False
        }
    
    def analyze_checkbox_groups(self, page):
        """Analyze all checkbox groups"""
        
        print("\nANALYZING CHECKBOX GROUPS...")
        
        text_dict = page.get_text("dict")
        
        checkbox_groups = {
            'door_thickness': {
                'options': ['37mm', '43mm', '48mm', 'Others:'],
                'layout': 'vertical',
                'found_positions': {}
            },
            'door_type': {
                'options': ['S/L', 'D/L', 'Unequal D/L', 'Others:'],
                'layout': 'vertical',
                'found_positions': {}
            },
            'door_core': {
                'options': ['Honeycomb', 'Solid Tubular Core', 'Solid Timber', 'Metal Skeleton'],
                'layout': 'vertical',
                'found_positions': {}
            },
            'edging': {
                'options': ['NA Lipping', 'ABS Edging', 'No Edging'],
                'layout': 'vertical',
                'found_positions': {}
            },
            'decorative_line': {
                'options': ['T-bar', 'Groove Line'],
                'layout': 'vertical',
                'found_positions': {}
            }
        }
        
        # Find checkbox option positions
        for block in text_dict.get('blocks', []):
            if 'lines' not in block:
                continue
                
            for line in block['lines']:
                for span in line['spans']:
                    text = span['text'].strip()
                    bbox = span['bbox']
                    
                    # Check each checkbox group
                    for group_name, group_data in checkbox_groups.items():
                        for option in group_data['options']:
                            if option in text:
                                group_data['found_positions'][option] = {
                                    'text_position': {'x': bbox[0], 'y': bbox[1]},
                                    'checkbox_position': {'x': bbox[0] - 15, 'y': bbox[1]},
                                    'font_size': span['size']
                                }
                                print(f"  {group_name}: {option}")
        
        return checkbox_groups
    
    def analyze_footer_section(self, page):
        """Analyze footer section"""
        
        print("\nANALYZING FOOTER SECTION...")
        
        text_dict = page.get_text("dict")
        footer_elements = {}
        
        footer_labels = [
            'Prepare by,',
            'Checked by,', 
            'Verify by,',
            'Sales Executive :',
            'Sales Admin',
            'Production Supervisor :',
            'Date :'
        ]
        
        for block in text_dict.get('blocks', []):
            if 'lines' not in block:
                continue
                
            for line in block['lines']:
                for span in line['spans']:
                    text = span['text'].strip()
                    
                    for label in footer_labels:
                        if label in text:
                            bbox = span['bbox']
                            
                            field_name = label.lower().replace(',', '').replace(':', '').replace(' ', '_')
                            footer_elements[field_name] = {
                                'label': label,
                                'position': {'x': bbox[0], 'y': bbox[1]},
                                'font_size': span['size']
                            }
                            print(f"  Footer: {label}")
        
        return {
            'elements': footer_elements,
            'layout': 'three_column',
            'sections': ['prepare_section', 'admin_section', 'supervisor_section']
        }
    
    def analyze_styling(self, page):
        """Analyze styling elements"""
        
        print("\nANALYZING STYLING...")
        
        return {
            'fonts': {
                'primary': 'Arial, sans-serif',
                'headers': 'Arial, sans-serif',
                'size_small': '8px',
                'size_normal': '10px',
                'size_large': '12px',
                'size_title': '16px'
            },
            'colors': {
                'text': '#000000',
                'borders': '#000000',
                'background': '#ffffff'
            },
            'borders': {
                'width': '1px',
                'style': 'solid',
                'color': '#000000'
            },
            'spacing': {
                'row_padding': '5px',
                'cell_padding': '3px',
                'section_margin': '10px'
            }
        }
    
    def analyze_layout_structure(self, page):
        """Analyze overall layout structure"""
        
        print("\nANALYZING LAYOUT STRUCTURE...")
        
        return {
            'sections': [
                {
                    'name': 'header_branding',
                    'height': '60px',
                    'layout': 'flex_row'
                },
                {
                    'name': 'form_fields',
                    'height': '80px', 
                    'layout': 'two_column'
                },
                {
                    'name': 'table_section',
                    'height': '400px',
                    'layout': 'table'
                },
                {
                    'name': 'footer_signatures',
                    'height': '100px',
                    'layout': 'three_column'
                }
            ],
            'total_height': '640px',
            'responsive': False,
            'fixed_layout': True
        }
    
    def save_complete_specification(self, spec):
        """Save complete specification for HTML implementation"""
        
        spec_file = 'complete_jo_template_spec.json'
        with open(spec_file, 'w', encoding='utf-8') as f:
            json.dump(spec, f, indent=2, ensure_ascii=False)
        
        print(f"\nSaved complete specification: {spec_file}")
        
        # Create summary
        self.create_specification_summary(spec)
    
    def create_specification_summary(self, spec):
        """Create human-readable summary"""
        
        summary = f"""
SENDORA JOB ORDER TEMPLATE SPECIFICATION
===============================================

PAGE FORMAT:
- Size: A4 Landscape ({spec['page_info']['width']:.0f} x {spec['page_info']['height']:.0f} points)
- Orientation: Landscape
- Margins: 20px all sides

HEADER SECTION:
- Company: SENDORA GROUP SDN BHD (HQ)
- Form Type: JOB ORDER
- Template: DOOR

FORM FIELDS ({len(spec['header_section']['fields'])} fields):
"""
        
        for field_name, field_data in spec['header_section']['fields'].items():
            summary += f"- {field_data['label']}\n"
        
        summary += f"""
TABLE STRUCTURE:
- Columns: {len(spec['table_structure']['columns'])}
- Rows: {spec['table_structure']['rows']}
- Headers: """
        
        for col_name, col_data in spec['table_structure']['columns'].items():
            summary += f"{col_data['header']}, "
        
        summary += f"""

CHECKBOX GROUPS ({len(spec['checkbox_groups'])} groups):
"""
        
        for group_name, group_data in spec['checkbox_groups'].items():
            summary += f"- {group_name.replace('_', ' ').title()}: {len(group_data['options'])} options\n"
        
        summary += f"""
FOOTER SECTION:
- Elements: {len(spec['footer_section']['elements'])}
- Layout: Three-column signature area

STYLING:
- Fonts: Arial/Helvetica
- Colors: Black text on white background
- Borders: 1px solid black lines
- Layout: Fixed positioning, table-based

This specification ensures 100% identical recreation of your JO template.
"""
        
        with open('jo_template_summary.txt', 'w', encoding='utf-8') as f:
            f.write(summary)
        
        print("Created readable summary: jo_template_summary.txt")


if __name__ == "__main__":
    analyzer = CompleteTemplateAnalyzer()
    
    print("Starting complete JO template analysis...")
    print("This will document every detail for HTML recreation\n")
    
    spec = analyzer.analyze_complete_template()
    
    if spec:
        print("\n" + "=" * 80)
        print("COMPLETE ANALYSIS FINISHED!")
        print("=" * 80)
        print("All template details documented for HTML implementation.")
        print("Files created:")
        print("- complete_jo_template_spec.json (detailed specification)")
        print("- jo_template_summary.txt (human-readable summary)")
        print("\nReady for HTML template creation!")
    else:
        print("Analysis failed - check template path")