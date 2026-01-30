import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import time

# --- SETUP ---
st.set_page_config(page_title="Thermobin Remote", layout="wide")
st.title("♻️ Thermobin")
st.markdown("### *where even your trash deserves a glow-up*")

# 1. Connect to the Google Sheet (The Shared Brain)
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. Fetch the current data from the cloud
df = conn.read(ttl=0) 

# 3. Choose the location
locations = ["Naga City People's Market Bin", "Plaza Rizal Bin", "Ateneo de Naga University"]
selected_bin = st.selectbox("Select Bin Location", locations)

# Get the data for that bin (or use defaults if new)
if selected_bin in df['bin_name'].values:
    current_data = df[df['bin_name'] == selected_bin].iloc[0]
else:
    current_data = {'status': 'Available/Empty', 'temp': 25, 'moisture': 10}

# --- THE REMOTE CONTROL LOGIC ---
st.sidebar.header("Device Role")
is_remote = st.sidebar.toggle("Use as Remote Controller")

if is_remote:
    # This is what you see on your PHONE
    st.sidebar.warning("REMOTE MODE ACTIVE")
    new_status = st.selectbox("Status", ["Available/Empty", "Running", "Ready for Collection"], index=0)
    new_temp = st.slider("Temperature", 0, 100, int(current_data['temp']))
    new_moist = st.slider("Moisture", 0, 100, int(current_data['moisture']))
    
    if st.button("🚀 SYNC TO CLOUD"):
        # Save updates to the sheet
        new_row = pd.DataFrame([{"bin_name": selected_bin, "status": new_status, "temp": new_temp, "moisture": new_moist}])
        updated_df = pd.concat([df[df['bin_name'] != selected_bin], new_row], ignore_index=True)
        conn.update(data=updated_df)
        st.success("Sent to cloud!")
        time.sleep(1)
        st.rerun()

else:
    # This is what you see on the LAPTOP (The Display)
    st.header(f"📍 {selected_bin}")
    c1, c2, c3 = st.columns(3)
    c1.metric("Temperature", f"{current_data['temp']}°C")
    c2.metric("Moisture", f"{current_data['moisture']}%")
    c3.subheader(f"Status: {current_data['status']}")

    if current_data['status'] == "Ready for Collection":
        st.balloons()

    # THE MAGIC: This makes the laptop check the cloud every 3 seconds
    time.sleep(3)
    st.rerun()
