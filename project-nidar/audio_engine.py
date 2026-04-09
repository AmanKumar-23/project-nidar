import pygame
import numpy as np
import sounddevice as sd
import time
import os
import requests
import json
import threading

def initialize_audio():
    """Initializes pygame.mixer for audio playback."""
    pygame.mixer.init()

def simulate_audio_inference() -> bool:
    """Mocks a YAMNet acoustic classification by returning a boolean anomaly trigger."""
    # For simulation, we return True assuming an anomaly is detected.
    return True

def _sync_to_cloud(is_jammed: bool):
    """Asynchronously sync the SOS event to the cloud backend endpoint."""
    url = "https://mock-api-endpoint.amazonaws.com/v1/sos-alert"  # Hook to your AWS API Gateway URL here
    payload = {
        "device_id": "PRIYA_EDGE_01",
        "latitude": 28.4595,
        "longitude": 77.0266,
        "jammer_status": is_jammed,
        "threat_type": "acoustic_anomaly"
    }
    
    try:
        # Fire HTTP POST request
        response = requests.post(url, json=payload, timeout=3.0)
        # Assuming success if it doesn't throw a timeout/connection error
        print(f"Cloud Sync Initialized: {response.status_code}")
    except requests.RequestException:
        # Gracefully handle connection drops or active jamming
        print("Cloud Sync Failed - Retaining Local Offline State")

def trigger_deterrent(is_jammed: bool):
    """
    If is_jammed is False, play deterrent.wav.
    If is_jammed is True, play blackbox.wav.
    Plays asynchronously to not block the main thread.
    """
    if not pygame.mixer.get_init():
        initialize_audio()
        
    filename = "blackbox.wav" if is_jammed else "deterrent.wav"
    
    if os.path.exists(filename):
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
    else:
        print(f"[Warning] Required audio file '{filename}' not found. Deployment simulated without audio output.")

    # Immediately fire the Cloud API webhook unblocking the main Streamlit interface
    threading.Thread(target=_sync_to_cloud, args=(is_jammed,), daemon=True).start()
