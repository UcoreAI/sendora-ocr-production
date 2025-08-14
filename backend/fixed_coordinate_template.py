"""
Fixed Coordinate Template Generator
Exact match to the actual Sendora JO template structure
"""

import os
from datetime import datetime
from typing import Dict, Any

class FixedCoordinateTemplate:
    """Generate HTML that exactly matches the ACTUAL Sendora JO template"""
    
    def __init__(self):
        self.output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'job_orders')
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_fixed_jo(self, validated_data: Dict[str, Any]) -> str:
        """Generate fixed JO based on exact template"""
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        html_filename = f"JO_FIXED_{timestamp}.html"
        html_path = os.path.join(self.output_dir, html_filename)
        
        # Generate HTML content
        html_content = self.create_exact_template(validated_data)
        
        # Save HTML file
        try:
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"SUCCESS! Fixed coordinates JO generated: {html_filename}")
            print("This exactly matches your template structure!")
            
            return html_path
            
        except Exception as e:
            print(f"Error generating fixed JO: {e}")
            return None
    
    def create_exact_template(self, data: Dict[str, Any]) -> str:
        """Create HTML matching the exact template structure"""
        
        # Extract data
        job_order_no = data.get('invoice_number', '')
        job_order_date = data.get('document_date', '')
        po_no = data.get('po_number', '')
        delivery_date = data.get('delivery_date', '')
        customer_name = data.get('customer_name', '')
        measure_by = data.get('measure_by', '')
        
        # Extract items
        door_items = self.extract_door_items(data)
        
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sendora Job Order - Fixed Coordinates</title>
    <style>
        @page {{
            size: A4;
            margin: 8mm;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: Arial, sans-serif;
            font-size: 8px;
            line-height: 1.0;
            background: white;
            color: black;
        }}
        
        .page {{
            width: 210mm;
            height: 297mm;
            position: relative;
            page-break-after: always;
            padding: 5mm;
        }}
        
        .page:last-child {{
            page-break-after: auto;
        }}
        
        /* Header */
        .header {{
            text-align: center;
            margin-bottom: 3mm;
        }}
        
        .company-name {{
            font-size: 12px;
            font-weight: bold;
            text-decoration: underline;
            margin-bottom: 2mm;
        }}
        
        /* Job Order Title and Form Fields */
        .title-section {{
            display: grid;
            grid-template-columns: 2fr auto 2fr;
            align-items: start;
            margin-bottom: 3mm;
        }}
        
        .left-fields {{
            font-size: 9px;
        }}
        
        .center-title {{
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        
        .job-order-box {{
            border: 2px solid #000;
            padding: 8px 16px;
            font-size: 18px;
            font-weight: bold;
            text-align: center;
        }}
        
        .right-fields {{
            font-size: 9px;
            text-align: right;
        }}
        
        .field-line {{
            display: flex;
            margin-bottom: 1mm;
        }}
        
        .field-label {{
            font-weight: bold;
            margin-right: 3px;
        }}
        
        .field-underline {{
            flex: 1;
            border-bottom: 1px solid #000;
            min-height: 12px;
            padding-left: 2px;
        }}
        
        /* Door/Frame Title */
        .form-type {{
            text-align: center;
            font-size: 32px;
            font-weight: bold;
            margin: 8mm 0 5mm 0;
            letter-spacing: 3px;
            border: 3px solid #000;
            padding: 5mm;
        }}
        
        /* Table */
        .items-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 7px;
        }}
        
        .items-table th,
        .items-table td {{
            border: 1px solid #000;
            padding: 1px;
            text-align: center;
            vertical-align: top;
        }}
        
        .items-table th {{
            background: #f8f8f8;
            font-weight: bold;
            padding: 2px;
        }}
        
        /* Column widths matching template */
        .col-item {{ width: 8mm; }}
        .col-laminate {{ width: 15mm; }}
        .col-thickness {{ width: 16mm; }}
        .col-size {{ width: 28mm; }}
        .col-type {{ width: 18mm; }}
        .col-core {{ width: 20mm; }}
        .col-edging {{ width: 16mm; }}
        .col-decorative {{ width: 16mm; }}
        .col-design {{ width: 18mm; }}
        .col-openhole {{ width: 16mm; }}
        .col-remark {{ width: 25mm; }}
        
        .item-row {{
            height: 35mm;
        }}
        
        /* Checkboxes */
        .checkbox-list {{
            display: flex;
            flex-direction: column;
            gap: 1px;
            font-size: 6px;
        }}
        
        .checkbox-item {{
            display: flex;
            align-items: center;
            gap: 1px;
            text-align: left;
        }}
        
        .checkbox {{
            width: 5px;
            height: 5px;
            border: 1px solid #000;
            display: inline-block;
            position: relative;
        }}
        
        .checkbox.checked::after {{
            content: '✓';
            position: absolute;
            top: -2px;
            left: -1px;
            font-size: 6px;
            font-weight: bold;
        }}
        
        .location-circle {{
            font-size: 16px;
            font-weight: bold;
            margin-top: 2px;
        }}
        
        .location-text {{
            font-size: 6px;
            margin-top: 1px;
        }}
        
        /* Footer */
        .signature-footer {{
            position: absolute;
            bottom: 8mm;
            left: 5mm;
            right: 5mm;
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            font-size: 8px;
        }}
        
        .sig-section {{
            text-align: left;
        }}
        
        .sig-section.center {{ text-align: center; }}
        .sig-section.right {{ text-align: right; }}
        
        .sig-label {{
            font-weight: bold;
            margin-bottom: 15px;
        }}
        
        .sig-role {{
            font-size: 7px;
            margin-bottom: 3px;
        }}
        
        .version {{
            position: absolute;
            bottom: 3mm;
            right: 5mm;
            font-size: 7px;
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
            <div class="company-name">SENDORA GROUP SDN BHD (HQ)</div>
        </div>
        
        <div class="title-section">
            <div class="left-fields">
                <div class="field-line">
                    <span class="field-label">Job Order No:</span>
                    <span class="field-underline">{job_order_no}</span>
                </div>
                <div class="field-line">
                    <span class="field-label">Job Order Date:</span>
                    <span class="field-underline">{job_order_date}</span>
                </div>
                <div class="field-line">
                    <span class="field-label">PO NO:</span>
                    <span class="field-underline">{po_no}</span>
                </div>
            </div>
            
            <div class="center-title">
                <div class="job-order-box">JOB ORDER</div>
            </div>
            
            <div class="right-fields">
                <div class="field-line">
                    <span class="field-label">Delivery Date:</span>
                    <span class="field-underline">{delivery_date}</span>
                </div>
                <div class="field-line">
                    <span class="field-label">Customer Name:</span>
                    <span class="field-underline">{customer_name}</span>
                </div>
                <div class="field-line">
                    <span class="field-label">Measure By:</span>
                    <span class="field-underline">{measure_by}</span>
                </div>
            </div>
        </div>
        
        <div class="form-type">DOOR</div>
        
        <table class="items-table">
            <thead>
                <tr>
                    <th class="col-item">ITEM</th>
                    <th class="col-laminate">LAMINATE CODE</th>
                    <th class="col-thickness">DOOR THICKNESS</th>
                    <th class="col-size">DOOR SIZE</th>
                    <th class="col-type">DOOR TYPE</th>
                    <th class="col-core">DOOR CORE</th>
                    <th class="col-edging">EDGING</th>
                    <th class="col-decorative">DECORATIVE LINE</th>
                    <th class="col-design">DESIGN NAME</th>
                    <th class="col-openhole">OPEN HOLE TYPE</th>
                    <th class="col-remark">DRAWING / REMARK</th>
                </tr>
            </thead>
            <tbody>
                {self.generate_door_table_rows(door_items, data)}
            </tbody>
        </table>
        
        <div class="signature-footer">
            <div class="sig-section">
                <div class="sig-label">Prepare by,</div>
                <div class="sig-role">Sales Executive :</div>
                <div class="sig-role">Date :</div>
            </div>
            <div class="sig-section center">
                <div class="sig-label">Checked by,</div>
                <div class="sig-role">Sales Admin</div>
                <div class="sig-role">Date :</div>
            </div>
            <div class="sig-section right">
                <div class="sig-label">Verify by,</div>
                <div class="sig-role">Production Supervisor :</div>
                <div class="sig-role">Date :</div>
            </div>
        </div>
        
        <div class="version">SGSB (v050625)</div>
    </div>
    
    <!-- FRAME PAGE -->
    <div class="page">
        <div class="header">
            <div class="company-name">SENDORA GROUP SDN BHD (HQ)</div>
        </div>
        
        <div class="title-section">
            <div class="left-fields">
                <div class="field-line">
                    <span class="field-label">Job Order No:</span>
                    <span class="field-underline">{job_order_no}</span>
                </div>
                <div class="field-line">
                    <span class="field-label">Job Order Date:</span>
                    <span class="field-underline">{job_order_date}</span>
                </div>
                <div class="field-line">
                    <span class="field-label">PO NO:</span>
                    <span class="field-underline">{po_no}</span>
                </div>
            </div>
            
            <div class="center-title">
                <div class="job-order-box">JOB ORDER</div>
            </div>
            
            <div class="right-fields">
                <div class="field-line">
                    <span class="field-label">Delivery Date:</span>
                    <span class="field-underline">{delivery_date}</span>
                </div>
                <div class="field-line">
                    <span class="field-label">Customer Name:</span>
                    <span class="field-underline">{customer_name}</span>
                </div>
                <div class="field-line">
                    <span class="field-label">Measure by:</span>
                    <span class="field-underline">{measure_by}</span>
                </div>
            </div>
        </div>
        
        <div class="form-type">FRAME</div>
        
        <table class="items-table">
            <thead>
                <tr>
                    <th class="col-item">ITEM</th>
                    <th class="col-laminate">FRAME LAMINATE CODE</th>
                    <th class="col-thickness">FRAME WIDTH</th>
                    <th class="col-type">REBATED</th>
                    <th class="col-size">FRAME SIZE</th>
                    <th class="col-core">INNER OR OUTER</th>
                    <th class="col-edging">FRAME PROFILE</th>
                    <th class="col-remark">DRAWING / REMARK</th>
                </tr>
            </thead>
            <tbody>
                {self.generate_frame_table_rows()}
            </tbody>
        </table>
        
        <div class="signature-footer">
            <div class="sig-section">
                <div class="sig-label">Prepare by,</div>
                <div class="sig-role">Sales Executive :</div>
                <div class="sig-role">Date :</div>
            </div>
            <div class="sig-section center">
                <div class="sig-label">Checked by,</div>
                <div class="sig-role">Sales Admin :</div>
                <div class="sig-role">Date :</div>
            </div>
            <div class="sig-section right">
                <div class="sig-label">Verify by,</div>
                <div class="sig-role">Production Supervisor :</div>
                <div class="sig-role">Date :</div>
            </div>
        </div>
        
        <div class="version">SGSB (v050625)</div>
    </div>
</body>
</html>'''
    
    def extract_door_items(self, data: Dict[str, Any]) -> list:
        """Extract door items from data"""
        items = []
        for i in range(4):  # Template shows 4 door items max
            desc_key = f'item_desc_{i}'
            if desc_key in data and data[desc_key]:
                items.append({
                    'item_no': i + 1,
                    'laminate_code': self.extract_laminate_code(data[desc_key]),
                    'size': data.get(f'item_size_{i}', ''),
                    'description': data[desc_key]
                })
        return items
    
    def generate_door_table_rows(self, items: list, data: Dict[str, Any]) -> str:
        """Generate door table rows matching exact template"""
        rows = ""
        
        # Extract checkbox states from data
        door_thickness = data.get('door_thickness', '').lower()
        door_type = data.get('door_type', '').lower()
        door_core = data.get('door_core', '').lower()
        door_edging = data.get('door_edging', '').lower()
        decorative_line = data.get('decorative_line', '').lower()
        
        for i in range(4):  # Always show 4 rows as per template
            item = items[i] if i < len(items) else {}
            
            # Only first row gets checkbox selections
            is_first_row = (i == 0)
            
            # Thickness checkboxes
            thickness_37 = "checked" if is_first_row and "37" in door_thickness else ""
            thickness_43 = "checked" if is_first_row and "43" in door_thickness else ""
            thickness_48 = "checked" if is_first_row and "48" in door_thickness else ""
            
            # Type checkboxes
            type_sl = "checked" if is_first_row and "s/l" in door_type else ""
            type_dl = "checked" if is_first_row and "d/l" in door_type else ""
            type_unequal = "checked" if is_first_row and "unequal" in door_type else ""
            
            # Core checkboxes
            core_honeycomb = "checked" if is_first_row and "honeycomb" in door_core else ""
            core_tubular = "checked" if is_first_row and "tubular" in door_core else ""
            core_timber = "checked" if is_first_row and "timber" in door_core else ""
            core_metal = "checked" if is_first_row and "metal" in door_core else ""
            
            # Edging checkboxes
            edging_na = "checked" if is_first_row and "na lipping" in door_edging else ""
            edging_abs = "checked" if is_first_row and "abs" in door_edging else ""
            edging_no = "checked" if is_first_row and "no edging" in door_edging else ""
            
            # Decorative checkboxes
            decorative_tbar = "checked" if is_first_row and "t-bar" in decorative_line else ""
            decorative_groove = "checked" if is_first_row and "groove" in decorative_line else ""
            
            rows += f'''
                <tr class="item-row">
                    <td>{item.get('item_no', '')}</td>
                    <td>{item.get('laminate_code', '')}</td>
                    <td>
                        <div class="checkbox-list">
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
                                <span>Others:</span>
                            </div>
                        </div>
                    </td>
                    <td>
                        {item.get('size', '')}
                        <div class="location-circle">{chr(9312 + i)}</div>
                        <div class="location-text">Location : </div>
                    </td>
                    <td>
                        <div class="checkbox-list">
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
                                <span>Others:</span>
                            </div>
                        </div>
                    </td>
                    <td>
                        <div class="checkbox-list">
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
                        <div class="checkbox-list">
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
                        <div class="checkbox-list">
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
    
    def generate_frame_table_rows(self) -> str:
        """Generate frame table rows"""
        rows = ""
        for i in range(4):  # 4 rows as per template
            rows += f'''
                <tr class="item-row">
                    <td>{1 if i == 0 else ''}</td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td>
                        <div class="location-circle">{chr(9312 + i)}</div>
                        <div class="location-text">Location : </div>
                    </td>
                    <td>
                        <div class="checkbox-list">
                            <div class="checkbox-item">
                                <span class="checkbox {'checked' if i == 0 else ''}"></span>
                                <span>INNER</span>
                            </div>
                            <div class="checkbox-item">
                                <span class="checkbox"></span>
                                <span>OUTER</span>
                            </div>
                        </div>
                    </td>
                    <td></td>
                    <td></td>
                </tr>
            '''
        return rows
    
    def extract_laminate_code(self, description: str) -> str:
        """Extract laminate code from description"""
        import re
        pattern = r'([0-9]+[A-Z]-[A-Z0-9]+)'
        match = re.search(pattern, description)
        return match.group(1) if match else ""


# Test the fixed generator
if __name__ == "__main__":
    generator = FixedCoordinateTemplate()
    
    test_data = {
        'invoice_number': 'JO-FIXED-001',
        'customer_name': 'KENCANA CONSTRUCTION SDN BHD',
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
    
    result = generator.generate_fixed_jo(test_data)
    print(f"Generated: {result}")