"""
Local development server with correct Windows paths
"""
import os
import sys

# Fix Unicode encoding issues on Windows
import locale
import codecs
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Set environment variables for Windows
os.environ['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
os.environ['OUTPUT_FOLDER'] = os.path.join(os.path.dirname(__file__), 'job_orders')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(os.path.dirname(__file__), 'config', 'google-credentials.json')
os.environ['DEMO_MODE'] = 'true'

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

# Import and run the app
from backend.app_v2_production import app

if __name__ == '__main__':
    # Create directories if they don't exist
    os.makedirs(os.environ['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.environ['OUTPUT_FOLDER'], exist_ok=True)
    
    print(f"Upload folder: {os.environ['UPLOAD_FOLDER']}")
    print(f"Output folder: {os.environ['OUTPUT_FOLDER']}")
    print(f"Starting server on http://localhost:5000")
    
    app.run(host='0.0.0.0', port=5000, debug=False)