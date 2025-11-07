import os
import sys

def handler(event, context):
    try:
        # Simple response that should always work
        response = {
            'status': 'success',
            'message': 'Hello from Vercel Python!',
            'python_version': sys.version.split()[0],
        }
        
        # Try to get additional info, but don't fail if it doesn't work
        try:
            response.update({
                'cwd': os.getcwd(),
                'files_in_root': os.listdir('.'),
                'python_path': sys.path
            })
        except Exception as e:
            response['warning'] = f'Could not get system info: {str(e)}'
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': str(response)  # Convert to string to avoid JSON serialization issues
        }
        
    except Exception as e:
        # Minimal error handling to avoid any potential issues
        return {
            'statusCode': 500,
            'body': str({
                'status': 'error',
                'error': str(e),
                'type': type(e).__name__
            })
        }

# For local testing
if __name__ == '__main__':
    print('Local test:')
    print(handler({}, {}))
