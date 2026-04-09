import json
import boto3
from datetime import datetime, timezone

# Initialize S3 client leveraging the Lambda execution role
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    """
    AWS Lambda endpoint for Project Nidar edge devices to submit SOS alerts.
    """
    try:
        # Assuming API Gateway Proxy integration, the event payload is in 'body'
        body = event.get('body', event)
        if isinstance(body, str):
            payload = json.loads(body)
        else:
            payload = body
            
        # Parse the required fields from the incoming payload
        device_id = payload.get('device_id', 'unknown_device')
        latitude = payload.get('latitude')
        longitude = payload.get('longitude')
        jammer_status = payload.get('jammer_status', False)
        threat_type = payload.get('threat_type', 'unspecified')
        
        # Append a secure server-side UTC timestamp to avoid device-time spoofing
        server_timestamp = datetime.now(timezone.utc).isoformat()
        
        # Formulate the document layout
        secure_log = {
            "device_id": device_id,
            "latitude": latitude,
            "longitude": longitude,
            "jammer_status": jammer_status,
            "threat_type": threat_type,
            "server_timestamp": server_timestamp
        }
        
        # Define S3 destination parameters
        bucket_name = "nidar-secure-logs"
        # Create a URL-safe key replacing colons
        object_key = f"logs/{device_id}/{server_timestamp.replace(':', '-')}.json"
        
        s3_put_kwargs = {
            'Bucket': bucket_name,
            'Key': object_key,
            'Body': json.dumps(secure_log),
            'ContentType': 'application/json'
        }
        
        # Edge Case Logic: Protocol Blackout metadata tagging
        if jammer_status is True:
            # Apply an S3 Object Meta Tag for high-priority lifecycles
            s3_put_kwargs['Tagging'] = "priority=PROTOCOL_BLACKOUT"
            
        # Execute the save to the database/bucket
        s3_client.put_object(**s3_put_kwargs)
        
        # Success response configured with universal CORS headers
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS, POST',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({
                "message": "SOS alert securely archived.",
                "status": "success"
            })
        }
        
    except Exception as e:
        # Log the internal failure trace for AWS CloudWatch
        print(f"Error handling edge payload: {str(e)}")
        
        # Fallback HTTP 500 response
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                "error": "Internal Server Error. Database write failed.",
                "status": "failure"
            })
        }
