import streamlit as st
import time
import pandas as pd
from datetime import datetime

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="SafeSense AI", layout="wide")

# ---------- HEADER ----------
st.markdown("""
<h1 style='text-align: center; color: #00ADB5;'>
🏭 SafeSense AI - Industrial Monitoring System
</h1>
""", unsafe_allow_html=True)

st.markdown("---")

# ---------- READ DATA ----------
try:
    with open("data.txt", "r") as f:
        data = f.read().split(",")
        temperature = int(data[0])
        violations = int(data[1])
        risk = data[2]
except:
    temperature = 0
    violations = 0
    risk = "NO DATA"

# ---------- METRICS ----------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🌡️ Temperature", temperature)

with col2:
    st.metric("👷 Violations", violations)

# Risk score
risk_score = temperature * 0.5 + violations * 10

with col3:
    st.metric("📊 Risk Score", int(risk_score))

st.markdown("---")

# ---------- RISK ALERT ----------
if risk == "HIGH":
    st.error("🚨 HIGH RISK - Immediate Action Required!")
elif risk == "MEDIUM":
    st.warning("⚠️ MEDIUM RISK - Stay Alert")
elif risk == "LOW":
    st.success("✅ LOW RISK - Safe Environment")
else:
    st.info("ℹ️ Waiting for Data...")

# ---------- SYSTEM STATUS ----------
st.markdown("### 🧠 System Status")

if risk == "HIGH":
    st.markdown("🔴 **System Critical**")
elif risk == "MEDIUM":
    st.markdown("🟡 **Moderate Risk**")
else:
    st.markdown("🟢 **All Systems Normal**")

# ---------- PROGRESS BAR ----------
st.markdown("### Risk Level Indicator")
progress = min(int(risk_score), 100)
st.progress(progress)

# ---------- GRAPH (RISK TREND) ----------
st.markdown("### 📈 Risk Trend")

# Store history
if "data_history" not in st.session_state:
    st.session_state.data_history = pd.DataFrame(
        columns=["Time", "Risk Score"]
    )

# Add new data
new_data = pd.DataFrame({
    "Time": [datetime.now().strftime("%H:%M:%S")],
    "Risk Score": [risk_score]
})

st.session_state.data_history = pd.concat(
    [st.session_state.data_history, new_data],
    ignore_index=True
)

# Limit to last 20 points
st.session_state.data_history = st.session_state.data_history.tail(20)

st.line_chart(st.session_state.data_history.set_index("Time"))

# ---------- WHATSAPP ALERT (SIMULATED) ----------
st.markdown("### 📱 Alert System")

if risk == "HIGH":
    st.error("📩 WhatsApp Alert Sent to Supervisor!")
elif risk == "MEDIUM":
    st.warning("📩 Alert Sent to Safety Officer")

# ---------- LIVE CAMERA (OPTIONAL) ----------
st.markdown("### 🎥 Live Monitoring (Demo)")

st.info("Camera feed runs in main system window")

# ---------- FOOTER ----------
st.markdown("---")
st.markdown("Made with ❤️ for Industrial Safety | SafeSense AI")

# ---------- AUTO REFRESH ----------
time.sleep(1)
st.rerun()

# ---------- ABOUT SYSTEM ----------
st.markdown("---")
st.markdown("## 📘 About SafeSense AI")

st.markdown("""
**SafeSense AI** is an intelligent industrial safety system that combines 
computer vision and machine learning to monitor worker safety in real time.

### 🚀 Key Features:
- 🎥 Real-time hazard detection  
- 📊 Dynamic risk scoring  
- 📈 Risk trend analysis  
- 🔊 Smart alert system  
- 🌐 Live monitoring dashboard  

---

### 🧠 How It Works:
The system captures real-time data from cameras and sensors, processes it using AI models, 
and calculates a risk score based on environmental and behavioral factors.

---

### ⚠️ Problem We Solve:
Traditional safety systems are reactive and expensive. They detect accidents only after they occur.

---

### ✅ Our Solution:
We provide a **proactive, affordable, and scalable system** that predicts risks before accidents happen.

---

### 🏆 Impact:
- Improves worker safety  
- Reduces industrial accidents  
- Affordable for MSMEs  
- Scalable across industries  

---

### 🔥 Vision:
To make industrial environments safer using intelligent and accessible AI solutions.
""")

# ---------- FINAL TAGLINE ----------
st.markdown("---")
st.markdown("""
<h3 style='text-align: center; color: #00ADB5;'>
🚀 “From Detection to Prediction — Making Industries Safer”
</h3>
""", unsafe_allow_html=True)