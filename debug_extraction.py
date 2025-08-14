#!/usr/bin/env python3
"""
Debug script to test Google Document AI extraction
"""

import sys
import os
import json

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from google_document_ai import GoogleDocumentProcessor
from simple_working_template import SimpleWorkingTemplate

def debug_latest_invoice():
    """Debug the latest uploaded invoice"""
    
    # Find latest invoice
    uploads_dir = os.path.join(os.path.dirname(__file__), 'uploads')
    invoice_files = [f for f in os.listdir(uploads_dir) if f.endswith('.pdf')]
    
    if not invoice_files:
        print("No invoice files found")
        return
    
    # Get the latest file
    latest_file = max(invoice_files)
    file_path = os.path.join(uploads_dir, latest_file)
    
    print(f"Debugging: {latest_file}")
    print("=" * 50)
    
    # Process with Google Document AI
    processor = GoogleDocumentProcessor()
    extracted_data = processor.process_document(file_path)
    
    # Print extracted data
    print("EXTRACTED DATA:")
    for key, value in extracted_data.items():
        if key != 'full_text':  # Skip full text for readability
            print(f"{key}: {value}")
    
    print("\nLINE ITEMS:")
    for i, item in enumerate(extracted_data.get('line_items', [])):
        print(f"Item {i+1}:")
        for k, v in item.items():
            print(f"  {k}: {v}")
    
    # Test template generation
    print("\n" + "=" * 50)
    print("TESTING TEMPLATE GENERATION")
    
    template_gen = SimpleWorkingTemplate()
    
    # Create mock data based on extraction
    mock_data = {
        'invoice_number': extracted_data.get('invoice_number', 'TEST-001'),
        'customer_name': extracted_data.get('customer', {}).get('name', 'TEST CUSTOMER'),
        'document_date': extracted_data.get('date', '2025-08-14'),
        'delivery_date': '',
        'po_number': extracted_data.get('po_number', ''),
        'measure_by': '',
        'door_thickness': extracted_data.get('door_thickness', ''),
        'door_type': extracted_data.get('door_type', ''),
        'door_core': extracted_data.get('door_core', ''),
        'door_edging': extracted_data.get('door_edging', ''),
        'decorative_line': extracted_data.get('decorative_line', ''),
        'item_desc_0': extracted_data.get('item_desc_0', ''),
        'item_size_0': extracted_data.get('item_size_0', ''),
        'door_size': extracted_data.get('door_size', ''),
        'line_items': extracted_data.get('line_items', [])
    }
    
    # Add line item data if available
    if extracted_data.get('line_items'):
        first_item = extracted_data['line_items'][0]
        mock_data['item_desc_0'] = first_item.get('description', '')
        mock_data['item_size_0'] = first_item.get('size', '')
    
    print("MOCK DATA FOR TEMPLATE:")
    for key, value in mock_data.items():
        if key != 'line_items':
            print(f"{key}: {value}")
    
    # Generate template
    result = template_gen.create_working_template(mock_data)
    
    print("\nTemplate generation completed")

if __name__ == "__main__":
    debug_latest_invoice()