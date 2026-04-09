# 🛡️ Project Nidar

Project Nidar is an experimental Edge AI prototype focused on personal safety, asynchronous telemetry, and mesh networking. It simulates local on-device acoustic classifications, handles resilient offline tracing, and maintains a clean boundary to a cloud-based serverless archiving backend.

## ✨ Features
- **🚨 Interactive SOS Telemetry**: A dark-themed, immersive Control Center built in Streamlit.
- **📡 Data Visualization Operations**: Uses PyDeck for real-time map representation of safe zones and active tracking.
- **🛰️ IMU Dead-Reckoning Subsystem**: When signal jamming knocks systems offline, the dashboard reverts to a physics-based Kinematic model to approximate trajectories natively through Pandas.
- **🎙️ Procedural Acoustic Deterrence**: Synthesizes and routes harsh deterrence sirens or local black-box audio footprints seamlessly depending on network states.
- **☁️ AWS Serverless Framework**: Contains mock-ups for Lambda `boto3` execution routines routing CORS-secured S3 `nidar-secure-logs` telemetry tags.

## 📂 Project Architecture
```text
.
├── project-nidar/
│   ├── app.py               # The main Streamlit Command Center dashboard
│   ├── audio_engine.py      # The engine interfacing with PyGame to manage local playback 
│   ├── generate_audio.py    # Generates local fallback .wav files procedurally via NumPy
│   ├── cloud_function.py    # The AWS Lambda architecture configuration script
│   ├── requirements.txt     # Dependency tracking for the Nidar environment
│   └── .streamlit/          # Enforces the professional dark mode emergency aesthetic
```

## 🚀 Getting Started

### 1. Install Dependencies
Run the installation script pointing to the project requirement manifest.
```bash
pip install -r project-nidar/requirements.txt
```

### 2. Synthesize Fallback Audio
Nidar relies on a local `deterrent.wav` and `blackbox.wav`. Generate them utilizing the built-in NumPy logic:
```bash
cd project-nidar
python generate_audio.py
```

### 3. Launch the Command Center
Initialize the frontend UI to interact with the simulated safety node:
```bash
streamlit run app.py
```
*Navigate to `http://localhost:8501` to view your dashboard.*
