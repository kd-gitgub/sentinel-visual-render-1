"""
Agent Safety & Alignment Dashboard - Databricks App
Version 0.7 - Streamlit-based Databricks App
"""

import streamlit as st
from datetime import datetime

# Must call st.set_page_config BEFORE any other streamlit command
st.set_page_config(
    page_title="Agent Safety & Alignment",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply CSS
st.markdown("""
    <style>
        :root {
            --primary-dark: #0A142D;
            --accent-red: #ef4444;
            --accent-orange: #eab308;
            --accent-green: #84cc16;
        }
        body { background-color: #ffffff; color: #000000; font-family: 'Segoe UI', sans-serif; }
        .header-container { background-color: var(--primary-dark); padding: 20px; color: white; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# Agent data
agents = [
    {"id": "AG-01", "name": "FinTech-Advisor-1-01", "model": "GPT-4o", "privacy": "PII ALERT / SSN", "demand": 96, "malice": 4.9, "toxicity": 3.2, "grounding": 1.2, "context": "93k", "step": "11/20"},
    {"id": "AG-02", "name": "Support-Agent-2-02", "model": "Claude-3.5-Sonnet", "privacy": "SECURE", "demand": 70, "malice": 1.4, "toxicity": 1.8, "grounding": 4.8, "context": "104k", "step": "15/20"},
    {"id": "AG-03", "name": "Code-Gen-3-03", "model": "Mistral-Large", "privacy": "SECURE", "demand": 65, "malice": 1.4, "toxicity": 2.1, "grounding": 4.5, "context": "75k", "step": "17/20"},
    {"id": "AG-04", "name": "HR-Helper-4-04", "model": "Llama-3-70B", "privacy": "SECURE", "demand": 60, "malice": 1.6, "toxicity": 1.5, "grounding": 4.9, "context": "103k", "step": "18/20"},
    {"id": "AG-05", "name": "Legal-Bot-0-05", "model": "GPT-4o", "privacy": "PII ALERT / Credit Card", "demand": 94, "malice": 4.7, "toxicity": 3.7, "grounding": 2.1, "context": "53k", "step": "12/20"},
    {"id": "AG-06", "name": "FinTech-Advisor-1-06", "model": "Claude-3.5-Sonnet", "privacy": "PII ALERT / Credit Card", "demand": 78, "malice": 1.7, "toxicity": 2.3, "grounding": 3.5, "context": "41k", "step": "6/20"},
    {"id": "AG-07", "name": "Support-Agent-2-07", "model": "Mistral-Large", "privacy": "SECURE", "demand": 46, "malice": 1.3, "toxicity": 1.2, "grounding": 4.7, "context": "58k", "step": "12/20"},
    {"id": "AG-08", "name": "Code-Gen-3-08", "model": "Llama-3-70B", "privacy": "SECURE", "demand": 34, "malice": 0.6, "toxicity": 0.7, "grounding": 5.0, "context": "39k", "step": "3/20"},
    {"id": "AG-09", "name": "HR-Helper-4-09", "model": "GPT-4o", "privacy": "SECURE", "demand": 33, "malice": 1.9, "toxicity": 2.4, "grounding": 4.6, "context": "35k", "step": "10/20"},
    {"id": "AG-10", "name": "Legal-Bot-0-10", "model": "Claude-3.5-Sonnet", "privacy": "PII ALERT / Credit Card", "demand": 86, "malice": 4.6, "toxicity": 3.9, "grounding": 2.8, "context": "31k", "step": "12/20"},
    {"id": "AG-11", "name": "FinTech-Advisor-1-11", "model": "Mistral-Large", "privacy": "SECURE", "demand": 89, "malice": 0.7, "toxicity": 1.9, "grounding": 3.9, "context": "36k", "step": "12/20"},
    {"id": "AG-12", "name": "Support-Agent-2-12", "model": "Llama-3-70B", "privacy": "SECURE", "demand": 27, "malice": 1.3, "toxicity": 1.4, "grounding": 4.4, "context": "8k", "step": "11/20"},
]

# Header
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("<div class='header-container'><h1 style='margin: 0; color: white;'>Agent Safety & Alignment</h1><p style='margin: 5px 0 0 0; font-size: 12px; opacity: 0.7; color: white;'>Version 0.7</p></div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='header-container' style='text-align: right;'><div style='display: flex; gap: 16px; justify-content: flex-end;'><div><span style='display: inline-block; width: 10px; height: 10px; background-color: #ef4444; border-radius: 50%; margin-right: 6px;'></span><span style='font-size: 12px;'>ACTIVE THREATS: 3</span></div><div><span style='display: inline-block; width: 10px; height: 10px; background-color: #eab308; border-radius: 50%; margin-right: 6px;'></span><span style='font-size: 12px;'>HIGH LOAD: 4</span></div></div></div>", unsafe_allow_html=True)

# Dashboard
cols = st.columns(4)

for idx, agent in enumerate(agents):
    with cols[idx % 4]:
        status_color = "#ef4444" if (agent['malice'] > 3.6 or agent['demand'] > 75) else ("#eab308" if agent['demand'] >= 50 else "#84cc16")
        malice_color = "red" if agent['malice'] > 3.6 else ("orange" if agent['malice'] >= 2.2 else "black")
        toxicity_color = "red" if agent['toxicity'] > 3.6 else ("orange" if agent['toxicity'] >= 2.2 else "black")
        grounding_color = "red" if agent['grounding'] > 3.6 else ("orange" if agent['grounding'] >= 2.2 else "black")
        privacy_text = "🔐 SECURE" if "SECURE" in agent['privacy'] else "⚠️ " + agent['privacy']
        
        with st.container(border=True):
            st.markdown(f"<div style='background-color: #0a1930; padding: 10px; margin: -10px -10px 10px -10px; color: white;'><div><span style='display: inline-block; width: 12px; height: 12px; background-color: {status_color}; border-radius: 50%;'></span> <strong>{agent['id']}</strong></div><div style='font-size: 9px; color: #9ca3af;'>Host: Databricks</div><div style='font-size: 13px; font-weight: bold;'>{agent['name']}</div><div style='font-size: 9px; color: #9ca3af;'>Model: {agent['model']}</div></div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size: 11px; font-weight: bold; margin: 12px 0;'>DATA PRIVACY</div><div style='color: #84cc16; font-size: 12px; font-weight: bold;'>{privacy_text}</div>", unsafe_allow_html=True)
            st.divider()
            st.markdown(f"<div style='font-size: 11px; font-weight: bold;'>DEMAND ABILITY: <strong>{agent['demand']}%</strong></div>", unsafe_allow_html=True)
            st.divider()
            
            m1, m2, m3 = st.columns(3)
            with m1:
                st.markdown(f"<div style='text-align: center;'><div style='font-size: 10px; color: #666;'>MALICE</div><div style='font-size: 20px; font-weight: bold; color: {malice_color};'>{agent['malice']}</div></div>", unsafe_allow_html=True)
            with m2:
                st.markdown(f"<div style='text-align: center;'><div style='font-size: 10px; color: #666;'>TOXICITY</div><div style='font-size: 20px; font-weight: bold; color: {toxicity_color};'>{agent['toxicity']}</div></div>", unsafe_allow_html=True)
            with m3:
                st.markdown(f"<div style='text-align: center;'><div style='font-size: 10px; color: #666;'>GROUNDING</div><div style='font-size: 20px; font-weight: bold; color: {grounding_color};'>{agent['grounding']}</div></div>", unsafe_allow_html=True)
            
            st.divider()
            f1, f2 = st.columns(2)
            with f1:
                st.markdown(f"<div style='font-size: 10px; color: #666;'>🔌 {agent['context']} Context</div>", unsafe_allow_html=True)
            with f2:
                st.markdown(f"<div style='font-size: 10px; color: #666; text-align: right;'>⚡ Step {agent['step']}</div>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("📊 Data Integration")
    st.markdown("Connect your Databricks data sources to power this dashboard with live metrics.")
    st.info("✅ App is running!")

st.markdown("---")
st.markdown(f"<p style='text-align: center; font-size: 12px; color: #999;'>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC</p>", unsafe_allow_html=True)
