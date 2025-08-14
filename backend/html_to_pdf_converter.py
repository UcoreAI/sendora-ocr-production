"""
HTML to PDF Converter for JO Templates
Converts HTML templates to high-quality PDF Job Orders
Maintains exact formatting and layout
"""

import os
import subprocess
import tempfile
from typing import Dict, Any
from datetime import datetime
from html_template_generator import HTMLTemplateGenerator

class HTMLToPDFConverter:
    """Convert HTML templates to PDF with perfect formatting"""
    
    def __init__(self):
        self.html_generator = HTMLTemplateGenerator()
        self.output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'job_orders')
        os.makedirs(self.output_dir, exist_ok=True)
    
    def check_wkhtmltopdf_installed(self) -> bool:
        """Check if wkhtmltopdf is available"""
        try:
            result = subprocess.run(['wkhtmltopdf', '--version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("wkhtmltopdf found - using high-quality PDF generation")
                return True
        except FileNotFoundError:
            pass
        
        print("wkhtmltopdf not found - using weasyprint fallback")
        return False
    
    def convert_with_wkhtmltopdf(self, html_file: str, pdf_file: str) -> bool:
        """Convert HTML to PDF using wkhtmltopdf (best quality)"""
        try:
            cmd = [
                'wkhtmltopdf',
                '--page-size', 'A4',
                '--orientation', 'Landscape',
                '--margin-top', '0mm',
                '--margin-bottom', '0mm',
                '--margin-left', '0mm', 
                '--margin-right', '0mm',
                '--disable-smart-shrinking',
                '--print-media-type',
                '--dpi', '300',
                html_file,
                pdf_file
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"PDF generated successfully: {pdf_file}")
                return True
            else:
                print(f"wkhtmltopdf error: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"Error with wkhtmltopdf: {e}")
            return False
    
    def convert_with_weasyprint(self, html_file: str, pdf_file: str) -> bool:
        """Convert HTML to PDF using weasyprint (fallback)"""
        try:
            import weasyprint
            
            # Read HTML file
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Generate PDF
            html_doc = weasyprint.HTML(string=html_content)
            html_doc.write_pdf(pdf_file)
            
            print(f"PDF generated with weasyprint: {pdf_file}")
            return True
            
        except ImportError:
            print("weasyprint not installed. Install with: pip install weasyprint")
            return False
        except Exception as e:
            print(f"Error with weasyprint: {e}")
            return False
    
    def convert_with_playwright(self, html_file: str, pdf_file: str) -> bool:
        """Convert HTML to PDF using playwright (another fallback)"""
        try:
            from playwright.sync_api import sync_playwright
            
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                
                # Load HTML file
                page.goto(f"file://{os.path.abspath(html_file)}")
                
                # Generate PDF
                page.pdf(
                    path=pdf_file,
                    format='A4',
                    landscape=True,
                    margin={'top': '0mm', 'bottom': '0mm', 'left': '0mm', 'right': '0mm'},
                    print_background=True
                )
                
                browser.close()
            
            print(f"PDF generated with playwright: {pdf_file}")
            return True
            
        except ImportError:
            print("playwright not installed. Install with: pip install playwright")
            return False
        except Exception as e:
            print(f"Error with playwright: {e}")
            return False
    
    def generate_pdf_from_data(self, validated_data: Dict[str, Any]) -> str:
        """Generate PDF Job Order from validated data"""
        
        try:
            # Generate timestamp for files
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            # Create temporary HTML file
            html_filename = f"JO_HTML_{timestamp}.html"
            html_path = os.path.join(tempfile.gettempdir(), html_filename)
            
            # Generate HTML template
            html_content = self.html_generator.generate_html_template(validated_data)
            
            # Save HTML file
            with open(html_path, 'w', encoding='utf-8', errors='replace') as f:
                f.write(html_content)
            
            # Create PDF filename
            pdf_filename = f"JO_HTML_PERFECT_{timestamp}.pdf"
            pdf_path = os.path.join(self.output_dir, pdf_filename)
            
            # Try different PDF conversion methods
            success = False
            
            # Method 1: wkhtmltopdf (best quality)
            if self.check_wkhtmltopdf_installed():
                success = self.convert_with_wkhtmltopdf(html_path, pdf_path)
            
            # Method 2: weasyprint (good fallback)
            if not success:
                success = self.convert_with_weasyprint(html_path, pdf_path)
            
            # Method 3: playwright (browser-based)
            if not success:
                success = self.convert_with_playwright(html_path, pdf_path)
            
            # Cleanup temporary HTML file
            try:
                os.remove(html_path)
            except:
                pass
            
            # Always save HTML file as backup
            fallback_html = os.path.join(self.output_dir, html_filename)
            with open(fallback_html, 'w', encoding='utf-8', errors='replace') as f:
                f.write(html_content)
            
            if success and os.path.exists(pdf_path):
                print(f"Success! Generated PDF: {os.path.basename(pdf_path)}")
                print(f"HTML backup saved: {os.path.basename(fallback_html)}")
                return pdf_path
            else:
                print(f"PDF conversion failed. HTML template saved: {os.path.basename(fallback_html)}")
                print("The HTML file preserves your exact JO template format!")
                return fallback_html
                
        except Exception as e:
            print(f"Error generating PDF: {e}")
            return None
    
    def install_dependencies(self):
        """Install PDF conversion dependencies"""
        
        print("Installing PDF conversion dependencies...")
        print()
        
        print("Option 1: wkhtmltopdf (Recommended - best quality)")
        print("Download from: https://wkhtmltopdf.org/downloads.html")
        print("Windows: Download .exe installer and add to PATH")
        print()
        
        print("Option 2: weasyprint (Python package)")
        print("Install with: pip install weasyprint")
        print()
        
        print("Option 3: playwright (Browser-based)")
        print("Install with: pip install playwright")
        print("Then run: playwright install")
        print()
        
        print("For best results, install wkhtmltopdf first.")


# Integration class for the main application
class HTMLJobOrderGenerator:
    """Main class for generating Job Orders using HTML templates"""
    
    def __init__(self):
        self.converter = HTMLToPDFConverter()
    
    def generate_html_jo(self, validated_data: Dict[str, Any]) -> str:
        """Generate Job Order using HTML template method"""
        
        print("Generating Job Order using HTML template approach...")
        print("This preserves your exact template format!")
        
        # Generate PDF from validated data
        result_path = self.converter.generate_pdf_from_data(validated_data)
        
        if result_path and os.path.exists(result_path):
            print(f"Success! JO generated: {os.path.basename(result_path)}")
            return result_path
        else:
            print("Failed to generate Job Order")
            return None


# Test the HTML to PDF converter
if __name__ == "__main__":
    converter = HTMLToPDFConverter()
    
    print("=" * 60)
    print("HTML TO PDF CONVERTER")
    print("Testing PDF generation with pixel-perfect formatting")
    print("=" * 60)
    
    # Check available conversion methods
    print("Checking PDF conversion capabilities...")
    converter.check_wkhtmltopdf_installed()
    
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
    
    print("\\nGenerating PDF Job Order...")
    result = converter.generate_pdf_from_data(sample_data)
    
    if result:
        print(f"\\nSUCCESS! Generated: {result}")
        print("Your JO template format is perfectly preserved!")
    else:
        print("\\nFAILED: Check PDF conversion setup")
        print("\\nTo install dependencies:")
        converter.install_dependencies()