import streamlit as st
import pandas as pd
import time

# Branding & Title
st.set_page_config(page_title="Thermobin Dashboard", layout="wide")
st.title("♻️ Thermobin")
st.markdown("### *where even your trash deserves a glow-up*")
st.divider()

# --- NAGA CITY LOCATIONS ---
if 'bins' not in st.session_state:
    st.session_state.bins = {
        "Naga City People's Market Bin": {"temp": 55, "moist": 65, "status": "Running", "n": 30, "p": 20, "k": 15},
        "Plaza Rizal Bin": {"temp": 28, "moist": 15, "status": "Available/Empty", "n": 0, "p": 0, "k": 0},
        "Ateneo de Naga University Bin": {"temp": 42, "moist": 80, "status": "Ready for Collection", "n": 50, "p": 45, "k": 40},
        "Magsaysay Avenue Bin": {"temp": 50, "moist": 55, "status": "Running", "n": 25, "p": 25, "k": 20}
    }

# --- CONTROL PANEL (Sidebar) ---
st.sidebar.header("🕹️ Remote Controller")
selected_name = st.sidebar.selectbox("Select Bin to Command", list(st.session_state.bins.keys()))
current = st.session_state.bins[selected_name]

# Manual Overrides for recording
st.sidebar.subheader("Live Simulation")
new_status = st.sidebar.radio("Force Status", ["Available/Empty", "Running", "Ready for Collection"], 
                               index=["Available/Empty", "Running", "Ready for Collection"].index(current["status"]))
new_temp = st.sidebar.slider("Simulate Temp", 0, 80, current["temp"])
new_moist = st.sidebar.slider("Simulate Moisture", 0, 100, current["moist"])

# Update State
st.session_state.bins[selected_name].update({"status": new_status, "temp": new_temp, "moist": new_moist})

# --- MAIN DASHBOARD DISPLAY ---
st.header(f"📍 Location: {selected_name}")

# Big Status Indicator
color = {"Available/Empty": "gray", "Running": "orange", "Ready for Collection": "green"}[new_status]
st.markdown(f"#### Current Status: :{color}[{new_status.upper()}]")

col1, col2, col3 = st.columns(3)
col1.metric("Temperature", f"{new_temp}°C", delta="In Progress" if new_status == "Running" else None)
col2.metric("Moisture", f"{new_moist}%")
col3.metric("NPK Quality Index", f"{(current['n']+current['p']+current['k'])//3}/50")

# Progress Bar for "Running" status
if new_status == "Running":
    st.write("Decomposition Progress:")
    st.progress(new_moist / 100) # Moisture used as a proxy for visual effect

st.divider()
st.subheader("Nutrient Profile")
npk_df = pd.DataFrame({
    "Nutrient": ["Nitrogen (N)", "Phosphorus (P)", "Potassium (K)"],
    "Level": [current['n'], current['p'], current['k']]
})
st.bar_chart(npk_df.set_index("Nutrient"))

if new_status == "Ready for Collection":
    st.balloons()