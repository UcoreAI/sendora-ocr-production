"""
HTML Template Generator for JO Forms
Creates pixel-perfect HTML recreation of your JO templates
Preserves exact layout, styling, and positioning for PDF generation
"""

import json
import os
from typing import Dict, Any
from datetime import datetime

class HTMLTemplateGenerator:
    """Generate HTML templates that exactly match your JO template format"""
    
    def __init__(self):
        self.spec_file = 'complete_jo_template_spec.json'
        self.load_template_specification()
    
    def load_template_specification(self):
        """Load the detailed template specification"""
        if os.path.exists(self.spec_file):
            with open(self.spec_file, 'r', encoding='utf-8') as f:
                self.spec = json.load(f)
            print("Loaded template specification for HTML generation")
        else:
            print(f"Warning: {self.spec_file} not found. Using default layout.")
            self.spec = self.get_default_specification()
    
    def get_default_specification(self):
        """Default specification if file not found"""
        return {
            'page_info': {
                'width': 841.68,
                'height': 595.20,
                'format': 'A4 Landscape',
                'orientation': 'landscape'
            }
        }
    
    def generate_html_template(self, data: Dict[str, Any]) -> str:
        """Generate complete HTML template with data"""
        
        # Convert points to pixels (assuming 96 DPI)
        width_px = int(self.spec['page_info']['width'] * 96 / 72)
        height_px = int(self.spec['page_info']['height'] * 96 / 72)
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sendora Job Order</title>
    <style>
        {self.generate_css_styles(width_px, height_px)}
    </style>
</head>
<body>
    <div class="jo-page">
        {self.generate_header_section(data)}
        {self.generate_form_fields_section(data)}
        {self.generate_table_section(data)}
        {self.generate_footer_section(data)}
    </div>
