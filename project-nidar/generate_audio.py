import numpy as np
import wave

def write_wav(filename, sample_rate, audio_data):
    """Write numpy array to a 16-bit PCM WAV file."""
    # Normalize to 16-bit range
    audio_data = np.int16(audio_data / np.max(np.abs(audio_data)) * 32767)
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())

def generate_deterrent(path):
    """Generates a harsh, oscillating 3-second siren sound."""
    sample_rate = 44100
    t = np.linspace(0, 3, sample_rate * 3, endpoint=False)
    # Frequency sweeps between 600Hz and 1200Hz
    freq = 900 + 300 * np.sin(2 * np.pi * 3 * t)
    # Instantaneous phase is integral of frequency
    phase = np.cumsum(freq) / sample_rate * 2 * np.pi
    signal = np.sin(phase)
    write_wav(path, sample_rate, signal)
    print(f"Generated {path}")

def generate_blackbox(path):
    """Generates a low frequency hum mixed with an intermittent electronic beep."""
    sample_rate = 44100
    t = np.linspace(0, 3, sample_rate * 3, endpoint=False)
    # Low frequency 50Hz hum
    hum = 0.3 * np.sin(2 * np.pi * 50 * t) 
    
    # Distressing 800Hz beep pattern
    beep_freq = 800
    beep_signal = np.sin(2 * np.pi * beep_freq * t)
    
    # Pulse envelope for beep: simple 4Hz square wave
    envelope = (np.sign(np.sin(2 * np.pi * 4 * t)) + 1) / 2
    
    signal = hum + 0.7 * beep_signal * envelope
    write_wav(path, sample_rate, signal)
    print(f"Generated {path}")

if __name__ == "__main__":
    import os
    # Ensure current working directory is the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    deterrent_path = os.path.join(script_dir, "deterrent.wav")
    blackbox_path = os.path.join(script_dir, "blackbox.wav")
    
    generate_deterrent(deterrent_path)
    generate_blackbox(blackbox_path)
