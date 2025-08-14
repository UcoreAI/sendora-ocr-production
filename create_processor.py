"""
Create Google Document AI Processor
This script will create an Invoice processor for your project
"""

from google.cloud import documentai_v1 as documentai
from google.oauth2 import service_account
from google.api_core.client_options import ClientOptions
import os

def create_processor():
    """Create a Document AI processor"""
    
    # Configuration
    project_id = "my-textbee-sms"
    location = "us"
    display_name = "sendora-invoice-processor"
    type_name = "INVOICE_PROCESSOR"  # or "OCR_PROCESSOR" for general OCR
    
    try:
        # Initialize client
        credentials_path = os.path.join('config', 'google-credentials.json')
        credentials = service_account.Credentials.from_service_account_file(credentials_path)
        
        opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
        client = documentai.DocumentProcessorServiceClient(
            credentials=credentials,
            client_options=opts
        )
        
        # The full resource name of the location
        parent = client.common_location_path(project_id, location)
        
        # Create processor request
        processor = documentai.Processor(
            display_name=display_name,
            type_=type_name
        )
        
        request = documentai.CreateProcessorRequest(
            parent=parent,
            processor=processor
        )
        
        # Create the processor
        print(f"Creating processor: {display_name}")
        print(f"Type: {type_name}")
        print(f"Location: {location}")
        print()
        
        operation = client.create_processor(request=request)
        print("Waiting for processor creation...")
        
        # Wait for the operation to complete
        response = operation.result(timeout=300)
        
        # Extract processor ID from the resource name
        # Format: projects/{project}/locations/{location}/processors/{processor_id}
        processor_id = response.name.split('/')[-1]
        
        print("✅ SUCCESS!")
        print("=" * 50)
        print(f"Processor Name: {response.display_name}")
        print(f"Processor ID: {processor_id}")
        print(f"Full Resource Name: {response.name}")
        print("=" * 50)
        print()
        print("Next steps:")
        print(f"1. Copy this Processor ID: {processor_id}")
        print("2. Update backend/google_document_ai.py:")
        print(f"   'invoice': '{processor_id}',")
        print("3. Run: python test_google_ai.py")
        
        return processor_id
        
    except Exception as e:
        print(f"❌ Error creating processor: {e}")
        print()
        print("Common issues:")
        print("1. Document AI API not enabled")
        print("2. Insufficient permissions")
        print("3. Billing not set up")
        print()
        print("Solutions:")
        print("1. Go to: https://console.cloud.google.com/apis/library/documentai.googleapis.com")
        print("2. Click ENABLE")
        print("3. Set up billing if needed")
        
        return None

if __name__ == "__main__":
    create_processor()