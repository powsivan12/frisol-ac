import os
import sys
import json

def create_response(status_code, body):
    """Helper function to create a properly formatted response."""
    if isinstance(body, dict):
        body_str = json.dumps(body, ensure_ascii=False)
    else:
        body_str = str(body)
    
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        },
        'body': body_str
    }

def handler(event, context):
    try:
        # Log the incoming request
        print(f"Received event: {json.dumps(event, default=str)}")
        
        # Simple response with minimal dependencies
        response_data = {
            'status': 'success',
            'message': 'Hello from Vercel Python!',
            'python_version': sys.version.split()[0],
        }
        
        # Add system info if possible
        try:
            response_data.update({
                'cwd': os.getcwd(),
                'files_in_root': os.listdir('.'),
                'python_path': sys.path
            })
        except Exception as e:
            response_data['warning'] = f'Could not get system info: {str(e)}'
        
        return create_response(200, response_data)
        
    except Exception as e:
        # Return a properly formatted error response
        error_info = {
            'status': 'error',
            'error': str(e),
            'type': type(e).__name__,
            'python_version': sys.version.split()[0]
        }
        print(f"Error in handler: {error_info}")
        return create_response(500, error_info)

# For local testing
if __name__ == '__main__':
    # Test the handler locally
    test_event = {
        'httpMethod': 'GET',
        'path': '/api/hello',
        'headers': {},
        'queryStringParameters': None,
        'body': None
    }
    
    print("Local test:")
    result = handler(test_event, {})
    print(json.dumps(result, indent=2))
