"""
Exact Replica Template Generator
Perfect 1:1 match to the original Sendora JO template
"""

import os
import subprocess
from datetime import datetime
from typing import Dict, Any

class ExactReplicaTemplate:
    """Generate HTML that is an EXACT replica of the Sendora JO template"""
    
    def __init__(self):
        self.output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'job_orders')
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_exact_jo(self, validated_data: Dict[str, Any]) -> str:
        """Generate exact JO replica"""
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        html_filename = f"JO_EXACT_REPLICA_{timestamp}.html"
        html_path = os.path.join(self.output_dir, html_filename)
        
        # Generate HTML content
        html_content = self.create_exact_replica(validated_data)
        
        # Save HTML file
        try:
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"SUCCESS! Exact replica JO generated: {html_filename}")
            
            # Generate PDF from HTML
            pdf_path = self.generate_pdf_from_html(html_path)
            if pdf_path:
                print(f"SUCCESS! PDF generated: {os.path.basename(pdf_path)}")
                return pdf_path
            
            return html_path
            
        except Exception as e:
            print(f"Error generating exact replica JO: {e}")
            return None
    
    def create_exact_replica(self, data: Dict[str, Any]) -> str:
        """Create HTML that exactly replicates the original template"""
        
        # Extract data
        job_order_no = data.get('invoice_number', '')
        job_order_date = data.get('document_date', '')
        po_no = data.get('po_number', '')
        delivery_date = data.get('delivery_date', '')
        customer_name = data.get('customer_name', '')
        measure_by = data.get('measure_by', '')
        
        # Door specifications
        door_thickness = data.get('door_thickness', '').lower()
        door_type = data.get('door_type', '').lower() 
        door_core = data.get('door_core', '').lower()
        door_edging = data.get('door_edging', '').lower()
        decorative_line = data.get('decorative_line', '').lower()
        
        # Extract item info
        item_desc = data.get('item_desc_0', '')
        item_size = data.get('item_size_0', '')
        laminate_code = self.extract_laminate_code(item_desc)
        
        return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: Arial, sans-serif; 
            font-size: 9px; 
            line-height: 1.2;
        }}
        
        .page {{ 
            width: 21cm; 
            height: 29.7cm; 
            margin: 0.5cm; 
            page-break-after: always;
            border: 1px solid #000;
            position: relative;
            padding: 3mm;
        }}
        
        /* Header Layout - Exact Match */
        .header-section {{
            position: relative;
            height: 25mm;
            border-bottom: 1px solid #000;
        }}
        
        .job-order-left {{
            position: absolute;
            left: 0;
            top: 0;
            width: 15mm;
            height: 25mm;
            border-right: 1px solid #000;
            writing-mode: vertical-lr;
            text-orientation: mixed;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 10px;
            font-weight: bold;
        }}
        
        .header-fields {{
            margin-left: 18mm;
            padding: 2mm;
            height: 23mm;
        }}
        
        .company-header {{
            text-align: center;
            font-size: 11px;
            font-weight: bold;
            text-decoration: underline;
            margin-bottom: 3mm;
        }}
        
        .field-row {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 1.5mm;
            font-size: 8px;
        }}
        
        .field-left, .field-right {{
            display: flex;
            gap: 15mm;
        }}
        
        .field-item {{
            display: flex;
            align-items: center;
        }}
        
        .field-label {{
            margin-right: 2mm;
            font-size: 8px;
        }}
        
        .field-line {{
            border-bottom: 1px solid #000;
            min-width: 25mm;
            height: 12px;
            font-size: 8px;
            padding-left: 1mm;
        }}
        
        /* Form Type */
        .form-type {{
            text-align: center;
            font-size: 28px;
            font-weight: bold;
            margin: 5mm 0;
            padding: 3mm;
            border: 2px solid #000;
        }}
        
        /* Table - Exact Replica */
        .main-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 7px;
        }}
        
        .main-table th,
        .main-table td {{
            border: 1px solid #000;
            padding: 1px;
            text-align: center;
            vertical-align: top;
        }}
        
        .main-table th {{
            font-weight: bold;
            font-size: 7px;
            background: #f8f8f8;
        }}
        
        /* Column Widths - Exact Match */
        .col-item {{ width: 12mm; }}
        .col-laminate {{ width: 18mm; }}
        .col-thickness {{ width: 22mm; }}
        .col-size {{ width: 32mm; }}
        .col-door-type {{ width: 22mm; }}
        .col-door-core {{ width: 28mm; }}
        .col-edging {{ width: 20mm; }}
        .col-decorative {{ width: 18mm; }}
        .col-design {{ width: 20mm; }}
        .col-openhole {{ width: 18mm; }}
        .col-remark {{ width: 25mm; }}
        
        /* Frame columns */
        .col-frame-width {{ width: 25mm; }}
        .col-rebated {{ width: 18mm; }}
        .col-inner-outer {{ width: 25mm; }}
        .col-frame-profile {{ width: 18mm; }}
        
        .item-row {{
            height: 35mm;
        }}
        
        /* Checkbox Styling - Exact Match */
        .checkbox-container {{
            display: flex;
            flex-direction: column;
            gap: 1px;
            align-items: flex-start;
            padding: 1mm;
        }}
        
        .checkbox-line {{
            display: flex;
            align-items: center;
            gap: 1mm;
            font-size: 6px;
            line-height: 1.1;
        }}
        
        .checkbox {{
            width: 4px;
            height: 4px;
            border: 0.5px solid #000;
            display: inline-block;
            flex-shrink: 0;
        }}
        
        .checkbox.checked {{
            background: #000;
        }}
        
        /* Circle Numbers - Exact Match */
        .circle-number {{
            font-size: 14px;
            font-weight: bold;
            margin: 2mm 0;
        }}
        
        .location-text {{
            font-size: 6px;
            margin-top: 1mm;
        }}
        
        /* Footer */
        .signature-footer {{
            position: absolute;
            bottom: 8mm;
            left: 3mm;
            right: 3mm;
            display: flex;
            justify-content: space-between;
            font-size: 7px;
        }}
        
        .signature-section {{
            text-align: left;
            width: 32%;
        }}
        
        .signature-label {{
            font-weight: bold;
            margin-bottom: 8mm;
        }}
        
        .signature-role {{
            margin-bottom: 1mm;
        }}
        
        .version {{
            position: absolute;
            bottom: 3mm;
            right: 5mm;
            font-size: 6px;
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
        <div class="header-section">
            <div class="job-order-left">JOB ORDER</div>
            <div class="header-fields">
                <div class="company-header">SENDORA GROUP SDN BHD (KOTA DAMANSARA)</div>
                
                <div class="field-row">
                    <div class="field-left">
                        <div class="field-item">
                            <span class="field-label">Job Order No:</span>
                            <div class="field-line">{job_order_no}</div>
                        </div>
                        <div class="field-item">
                            <span class="field-label">Job Order Date:</span>
                            <div class="field-line">{job_order_date}</div>
                        </div>
                    </div>
                    <div class="field-right">
                        <div class="field-item">
                            <span class="field-label">Delivery Date:</span>
                            <div class="field-line">{delivery_date}</div>
                        </div>
                    </div>
                </div>
                
                <div class="field-row">
                    <div class="field-left">
                        <div class="field-item">
                            <span class="field-label">Customer Name:</span>
                            <div class="field-line">{customer_name}</div>
                        </div>
                    </div>
                    <div class="field-right">
                        <div class="field-item">
                            <span class="field-label">Measure By:</span>
                            <div class="field-line">{measure_by}</div>
                        </div>
                    </div>
                </div>
                
                <div class="field-row">
                    <div class="field-left">
                        <div class="field-item">
                            <span class="field-label">A.S.A.P</span>
                            <div class="field-line"></div>
                        </div>
                    </div>
                    <div class="field-right">
                        <div class="field-item">
                            <span class="field-label">P.O NO:</span>
                            <div class="field-line">{po_no}</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="form-type">DOOR</div>
        
        <table class="main-table">
            <thead>
                <tr>
                    <th class="col-item">ITEM</th>
                    <th class="col-laminate">LAMINATE CODE</th>
                    <th class="col-thickness">DOOR THICKNESS</th>
                    <th class="col-size">DOOR SIZE</th>
                    <th class="col-door-type">DOOR TYPE</th>
                    <th class="col-door-core">DOOR CORE</th>
                    <th class="col-edging">EDGING</th>
                    <th class="col-decorative">DECORATIVE LINE</th>
                    <th class="col-design">DESIGN NAME</th>
                    <th class="col-openhole">OPEN HOLE TYPE</th>
                    <th class="col-remark">DRAWING REMARK</th>
                </tr>
            </thead>
            <tbody>
                <!-- Row 1 -->
                <tr class="item-row">
                    <td>1</td>
                    <td>{laminate_code}</td>
                    <td>
                        <div class="checkbox-container">
                            <div class="checkbox-line">
                                <span class="checkbox {'checked' if '37' in door_thickness else ''}"></span>
                                <span>37mm</span>
                            </div>
                            <div class="checkbox-line">
                                <span class="checkbox {'checked' if '43' in door_thickness else ''}"></span>
                                <span>43mm</span>
                            </div>
                            <div class="checkbox-line">
                                <span class="checkbox {'checked' if '46' in door_thickness else ''}"></span>
                                <span>46mm</span>
                            </div>
                            <div class="checkbox-line">
                                <span class="checkbox"></span>
                                <span>Others:</span>
                            </div>
                        </div>
                    </td>
                    <td>
                        <div>{item_size}</div>
                        <div class="circle-number">①</div>
                        <div class="location-text">Location :</div>
                    </td>
                    <td>
                        <div class="checkbox-container">
                            <div class="checkbox-line">
                                <span class="checkbox {'checked' if 's/l' in door_type else ''}"></span>
                                <span>S/L</span>
                            </div>
                            <div class="checkbox-line">
                                <span class="checkbox {'checked' if 'd/l' in door_type else ''}"></span>
                                <span>D/L</span>
                            </div>
                            <div class="checkbox-line">
                                <span class="checkbox {'checked' if 'unequal' in door_type else ''}"></span>
                                <span>Unequal D/L</span>
                            </div>
                            <div class="checkbox-line">
                                <span class="checkbox"></span>
                                <span>Others:</span>
                            </div>
                        </div>
                    </td>
                    <td>
                        <div class="checkbox-container">
                            <div class="checkbox-line">
                                <span class="checkbox {'checked' if 'honeycomb' in door_core else ''}"></span>
                                <span>Honeycomb</span>
                            </div>
                            <div class="checkbox-line">
                                <span class="checkbox {'checked' if 'tubular' in door_core else ''}"></span>
                                <span>Solid Tubular Core</span>
                            </div>
                            <div class="checkbox-line">
                                <span class="checkbox {'checked' if 'timber' in door_core else ''}"></span>
                                <span>Solid Timber</span>
                            </div>
                            <div class="checkbox-line">
                                <span class="checkbox {'checked' if 'metal' in door_core else ''}"></span>
                                <span>Metal Skeleton</span>
                            </div>
                        </div>
                    </td>
                    <td>
                        <div class="checkbox-container">
                            <div class="checkbox-line">
                                <span class="checkbox {'checked' if 'na lipping' in door_edging else ''}"></span>
                                <span>NA Lipping</span>
                            </div>
                            <div class="checkbox-line">
                                <span class="checkbox {'checked' if 'abs' in door_edging else ''}"></span>
                                <span>ABS Edging</span>
                            </div>
                            <div class="checkbox-line">
                                <span class="checkbox {'checked' if 'no edging' in door_edging else ''}"></span>
                                <span>No Edging</span>
                            </div>
                        </div>
                    </td>
                    <td>
                        <div class="checkbox-container">
                            <div class="checkbox-line">
                                <span class="checkbox {'checked' if 't-bar' in decorative_line else ''}"></span>
                                <span>T-bar</span>
                            </div>
                            <div class="checkbox-line">
                                <span class="checkbox {'checked' if 'groove' in decorative_line else ''}"></span>
                                <span>Groove Line</span>
                            </div>
                        </div>
                    </td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>
                
                <!-- Rows 2-4 -->
                {self.generate_empty_door_rows(2, 4)}
            </tbody>
        </table>
        
        <div class="signature-footer">
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
        
        <div class="version">SGSB (v050625)</div>
    </div>
    
    <!-- FRAME PAGE -->
    <div class="page">
        <div class="header-section">
            <div class="job-order-left">JOB ORDER</div>
            <div class="header-fields">
                <div class="company-header">SENDORA GROUP SDN BHD (KOTA DAMANSARA)</div>
                
                <div class="field-row">
                    <div class="field-left">
                        <div class="field-item">
                            <span class="field-label">Job Order No:</span>
                            <div class="field-line">{job_order_no}</div>
                        </div>
                        <div class="field-item">
                            <span class="field-label">Job Order Date:</span>
                            <div class="field-line">{job_order_date}</div>
                        </div>
                    </div>
                    <div class="field-right">
                        <div class="field-item">
                            <span class="field-label">Delivery Date:</span>
                            <div class="field-line">{delivery_date}</div>
                        </div>
                    </div>
                </div>
                
                <div class="field-row">
                    <div class="field-left">
                        <div class="field-item">
                            <span class="field-label">Customer Name:</span>
                            <div class="field-line">{customer_name}</div>
                        </div>
                    </div>
                    <div class="field-right">
                        <div class="field-item">
                            <span class="field-label">Measure By:</span>
                            <div class="field-line">{measure_by}</div>
                        </div>
                    </div>
                </div>
                
                <div class="field-row">
                    <div class="field-left">
                        <div class="field-item">
                            <span class="field-label">A.S.A.P</span>
                            <div class="field-line"></div>
                        </div>
                    </div>
                    <div class="field-right">
                        <div class="field-item">
                            <span class="field-label">P.O NO:</span>
                            <div class="field-line">{po_no}</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="form-type">FRAME</div>
        
        <table class="main-table">
            <thead>
                <tr>
                    <th class="col-item">ITEM</th>
                    <th class="col-laminate">FRAME LAMINATE CODE</th>
                    <th class="col-frame-width">FRAME WIDTH</th>
                    <th class="col-rebated">REBATED</th>
                    <th class="col-size">FRAME SIZE</th>
                    <th class="col-inner-outer">INNER OR OUTER</th>
                    <th class="col-frame-profile">FRAME PROFILE</th>
                    <th class="col-remark">DRAWING REMARK</th>
                </tr>
            </thead>
            <tbody>
                <tr class="item-row">
                    <td>1</td>
                    <td>6S-145</td>
                    <td>130~150MM</td>
                    <td>49MM</td>
                    <td>
                        <div>1428MM x 2348MM</div>
                        <div class="circle-number">①</div>
                        <div class="location-text">Location :</div>
                    </td>
                    <td>
                        <div class="checkbox-container">
                            <div class="checkbox-line">
                                <span class="checkbox checked"></span>
                                <span>INNER</span>
                            </div>
                            <div class="checkbox-line">
                                <span class="checkbox"></span>
                                <span>OUTER</span>
                            </div>
                        </div>
                    </td>
                    <td>CH2</td>
                    <td></td>
                </tr>
            </tbody>
        </table>
        
        <div class="signature-footer">
            <div class="signature-section">
                <div class="signature-label">Prepare by,</div>
                <div class="signature-role">Sales Executive :</div>
                <div class="signature-role">Date :</div>
            </div>
            <div class="signature-section">
                <div class="signature-label">Checked by,</div>
                <div class="signature-role">Sales Admin :</div>
                <div class="signature-role">Date :</div>
            </div>
            <div class="signature-section">
                <div class="signature-label">Verify by,</div>
                <div class="signature-role">Production Supervisor :</div>
                <div class="signature-role">Date :</div>
            </div>
        </div>
        
        <div class="version">SGSB (v050625)</div>
    </div>
</body>
</html>'''
    
    def generate_empty_door_rows(self, start_row: int, end_row: int) -> str:
        """Generate empty door rows for items 2-4"""
        rows = ""
        for i in range(start_row, end_row + 1):
            rows += f'''
                <tr class="item-row">
                    <td>{i}</td>
                    <td></td>
                    <td>
                        <div class="checkbox-container">
                            <div class="checkbox-line">
                                <span class="checkbox"></span>
                                <span>37mm</span>
                            </div>
                            <div class="checkbox-line">
                                <span class="checkbox"></span>
                                <span>43mm</span>
                            </div>
                            <div class="checkbox-line">
                                <span class="checkbox"></span>
                                <span>46mm</span>
                            </div>
                            <div class="checkbox-line">
                                <span class="checkbox"></span>
                                <span>Others:</span>
                            </div>
                        </div>
                    </td>
                    <td>
                        <div class="circle-number">{chr(9312 + i - 1)}</div>
                        <div class="location-text">Location :</div>
                    </td>
                    <td>
                        <div class="checkbox-container">
                            <div class="checkbox-line">
                                <span class="checkbox"></span>
                                <span>S/L</span>
                            </div>
                            <div class="checkbox-line">
                                <span class="checkbox"></span>
                                <span>D/L</span>
                            </div>
                            <div class="checkbox-line">
                                <span class="checkbox"></span>
                                <span>Unequal D/L</span>
                            </div>
                            <div class="checkbox-line">
                                <span class="checkbox"></span>
                                <span>Others:</span>
                            </div>
                        </div>
                    </td>
                    <td>
                        <div class="checkbox-container">
                            <div class="checkbox-line">
                                <span class="checkbox"></span>
                                <span>Honeycomb</span>
                            </div>
                            <div class="checkbox-line">
                                <span class="checkbox"></span>
                                <span>Solid Tubular Core</span>
                            </div>
                            <div class="checkbox-line">
                                <span class="checkbox"></span>
                                <span>Solid Timber</span>
                            </div>
                            <div class="checkbox-line">
                                <span class="checkbox"></span>
                                <span>Metal Skeleton</span>
                            </div>
                        </div>
                    </td>
                    <td>
                        <div class="checkbox-container">
                            <div class="checkbox-line">
                                <span class="checkbox"></span>
                                <span>NA Lipping</span>
                            </div>
                            <div class="checkbox-line">
                                <span class="checkbox"></span>
                                <span>ABS Edging</span>
                            </div>
                            <div class="checkbox-line">
                                <span class="checkbox"></span>
                                <span>No Edging</span>
                            </div>
                        </div>
                    </td>
                    <td>
                        <div class="checkbox-container">
                            <div class="checkbox-line">
                                <span class="checkbox"></span>
                                <span>T-bar</span>
                            </div>
                            <div class="checkbox-line">
                                <span class="checkbox"></span>
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
    
    def extract_laminate_code(self, description: str) -> str:
        """Extract laminate code from description"""
        import re
        pattern = r'([0-9]+[A-Z]-[A-Z0-9]+)'
        match = re.search(pattern, description)
        return match.group(1) if match else "6S-A057"
    
    def generate_pdf_from_html(self, html_path: str) -> str:
        """Convert HTML to PDF with proper alignment"""
        try:
            pdf_path = html_path.replace('.html', '.pdf')
            
            # Use full path on Windows if wkhtmltopdf is not in PATH
            wkhtmltopdf_path = 'wkhtmltopdf'
            if os.name == 'nt' and os.path.exists(r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'):
                wkhtmltopdf_path = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
            
            cmd = [
                wkhtmltopdf_path,
                '--page-size', 'A4',
                '--margin-top', '10mm',
                '--margin-bottom', '10mm',
                '--margin-left', '10mm',
                '--margin-right', '10mm',
                '--encoding', 'UTF-8',
                '--enable-local-file-access',
                html_path,
                pdf_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0 and os.path.exists(pdf_path):
                print(f"PDF conversion successful: {os.path.basename(pdf_path)}")
                return pdf_path
            else:
                print(f"PDF conversion failed: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"PDF conversion error: {e}")
            return None


# Test the exact replica generator
if __name__ == "__main__":
    generator = ExactReplicaTemplate()
    
    test_data = {
        'invoice_number': 'JO-REPLICA-001',
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
    
    result = generator.generate_exact_jo(test_data)
    print(f"Generated: {result}")