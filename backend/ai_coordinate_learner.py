"""
AI Coordinate Learning System
Learns precise field positions from your filled JO sample
"""

import fitz  # PyMuPDF
import json
import cv2
import numpy as np
from typing import Dict, List, Tuple, Any
import re

class AICoordinateLearner:
    """Learn field positions from filled JO sample using computer vision"""
    
    def __init__(self):
        self.sample_pdf = r'C:\Users\USER\Desktop\Project management\Sendora\Material\JOB ORDER FORM.pdf'
        self.learned_coordinates = {}
        
    def analyze_sample_form(self) -> Dict[str, Any]:
        """Analyze the filled sample form to learn field positions"""
        
        print("Analyzing sample JO form to learn field positions...")
        
        # Open the sample PDF
        doc = fitz.open(self.sample_pdf)
        
        coordinates = {
            'page_size': None,
            'header_fields': {},
            'door_table': {
                'rows': [],
                'columns': {},
                'checkboxes': {}
            },
            'frame_table': {
                'rows': [],
                'columns': {},
                'checkboxes': {}
            }
        }
        
        # Analyze Page 1 (DOOR page)
        page1 = doc[0]
        coordinates['page_size'] = [page1.rect.width, page1.rect.height]
        
        # Learn header field positions from Page 1
        self.learn_header_positions(page1, coordinates)
        
        # Learn door table structure from Page 1
        self.learn_door_table_structure(page1, coordinates)
        
        # Analyze Page 2 (FRAME page) if it exists
        if len(doc) > 1:
            page2 = doc[1]
            self.learn_frame_table_structure(page2, coordinates)
        
        doc.close()
        
        # Save learned coordinates
        self.save_learned_coordinates(coordinates)
        
        return coordinates
    
    def learn_header_positions(self, page, coordinates: Dict):
        """Learn header field positions from the sample"""
        
        # Get all text on the page with positions
        text_dict = page.get_text("dict")
        
        # If no text found, this might be an image-based PDF
        if not text_dict.get('blocks'):
            print("No text blocks found - PDF might be image-based")
            # Use a fallback method with hardcoded positions based on standard JO layout
            self.use_fallback_positions(coordinates)
            return
        
        # Look for header labels and their positions
        header_labels = {
            'Job Order No': 'job_order_no',
            'Job Order Date': 'job_order_date', 
            'PO NO': 'po_no',
            'Delivery Date': 'delivery_date',
            'Customer Name': 'customer_name',
            'Measure By': 'measure_by'
        }
        
        for block in text_dict.get('blocks', []):
            if 'lines' not in block:
                continue
                
            for line in block['lines']:
                for span in line['spans']:
                    text = span['text'].strip()
                    
                    # Check if this text matches a header label
                    for label, field_name in header_labels.items():
                        if label.lower() in text.lower():
                            # Found a header label, now find where data should go
                            label_bbox = span['bbox']
                            
                            # Data position is typically to the right of the label
                            # Look for actual data in the sample
                            data_position = self.find_data_position_for_label(
                                page, label_bbox, field_name
                            )
                            
                            coordinates['header_fields'][field_name] = {
                                'label_position': {
                                    'x': label_bbox[0],
                                    'y': label_bbox[1], 
                                    'width': label_bbox[2] - label_bbox[0],
                                    'height': label_bbox[3] - label_bbox[1]
                                },
                                'data_position': data_position,
                                'font_size': span['size']
                            }
    
    def find_data_position_for_label(self, page, label_bbox: Tuple, field_name: str) -> Dict:
        """Find where data appears relative to the label"""
        
        # Get all text near the label
        text_dict = page.get_text("dict")
        label_right = label_bbox[2]
        label_y = label_bbox[1]
        
        # Look for data in the same row, to the right of the label
        for block in text_dict.get('blocks', []):
            if 'lines' not in block:
                continue
                
            for line in block['lines']:
                for span in line['spans']:
                    span_bbox = span['bbox']
                    text = span['text'].strip()
                    
                    # Check if this text is in the same row and to the right
                    if (abs(span_bbox[1] - label_y) < 10 and  # Same row (within 10 points)
                        span_bbox[0] > label_right and        # To the right of label
                        text and                              # Has content
                        not self.is_label_text(text)):       # Not another label
                        
                        return {
                            'x': span_bbox[0],
                            'y': span_bbox[1],
                            'width': span_bbox[2] - span_bbox[0],
                            'height': span_bbox[3] - span_bbox[1],
                            'sample_text': text
                        }
        
        # If no data found, estimate position
        return {
            'x': label_right + 20,  # 20 points to the right
            'y': label_y,
            'width': 150,
            'height': 12,
            'sample_text': None
        }
    
    def learn_door_table_structure(self, page, coordinates: Dict):
        """Learn door table structure and positions"""
        
        # Find the door table by looking for specific text patterns
        text_dict = page.get_text("dict")
        
        # Door table headers to look for
        door_headers = [
            'LAMINATE CODE', 'DOOR THICKNESS', 'DOOR SIZE', 'DOOR TYPE', 
            'DOOR CORE', 'EDGING', 'DECORATIVE LINE', 'DESIGN NAME',
            'OPEN HOLE TYPE', 'DRAWING REMARK'
        ]
        
        # Find table header positions
        header_positions = {}
        for block in text_dict.get('blocks', []):
            if 'lines' not in block:
                continue
                
            for line in block['lines']:
                for span in line['spans']:
                    text = span['text'].strip()
                    
                    for header in door_headers:
                        if header.lower() in text.lower() or text.upper() in header:
                            header_positions[header] = {
                                'x': span['bbox'][0],
                                'y': span['bbox'][1],
                                'width': span['bbox'][2] - span['bbox'][0]
                            }
        
        coordinates['door_table']['headers'] = header_positions
        
        # Learn row positions by finding actual data rows
        self.learn_door_rows(page, coordinates)
        
        # Learn checkbox positions
        self.learn_door_checkboxes(page, coordinates)
    
    def learn_door_rows(self, page, coordinates: Dict):
        """Learn door table row positions from sample data"""
        
        text_dict = page.get_text("dict")
        
        # Look for laminate codes (like 6S-A057) to identify data rows
        laminate_pattern = r'[0-9]+[A-Z]-[A-Z0-9]+'
        door_rows = []
        
        for block in text_dict.get('blocks', []):
            if 'lines' not in block:
                continue
                
            for line in block['lines']:
                for span in line['spans']:
                    text = span['text'].strip()
                    
                    # Check if this looks like a laminate code
                    if re.match(laminate_pattern, text):
                        row_info = {
                            'y_position': span['bbox'][1],
                            'height': span['bbox'][3] - span['bbox'][1],
                            'laminate_code': text,
                            'laminate_x': span['bbox'][0]
                        }
                        
                        # Find other data in this row
                        row_info.update(self.find_row_data(page, span['bbox']))
                        door_rows.append(row_info)
        
        # Sort rows by Y position
        door_rows.sort(key=lambda x: x['y_position'], reverse=True)  # Top to bottom
        coordinates['door_table']['rows'] = door_rows
    
    def find_row_data(self, page, reference_bbox: Tuple) -> Dict:
        """Find all data in the same row as the reference"""
        
        text_dict = page.get_text("dict")
        row_y = reference_bbox[1]
        row_data = {}
        
        # Look for size patterns (like 850MM x 2021MM)
        size_pattern = r'\d+MM?\s*[xX×]\s*\d+MM?'
        
        for block in text_dict.get('blocks', []):
            if 'lines' not in block:
                continue
                
            for line in block['lines']:
                for span in line['spans']:
                    span_bbox = span['bbox']
                    text = span['text'].strip()
                    
                    # Check if in same row (within 20 points vertically)
                    if abs(span_bbox[1] - row_y) < 20 and text:
                        
                        # Classify the text type
                        if re.search(size_pattern, text):
                            row_data['door_size'] = {
                                'text': text,
                                'x': span_bbox[0],
                                'y': span_bbox[1]
                            }
                        elif 'Location' in text:
                            row_data['location'] = {
                                'text': text,
                                'x': span_bbox[0],
                                'y': span_bbox[1]
                            }
        
        return row_data
    
    def learn_door_checkboxes(self, page, coordinates: Dict):
        """Learn checkbox positions for door specifications"""
        
        # Look for checkbox symbols and their associated text
        text_dict = page.get_text("dict")
        
        checkbox_groups = {
            'door_thickness': ['37mm', '43mm', '48mm'],
            'door_type': ['S/L', 'D/L', 'Unequal D/L'],
            'door_core': ['Honeycomb', 'Solid Tubular Core', 'Solid Timber', 'Metal Skeleton'],
            'edging': ['NA Lipping', 'ABS Edging', 'No Edging'],
            'decorative_line': ['T-bar', 'Groove Line']
        }
        
        checkbox_positions = {}
        
        for group_name, options in checkbox_groups.items():
            checkbox_positions[group_name] = {}
            
            for option in options:
                # Find this option text
                position = self.find_checkbox_option_position(page, option)
                if position:
                    checkbox_positions[group_name][option] = position
        
        coordinates['door_table']['checkboxes'] = checkbox_positions
    
    def find_checkbox_option_position(self, page, option_text: str) -> Dict:
        """Find the position of a checkbox option"""
        
        text_dict = page.get_text("dict")
        
        for block in text_dict.get('blocks', []):
            if 'lines' not in block:
                continue
                
            for line in block['lines']:
                for span in line['spans']:
                    text = span['text'].strip()
                    
                    if option_text.lower() in text.lower():
                        return {
                            'text_x': span['bbox'][0],
                            'text_y': span['bbox'][1],
                            'checkbox_x': span['bbox'][0] - 15,  # Checkbox typically before text
                            'checkbox_y': span['bbox'][1] + 2,   # Slightly below text baseline
                            'font_size': span['size']
                        }
        
        return None
    
    def learn_frame_table_structure(self, page, coordinates: Dict):
        """Learn frame table structure from page 2"""
        
        text_dict = page.get_text("dict")
        
        # Frame table headers
        frame_headers = [
            'FRAME LAMINATE CODE', 'FRAME WIDTH', 'REBATED', 'FRAME SIZE',
            'INNER OR OUTER', 'FRAME PROFILE', 'DRAWING REMARK'
        ]
        
        # Similar process as door table
        header_positions = {}
        for block in text_dict.get('blocks', []):
            if 'lines' not in block:
                continue
                
            for line in block['lines']:
                for span in line['spans']:
                    text = span['text'].strip()
                    
                    for header in frame_headers:
                        if header.lower() in text.lower():
                            header_positions[header] = {
                                'x': span['bbox'][0],
                                'y': span['bbox'][1],
                                'width': span['bbox'][2] - span['bbox'][0]
                            }
        
        coordinates['frame_table'] = {
            'headers': header_positions,
            'rows': self.learn_frame_rows(page),
            'checkboxes': self.learn_frame_checkboxes(page)
        }
    
    def learn_frame_rows(self, page) -> List[Dict]:
        """Learn frame table row positions"""
        
        # Look for frame laminate codes (like 6S-145)
        text_dict = page.get_text("dict")
        frame_rows = []
        
        # Similar to door rows but for frame data
        for block in text_dict.get('blocks', []):
            if 'lines' not in block:
                continue
                
            for line in block['lines']:
                for span in line['spans']:
                    text = span['text'].strip()
                    
                    # Look for laminate codes or "6S-145" pattern
                    if re.match(r'[0-9]+[A-Z]-[0-9]+', text):
                        frame_rows.append({
                            'y_position': span['bbox'][1],
                            'laminate_code': text,
                            'laminate_x': span['bbox'][0]
                        })
        
        return sorted(frame_rows, key=lambda x: x['y_position'], reverse=True)
    
    def learn_frame_checkboxes(self, page) -> Dict:
        """Learn frame checkbox positions"""
        
        # Frame checkboxes are simpler - just INNER/OUTER
        checkbox_positions = {
            'frame_type': {}
        }
        
        for option in ['INNER', 'OUTER']:
            position = self.find_checkbox_option_position(page, option)
            if position:
                checkbox_positions['frame_type'][option] = position
        
        return checkbox_positions
    
    def use_fallback_positions(self, coordinates: Dict):
        """Use hardcoded fallback positions based on standard JO layout"""
        
        print("Using fallback positioning based on standard JO layout")
        
        # Standard A4 page dimensions from the extracted page size
        page_width = coordinates['page_size'][0]  # 594.3
        page_height = coordinates['page_size'][1]  # 840.5
        
        # Header field positions (estimated from typical JO layout)
        coordinates['header_fields'] = {
            'job_order_no': {
                'label_position': {'x': 50, 'y': 100, 'width': 80, 'height': 12},
                'data_position': {'x': 140, 'y': 100, 'width': 120, 'height': 12},
                'font_size': 10
            },
            'job_order_date': {
                'label_position': {'x': 300, 'y': 100, 'width': 90, 'height': 12},
                'data_position': {'x': 400, 'y': 100, 'width': 100, 'height': 12},
                'font_size': 10
            },
            'customer_name': {
                'label_position': {'x': 50, 'y': 130, 'width': 100, 'height': 12},
                'data_position': {'x': 160, 'y': 130, 'width': 300, 'height': 12},
                'font_size': 10
            },
            'po_no': {
                'label_position': {'x': 50, 'y': 160, 'width': 60, 'height': 12},
                'data_position': {'x': 120, 'y': 160, 'width': 120, 'height': 12},
                'font_size': 10
            },
            'delivery_date': {
                'label_position': {'x': 300, 'y': 160, 'width': 90, 'height': 12},
                'data_position': {'x': 400, 'y': 160, 'width': 100, 'height': 12},
                'font_size': 10
            },
            'measure_by': {
                'label_position': {'x': 50, 'y': 190, 'width': 80, 'height': 12},
                'data_position': {'x': 140, 'y': 190, 'width': 150, 'height': 12},
                'font_size': 10
            }
        }
        
        # Door table structure (estimated positions)
        coordinates['door_table']['headers'] = {
            'LAMINATE CODE': {'x': 50, 'y': 250, 'width': 80},
            'DOOR THICKNESS': {'x': 140, 'y': 250, 'width': 70},
            'DOOR SIZE': {'x': 220, 'y': 250, 'width': 80},
            'DOOR TYPE': {'x': 310, 'y': 250, 'width': 60},
            'DOOR CORE': {'x': 380, 'y': 250, 'width': 70},
            'EDGING': {'x': 460, 'y': 250, 'width': 50}
        }
        
        # Sample door rows (typical positions)
        coordinates['door_table']['rows'] = [
            {
                'y_position': 280,
                'height': 25,
                'laminate_code': '6S-A057',
                'laminate_x': 55,
                'door_size': {'text': '850MM x 2100MM', 'x': 225, 'y': 280}
            },
            {
                'y_position': 310,
                'height': 25, 
                'laminate_code': '',
                'laminate_x': 55,
                'door_size': {'text': '', 'x': 225, 'y': 310}
            }
        ]
        
        # Door checkboxes (estimated positions)
        coordinates['door_table']['checkboxes'] = {
            'door_thickness': {
                '37mm': {'checkbox_x': 35, 'checkbox_y': 350, 'text_x': 50, 'text_y': 350, 'font_size': 9},
                '43mm': {'checkbox_x': 95, 'checkbox_y': 350, 'text_x': 110, 'text_y': 350, 'font_size': 9},
                '48mm': {'checkbox_x': 155, 'checkbox_y': 350, 'text_x': 170, 'text_y': 350, 'font_size': 9}
            },
            'door_type': {
                'S/L': {'checkbox_x': 35, 'checkbox_y': 380, 'text_x': 50, 'text_y': 380, 'font_size': 9},
                'D/L': {'checkbox_x': 95, 'checkbox_y': 380, 'text_x': 110, 'text_y': 380, 'font_size': 9},
                'Unequal D/L': {'checkbox_x': 155, 'checkbox_y': 380, 'text_x': 170, 'text_y': 380, 'font_size': 9}
            },
            'door_core': {
                'Honeycomb': {'checkbox_x': 35, 'checkbox_y': 410, 'text_x': 50, 'text_y': 410, 'font_size': 9},
                'Solid Tubular Core': {'checkbox_x': 150, 'checkbox_y': 410, 'text_x': 165, 'text_y': 410, 'font_size': 9},
                'Solid Timber': {'checkbox_x': 300, 'checkbox_y': 410, 'text_x': 315, 'text_y': 410, 'font_size': 9},
                'Metal Skeleton': {'checkbox_x': 430, 'checkbox_y': 410, 'text_x': 445, 'text_y': 410, 'font_size': 9}
            },
            'edging': {
                'NA Lipping': {'checkbox_x': 35, 'checkbox_y': 440, 'text_x': 50, 'text_y': 440, 'font_size': 9},
                'ABS Edging': {'checkbox_x': 150, 'checkbox_y': 440, 'text_x': 165, 'text_y': 440, 'font_size': 9},
                'No Edging': {'checkbox_x': 270, 'checkbox_y': 440, 'text_x': 285, 'text_y': 440, 'font_size': 9}
            },
            'decorative_line': {
                'T-bar': {'checkbox_x': 35, 'checkbox_y': 470, 'text_x': 50, 'text_y': 470, 'font_size': 9},
                'Groove Line': {'checkbox_x': 120, 'checkbox_y': 470, 'text_x': 135, 'text_y': 470, 'font_size': 9}
            }
        }
        
        print(f"Applied fallback positions: {len(coordinates['header_fields'])} header fields, {len(coordinates['door_table']['rows'])} door rows")
    
    def is_label_text(self, text: str) -> bool:
        """Check if text is likely a label rather than data"""
        
        label_keywords = [
            'job order', 'delivery', 'customer', 'measure', 'laminate',
            'thickness', 'size', 'type', 'core', 'edging', 'decorative',
            'design', 'hole', 'drawing', 'remark', 'frame', 'width',
            'rebated', 'inner', 'outer', 'profile'
        ]
        
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in label_keywords)
    
    def save_learned_coordinates(self, coordinates: Dict):
        """Save learned coordinates to JSON files"""
        
        # Save detailed analysis
        with open('ai_learned_coordinates.json', 'w', encoding='utf-8') as f:
            json.dump(coordinates, f, indent=2, ensure_ascii=False)
        
        # Create overlay specifications for each template
        door_spec = self.create_door_overlay_spec(coordinates)
        with open('ai_door_overlay_spec.json', 'w', encoding='utf-8') as f:
            json.dump(door_spec, f, indent=2, ensure_ascii=False)
        
        frame_spec = self.create_frame_overlay_spec(coordinates)
        with open('ai_frame_overlay_spec.json', 'w', encoding='utf-8') as f:
            json.dump(frame_spec, f, indent=2, ensure_ascii=False)
        
        print("AI-learned coordinates saved!")
        print("  - ai_learned_coordinates.json")
        print("  - ai_door_overlay_spec.json") 
        print("  - ai_frame_overlay_spec.json")
    
    def create_door_overlay_spec(self, coordinates: Dict) -> Dict:
        """Create door template overlay specification"""
        
        spec = {
            'page_size': coordinates['page_size'],
            'fields': {},
            'checkboxes': {},
            'table_rows': []
        }
        
        # Header fields
        for field_name, field_info in coordinates['header_fields'].items():
            data_pos = field_info['data_position']
            spec['fields'][field_name] = {
                'x': data_pos['x'],
                'y': data_pos['y'],
                'font': 'Helvetica',
                'size': min(field_info['font_size'], 10)
            }
        
        # Checkboxes
        for group_name, group_checkboxes in coordinates['door_table']['checkboxes'].items():
            spec['checkboxes'][group_name] = []
            for option_text, option_pos in group_checkboxes.items():
                spec['checkboxes'][group_name].append({
                    'label': option_text,
                    'x': option_pos['checkbox_x'],
                    'y': option_pos['checkbox_y'],
                    'size': 8
                })
        
        # Table rows
        for i, row in enumerate(coordinates['door_table']['rows']):
            spec['table_rows'].append({
                'row_index': i,
                'y_position': row['y_position'],
                'laminate_code_x': row['laminate_x'],
                'door_size_x': row.get('door_size', {}).get('x', row['laminate_x'] + 100)
            })
        
        return spec
    
    def create_frame_overlay_spec(self, coordinates: Dict) -> Dict:
        """Create frame template overlay specification"""
        
        spec = {
            'page_size': coordinates['page_size'],
            'fields': {},
            'checkboxes': {},
            'table_rows': []
        }
        
        # Header fields (same as door)
        for field_name, field_info in coordinates['header_fields'].items():
            data_pos = field_info['data_position']
            spec['fields'][field_name] = {
                'x': data_pos['x'],
                'y': data_pos['y'],
                'font': 'Helvetica',
                'size': min(field_info['font_size'], 10)
            }
        
        # Frame checkboxes
        for group_name, group_checkboxes in coordinates['frame_table']['checkboxes'].items():
            spec['checkboxes'][group_name] = []
            for option_text, option_pos in group_checkboxes.items():
                spec['checkboxes'][group_name].append({
                    'label': option_text,
                    'x': option_pos['checkbox_x'],
                    'y': option_pos['checkbox_y'],
                    'size': 8
                })
        
        # Frame table rows
        for i, row in enumerate(coordinates['frame_table']['rows']):
            spec['table_rows'].append({
                'row_index': i,
                'y_position': row['y_position'],
                'laminate_code_x': row['laminate_x']
            })
        
        return spec


# Run the AI learning system
if __name__ == "__main__":
    learner = AICoordinateLearner()
    
    print("AI Coordinate Learning System")
    print("=" * 50)
    print("Learning field positions from your sample JO form...")
    
    try:
        coordinates = learner.analyze_sample_form()
        
        print(f"\nLearning Results:")
        print(f"  Header fields: {len(coordinates['header_fields'])}")
        print(f"  Door table rows: {len(coordinates['door_table']['rows'])}")
        print(f"  Door checkboxes: {sum(len(group) for group in coordinates['door_table']['checkboxes'].values())}")
        
        if 'frame_table' in coordinates:
            print(f"  Frame table rows: {len(coordinates['frame_table']['rows'])}")
            print(f"  Frame checkboxes: {sum(len(group) for group in coordinates['frame_table']['checkboxes'].values())}")
        
        print("\nAI learning complete! Use ai_*_overlay_spec.json for precise positioning.")
        
    except Exception as e:
        print(f"Error during AI learning: {e}")
        import traceback
        traceback.print_exc()