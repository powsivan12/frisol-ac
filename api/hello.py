"""Minimal Vercel Python serverless function.

This is designed to work with Vercel's serverless functions.
"""

def handler(request, context):
    """Handle the incoming request."""
    try:
        # Simple response with minimal dependencies
        response_data = {
            'status': 'success',
            'message': 'Hello from Vercel Python!',
            'python_version': '3.9.0'  # Hardcoded for now
        }
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': str(response_data)  # Convert to string to ensure JSON serialization
        }
        
    except Exception as e:
        # Minimal error response
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
    print("Local test:")
    print(handler({}, {}))
