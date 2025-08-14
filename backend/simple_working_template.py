"""
Simple Working Template Generator
Clean, functional template that actually works
"""

import os
from datetime import datetime
from typing import Dict, Any
import re

class SimpleWorkingTemplate:
    """Generate a simple, clean template that actually works"""
    
    def __init__(self):
        self.output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'job_orders')
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_working_jo(self, validated_data: Dict[str, Any]) -> str:
        """Generate working JO that actually displays correctly"""
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        html_filename = f"JO_WORKING_{timestamp}.html"
        html_path = os.path.join(self.output_dir, html_filename)
        
        # Generate HTML content
        html_content = self.create_working_template(validated_data)
        
        # Save HTML file
        try:
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"SUCCESS! Working JO generated: {html_filename}")
            
            return html_path
            
        except Exception as e:
            print(f"Error generating working JO: {e}")
            return None
    
    def create_working_template(self, data: Dict[str, Any]) -> str:
        """Create simple HTML that actually works"""
        
        # Extract and map data properly
        job_order_no = data.get('invoice_number', '')
        job_order_date = data.get('document_date', '')
        po_no = data.get('po_number', '')
        delivery_date = data.get('delivery_date', '')
        customer_name = data.get('customer_name', '')
        measure_by = data.get('measure_by', '')
        
        # Extract item info first
        item_desc = data.get('item_desc_0', '')
        item_size = data.get('item_size_0', '')
        
        # Parse specifications
        door_thickness = data.get('door_thickness', '').lower()
        door_type = data.get('door_type', '').lower() 
        door_core = data.get('door_core', '').lower()
        door_edging = data.get('door_edging', '').lower()
        decorative_line = data.get('decorative_line', '').lower()
        
        # Get door size from data  
        door_size = data.get('door_size', '') or data.get('item_size_0', '')
        
        # Print key specs for verification
        print(f"Template: door_thickness='{door_thickness}', door_type='{door_type}', door_core='{door_core}', door_size='{door_size}'")
        
        # If door_thickness is empty, try to extract from line items or descriptions
        if not door_thickness:
            # Check item description
            if item_desc:
                desc_lower = item_desc.lower()
                if '43mm' in desc_lower or '43 mm' in desc_lower:
                    door_thickness = '43mm'
                    print(f"EXTRACTED door_thickness from item_desc: '{door_thickness}'")
                elif '37mm' in desc_lower or '37 mm' in desc_lower:
                    door_thickness = '37mm'
                    print(f"EXTRACTED door_thickness from item_desc: '{door_thickness}'")
                elif '46mm' in desc_lower or '46 mm' in desc_lower:
                    door_thickness = '46mm'
                    print(f"EXTRACTED door_thickness from item_desc: '{door_thickness}'")
            
            # Check line_items if available
            line_items = data.get('line_items', [])
            if not door_thickness and line_items:
                for item in line_items:
                    specs = item.get('specifications', {})
                    thickness = specs.get('thickness', '')
                    if thickness:
                        door_thickness = thickness.lower()
                        print(f"EXTRACTED door_thickness from line_items: '{door_thickness}'")
                        break
        laminate_code = self.extract_laminate_code(item_desc)
        
        # Generate checkbox states
        thickness_37 = "checked" if "37" in door_thickness else ""
        thickness_43 = "checked" if "43" in door_thickness else ""
        thickness_46 = "checked" if "46" in door_thickness else ""
        
        # DEBUG: Print checkbox states
        print(f"CHECKBOX DEBUG - thickness_37: '{thickness_37}' (checking '37' in '{door_thickness}')")
        print(f"CHECKBOX DEBUG - thickness_43: '{thickness_43}' (checking '43' in '{door_thickness}')")  
        print(f"CHECKBOX DEBUG - thickness_46: '{thickness_46}' (checking '46' in '{door_thickness}')")
        
        type_sl = "checked" if "s/l" in door_type else ""
        type_dl = "checked" if "d/l" in door_type and "unequal" not in door_type else ""
        type_unequal = "checked" if "unequal" in door_type else ""
        
        core_honeycomb = "checked" if "honeycomb" in door_core else ""
        core_tubular = "checked" if "tubular" in door_core else ""
        core_timber = "checked" if "timber" in door_core else ""
        core_metal = "checked" if "metal" in door_core else ""
        
        edging_na = "checked" if "na lipping" in door_edging else ""
        edging_abs = "checked" if "abs" in door_edging else ""
        edging_no = "checked" if "no edging" in door_edging else ""
        
        decorative_tbar = "checked" if "t-bar" in decorative_line else ""
        decorative_groove = "checked" if "groove" in decorative_line else ""
        
        return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Sendora Job Order</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            font-size: 10px;
            margin: 15px;
            line-height: 1.3;
        }}
        
        .page {{
            width: 190mm;
            min-height: 270mm;
            margin: 0 auto;
            border: 1px solid #000;
            padding: 8mm;
            page-break-after: always;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 8mm;
        }}
        
        .company-name {{
            font-size: 12px;
            font-weight: bold;
            text-decoration: underline;
            margin-bottom: 5mm;
        }}
        
        .fields-section {{
            display: table;
            width: 100%;
            margin-bottom: 5mm;
        }}
        
        .field-row {{
            display: table-row;
        }}
        
        .field-cell {{
            display: table-cell;
            padding: 2mm;
            vertical-align: middle;
        }}
        
        .field-label {{
            font-weight: bold;
            margin-right: 3mm;
        }}
        
        .field-value {{
            border-bottom: 1px solid #000;
            min-width: 40mm;
            padding: 1mm 2mm;
            display: inline-block;
            letter-spacing: 0.3px;
        }}
        
        .form-type {{
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            border: 2px solid #000;
            padding: 8mm;
            margin: 5mm 0;
        }}
        
        .main-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 8px;
            margin-bottom: 10mm;
        }}
        
        .main-table th,
        .main-table td {{
            border: 1px solid #000;
            padding: 2mm;
            text-align: left;
            vertical-align: top;
        }}
        
        .main-table th {{
            background-color: #f0f0f0;
            font-weight: bold;
            text-align: center;
        }}
        
        .item-row {{
            min-height: 25mm;
        }}
        
        .checkbox-section {{
            font-size: 7px;
            line-height: 1.6;
        }}
        
        .checkbox-item {{
            margin: 1.5mm 0;
            padding: 0.5mm 0;
        }}
        
        .checkbox {{
            display: inline-block;
            width: 3mm;
            height: 3mm;
            border: 1px solid #000;
            margin-right: 3mm;
            vertical-align: middle;
        }}
        
        .checkbox.checked {{
            background-color: #000;
        }}
        
        .circle-number {{
            font-size: 16px;
            font-weight: bold;
            text-align: center;
            margin: 2mm 0;
        }}
        
        .location-text {{
            font-size: 7px;
            text-align: center;
        }}
        
        .door-size {{
            font-size: 9px;
            font-weight: bold;
            margin-bottom: 2mm;
            letter-spacing: 0.5px;
        }}
        
        .footer {{
            display: table;
            width: 100%;
            margin-top: 10mm;
        }}
        
        .footer-row {{
            display: table-row;
        }}
        
        .footer-cell {{
            display: table-cell;
            width: 33%;
            padding: 2mm;
            vertical-align: top;
        }}
        
        .signature-label {{
            font-weight: bold;
            margin-bottom: 8mm;
        }}
        
        .signature-line {{
            margin: 2mm 0;
        }}
        
        .version {{
            position: absolute;
            bottom: 5mm;
            right: 10mm;
            font-size: 8px;
        }}
    </style>
