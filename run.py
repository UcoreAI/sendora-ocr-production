#!/usr/bin/env python3
"""
Sendora OCR Application Runner
Starts the Flask web server for document processing
"""

import os
import sys
from dotenv import load_dotenv

# Add backend to path
sys.path.append('backend')

# Load environment variables
load_dotenv()

if __name__ == '__main__':
    try:
        from app import app
        print("🚀 Starting Sendora OCR System...")
        print("📁 Template Overlay System: ACTIVE")
        print("🔑 Azure Form Recognizer: CONFIGURED")
        print("🌐 Web Interface: http://localhost:5000")
        print("=" * 50)
        
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("💡 Make sure you've installed dependencies: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        print("💡 Check that all template files are accessible")