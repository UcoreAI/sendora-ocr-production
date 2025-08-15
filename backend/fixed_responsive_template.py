"""
Fixed Responsive Template Generator
Addresses alignment issues for Elestio deployment
"""

import os
import subprocess
from datetime import datetime
from typing import Dict, Any
import re

class FixedResponsiveTemplate:
    """Generate properly aligned templates for web and PDF"""
    
    def __init__(self):
        self.output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'job_orders')
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_fixed_jo(self, validated_data: Dict[str, Any]) -> str:
        """Generate JO with proper alignment"""
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        html_filename = f"JO_FIXED_{timestamp}.html"
        html_path = os.path.join(self.output_dir, html_filename)
        
        # Generate responsive HTML
        html_content = self.create_responsive_template(validated_data)
        
        try:
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"SUCCESS! Fixed responsive JO generated: {html_filename}")
            
            # Generate PDF
            pdf_path = self.generate_pdf_from_html(html_path)
            if pdf_path:
                print(f"SUCCESS! PDF generated: {os.path.basename(pdf_path)}")
                return pdf_path
            
            return html_path
            
        except Exception as e:
            print(f"Error generating fixed JO: {e}")
            return None
    
    def create_responsive_template(self, data: Dict[str, Any]) -> str:
        """Create responsive template that works on all devices"""
        
        # Extract data
        job_order_no = data.get('invoice_number', '')
        job_order_date = data.get('document_date', '')
        po_no = data.get('po_number', '')
        delivery_date = data.get('delivery_date', '')
        customer_name = data.get('customer_name', '')
        measure_by = data.get('measure_by', '')
        
        # Get specifications
        door_thickness = data.get('door_thickness', '').lower()
        door_type = data.get('door_type', '').lower() 
        door_core = data.get('door_core', '').lower()
        door_edging = data.get('door_edging', '').lower()
        door_size = data.get('door_size', '') or data.get('item_size_0', '')
        
        # Extract laminate code
        item_desc = data.get('item_desc_0', '')
        laminate_code = self.extract_laminate_code(item_desc)
        
        # Generate checkbox states
        thickness_37 = "✓" if "37" in door_thickness else "☐"
        thickness_43 = "✓" if "43" in door_thickness else "☐"
        thickness_46 = "✓" if "46" in door_thickness else "☐"
        
        type_sl = "✓" if "s/l" in door_type else "☐"
        type_dl = "✓" if "d/l" in door_type and "unequal" not in door_type else "☐"
        type_unequal = "✓" if "unequal" in door_type else "☐"
        
        core_honeycomb = "✓" if "honeycomb" in door_core else "☐"
        core_tubular = "✓" if "tubular" in door_core else "☐"
        core_timber = "✓" if "timber" in door_core else "☐"
        core_metal = "✓" if "metal" in door_core else "☐"
        
        edging_na = "✓" if "na lipping" in door_edging else "☐"
        edging_abs = "✓" if "abs" in door_edging else "☐"
        edging_no = "✓" if "no edging" in door_edging else "☐"
        
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sendora Job Order - {job_order_no}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
            background-color: #f5f5f5;
            color: #333;
            line-height: 1.4;
        }}
        
        .container {{
            max-width: 21cm;
            margin: 0 auto;
            background: white;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }}
        
        .page {{
            width: 100%;
            min-height: 29.7cm;
            padding: 1.5cm;
            page-break-after: always;
            position: relative;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 1.5cm;
            border-bottom: 2px solid #000;
            padding-bottom: 1cm;
        }}
        
        .company-name {{
            font-size: 18px;
            font-weight: bold;
            text-decoration: underline;
            margin-bottom: 0.5cm;
            color: #000;
        }}
        
        .form-info {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1cm;
            margin-bottom: 1cm;
            font-size: 12px;
        }}
        
        .form-field {{
            display: flex;
            align-items: center;
            margin-bottom: 0.5cm;
        }}
        
        .form-label {{
            font-weight: bold;
            width: 40%;
            min-width: 100px;
        }}
        
        .form-value {{
            border-bottom: 1px solid #000;
            flex: 1;
            padding: 0.2cm 0.5cm;
            min-height: 1.2em;
        }}
        
        .form-type {{
            text-align: center;
            font-size: 28px;
            font-weight: bold;
            border: 3px solid #000;
            padding: 1cm;
            margin: 1cm 0;
            background-color: #f8f8f8;
        }}
        
        .specs-table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 1.5cm;
            font-size: 10px;
        }}
        
        .specs-table th {{
            background-color: #e8e8e8;
            border: 1px solid #000;
            padding: 0.5cm;
            text-align: center;
            font-weight: bold;
            font-size: 9px;
        }}
        
        .specs-table td {{
            border: 1px solid #000;
            padding: 0.4cm;
            vertical-align: top;
            min-height: 3cm;
        }}
        
        .item-cell {{
            text-align: center;
            font-weight: bold;
            font-size: 12px;
        }}
        
        .checkbox-group {{
            line-height: 1.8;
        }}
        
        .checkbox-item {{
            margin: 0.2cm 0;
            font-size: 10px;
        }}
        
        .checkbox {{
            font-family: monospace;
            font-size: 14px;
            margin-right: 0.3cm;
            font-weight: bold;
        }}
        
        .door-size {{
            text-align: center;
            font-size: 12px;
            font-weight: bold;
            margin-bottom: 0.5cm;
        }}
        
        .location-number {{
            font-size: 20px;
            font-weight: bold;
            text-align: center;
            margin: 0.3cm 0;
        }}
        
        .location-text {{
            font-size: 9px;
            text-align: center;
            font-style: italic;
        }}
        
        .footer {{
            position: absolute;
            bottom: 1.5cm;
            left: 1.5cm;
            right: 1.5cm;
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 1cm;
            border-top: 1px solid #000;
            padding-top: 0.5cm;
        }}
        
        .signature-section {{
            text-align: center;
            font-size: 10px;
        }}
        
        .signature-title {{
            font-weight: bold;
            margin-bottom: 0.5cm;
        }}
        
        .signature-line {{
            border-bottom: 1px solid #000;
            margin: 0.3cm 0;
            height: 1.5cm;
        }}
        
        .version {{
            position: absolute;
            bottom: 0.5cm;
            right: 1cm;
            font-size: 8px;
            color: #666;
        }}
        
        /* Responsive Design */
        @media screen and (max-width: 768px) {{
            .container {{
                margin: 0;
                box-shadow: none;
            }}
            
            .page {{
                padding: 1cm;
            }}
            
            .form-info {{
                grid-template-columns: 1fr;
                gap: 0.5cm;
            }}
            
            .company-name {{
                font-size: 16px;
            }}
            
            .form-type {{
                font-size: 24px;
                padding: 0.8cm;
            }}
            
            .specs-table {{
                font-size: 8px;
            }}
            
            .specs-table th,
            .specs-table td {{
                padding: 0.2cm;
            }}
            
            .footer {{
                position: static;
                margin-top: 2cm;
                grid-template-columns: 1fr;
                gap: 0.5cm;
            }}
        }}
        
        /* Print Styles */
        @media print {{
            body {{
                background: white;
            }}
            
            .container {{
                box-shadow: none;
                max-width: none;
            }}
            
            .page {{
                page-break-after: always;
            }}
            
            .footer {{
                position: absolute;
                bottom: 1.5cm;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- DOOR PAGE -->
        <div class="page">
            <div class="header">
                <div class="company-name">SENDORA GROUP SDN BHD (KOTA DAMANSARA)</div>
            </div>
            
            <div class="form-info">
                <div>
                    <div class="form-field">
                        <span class="form-label">Job Order No:</span>
                        <span class="form-value">{job_order_no}</span>
                    </div>
                    <div class="form-field">
                        <span class="form-label">Job Order Date:</span>
                        <span class="form-value">{job_order_date}</span>
                    </div>
                    <div class="form-field">
                        <span class="form-label">P.O NO:</span>
                        <span class="form-value">{po_no}</span>
                    </div>
                </div>
                <div>
                    <div class="form-field">
                        <span class="form-label">Delivery Date:</span>
                        <span class="form-value">{delivery_date}</span>
                    </div>
                    <div class="form-field">
                        <span class="form-label">Customer Name:</span>
                        <span class="form-value">{customer_name}</span>
                    </div>
                    <div class="form-field">
                        <span class="form-label">Measure By:</span>
                        <span class="form-value">{measure_by}</span>
                    </div>
                </div>
            </div>
            
            <div class="form-type">DOOR</div>
            
            <table class="specs-table">
                <thead>
                    <tr>
                        <th style="width: 5%;">ITEM</th>
                        <th style="width: 12%;">LAMINATE CODE</th>
                        <th style="width: 15%;">DOOR THICKNESS</th>
                        <th style="width: 15%;">DOOR SIZE</th>
                        <th style="width: 15%;">DOOR TYPE</th>
                        <th style="width: 18%;">DOOR CORE</th>
                        <th style="width: 12%;">EDGING</th>
                        <th style="width: 8%;">REMARKS</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td class="item-cell">1</td>
                        <td style="text-align: center; font-weight: bold;">{laminate_code}</td>
                        <td>
                            <div class="checkbox-group">
                                <div class="checkbox-item">
                                    <span class="checkbox">{thickness_37}</span> 37mm
                                </div>
                                <div class="checkbox-item">
                                    <span class="checkbox">{thickness_43}</span> 43mm
                                </div>
                                <div class="checkbox-item">
                                    <span class="checkbox">{thickness_46}</span> 46mm
                                </div>
                                <div class="checkbox-item">
                                    <span class="checkbox">☐</span> Others:
                                </div>
                            </div>
                        </td>
                        <td>
                            <div class="door-size">{door_size}</div>
                            <div class="location-number">①</div>
                            <div class="location-text">Location:</div>
                        </td>
                        <td>
                            <div class="checkbox-group">
                                <div class="checkbox-item">
                                    <span class="checkbox">{type_sl}</span> S/L
                                </div>
                                <div class="checkbox-item">
                                    <span class="checkbox">{type_dl}</span> D/L
                                </div>
                                <div class="checkbox-item">
                                    <span class="checkbox">{type_unequal}</span> Unequal D/L
                                </div>
                                <div class="checkbox-item">
                                    <span class="checkbox">☐</span> Others:
                                </div>
                            </div>
                        </td>
                        <td>
                            <div class="checkbox-group">
                                <div class="checkbox-item">
                                    <span class="checkbox">{core_honeycomb}</span> Honeycomb
                                </div>
                                <div class="checkbox-item">
                                    <span class="checkbox">{core_tubular}</span> Solid Tubular
                                </div>
                                <div class="checkbox-item">
                                    <span class="checkbox">{core_timber}</span> Solid Timber
                                </div>
                                <div class="checkbox-item">
                                    <span class="checkbox">{core_metal}</span> Metal Skeleton
                                </div>
                            </div>
                        </td>
                        <td>
                            <div class="checkbox-group">
                                <div class="checkbox-item">
                                    <span class="checkbox">{edging_na}</span> NA Lipping
                                </div>
                                <div class="checkbox-item">
                                    <span class="checkbox">{edging_abs}</span> ABS Edging
                                </div>
                                <div class="checkbox-item">
                                    <span class="checkbox">{edging_no}</span> No Edging
                                </div>
                            </div>
                        </td>
                        <td></td>
                    </tr>
                    
                    <!-- Empty rows 2-4 -->
                    <tr>
                        <td class="item-cell">2</td>
                        <td></td>
                        <td>
                            <div class="checkbox-group">
                                <div class="checkbox-item"><span class="checkbox">☐</span> 37mm</div>
                                <div class="checkbox-item"><span class="checkbox">☐</span> 43mm</div>
                                <div class="checkbox-item"><span class="checkbox">☐</span> 46mm</div>
                                <div class="checkbox-item"><span class="checkbox">☐</span> Others:</div>
                            </div>
                        </td>
                        <td>
                            <div class="location-number">②</div>
                            <div class="location-text">Location:</div>
                        </td>
                        <td>
                            <div class="checkbox-group">
                                <div class="checkbox-item"><span class="checkbox">☐</span> S/L</div>
                                <div class="checkbox-item"><span class="checkbox">☐</span> D/L</div>
                                <div class="checkbox-item"><span class="checkbox">☐</span> Unequal D/L</div>
                                <div class="checkbox-item"><span class="checkbox">☐</span> Others:</div>
                            </div>
                        </td>
                        <td>
                            <div class="checkbox-group">
                                <div class="checkbox-item"><span class="checkbox">☐</span> Honeycomb</div>
                                <div class="checkbox-item"><span class="checkbox">☐</span> Solid Tubular</div>
                                <div class="checkbox-item"><span class="checkbox">☐</span> Solid Timber</div>
                                <div class="checkbox-item"><span class="checkbox">☐</span> Metal Skeleton</div>
                            </div>
                        </td>
                        <td>
                            <div class="checkbox-group">
                                <div class="checkbox-item"><span class="checkbox">☐</span> NA Lipping</div>
                                <div class="checkbox-item"><span class="checkbox">☐</span> ABS Edging</div>
                                <div class="checkbox-item"><span class="checkbox">☐</span> No Edging</div>
                            </div>
                        </td>
                        <td></td>
                    </tr>
                </tbody>
            </table>
            
            <div class="footer">
                <div class="signature-section">
                    <div class="signature-title">Prepared by,</div>
                    <div class="signature-line"></div>
                    <div>Sales Executive</div>
                    <div>Date: ___________</div>
                </div>
                <div class="signature-section">
                    <div class="signature-title">Checked by,</div>
                    <div class="signature-line"></div>
                    <div>Sales Admin</div>
                    <div>Date: ___________</div>
                </div>
                <div class="signature-section">
                    <div class="signature-title">Verified by,</div>
                    <div class="signature-line"></div>
                    <div>Production Supervisor</div>
                    <div>Date: ___________</div>
                </div>
            </div>
            
            <div class="version">SGSB (v150825)</div>
        </div>
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
    
    def generate_pdf_from_html(self, html_path: str) -> str:
        """Convert HTML to PDF with proper alignment"""
        try:
            pdf_path = html_path.replace('.html', '.pdf')
            
            # Optimized wkhtmltopdf settings for responsive design
            cmd = [
                'wkhtmltopdf',
                '--page-size', 'A4',
                '--orientation', 'Portrait',
                '--margin-top', '10mm',
                '--margin-bottom', '10mm', 
                '--margin-left', '10mm',
                '--margin-right', '10mm',
                '--encoding', 'UTF-8',
                '--enable-local-file-access',
                '--print-media-type',
                '--disable-smart-shrinking',
                '--zoom', '1.0',
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

# Test the fixed template
if __name__ == "__main__":
    generator = FixedResponsiveTemplate()
    
    test_data = {
        'invoice_number': 'JO-FIXED-001',
        'customer_name': 'KENCANA CONSTRUCTION SDN BHD',
        'document_date': '2025-08-15',
        'delivery_date': '2025-08-22',
        'po_number': 'PO-2025-001',
        'measure_by': 'John Doe',
        'door_thickness': '43mm',
        'door_type': 'S/L',
        'door_core': 'solid tubular core',
        'door_edging': 'na lipping',
        'item_desc_0': '6S-A057 DOOR 850MM x 2021MM',
        'item_size_0': '850MM x 2021MM',
        'door_size': '850MM x 2021MM'
    }
    
    result = generator.generate_fixed_jo(test_data)
    print(f"Generated fixed template: {result}")