"""
Clean Template Generator
Simple, exact match to the Sendora JO template
"""

import os
from datetime import datetime
from typing import Dict, Any

class CleanTemplateGenerator:
    """Generate clean HTML that exactly matches the Sendora JO template"""
    
    def __init__(self):
        self.output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'job_orders')
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_clean_jo(self, validated_data: Dict[str, Any]) -> str:
        """Generate clean JO based on exact template"""
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        html_filename = f"JO_CLEAN_{timestamp}.html"
        html_path = os.path.join(self.output_dir, html_filename)
        
        # Generate HTML content
        html_content = self.create_clean_template(validated_data)
        
        # Save HTML file
        try:
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"SUCCESS! Clean JO generated: {html_filename}")
            
            return html_path
            
        except Exception as e:
            print(f"Error generating clean JO: {e}")
            return None
    
    def create_clean_template(self, data: Dict[str, Any]) -> str:
        """Create simple HTML matching the exact template"""
        
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
        body {{ font-family: Arial, sans-serif; font-size: 10px; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ border: 1px solid black; padding: 3px; text-align: center; font-size: 8px; }}
        .page {{ width: 21cm; margin: 0.5cm; page-break-after: always; }}
        .header {{ text-align: center; margin-bottom: 10px; }}
        .company {{ font-size: 12px; font-weight: bold; text-decoration: underline; }}
        .title-row {{ display: flex; justify-content: space-between; align-items: center; margin: 10px 0; }}
        .job-order-box {{ border: 2px solid black; padding: 5px 15px; font-size: 16px; font-weight: bold; }}
        .form-type {{ text-align: center; font-size: 24px; font-weight: bold; margin: 15px 0; border: 2px solid black; padding: 10px; }}
        .field {{ margin: 3px 0; }}
        .checkbox {{ width: 8px; height: 8px; border: 1px solid black; display: inline-block; margin-right: 3px; }}
        .checked {{ background: black; }}
        .item-cell {{ height: 80px; vertical-align: top; }}
        .footer {{ margin-top: 20px; display: flex; justify-content: space-between; }}
    </style>
