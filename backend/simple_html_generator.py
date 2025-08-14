"""
Simple HTML Job Order Generator
Creates perfect HTML version of your JO that can be printed to PDF
"""

import os
import json
from datetime import datetime
from typing import Dict, Any

class SimpleHTMLJobOrderGenerator:
    """Generate HTML JOs that match your template exactly"""
    
    def __init__(self):
        self.output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'job_orders')
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_simple_html_jo(self, validated_data: Dict[str, Any]) -> str:
        """Generate HTML JO that preserves your exact template format"""
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        html_filename = f"JO_PERFECT_HTML_{timestamp}.html"
        html_path = os.path.join(self.output_dir, html_filename)
        
        # Generate HTML content
        html_content = self.create_perfect_html_template(validated_data)
        
        # Save HTML file
        try:
            with open(html_path, 'w', encoding='utf-8', errors='replace') as f:
                f.write(html_content)
            
            print(f"SUCCESS! Perfect HTML JO generated: {html_filename}")
            print("This HTML preserves your exact JO template format!")
            print("You can:")
            print("1. Open in browser and print to PDF")
            print("2. Use browser's 'Print to PDF' feature") 
            print("3. The layout matches your original template exactly")
            
            return html_path
            
        except Exception as e:
            print(f"Error generating HTML JO: {e}")
            return None
    
    def get_checkbox_class(self, option_value: str, selected_value: str) -> str:
        """Helper to determine if checkbox should be checked"""
        if option_value.lower() in selected_value.lower():
            return "checked"
        return ""
    
    def create_perfect_html_template(self, data: Dict[str, Any]) -> str:
        """Create HTML that exactly matches your JO template"""
        
        # Extract data
        job_order_no = data.get('invoice_number', '')
        job_order_date = data.get('document_date', '')
        po_no = data.get('po_number', '')
        delivery_date = data.get('delivery_date', '')
        customer_name = data.get('customer_name', '')
        measure_by = data.get('measure_by', 'Auto Generated')
        
        # Extract checkbox selections
        door_thickness = data.get('door_thickness', '').lower()
        door_type = data.get('door_type', '').lower()
        door_core = data.get('door_core', '').lower()
        door_edging = data.get('door_edging', '').lower()
        decorative_line = data.get('decorative_line', '').lower()
        
        # Extract first line item
        first_item = self.extract_first_item(data)
        
        # Pre-calculate checkbox classes to avoid f-string issues
        thickness_37_class = self.get_checkbox_class('37', door_thickness)
        thickness_43_class = self.get_checkbox_class('43', door_thickness)
        thickness_48_class = self.get_checkbox_class('48', door_thickness)
        
        type_sl_class = self.get_checkbox_class('s/l', door_type)
        type_dl_class = self.get_checkbox_class('d/l', door_type)
        type_unequal_class = self.get_checkbox_class('unequal', door_type)
        
        core_honeycomb_class = self.get_checkbox_class('honeycomb', door_core)
        core_tubular_class = self.get_checkbox_class('tubular', door_core)
        core_timber_class = self.get_checkbox_class('timber', door_core)
        core_metal_class = self.get_checkbox_class('metal', door_core)
        
        edging_na_class = self.get_checkbox_class('na lipping', door_edging)
        edging_abs_class = self.get_checkbox_class('abs', door_edging)
        edging_no_class = self.get_checkbox_class('no edging', door_edging)
        
        decorative_tbar_class = self.get_checkbox_class('t-bar', decorative_line)
        decorative_groove_class = self.get_checkbox_class('groove', decorative_line)
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sendora Job Order - {job_order_no}</title>
    <style>
        @page {{
            size: A4 landscape;
            margin: 10mm;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: Arial, sans-serif;
            font-size: 10px;
            line-height: 1.2;
            background: white;
            color: black;
        }}
        
        .jo-page {{
            width: 297mm;
            height: 210mm;
            position: relative;
            border: 2px solid #000;
            background: white;
            padding: 8mm;
        }}
        
        /* Header */
        .company-name {{
            position: absolute;
            top: 15mm;
            left: 12mm;
            font-size: 14px;
            font-weight: bold;
        }}
        
        .form-type {{
            position: absolute;
            top: 12mm;
            right: 15mm;
            font-size: 16px;
            font-weight: bold;
            border: 2px solid #000;
            padding: 6px 15px;
        }}
        
        .form-title {{
            position: absolute;
            top: 22mm;
            left: 50%;
            transform: translateX(-50%);
            font-size: 14px;
            font-weight: bold;
            border: 1px solid #000;
            padding: 4px 15px;
        }}
        
        /* Form Fields */
        .field {{
            position: absolute;
            font-size: 11px;
        }}
        
        .field-label {{
            font-weight: bold;
            margin-right: 8px;
        }}
        
        .field-value {{
            border-bottom: 1px solid #333;
            min-width: 100px;
            display: inline-block;
            padding-bottom: 1px;
        }}
        
        /* Left column */
        .job-order-no {{ top: 40mm; left: 12mm; }}
        .job-order-date {{ top: 48mm; left: 12mm; }}
        .po-no {{ top: 56mm; left: 12mm; }}
        
        /* Right column */
        .delivery-date {{ top: 40mm; right: 15mm; }}
        .customer-name {{ top: 48mm; right: 15mm; }}
        .measure-by {{ top: 56mm; right: 15mm; }}
        
        /* Table */
        .jo-table {{
            position: absolute;
            top: 70mm;
            left: 12mm;
            right: 12mm;
            border-collapse: collapse;
            width: calc(100% - 24mm);
        }}
        
        .jo-table th,
        .jo-table td {{
            border: 1px solid #000;
            padding: 3px 2px;
            text-align: center;
            vertical-align: top;
            font-size: 9px;
        }}
        
        .jo-table th {{
            background: #f5f5f5;
            font-weight: bold;
            height: 12mm;
            line-height: 1.1;
        }}
        
        .data-row {{
            height: 25mm;
        }}
        
        /* Column widths */
        .col-item {{ width: 8%; }}
        .col-laminate {{ width: 12%; }}
        .col-thickness {{ width: 10%; }}
        .col-size {{ width: 12%; }}
        .col-type {{ width: 10%; }}
        .col-core {{ width: 12%; }}
        .col-edging {{ width: 10%; }}
        .col-decorative {{ width: 10%; }}
        .col-design {{ width: 8%; }}
        .col-hole {{ width: 8%; }}
        
        /* Checkboxes */
        .checkbox-container {{
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            gap: 1px;
            font-size: 7px;
            padding: 1px;
        }}
        
        .checkbox-item {{
            display: flex;
            align-items: center;
            gap: 2px;
            width: 100%;
        }}
        
        .checkbox {{
            width: 7px;
            height: 7px;
            border: 1px solid #000;
            display: inline-block;
            position: relative;
            flex-shrink: 0;
        }}
        
        .checkbox.checked::after {{
            content: '✓';
            position: absolute;
            top: -1px;
            left: 0px;
            font-size: 6px;
            font-weight: bold;
        }}
        
        .checkbox-label {{
            font-size: 6px;
            white-space: nowrap;
        }}
        
        /* Footer */
        .footer {{
            position: absolute;
            bottom: 15mm;
            left: 12mm;
            right: 12mm;
            height: 25mm;
        }}
        
        .signature-section {{
            position: absolute;
            width: 85mm;
            font-size: 9px;
        }}
        
        .signature-section.left {{ left: 0; }}
        .signature-section.center {{ left: 50%; transform: translateX(-50%); }}
        .signature-section.right {{ right: 0; }}
        
        .signature-label {{
            font-weight: bold;
            margin-bottom: 12px;
        }}
        
        .signature-role {{
            font-size: 8px;
            color: #666;
            margin-bottom: 3px;
        }}
        
        .signature-date {{
            font-size: 8px;
            color: #666;
        }}
        
        .location-field {{
            position: absolute;
            bottom: 2px;
            left: 2px;
            font-size: 6px;
            color: #666;
        }}
        
        @media print {{
            body {{ margin: 0; }}
            .jo-page {{ margin: 0; }}
        }}
    </style>
