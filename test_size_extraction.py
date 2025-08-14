#!/usr/bin/env python3
"""
Test size extraction regex patterns
"""

import re

def test_extract_size(text: str):
    """Test size extraction patterns"""
    
    print(f"Testing text: '{text}'")
    print("=" * 50)
    
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
    
    for i, pattern in enumerate(patterns):
        print(f"Pattern {i+1}: {pattern}")
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            print(f"  MATCHED: {match.groups()}")
            print(f"  Pattern has 'ft': {'ft' in pattern.lower()}")
            
            if '[fF][tT]' in pattern or 'ft' in pattern.lower():
                # Handle feet conversion
                if len(match.groups()) == 3:  # 43MM X 3FT X 8FT format
                    thickness = match.group(1)
                    width_ft = int(match.group(2))
                    height_ft = int(match.group(3))
                    width_mm = width_ft * 305  # 1 foot ≈ 305mm (rounded)
                    height_mm = height_ft * 305
                    result = f"{width_mm}MM x {height_mm}MM"
                    print(f"  CONVERTED: {result}")
                elif len(match.groups()) == 2:
                    if 'mm' in match.group(1).lower():
                        # Mixed: 43mm x 8ft
                        thickness = match.group(1).replace('mm', '').replace('MM', '')
                        height_ft = int(match.group(2))
                        height_mm = height_ft * 305
                        result = f"{thickness}MM x {height_mm}MM"
                        print(f"  CONVERTED: {result}")
                    else:
                        # Both in feet: 3ft x 8ft  
                        width_ft = int(match.group(1))
                        height_ft = int(match.group(2))
                        width_mm = width_ft * 305
                        height_mm = height_ft * 305
                        result = f"{width_mm}MM x {height_mm}MM"
                        print(f"  CONVERTED: {result}")
            else:
                # MM patterns
                result = f"{match.group(1)}MM x {match.group(2)}MM"
                print(f"  RESULT: {result}")
            
            return  # Stop at first match
        else:
            print(f"  No match")
    
    print("No patterns matched!")

if __name__ == "__main__":
    # Test the actual text from the invoice
    test_text1 = "DOOR SIZE: 43MM X 3FT X 8FT"
    test_extract_size(test_text1)
    
    print("\n" + "=" * 60 + "\n")
    
    test_text2 = "43MM X 3FT X 8FT"
    test_extract_size(test_text2)