</head>
<body>
    <!-- DOOR PAGE -->
    <div class="page">
        <div class="header">
            <div class="company">SENDORA GROUP SDN BHD (HQ)</div>
        </div>
        
        <div class="title-row">
            <div>
                <div class="field">Job Order No: ________________{job_order_no}________________</div>
                <div class="field">Job Order Date: ________________{job_order_date}________________</div>
                <div class="field">PO NO: ________________{po_no}________________</div>
            </div>
            <div class="job-order-box">JOB ORDER</div>
            <div>
                <div class="field">Delivery Date: ________________{delivery_date}________________</div>
                <div class="field">Customer Name: ________________{customer_name}________________</div>
                <div class="field">Measure By: ________________{measure_by}________________</div>
            </div>
        </div>
        
        <div class="form-type">DOOR</div>
        
        <table>
            <tr>
                <th style="width: 30px;">ITEM</th>
                <th style="width: 60px;">LAMINATE CODE</th>
                <th style="width: 80px;">DOOR THICKNESS</th>
                <th style="width: 120px;">DOOR SIZE</th>
                <th style="width: 80px;">DOOR TYPE</th>
                <th style="width: 100px;">DOOR CORE</th>
                <th style="width: 80px;">EDGING</th>
                <th style="width: 80px;">DECORATIVE LINE</th>
                <th style="width: 80px;">DESIGN NAME</th>
                <th style="width: 80px;">OPEN HOLE TYPE</th>
                <th style="width: 100px;">DRAWING / REMARK</th>
            </tr>
            
            <!-- Row 1 -->
            <tr>
                <td class="item-cell">1</td>
                <td class="item-cell">{laminate_code}</td>
                <td class="item-cell">
                    <span class="checkbox {'checked' if '37' in door_thickness else ''}"></span>37mm<br>
                    <span class="checkbox {'checked' if '43' in door_thickness else ''}"></span>43mm<br>
                    <span class="checkbox {'checked' if '48' in door_thickness else ''}"></span>48mm<br>
                    <span class="checkbox"></span>Others:
                </td>
                <td class="item-cell">
                    {item_size}
                    <div style="font-size: 18px;">①</div>
                    Location :
                </td>
                <td class="item-cell">
                    <span class="checkbox {'checked' if 's/l' in door_type else ''}"></span>S/L<br>
                    <span class="checkbox {'checked' if 'd/l' in door_type else ''}"></span>D/L<br>
                    <span class="checkbox {'checked' if 'unequal' in door_type else ''}"></span>Unequal D/L<br>
                    <span class="checkbox"></span>Others:
                </td>
                <td class="item-cell">
                    <span class="checkbox {'checked' if 'honeycomb' in door_core else ''}"></span>Honeycomb<br>
                    <span class="checkbox {'checked' if 'tubular' in door_core else ''}"></span>Solid Tubular Core<br>
                    <span class="checkbox {'checked' if 'timber' in door_core else ''}"></span>Solid Timber<br>
                    <span class="checkbox {'checked' if 'metal' in door_core else ''}"></span>Metal Skeleton
                </td>
                <td class="item-cell">
                    <span class="checkbox {'checked' if 'na lipping' in door_edging else ''}"></span>NA Lipping<br>
                    <span class="checkbox {'checked' if 'abs' in door_edging else ''}"></span>ABS Edging<br>
                    <span class="checkbox {'checked' if 'no edging' in door_edging else ''}"></span>No Edging
                </td>
                <td class="item-cell">
                    <span class="checkbox {'checked' if 't-bar' in decorative_line else ''}"></span>T-bar<br>
                    <span class="checkbox {'checked' if 'groove' in decorative_line else ''}"></span>Groove Line
                </td>
                <td class="item-cell"></td>
                <td class="item-cell"></td>
                <td class="item-cell"></td>
            </tr>
            
            <!-- Rows 2-4 (empty but with structure) -->
            <tr>
                <td class="item-cell"></td>
                <td class="item-cell"></td>
                <td class="item-cell">
                    <span class="checkbox"></span>37mm<br>
                    <span class="checkbox"></span>43mm<br>
                    <span class="checkbox"></span>48mm<br>
                    <span class="checkbox"></span>Others:
                </td>
                <td class="item-cell">
                    <div style="font-size: 18px;">②</div>
                    Location :
                </td>
                <td class="item-cell">
                    <span class="checkbox"></span>S/L<br>
                    <span class="checkbox"></span>D/L<br>
                    <span class="checkbox"></span>Unequal D/L<br>
                    <span class="checkbox"></span>Others:
                </td>
                <td class="item-cell">
                    <span class="checkbox"></span>Honeycomb<br>
                    <span class="checkbox"></span>Solid Tubular Core<br>
                    <span class="checkbox"></span>Solid Timber<br>
                    <span class="checkbox"></span>Metal Skeleton
                </td>
                <td class="item-cell">
                    <span class="checkbox"></span>NA Lipping<br>
                    <span class="checkbox"></span>ABS Edging<br>
                    <span class="checkbox"></span>No Edging
                </td>
                <td class="item-cell">
                    <span class="checkbox"></span>T-bar<br>
                    <span class="checkbox"></span>Groove Line
                </td>
                <td class="item-cell"></td>
                <td class="item-cell"></td>
                <td class="item-cell"></td>
            </tr>
            
            <tr>
                <td class="item-cell"></td>
                <td class="item-cell"></td>
                <td class="item-cell">
                    <span class="checkbox"></span>37mm<br>
                    <span class="checkbox"></span>43mm<br>
                    <span class="checkbox"></span>48mm<br>
                    <span class="checkbox"></span>Others:
                </td>
                <td class="item-cell">
                    <div style="font-size: 18px;">③</div>
                    Location :
                </td>
                <td class="item-cell">
                    <span class="checkbox"></span>S/L<br>
                    <span class="checkbox"></span>D/L<br>
                    <span class="checkbox"></span>Unequal D/L<br>
                    <span class="checkbox"></span>Others:
                </td>
                <td class="item-cell">
                    <span class="checkbox"></span>Honeycomb<br>
                    <span class="checkbox"></span>Solid Tubular Core<br>
                    <span class="checkbox"></span>Solid Timber<br>
                    <span class="checkbox"></span>Metal Skeleton
                </td>
                <td class="item-cell">
                    <span class="checkbox"></span>NA Lipping<br>
                    <span class="checkbox"></span>ABS Edging<br>
                    <span class="checkbox"></span>No Edging
                </td>
                <td class="item-cell">
                    <span class="checkbox"></span>T-bar<br>
                    <span class="checkbox"></span>Groove Line
                </td>
                <td class="item-cell"></td>
                <td class="item-cell"></td>
                <td class="item-cell"></td>
            </tr>
            
            <tr>
                <td class="item-cell"></td>
                <td class="item-cell"></td>
                <td class="item-cell">
                    <span class="checkbox"></span>37mm<br>
                    <span class="checkbox"></span>43mm<br>
                    <span class="checkbox"></span>48mm<br>
                    <span class="checkbox"></span>Others:
                </td>
                <td class="item-cell">
                    <div style="font-size: 18px;">④</div>
                    Location :
                </td>
                <td class="item-cell">
                    <span class="checkbox"></span>S/L<br>
                    <span class="checkbox"></span>D/L<br>
                    <span class="checkbox"></span>Unequal D/L<br>
                    <span class="checkbox"></span>Others:
                </td>
                <td class="item-cell">
                    <span class="checkbox"></span>Honeycomb<br>
                    <span class="checkbox"></span>Solid Tubular Core<br>
                    <span class="checkbox"></span>Solid Timber<br>
                    <span class="checkbox"></span>Metal Skeleton
                </td>
                <td class="item-cell">
                    <span class="checkbox"></span>NA Lipping<br>
                    <span class="checkbox"></span>ABS Edging<br>
                    <span class="checkbox"></span>No Edging
                </td>
                <td class="item-cell">
                    <span class="checkbox"></span>T-bar<br>
                    <span class="checkbox"></span>Groove Line
                </td>
                <td class="item-cell"></td>
                <td class="item-cell"></td>
                <td class="item-cell"></td>
            </tr>
        </table>
        
        <div class="footer">
            <div>
                <strong>Prepare by,</strong><br><br>
                Sales Executive :<br>
                Date :
            </div>
            <div>
                <strong>Checked by,</strong><br><br>
                Sales Admin<br>
                Date :
            </div>
            <div>
                <strong>Verify by,</strong><br><br>
                Production Supervisor :<br>
                Date :
            </div>
        </div>
        
        <div style="position: absolute; bottom: 10px; right: 10px; font-size: 8px;">
            SGSB (v050625)
        </div>
    </div>
    
    <!-- FRAME PAGE -->
    <div class="page">
        <div class="header">
            <div class="company">SENDORA GROUP SDN BHD (HQ)</div>
        </div>
        
        <div class="title-row">
            <div>
                <div class="field">Job Order No: ________________{job_order_no}________________</div>
                <div class="field">Job Order Date: ________________{job_order_date}________________</div>
                <div class="field">PO NO: ________________{po_no}________________</div>
            </div>
            <div class="job-order-box">JOB ORDER</div>
            <div>
                <div class="field">Delivery Date: ________________{delivery_date}________________</div>
                <div class="field">Customer Name: ________________{customer_name}________________</div>
                <div class="field">Measure by: ________________{measure_by}________________</div>
            </div>
        </div>
        
        <div class="form-type">FRAME</div>
        
        <table>
            <tr>
                <th style="width: 40px;">ITEM</th>
                <th style="width: 80px;">FRAME LAMINATE CODE</th>
                <th style="width: 80px;">FRAME WIDTH</th>
                <th style="width: 60px;">REBATED</th>
                <th style="width: 120px;">FRAME SIZE</th>
                <th style="width: 100px;">INNER OR OUTER</th>
                <th style="width: 80px;">FRAME PROFILE</th>
                <th style="width: 120px;">DRAWING / REMARK</th>
            </tr>
            
            <tr>
                <td class="item-cell">1</td>
                <td class="item-cell"></td>
                <td class="item-cell"></td>
                <td class="item-cell"></td>
                <td class="item-cell">
                    <div style="font-size: 18px;">①</div>
                    Location :
                </td>
                <td class="item-cell">
                    <span class="checkbox checked"></span>INNER<br>
                    <span class="checkbox"></span>OUTER
                </td>
                <td class="item-cell"></td>
                <td class="item-cell"></td>
            </tr>
            
            <tr>
                <td class="item-cell"></td>
                <td class="item-cell"></td>
                <td class="item-cell"></td>
                <td class="item-cell"></td>
                <td class="item-cell">
                    <div style="font-size: 18px;">②</div>
                    Location :
                </td>
                <td class="item-cell">
                    <span class="checkbox"></span>INNER<br>
                    <span class="checkbox"></span>OUTER
                </td>
                <td class="item-cell"></td>
                <td class="item-cell"></td>
            </tr>
            
            <tr>
                <td class="item-cell"></td>
                <td class="item-cell"></td>
                <td class="item-cell"></td>
                <td class="item-cell"></td>
                <td class="item-cell">
                    <div style="font-size: 18px;">③</div>
                    Location :
                </td>
                <td class="item-cell">
                    <span class="checkbox"></span>INNER<br>
                    <span class="checkbox"></span>OUTER
                </td>
                <td class="item-cell"></td>
                <td class="item-cell"></td>
            </tr>
        </table>
        
        <div class="footer">
            <div>
                <strong>Prepare by,</strong><br><br>
                Sales Executive :<br>
                Date :
            </div>
            <div>
                <strong>Checked by,</strong><br><br>
                Sales Admin :<br>
                Date :
            </div>
            <div>
                <strong>Verify by,</strong><br><br>
                Production Supervisor :<br>
                Date :
            </div>
        </div>
        
        <div style="position: absolute; bottom: 10px; right: 10px; font-size: 8px;">
            SGSB (v050625)
        </div>
    </div>
</body>
</html>'''
    
    def extract_laminate_code(self, description: str) -> str:
        """Extract laminate code from description"""
        import re
        pattern = r'([0-9]+[A-Z]-[A-Z0-9]+)'
        match = re.search(pattern, description)
        return match.group(1) if match else ""


# Test the clean generator
if __name__ == "__main__":
    generator = CleanTemplateGenerator()
    
    test_data = {
        'invoice_number': 'JO-CLEAN-001',
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
    
    result = generator.generate_clean_jo(test_data)
    print(f"Generated: {result}")