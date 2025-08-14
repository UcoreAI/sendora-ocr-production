"""
Google Document AI Processor for Sendora OCR V2.0
High-accuracy document processing with structured data extraction
"""

from google.cloud import documentai_v1 as documentai
from google.oauth2 import service_account
from google.api_core.client_options import ClientOptions
import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime


class GoogleDocumentProcessor:
    """Google Document AI processor for invoices and purchase orders"""
    
    def __init__(self):
        """Initialize Google Document AI client"""
        
        # Configuration
        self.project_id = "my-textbee-sms"  # Updated with your actual project ID
        self.location = "us"  # or "eu" for Europe
        self.processor_id = None  # Will be set based on document type
        
        # Processor IDs for different document types
        self.processors = {
            'invoice': '1699972f50f6529',  # Your Invoice Processor
            'purchase_order': '81116d27ff6c4a06',  # Your Form Parser Processor  
            'quote': '81116d27ff6c4a06',  # Use form parser for quotes
            'quotation': '81116d27ff6c4a06',  # Alternative name for quotes
            'receipt': '1699972f50f6529',
            'general': '81116d27ff6c4a06'  # Your Form Parser for general OCR
        }
        
        # Initialize client with credentials
        try:
            credentials_path = os.path.join('config', 'google-credentials.json')
            if os.path.exists(credentials_path):
                credentials = service_account.Credentials.from_service_account_file(
                    credentials_path
                )
            else:
                # Use default credentials if file not found
                print("Warning: google-credentials.json not found. Using default credentials.")
                credentials = None
            
            # Set up client options
            opts = ClientOptions(api_endpoint=f"{self.location}-documentai.googleapis.com")
            
            # Initialize the client
            self.client = documentai.DocumentProcessorServiceClient(
                credentials=credentials,
                client_options=opts
            )
            
            print("Google Document AI processor initialized")
            
        except Exception as e:
            print(f"Error initializing Google Document AI: {e}")
            self.client = None
    
    def detect_document_type(self, file_path: str) -> str:
        """Detect document type from filename and content patterns"""
        
        filename = os.path.basename(file_path).lower()
        
        # Check filename patterns
        if any(word in filename for word in ['quote', 'quotation', 'estimate']):
            return 'quote'
        elif any(word in filename for word in ['po', 'purchase_order', 'purchase']):
            return 'purchase_order'
        elif any(word in filename for word in ['invoice', 'bill', 'inv']):
            return 'invoice'
        elif any(word in filename for word in ['receipt', 'rcpt']):
            return 'receipt'
        
        # If no clear pattern in filename, try to read content for keywords
        try:
            if file_path.lower().endswith('.pdf'):
                import PyPDF2
                with open(file_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    text = ""
                    for page in reader.pages[:2]:  # Check first 2 pages
                        text += page.extract_text().lower()
                    
                    if any(word in text for word in ['quotation', 'quote', 'estimate']):
                        return 'quote'
                    elif any(word in text for word in ['purchase order', 'p.o.', 'po number']):
                        return 'purchase_order'
                    elif any(word in text for word in ['invoice', 'bill to', 'invoice number']):
                        return 'invoice'
        except:
            pass
        
        # Default to invoice processor
        return 'invoice'
    
    def process_document(self, file_path: str) -> Dict[str, Any]:
        """Process document with Google Document AI"""
        
        if not self.client:
            return self.fallback_processing(file_path)
        
        try:
            # Detect document type
            doc_type = self.detect_document_type(file_path)
            self.processor_id = self.processors.get(doc_type, self.processors['general'])
            
            # Read file
            with open(file_path, 'rb') as f:
                content = f.read()
            
            # Determine MIME type
            if file_path.lower().endswith('.pdf'):
                mime_type = 'application/pdf'
            elif file_path.lower().endswith(('.jpg', '.jpeg')):
                mime_type = 'image/jpeg'
            elif file_path.lower().endswith('.png'):
                mime_type = 'image/png'
            else:
                mime_type = 'application/octet-stream'
            
            # Create document object
            raw_document = documentai.RawDocument(
                content=content,
                mime_type=mime_type
            )
            
            # Configure the process request
            name = self.client.processor_path(
                self.project_id,
                self.location,
                self.processor_id
            )
            
            request = documentai.ProcessRequest(
                name=name,
                raw_document=raw_document
            )
            
            # Process the document
            print(f"Processing document with Google Document AI...")
            result = self.client.process_document(request=request)
            
            # Extract structured data
            extracted_data = self.extract_structured_data(result.document)
            
            print(f"Document processed successfully")
            return extracted_data
            
        except Exception as e:
            print(f"Error processing with Google Document AI: {e}")
            return self.fallback_processing(file_path)
    
    def extract_structured_data(self, document) -> Dict[str, Any]:
        """Extract structured data from Document AI response"""
        
        extracted = {
            'invoice_number': None,
            'po_number': None,
            'date': None,
            'due_date': None,
            'vendor': {
                'name': None,
                'address': None,
                'phone': None
            },
            'customer': {
                'name': None,
                'address': None,
                'phone': None
            },
            'line_items': [],
            'subtotal': None,
            'tax': None,
            'total': None,
            'currency': 'MYR',
            'confidence_scores': {},
            'full_text': document.text,
            'document_type': 'invoice'
        }
        
        # Extract entities
        for entity in document.entities:
            entity_type = entity.type_.lower()
            confidence = entity.confidence
            
            # Invoice/PO identifiers
            if entity_type in ['invoice_id', 'invoice_number', 'invoice#']:
                extracted['invoice_number'] = entity.mention_text
                extracted['confidence_scores']['invoice_number'] = confidence
                
            elif entity_type in ['purchase_order', 'po_number', 'po#']:
                extracted['po_number'] = entity.mention_text
                extracted['confidence_scores']['po_number'] = confidence
                
            # Dates
            elif entity_type in ['invoice_date', 'date']:
                extracted['date'] = entity.mention_text
                extracted['confidence_scores']['date'] = confidence
                
            elif entity_type in ['due_date', 'delivery_date']:
                extracted['due_date'] = entity.mention_text
                extracted['confidence_scores']['due_date'] = confidence
                
            # Vendor/Supplier info
            elif entity_type in ['supplier_name', 'vendor_name', 'seller']:
                extracted['vendor']['name'] = entity.mention_text
                extracted['confidence_scores']['vendor_name'] = confidence
                
            elif entity_type in ['supplier_address', 'vendor_address']:
                extracted['vendor']['address'] = entity.mention_text
                
            # Customer info
            elif entity_type in ['receiver_name', 'customer_name', 'buyer', 'bill_to']:
                extracted['customer']['name'] = entity.mention_text
                extracted['confidence_scores']['customer_name'] = confidence
                
            elif entity_type in ['receiver_address', 'customer_address', 'ship_to']:
                extracted['customer']['address'] = entity.mention_text
                
            # Financial totals
            elif entity_type in ['total_amount', 'total', 'grand_total']:
                extracted['total'] = entity.mention_text
                extracted['confidence_scores']['total'] = confidence
                
            elif entity_type == 'subtotal':
                extracted['subtotal'] = entity.mention_text
                
            elif entity_type in ['total_tax', 'tax']:
                extracted['tax'] = entity.mention_text
                
            # Line items
            elif entity_type == 'line_item':
                item = self.extract_line_item(entity)
                if item:
                    extracted['line_items'].append(item)
        
        # Extract Malaysian-specific patterns
        extracted = self.extract_malaysian_patterns(extracted, document.text)
        
        # Process line items to extract aggregated door specifications
        extracted = self.aggregate_door_specifications(extracted)
        
        # Final cleanup - ensure customer name is not Sendora-related
        extracted = self.cleanup_customer_name(extracted)
        
        return extracted
    
    def extract_line_item(self, entity) -> Dict[str, Any]:
        """Extract line item details from entity"""
        
        item = {
            'description': None,
            'quantity': None,
            'unit_price': None,
            'amount': None,
            'unit': None,
            'size': None,
            'specifications': {}
        }
        
        # Extract properties
        for prop in entity.properties:
            prop_type = prop.type_.lower()
            
            if prop_type in ['line_item/description', 'description', 'item']:
                item['description'] = prop.mention_text
                # Extract size from description
                item['size'] = self.extract_size(prop.mention_text)
                
            elif prop_type in ['line_item/quantity', 'quantity', 'qty']:
                item['quantity'] = prop.mention_text
                
            elif prop_type in ['line_item/unit_price', 'unit_price', 'rate']:
                item['unit_price'] = prop.mention_text
                
            elif prop_type in ['line_item/amount', 'amount', 'total']:
                item['amount'] = prop.mention_text
                
            elif prop_type in ['line_item/unit', 'unit', 'uom']:
                item['unit'] = prop.mention_text
        
        # Extract door/frame specifications from description
        if item['description']:
            item['specifications'] = self.extract_specifications(item['description'])
        
        return item if item['description'] else None
    
    def extract_size(self, text: str) -> Optional[str]:
        """Extract size pattern from text"""
        
        import re
        
        # Enhanced size patterns including feet conversion - ordered by specificity
        patterns = [
            # Most specific patterns first
            r'(\d+)[mM][mM]\s*[xX]\s*(\d+)\s*[fF][tT]\s*[xX]\s*(\d+)\s*[fF][tT]',  # 43MM X 3FT X 8FT
            
            # MM patterns
            r'(\d+)\s*[mM][mM]\s*[xX]\s*(\d+)\s*[mM][mM]',  # 850mm x 2100mm
            r'(\d+)\s*[xX]\s*(\d+)\s*[mM][mM]',              # 850x2100mm
            r'(\d+)\s*[xX]\s*(\d+)',                          # 850x2100
            
            # Feet patterns - need conversion
            r'(\d+)[mM][mM]\s*[xX]\s*(\d+)\s*[fF][tT]',     # 43mm x 8ft
            r'(\d+)\s*[fF][tT]\s*[xX]\s*(\d+)\s*[fF][tT]', # 3ft x 8ft
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                if '[fF][tT]' in pattern or 'ft' in pattern.lower():
                    # Handle feet conversion
                    if len(match.groups()) == 3:  # 43MM X 3FT X 8FT format
                        thickness = match.group(1)
                        width_ft = int(match.group(2))
                        height_ft = int(match.group(3))
                        width_mm = width_ft * 305  # 1 foot ≈ 305mm (rounded)
                        height_mm = height_ft * 305
                        return f"{width_mm}MM x {height_mm}MM"
                    elif len(match.groups()) == 2:
                        if 'mm' in match.group(1).lower():
                            # Mixed: 43mm x 8ft
                            thickness = match.group(1).replace('mm', '').replace('MM', '')
                            height_ft = int(match.group(2))
                            height_mm = height_ft * 305
                            return f"{thickness}MM x {height_mm}MM"
                        else:
                            # Both in feet: 3ft x 8ft  
                            width_ft = int(match.group(1))
                            height_ft = int(match.group(2))
                            width_mm = width_ft * 305
                            height_mm = height_ft * 305
                            return f"{width_mm}MM x {height_mm}MM"
                else:
                    # MM patterns
                    return f"{match.group(1)}MM x {match.group(2)}MM"
        
        # Special case: try to find size in descriptions like "DOOR SIZE: 43MM X 3FT X 8FT"
        size_match = re.search(r'door\s+size[:\s]*([^\n]+)', text, re.IGNORECASE)
        if size_match:
            size_text = size_match.group(1)
            return self.extract_size(size_text)  # Recursive call with just the size part
        
        return None
    
    def extract_specifications(self, description: str) -> Dict[str, str]:
        """Extract door/frame specifications from description"""
        
        specs = {}
        desc_lower = description.lower()
        
        # Door thickness - enhanced patterns
        thickness_patterns = [
            r'(\d+)mm\s*thick',
            r'thickness[:\s]*(\d+)mm',
            r'(\d+)\s*mm\s*door',
            r'door\s*(\d+)mm',
            r'(\d+)\s*mm(?:\s|$)',
        ]
        
        import re
        for pattern in thickness_patterns:
            match = re.search(pattern, desc_lower)
            if match:
                thickness = match.group(1)
                if thickness in ['37', '43', '46', '48']:
                    specs['thickness'] = f'{thickness}mm'
                    break
        
        # Door type - enhanced patterns
        if any(term in desc_lower for term in ['s/l', 'single leaf', 'single door']):
            specs['type'] = 'S/L'
        elif any(term in desc_lower for term in ['d/l', 'double leaf', 'double door', 'unequal']):
            if 'unequal' in desc_lower:
                specs['type'] = 'Unequal D/L'
            else:
                specs['type'] = 'D/L'
        
        # Door core - enhanced patterns
        if any(term in desc_lower for term in ['honeycomb', 'honey comb']):
            specs['core'] = 'honeycomb'
        elif any(term in desc_lower for term in ['solid tubular', 'tubular core', 'tubular']):
            specs['core'] = 'solid_tubular'
        elif any(term in desc_lower for term in ['solid timber', 'timber core', 'solid wood']):
            specs['core'] = 'solid_timber'
        elif any(term in desc_lower for term in ['metal skeleton', 'metal frame']):
            specs['core'] = 'metal_skeleton'
        
        # Edging type
        if any(term in desc_lower for term in ['na lipping', 'natural lipping']):
            specs['edging'] = 'na_lipping'
        elif any(term in desc_lower for term in ['abs edging', 'abs edge']):
            specs['edging'] = 'abs_edging'
        elif any(term in desc_lower for term in ['no edging', 'without edge']):
            specs['edging'] = 'no_edging'
        
        # Decorative line
        if any(term in desc_lower for term in ['t-bar', 't bar', 'tbar']):
            specs['decorative'] = 't_bar'
        elif any(term in desc_lower for term in ['groove line', 'groove']):
            specs['decorative'] = 'groove_line'
        
        # Frame type
        if 'inner' in desc_lower:
            specs['frame_type'] = 'inner'
        elif 'outer' in desc_lower:
            specs['frame_type'] = 'outer'
        
        return specs
    
    def extract_malaysian_patterns(self, extracted: Dict, text: str) -> Dict:
        """Extract Malaysian-specific patterns"""
        
        text_lower = text.lower()
        
        # Malaysian company indicators
        company_patterns = ['sdn bhd', 'sdn. bhd.', 'bhd', 'enterprise', 'trading']
        
        # If customer name not found, search for Malaysian company names
        if not extracted['customer']['name']:
            # First try to find "Bill To:" or "Customer:" sections
            bill_to_patterns = [
                r'bill\s+to[:\s]+([^\n]+(?:sdn\s+bhd|bhd|enterprise|trading)[^\n]*)',
                r'customer[:\s]+([^\n]+(?:sdn\s+bhd|bhd|enterprise|trading)[^\n]*)',
                r'sold\s+to[:\s]+([^\n]+(?:sdn\s+bhd|bhd|enterprise|trading)[^\n]*)',
                r'buyer[:\s]+([^\n]+(?:sdn\s+bhd|bhd|enterprise|trading)[^\n]*)',
            ]
            
            import re
            for pattern in bill_to_patterns:
                match = re.search(pattern, text_lower, re.IGNORECASE)
                if match:
                    company_name = match.group(1).strip().upper()
                    # Exclude Sendora-related text
                    if not self.is_sendora_text(company_name):
                        extracted['customer']['name'] = company_name
                        break
            
            # If still not found, search for general Malaysian company names
            if not extracted['customer']['name']:
                for pattern in company_patterns:
                    match = re.search(r'([A-Za-z0-9\s&]+)\s+' + pattern, text_lower)
                    if match:
                        company_name = match.group(0).upper()
                        # Exclude Sendora-related text
                        if not self.is_sendora_text(company_name):
                            extracted['customer']['name'] = company_name
                            break
        
        # Malaysian currency
        if 'rm' in text_lower or 'ringgit' in text_lower:
            extracted['currency'] = 'MYR'
        
        # Door/Frame specific terms
        if 'pintu' in text_lower:
            extracted['document_type'] = 'door_order'
        elif 'bingkai' in text_lower or 'frame' in text_lower:
            extracted['document_type'] = 'frame_order'
        
        return extracted
    
    def is_sendora_text(self, text: str) -> bool:
        """Check if text contains Sendora-related content that should be excluded"""
        if not text:
            return False
            
        sendora_indicators = [
            'sendora', 'trusted', 'reliable', 'door brand', 
            'group sdn bhd', 'kota damansara', 'manufacturer',
            'marketing', 'branding', 'sendoraa'
        ]
        
        text_lower = text.lower().strip()
        
        # Direct matches for problematic text patterns
        if 'sendoraa trusted' in text_lower:
            return True
        if 'reliable door brand' in text_lower:
            return True
        if text_lower.startswith('sendora'):
            return True
        
        return any(indicator in text_lower for indicator in sendora_indicators)
    
    def aggregate_door_specifications(self, extracted: Dict) -> Dict:
        """Aggregate door specifications from line items for template use"""
        
        # Initialize aggregated specs
        aggregated_specs = {
            'door_thickness': '',
            'door_type': '',
            'door_core': '',
            'door_edging': '',
            'decorative_line': '',
            'frame_type': '',
            'door_size': '',
            'item_desc_0': '',
            'item_size_0': ''
        }
        
        # Process line items to extract common specifications
        door_item_found = False
        for i, item in enumerate(extracted.get('line_items', [])):
            specs = item.get('specifications', {})
            description = item.get('description', '')
            
            # Find the main door item (usually first item or one with door specifications)
            if not door_item_found and ('door' in description.lower() or specs.get('thickness') or specs.get('type')):
                door_item_found = True
                aggregated_specs['item_desc_0'] = description
                
                # Try to get size from this item or extract from description
                item_size = item.get('size')
                if item_size:
                    aggregated_specs['item_size_0'] = item_size
                    aggregated_specs['door_size'] = item_size
                else:
                    # Try to extract size from description
                    extracted_size = self.extract_size(description)
                    if extracted_size:
                        aggregated_specs['item_size_0'] = extracted_size
                        aggregated_specs['door_size'] = extracted_size
                        print(f"EXTRACTED door size from description: {extracted_size}")
            
            # Aggregate thickness
            if specs.get('thickness') and not aggregated_specs['door_thickness']:
                aggregated_specs['door_thickness'] = specs['thickness']
            
            # Aggregate type
            if specs.get('type') and not aggregated_specs['door_type']:
                aggregated_specs['door_type'] = specs['type']
            
            # Aggregate core
            if specs.get('core') and not aggregated_specs['door_core']:
                aggregated_specs['door_core'] = specs['core']
            
            # Aggregate edging
            if specs.get('edging') and not aggregated_specs['door_edging']:
                aggregated_specs['door_edging'] = specs['edging']
            
            # Aggregate decorative
            if specs.get('decorative') and not aggregated_specs['decorative_line']:
                aggregated_specs['decorative_line'] = specs['decorative']
            
            # Aggregate frame type
            if specs.get('frame_type') and not aggregated_specs['frame_type']:
                aggregated_specs['frame_type'] = specs['frame_type']
        
        # If no door size found yet, try to extract from full text with door priority
        if not aggregated_specs['door_size']:
            full_text = extracted.get('full_text', '')
            # First try to find door-specific size mentions
            import re
            door_size_match = re.search(r'door\s+size[:\s]*([^\n]+)', full_text, re.IGNORECASE)
            if door_size_match:
                door_size_text = door_size_match.group(1)
                extracted_size = self.extract_size(door_size_text)
                if extracted_size:
                    aggregated_specs['door_size'] = extracted_size 
                    aggregated_specs['item_size_0'] = extracted_size
                    print(f"EXTRACTED door size from door-specific text: {extracted_size}")
            else:
                # Fallback to general size extraction
                extracted_size = self.extract_size(full_text)
                if extracted_size:
                    aggregated_specs['door_size'] = extracted_size
                    aggregated_specs['item_size_0'] = extracted_size
                    print(f"EXTRACTED door size from full text: {extracted_size}")
        
        # Add aggregated specs to extracted data
        extracted.update(aggregated_specs)
        
        return extracted
    
    def cleanup_customer_name(self, extracted: Dict) -> Dict:
        """Final cleanup to ensure customer name is not Sendora-related"""
        
        customer_name = extracted.get('customer', {}).get('name', '')
        
        # If customer name is Sendora-related, clear it
        if customer_name and self.is_sendora_text(customer_name):
            print(f"WARNING: Removing Sendora-related customer name: {customer_name}")
            extracted['customer']['name'] = None
            
            # Try to find actual customer name in the full text
            text = extracted.get('full_text', '')
            if text:
                # Look for "Bill To:" or similar patterns
                import re
                patterns = [
                    r'bill\s+to[:\s]*\n\s*([^\n]+(?:sdn\s+bhd|enterprise|trading)[^\n]*)',
                    r'customer[:\s]*\n\s*([^\n]+(?:sdn\s+bhd|enterprise|trading)[^\n]*)',
                    r'sold\s+to[:\s]*\n\s*([^\n]+(?:sdn\s+bhd|enterprise|trading)[^\n]*)',
                ]
                
                for pattern in patterns:
                    match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
                    if match:
                        potential_name = match.group(1).strip().upper()
                        if not self.is_sendora_text(potential_name):
                            extracted['customer']['name'] = potential_name
                            print(f"Found actual customer name: {potential_name}")
                            break
        
        return extracted
    
    def fallback_processing(self, file_path: str) -> Dict[str, Any]:
        """Fallback processing when Google Document AI is not available"""
        
        print("Using fallback processing (Google Document AI not configured)")
        
        # Return basic structure with empty data
        return {
            'invoice_number': 'DEMO-001',
            'po_number': 'PO-2024-001',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'vendor': {'name': 'Demo Vendor'},
            'customer': {'name': 'Demo Customer SDN BHD'},
            'line_items': [
                {
                    'description': 'Sample Door 850MM x 2100MM',
                    'quantity': '1',
                    'unit_price': '500.00',
                    'amount': '500.00',
                    'size': '850MM x 2100MM',
                    'specifications': {
                        'thickness': '43mm',
                        'type': 'S/L',
                        'core': 'honeycomb'
                    }
                }
            ],
            'total': '500.00',
            'currency': 'MYR',
            'confidence_scores': {},
            'full_text': 'Demo document - Google Document AI not configured',
            'document_type': 'invoice'
        }


# Test function
if __name__ == "__main__":
    processor = GoogleDocumentProcessor()
    
    # Test with a sample file
    test_file = "../uploads/sample_invoice.pdf"
    if os.path.exists(test_file):
        result = processor.process_document(test_file)
        print(json.dumps(result, indent=2))
    else:
        print("Test file not found. Using fallback demo data.")
        result = processor.fallback_processing("")
        print(json.dumps(result, indent=2))