</head>
<body>
    <div class="jo-page">
        <!-- Header -->
        <div class="company-name">SENDORA GROUP SDN BHD (HQ)</div>
        <div class="form-type">JOB ORDER</div>
        <div class="form-title">DOOR</div>
        
        <!-- Form Fields -->
        <div class="field job-order-no">
            <span class="field-label">Job Order No:</span>
            <span class="field-value">{job_order_no}</span>
        </div>
        <div class="field job-order-date">
            <span class="field-label">Job Order Date:</span>
            <span class="field-value">{job_order_date}</span>
        </div>
        <div class="field po-no">
            <span class="field-label">PO NO:</span>
            <span class="field-value">{po_no}</span>
        </div>
        <div class="field delivery-date">
            <span class="field-label">Delivery Date:</span>
            <span class="field-value">{delivery_date}</span>
        </div>
        <div class="field customer-name">
            <span class="field-label">Customer Name:</span>
            <span class="field-value">{customer_name}</span>
        </div>
        <div class="field measure-by">
            <span class="field-label">Measure By:</span>
            <span class="field-value">{measure_by}</span>
        </div>
        
        <!-- Table -->
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
                    <th>DRAWING /<br>REMARK</th>
                </tr>
            </thead>
            <tbody>
                <!-- Row 1 -->
                <tr class="data-row">
                    <td>1</td>
                    <td style="position: relative;">
                        {first_item['laminate_code']}
                        <div class="location-field">Location: 1</div>
                    </td>
                    <td>
                        <div class="checkbox-container">
                            <div class="checkbox-item">
                                <span class="checkbox {thickness_37_class}"></span>
                                <span class="checkbox-label">37mm</span>
                            </div>
                            <div class="checkbox-item">
                                <span class="checkbox {thickness_43_class}"></span>
                                <span class="checkbox-label">43mm</span>
                            </div>
                            <div class="checkbox-item">
                                <span class="checkbox {thickness_48_class}"></span>
                                <span class="checkbox-label">48mm</span>
                            </div>
                            <div class="checkbox-item">
                                <span class="checkbox"></span>
                                <span class="checkbox-label">Others:</span>
                            </div>
                        </div>
                    </td>
                    <td>{first_item['size']}</td>
                    <td>
                        <div class="checkbox-container">
                            <div class="checkbox-item">
                                <span class="checkbox {type_sl_class}"></span>
                                <span class="checkbox-label">S/L</span>
                            </div>
                            <div class="checkbox-item">
                                <span class="checkbox {type_dl_class}"></span>
                                <span class="checkbox-label">D/L</span>
                            </div>
                            <div class="checkbox-item">
                                <span class="checkbox {type_unequal_class}"></span>
                                <span class="checkbox-label">Unequal D/L</span>
                            </div>
                            <div class="checkbox-item">
                                <span class="checkbox"></span>
                                <span class="checkbox-label">Others:</span>
                            </div>
                        </div>
                    </td>
                    <td>
                        <div class="checkbox-container">
                            <div class="checkbox-item">
                                <span class="checkbox {'checked' if 'honeycomb' in door_core else ''}"></span>
                                <span class="checkbox-label">Honeycomb</span>
                            </div>
                            <div class="checkbox-item">
                                <span class="checkbox {'checked' if 'tubular' in door_core else ''}"></span>
                                <span class="checkbox-label">Solid Tubular Core</span>
                            </div>
                            <div class="checkbox-item">
                                <span class="checkbox {'checked' if 'timber' in door_core else ''}"></span>
                                <span class="checkbox-label">Solid Timber</span>
                            </div>
                            <div class="checkbox-item">
                                <span class="checkbox {'checked' if 'metal' in door_core else ''}"></span>
                                <span class="checkbox-label">Metal Skeleton</span>
                            </div>
                        </div>
                    </td>
                    <td>
                        <div class="checkbox-container">
                            <div class="checkbox-item">
                                <span class="checkbox {'checked' if 'na lipping' in door_edging else ''}"></span>
                                <span class="checkbox-label">NA Lipping</span>
                            </div>
                            <div class="checkbox-item">
                                <span class="checkbox {'checked' if 'abs' in door_edging else ''}"></span>
                                <span class="checkbox-label">ABS Edging</span>
                            </div>
                            <div class="checkbox-item">
                                <span class="checkbox {'checked' if 'no edging' in door_edging else ''}"></span>
                                <span class="checkbox-label">No Edging</span>
                            </div>
                        </div>
                    </td>
                    <td>
                        <div class="checkbox-container">
                            <div class="checkbox-item">
                                <span class="checkbox {'checked' if 't-bar' in decorative_line or 'tbar' in decorative_line else ''}"></span>
                                <span class="checkbox-label">T-bar</span>
                            </div>
                            <div class="checkbox-item">
                                <span class="checkbox {'checked' if 'groove' in decorative_line else ''}"></span>
                                <span class="checkbox-label">Groove Line</span>
                            </div>
                        </div>
                    </td>
                    <td>{first_item['design_name']}</td>
                    <td></td>
                    <td></td>
                </tr>
                
                <!-- Empty rows 2-4 -->
                <tr class="data-row">
                    <td></td>
                    <td style="position: relative;"><div class="location-field">Location: 2</div></td>
                    <td><div class="checkbox-container">
                        <div class="checkbox-item"><span class="checkbox"></span><span class="checkbox-label">37mm</span></div>
                        <div class="checkbox-item"><span class="checkbox"></span><span class="checkbox-label">43mm</span></div>
                        <div class="checkbox-item"><span class="checkbox"></span><span class="checkbox-label">48mm</span></div>
                        <div class="checkbox-item"><span class="checkbox"></span><span class="checkbox-label">Others:</span></div>
                    </div></td>
                    <td></td>
                    <td><div class="checkbox-container">
                        <div class="checkbox-item"><span class="checkbox"></span><span class="checkbox-label">S/L</span></div>
                        <div class="checkbox-item"><span class="checkbox"></span><span class="checkbox-label">D/L</span></div>
                        <div class="checkbox-item"><span class="checkbox"></span><span class="checkbox-label">Unequal D/L</span></div>
                        <div class="checkbox-item"><span class="checkbox"></span><span class="checkbox-label">Others:</span></div>
                    </div></td>
                    <td><div class="checkbox-container">
                        <div class="checkbox-item"><span class="checkbox"></span><span class="checkbox-label">Honeycomb</span></div>
                        <div class="checkbox-item"><span class="checkbox"></span><span class="checkbox-label">Solid Tubular Core</span></div>
                        <div class="checkbox-item"><span class="checkbox"></span><span class="checkbox-label">Solid Timber</span></div>
                        <div class="checkbox-item"><span class="checkbox"></span><span class="checkbox-label">Metal Skeleton</span></div>
                    </div></td>
                    <td><div class="checkbox-container">
                        <div class="checkbox-item"><span class="checkbox"></span><span class="checkbox-label">NA Lipping</span></div>
                        <div class="checkbox-item"><span class="checkbox"></span><span class="checkbox-label">ABS Edging</span></div>
                        <div class="checkbox-item"><span class="checkbox"></span><span class="checkbox-label">No Edging</span></div>
                    </div></td>
                    <td><div class="checkbox-container">
                        <div class="checkbox-item"><span class="checkbox"></span><span class="checkbox-label">T-bar</span></div>
                        <div class="checkbox-item"><span class="checkbox"></span><span class="checkbox-label">Groove Line</span></div>
                    </div></td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>
                
                <tr class="data-row">
                    <td></td>
                    <td style="position: relative;"><div class="location-field">Location: 3</div></td>
                    <td><div class="checkbox-container">
                        <div class="checkbox-item"><span class="checkbox"></span><span class="checkbox-label">37mm</span></div>
                        <div class="checkbox-item"><span class="checkbox"></span><span class="checkbox-label">43mm</span></div>
                        <div class="checkbox-item"><span class="checkbox"></span><span class="checkbox-label">48mm</span></div>
                        <div class="checkbox-item"><span class="checkbox"></span><span class="checkbox-label">Others:</span></div>
                    </div></td>
                    <td></td>
                    <td><div class="checkbox-container">
                        <div class="checkbox-item"><span class="checkbox"></span><span class="checkbox-label">S/L</span></div>
                        <div class="checkbox-item"><span class="checkbox"></span><span class="checkbox-label">D/L</span></div>
                        <div class="checkbox-item"><span class="checkbox"></span><span class="checkbox-label">Unequal D/L</span></div>
                        <div class="checkbox-item"><span class="checkbox"></span><span class="checkbox-label">Others:</span></div>
                    </div></td>
                    <td><div class="checkbox-container">
                        <div class="checkbox-item"><span class="checkbox"></span><span class="checkbox-label">Honeycomb</span></div>
                        <div class="checkbox-item"><span class="checkbox"></span><span class="checkbox-label">Solid Tubular Core</span></div>
                        <div class="checkbox-item"><span class="checkbox"></span><span class="checkbox-label">Solid Timber</span></div>
                        <div class="checkbox-item"><span class="checkbox"></span><span class="checkbox-label">Metal Skeleton</span></div>
                    </div></td>
                    <td><div class="checkbox-container">
                        <div class="checkbox-item"><span class="checkbox"></span><span class="checkbox-label">NA Lipping</span></div>
                        <div class="checkbox-item"><span class="checkbox"></span><span class="checkbox-label">ABS Edging</span></div>
                        <div class="checkbox-item"><span class="checkbox"></span><span class="checkbox-label">No Edging</span></div>
                    </div></td>
                    <td><div class="checkbox-container">
                        <div class="checkbox-item"><span class="checkbox"></span><span class="checkbox-label">T-bar</span></div>
                        <div class="checkbox-item"><span class="checkbox"></span><span class="checkbox-label">Groove Line</span></div>
                    </div></td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>
                
                <tr class="data-row">
                    <td></td>
                    <td style="position: relative;"><div class="location-field">Location: 4</div></td>
                    <td><div class="checkbox-container">
                        <div class="checkbox-item"><span class="checkbox"></span><span class="checkbox-label">37mm</span></div>
                        <div class="checkbox-item"><span class="checkbox"></span><span class="checkbox-label">43mm</span></div>
                        <div class="checkbox-item"><span class="checkbox"></span><span class="checkbox-label">48mm</span></div>
                        <div class="checkbox-item"><span class="checkbox"></span><span class="checkbox-label">Others:</span></div>
                    </div></td>
                    <td></td>
                    <td><div class="checkbox-container">
                        <div class="checkbox-item"><span class="checkbox"></span><span class="checkbox-label">S/L</span></div>
                        <div class="checkbox-item"><span class="checkbox"></span><span class="checkbox-label">D/L</span></div>
                        <div class="checkbox-item"><span class="checkbox"></span><span class="checkbox-label">Unequal D/L</span></div>
                        <div class="checkbox-item"><span class="checkbox"></span><span class="checkbox-label">Others:</span></div>
                    </div></td>
                    <td><div class="checkbox-container">
                        <div class="checkbox-item"><span class="checkbox"></span><span class="checkbox-label">Honeycomb</span></div>
                        <div class="checkbox-item"><span class="checkbox"></span><span class="checkbox-label">Solid Tubular Core</span></div>
                        <div class="checkbox-item"><span class="checkbox"></span><span class="checkbox-label">Solid Timber</span></div>
                        <div class="checkbox-item"><span class="checkbox"></span><span class="checkbox-label">Metal Skeleton</span></div>
                    </div></td>
                    <td><div class="checkbox-container">
                        <div class="checkbox-item"><span class="checkbox"></span><span class="checkbox-label">NA Lipping</span></div>
                        <div class="checkbox-item"><span class="checkbox"></span><span class="checkbox-label">ABS Edging</span></div>
                        <div class="checkbox-item"><span class="checkbox"></span><span class="checkbox-label">No Edging</span></div>
                    </div></td>
                    <td><div class="checkbox-container">
                        <div class="checkbox-item"><span class="checkbox"></span><span class="checkbox-label">T-bar</span></div>
                        <div class="checkbox-item"><span class="checkbox"></span><span class="checkbox-label">Groove Line</span></div>
                    </div></td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>
            </tbody>
        </table>
        
        <!-- Footer -->
        <div class="footer">
            <div class="signature-section left">
                <div class="signature-label">Prepare by,</div>
                <div class="signature-role">Sales Executive :</div>
                <div class="signature-date">Date :</div>
            </div>
            <div class="signature-section center">
                <div class="signature-label">Checked by,</div>
                <div class="signature-role">Sales Admin</div>
                <div class="signature-date">Date :</div>
            </div>
            <div class="signature-section right">
                <div class="signature-label">Verify by,</div>
                <div class="signature-role">Production Supervisor :</div>
                <div class="signature-date">Date :</div>
            </div>
        </div>
    </div>
