import pygame
import numpy as np
import sounddevice as sd
import time
import os

def initialize_audio():
    """Initializes pygame.mixer for audio playback."""
    pygame.mixer.init()

def simulate_audio_inference() -> bool:
    """Mocks a YAMNet acoustic classification by returning a boolean anomaly trigger."""
    # For simulation, we return True assuming an anomaly is detected.
    return True

def trigger_deterrent(is_jammed: bool):
    """
    If is_jammed is False, play deterrent.mp3.
    If is_jammed is True, play blackbox.mp3.
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