</body>
</html>"""
        
        return html
    
    def generate_css_styles(self, width_px: int, height_px: int) -> str:
        """Generate CSS styles that match the template exactly"""
        
        return f"""
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: Arial, sans-serif;
            background: white;
            color: black;
            font-size: 10px;
            line-height: 1.2;
        }}
        
        .jo-page {{
            width: {width_px}px;
            height: {height_px}px;
            position: relative;
            border: 1px solid #000;
            background: white;
            margin: 0 auto;
            padding: 15px;
        }}
        
        /* Header Section */
        .header-section {{
            position: absolute;
            top: 15px;
            left: 15px;
            right: 15px;
            height: 80px;
        }}
        
        .company-name {{
            position: absolute;
            top: 10px;
            left: 30px;
            font-size: 14px;
            font-weight: bold;
            color: #000;
        }}
        
        .form-type {{
            position: absolute;
            top: 10px;
            right: 30px;
            font-size: 16px;
            font-weight: bold;
            border: 2px solid #000;
            padding: 8px 16px;
            background: white;
        }}
        
        .form-title {{
            position: absolute;
            top: 50px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 14px;
            font-weight: bold;
            border: 1px solid #000;
            padding: 6px 20px;
            background: white;
        }}
        
        /* Form Fields Section */
        .form-fields {{
            position: absolute;
            top: 100px;
            left: 15px;
            right: 15px;
            height: 60px;
        }}
        
        .field-group {{
            position: absolute;
        }}
        
        .field-label {{
            font-size: 11px;
            font-weight: bold;
            color: #000;
        }}
        
        .field-value {{
            font-size: 10px;
            color: #000;
            margin-left: 5px;
            min-width: 120px;
            display: inline-block;
            border-bottom: 1px solid #ccc;
            padding-bottom: 2px;
        }}
        
        /* Left column fields */
        .job-order-no {{ top: 5px; left: 30px; }}
        .job-order-date {{ top: 25px; left: 30px; }}
        .po-no {{ top: 45px; left: 30px; }}
        
        /* Right column fields */
        .delivery-date {{ top: 5px; right: 30px; }}
        .customer-name {{ top: 25px; right: 30px; }}
        .measure-by {{ top: 45px; right: 30px; }}
        
        /* Table Section */
        .table-section {{
            position: absolute;
            top: 180px;
            left: 15px;
            right: 15px;
            height: 320px;
        }}
        
        .jo-table {{
            width: 100%;
            border-collapse: collapse;
            border: 2px solid #000;
            font-size: 9px;
        }}
        
        .jo-table th,
        .jo-table td {{
            border: 1px solid #000;
            padding: 4px 2px;
            text-align: center;
            vertical-align: top;
            position: relative;
        }}
        
        .jo-table th {{
            background: #f0f0f0;
            font-weight: bold;
            font-size: 9px;
            height: 40px;
            line-height: 1.1;
        }}
        
        .jo-table .data-row {{
            height: 70px;
        }}
        
        /* Checkbox columns */
        .checkbox-column {{
            width: 70px;
            position: relative;
        }}
        
        .checkbox-group {{
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            padding: 2px;
            font-size: 7px;
        }}
        
        .checkbox-item {{
            display: flex;
            align-items: center;
            margin-bottom: 2px;
            width: 100%;
        }}
        
        .checkbox {{
            width: 8px;
            height: 8px;
            border: 1px solid #000;
            margin-right: 3px;
            position: relative;
            flex-shrink: 0;
        }}
        
        .checkbox.checked::before {{
            content: '✓';
            position: absolute;
            top: -2px;
            left: 0px;
            font-size: 8px;
            font-weight: bold;
            color: #000;
        }}
        
        .checkbox-label {{
            font-size: 7px;
            line-height: 1;
            white-space: nowrap;
        }}
        
        /* Specific column widths */
        .col-item {{ width: 40px; }}
        .col-laminate {{ width: 80px; }}
        .col-thickness {{ width: 70px; }}
        .col-size {{ width: 90px; }}
        .col-type {{ width: 70px; }}
        .col-core {{ width: 80px; }}
        .col-edging {{ width: 70px; }}
        .col-decorative {{ width: 70px; }}
        .col-design {{ width: 80px; }}
        .col-hole {{ width: 80px; }}
        .col-remark {{ width: 100px; }}
        
        /* Footer Section */
        .footer-section {{
            position: absolute;
            bottom: 15px;
            left: 15px;
            right: 15px;
            height: 80px;
        }}
        
        .signature-group {{
            position: absolute;
            width: 250px;
            height: 70px;
            font-size: 9px;
        }}
        
        .signature-group.left {{ left: 30px; }}
        .signature-group.center {{ left: 50%; transform: translateX(-50%); }}
        .signature-group.right {{ right: 30px; }}
        
        .signature-line {{
            margin-bottom: 8px;
        }}
        
        .signature-label {{
            font-weight: bold;
            margin-bottom: 15px;
        }}
        
        .signature-role {{
            font-size: 8px;
            color: #666;
        }}
        
        .signature-date {{
            font-size: 8px;
            margin-top: 5px;
        }}
        
        /* Location fields within table rows */
        .location-field {{
            position: absolute;
            bottom: 2px;
            left: 2px;
            font-size: 7px;
            color: #666;
        }}
        
        @media print {{
            body {{ margin: 0; }}
            .jo-page {{ margin: 0; }}
        }}
        """
    
    def generate_header_section(self, data: Dict[str, Any]) -> str:
        """Generate header with company branding"""
        
        company_name = "SENDORA GROUP SDN BHD (HQ)"
        form_type = "JOB ORDER"
        form_title = "DOOR"
        
        return f"""
        <div class="header-section">
            <div class="company-name">{company_name}</div>
            <div class="form-type">{form_type}</div>
            <div class="form-title">{form_title}</div>
        </div>
        """
    
    def generate_form_fields_section(self, data: Dict[str, Any]) -> str:
        """Generate form fields section"""
        
        # Extract field values from data
        fields = {
            'job_order_no': data.get('invoice_number', ''),
            'job_order_date': data.get('document_date', ''),
            'po_no': data.get('po_number', ''),
            'delivery_date': data.get('delivery_date', ''),
            'customer_name': data.get('customer_name', ''),
            'measure_by': data.get('measure_by', 'Auto Generated')
        }
        
        return f"""
        <div class="form-fields">
            <div class="field-group job-order-no">
                <span class="field-label">Job Order No:</span>
                <span class="field-value">{fields['job_order_no']}</span>
            </div>
            <div class="field-group job-order-date">
                <span class="field-label">Job Order Date:</span>
                <span class="field-value">{fields['job_order_date']}</span>
            </div>
            <div class="field-group po-no">
                <span class="field-label">PO NO:</span>
                <span class="field-value">{fields['po_no']}</span>
            </div>
            <div class="field-group delivery-date">
                <span class="field-label">Delivery Date:</span>
                <span class="field-value">{fields['delivery_date']}</span>
            </div>
            <div class="field-group customer-name">
                <span class="field-label">Customer Name:</span>
                <span class="field-value">{fields['customer_name']}</span>
            </div>
            <div class="field-group measure-by">
                <span class="field-label">Measure By:</span>
                <span class="field-value">{fields['measure_by']}</span>
            </div>
        </div>
        """
    
    def generate_table_section(self, data: Dict[str, Any]) -> str:
        """Generate table section with line items and checkboxes"""
        
        # Extract line items
        line_items = self.extract_line_items(data)
        
        # Generate table header
        table_html = """
        <div class="table-section">
            <table class="jo-table">
                <thead>
                    <tr>
                        <th class="col-item">ITEM</th>
                        <th class="col-laminate">LAMINATE<br>CODE</th>
                        <th class="col-thickness">DOOR<br>THICKNESS</th>
                        <th class="col-size">DOOR<br>SIZE</th>
                        <th class="col-type">DOOR<br>TYPE</th>
                        <th class="col-core">DOOR<br>CORE</th>
                        <th class="col-edging">EDGING</th>
                        <th class="col-decorative">DECORATIVE<br>LINE</th>
                        <th class="col-design">DESIGN<br>NAME</th>
                        <th class="col-hole">OPEN HOLE<br>TYPE</th>
                        <th class="col-remark">DRAWING /<br>REMARK</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        # Generate 4 rows (standard JO template)
        for i in range(4):
            item = line_items[i] if i < len(line_items) else {}
            table_html += self.generate_table_row(i + 1, item, data)
        
        table_html += """
                </tbody>
            </table>
        </div>
        """
        
        return table_html
    
    def generate_table_row(self, row_num: int, item: Dict, data: Dict[str, Any]) -> str:
        """Generate a single table row with checkboxes"""
        
        # Extract item data
        laminate_code = item.get('laminate_code', '')
        door_size = item.get('size', '')
        design_name = item.get('design_name', '')
        
        # Only first row has data by default
        if row_num == 1:
            door_thickness = data.get('door_thickness', '')
            door_type = data.get('door_type', '')
            door_core = data.get('door_core', '')
            door_edging = data.get('door_edging', '')
            decorative_line = data.get('decorative_line', '')
        else:
            door_thickness = door_type = door_core = door_edging = decorative_line = ''
        
        return f"""
            <tr class="data-row">
                <td class="col-item">{row_num if item else ''}</td>
                <td class="col-laminate">{laminate_code}
                    <div class="location-field">Location: {row_num}</div>
                </td>
                <td class="col-thickness checkbox-column">
                    {self.generate_checkbox_group('thickness', door_thickness)}
                </td>
                <td class="col-size">{door_size}</td>
                <td class="col-type checkbox-column">
                    {self.generate_checkbox_group('type', door_type)}
                </td>
                <td class="col-core checkbox-column">
                    {self.generate_checkbox_group('core', door_core)}
                </td>
                <td class="col-edging checkbox-column">
                    {self.generate_checkbox_group('edging', door_edging)}
                </td>
                <td class="col-decorative checkbox-column">
                    {self.generate_checkbox_group('decorative', decorative_line)}
                </td>
                <td class="col-design">{design_name}</td>
                <td class="col-hole"></td>
                <td class="col-remark"></td>
            </tr>
        """
    
    def generate_checkbox_group(self, group_type: str, selected_value: str) -> str:
        """Generate checkbox group for a specific type"""
        
        checkbox_options = {
            'thickness': ['37mm', '43mm', '48mm', 'Others'],
            'type': ['S/L', 'D/L', 'Unequal D/L', 'Others'],
            'core': ['Honeycomb', 'Solid Tubular Core', 'Solid Timber', 'Metal Skeleton'],
            'edging': ['NA Lipping', 'ABS Edging', 'No Edging'],
            'decorative': ['T-bar', 'Groove Line']
        }
        
        options = checkbox_options.get(group_type, [])
        selected_lower = selected_value.lower()
        
        html = '<div class="checkbox-group">'
        
        for option in options:
            # Check if this option should be marked
            is_checked = False
            if selected_lower:
                if group_type == 'thickness' and option.replace('mm', '') in selected_lower:
                    is_checked = True
                elif group_type == 'type' and option.lower() in selected_lower:
                    is_checked = True
                elif group_type == 'core' and any(word in selected_lower for word in option.lower().split()):
                    is_checked = True
                elif group_type == 'edging' and any(word in selected_lower for word in option.lower().split()):
                    is_checked = True
                elif group_type == 'decorative' and option.lower().replace('-', '') in selected_lower.replace('-', ''):
                    is_checked = True
            
            checkbox_class = 'checkbox checked' if is_checked else 'checkbox'
            
            html += f"""
                <div class="checkbox-item">
                    <div class="{checkbox_class}"></div>
                    <span class="checkbox-label">{option}</span>
                </div>
            """
        
        html += '</div>'
        return html
    
    def generate_footer_section(self, data: Dict[str, Any]) -> str:
        """Generate footer with signature fields"""
        
        return """
        <div class="footer-section">
            <div class="signature-group left">
                <div class="signature-label">Prepare by,</div>
                <div class="signature-role">Sales Executive :</div>
                <div class="signature-date">Date :</div>
            </div>
            <div class="signature-group center">
                <div class="signature-label">Checked by,</div>
                <div class="signature-role">Sales Admin</div>
                <div class="signature-date">Date :</div>
            </div>
            <div class="signature-group right">
                <div class="signature-label">Verify by,</div>
                <div class="signature-role">Production Supervisor :</div>
                <div class="signature-date">Date :</div>
            </div>
        </div>
        """
    
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
                    'laminate_code': self.extract_laminate_code(data[desc_key]),
                    'design_name': data.get(f'item_design_{i}', '')
                }
                line_items.append(item)
        return line_items
    
    def extract_laminate_code(self, description: str) -> str:
        """Extract laminate code from description"""
        import re
        pattern = r'([0-9]+[A-Z]-[A-Z0-9]+)'
        match = re.search(pattern, description)
        return match.group(1) if match else ""
    
    def save_html_template(self, html_content: str, output_path: str) -> bool:
        """Save HTML template to file"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"HTML template saved: {output_path}")
            return True
        except Exception as e:
            print(f"Error saving HTML template: {e}")
            return False
    
    def generate_jo_html(self, validated_data: Dict[str, Any], output_path: str = None) -> str:
        """Generate JO as HTML file"""
        
        if not output_path:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = f"JO_HTML_{timestamp}.html"
        
        # Generate HTML content
        html_content = self.generate_html_template(validated_data)
        
        # Save to file
        if self.save_html_template(html_content, output_path):
            return output_path
        else:
            return None


# Test the HTML template generator
if __name__ == "__main__":
    generator = HTMLTemplateGenerator()
    
    print("=" * 60)
    print("HTML TEMPLATE GENERATOR")
    print("Creating pixel-perfect HTML recreation of JO template")
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
    
    print("\\nGenerating HTML template...")
    result = generator.generate_jo_html(sample_data)
    
    if result:
        print(f"\\nSUCCESS! Generated HTML template: {result}")
        print("This HTML preserves your exact JO format!")
        print("\\nNext step: Convert HTML to PDF for final JO generation")
    else:
        print("\\nFAILED: Check template specification and data")