"""
PDFtk Form Filling Solution
The CORRECT approach - use fillable PDF forms instead of coordinate overlay
"""

import os
import subprocess
import json
from typing import Dict, Any
from datetime import datetime
import tempfile

class PDFtkFormFiller:
    """Fill PDF forms using PDFtk - the proper solution"""
    
    def __init__(self):
        self.template_paths = {
            'door': r'C:\Users\USER\Desktop\Project management\Sendora\Material\JOB ORDER FORM -DOOR.pdf',
            'frame': r'C:\Users\USER\Desktop\Project management\Sendora\Material\JOB ORDER FORM  - FRAME.pdf', 
            'combined': r'C:\Users\USER\Desktop\Project management\Sendora\Material\JOB ORDER FORM.pdf'
        }
        
    def check_pdftk_available(self) -> bool:
        """Check if PDFtk is installed"""
        try:
            result = subprocess.run(['pdftk', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def install_pdftk_windows(self):
        """Install PDFtk on Windows using chocolatey or manual download"""
        print("PDFtk not found. Installing...")
        
        # Try chocolatey first
        try:
            result = subprocess.run(['choco', 'install', 'pdftk-server', '-y'], 
                                  capture_output=True, text=True, timeout=300)
            if result.returncode == 0:
                print("✅ PDFtk installed via Chocolatey")
                return True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print("Chocolatey not available")
        
        # Provide manual installation instructions
        print("""
📋 MANUAL PDFtk INSTALLATION REQUIRED:
        
1. Download PDFtk Server from: https://www.pdflabs.com/tools/pdftk-server/
2. Install PDFtk Server for Windows
3. Add PDFtk to your PATH environment variable
4. Restart your command prompt
5. Re-run this script

Alternative: Use pypdf or PyPDF2 as fallback (less reliable)
        """)
        return False
    
    def extract_form_fields(self, pdf_path: str) -> Dict[str, Any]:
        """Extract form fields from PDF using PDFtk"""
        
        if not self.check_pdftk_available():
            print("❌ PDFtk not available")
            return {}
        
        try:
            # Get form field information
            result = subprocess.run([
                'pdftk', pdf_path, 'dump_data_fields'
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                fields = self.parse_field_data(result.stdout)
                print(f"📋 Found {len(fields)} form fields in {os.path.basename(pdf_path)}")
                return fields
            else:
                print(f"❌ No form fields found in {os.path.basename(pdf_path)}")
                return {}
                
        except Exception as e:
            print(f"❌ Error extracting fields: {e}")
            return {}
    
    def parse_field_data(self, field_data: str) -> Dict[str, Any]:
        """Parse PDFtk field data output"""
        
        fields = {}
        current_field = {}
        
        for line in field_data.split('\n'):
            line = line.strip()
            if line.startswith('FieldName:'):
                if current_field.get('name'):
                    fields[current_field['name']] = current_field
                current_field = {'name': line.replace('FieldName:', '').strip()}
            elif line.startswith('FieldType:'):
                current_field['type'] = line.replace('FieldType:', '').strip()
            elif line.startswith('FieldFlags:'):
                current_field['flags'] = line.replace('FieldFlags:', '').strip()
            elif line.startswith('FieldValue:'):
                current_field['value'] = line.replace('FieldValue:', '').strip()
        
        if current_field.get('name'):
            fields[current_field['name']] = current_field
            
        return fields
    
    def create_fillable_template(self, template_path: str, template_name: str):
        """Create a fillable version of the template (manual process guidance)"""
        
        print(f"""
🔧 CREATING FILLABLE FORM: {template_name}
        
MANUAL STEPS REQUIRED:
1. Open {template_path} in Adobe Acrobat Pro DC
2. Go to Tools → Prepare Form
3. Add form fields for:
   - job_order_no (Text field in Job Order No area)
   - job_order_date (Text field in Job Order Date area) 
   - customer_name (Text field in Customer Name area)
   - po_no (Text field in PO NO area)
   - delivery_date (Text field in Delivery Date area)
   - measure_by (Text field in Measure By area)
   - item_1_laminate (Text field in first row Laminate Code)
   - item_1_size (Text field in first row Door Size)
   - door_thickness_43mm (Checkbox for 43mm option)
   - door_type_sl (Checkbox for S/L option)
   - door_core_solid (Checkbox for Solid Tubular Core)
   
4. Save as: fillable_{template_name}_form.pdf
5. Place in: C:\\Users\\USER\\Desktop\\Sendora-OCR-Complete-Project\\fillable_templates\\

FIELD NAMING CONVENTION:
- Use underscores instead of spaces
- Use descriptive names that match our data fields
- For checkboxes, include the option value in the name
        """)
    
    def fill_form_with_pdftk(self, fillable_template: str, data: Dict[str, Any], output_path: str) -> bool:
        """Fill PDF form using PDFtk"""
        
        if not self.check_pdftk_available():
            print("❌ PDFtk not available")
            return False
        
        # Create FDF data file
        fdf_content = self.create_fdf_data(data)
        
        # Write to temporary FDF file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.fdf', delete=False, encoding='utf-8') as fdf_file:
            fdf_file.write(fdf_content)
            fdf_path = fdf_file.name
        
        try:
            # Fill form using PDFtk
            result = subprocess.run([
                'pdftk', fillable_template, 
                'fill_form', fdf_path,
                'output', output_path,
                'flatten'  # Flatten to prevent further editing
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                print(f"✅ Form filled successfully: {output_path}")
                return True
            else:
                print(f"❌ PDFtk error: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error filling form: {e}")
            return False
        finally:
            # Clean up temp FDF file
            try:
                os.unlink(fdf_path)
            except:
                pass
    
    def create_fdf_data(self, data: Dict[str, Any]) -> str:
        """Create FDF data format for PDFtk"""
        
        # Map our data fields to form field names
        field_mapping = {
            'job_order_no': data.get('invoice_number', ''),
            'job_order_date': data.get('document_date', ''),
            'customer_name': data.get('customer_name', ''),
            'po_no': data.get('po_number', ''),
            'delivery_date': data.get('delivery_date', ''),
            'measure_by': 'Auto Generated',
            'item_1_laminate': self.extract_laminate_code(data.get('item_desc_0', '')),
            'item_1_size': data.get('item_size_0', ''),
            'door_thickness_43mm': 'Yes' if '43mm' in data.get('door_thickness', '') else 'Off',
            'door_type_sl': 'Yes' if 'S/L' in data.get('door_type', '') else 'Off',
            'door_core_solid': 'Yes' if 'solid' in data.get('door_core', '').lower() else 'Off'
        }
        
        # Create FDF content
        fdf_header = """%FDF-1.2
1 0 obj
<<
/FDF
<<
/Fields [
"""
        
        fdf_fields = []
        for field_name, field_value in field_mapping.items():
            if field_value:
                fdf_fields.append(f"<< /T ({field_name}) /V ({field_value}) >>")
        
        fdf_footer = """]
>>
>>
endobj
trailer

<<
/Root 1 0 R
>>
%%EOF"""
        
        return fdf_header + "\n".join(fdf_fields) + "\n" + fdf_footer
    
    def extract_laminate_code(self, description: str) -> str:
        """Extract laminate code from description"""
        import re
        pattern = r'([0-9]+[A-Z]-[A-Z0-9]+)'
        match = re.search(pattern, description)
        return match.group(1) if match else ""
    
    def generate_jo_with_pdftk(self, validated_data: Dict[str, Any], template_type: str = 'door') -> str:
        """Generate JO using PDFtk form filling"""
        
        # Check for fillable template
        fillable_template = f"C:\\Users\\USER\\Desktop\\Sendora-OCR-Complete-Project\\fillable_templates\\fillable_{template_type}_form.pdf"
        
        if not os.path.exists(fillable_template):
            print(f"❌ Fillable template not found: {fillable_template}")
            self.create_fillable_template(self.template_paths[template_type], template_type)
            return None
        
        # Generate output filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_filename = f"JO_PDFTK_{template_type.upper()}_{timestamp}.pdf"
        output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'job_orders', output_filename)
        
        # Fill form
        if self.fill_form_with_pdftk(fillable_template, validated_data, output_path):
            return output_path
        else:
            return None


# Test and setup
if __name__ == "__main__":
    filler = PDFtkFormFiller()
    
    print("PDFtk Form Filling System")
    print("=" * 50)
    
    # Check PDFtk availability
    if filler.check_pdftk_available():
        print("✅ PDFtk is available")
        
        # Test extracting fields from existing template
        for template_name, template_path in filler.template_paths.items():
            if os.path.exists(template_path):
                fields = filler.extract_form_fields(template_path)
                if fields:
                    print(f"📋 {template_name} has {len(fields)} form fields")
                else:
                    print(f"📋 {template_name} needs to be converted to fillable form")
                    filler.create_fillable_template(template_path, template_name)
    else:
        print("❌ PDFtk not available")
        filler.install_pdftk_windows()
    
    print("\n💡 PDFtk approach will give us 100% accurate positioning!")
    print("   Forms are filled programmatically instead of coordinate guessing.")