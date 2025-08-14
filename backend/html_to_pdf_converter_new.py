"""
HTML to PDF Converter for Sendora Job Orders
Converts HTML templates to PDF format
"""

import os
import subprocess
from pathlib import Path
from typing import Optional

class HTMLToPDFConverter:
    """Convert HTML Job Orders to PDF format"""
    
    def __init__(self):
        self.output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'job_orders', 'pdf')
        os.makedirs(self.output_dir, exist_ok=True)
    
    def convert_with_wkhtmltopdf(self, html_path: str) -> Optional[str]:
        """Convert HTML to PDF using wkhtmltopdf if available"""
        try:
            # Check if wkhtmltopdf is installed
            result = subprocess.run(['wkhtmltopdf', '--version'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                # Generate PDF filename
                html_name = Path(html_path).stem
                pdf_path = os.path.join(self.output_dir, f"{html_name}.pdf")
                
                # Convert HTML to PDF
                cmd = [
                    'wkhtmltopdf',
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
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0 and os.path.exists(pdf_path):
                    print(f"PDF generated successfully: {pdf_path}")
                    return pdf_path
                else:
                    print(f"Error converting to PDF: {result.stderr}")
                    return None
        except FileNotFoundError:
            print("wkhtmltopdf not installed. Trying alternative method...")
            return None
    
    def convert_with_weasyprint(self, html_path: str) -> Optional[str]:
        """Convert HTML to PDF using WeasyPrint library"""
        try:
            from weasyprint import HTML
            
            # Generate PDF filename
            html_name = Path(html_path).stem
            pdf_path = os.path.join(self.output_dir, f"{html_name}.pdf")
            
            # Convert HTML to PDF
            HTML(filename=html_path).write_pdf(pdf_path)
            
            if os.path.exists(pdf_path):
                print(f"PDF generated successfully with WeasyPrint: {pdf_path}")
                return pdf_path
            else:
                return None
                
        except ImportError:
            print("WeasyPrint not installed. Install with: pip install weasyprint")
            return None
        except Exception as e:
            print(f"Error with WeasyPrint: {e}")
            return None
    
    def convert_with_pdfkit(self, html_path: str) -> Optional[str]:
        """Convert HTML to PDF using pdfkit library"""
        try:
            import pdfkit
            
            # Generate PDF filename
            html_name = Path(html_path).stem
            pdf_path = os.path.join(self.output_dir, f"{html_name}.pdf")
            
            # Configuration
            config = pdfkit.configuration()
            options = {
                'page-size': 'A4',
                'margin-top': '10mm',
                'margin-right': '10mm',
                'margin-bottom': '10mm',
                'margin-left': '10mm',
                'encoding': "UTF-8",
                'no-outline': None,
                'enable-local-file-access': None
            }
            
            # Convert HTML to PDF
            pdfkit.from_file(html_path, pdf_path, options=options, configuration=config)
            
            if os.path.exists(pdf_path):
                print(f"PDF generated successfully with pdfkit: {pdf_path}")
                return pdf_path
            else:
                return None
                
        except ImportError:
            print("pdfkit not installed. Install with: pip install pdfkit")
            return None
        except Exception as e:
            print(f"Error with pdfkit: {e}")
            return None
    
    def convert(self, html_path: str) -> Optional[str]:
        """Convert HTML to PDF using available method"""
        
        if not os.path.exists(html_path):
            print(f"HTML file not found: {html_path}")
            return None
        
        print(f"Converting HTML to PDF: {html_path}")
        
        # Try different conversion methods
        pdf_path = self.convert_with_wkhtmltopdf(html_path)
        if pdf_path:
            return pdf_path
        
        pdf_path = self.convert_with_pdfkit(html_path)
        if pdf_path:
            return pdf_path
        
        pdf_path = self.convert_with_weasyprint(html_path)
        if pdf_path:
            return pdf_path
        
        print("\nNo PDF converter available. Please install one of:")
        print("  1. wkhtmltopdf: https://wkhtmltopdf.org/downloads.html")
        print("  2. weasyprint: pip install weasyprint")
        print("  3. pdfkit: pip install pdfkit (requires wkhtmltopdf)")
        
        print("\nFor now, you can:")
        print(f"  1. Open the HTML file directly in a browser: {html_path}")
        print("  2. Use browser's Print to PDF feature (Ctrl+P)")
        
        return None


# Test function
if __name__ == "__main__":
    converter = HTMLToPDFConverter()
    
    # Find the latest HTML file
    html_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'job_orders')
    html_files = sorted([f for f in os.listdir(html_dir) if f.endswith('.html')])
    
    if html_files:
        latest_html = os.path.join(html_dir, html_files[-1])
        print(f"Converting latest HTML: {latest_html}")
        
        pdf_path = converter.convert(latest_html)
        
        if pdf_path:
            print(f"\nSuccess! PDF saved to: {pdf_path}")
            print(f"You can now open the PDF file.")
        else:
            print(f"\nHTML file is ready at: {latest_html}")
            print("Open it in your browser and use Print to PDF (Ctrl+P)")
    else:
        print("No HTML files found to convert")