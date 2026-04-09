import numpy as np

def calculate_radius_responders(user_lat, user_lon):
    """
    Generates 5 mock 'Driver' objects representing Gig workers
    within a 500m radius of the SOS incident.
    """
    np.random.seed()
    
    # Approx 0.0045 degrees lat/lon is ~500 meters
    lat_offsets = np.random.uniform(-0.0045, 0.0045, 5)
    lon_offsets = np.random.uniform(-0.0045, 0.0045, 5)
    
    aliases = ['Zomato_Rider_01', 'Uber_Driver_04', 'Swiggy_Rapido_33', 'Ola_Auto_09', 'Amazon_Delivery_12']
    responders = []
    
    for i in range(5):
        # Convert coordinate offsets to rough meters for ETA calcs
        dist_m = np.sqrt(lat_offsets[i]**2 + lon_offsets[i]**2) * 111000 
        
        # Approximate urban speed of 400m per minute
        eta_mins = max(1, int((dist_m / 400))) 
        
        responders.append({
            "id": aliases[i],
            "latitude": user_lat + lat_offsets[i],
            "longitude": user_lon + lon_offsets[i],
            "distance_m": int(dist_m),
            "eta_mins": eta_mins
        })
        
    # Sort closest to furthest
    return sorted(responders, key=lambda x: x["distance_m"])

def send_broadcast_alert(responders):
    """
    Simulates an asynchronous API push to localized drivers containing incentivization.
    """
    print(f"Broadcasting Emergency Dispatch to {len(responders)} local gig workers...")
    for driver in responders:
        print(f"-> PUSH API Sent: [{driver['id']}] Payload: [🚨 SOS INTERVENTION REQUIRED! CLAIM REWARD BUTTON: ACTIVE]")
    return True
