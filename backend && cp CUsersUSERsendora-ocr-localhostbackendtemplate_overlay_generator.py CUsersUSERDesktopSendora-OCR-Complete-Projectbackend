"""
Enhanced Azure Form Recognizer Integration for Sendora OCR
Specialized for Malaysian door manufacturing documents
"""

import os
import io
import json
import time
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import requests
from PIL import Image
import cv2
import numpy as np


class SendoraFormRecognizer:
    """Azure Form Recognizer client optimized for Sendora documents"""
    
    def __init__(self):
        self.endpoint = "https://sendoraformparser.cognitiveservices.azure.com/"
        self.api_key = "6LVEZiaOrkHK60L5Rqn1trreA0wiSQSizvI1QQSizvI1QQjpfp6FV8G7VqcYJQQJ99BHACqBBLyXJ3w3AAALACOGwtQN"
        self.api_version = "2023-07-31"
        self.headers = {
            'Ocp-Apim-Subscription-Key': self.api_key,
            'Content-Type': 'application/octet-stream'
        }
        
        # Malaysian business document patterns
        self.malaysian_patterns = {
            'company_indicators': ['sdn bhd', 'sdn.bhd', 'bhd', 'enterprise', 'trading'],
            'currency_patterns': ['rm', 'ringgit', 'sen'],
            'po_patterns': ['purchase order', 'po no', 'po#', 'po number'],
            'invoice_patterns': ['invoice no', 'inv no', 'invoice#', 'bil no'],
            'quotation_patterns': ['quotation', 'quote no', 'quotation no', 'quote#'],
            'door_terms': ['door', 'pintu', 'leaf', 'panel', 'swing', 'sliding'],
            'frame_terms': ['frame', 'bingkai', 'jamb', 'casing', 'architrave'],
            'material_terms': ['solid wood', 'plywood', 'mdf', 'particle board', 'veneer', 'laminate']
        }
        
        print("Azure Form Recognizer initialized for Sendora documents")
    
    def preprocess_document(self, image_path: str) -> str:
        """Enhanced preprocessing for Malaysian business documents"""
        try:
            # Load image
            image = cv2.imread(image_path)
            if image is None:
                return image_path
            
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Enhance contrast for better text recognition
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            enhanced = clahe.apply(gray)
            
            # Noise reduction
            denoised = cv2.bilateralFilter(enhanced, 9, 75, 75)
            
            # Adaptive thresholding for varying lighting conditions
            binary = cv2.adaptiveThreshold(
                denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
            )
            
            # Morphological operations to clean up text
            kernel = np.ones((1,1), np.uint8)
            cleaned = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
            
            # Save enhanced image
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            enhanced_path = os.path.join(os.path.dirname(image_path), f"{base_name}_enhanced.png")
            cv2.imwrite(enhanced_path, cleaned)
            
            return enhanced_path
            
        except Exception as e:
            print(f"Preprocessing error: {e}")
            return image_path
    
    def analyze_document(self, image_path: str) -> Dict[str, Any]:
        """Analyze document using Azure Form Recognizer"""
        try:
            # Preprocess document for better accuracy
            processed_path = self.preprocess_document(image_path)
            
            # Read the processed image
            with open(processed_path, 'rb') as image_file:
                image_data = image_file.read()
            
            # Submit for analysis
            analyze_url = f"{self.endpoint}formrecognizer/v3.1/layout/analyze"
            
            response = requests.post(
                analyze_url,
                headers=self.headers,
                data=image_data
            )
            
            if response.status_code != 202:
                raise Exception(f"Form Recognizer API error: {response.status_code} - {response.text}")
            
            # Get operation location
            operation_location = response.headers['Operation-Location']
            
            # Poll for results
            result = self._poll_for_result(operation_location)
            
            # Process and enhance the results
            enhanced_result = self._enhance_extraction_results(result)
            
            return enhanced_result
            
        except Exception as e:
            print(f"Azure Form Recognizer error: {e}")
            # Fallback to demo mode
            return self._create_demo_result(image_path)
    
    def _poll_for_result(self, operation_location: str, max_wait: int = 30) -> Dict:
        """Poll for analysis completion"""
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            response = requests.get(operation_location, headers={'Ocp-Apim-Subscription-Key': self.api_key})
            
            if response.status_code == 200:
                result = response.json()
                if result['status'] == 'succeeded':
                    return result
                elif result['status'] == 'failed':
                    raise Exception(f"Analysis failed: {result.get('error', 'Unknown error')}")
            
            time.sleep(1)
        
        raise Exception("Analysis timed out")
    
    def _enhance_extraction_results(self, raw_result: Dict) -> Dict[str, Any]:
        """Enhance and structure the extraction results for Sendora use"""
        
        # Extract text content
        full_text = ""
        text_blocks = []
        tables = []
        key_value_pairs = {}
        
        if 'analyzeResult' in raw_result:
            analyze_result = raw_result['analyzeResult']
            
            # Extract text from pages
            if 'pages' in analyze_result:
                for page in analyze_result['pages']:
                    if 'lines' in page:
                        for line in page['lines']:
                            full_text += line['content'] + "\n"
                            
                            # Create text blocks with coordinates
                            text_blocks.append({
                                'content': line['content'],
                                'confidence': line.get('confidence', 0.9),
                                'bounding_box': line.get('boundingBox', []),
                                'page': page.get('pageNumber', 1)
                            })
            
            # Extract tables
            if 'tables' in analyze_result:
                for table in analyze_result['tables']:
                    table_data = []
                    if 'cells' in table:
                        # Organize cells into rows and columns
                        max_row = max([cell.get('rowIndex', 0) for cell in table['cells']]) + 1
                        max_col = max([cell.get('columnIndex', 0) for cell in table['cells']]) + 1
                        
                        table_grid = [['' for _ in range(max_col)] for _ in range(max_row)]
                        
                        for cell in table['cells']:
                            row = cell.get('rowIndex', 0)
                            col = cell.get('columnIndex', 0)
                            content = cell.get('content', '')
                            table_grid[row][col] = content
                        
                        table_data = table_grid
                    
                    tables.append({
                        'data': table_data,
                        'row_count': table.get('rowCount', 0),
                        'column_count': table.get('columnCount', 0)
                    })
            
            # Extract key-value pairs
            if 'keyValuePairs' in analyze_result:
                for kvp in analyze_result['keyValuePairs']:
                    key = kvp.get('key', {}).get('content', '')
                    value = kvp.get('value', {}).get('content', '')
                    if key and value:
                        key_value_pairs[key.lower().strip()] = value.strip()
        
        # Apply Sendora-specific field extraction
        structured_data = self._extract_sendora_fields(full_text, text_blocks, tables, key_value_pairs)
        
        return {
            'full_text': full_text.strip(),
            'text_blocks': text_blocks,
            'tables': tables,
            'key_value_pairs': key_value_pairs,
            'structured_data': structured_data,
            'document_type': self._determine_document_type(full_text),
            'confidence': self._calculate_overall_confidence(text_blocks),
            'processing_time': datetime.now().isoformat(),
            'api_provider': 'azure_form_recognizer'
        }
    
    def _extract_sendora_fields(self, text: str, blocks: List, tables: List, kvp: Dict) -> Dict[str, Any]:
        """Extract Sendora-specific fields for JO generation"""
        
        text_lower = text.lower()
        extracted = {}
        
        # Document identification
        extracted['document_info'] = self._extract_document_info(text, kvp)
        
        # Company and customer information
        extracted['company_info'] = self._extract_company_info(text, blocks)
        
        # Product specifications
        extracted['product_specs'] = self._extract_product_specifications(text, tables)
        
        # Financial information
        extracted['financial_info'] = self._extract_financial_info(text, kvp)
        
        # Door-specific information
        extracted['door_specs'] = self._extract_door_specifications(text, tables)
        
        # Frame-specific information
        extracted['frame_specs'] = self._extract_frame_specifications(text, tables)
        
        # Location and installation details
        extracted['location_info'] = self._extract_location_info(text, blocks)
        
        return extracted
    
    def _extract_document_info(self, text: str, kvp: Dict) -> Dict[str, str]:
        """Extract document identification information"""
        import re
        
        doc_info = {}
        text_lower = text.lower()
        
        # Document numbers
        po_patterns = [
            r'po\s*no[:\.]?\s*([A-Z0-9\-/]+)',
            r'purchase\s*order\s*no[:\.]?\s*([A-Z0-9\-/]+)',
            r'po[:\#]?\s*([A-Z0-9\-/]{3,})'
        ]
        
        for pattern in po_patterns:
            match = re.search(pattern, text_lower, re.IGNORECASE)
            if match:
                doc_info['po_number'] = match.group(1).upper()
                break
        
        # Invoice numbers
        inv_patterns = [
            r'invoice\s*no[:\.]?\s*([A-Z0-9\-/]+)',
            r'inv\s*no[:\.]?\s*([A-Z0-9\-/]+)',
            r'invoice[:\#]?\s*([A-Z0-9\-/]{3,})'
        ]
        
        for pattern in inv_patterns:
            match = re.search(pattern, text_lower, re.IGNORECASE)
            if match:
                doc_info['invoice_number'] = match.group(1).upper()
                break
        
        # Quotation numbers
        quote_patterns = [
            r'quotation\s*no[:\.]?\s*([A-Z0-9\-/]+)',
            r'quote\s*no[:\.]?\s*([A-Z0-9\-/]+)'
        ]
        
        for pattern in quote_patterns:
            match = re.search(pattern, text_lower, re.IGNORECASE)
            if match:
                doc_info['quotation_number'] = match.group(1).upper()
                break
        
        # Dates
        date_patterns = [
            r'date[:\.]?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})'
        ]
        
        for pattern in date_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                doc_info['date'] = matches[0]
                break
        
        return doc_info
    
    def _extract_company_info(self, text: str, blocks: List) -> Dict[str, str]:
        """Extract company and customer information"""
        import re
        
        company_info = {}
        
        # Malaysian company patterns
        company_patterns = [
            r'([A-Z][A-Za-z\s&\.]+(?:SDN\s*BHD|BHD|ENTERPRISE|TRADING))',
            r'([A-Z][A-Za-z\s&\.]{10,})'
        ]
        
        for pattern in company_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                # Filter out common words and keep likely company names
                for match in matches:
                    if len(match) > 5 and any(indicator in match.lower() for indicator in self.malaysian_patterns['company_indicators']):
                        company_info['company_name'] = match.strip()
                        break
                if 'company_name' in company_info:
                    break
        
        # Address extraction
        address_patterns = [
            r'(?:address|alamat)[:\.]?\s*([A-Za-z0-9\s,\-\.]{20,})',
            r'(\d+[A-Za-z]?,?\s*[A-Za-z\s,\-\.]{10,}\d{5})'  # Malaysian postcode pattern
        ]
        
        for pattern in address_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                company_info['address'] = match.group(1).strip()
                break
        
        return company_info
    
    def _extract_product_specifications(self, text: str, tables: List) -> List[Dict]:
        """Extract product specifications from text and tables"""
        import re
        
        products = []
        
        # Door dimensions pattern
        dimension_patterns = [
            r'(\d+)\s*mm?\s*[xX×]\s*(\d+)\s*mm?\s*[xX×]?\s*(\d+)?mm?',
            r'(\d+)[\'\"]\s*[xX×]\s*(\d+)[\'\"]\s*[xX×]?\s*(\d+)?[\'\"]+',
            r'(\d+)\s*[xX×]\s*(\d+)\s*[xX×]?\s*(\d+)?'
        ]
        
        for pattern in dimension_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                width, height, thickness = match
                if width and height:
                    products.append({
                        'type': 'door',
                        'width': int(width),
                        'height': int(height),
                        'thickness': int(thickness) if thickness else None,
                        'unit': 'mm'
                    })
        
        # Extract from tables if available
        for table in tables:
            table_products = self._extract_products_from_table(table['data'])
            products.extend(table_products)
        
        return products
    
    def _extract_products_from_table(self, table_data: List[List]) -> List[Dict]:
        """Extract products from table structure"""
        products = []
        
        if not table_data or len(table_data) < 2:
            return products
        
        # Find headers
        headers = [cell.lower().strip() for cell in table_data[0]]
        
        # Common column mappings
        column_map = {}
        for i, header in enumerate(headers):
            if 'size' in header or 'dimension' in header:
                column_map['size'] = i
            elif 'thickness' in header:
                column_map['thickness'] = i
            elif 'type' in header:
                column_map['type'] = i
            elif 'material' in header:
                column_map['material'] = i
            elif 'qty' in header or 'quantity' in header:
                column_map['quantity'] = i
        
        # Extract data rows
        for row in table_data[1:]:
            if len(row) > max(column_map.values(), default=-1):
                product = {}
                
                for field, col_index in column_map.items():
                    if col_index < len(row):
                        product[field] = row[col_index].strip()
                
                if product:
                    products.append(product)
        
        return products
    
    def _extract_financial_info(self, text: str, kvp: Dict) -> Dict[str, Any]:
        """Extract financial information"""
        import re
        
        financial = {}
        
        # Currency amounts
        amount_patterns = [
            r'rm\s*(\d+(?:,\d{3})*(?:\.\d{2})?)',
            r'total[:\s]*rm\s*(\d+(?:,\d{3})*(?:\.\d{2})?)',
            r'amount[:\s]*rm\s*(\d+(?:,\d{3})*(?:\.\d{2})?)'
        ]
        
        for pattern in amount_patterns:
            match = re.search(pattern, text.lower())
            if match:
                amount_str = match.group(1).replace(',', '')
                try:
                    financial['total_amount'] = float(amount_str)
                    financial['currency'] = 'RM'
                    break
                except ValueError:
                    continue
        
        return financial
    
    def _extract_door_specifications(self, text: str, tables: List) -> Dict[str, Any]:
        """Extract door-specific specifications"""
        door_specs = {}
        text_lower = text.lower()
        
        # Door types
        door_types = ['swing', 'sliding', 'folding', 'bi-fold', 'pivot']
        for door_type in door_types:
            if door_type in text_lower:
                door_specs['door_type'] = door_type
                break
        
        # Door core types
        core_types = ['solid timber', 'honeycomb', 'solid tubular core', 'metal skeleton']
        for core_type in core_types:
            if core_type in text_lower:
                door_specs['core_type'] = core_type
                break
        
        # Edging types
        edging_types = ['abs edging', 'na lipping', 'no edging']
        for edging_type in edging_types:
            if edging_type in text_lower:
                door_specs['edging'] = edging_type
                break
        
        return door_specs
    
    def _extract_frame_specifications(self, text: str, tables: List) -> Dict[str, Any]:
        """Extract frame-specific specifications"""
        frame_specs = {}
        text_lower = text.lower()
        
        # Frame types
        if 'inner' in text_lower and 'outer' in text_lower:
            frame_specs['frame_options'] = ['inner', 'outer']
        elif 'inner' in text_lower:
            frame_specs['frame_options'] = ['inner']
        elif 'outer' in text_lower:
            frame_specs['frame_options'] = ['outer']
        
        # Frame profile
        if 'frame profile' in text_lower:
            frame_specs['has_profile'] = True
        
        return frame_specs
    
    def _extract_location_info(self, text: str, blocks: List) -> Dict[str, Any]:
        """Extract location and installation information"""
        import re
        
        location_info = {}
        
        # Location patterns
        location_patterns = [
            r'location[:\.]?\s*([A-Za-z0-9\s,\-\.]{5,50})',
            r'site[:\.]?\s*([A-Za-z0-9\s,\-\.]{5,50})',
            r'project[:\.]?\s*([A-Za-z0-9\s,\-\.]{5,50})'
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                location_info['location'] = match.group(1).strip()
                break
        
        return location_info
    
    def _determine_document_type(self, text: str) -> str:
        """Determine document type based on content"""
        text_lower = text.lower()
        
        if any(pattern in text_lower for pattern in self.malaysian_patterns['invoice_patterns']):
            return 'invoice'
        elif any(pattern in text_lower for pattern in self.malaysian_patterns['po_patterns']):
            return 'purchase_order'
        elif any(pattern in text_lower for pattern in self.malaysian_patterns['quotation_patterns']):
            return 'quotation'
        else:
            return 'unknown'
    
    def _calculate_overall_confidence(self, blocks: List) -> float:
        """Calculate overall confidence score"""
        if not blocks:
            return 0.0
        
        confidences = [block.get('confidence', 0.9) for block in blocks]
        return sum(confidences) / len(confidences)
    
    def _create_demo_result(self, image_path: str) -> Dict[str, Any]:
        """Create demo result when API fails"""
        return {
            'full_text': """DEMO MODE - AZURE FORM RECOGNIZER
SENDORA GROUP SDN BHD
Invoice No: INV-2025-003
Date: 15/01/2025
PO No: PO-2025-SG-001

Door Specifications:
- Door Size: 850MM x 2021MM
- Thickness: 43mm
- Door Type: S/L
- Door Core: Honeycomb
- Edging: NA Lipping
- Location: Main Entrance

Frame Specifications:
- Frame Size: 850MM x 2021MM
- Frame Type: Inner
- Frame Profile: T-bar

Total Amount: RM 2,850.00""",
            'structured_data': {
                'document_info': {
                    'invoice_number': 'INV-2025-003',
                    'po_number': 'PO-2025-SG-001',
                    'date': '15/01/2025'
                },
                'company_info': {
                    'company_name': 'SENDORA GROUP SDN BHD'
                },
                'product_specs': [
                    {
                        'type': 'door',
                        'width': 850,
                        'height': 2021,
                        'thickness': 43,
                        'unit': 'mm'
                    }
                ],
                'door_specs': {
                    'door_type': 'S/L',
                    'core_type': 'honeycomb',
                    'edging': 'na lipping'
                },
                'frame_specs': {
                    'frame_options': ['inner'],
                    'has_profile': True
                },
                'financial_info': {
                    'total_amount': 2850.00,
                    'currency': 'RM'
                }
            },
            'document_type': 'invoice',
            'confidence': 0.95,
            'api_provider': 'demo_mode',
            'processing_time': datetime.now().isoformat()
        }