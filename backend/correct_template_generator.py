"""
Correct Template Generator
Based on the ACTUAL Sendora JO template structure
"""

import os
from datetime import datetime
from typing import Dict, Any

class CorrectTemplateGenerator:
    """Generate HTML that matches the ACTUAL Sendora JO template"""
    
    def __init__(self):
        self.output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'job_orders')
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_correct_jo(self, validated_data: Dict[str, Any]) -> str:
        """Generate correct JO based on actual template"""
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        html_filename = f"JO_CORRECT_{timestamp}.html"
        html_path = os.path.join(self.output_dir, html_filename)
        
        # Generate HTML content
        html_content = self.create_correct_template(validated_data)
        
        # Save HTML file
        try:
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"SUCCESS! Correct JO generated: {html_filename}")
            print("This matches your actual template structure!")
            
            return html_path
            
        except Exception as e:
            print(f"Error generating correct JO: {e}")
            return None
    
    def create_correct_template(self, data: Dict[str, Any]) -> str:
        """Create HTML matching the actual template structure"""
        
        # Extract data
        job_order_no = data.get('invoice_number', '')
        job_order_date = data.get('document_date', '')
        po_no = data.get('po_number', '')
        delivery_date = data.get('delivery_date', '')
        customer_name = data.get('customer_name', '')  # This is the actual customer from the invoice
        measure_by = data.get('measure_by', '')
        
        # Extract items (up to 4 per page as per template)
        door_items = self.extract_door_items(data)
        frame_items = self.extract_frame_items(data)
        
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sendora Job Order</title>
    <style>
        @page {{
            size: A4;
            margin: 10mm;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: Arial, sans-serif;
            font-size: 9px;
            line-height: 1.1;
            background: white;
            color: black;
        }}
        
        .page {{
            width: 210mm;
            height: 297mm;
            position: relative;
            page-break-after: always;
            border: 1px solid #000;
            padding: 5mm;
        }}
        
        .page:last-child {{
            page-break-after: auto;
        }}
        
        /* Header Section */
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
            border-bottom: 1px solid #000;
            padding-bottom: 5px;
        }}
        
        .company-info {{
            font-weight: bold;
        }}
        
        .job-order-title {{
            font-size: 16px;
            font-weight: bold;
            border: 2px solid #000;
            padding: 5px 10px;
        }}
        
        .form-type {{
            font-size: 24px;
            font-weight: bold;
            text-align: center;
            margin: 10px 0;
        }}
        
        /* Form Fields */
        .form-fields {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-bottom: 10px;
            font-size: 10px;
        }}
        
        .field-group {{
            display: flex;
            align-items: center;
        }}
        
        .field-label {{
            font-weight: bold;
            margin-right: 5px;
            min-width: 80px;
        }}
        
        .field-value {{
            border-bottom: 1px solid #000;
            flex: 1;
            padding: 2px;
        }}
        
        /* Table Section */
        .items-table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 10px;
        }}
        
        .items-table th,
        .items-table td {{
            border: 1px solid #000;
            padding: 3px;
            text-align: center;
            vertical-align: top;
            font-size: 8px;
        }}
        
        .items-table th {{
            background: #f0f0f0;
            font-weight: bold;
        }}
        
        .item-column {{
            width: 20mm;
        }}
        
        .laminate-column {{
            width: 25mm;
        }}
        
        .thickness-column {{
            width: 20mm;
        }}
        
        .size-column {{
            width: 35mm;
        }}
        
        .door-type-column {{
            width: 20mm;
        }}
        
        .door-core-column {{
            width: 25mm;
        }}
        
        .edging-column {{
            width: 20mm;
        }}
        
        .decorative-column {{
            width: 20mm;
        }}
        
        .design-column {{
            width: 20mm;
        }}
        
        .openhole-column {{
            width: 20mm;
        }}
        
        .remark-column {{
            width: 25mm;
        }}
        
        /* Checkbox styles */
        .checkbox-group {{
            display: flex;
            flex-direction: column;
            gap: 1px;
        }}
        
        .checkbox-item {{
            display: flex;
            align-items: center;
            gap: 2px;
            font-size: 6px;
        }}
        
        .checkbox {{
            width: 6px;
            height: 6px;
            border: 1px solid #000;
            display: inline-block;
            position: relative;
        }}
        
        .checkbox.checked::after {{
            content: '✓';
            position: absolute;
            top: -2px;
            left: -1px;
            font-size: 7px;
            font-weight: bold;
        }}
        
        .location-text {{
            font-size: 6px;
            color: #666;
            margin-top: 2px;
        }}
        
        /* Footer */
        .footer {{
            position: absolute;
            bottom: 10mm;
            left: 5mm;
            right: 5mm;
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 10px;
            font-size: 8px;
        }}
        
        .signature-section {{
            text-align: center;
        }}
        
        .signature-label {{
            font-weight: bold;
            margin-bottom: 20px;
        }}
        
        .signature-role {{
            font-size: 7px;
            color: #666;
        }}
        
        @media print {{
            body {{ margin: 0; }}
            .page {{ margin: 0; }}
        }}
    </style>
