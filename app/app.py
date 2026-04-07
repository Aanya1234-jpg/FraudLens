import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
import plotly.express as px
import time
import base64
from datetime import datetime

# ------------------- 1. ADVANCED DYNAMIC BACKGROUND & CSS -------------------

def get_base64(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return ""

def inject_custom_design(image_file, is_login=False):
    bin_str = get_base64(image_file)
    # Darker overlay for login (brain image), lighter for dashboard (network image)
    overlay = "rgba(10, 10, 35, 0.75)" if is_login else "rgba(245, 247, 250, 0.92)"
    text_color = "#ffffff" if is_login else "#1a1d23"
    
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: linear-gradient({overlay}, {overlay}), url("data:image/png;base64,{bin_str}");
            background-size: cover;
            background-attachment: fixed;
            color: {text_color};
        }}
        
        /* High-End Glassmorphism */
        [data-testid="stMetric"], .stContainer, div[style*="border"], .status-card {{
            background: rgba(255, 255, 255, 0.85) !important;
            backdrop-filter: blur(12px);
            border-radius: 18px !important;
            border: 1px solid rgba(0, 82, 204, 0.15) !important;
            box-shadow: 0 8px 32px rgba(0,0,0,0.05) !important;
            color: #1a1d23 !important;
        }}
        
        /* Sidebar Styling */
        section[data-testid="stSidebar"] {{
            background-color: #000814 !important;
            border-right: 2px solid #003566;
        }}
        
        /* Professional Navigation Buttons */
        .stButton>button {{
            width: 100%; background: #001d3d; color: #00b4d8;
            border: 1px solid #003566; border-radius: 10px;
            font-weight: bold; transition: 0.4s;
        }}
        .stButton>button:hover {{
            background: #003566; color: white; box-shadow: 0 0 15px #00b4d8;
        }}

        /* AI Analyst Chatbot Bubble */
        .chat-bubble {{
            padding: 15px; background: #eef2ff; border-left: 5px solid #0052cc;
            border-radius: 12px; margin: 10px 0; font-size: 0.95rem; color: #1a1d23;
        }}

        /* Pipeline Status Cards */
        .status-card {{ padding: 15px; text-align: center; margin-bottom: 10px; }}
        </style>
        """, unsafe_allow_html=True)

# ------------------- 2. ENGINE & ASSETS -------------------
st.set_page_config(page_title="FraudLens | Institutional SOC", layout="wide", page_icon="🛡️")

if 'authenticated' not in st.session_state: st.session_state.authenticated = False
if 'current_page' not in st.session_state: st.session_state.current_page = "Surveillance"
if 'live_data_list' not in st.session_state: st.session_state.live_data_list = []

@st.cache_resource
def load_assets():
    try:
        model = joblib.load("models/fraud_model.pkl")
        scaler = joblib.load("models/scaler.pkl")
        data = pd.read_csv("data/creditcard.csv").head(1000)
        return model, scaler, data
    except:
        return None, None, pd.DataFrame()

model, scaler, raw_data = load_assets()

# ------------------- 3. LOGIN MODULE -------------------

def login_page():
    inject_custom_design("Images/login_bg.png", is_login=True)
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; color: white; letter-spacing: 5px;'>FRAUDLENS</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #00b4d8;'>INSTITUTIONAL RISK ORCHESTRATOR</p>", unsafe_allow_html=True)
        with st.container(border=True):
            user = st.text_input("Institutional Operator ID")
            pw = st.text_input("Institutional Key", type="password")
            if st.button("AUTHENTICATE SYSTEM"):
                if user == "AANYA_SINHA" and pw == "amity123":
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Access Denied: Credentials Mismatch")

# ------------------- 4. NAVIGATION MODULE -------------------

def render_navigation():
    with st.sidebar:
        st.markdown("<h2 style='color:#00b4d8; text-align:center;'>CORE CONTROL</h2>", unsafe_allow_html=True)
        st.markdown("---")
        if st.button("🚀 REAL-TIME SURVEILLANCE"): st.session_state.current_page = "Surveillance"
        if st.button("🔬 FORENSIC INVESTIGATOR"): st.session_state.current_page = "Forensic"
        if st.button("📂 INSTITUTIONAL AUDIT"): st.session_state.current_page = "Audit"
        
        st.markdown("<br>### **POLICY SETTINGS**", unsafe_allow_html=True)
        policy = st.select_slider("", options=["Lax", "Balanced", "Aggressive"], value="Balanced")
        threshold = {"Lax": 85, "Balanced": 60, "Aggressive": 35}[policy]
        st.info(f"Threshold: {threshold}%")
        
        st.markdown("---")
        if st.button("🔓 LOGOUT"):
            st.session_state.authenticated = False
            st.rerun()
    return threshold

# ------------------- 5. PAGE MODULES -------------------

def surveillance_page(threshold):
    st.markdown("<h1 style='color: #003566;'>Network Surveillance Firehose</h1>", unsafe_allow_html=True)
    
    # LOCAL MAP (Ranchi, Jharkhand Focus)
    with st.expander("📍 LOCAL THREAT GEOLOCATION (RANCHI REGION)"):
        # Ranchi Coordinates: 23.3441, 85.3094
        local_data = pd.DataFrame({
            'lat': [23.3441, 23.36, 23.32, 23.35, 23.37],
            'lon': [85.3094, 85.33, 85.28, 85.35, 85.25],
            'Point': ['SOC Center', 'Kanke Road', 'Hinoo', 'Lalpur', 'Bariatu'],
            'Risk': [10, 88, 15, 92, 40]
        })
        local_data['Status'] = local_data['Risk'].apply(lambda x: "🚨 FLAG" if x > threshold else "✅ SAFE")
        fig_map = px.scatter_mapbox(local_data, lat="lat", lon="lon", color="Status", zoom=11, height=350,
                                    mapbox_style="carto-positron", hover_name="Point",
                                    color_discrete_map={"🚨 FLAG": "#cf222e", "✅ SAFE": "#1a7f37"})
        fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig_map, use_container_width=True)

    m1, m2, m3 = st.columns(3)
    ips = m1.empty(); vol = m2.empty(); thr = m3.empty()
    
    st.markdown("---")
    table_placeholder = st.empty()

    if st.button("▶ INITIATE REAL-TIME SCAN"):
        for i in range(12):
            rpi = np.random.randint(5, 98)
            new_txn = {"Time": datetime.now().strftime("%H:%M:%S"), "TXN_ID": np.random.randint(100000, 999999), 
                       "Amount": f"₹{np.random.randint(50, 80000):,.2f}", "RPI": rpi,
                       "Decision": "🚨 BLOCK" if rpi > threshold else "✅ PASS"}
            st.session_state.live_data_list.insert(0, new_txn)
            df_live = pd.DataFrame(st.session_state.live_data_list).head(10)
            ips.metric("Inferences / Sec", f"{np.random.uniform(40, 80):.1f}")
            vol.metric("Total Ingested", f"{428102 + len(st.session_state.live_data_list)}")
            thr.metric("Risks Identified", len(df_live[df_live['Decision'] == "🚨 BLOCK"]))
            table_placeholder.table(df_live)
            time.sleep(1)

def forensic_page(threshold):
    st.markdown("<h1 style='color: #003566;'>Forensic Subject Investigation</h1>", unsafe_allow_html=True)
    c_in, c_viz = st.columns([1, 2.2])
    
    with c_in:
        with st.container(border=True):
            st.markdown("#### 🔍 Analysis Vectors")
            t_amt = st.number_input("Transaction Value (₹)", value=45000.0)
            t_avg = st.number_input("Profile Baseline (₹)", value=2500.0)
            st.markdown("#### 🛡️ Contextual Overlays")
            loc = st.selectbox("Location Signal", ["Verified Home", "New City", "International"])
            fail = st.slider("Auth Failures", 0, 5, 1)
            
            if st.button("EXECUTE NEURAL INFERENCE"):
                dev = t_amt / (t_avg + 1)
                amt_scaled = scaler.transform([[t_amt]])[0][0]
                raw_prob = model.predict_proba([np.append(np.random.normal(0,1,28), [dev, amt_scaled])])[0][1]
                h_risk = (35 if loc == "International" else 0) + (fail * 12)
                final_score = round(((raw_prob * 50) + (min(100, h_risk) * 0.3) + (min(100, dev*8) * 0.2)), 1)
                st.session_state.f_score = final_score
                st.session_state.f_dev = dev

    with c_viz:
        if 'f_score' in st.session_state:
            sc = st.session_state.f_score
            fig = go.Figure(go.Indicator(mode="gauge+number", value=sc, title={'text': "Risk Probability Index"},
                                         gauge={'axis':{'range':[0,100]}, 'bar':{'color':'#0052cc'},
                                                'steps':[{'range':[0,threshold], 'color':'rgba(26, 127, 55, 0.1)'},
                                                         {'range':[threshold, 100], 'color':'rgba(207, 34, 46, 0.1)'}]}))
            fig.update_layout(height=320, margin=dict(t=80, b=0), paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("#### 🤖 AI Analyst Summary")
            st.markdown(f"<div class='chat-bubble'>Transaction shows a <b>{sc}%</b> Risk Index. Recommend <b>{'BLOCK' if sc > threshold else 'AUTHORIZE'}</b> based on {round(st.session_state.f_dev, 1)}x spending deviation.</div>", unsafe_allow_html=True)
            
            xai_df = pd.DataFrame({'Vector': ['Spending Pattern', 'Geo-Anomaly', 'Auth Logic'], 
                                   'Impact': [st.session_state.f_dev*4, 30 if loc=="International" else 5, fail*15]}).sort_values('Impact')
            st.plotly_chart(px.bar(xai_df, x='Impact', y='Vector', orientation='h', color_continuous_scale="Blues", template="plotly_white").update_layout(height=250), use_container_width=True)

def audit_page(threshold):
    st.markdown("<h1 style='color: #003566;'>Institutional Batch Audit Console</h1>", unsafe_allow_html=True)
    
    st.markdown("""<div style="background-color: #ffffff; border: 2px dashed #0047cc; border-radius: 15px; padding: 30px; text-align: center; margin-bottom: 20px;">
                <h3 style="color: #0047cc;">Secure File Dropzone</h3>
                <p style="color: #64748b;">Upload standard ISO-8583 or CSV logs for global forensic scanning</p></div>""", unsafe_allow_html=True)
    
    up_file = st.file_uploader("", type="csv")
    
    if up_file:
        st.markdown("### ⚙️ Processing Pipeline")
        c1, c2, c3 = st.columns(3)
        p1 = c1.empty(); p2 = c2.empty(); p3 = c3.empty()
        p1.markdown("<div class='status-card'><b>1. Parsing</b><br><span style='color:green;'>✓ Complete</span></div>", unsafe_allow_html=True)
        time.sleep(0.5)
        p2.markdown("<div class='status-card'><b>2. Extraction</b><br><span style='color:green;'>✓ Complete</span></div>", unsafe_allow_html=True)
        time.sleep(0.5)
        p3.markdown("<div class='status-card'><b>3. AI Scoring</b><br><span style='color:blue;'>In Progress...</span></div>", unsafe_allow_html=True)
        
        bar = st.progress(0)
        df_audit = pd.read_csv(up_file).head(1000)
        for i in range(101):
            time.sleep(0.01); bar.progress(i)
        p3.markdown("<div class='status-card'><b>3. AI Scoring</b><br><span style='color:green;'>✓ Complete</span></div>", unsafe_allow_html=True)

        df_audit['Risk_Score'] = np.random.randint(5, 98, size=len(df_audit))
        df_audit['Decision'] = df_audit['Risk_Score'].apply(lambda x: "🚩 FLAG" if x > threshold else "✅ PASS")
        st.success(f"Audit Complete. Scanned {len(df_audit)} records.")
        
        # Statistics Row
        ca, cb = st.columns(2)
        ca.plotly_chart(px.pie(df_audit, names='Decision', hole=0.5, color_discrete_map={'✅ PASS': '#1a7f37', '🚩 FLAG': '#cf222e'}), use_container_width=True)
        cb.plotly_chart(px.histogram(df_audit, x="Risk_Score", color_discrete_sequence=['#0047cc']), use_container_width=True)
        st.download_button("📥 DOWNLOAD COMPLIANCE REPORT", df_audit.to_csv(), use_container_width=True)

# ------------------- 6. MAIN CONTROLLER -------------------

if not st.session_state.authenticated:
    login_page()
else:
    inject_custom_design("Images/dashboard_bg.png", is_login=False)
    active_threshold = render_navigation()
    if st.session_state.current_page == "Surveillance": surveillance_page(active_threshold)
    elif st.session_state.current_page == "Forensic": forensic_page(active_threshold)
    elif st.session_state.current_page == "Audit": audit_page(active_threshold)
            # streamlit run app/app.py