</head>
<body>
    <!-- DOOR PAGE -->
    <div class="page">
        <div class="header">
            <div class="company-name">SENDORA GROUP SDN BHD (KOTA DAMANSARA)</div>
        </div>
        
        <div class="fields-section">
            <div class="field-row">
                <div class="field-cell">
                    <span class="field-label">Job Order No:</span>
                    <span class="field-value">{job_order_no}</span>
                </div>
                <div class="field-cell">
                    <span class="field-label">Delivery Date:</span>
                    <span class="field-value">{delivery_date}</span>
                </div>
            </div>
            <div class="field-row">
                <div class="field-cell">
                    <span class="field-label">Job Order Date:</span>
                    <span class="field-value">{job_order_date}</span>
                </div>
                <div class="field-cell">
                    <span class="field-label">Customer Name:</span>
                    <span class="field-value">{customer_name}</span>
                </div>
            </div>
            <div class="field-row">
                <div class="field-cell">
                    <span class="field-label">P.O NO:</span>
                    <span class="field-value">{po_no}</span>
                </div>
                <div class="field-cell">
                    <span class="field-label">Measure By:</span>
                    <span class="field-value">{measure_by}</span>
                </div>
            </div>
        </div>
        
        <div class="form-type">DOOR</div>
        
        <table class="main-table">
            <thead>
                <tr>
                    <th style="width: 8mm;">ITEM</th>
                    <th style="width: 20mm;">LAMINATE CODE</th>
                    <th style="width: 25mm;">DOOR THICKNESS</th>
                    <th style="width: 30mm;">DOOR SIZE</th>
                    <th style="width: 25mm;">DOOR TYPE</th>
                    <th style="width: 30mm;">DOOR CORE</th>
                    <th style="width: 20mm;">EDGING</th>
                    <th style="width: 20mm;">DECORATIVE LINE</th>
                    <th style="width: 15mm;">DESIGN NAME</th>
                    <th style="width: 15mm;">OPEN HOLE TYPE</th>
                    <th>DRAWING REMARK</th>
                </tr>
            </thead>
            <tbody>
                <tr class="item-row">
                    <td style="text-align: center;">1</td>
                    <td style="text-align: center;">{laminate_code}</td>
                    <td>
                        <div class="checkbox-section">
                            <div class="checkbox-item">
                                <span class="checkbox {thickness_37}"></span>37mm
                            </div>
                            <div class="checkbox-item">
                                <span class="checkbox {thickness_43}"></span>43mm
                            </div>
                            <div class="checkbox-item">
                                <span class="checkbox {thickness_46}"></span>46mm
                            </div>
                            <div class="checkbox-item">
                                <span class="checkbox"></span>Others:
                            </div>
                        </div>
                    </td>
                    <td style="text-align: center;">
                        <div class="door-size">{door_size}</div>
                        <div class="circle-number">①</div>
                        <div class="location-text">Location :</div>
                    </td>
                    <td>
                        <div class="checkbox-section">
                            <div class="checkbox-item">
                                <span class="checkbox {type_sl}"></span>S/L
                            </div>
                            <div class="checkbox-item">
                                <span class="checkbox {type_dl}"></span>D/L
                            </div>
                            <div class="checkbox-item">
                                <span class="checkbox {type_unequal}"></span>Unequal D/L
                            </div>
                            <div class="checkbox-item">
                                <span class="checkbox"></span>Others:
                            </div>
                        </div>
                    </td>
                    <td>
                        <div class="checkbox-section">
                            <div class="checkbox-item">
                                <span class="checkbox {core_honeycomb}"></span>Honeycomb
                            </div>
                            <div class="checkbox-item">
                                <span class="checkbox {core_tubular}"></span>Solid Tubular Core
                            </div>
                            <div class="checkbox-item">
                                <span class="checkbox {core_timber}"></span>Solid Timber
                            </div>
                            <div class="checkbox-item">
                                <span class="checkbox {core_metal}"></span>Metal Skeleton
                            </div>
                        </div>
                    </td>
                    <td>
                        <div class="checkbox-section">
                            <div class="checkbox-item">
                                <span class="checkbox {edging_na}"></span>NA Lipping
                            </div>
                            <div class="checkbox-item">
                                <span class="checkbox {edging_abs}"></span>ABS Edging
                            </div>
                            <div class="checkbox-item">
                                <span class="checkbox {edging_no}"></span>No Edging
                            </div>
                        </div>
                    </td>
                    <td>
                        <div class="checkbox-section">
                            <div class="checkbox-item">
                                <span class="checkbox {decorative_tbar}"></span>T-bar
                            </div>
                            <div class="checkbox-item">
                                <span class="checkbox {decorative_groove}"></span>Groove Line
                            </div>
                        </div>
                    </td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>
                
                <!-- Empty rows 2-4 -->
                <tr class="item-row">
                    <td style="text-align: center;">2</td>
                    <td></td>
                    <td>
                        <div class="checkbox-section">
                            <div class="checkbox-item"><span class="checkbox"></span>37mm</div>
                            <div class="checkbox-item"><span class="checkbox"></span>43mm</div>
                            <div class="checkbox-item"><span class="checkbox"></span>46mm</div>
                            <div class="checkbox-item"><span class="checkbox"></span>Others:</div>
                        </div>
                    </td>
                    <td style="text-align: center;">
                        <div class="circle-number">②</div>
                        <div class="location-text">Location :</div>
                    </td>
                    <td>
                        <div class="checkbox-section">
                            <div class="checkbox-item"><span class="checkbox"></span>S/L</div>
                            <div class="checkbox-item"><span class="checkbox"></span>D/L</div>
                            <div class="checkbox-item"><span class="checkbox"></span>Unequal D/L</div>
                            <div class="checkbox-item"><span class="checkbox"></span>Others:</div>
                        </div>
                    </td>
                    <td>
                        <div class="checkbox-section">
                            <div class="checkbox-item"><span class="checkbox"></span>Honeycomb</div>
                            <div class="checkbox-item"><span class="checkbox"></span>Solid Tubular Core</div>
                            <div class="checkbox-item"><span class="checkbox"></span>Solid Timber</div>
                            <div class="checkbox-item"><span class="checkbox"></span>Metal Skeleton</div>
                        </div>
                    </td>
                    <td>
                        <div class="checkbox-section">
                            <div class="checkbox-item"><span class="checkbox"></span>NA Lipping</div>
                            <div class="checkbox-item"><span class="checkbox"></span>ABS Edging</div>
                            <div class="checkbox-item"><span class="checkbox"></span>No Edging</div>
                        </div>
                    </td>
                    <td>
                        <div class="checkbox-section">
                            <div class="checkbox-item"><span class="checkbox"></span>T-bar</div>
                            <div class="checkbox-item"><span class="checkbox"></span>Groove Line</div>
                        </div>
                    </td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>
                
                <tr class="item-row">
                    <td style="text-align: center;">3</td>
                    <td></td>
                    <td>
                        <div class="checkbox-section">
                            <div class="checkbox-item"><span class="checkbox"></span>37mm</div>
                            <div class="checkbox-item"><span class="checkbox"></span>43mm</div>
                            <div class="checkbox-item"><span class="checkbox"></span>46mm</div>
                            <div class="checkbox-item"><span class="checkbox"></span>Others:</div>
                        </div>
                    </td>
                    <td style="text-align: center;">
                        <div class="circle-number">③</div>
                        <div class="location-text">Location :</div>
                    </td>
                    <td>
                        <div class="checkbox-section">
                            <div class="checkbox-item"><span class="checkbox"></span>S/L</div>
                            <div class="checkbox-item"><span class="checkbox"></span>D/L</div>
                            <div class="checkbox-item"><span class="checkbox"></span>Unequal D/L</div>
                            <div class="checkbox-item"><span class="checkbox"></span>Others:</div>
                        </div>
                    </td>
                    <td>
                        <div class="checkbox-section">
                            <div class="checkbox-item"><span class="checkbox"></span>Honeycomb</div>
                            <div class="checkbox-item"><span class="checkbox"></span>Solid Tubular Core</div>
                            <div class="checkbox-item"><span class="checkbox"></span>Solid Timber</div>
                            <div class="checkbox-item"><span class="checkbox"></span>Metal Skeleton</div>
                        </div>
                    </td>
                    <td>
                        <div class="checkbox-section">
                            <div class="checkbox-item"><span class="checkbox"></span>NA Lipping</div>
                            <div class="checkbox-item"><span class="checkbox"></span>ABS Edging</div>
                            <div class="checkbox-item"><span class="checkbox"></span>No Edging</div>
                        </div>
                    </td>
                    <td>
                        <div class="checkbox-section">
                            <div class="checkbox-item"><span class="checkbox"></span>T-bar</div>
                            <div class="checkbox-item"><span class="checkbox"></span>Groove Line</div>
                        </div>
                    </td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>
                
                <tr class="item-row">
                    <td style="text-align: center;">4</td>
                    <td></td>
                    <td>
                        <div class="checkbox-section">
                            <div class="checkbox-item"><span class="checkbox"></span>37mm</div>
                            <div class="checkbox-item"><span class="checkbox"></span>43mm</div>
                            <div class="checkbox-item"><span class="checkbox"></span>46mm</div>
                            <div class="checkbox-item"><span class="checkbox"></span>Others:</div>
                        </div>
                    </td>
                    <td style="text-align: center;">
                        <div class="circle-number">④</div>
                        <div class="location-text">Location :</div>
                    </td>
                    <td>
                        <div class="checkbox-section">
                            <div class="checkbox-item"><span class="checkbox"></span>S/L</div>
                            <div class="checkbox-item"><span class="checkbox"></span>D/L</div>
                            <div class="checkbox-item"><span class="checkbox"></span>Unequal D/L</div>
                            <div class="checkbox-item"><span class="checkbox"></span>Others:</div>
                        </div>
                    </td>
                    <td>
                        <div class="checkbox-section">
                            <div class="checkbox-item"><span class="checkbox"></span>Honeycomb</div>
                            <div class="checkbox-item"><span class="checkbox"></span>Solid Tubular Core</div>
                            <div class="checkbox-item"><span class="checkbox"></span>Solid Timber</div>
                            <div class="checkbox-item"><span class="checkbox"></span>Metal Skeleton</div>
                        </div>
                    </td>
                    <td>
                        <div class="checkbox-section">
                            <div class="checkbox-item"><span class="checkbox"></span>NA Lipping</div>
                            <div class="checkbox-item"><span class="checkbox"></span>ABS Edging</div>
                            <div class="checkbox-item"><span class="checkbox"></span>No Edging</div>
                        </div>
                    </td>
                    <td>
                        <div class="checkbox-section">
                            <div class="checkbox-item"><span class="checkbox"></span>T-bar</div>
                            <div class="checkbox-item"><span class="checkbox"></span>Groove Line</div>
                        </div>
                    </td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>
            </tbody>
        </table>
        
        <div class="footer">
            <div class="footer-row">
                <div class="footer-cell">
                    <div class="signature-label">Prepare by,</div>
                    <div class="signature-line">Sales Executive :</div>
                    <div class="signature-line">Date :</div>
                </div>
                <div class="footer-cell">
                    <div class="signature-label">Checked by,</div>
                    <div class="signature-line">Sales Admin</div>
                    <div class="signature-line">Date :</div>
                </div>
                <div class="footer-cell">
                    <div class="signature-label">Verify by,</div>
                    <div class="signature-line">Production Supervisor :</div>
                    <div class="signature-line">Date :</div>
                </div>
            </div>
        </div>
        
        <div class="version">SGSB (v050625)</div>
    </div>
    
    <!-- FRAME PAGE -->
    <div class="page">
        <div class="header">
            <div class="company-name">SENDORA GROUP SDN BHD (KOTA DAMANSARA)</div>
        </div>
        
        <div class="fields-section">
            <div class="field-row">
                <div class="field-cell">
                    <span class="field-label">Job Order No:</span>
                    <span class="field-value">{job_order_no}</span>
                </div>
                <div class="field-cell">
                    <span class="field-label">Delivery Date:</span>
                    <span class="field-value">{delivery_date}</span>
                </div>
            </div>
            <div class="field-row">
                <div class="field-cell">
                    <span class="field-label">Job Order Date:</span>
                    <span class="field-value">{job_order_date}</span>
                </div>
                <div class="field-cell">
                    <span class="field-label">Customer Name:</span>
                    <span class="field-value">{customer_name}</span>
                </div>
            </div>
            <div class="field-row">
                <div class="field-cell">
                    <span class="field-label">P.O NO:</span>
                    <span class="field-value">{po_no}</span>
                </div>
                <div class="field-cell">
                    <span class="field-label">Measure by:</span>
                    <span class="field-value">{measure_by}</span>
                </div>
            </div>
        </div>
        
        <div class="form-type">FRAME</div>
        
        <table class="main-table">
            <thead>
                <tr>
                    <th style="width: 8mm;">ITEM</th>
                    <th style="width: 25mm;">FRAME LAMINATE CODE</th>
                    <th style="width: 20mm;">FRAME WIDTH</th>
                    <th style="width: 15mm;">REBATED</th>
                    <th style="width: 30mm;">FRAME SIZE</th>
                    <th style="width: 25mm;">INNER OR OUTER</th>
                    <th style="width: 20mm;">FRAME PROFILE</th>
                    <th>DRAWING REMARK</th>
                </tr>
            </thead>
            <tbody>
                <tr class="item-row">
                    <td style="text-align: center;">1</td>
                    <td style="text-align: center;">6S-145</td>
                    <td style="text-align: center;">130~150MM</td>
                    <td style="text-align: center;">49MM</td>
                    <td style="text-align: center;">
                        <div>1428MM x 2348MM</div>
                        <div class="circle-number">①</div>
                        <div class="location-text">Location :</div>
                    </td>
                    <td>
                        <div class="checkbox-section">
                            <div class="checkbox-item">
                                <span class="checkbox checked"></span>INNER
                            </div>
                            <div class="checkbox-item">
                                <span class="checkbox"></span>OUTER
                            </div>
                        </div>
                    </td>
                    <td style="text-align: center;">CH2</td>
                    <td></td>
                </tr>
            </tbody>
        </table>
        
        <div class="footer">
            <div class="footer-row">
                <div class="footer-cell">
                    <div class="signature-label">Prepare by,</div>
                    <div class="signature-line">Sales Executive :</div>
                    <div class="signature-line">Date :</div>
                </div>
                <div class="footer-cell">
                    <div class="signature-label">Checked by,</div>
                    <div class="signature-line">Sales Admin :</div>
                    <div class="signature-line">Date :</div>
                </div>
                <div class="footer-cell">
                    <div class="signature-label">Verify by,</div>
                    <div class="signature-line">Production Supervisor :</div>
                    <div class="signature-line">Date :</div>
                </div>
            </div>
        </div>
        
        <div class="version">SGSB (v050625)</div>
    </div>
</body>
</html>'''
    
    def extract_laminate_code(self, description: str) -> str:
        """Extract laminate code from description"""
        if not description:
            return "6S-A057"
        pattern = r'([0-9]+[A-Z]-[A-Z0-9]+)'
        match = re.search(pattern, description)
        return match.group(1) if match else "6S-A057"
    


# Test the working template generator
if __name__ == "__main__":
    generator = SimpleWorkingTemplate()
    
    test_data = {
        'invoice_number': 'JO-WORKING-001',
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
    
    result = generator.generate_working_jo(test_data)
    print(f"Generated: {result}")