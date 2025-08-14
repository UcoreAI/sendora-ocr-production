"""
PyPDF Form Filling System
Professional PDF form filling using PyPDF2 - immediate solution
"""

import os
from PyPDF2 import PdfReader, PdfWriter
import json
from typing import Dict, Any
from datetime import datetime
import tempfile

class PyPDFFormFiller:
    """Professional PDF form filling using PyPDF2"""
    
    def __init__(self):
        self.template_paths = {
            'door': r'C:\Users\USER\Desktop\Project management\Sendora\Material\JOB ORDER FORM -DOOR.pdf',
            'frame': r'C:\Users\USER\Desktop\Project management\Sendora\Material\JOB ORDER FORM  - FRAME.pdf', 
            'combined': r'C:\Users\USER\Desktop\Project management\Sendora\Material\JOB ORDER FORM.pdf'
        }
        
        # Create fillable templates directory
        self.fillable_dir = r'C:\Users\USER\Desktop\Sendora-OCR-Complete-Project\fillable_templates'
        os.makedirs(self.fillable_dir, exist_ok=True)
        
    def check_form_fields(self, pdf_path: str) -> Dict[str, Any]:
        """Check if PDF has fillable form fields"""
        
        try:
            reader = PdfReader(pdf_path)
            
            if "/AcroForm" in reader.trailer["/Root"]:
                form = reader.trailer["/Root"]["/AcroForm"]
                if "/Fields" in form:
                    fields = {}
                    for field in form["/Fields"]:
                        field_obj = field.get_object()
                        if "/T" in field_obj:
                            field_name = field_obj["/T"]
                            field_type = field_obj.get("/FT", "Unknown")
                            fields[field_name] = {
                                'type': str(field_type),
                                'value': field_obj.get("/V", "")
                            }
                    
                    print(f"Found {len(fields)} form fields in {os.path.basename(pdf_path)}")
                    return fields
                else:
                    print(f"No form fields found in {os.path.basename(pdf_path)}")
                    return {}
            else:
                print(f"No AcroForm found in {os.path.basename(pdf_path)}")
                return {}
                
        except Exception as e:
            print(f"Error checking form fields: {e}")
            return {}
    
    def create_fillable_template_guide(self):
        """Create guide for converting templates to fillable forms"""
        
        guide_content = """
SENDORA JO FILLABLE FORM CREATION GUIDE
======================================

STEP 1: Install Adobe Acrobat Pro DC (Required)
- Download from Adobe Creative Cloud
- Professional PDF editing tool required for adding form fields

STEP 2: Convert Each Template to Fillable Form

FOR DOOR TEMPLATE:
1. Open: C:\\Users\\USER\\Desktop\\Project management\\Sendora\\Material\\JOB ORDER FORM -DOOR.pdf
2. Go to Tools → Prepare Form
3. Let Acrobat auto-detect fields, then add these specific fields:

HEADER FIELDS (Text Fields):
- job_order_no (in Job Order No area)
- job_order_date (in Job Order Date area) 
- customer_name (in Customer Name area)
- po_no (in PO NO area)
- delivery_date (in Delivery Date area)
- measure_by (in Measure By area)

TABLE FIELDS (Text Fields):
- item_1_number (first row, ITEM column)
- item_1_laminate (first row, LAMINATE CODE column)
- item_1_size (first row, DOOR SIZE column)
- item_1_location (first row, Location area)

- item_2_number (second row, ITEM column)
- item_2_laminate (second row, LAMINATE CODE column)
- item_2_size (second row, DOOR SIZE column)
- item_2_location (second row, Location area)

CHECKBOX FIELDS (Checkboxes):
DOOR THICKNESS group:
- door_thickness_37mm (37mm checkbox)
- door_thickness_43mm (43mm checkbox)
- door_thickness_48mm (48mm checkbox)

DOOR TYPE group:
- door_type_sl (S/L checkbox)
- door_type_dl (D/L checkbox)
- door_type_unequal (Unequal D/L checkbox)

DOOR CORE group:
- door_core_honeycomb (Honeycomb checkbox)
- door_core_solid_tubular (Solid Tubular Core checkbox)
- door_core_solid_timber (Solid Timber checkbox)
- door_core_metal (Metal Skeleton checkbox)

EDGING group:
- edging_na_lipping (NA Lipping checkbox)
- edging_abs (ABS Edging checkbox)
- edging_no (No Edging checkbox)

DECORATIVE LINE group:
- decorative_tbar (T-bar checkbox)
- decorative_groove (Groove Line checkbox)

FOOTER FIELDS (Text Fields):
- prepare_by (bottom left)
- checked_by (bottom center)
- verify_by (bottom right)

STEP 3: Save as Fillable Form
- Save as: fillable_door_form.pdf
- Save to: C:\\Users\\USER\\Desktop\\Sendora-OCR-Complete-Project\\fillable_templates\\

STEP 4: Repeat for Other Templates
- Create fillable_frame_form.pdf
- Create fillable_combined_form.pdf

FIELD NAMING RULES:
- Use lowercase with underscores
- Be descriptive and consistent
- Group related fields with prefixes
- Checkbox values: "Yes" for checked, "Off" for unchecked

TESTING:
After creating fillable forms, test with our PyPDF system:
python pypdf_form_filler.py
"""
        
        guide_path = os.path.join(self.fillable_dir, 'FILLABLE_FORM_CREATION_GUIDE.txt')
        with open(guide_path, 'w', encoding='utf-8') as f:
            f.write(guide_content)
        
        print(f"Created fillable form guide: {guide_path}")
        return guide_path
    
    def fill_form_with_pypdf(self, fillable_template: str, data: Dict[str, Any], output_path: str) -> bool:
        """Fill PDF form using PyPDF2"""
        
        try:
            reader = PdfReader(fillable_template)
            writer = PdfWriter()
            
            # Check if form has fields
            form_fields = self.check_form_fields(fillable_template)
            
            if not form_fields:
                print(f"No form fields found in {fillable_template}")
                print("Template needs to be converted to fillable form first!")
                return False
            
            # Create field data mapping
            field_data = self.create_field_mapping(data)
            
            # Fill form fields
            for page in reader.pages:
                if "/Annots" in page:
                    for annot in page["/Annots"]:
                        annot_obj = annot.get_object()
                        if "/T" in annot_obj:
                            field_name = annot_obj["/T"]
                            if field_name in field_data:
                                annot_obj.update({"/V": field_data[field_name]})
                
                writer.add_page(page)
            
            # Update form
            if "/AcroForm" in reader.trailer["/Root"]:
                writer._root_object.update({"/AcroForm": reader.trailer["/Root"]["/AcroForm"]})
            
            # Write filled form
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            print(f"Form filled successfully: {output_path}")
            return True
            
        except Exception as e:
            print(f"Error filling form: {e}")
            return False
    
    def create_field_mapping(self, data: Dict[str, Any]) -> Dict[str, str]:
        """Map our data to form field names"""
        
        # Extract line items
        line_items = []
        for i in range(10):
            desc_key = f'item_desc_{i}'
            if desc_key in data and data[desc_key]:
                line_items.append({
                    'description': data[desc_key],
                    'size': data.get(f'item_size_{i}', ''),
                    'laminate_code': self.extract_laminate_code(data[desc_key])
                })
        
        # Create field mapping
        field_mapping = {
            # Header fields
            'job_order_no': data.get('invoice_number', ''),
            'job_order_date': data.get('document_date', ''),
            'customer_name': data.get('customer_name', ''),
            'po_no': data.get('po_number', ''),
            'delivery_date': data.get('delivery_date', ''),
            'measure_by': 'Auto Generated',
            
            # Footer fields
            'prepare_by': data.get('invoice_number', ''),
            'checked_by': data.get('document_date', ''),
            'verify_by': data.get('customer_name', ''),
            
            # Checkbox fields (Yes/Off values)
            'door_thickness_43mm': 'Yes' if '43mm' in data.get('door_thickness', '') else 'Off',
            'door_thickness_37mm': 'Yes' if '37mm' in data.get('door_thickness', '') else 'Off',
            'door_thickness_48mm': 'Yes' if '48mm' in data.get('door_thickness', '') else 'Off',
            
            'door_type_sl': 'Yes' if 'S/L' in data.get('door_type', '') else 'Off',
            'door_type_dl': 'Yes' if 'D/L' in data.get('door_type', '') else 'Off',
            'door_type_unequal': 'Yes' if 'Unequal' in data.get('door_type', '') else 'Off',
            
            'door_core_honeycomb': 'Yes' if 'honeycomb' in data.get('door_core', '').lower() else 'Off',
            'door_core_solid_tubular': 'Yes' if 'solid tubular' in data.get('door_core', '').lower() else 'Off',
            'door_core_solid_timber': 'Yes' if 'solid timber' in data.get('door_core', '').lower() else 'Off',
            'door_core_metal': 'Yes' if 'metal' in data.get('door_core', '').lower() else 'Off',
            
            'edging_na_lipping': 'Yes' if 'na lipping' in data.get('door_edging', '').lower() else 'Off',
            'edging_abs': 'Yes' if 'abs' in data.get('door_edging', '').lower() else 'Off',
            'edging_no': 'Yes' if 'no edging' in data.get('door_edging', '').lower() else 'Off',
            
            'decorative_tbar': 'Yes' if 't-bar' in data.get('decorative_line', '').lower() else 'Off',
            'decorative_groove': 'Yes' if 'groove' in data.get('decorative_line', '').lower() else 'Off',
        }
        
        # Add line item fields
        for i, item in enumerate(line_items[:4], 1):  # Up to 4 items
            field_mapping[f'item_{i}_number'] = str(i)
            field_mapping[f'item_{i}_laminate'] = item['laminate_code']
            field_mapping[f'item_{i}_size'] = item['size']
            field_mapping[f'item_{i}_location'] = f'Location: {i}'
        
        return field_mapping
    
    def extract_laminate_code(self, description: str) -> str:
        """Extract laminate code from description"""
        import re
        pattern = r'([0-9]+[A-Z]-[A-Z0-9]+)'
        match = re.search(pattern, description)
        return match.group(1) if match else ""
    
    def generate_jo_with_pypdf(self, validated_data: Dict[str, Any], template_type: str = 'door') -> str:
        """Generate JO using PyPDF form filling"""
        
        # Check for fillable template
        fillable_template = os.path.join(self.fillable_dir, f'fillable_{template_type}_form.pdf')
        
        if not os.path.exists(fillable_template):
            print(f"Fillable template not found: {fillable_template}")
            print("Creating fillable form guide...")
            self.create_fillable_template_guide()
            print("\nPlease create fillable PDF forms using Adobe Acrobat Pro:")
            print(f"1. Follow guide in: {self.fillable_dir}\\FILLABLE_FORM_CREATION_GUIDE.txt")
            print(f"2. Create: {fillable_template}")
            print("3. Run this script again")
            return None
        
        # Generate output filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_filename = f"JO_PYPDF_{template_type.upper()}_{timestamp}.pdf"
        output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'job_orders', output_filename)
        
        # Fill form
        if self.fill_form_with_pypdf(fillable_template, validated_data, output_path):
            return output_path
        else:
            return None
    
    def test_with_sample_data(self):
        """Test the system with sample data"""
        
        sample_data = {
            'invoice_number': 'KDI-2507-003',
            'customer_name': 'SENDORA GROUP SDN BHD',
            'document_date': '2025-08-13',
            'delivery_date': '2025-08-20',
            'po_number': 'PO-2025-001',
            'door_thickness': '43mm',
            'door_type': 'S/L',
            'door_core': 'solid tubular',
            'door_edging': 'na lipping',
            'decorative_line': 't-bar',
            'item_desc_0': '6S-A057 DOOR 43MM x 850MM x 2100MM',
            'item_size_0': '850MM x 2100MM',
            'item_qty_0': '2',
            'item_type_0': 'door'
        }
        
        print("Testing with sample data...")
        result = self.generate_jo_with_pypdf(sample_data, 'door')
        
        if result:
            print(f"SUCCESS: Generated {result}")
        else:
            print("FAILED: Check fillable template creation")


# Main execution
if __name__ == "__main__":
    filler = PyPDFFormFiller()
    
    print("PyPDF Form Filling System - Professional Solution")
    print("=" * 60)
    
    # Check existing templates for form fields
    print("Checking existing templates for form fields...")
    for template_name, template_path in filler.template_paths.items():
        if os.path.exists(template_path):
            fields = filler.check_form_fields(template_path)
            print(f"{template_name}: {len(fields)} fields")
    
    print("\nCreating fillable form conversion guide...")
    guide_path = filler.create_fillable_template_guide()
    
    print("\nTesting with sample data...")
    filler.test_with_sample_data()
    
    print("\n" + "=" * 60)
    print("NEXT STEPS:")
    print("1. Follow the guide to create fillable PDF forms using Adobe Acrobat")
    print("2. Save fillable forms in fillable_templates folder")
    print("3. Run this script again to test form filling")
    print("4. Integration with main Sendora OCR system")
    print("\nThis approach gives 100% accurate positioning!")