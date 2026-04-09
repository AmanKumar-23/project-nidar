import json
import boto3
from datetime import datetime, timezone

# Initialize S3 client leveraging the Lambda execution role
s3_client = boto3.client('s3')

def process_sos(payload, server_timestamp):
    """Handles the legacy incoming SOS edge triggers."""
    device_id = payload.get('device_id', 'unknown_device')
    latitude = payload.get('latitude')
    longitude = payload.get('longitude')
    jammer_status = payload.get('jammer_status', False)
    threat_type = payload.get('threat_type', 'unspecified')
    
    secure_log = {
        "event_type": "sos_trigger",
        "device_id": device_id,
        "latitude": latitude,
        "longitude": longitude,
        "jammer_status": jammer_status,
        "threat_type": threat_type,
        "server_timestamp": server_timestamp
    }
    
    object_key = f"logs/{device_id}/{server_timestamp.replace(':', '-')}.json"
    s3_put_kwargs = {
        'Bucket': 'nidar-secure-logs',
        'Key': object_key,
        'Body': json.dumps(secure_log),
        'ContentType': 'application/json'
    }
    
    if jammer_status:
        s3_put_kwargs['Tagging'] = "priority=PROTOCOL_BLACKOUT"
        
    s3_client.put_object(**s3_put_kwargs)
    
    return {
        "message": "SOS alert securely archived.",
        "status": "success"
    }

def verify_reward(payload, server_timestamp):
    """
    Mock Database logic for linking successful responder interventions
    to the Nirbhaya Fund social safety pool.
    """
    responder_id = payload.get('responder_id', 'unknown_responder')
    lat = payload.get('latitude', 0.0)
    lon = payload.get('longitude', 0.0)
    
    reward_entry = {
        "event_type": "reward_verification",
        "responder_id": responder_id,
        "intervention_lat": lat,
        "intervention_lon": lon,
        "funds_source": "Nirbhaya_Fund_Safety_Pool",
        "credits_allocated": 500,
        "flag_eshram_priority": True,
        "flag_pmjay_enrollment": True,
        "server_timestamp": server_timestamp
    }
    
    # Save validation transaction to the secure logging bucket
    object_key = f"interventions/{responder_id}/{server_timestamp.replace(':', '-')}.json"
    
    s3_client.put_object(
        Bucket='nidar-secure-logs',
        Key=object_key,
        Body=json.dumps(reward_entry),
        ContentType='application/json',
        Tagging="intervention=verified"
    )
    
    return {
        "message": "Verification active. 500 Credits Transferred.",
        "status": "success",
        "responder_id": responder_id
    }

def lambda_handler(event, context):
    """
    AWS Lambda endpoint for Project Nidar APIs. Routes based on path.
    """
    try:
        body = event.get('body', event)
        if isinstance(body, str):
            payload = json.loads(body)
        else:
            payload = body
            
        path = event.get('path', '/sos')
        server_timestamp = datetime.now(timezone.utc).isoformat()
        
        if path == '/verify-reward':
            response_data = verify_reward(payload, server_timestamp)
        else:
            response_data = process_sos(payload, server_timestamp)
            
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS, POST',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps(response_data)
        }
        
    except Exception as e:
        print(f"Error handling edge payload: {str(e)}")
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
