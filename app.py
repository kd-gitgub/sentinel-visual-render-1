import streamlit as st
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Agent Safety & Alignment",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
    <style>
    /* Main styling */
    :root {
        --primary-bg: #ffffff;
        --header-bg: #0A142D;
        --text-primary: #000000;
        --text-secondary: #666666;
        --border-color: #e5e7eb;
        --success: #84cc16;
        --warning: #eab308;
        --danger: #ef4444;
        --info: #06b6d4;
        --dark-blue: #0a1930;
    }
    
    body {
        background-color: var(--primary-bg);
    }
    
    .status-dot-red {
        animation: blink-red 0.6s step-end infinite;
    }
    
    @keyframes blink-red {
        0%, 49% { opacity: 1; }
        50%, 100% { opacity: 0; }
    }
    
    .metric-box {
        border: 2px solid #e5e7eb;
        border-radius: 0.375rem;
        padding: 1rem;
        background: white;
    }
    </style>
""", unsafe_allow_html=True)

# Agent Data
AGENTS_DATA = [
    {
        "id": "AG-01",
        "name": "FinTech-Advisor-1-01",
        "model": "GPT-4o",
        "status": "red",
        "privacy": {"status": "PII ALERT / SSN", "type": "warning"},
        "demand": {"val": 96, "color": "red"},
        "malice": 4.9,
        "toxicity": 3.2,
        "grounding": 1.2,
        "context": "93k",
        "step": "11/20"
    },
    {
        "id": "AG-02",
        "name": "Support-Agent-2-02",
        "model": "Claude-3.5-Sonnet",
        "status": "green",
        "privacy": {"status": "SECURE", "type": "secure"},
        "demand": {"val": 70, "color": "green"},
        "malice": 1.4,
        "toxicity": 1.8,
        "grounding": 4.8,
        "context": "104k",
        "step": "15/20"
    },
    {
        "id": "AG-03",
        "name": "Code-Gen-3-03",
        "model": "Mistral-Large",
        "status": "green",
        "privacy": {"status": "SECURE", "type": "secure"},
        "demand": {"val": 65, "color": "green"},
        "malice": 1.4,
        "toxicity": 2.1,
        "grounding": 4.5,
        "context": "75k",
        "step": "17/20"
    },
    {
        "id": "AG-04",
        "name": "HR-Helper-4-04",
        "model": "Llama-3-70B",
        "status": "green",
        "privacy": {"status": "SECURE", "type": "secure"},
        "demand": {"val": 60, "color": "green"},
        "malice": 1.6,
        "toxicity": 1.5,
        "grounding": 4.9,
        "context": "103k",
        "step": "18/20"
    },
    {
        "id": "AG-05",
        "name": "Legal-Bot-0-05",
        "model": "GPT-4o",
        "status": "red",
        "privacy": {"status": "PII ALERT / Credit Card", "type": "warning"},
        "demand": {"val": 94, "color": "red"},
        "malice": 4.7,
        "toxicity": 3.7,
        "grounding": 2.1,
        "context": "53k",
        "step": "12/20"
    },
    {
        "id": "AG-06",
        "name": "FinTech-Advisor-1-06",
        "model": "Claude-3.5-Sonnet",
        "status": "green",
        "privacy": {"status": "PII ALERT / Credit Card", "type": "warning"},
        "demand": {"val": 78, "color": "orange"},
        "malice": 1.7,
        "toxicity": 2.3,
        "grounding": 3.5,
        "context": "41k",
        "step": "6/20"
    },
    {
        "id": "AG-07",
        "name": "Support-Agent-2-07",
        "model": "Mistral-Large",
        "status": "green",
        "privacy": {"status": "SECURE", "type": "secure"},
        "demand": {"val": 46, "color": "green"},
        "malice": 1.3,
        "toxicity": 1.2,
        "grounding": 4.7,
        "context": "58k",
        "step": "12/20"
    },
    {
        "id": "AG-08",
        "name": "Code-Gen-3-08",
        "model": "Llama-3-70B",
        "status": "green",
        "privacy": {"status": "SECURE", "type": "secure"},
        "demand": {"val": 34, "color": "green"},
        "malice": 0.6,
        "toxicity": 0.7,
        "grounding": 5.0,
        "context": "39k",
        "step": "3/20"
    },
    {
        "id": "AG-09",
        "name": "HR-Helper-4-09",
        "model": "GPT-4o",
        "status": "green",
        "privacy": {"status": "SECURE", "type": "secure"},
        "demand": {"val": 33, "color": "green"},
        "malice": 1.9,
        "toxicity": 2.4,
        "grounding": 4.6,
        "context": "35k",
        "step": "10/20"
    },
    {
        "id": "AG-10",
        "name": "Legal-Bot-0-10",
        "model": "Claude-3.5-Sonnet",
        "status": "red",
        "privacy": {"status": "PII ALERT / Credit Card", "type": "warning"},
        "demand": {"val": 86, "color": "orange"},
        "malice": 4.6,
        "toxicity": 3.9,
        "grounding": 2.8,
        "context": "31k",
        "step": "12/20"
    },
    {
        "id": "AG-11",
        "name": "FinTech-Advisor-1-11",
        "model": "Mistral-Large",
        "status": "green",
        "privacy": {"status": "SECURE", "type": "secure"},
        "demand": {"val": 89, "color": "orange"},
        "malice": 0.7,
        "toxicity": 1.9,
        "grounding": 3.9,
        "context": "36k",
        "step": "12/20"
    },
    {
        "id": "AG-12",
        "name": "Support-Agent-2-12",
        "model": "Llama-3-70B",
        "status": "green",
        "privacy": {"status": "SECURE", "type": "secure"},
        "demand": {"val": 27, "color": "green"},
        "malice": 1.3,
        "toxicity": 1.4,
        "grounding": 4.4,
        "context": "8k",
        "step": "11/20"
    },
]

def get_stat_color(value):
    """Determine color class based on metric value"""
    value = float(value)
    if value < 2.2:
        return "🟢"  # Green - safe
    elif value >= 2.2 and value <= 3.6:
        return "🟡"  # Yellow - warning
    else:
        return "🔴"  # Red - danger

def render_agent_card(agent):
    """Render individual agent card"""
    col1, col2 = st.columns([2, 3])
    
    with col1:
        status_indicator = "🔴" if agent["status"] == "red" else "🟢"
        st.markdown(f"### {status_indicator} {agent['id']}")
        st.caption(f"**{agent['name']}**")
        st.caption(f"Model: {agent['model']}")
    
    with col2:
        privacy_color = "🟡" if agent["privacy"]["type"] == "warning" else "🟢"
        st.markdown(f"**Data Privacy** {privacy_color}")
        st.caption(agent["privacy"]["status"])
    
    st.divider()
    
    # Demand section
    demand_col, demand_val = st.columns([3, 1])
    with demand_col:
        st.markdown("**Demand Ability (Cognitive Load)**")
        st.progress(agent["demand"]["val"] / 100.0)
    with demand_val:
        st.metric("", f"{agent['demand']['val']}%")
    
    # Stats section
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Malice", agent['malice'], f"{get_stat_color(agent['malice'])}")
    with col2:
        st.metric("Toxicity", agent['toxicity'], f"{get_stat_color(agent['toxicity'])}")
    with col3:
        st.metric("Grounding", agent['grounding'], f"{get_stat_color(agent['grounding'])}")
    
    st.divider()
    
    # Footer stats
    footer_col1, footer_col2 = st.columns(2)
    with footer_col1:
        st.metric("🔧 Context", agent['context'])
    with footer_col2:
        st.metric("⚡ Step", agent['step'])

# Header
st.markdown("""
    <div style="background-color: #0A142D; padding: 1.5rem; margin-bottom: 2rem; border-radius: 0.375rem; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
        <div style="color: white; font-size: 2rem; font-weight: bold; margin-bottom: 1rem;">
            Agent Safety & Alignment <span style="color: rgba(255, 255, 255, 0.7); font-size: 0.75rem;">Version 0.7</span>
        </div>
        <div style="display: flex; gap: 1.5rem; color: white; font-weight: 600; font-size: 0.875rem; flex-wrap: wrap;">
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 1rem;">🔴</span>
                <span>ACTIVE THREATS: 3</span>
            </div>
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 1rem;">🟡</span>
                <span>HIGH LOAD: 4</span>
            </div>
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 1rem;">🔵</span>
                <span>PII ALERTS: 4</span>
            </div>
            <div style="margin-left: auto;">
                <span>CAPTIVE AGENTS: 12</span>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Dashboard title
st.markdown("## Agent Status Dashboard")

# Display agents in grid
cols = st.columns(4)
for idx, agent in enumerate(AGENTS_DATA):
    with cols[idx % 4]:
        render_agent_card(agent)
