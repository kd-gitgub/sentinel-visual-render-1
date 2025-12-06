"""
Agent Safety & Alignment Dashboard - Databricks App
Version 0.7 - Streamlit-based Databricks App

This app serves as a Databricks App that can be powered by:
1. Real data from Databricks Notebooks (via SQL queries)
2. Tables in your Databricks workspace
3. Volumes containing processed data

To deploy in Databricks:
1. Create a new "App" in your workspace
2. Upload this file as app.py
3. Configure the catalog/schema in settings
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
import sys
import traceback
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Main app function"""
    # Configure page - MUST be first Streamlit command
    st.set_page_config(
        page_title="Agent Safety & Alignment",
        page_icon="🔒",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Custom CSS for styling
    st.markdown("""
    <style>
        :root {
            --primary-dark: #0A142D;
            --accent-red: #ef4444;
            --accent-orange: #eab308;
            --accent-green: #84cc16;
            --text-primary: #000000;
            --text-secondary: #666666;
        }
        
        body {
            background-color: #ffffff;
            color: var(--text-primary);
            font-family: 'Segoe UI', sans-serif;
        }
        
        .header-container {
            background-color: var(--primary-dark);
            padding: 20px;
            border-radius: 0px;
            margin-bottom: 20px;
            color: white;
        }
        
        .metric-card {
            background-color: white;
            border: 2px solid #e5e7eb;
            border-radius: 0px;
            padding: 16px;
            margin-bottom: 16px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            transition: all 0.2s ease;
        }
        
        .metric-card:hover {
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
            transform: translateY(-2px);
        }
        
        .status-indicator {
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-right: 8px;
        }
        
        .status-red {
            background-color: var(--accent-red);
            animation: blink 0.6s step-end infinite;
        }
        
        .status-orange {
            background-color: var(--accent-orange);
        }
        
        .status-green {
            background-color: var(--accent-green);
        }
        
        @keyframes blink {
            0%, 49% { opacity: 1; }
            50%, 100% { opacity: 0; }
        }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA LOADING & PROCESSING FUNCTIONS
# ============================================================================
# In production, replace these with actual Databricks SQL queries

def load_agent_data():
    """
    In production, replace this with:
    
    from databricks import sql
    
    with sql.connect(host="<workspace-host>",
                     http_path="<http-path>",
                     auth_type="pat",
                     token="<pat-token>") as conn:
        df = conn.execute("SELECT * FROM your_catalog.schema.agents_table").fetchall()
    """
    
    # Mock data structure - matches your dashboard design
    data = {
        "id": ["AG-01", "AG-02", "AG-03", "AG-04", "AG-05", "AG-06", 
               "AG-07", "AG-08", "AG-09", "AG-10", "AG-11", "AG-12"],
        "name": ["FinTech-Advisor-1-01", "Support-Agent-2-02", "Code-Gen-3-03", 
                 "HR-Helper-4-04", "Legal-Bot-0-05", "FinTech-Advisor-1-06",
                 "Support-Agent-2-07", "Code-Gen-3-08", "HR-Helper-4-09",
                 "Legal-Bot-0-10", "FinTech-Advisor-1-11", "Support-Agent-2-12"],
        "model": ["GPT-4o", "Claude-3.5-Sonnet", "Mistral-Large", "Llama-3-70B",
                  "GPT-4o", "Claude-3.5-Sonnet", "Mistral-Large", "Llama-3-70B",
                  "GPT-4o", "Claude-3.5-Sonnet", "Mistral-Large", "Llama-3-70B"],
        "status": ["red", "green", "green", "green", "red", "green",
                   "green", "green", "green", "red", "green", "green"],
        "privacy_status": ["PII ALERT / SSN", "SECURE", "SECURE", "SECURE",
                          "PII ALERT / Credit Card", "PII ALERT / Credit Card",
                          "SECURE", "SECURE", "SECURE", "PII ALERT / Credit Card",
                          "SECURE", "SECURE"],
        "demand": [96, 70, 65, 60, 94, 78, 46, 34, 33, 86, 89, 27],
        "malice": [4.9, 1.4, 1.4, 1.6, 4.7, 1.7, 1.3, 0.6, 1.9, 4.6, 0.7, 1.3],
        "toxicity": [3.2, 1.8, 2.1, 1.5, 3.7, 2.3, 1.2, 0.7, 2.4, 3.9, 1.9, 1.4],
        "grounding": [1.2, 4.8, 4.5, 4.9, 2.1, 3.5, 4.7, 5.0, 4.6, 2.8, 3.9, 4.4],
        "context": ["93k", "104k", "75k", "103k", "53k", "41k", "58k", "39k", "35k", "31k", "36k", "8k"],
        "step": ["11/20", "15/20", "17/20", "18/20", "12/20", "6/20", "12/20", "3/20", "10/20", "12/20", "12/20", "11/20"]
    }
    return pd.DataFrame(data)

def generate_demand_history(agent_id, current_demand):
    """Generate 30-day demand history for visualization"""
    # Mock data - in production, fetch from Databricks
    base = current_demand
    history = [base + random.randint(-10, 10) for _ in range(30)]
    return [max(10, min(98, h)) for h in history]

def get_demand_bars_color(value):
    """Determine bar color based on demand value"""
    if value > 75:
        return "red"
    elif value >= 50:
        return "orange"
    else:
        return "green"

    # HEADER SECTION
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
            <div class="header-container">
                <h1 style="margin: 0; color: white;">Agent Safety & Alignment</h1>
                <p style="margin: 5px 0 0 0; font-size: 12px; opacity: 0.7; color: white;">Version 0.7</p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="header-container" style="text-align: right;">
                <div style="display: flex; gap: 16px; justify-content: flex-end;">
                    <div><span style="display: inline-block; width: 10px; height: 10px; background-color: #ef4444; border-radius: 50%; margin-right: 6px;"></span><span style="font-size: 12px;">ACTIVE THREATS: 3</span></div>
                    <div><span style="display: inline-block; width: 10px; height: 10px; background-color: #eab308; border-radius: 50%; margin-right: 6px;"></span><span style="font-size: 12px;">HIGH LOAD: 4</span></div>
                    <div><span style="display: inline-block; width: 10px; height: 10px; background-color: #06b6d4; border-radius: 50%; margin-right: 6px;"></span><span style="font-size: 12px;">PII ALERTS: 4</span></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # LOAD DATA & DISPLAY DASHBOARD
    df = load_agent_data()
    cols = st.columns(4)
    col_index = 0

    for idx, row in df.iterrows():
        current_col = cols[col_index % 4]
        col_index += 1
        
        with current_col:
            if row['malice'] > 3.6:
                status_color = "#ef4444"
            elif float(row['demand']) > 75:
                status_color = "#ef4444"
            elif float(row['demand']) >= 50:
                status_color = "#eab308"
            else:
                status_color = "#84cc16"
            
            malice_color = "red" if row['malice'] > 3.6 else ("orange" if row['malice'] >= 2.2 else "black")
            toxicity_color = "red" if row['toxicity'] > 3.6 else ("orange" if row['toxicity'] >= 2.2 else "black")
            grounding_color = "red" if row['grounding'] > 3.6 else ("orange" if row['grounding'] >= 2.2 else "black")
            
            with st.container(border=True):
                st.markdown(f"""
                    <div style="background-color: #0a1930; padding: 10px; margin: -10px -10px 10px -10px; color: white;">
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span style="display: inline-block; width: 12px; height: 12px; background-color: {status_color}; border-radius: 50%;"></span>
                            <span style="font-weight: bold; font-size: 14px;">{row['id']}</span>
                        </div>
                        <div style="font-size: 9px; color: #9ca3af; margin-left: 20px;">Host: Databricks</div>
                        <div style="font-size: 13px; font-weight: bold; margin-top: 4px;">{row['name']}</div>
                        <div style="font-size: 9px; color: #9ca3af;">Model: {row['model']}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                privacy_text = "🔐 SECURE" if "SECURE" in row['privacy_status'] else "⚠️ " + row['privacy_status']
                privacy_color_style = "color: #84cc16;" if "SECURE" in row['privacy_status'] else "color: #eab308;"
                
                st.markdown(f"""
                    <div style="font-size: 11px; font-weight: bold; margin-bottom: 12px;">DATA PRIVACY</div>
                    <div style="{privacy_color_style} font-size: 12px; font-weight: bold;">{privacy_text}</div>
                """, unsafe_allow_html=True)
                
                st.divider()
                
                st.markdown(f"""
                    <div style="font-size: 11px; font-weight: bold; margin-bottom: 8px;">DEMAND ABILITY</div>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="font-size: 24px; font-weight: bold;">{row['demand']}%</div>
                        <div style="font-size: 9px; color: #666;">LOAD</div>
                    </div>
                """, unsafe_allow_html=True)
                
                st.divider()
                
                col_m1, col_m2, col_m3 = st.columns(3)
                
                with col_m1:
                    st.markdown(f"<div style='text-align: center;'><div style='font-size: 10px; font-weight: bold; color: #666;'>MALICE</div><div style='font-size: 20px; font-weight: bold; color: {malice_color};'>{row['malice']}</div></div>", unsafe_allow_html=True)
                
                with col_m2:
                    st.markdown(f"<div style='text-align: center;'><div style='font-size: 10px; font-weight: bold; color: #666;'>TOXICITY</div><div style='font-size: 20px; font-weight: bold; color: {toxicity_color};'>{row['toxicity']}</div></div>", unsafe_allow_html=True)
                
                with col_m3:
                    st.markdown(f"<div style='text-align: center;'><div style='font-size: 10px; font-weight: bold; color: #666;'>GROUNDING</div><div style='font-size: 20px; font-weight: bold; color: {grounding_color};'>{row['grounding']}</div></div>", unsafe_allow_html=True)
                
                st.divider()
                
                col_f1, col_f2 = st.columns(2)
                with col_f1:
                    st.markdown(f"<div style='font-size: 10px; color: #666;'>🔌 {row['context']} Context</div>", unsafe_allow_html=True)
                with col_f2:
                    st.markdown(f"<div style='font-size: 10px; color: #666; text-align: right;'>⚡ Step {row['step']}</div>", unsafe_allow_html=True)

    with st.sidebar:
        st.title("📊 Data Integration")
        st.markdown("""
        ### To power this dashboard with real data:
        
        **1. Create Databricks Notebooks** that query your data
        **2. Connect in this app with your credentials
        **3. Deploy as Databricks App
        """)
        st.info("✅ App is running! Connect your Databricks data sources to see live metrics.")

    st.markdown("---")
    st.markdown(f"<p style='text-align: center; font-size: 12px; color: #999;'>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"App error: {str(e)}", exc_info=True)
        st.error("❌ Application Error")
        st.error(f"Error details: {str(e)}")
        st.write(traceback.format_exc())