</body>
</html>"""
    
    def extract_first_item(self, data: Dict[str, Any]) -> Dict[str, str]:
        """Extract first line item"""
        first_item = {
            'laminate_code': '',
            'size': '',
            'design_name': ''
        }
        
        # Look for first item
        for i in range(10):
            desc_key = f'item_desc_{i}'
            if desc_key in data and data[desc_key]:
                description = data[desc_key]
                
                # Extract laminate code from description
                import re
                pattern = r'([0-9]+[A-Z]-[A-Z0-9]+)'
                match = re.search(pattern, description)
                if match:
                    first_item['laminate_code'] = match.group(1)
                
                # Get size
                first_item['size'] = data.get(f'item_size_{i}', '')
                
                # Get design name if available
                first_item['design_name'] = data.get(f'item_design_{i}', '')
                
                break
        
        return first_item


# Test the simple HTML generator
if __name__ == "__main__":
    generator = SimpleHTMLJobOrderGenerator()
    
    # Test data
    test_data = {
        'invoice_number': 'KDI-2507-003',
        'customer_name': 'SENDORA GROUP SDN BHD',
        'document_date': '2025-08-14',
        'delivery_date': '2025-08-20',
        'po_number': 'PO-2025-001',
        'door_thickness': '43mm',
        'door_type': 'S/L',
        'door_core': 'solid tubular core',
        'door_edging': 'na lipping',
        'decorative_line': 't-bar',
        'item_desc_0': '6S-A057 DOOR 43MM x 850MM x 2100MM',
        'item_size_0': '850MM x 2100MM'
    }
    
    result = generator.generate_simple_html_jo(test_data)
    print(f"Generated: {result}")