</head>
<body>
    <!-- DOOR PAGE -->
    <div class="page">
        <div class="header">
            <div class="company-info">
                SENDORA GROUP SDN BHD (HQ)
            </div>
            <div class="job-order-title">JOB ORDER</div>
        </div>
        
        <div class="form-type">DOOR</div>
        
        <div class="form-fields">
            <div class="field-group">
                <span class="field-label">Job Order No:</span>
                <span class="field-value">{job_order_no}</span>
            </div>
            <div class="field-group">
                <span class="field-label">Delivery Date:</span>
                <span class="field-value">{delivery_date}</span>
            </div>
            <div class="field-group">
                <span class="field-label">Job Order Date:</span>
                <span class="field-value">{job_order_date}</span>
            </div>
            <div class="field-group">
                <span class="field-label">Customer Name:</span>
                <span class="field-value">{customer_name}</span>
            </div>
            <div class="field-group">
                <span class="field-label">P.O NO:</span>
                <span class="field-value">{po_no}</span>
            </div>
            <div class="field-group">
                <span class="field-label">Measure By:</span>
                <span class="field-value">{measure_by}</span>
            </div>
        </div>
        
        <table class="items-table">
            <thead>
                <tr>
                    <th class="item-column">ITEM</th>
                    <th class="laminate-column">LAMINATE CODE</th>
                    <th class="thickness-column">DOOR THICKNESS</th>
                    <th class="size-column">DOOR SIZE</th>
                    <th class="door-type-column">DOOR TYPE</th>
                    <th class="door-core-column">DOOR CORE</th>
                    <th class="edging-column">EDGING</th>
                    <th class="decorative-column">DECORATIVE LINE</th>
                    <th class="design-column">DESIGN NAME</th>
                    <th class="openhole-column">OPEN HOLE TYPE</th>
                    <th class="remark-column">DRAWING REMARK</th>
                </tr>
            </thead>
            <tbody>
                {self.generate_door_rows(door_items, data)}
            </tbody>
        </table>
        
        <div class="footer">
            <div class="signature-section">
                <div class="signature-label">Prepare by,</div>
                <div class="signature-role">Sales Executive :</div>
                <div class="signature-role">Date :</div>
            </div>
            <div class="signature-section">
                <div class="signature-label">Checked by,</div>
                <div class="signature-role">Sales Admin</div>
                <div class="signature-role">Date :</div>
            </div>
            <div class="signature-section">
                <div class="signature-label">Verify by,</div>
                <div class="signature-role">Production Supervisor :</div>
                <div class="signature-role">Date :</div>
            </div>
        </div>
    </div>
    
    <!-- FRAME PAGE -->
    <div class="page">
        <div class="header">
            <div class="company-info">
                SENDORA GROUP SDN BHD (HQ)
            </div>
            <div class="job-order-title">JOB ORDER</div>
        </div>
        
        <div class="form-type">FRAME</div>
        
        <div class="form-fields">
            <div class="field-group">
                <span class="field-label">Job Order No:</span>
                <span class="field-value">{job_order_no}</span>
            </div>
            <div class="field-group">
                <span class="field-label">Delivery Date:</span>
                <span class="field-value">{delivery_date}</span>
            </div>
            <div class="field-group">
                <span class="field-label">Job Order Date:</span>
                <span class="field-value">{job_order_date}</span>
            </div>
            <div class="field-group">
                <span class="field-label">Customer Name:</span>
                <span class="field-value">{customer_name}</span>
            </div>
            <div class="field-group">
                <span class="field-label">P.O NO:</span>
                <span class="field-value">{po_no}</span>
            </div>
            <div class="field-group">
                <span class="field-label">Measure By:</span>
                <span class="field-value">{measure_by}</span>
            </div>
        </div>
        
        <table class="items-table">
            <thead>
                <tr>
                    <th class="item-column">ITEM</th>
                    <th class="laminate-column">FRAME LAMINATE CODE</th>
                    <th class="thickness-column">FRAME WIDTH</th>
                    <th class="size-column">FRAME SIZE</th>
                    <th class="door-type-column">INNER OR OUTER</th>
                    <th colspan="6">DRAWING REMARK</th>
                </tr>
            </thead>
            <tbody>
                {self.generate_frame_rows(frame_items)}
            </tbody>
        </table>
        
        <div class="footer">
            <div class="signature-section">
                <div class="signature-label">Prepare by,</div>
                <div class="signature-role">Sales Executive :</div>
                <div class="signature-role">Date :</div>
            </div>
            <div class="signature-section">
                <div class="signature-label">Checked by,</div>
                <div class="signature-role">Sales Admin</div>
                <div class="signature-role">Date :</div>
            </div>
            <div class="signature-section">
                <div class="signature-label">Verify by,</div>
                <div class="signature-role">Production Supervisor :</div>
                <div class="signature-role">Date :</div>
            </div>
        </div>
    </div>
