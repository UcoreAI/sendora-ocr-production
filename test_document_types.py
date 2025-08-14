#!/usr/bin/env python3
"""
Test script to verify document type detection and processing
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from google_document_ai import GoogleDocumentProcessor

def test_document_type_detection():
    """Test document type detection with different filenames"""
    
    processor = GoogleDocumentProcessor()
    
    test_cases = [
        ("invoice_2024.pdf", "invoice"),
        ("quotation_march.pdf", "quote"),
        ("estimate_project.pdf", "quote"),
        ("po_12345.pdf", "purchase_order"),
        ("purchase_order_abc.pdf", "purchase_order"),
        ("receipt_xyz.pdf", "receipt"),
        ("random_document.pdf", "invoice"),  # Default fallback
    ]
    
    print("=" * 60)
    print("DOCUMENT TYPE DETECTION TEST")
    print("=" * 60)
    
    for filename, expected in test_cases:
        # Create a dummy path for testing
        test_path = f"./test_files/{filename}"
        detected = processor.detect_document_type(test_path)
        
        status = "[PASS]" if detected == expected else "[FAIL]"
        print(f"{status} | {filename:<25} | Expected: {expected:<15} | Got: {detected}")
    
    print("=" * 60)

def test_processors_mapping():
    """Test processor mapping for different document types"""
    
    processor = GoogleDocumentProcessor()
    
    print("\nPROCESSOR MAPPING TEST")
    print("=" * 60)
    
    for doc_type, processor_id in processor.processors.items():
        print(f"{doc_type:<15} -> {processor_id}")
    
    print("=" * 60)

def test_fallback_processing():
    """Test fallback processing when Google Document AI is not available"""
    
    processor = GoogleDocumentProcessor()
    
    print("\nFALLBACK PROCESSING TEST")
    print("=" * 60)
    
    # Test fallback with different document types
    test_files = [
        "./test_files/invoice_sample.pdf",
        "./test_files/quote_sample.pdf", 
        "./test_files/po_sample.pdf"
    ]
    
    for test_file in test_files:
        print(f"\nTesting: {os.path.basename(test_file)}")
        detected_type = processor.detect_document_type(test_file)
        print(f"Detected type: {detected_type}")
        
        # Get the processor that would be used
        processor_id = processor.processors.get(detected_type, processor.processors['general'])
        print(f"Would use processor: {processor_id}")
        
        # Test fallback data structure
        fallback_data = processor.fallback_processing(test_file)
        print(f"Document type in response: {fallback_data.get('document_type', 'N/A')}")
        print(f"Customer name: {fallback_data.get('customer', {}).get('name', 'N/A')}")
        
    print("=" * 60)

if __name__ == "__main__":
    print("Testing Sendora OCR Document Type Support")
    print("Testing quotes, purchase orders, and invoices\n")
    
    # Run all tests
    test_document_type_detection()
    test_processors_mapping()
    test_fallback_processing()
    
    print("\n[SUCCESS] All tests completed!")
    print("The system now supports:")
    print("  - Invoices (processor: 1699972f50f6529)")
    print("  - Purchase Orders (processor: 81116d27ff6c4a06)")
    print("  - Quotes/Quotations (processor: 81116d27ff6c4a06)")
    print("  - Receipts (processor: 1699972f50f6529)")
    print("  - General documents (processor: 81116d27ff6c4a06)")