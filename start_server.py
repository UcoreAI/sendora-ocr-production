#!/usr/bin/env python3
"""
Simple Sendora OCR Server Startup
Runs the Flask app from backend directory
"""

import os
import sys
from dotenv import load_dotenv

# Change to backend directory
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
os.chdir(backend_dir)

# Add backend to Python path
sys.path.insert(0, backend_dir)

# Load environment variables from parent directory
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

if __name__ == '__main__':
    try:
        print("🚀 Starting Sendora OCR System...")
        print("📁 Template Overlay System: ACTIVE")
        print("🔑 Azure Form Recognizer: CONFIGURED")
        print("🌐 Web Interface: http://localhost:5000")
        print("=" * 50)
        
        # Import and run the Flask app
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("💡 Make sure you've installed dependencies: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        print("💡 Check that all template files are accessible")