import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import audio_engine
import datetime

# Configure Streamlit page layout and dark theme aesthetic suitable for emergency ops
st.set_page_config(
    page_title="Nidar Command Center",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# Sidebar / Control Panel 
# ==========================================
with st.sidebar:
    st.header("Nidar Framework")
    st.caption("Edge AI Security Node")
    st.markdown("___")
    
    # Toggle switch for Jamming
    is_jammed = st.toggle("Simulate Signal Jammer (Protocol Blackout)", value=False)
    
    st.markdown("<br>", unsafe_allow_html=True)
    # Large manual trigger button
    sos_triggered = st.button("🚨 Simulate Live Edge AI SOS Event", type="primary", use_container_width=True)

    st.markdown("___")
    st.subheader("Device Diagnostics")
    # Added diagnostic visuals for visual density
    st.progress(85, "🔋 Internal Battery: 85%")
    st.progress(22, "🌡️ Core Temp: 45°C")
    st.progress(100 if not is_jammed else 0, "📶 Signal Strength")


# ==========================================
# Main Dashboard Layout 
# ==========================================
st.title("🛡️ Nidar Tactical Operations Dashboard")
st.markdown("Real-time telemetry, threat deterrence, and mesh network coordination.")

# --- TOP METRICS ROW ---
# Adding key performance indicators immediately to the top of the app
m1, m2, m3, m4 = st.columns(4)
m1.metric("Active Mesh Nodes", "4" if not is_jammed else "1 (Isolated)", delta="-3" if is_jammed else "Optimal", delta_color="inverse" if is_jammed else "normal")
m2.metric("Uplink Latency", "24 ms" if not is_jammed else "OFFLINE", delta="Stable" if not is_jammed else "ERR", delta_color="inverse" if is_jammed else "normal")
m3.metric("Acoustic Sensors", "ONLINE", "Listening...")

# Determine threat level state dynamically
if sos_triggered:
    m4.metric("Threat Level", "CRITICAL", "Anomaly Detected", delta_color="inverse")
else:
    m4.metric("Threat Level", "LOW", "All clear", delta_color="normal")

st.markdown("---")

# Using a 2:1 column ratio to give the Live Map more visual real estate
col1, col2 = st.columns([2, 1], gap="large")

with col1:
    st.subheader("Live Operations Map")
    
    if not is_jammed:
        # Standard GPS Map rendering with pydeck
        GURUGRAM_LAT, GURUGRAM_LON = 28.4595, 77.0266
        
        # Generate simulated Safe Zones (Green dots)
        safe_zones = pd.DataFrame({
            "lat": [GURUGRAM_LAT + 0.01, GURUGRAM_LAT - 0.015, GURUGRAM_LAT + 0.005],
            "lon": [GURUGRAM_LON + 0.012, GURUGRAM_LON - 0.005, GURUGRAM_LON - 0.015],
            "color": [[0, 255, 0, 160]] * 3
        })
        
        sos_incident = pd.DataFrame({
            "lat": [GURUGRAM_LAT],
            "lon": [GURUGRAM_LON],
            "color": [[255, 0, 0, 255]]
        })
        
        # PyDeck Scatterplot Layers
        safe_zone_layer = pdk.Layer(
            "ScatterplotLayer",
            data=safe_zones,
            get_position="[lon, lat]",
            get_color="color",
            get_radius=400,
            pickable=True
        )
        
        sos_layer = pdk.Layer(
            "ScatterplotLayer",
            data=sos_incident,
            get_position="[lon, lat]",
            get_color="color",
            get_radius=800 if sos_triggered else 200,
            pickable=True
        )
        
        view_state = pdk.ViewState(
            latitude=GURUGRAM_LAT,
            longitude=GURUGRAM_LON,
            zoom=12.5,
            pitch=45
        )
        
        st.pydeck_chart(pdk.Deck(
            map_style=None,
            initial_view_state=view_state,
            layers=[safe_zone_layer, sos_layer],
            tooltip={"text": "Node Coordinator"}
        ))
        
    else:
        # JAMMER ON: Remove map and trigger Dead Reckoning graph
        st.warning("⚠️ SATELLITE GPS LOST. Engaging offline tracking...", icon="📡")
        st.subheader("IMU Dead Reckoning Route Estimation")
        
        np.random.seed(int(pd.Timestamp.now().timestamp()) if sos_triggered else 42)
        simulated_offline_path = np.cumsum(np.random.randn(150, 2), axis=0) * 0.5 
        df_route = pd.DataFrame(simulated_offline_path, columns=["X-Axis Drift (m)", "Y-Axis Drift (m)"])
        
        st.line_chart(df_route, use_container_width=True)

with col2:
    st.subheader("Live Telemetry Feed")
    st.caption("Incoming system logs and edge alerts.")
    st.markdown("---")
    
    if sos_triggered:
        audio_engine.simulate_audio_inference()
        audio_engine.trigger_deterrent(is_jammed)
        
        if not is_jammed:
            st.success("Acoustic Threat Detected. GenAI Deterrent Active.", icon="🚨")
            st.code(">> SYSTEM LOG <<\n\nBLE Mesh Network Deployed:\n- Alerted Watchman (20m)\n- Alerted Apartment B (50m)\n- Lambda Endpoint Response: 200 OK", language="text")
        else:
            st.error("**CRITICAL: SIGNAL JAMMING DETECTED.**\n\nLocal Black-Box Recording Initiated.\n\nBroadcasting asymmetric BLE pulse.", icon="🛑")
            
        # Dynamically generated timeline of events when an SOS is triggered
        st.subheader("Event Sequence")
        now = datetime.datetime.now()
        events = pd.DataFrame({
            "Time": [
                (now - datetime.timedelta(seconds=5)).strftime("%H:%M:%S"),
                (now - datetime.timedelta(seconds=2)).strftime("%H:%M:%S"),
                now.strftime("%H:%M:%S")
            ],
            "Event log": [
                "Acoustic threshold exceeded",
                "YAMNet classification: True",
                "Deterrent & Cloud Sync Initiated"
            ],
            "Severity": ["Warning", "Critical", "Action"]
        })
        st.dataframe(events, hide_index=True, use_container_width=True)
            
    else:
        if not is_jammed:
            st.info("System Nominal. Awaiting incident detection...", icon="✅")
            st.code(">> SYSTEM LOG <<\n\nStatus: Online\nGPS: Locked (7 Satellites)\nListening: Nominal", language="text")
        else:
            st.warning("Protocol Blackout active. Network severed. Device is offline.", icon="⚠️")
            st.code(">> OFFLINE LOG <<\n\nStatus: Isolated\nGPS: Searching...\nFallback: IMU Dead Reckoning active", language="text")

st.markdown("<br>", unsafe_allow_html=True)

# Expandable block for environmental sensor reading metrics
with st.expander("Node Environmental Sensors"):
    c1, c2, c3 = st.columns(3)
    c1.metric("Ambient Noise", "42 dB" if not sos_triggered else "105 dB")
    c2.metric("BLE Frequency", "2.4 GHz" if not is_jammed else "JAMMED")
    c3.metric("Local Storage", "45 GB Free")