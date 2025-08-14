"""
Test Google Document AI integration
Run this to verify the setup is working
"""

import os
import sys
sys.path.append('backend')

from google_document_ai import GoogleDocumentProcessor

def test_google_document_ai():
    """Test Google Document AI with demo data"""
    
    print("=" * 60)
    print("Testing Google Document AI Integration")
    print("=" * 60)
    
    # Initialize processor
    processor = GoogleDocumentProcessor()
    
    # Check if we have a test file
    test_files = [
        'uploads/20250813_083125_INVOICE.pdf',
        'uploads/sample_invoice.pdf',
        'test_invoice.pdf'
    ]
    
    test_file = None
    for file in test_files:
        if os.path.exists(file):
            test_file = file
            break
    
    if test_file:
        print(f"\nProcessing test file: {test_file}")
        result = processor.process_document(test_file)
    else:
        print("\nNo test file found. Using fallback demo mode.")
        result = processor.fallback_processing("")
    
    # Display results
    print("\n" + "=" * 60)
    print("EXTRACTED DATA:")
    print("=" * 60)
    
    print(f"\nInvoice Number: {result.get('invoice_number', 'N/A')}")
    print(f"PO Number: {result.get('po_number', 'N/A')}")
    print(f"Date: {result.get('date', 'N/A')}")
    print(f"Customer: {result.get('customer', {}).get('name', 'N/A')}")
    print(f"Currency: {result.get('currency', 'N/A')}")
    print(f"Total: {result.get('total', 'N/A')}")
    
    print("\nLine Items:")
    for i, item in enumerate(result.get('line_items', []), 1):
        print(f"\n  Item {i}:")
        print(f"    Description: {item.get('description', 'N/A')}")
        print(f"    Size: {item.get('size', 'N/A')}")
        print(f"    Quantity: {item.get('quantity', 'N/A')}")
        print(f"    Specifications: {item.get('specifications', {})}")
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)
    
    return result

if __name__ == "__main__":
    test_google_document_ai()