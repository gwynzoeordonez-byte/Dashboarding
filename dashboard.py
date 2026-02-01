import streamlit as st
import json
import os
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

# 1. DATABASE & CONFIG
DB_FILE = "thermobin_final_data.json"
LOCATIONS = ["Naga City People's Market Bin", "Plaza Rizal Bin", "ADNU Bin"]

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f: return json.load(f)
    return {loc: {"temp": 30, "moist": 50, "n": 10, "p": 10, "k": 10, "status": "Available/Empty"} for loc in LOCATIONS}

def save_data(data):
    with open(DB_FILE, "w") as f: json.dump(data, f)

# 2. RECOMMENDATION ENGINE
def get_recommendation(n, p, k):
    if n >= 15: return "Leafy Crops", "Seedling/Vegetative"
    if p >= 20: return "Fruiting", "Pre-bloom/Flowering"
    if k >= 20: return "Root Crops", "Fruiting/Root"
    return "All-Purpose Use", "Seedling/Vegetative"

# 3. PAGE CONFIG
st.set_page_config(page_title="Thermobin Monitor", layout="wide")
st_autorefresh(interval=5000, key="datarefresh")

# --- 4. CUSTOM CSS ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@800;900&family=Dancing+Script:wght@600&display=swap');
    
    .stApp {{ background-color: #FFFFFF; }}

    .hero-title {{
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        color: #2E7D32;
        font-size: 55px !important;
        line-height: 1;
        margin-top: -65px;
        margin-bottom: 5px;
    }}
    
    .sub-title {{
        font-family: 'Inter', sans-serif;
        color: #666666;
        font-size: 20px;
        font-weight: 500;
        margin-bottom: 25px;
    }}
    
    [data-testid="stSidebar"] {{ background-color: #2E7D32 !important; }}
    
    /* Sidebar Location Text */
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {{
        font-size: 20px !important; 
        color: white !important;
        font-weight: 600 !important;
        padding: 10px 0px !important;
    }}
    
    .status-card {{
        background: #fdfdfd;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #eeeeee;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    }}
    
    .big-status {{ font-size: 55px; font-weight: 800; color: #1B5E20; }}
    .metric-val {{ font-size: 40px; font-weight: 700; }}
    
    /* Dark Green Recommendation Box */
    .rec-box {{
        background-color: #1B5E20;
        padding: 20px;
        border-radius: 12px;
        color: white;
        font-family: 'Inter', sans-serif;
    }}
    
    .motto {{
        font-family: 'Dancing Script', cursive;
        font-size: 32px;
        color: #2E7D32;
        text-align: center;
        margin-top: 40px;
    }}
    
    .admin-spacer {{ margin-top: 400px; border-top: 1px solid rgba(255,255,255,0.2); }}
    </style>
    """, unsafe_allow_html=True)

# 5. DATA HANDLING
data = load_data()

# --- 6. SIDEBAR NAVIGATION ---
with st.sidebar:
    try:
        st.image("logooo.png", use_container_width=True)
    except:
        st.markdown("<h1 style='color:white; text-align:center;'>THERMOBIN</h1>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("## 📍 SITES")
    user_location = st.radio("Sites", LOCATIONS, label_visibility="collapsed")
    
    st.markdown('<div class="admin-spacer"></div>', unsafe_allow_html=True)
    with st.expander("🛠 REMOTE CONTROL"):
        admin_target = st.selectbox("Site to Edit", LOCATIONS)
        a_temp = st.slider("Temp", 0, 100, data[admin_target]["temp"])
        a_moist = st.slider("Moisture", 0, 100, data[admin_target]["moist"])
        a_n = st.number_input("Nitrogen", 0, 100, data[admin_target]["n"])
        a_p = st.number_input("Phosphorus", 0, 100, data[admin_target]["p"])
        a_k = st.number_input("Potassium", 0, 100, data[admin_target]["k"])
        a_stat = st.selectbox("Phase", ["Available/Empty", "Running", "Ready for Collection"])
        if st.button("SAVE UPDATES"):
            data[admin_target] = {"temp": a_temp, "moist": a_moist, "n": a_n, "p": a_p, "k": a_k, "status": a_stat}
            save_data(data)
            st.rerun()

# --- 7. MAIN BOARD ---
bin_info = data[user_location]

st.markdown('<p class="hero-title">THERMOBIN</p>', unsafe_allow_html=True)
st.markdown(f'<p class="sub-title">Monitoring Station: {user_location}</p>', unsafe_allow_html=True)

# Phase Status Card
st.markdown(f"""
    <div class="status-card">
        <p style="color:#888; letter-spacing:1px; font-weight:bold; font-size:12px;">CURRENT PHASE</p>
        <div class="big-status">{bin_info['status']}</div>
    </div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Metrics
c1, c2 = st.columns(2)
with c1:
    st.markdown(f"""<div class="status-card">
        <p style="color:#888; font-weight:bold; font-size:12px;">TEMPERATURE</p>
        <div class="metric-val" style="color:#D32F2F;">{bin_info['temp']}°C</div>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""<div class="status-card">
        <p style="color:#888; font-weight:bold; font-size:12px;">MOISTURE</p>
        <div class="metric-val" style="color:#1976D2;">{bin_info['moist']}%</div>
    </div>""", unsafe_allow_html=True)

# NPK Graph (N at Top)
st.markdown("<br><h4 style='color:black; margin-bottom:10px;'>Nutrient Composition</h4>", unsafe_allow_html=True)

# Plotly renders bottom to top, so list is K -> P -> N
fig = go.Figure(go.Bar(
    x=[bin_info['k'], bin_info['p'], bin_info['n']],
    y=['Potassium (K)  ', 'Phosphorus (P)  ', 'Nitrogen (N)  '],
    orientation='h',
    marker=dict(
        color=['#A5D6A7', '#4CAF50', '#1B5E20'], # Light Green to Dark Green
        line=dict(color='#FFFFFF', width=1)
    ),
    text=[f"{bin_info['k']}%", f"{bin_info['p']}%", f"{bin_info['n']}%"],
    textposition='inside',
    textfont=dict(color='white', size=14, family='Inter')
))

fig.update_layout(
    height=260, 
    paper_bgcolor='white', 
    plot_bgcolor='rgba(0,0,0,0)', 
    xaxis=dict(range=[0, 105], showgrid=False, zeroline=False), 
    yaxis=dict(tickfont=dict(color='#1B5E20', size=15, weight='bold')), # Dark Green Labels
    margin=dict(l=0, r=0, t=0, b=0)
)
st.plotly_chart(fig, use_container_width=True)

# Recommendation
p_type, p_stage = get_recommendation(bin_info['n'], bin_info['p'], bin_info['k'])
st.markdown(f"""
    <div class="rec-box">
        <span style="font-size:1.1em;">🌱 <b>Recommended Usage:</b></span><br>
        Best for <b>{p_type}</b> during the <b>{p_stage}</b> stage.
    </div>
""", unsafe_allow_html=True)

# Motto
st.markdown('<p class="motto">"where even your trash deserves a glow-up"</p>', unsafe_allow_html=True)
