# 🛡️ Project Nidar

Project Nidar is an experimental Edge AI prototype focused on personal safety, asynchronous telemetry, and rapid mesh networking. It simulates local on-device acoustic classifications, utilizes GenAI for psychological behavioral intervention, tracks resilient offline pathing, and maintains a clean boundary to a cloud-based serverless archiving backend.

## ✨ Features
- **🚨 Interactive SOS Telemetry**: A fully featured, dark-themed Command Center built natively in Streamlit for ops tracking.
- **📡 Data Visualization Operations**: Uses PyDeck for accurate, real-time map representation of local safe zones and active edge tracking.
- **🛰️ IMU Dead-Reckoning Subsystem**: When signal jamming knocks systems offline, the dashboard reverts to a physics-based Kinematic model to approximate un-networked device trajectories natively.
- **👻 GenAI "Ghost Escort" Deterrence**: Ditches standard police sirens in favor of hyper-realistic generative TTS voices (e.g. playing localized, authoritative Hindi audio interventions) designed to actively deter malicious psychology.
- **🚴‍♂️ Community Response Network**: Simulates an asynchronous gig-worker intervention layer. Calculates proximate delivery drivers within a 500m radius during a crisis and models intervention ETAs.
- **☁️ AWS Serverless API**: Features a dual-endpoint AWS Lambda mock-up (`cloud_function.py`) capable of parsing raw SOS payloads (logging them securely into S3 `nidar-secure-logs`) alongside a dedicated `/verify-reward` endpoint simulating Nirbhaya Fund API credit routing.

## 📂 Project Architecture
```text
.
├── project-nidar/
│   ├── app.py               # The main Streamlit Command Center dashboard
│   ├── audio_engine.py      # The engine managing local PyGame asynchronous audio tasks 
│   ├── responder_hub.py     # Geographical math routing system logic for surrounding gig workers
│   ├── cloud_function.py    # The scalable AWS Lambda architecture containing dual endpoints
│   ├── generate_audio.py    # Legacy script to procedurally synthesize offline .wav targets
│   ├── requirements.txt     # Dependency tracking for the Nidar edge environment
│   └── .streamlit/          # Enforces the professional dark mode emergency aesthetics
```

## 🚀 Getting Started

### 1. Install Dependencies
Run the installation script pointing to the project requirement manifest.
```bash
pip install -r project-nidar/requirements.txt
```

### 2. Synthesize Fallback Audio (Optional)
Generate the legacy local `deterrent.wav` and `blackbox.wav` artifacts procedurally if testing without the Ghost Escort overrides:
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
