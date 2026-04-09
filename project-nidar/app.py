import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

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
    st.header("Nidar Command Center")
    st.markdown("___")
    
    # Toggle switch for Jamming
    is_jammed = st.toggle("Simulate Signal Jammer (Protocol Blackout)", value=False)
    
    st.markdown("<br>", unsafe_allow_html=True)
    # Large manual trigger button
    sos_triggered = st.button("🚨 Simulate Live Edge AI SOS Event", type="primary", use_container_width=True)


# ==========================================
# Main Dashboard Layout (2 Columns)
# ==========================================

# Using a 2:1 column ratio to give the Live Map more visual real estate
col1, col2 = st.columns([2, 1], gap="large")

with col1:
    st.subheader("Live Operations Map")
    
    if not is_jammed:
        # Standard GPS Map rendering with pydeck
        # Centering map on Gurugram (~28.4595 N, 77.0266 E)
        GURUGRAM_LAT, GURUGRAM_LON = 28.4595, 77.0266
        
        # Generate simulated Safe Zones (Green dots)
        safe_zones = pd.DataFrame({
            "lat": [GURUGRAM_LAT + 0.01, GURUGRAM_LAT - 0.015, GURUGRAM_LAT + 0.005],
            "lon": [GURUGRAM_LON + 0.012, GURUGRAM_LON - 0.005, GURUGRAM_LON - 0.015],
            "color": [[0, 255, 0, 160]] * 3
        })
        
        # Generate simulated SOS Incident (Red dot)
        # Using the triggered variable to make it pulse larger if pressed
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
        
        # Initial map view
        view_state = pdk.ViewState(
            latitude=GURUGRAM_LAT,
            longitude=GURUGRAM_LON,
            zoom=12.5,
            pitch=45
        )
        
        # Render the map
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
        
        # Use pandas and numpy.random.randn to plot the simulated offline tracked path
        np.random.seed(int(pd.Timestamp.now().timestamp()) if sos_triggered else 42)
        
        # Start at origin (0,0) and do a random cumulative walk representing tracked trajectory
        simulated_offline_path = np.cumsum(np.random.randn(150, 2), axis=0) * 0.5 
        df_route = pd.DataFrame(simulated_offline_path, columns=["X-Axis Drift (m)", "Y-Axis Drift (m)"])
        
        st.line_chart(df_route, use_container_width=True)

with col2:
    st.subheader("Live Telemetry Feed")
    st.caption("Incoming system logs and edge alerts.")
    
    st.markdown("---")
    
    # --------------------------------------------------------------------------
    # Clean Separation: Edge UI representation vs Serverless Data Fetch
    # In production, this section would execute a REST call to AWS API Gateway,
    # which would invoke our `cloud_function.py` Lambda to securely log to S3.
    # Here, we are rendering the local edge logic visual state directly.
    # --------------------------------------------------------------------------
    
    if sos_triggered:
        if not is_jammed:
            st.success("Acoustic Threat Detected. GenAI Deterrent Active.", icon="🚨")
            
            # Mimicking network deployment telemetry
            st.code(">> SYSTEM LOG <<\n\nBLE Mesh Network Deployed:\n- Alerted Watchman (20m)\n- Alerted Apartment B (50m)\n- Lambda Endpoint Response: 200 OK", language="text")
        else:
            st.error("**CRITICAL: SIGNAL JAMMING DETECTED.**\n\nLocal Black-Box Recording Initiated.\n\nBroadcasting asymmetric BLE pulse.", icon="🛑")
    else:
        # Idle status waiting for button push
        if not is_jammed:
            st.info("System Nominal. Awaiting incident detection...", icon="✅")
        else:
            st.warning("Protocol Blackout active. Network severed. Device is offline.", icon="⚠️")
