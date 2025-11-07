import json
import sys

def log(message):
    print(f"[HELLO] {message}", file=sys.stderr)
    sys.stderr.flush()

def handler(event, context):
    try:
        log("Handler called")
        log(f"Event: {event}")
        log(f"Context: {context}")
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'status': 'success',
                'message': 'Hello from Vercel!',
                'python_version': sys.version,
                'cwd': os.getcwd(),
                'files_in_root': os.listdir('.'),
                'python_path': sys.path
            })
        }
    except Exception as e:
        log(f"Error in handler: {str(e)}")
        import traceback
        return {
            'statusCode': 500,
            'body': json.dumps({
                'status': 'error',
                'error': str(e),
                'traceback': traceback.format_exc(),
                'python_path': sys.path
            })
        }

# For local testing
if __name__ == '__main__':
    print(handler({}, {}))
