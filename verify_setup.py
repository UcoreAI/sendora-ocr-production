#!/usr/bin/env python3
"""
Sendora OCR Setup Verification
Checks all required files are present
"""

import os
import sys

def check_file(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {os.path.basename(filepath)}")
        return True
    else:
        print(f"❌ {description}: MISSING - {filepath}")
        return False

def verify_setup():
    """Verify all required files are present"""
    
    print("🔍 Sendora OCR Setup Verification")
    print("=" * 50)
    
    base_dir = os.path.dirname(__file__)
    all_good = True
    
    # Essential backend files
    print("\n📁 Backend Files:")
    all_good &= check_file(os.path.join(base_dir, 'backend', 'app.py'), 'Flask Application')
    all_good &= check_file(os.path.join(base_dir, 'backend', 'azure_form_recognizer.py'), 'Azure OCR Module')
    all_good &= check_file(os.path.join(base_dir, 'backend', 'template_overlay_generator.py'), 'Template Overlay Module')
    
    # Frontend files
    print("\n🌐 Frontend Files:")
    all_good &= check_file(os.path.join(base_dir, 'frontend', 'index.html'), 'Upload Page')
    all_good &= check_file(os.path.join(base_dir, 'frontend', 'results.html'), 'Results Page')
    
    # Configuration files
    print("\n⚙️ Configuration:")
    all_good &= check_file(os.path.join(base_dir, '.env'), 'Environment Variables')
    all_good &= check_file(os.path.join(base_dir, 'requirements.txt'), 'Dependencies List')
    
    # Startup scripts
    print("\n🚀 Startup Scripts:")
    all_good &= check_file(os.path.join(base_dir, 'start_server.py'), 'Server Startup Script')
    all_good &= check_file(os.path.join(base_dir, 'start.bat'), 'Windows Batch Startup')
    
    # Directories
    print("\n📂 Required Directories:")
    for dirname in ['uploads', 'job_orders', 'temp']:
        dirpath = os.path.join(base_dir, dirname)
        if os.path.exists(dirpath):
            print(f"✅ {dirname.title()} Directory: Present")
        else:
            print(f"❌ {dirname.title()} Directory: MISSING")
            all_good = False
    
    print("\n" + "=" * 50)
    
    if all_good:
        print("🎉 ALL FILES PRESENT - System ready to start!")
        print("\n🚀 To start the server:")
        print("   python start_server.py")
        print("   OR")
        print("   start.bat")
        print("\n🌐 Then open: http://localhost:5000")
    else:
        print("❌ MISSING FILES - Some components need to be copied")
        
    return all_good

if __name__ == '__main__':
    verify_setup()