</body>
</html>'''
    
    def extract_door_items(self, data: Dict[str, Any]) -> list:
        """Extract door items from data"""
        items = []
        for i in range(4):  # Template shows 4 door items
            desc_key = f'item_desc_{i}'
            if desc_key in data and data[desc_key]:
                items.append({
                    'item_no': i + 1,
                    'laminate_code': self.extract_laminate_code(data[desc_key]),
                    'size': data.get(f'item_size_{i}', ''),
                    'description': data[desc_key]
                })
        return items
    
    def extract_frame_items(self, data: Dict[str, Any]) -> list:
        """Extract frame items from data"""
        # Frame items would be separate, for now use sample
        return [{'item_no': 1, 'laminate_code': '6S-145', 'width': '130-150MM', 'size': '1428MM x 2348MM'}]
    
    def generate_door_rows(self, items: list, data: Dict[str, Any]) -> str:
        """Generate door table rows"""
        rows = ""
        door_thickness = data.get('door_thickness', '').lower()
        door_type = data.get('door_type', '').lower()
        door_core = data.get('door_core', '').lower()
        door_edging = data.get('door_edging', '').lower()
        decorative_line = data.get('decorative_line', '').lower()
        
        for i in range(4):  # Always show 4 rows as per template
            item = items[i] if i < len(items) else {}
            
            # Checkbox logic - only first item has selections
            thickness_37 = "checked" if i == 0 and "37" in door_thickness else ""
            thickness_43 = "checked" if i == 0 and "43" in door_thickness else ""
            thickness_48 = "checked" if i == 0 and "48" in door_thickness else ""
            
            type_sl = "checked" if i == 0 and "s/l" in door_type else ""
            type_dl = "checked" if i == 0 and "d/l" in door_type else ""
            type_unequal = "checked" if i == 0 and "unequal" in door_type else ""
            
            core_honeycomb = "checked" if i == 0 and "honeycomb" in door_core else ""
            core_tubular = "checked" if i == 0 and "tubular" in door_core else ""
            core_timber = "checked" if i == 0 and "timber" in door_core else ""
            core_metal = "checked" if i == 0 and "metal" in door_core else ""
            
            edging_na = "checked" if i == 0 and "na lipping" in door_edging else ""
            edging_abs = "checked" if i == 0 and "abs" in door_edging else ""
            edging_no = "checked" if i == 0 and "no edging" in door_edging else ""
            
            decorative_tbar = "checked" if i == 0 and "t-bar" in decorative_line else ""
            decorative_groove = "checked" if i == 0 and "groove" in decorative_line else ""
            
            rows += f'''
                <tr style="height: 60px;">
                    <td>{item.get('item_no', '')}</td>
                    <td>
                        {item.get('laminate_code', '')}
                    </td>
                    <td>
                        <div class="checkbox-group">
                            <div class="checkbox-item">
                                <span class="checkbox {thickness_37}"></span>
                                <span>37mm</span>
                            </div>
                            <div class="checkbox-item">
                                <span class="checkbox {thickness_43}"></span>
                                <span>43mm</span>
                            </div>
                            <div class="checkbox-item">
                                <span class="checkbox {thickness_48}"></span>
                                <span>48mm</span>
                            </div>
                            <div class="checkbox-item">
                                <span class="checkbox"></span>
                                <span>Others</span>
                            </div>
                        </div>
                    </td>
                    <td>
                        {item.get('size', '')} {chr(9312 + i)}
                        <div class="location-text">Location: D{i+1}</div>
                    </td>
                    <td>
                        <div class="checkbox-group">
                            <div class="checkbox-item">
                                <span class="checkbox {type_sl}"></span>
                                <span>S/L</span>
                            </div>
                            <div class="checkbox-item">
                                <span class="checkbox {type_dl}"></span>
                                <span>D/L</span>
                            </div>
                            <div class="checkbox-item">
                                <span class="checkbox {type_unequal}"></span>
                                <span>Unequal D/L</span>
                            </div>
                            <div class="checkbox-item">
                                <span class="checkbox"></span>
                                <span>Others</span>
                            </div>
                        </div>
                    </td>
                    <td>
                        <div class="checkbox-group">
                            <div class="checkbox-item">
                                <span class="checkbox {core_honeycomb}"></span>
                                <span>Honeycomb</span>
                            </div>
                            <div class="checkbox-item">
                                <span class="checkbox {core_tubular}"></span>
                                <span>Solid Tubular Core</span>
                            </div>
                            <div class="checkbox-item">
                                <span class="checkbox {core_timber}"></span>
                                <span>Solid Timber</span>
                            </div>
                            <div class="checkbox-item">
                                <span class="checkbox {core_metal}"></span>
                                <span>Metal Skeleton</span>
                            </div>
                        </div>
                    </td>
                    <td>
                        <div class="checkbox-group">
                            <div class="checkbox-item">
                                <span class="checkbox {edging_na}"></span>
                                <span>NA Lipping</span>
                            </div>
                            <div class="checkbox-item">
                                <span class="checkbox {edging_abs}"></span>
                                <span>ABS Edging</span>
                            </div>
                            <div class="checkbox-item">
                                <span class="checkbox {edging_no}"></span>
                                <span>No Edging</span>
                            </div>
                        </div>
                    </td>
                    <td>
                        <div class="checkbox-group">
                            <div class="checkbox-item">
                                <span class="checkbox {decorative_tbar}"></span>
                                <span>T-bar</span>
                            </div>
                            <div class="checkbox-item">
                                <span class="checkbox {decorative_groove}"></span>
                                <span>Groove Line</span>
                            </div>
                        </div>
                    </td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>
            '''
        return rows
    
    def generate_frame_rows(self, items: list) -> str:
        """Generate frame table rows"""
        rows = ""
        for i in range(1):  # Frame typically has 1 row
            item = items[i] if i < len(items) else {}
            rows += f'''
                <tr style="height: 60px;">
                    <td>{item.get('item_no', '')}</td>
                    <td>
                        {item.get('laminate_code', '')}
                        <div class="location-text">Location: F{i+1}</div>
                    </td>
                    <td>{item.get('width', '')}</td>
                    <td>{item.get('size', '')}</td>
                    <td>
                        <div class="checkbox-group">
                            <div class="checkbox-item">
                                <span class="checkbox checked"></span>
                                <span>INNER</span>
                            </div>
                            <div class="checkbox-item">
                                <span class="checkbox"></span>
                                <span>OUTER</span>
                            </div>
                        </div>
                    </td>
                    <td colspan="6"></td>
                </tr>
            '''
        return rows
    
    def extract_laminate_code(self, description: str) -> str:
        """Extract laminate code from description"""
        import re
        pattern = r'([0-9]+[A-Z]-[A-Z0-9]+)'
        match = re.search(pattern, description)
        return match.group(1) if match else ""


# Test the correct generator
if __name__ == "__main__":
    generator = CorrectTemplateGenerator()
    
    test_data = {
        'invoice_number': 'JO-001',
        'customer_name': 'KENCANA CONSTRUCTION SDN BHD',  # Actual customer from invoices
        'document_date': '2025-08-14',
        'delivery_date': '2025-08-20',
        'po_number': 'PO-2025-001',
        'measure_by': 'John Doe',
        'door_thickness': '43mm',
        'door_type': 'S/L',
        'door_core': 'solid tubular core',
        'door_edging': 'na lipping',
        'decorative_line': 't-bar',
        'item_desc_0': '6S-A057 DOOR 850MM x 2021MM',
        'item_size_0': '850MM x 2021MM'
    }
    
    result = generator.generate_correct_jo(test_data)
    print(f"Generated: {result}")