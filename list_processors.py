"""
List existing Document AI processors in your project
"""

from google.cloud import documentai_v1 as documentai
from google.oauth2 import service_account
from google.api_core.client_options import ClientOptions
import os

def list_processors():
    """List all processors in the project"""
    
    project_id = "my-textbee-sms"
    location = "us"
    
    try:
        # Initialize client
        credentials_path = os.path.join('config', 'google-credentials.json')
        credentials = service_account.Credentials.from_service_account_file(credentials_path)
        
        opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
        client = documentai.DocumentProcessorServiceClient(
            credentials=credentials,
            client_options=opts
        )
        
        # List processors
        parent = client.common_location_path(project_id, location)
        request = documentai.ListProcessorsRequest(parent=parent)
        
        print(f"Listing processors in project: {project_id}")
        print(f"Location: {location}")
        print("=" * 60)
        
        processors = client.list_processors(request=request)
        
        if not processors:
            print("No processors found.")
            print()
            print("You need to create a processor first:")
            print("1. Go to: https://console.cloud.google.com/ai/document-ai")
            print("2. Click CREATE PROCESSOR")
            print("3. Choose Invoice Parser")
            print("4. Name: sendora-invoice-processor")
            print("5. Region: us")
            print("6. Click CREATE")
            return None
        
        processor_found = None
        for processor in processors:
            processor_id = processor.name.split('/')[-1]
            print(f"Name: {processor.display_name}")
            print(f"Type: {processor.type_}")
            print(f"Processor ID: {processor_id}")
            print(f"State: {processor.state.name}")
            print(f"Full Resource Name: {processor.name}")
            print("-" * 40)
            
            # Save the first processor for use
            if not processor_found:
                processor_found = processor_id
        
        if processor_found:
            print()
            print("SUCCESS! Found processor(s).")
            print(f"Use this Processor ID: {processor_found}")
            print()
            print("Update your code:")
            print(f"In backend/google_document_ai.py, change:")
            print(f"'invoice': '{processor_found}',")
            
        return processor_found
        
    except Exception as e:
        print(f"Error listing processors: {e}")
        print()
        if "API has not been used in project" in str(e):
            print("Document AI API is not enabled!")
            print("Go to: https://console.cloud.google.com/apis/library/documentai.googleapis.com")
            print("Click ENABLE")
        elif "billing" in str(e).lower():
            print("Billing needs to be enabled!")
            print("Go to: https://console.cloud.google.com/billing")
        
        return None

if __name__ == "__main__":
    list_processors()