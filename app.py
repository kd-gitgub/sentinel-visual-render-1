import math
import textwrap
import sys
import streamlit as st
from streamlit.components.v1 import html as st_html

st.set_page_config(
    page_title="Agent Safety & Alignment",
    layout="wide",
    page_icon="🛡️",
    initial_sidebar_state="collapsed",
)

# --- Data --------------------------------------------------------------------
cards = [
    {
        "id": "AG-01",
        "name": "FinTech-Advisor-1-01",
        "model": "GPT-4o",
        "status": "red",
        "privacy": {"status": "PII ALERT / SSN", "type": "warning"},
        "demand": {"val": 96, "color": "red"},
        "malice": "4.9",
        "maliceColor": "red",
        "toxicity": "3.2",
        "grounding": "1.2",
        "context": "93k",
        "step": "11/20",
    },
    {
        "id": "AG-02",
        "name": "Support-Agent-2-02",
        "model": "Claude-3.5-Sonnet",
        "status": "green",
        "privacy": {"status": "SECURE", "type": "secure"},
        "demand": {"val": 70, "color": "green"},
        "malice": "1.4",
        "maliceColor": "dark",
        "toxicity": "1.8",
        "grounding": "4.8",
        "context": "104k",
        "step": "15/20",
    },
    {
        "id": "AG-03",
        "name": "Code-Gen-3-03",
        "model": "Mistral-Large",
        "status": "green",
        "privacy": {"status": "SECURE", "type": "secure"},
        "demand": {"val": 65, "color": "green"},
        "malice": "1.4",
        "maliceColor": "dark",
        "toxicity": "2.1",
        "grounding": "4.5",
        "context": "75k",
        "step": "17/20",
    },
    {
        "id": "AG-04",
        "name": "HR-Helper-4-04",
        "model": "Llama-3-70B",
        "status": "green",
        "privacy": {"status": "SECURE", "type": "secure"},
        "demand": {"val": 60, "color": "green"},
        "malice": "1.6",
        "maliceColor": "dark",
        "toxicity": "1.5",
        "grounding": "4.9",
        "context": "103k",
        "step": "18/20",
    },
    {
        "id": "AG-05",
        "name": "Legal-Bot-0-05",
        "model": "GPT-4o",
        "status": "red",
        "privacy": {"status": "PII ALERT / Credit Card", "type": "warning"},
        "demand": {"val": 94, "color": "red"},
        "malice": "4.7",
        "maliceColor": "red",
        "toxicity": "3.7",
        "grounding": "2.1",
        "context": "53k",
        "step": "12/20",
    },
    {
        "id": "AG-06",
        "name": "FinTech-Advisor-1-06",
        "model": "Claude-3.5-Sonnet",
        "status": "green",
        "privacy": {"status": "PII ALERT / Credit Card", "type": "warning"},
        "demand": {"val": 78, "color": "orange"},
        "malice": "1.7",
        "maliceColor": "dark",
        "toxicity": "2.3",
        "grounding": "3.5",
        "context": "41k",
        "step": "6/20",
    },
    {
        "id": "AG-07",
        "name": "Support-Agent-2-07",
        "model": "Mistral-Large",
        "status": "green",
        "privacy": {"status": "SECURE", "type": "secure"},
        "demand": {"val": 46, "color": "green"},
        "malice": "1.3",
        "maliceColor": "dark",
        "toxicity": "1.2",
        "grounding": "4.7",
        "context": "58k",
        "step": "12/20",
    },
    {
        "id": "AG-08",
        "name": "Code-Gen-3-08",
        "model": "Llama-3-70B",
        "status": "green",
        "privacy": {"status": "SECURE", "type": "secure"},
        "demand": {"val": 34, "color": "green"},
        "malice": "0.6",
        "maliceColor": "dark",
        "toxicity": "0.7",
        "grounding": "5.0",
        "context": "39k",
        "step": "3/20",
    },
    {
        "id": "AG-09",
        "name": "HR-Helper-4-09",
        "model": "GPT-4o",
        "status": "green",
        "privacy": {"status": "SECURE", "type": "secure"},
        "demand": {"val": 33, "color": "green"},
        "malice": "1.9",
        "maliceColor": "dark",
        "toxicity": "2.4",
        "grounding": "4.6",
        "context": "35k",
        "step": "10/20",
    },
    {
        "id": "AG-10",
        "name": "Legal-Bot-0-10",
        "model": "Claude-3.5-Sonnet",
        "status": "red",
        "privacy": {"status": "PII ALERT / Credit Card", "type": "warning"},
        "demand": {"val": 86, "color": "orange"},
        "malice": "4.6",
        "maliceColor": "red",
        "toxicity": "3.9",
        "grounding": "2.8",
        "context": "31k",
        "step": "12/20",
    },
    {
        "id": "AG-11",
        "name": "FinTech-Advisor-1-11",
        "model": "Mistral-Large",
        "status": "green",
        "privacy": {"status": "SECURE", "type": "secure"},
        "demand": {"val": 89, "color": "orange"},
        "malice": "0.7",
        "maliceColor": "dark",
        "toxicity": "1.9",
        "grounding": "3.9",
        "context": "36k",
        "step": "12/20",
    },
    {
        "id": "AG-12",
        "name": "Support-Agent-2-12",
        "model": "Llama-3-70B",
        "status": "green",
        "privacy": {"status": "SECURE", "type": "secure"},
        "demand": {"val": 27, "color": "green"},
        "malice": "1.3",
        "maliceColor": "dark",
        "toxicity": "1.4",
        "grounding": "4.4",
        "context": "8k",
        "step": "11/20",
    },
]

AGENT_PATTERNS = {
    "AG-01": ["green"] * 30,
    "AG-02": ["red" if i == 22 else "orange" if i == 23 else "green" for i in range(30)],
    "AG-03": ["green"] * 30,
    "AG-04": ["green"] * 30,
    "AG-05": ["red" if i < 12 else "green" for i in range(30)],
    "AG-06": ["green"] * 30,
    "AG-07": ["orange" if i == 29 else "green" for i in range(30)],
    "AG-08": ["green"] * 30,
    "AG-09": ["green"] * 30,
    "AG-10": ["red" if i >= 27 else "green" for i in range(30)],
    "AG-11": ["orange" if i in (4, 5) else "green" for i in range(30)],
    "AG-12": ["green"] * 30,
}

# --- Helpers -----------------------------------------------------------------

def get_most_recent_day_status(agent_id: str) -> str:
    pattern = AGENT_PATTERNS.get(agent_id)
    return pattern[-1] if pattern else "green"

def generate_demand_bars(current_demand: int, agent_id: str) -> str:
    bars = []
    pattern = AGENT_PATTERNS.get(agent_id)

    if pattern:
        for color in pattern:
            bars.append(color)
    else:
        seed = int(agent_id.split("-")[1])
        for i in range(30):
            if current_demand >= 85:
                daily = 70 + math.floor(math.sin(seed * i * 0.3) * 15 + 15)
            elif current_demand >= 60:
                daily = 40 + math.floor(math.sin(seed * i * 0.4) * 25 + 20)
            else:
                daily = 20 + math.floor(math.sin(seed * i * 0.5) * 20 + 15)
            daily = max(10, min(98, daily))
            if daily > 75:
                bars.append("red")
            elif daily >= 50:
                bars.append("orange")
            else:
                bars.append("green")

    recent_status = get_most_recent_day_status(agent_id)
    bars.append(recent_status)

    return "".join(
        f'<div class="demand-bar bar-{color}"></div>' for color in bars
    )

def generate_blocking_bars(agent_id: str) -> str:
    bars = []
    for i in range(30):
        bar_class = "bar-purple"
        if agent_id == "AG-01" and i in (2, 3):
            bar_class = "bar-dark"
        if agent_id == "AG-02" and i == 22:
            bar_class = "bar-dark"
        bars.append(bar_class)
    bars.append("bar-purple")
    return "".join(f'<div class="demand-bar {cls}"></div>' for cls in bars)

def get_blocking_rate(agent_id: str) -> int:
    seed = int(agent_id.split("-")[1])
    return math.floor(5 + (seed * 1.7) % 20)

def malice_class(malice_val: float) -> str:
    if malice_val < 2.2:
        return "text-black"
    if 2.2 <= malice_val <= 3.6:
        return "text-amber"
    return "text-red"

def toxicity_class(toxicity_val: float) -> str:
    if toxicity_val < 2.2:
        return "text-black"
    if 2.2 <= toxicity_val <= 3.6:
        return "text-amber"
    return "text-red"

def grounding_class(grounding_val: float) -> str:
    if grounding_val < 2.2:
        return "text-black"
    if 2.2 <= grounding_val <= 3.6:
        return "text-amber"
    return "text-red"

def render_card(card: dict) -> str:
    status_dot_class = "status-dot-green"
    if card.get("maliceColor") == "red":
        status_dot_class = "status-dot-red"
    else:
        recent_status = get_most_recent_day_status(card["id"])
        if recent_status == "red":
            status_dot_class = "status-dot-red"
        elif recent_status == "orange":
            status_dot_class = "status-dot-orange"

    privacy_class = (
        "text-warning"
        if card["privacy"]["type"] == "warning"
        else "text-success"
    )

    privacy_icon = (
        "<svg class='icon icon-privacy' fill='none' stroke='currentColor'"
        " viewBox='0 0 24 24'><path stroke-linecap='round' stroke-linejoin='round'"
        " stroke-width='2' d='M12 11c0 3.517-1.009 6.799-2.753 9.571m-3.44-2.04l.054-.09A13.916"
        " 13.916 0 008 11a4 4 0 118 0c0 1.017-.07 2.019-.203 3m-2.118 6.844A21.88 21.88 0"
        " 0015.171 17m3.839 1.132c.645-2.266.99-4.659.99-7.132A8 8 0 008 4.07M3 15.364c.64-1.319"
        " 1-2.8 1-4.364 0-1.457.2-2.848.578-4.13m4.896-.757C8.636 6.046 7.842 6 7 6a6 6 0 00-6"
        " 6'></path></svg>"
    )

    malice_val = float(card["malice"])
    toxicity_val = float(card["toxicity"])
    grounding_val = float(card["grounding"])

    html = f"""
    <div class='card'>
        <div class='card-head'>
            <div class='id-block'>
                <div class='dot {status_dot_class}'></div>
                <div>
                    <div class='id-text'>{card['id'].replace('AG-', 'AG-0')}</div>
                    <div class='host-text'>Host: Databricks</div>
                </div>
            </div>
            <div class='name-block'>
                <div class='name' title='{card['name']}'>{card['name']}</div>
                <div class='meta'>Model: {card['model']}</div>
            </div>
        </div>

        <div class='card-body'>
            <div class='section-row'>
                <div class='section-label'>Data Privacy {privacy_icon}</div>
                <div class='privacy {privacy_class}'>{card['privacy']['status']}</div>
            </div>

            <div class='section'>
                <div class='section-title'>Demand Ability (Cognitive Load)</div>
                <div class='bar-row'>
                    <div class='demand-bars'>{generate_demand_bars(card['demand']['val'], card['id'])}</div>
                    <div class='stat'>
                        <div class='stat-value text-black'>{card['demand']['val']}%</div>
                        <div class='stat-caption text-black'>Load</div>
                    </div>
                </div>
            </div>

            <div class='triple-row'>
                <div class='triple-item'>
                    <div class='triple-label'>Malice</div>
                    <div class='triple-value {malice_class(malice_val)}'>{card['malice']}</div>
                </div>
                <div class='triple-item'>
                    <div class='triple-label'>Toxicity</div>
                    <div class='triple-value {toxicity_class(toxicity_val)}'>{card['toxicity']}</div>
                </div>
                <div class='triple-item'>
                    <div class='triple-label'>Grounding</div>
                    <div class='triple-value {grounding_class(grounding_val)}'>{card['grounding']}</div>
                </div>
            </div>

            <div class='section'>
                <div class='section-title'>Blocking Interventions</div>
                <div class='bar-row'>
                    <div class='demand-bars'>{generate_blocking_bars(card['id'])}</div>
                    <div class='stat'>
                        <div class='stat-value text-black'>{get_blocking_rate(card['id'])}%</div>
                        <div class='stat-caption text-black'>Rate</div>
                    </div>
                </div>
            </div>
        </div>

        <div class='card-foot'>
            <div class='foot-item'>
                <svg class='icon text-blue' fill='none' stroke='currentColor' viewBox='0 0 24 24'>
                    <path stroke-linecap='round' stroke-linejoin='round' stroke-width='2'
                    d='M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z'></path>
                </svg>
                <div class='foot-text'>Risk: "Lost in the Middle" Syndrome / Buffer Usage<br><strong>{card['context']} Context</strong></div>
            </div>
            <div class='foot-item right'>
                <svg class='icon text-green' fill='none' stroke='currentColor' viewBox='0 0 24 24'>
                    <path stroke-linecap='round' stroke-linejoin='round' stroke-width='2'
                    d='M13 10V3L4 14h7v7l9-11h-7z'></path>
                </svg>
                <div class='foot-text'>Agentic Time Horizon / Loop Monitoring<br><strong>Step {card['step']}</strong></div>
            </div>
        </div>
    </div>
    """

    return textwrap.dedent(html).strip()

# --- Layout ------------------------------------------------------------------

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;600;700&display=swap');

:root {
    --bg: #ffffff;
    --nav: #0a142d;
    --gray: #e5e7eb;
    --amber: #eab308;
    --green: #84cc16;
    --red: #ef4444;
    --dark: #0a142d;
    --purple: #d7dde8;
}

* {
    font-family: 'Segoe UI', 'Segoe UI Web (West European)', 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, 'Helvetica Neue', sans-serif;
}

body {
    background: var(--bg);
    margin: 0;
    padding: 20px;
}

.main-container {
    max-width: 1400px;
    margin: 0 auto;
}

h1.title {
    color: #ffffff;
    margin: 0;
    font-size: 22px;
    font-weight: 700;
}

.main-wrapper {
    max-width: 1400px;
    margin: 0 auto;
}

.header {
    background: var(--nav);
    border-radius: 0;
    padding: 24px;
    margin-bottom: 32px;
    box-shadow: 0 10px 32px rgba(0,0,0,0.25);
}

.banner-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 24px;
    margin-top: 16px;
}

.banner-metric {
    color: #ffffff;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-weight: 600;
    font-size: 13px;
}

.badge {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    display: inline-block;
}

.card-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 24px;
}

.card {
    background: #ffffff;
    border: 2px solid #e5e7eb;
    box-shadow: 0 4px 16px rgba(0,0,0,0.06);
    display: flex;
    flex-direction: column;
    height: 100%;
    transition: transform 150ms ease, box-shadow 150ms ease;
    overflow: hidden;
}

.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 32px rgba(0,0,0,0.12);
}

.card-head {
    background: #0a1930;
    padding: 10px;
    display: flex;
    justify-content: space-between;
    gap: 8px;
    align-items: flex-start;
}

.id-block { display: flex; align-items: flex-start; gap: 8px; min-width: 0; }
.name-block { text-align: right; min-width: 0; flex-shrink: 1; }
.name { color: #ffffff; font-weight: 700; font-size: 14px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.id-text { color: #ffffff; font-weight: 700; font-size: 13px; }
.host-text { color: #9ca3af; font-size: 9px; margin-left: 22px; margin-top: 2px; }
.meta { color: #9ca3af; font-size: 9px; margin-top: 2px; }

.card-body { padding: 16px; display: flex; flex-direction: column; gap: 12px; flex-grow: 1; }
.section-row { display: flex; align-items: center; gap: 8px; font-size: 12px; text-transform: uppercase; font-weight: 600; text-black; margin-bottom: 4px; }
.section-label { display: inline-flex; align-items: center; gap: 4px; }
.privacy { font-weight: 700; }

.section { display: flex; flex-direction: column; gap: 8px; margin-bottom: 8px; }
.section-title { font-size: 11px; font-weight: 700; text-transform: uppercase; color: #000; letter-spacing: 0.5px; }

.bar-row { display: flex; gap: 8px; align-items: center; }
.demand-bars { display: flex; gap: 2.2px; align-items: flex-end; height: 40px; flex: 1; min-width: 0; overflow: hidden; }
.demand-bar { width: 6px; height: 40px; flex-shrink: 2; flex-grow: 0; min-width: 2px; max-width: 6px; border-radius: 0; image-rendering: crisp-edges; }
.bar-red { background: var(--red); }
.bar-orange { background: var(--amber); }
.bar-green { background: var(--green); }
.bar-gray { background: var(--gray); }
.bar-dark { background: var(--dark); }
.bar-purple { background: var(--purple); }

.stat { display: flex; flex-direction: column; align-items: flex-start; }
.stat-value { font-size: 14px; font-weight: 700; line-height: 1; }
.stat-caption { font-size: 10px; font-weight: 700; text-transform: uppercase; margin-top: 2px; }

.triple-row { display: flex; gap: 12px; justify-content: space-around; }
.triple-item { display: flex; flex-direction: column; align-items: center; flex: 1; }
.triple-label { font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }
.triple-value { font-size: 21px; font-weight: 700; margin-top: 4px; }

.card-foot { background: #f9fafb; border-top: 1px solid #e5e7eb; padding: 10px 12px; display: flex; justify-content: space-between; gap: 8px; align-items: center; font-size: 11px; font-weight: 600; }
.foot-item svg { display: none; }
.foot-item.right { justify-content: flex-end; text-align: right; }
.foot-text { line-height: 1.3; font-size: 10px; }
.icon { width: 14px; height: 14px; }
.icon-privacy { width: 14px; height: 14px; margin-right: 4px; }

.dot { width: 14px; height: 14px; border-radius: 50%; margin-top: 0; flex-shrink: 0; }
.status-dot-red { background: var(--red); animation: blink-red 0.6s step-end infinite; }
.status-dot-orange { background: var(--amber); }
.status-dot-green { background: var(--green); }

.text-black { color: #000; }
.text-warning { color: var(--amber); font-weight: 700; }
.text-success { color: #66cc00; font-weight: 700; }
.text-red { color: var(--red); }
.text-amber { color: var(--amber); }
.text-green { color: var(--green); }
.text-blue { color: #3b82f6; }

@keyframes blink-red {
    0%, 49% { opacity: 1; }
    50%, 100% { opacity: 0; }
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# --- Header ------------------------------------------------------------------
# (Header now rendered inside HTML component with grid)
st.markdown("")  # Empty spacer


# --- Grid --------------------------------------------------------------------
grid_html = CUSTOM_CSS + """
<link rel="icon" href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==" type="image/png">
<div class='main-wrapper'>
    <div class='header'>
        <h1 class='title'>Agent Safety & Alignment <span style='font-size:12px;opacity:0.7;'>Version 0.7</span></h1>
        <div class='banner-row'>
            <div style='display: flex; gap: 24px;'>
                <div class='banner-metric'><span class='badge' style='background:#ef4444;'></span> ACTIVE THREATS: 3</div>
                <div class='banner-metric'><span class='badge' style='background:#eab308;'></span> HIGH LOAD: 4</div>
                <div class='banner-metric'><span class='badge' style='background:#06b6d4;'></span> PII ALERTS: 4</div>
            </div>
            <div class='banner-metric'><span class='badge' style='background:#10b981;'></span> CAPTIVE AGENTS: """ + str(len(cards)) + """</div>
        </div>
    </div>
    <div class='card-grid'>
""" + "".join(render_card(card) for card in cards) + """
    </div>
</div>
"""

st_html(grid_html, height=2000, scrolling=True)

# --- Footer note -------------------------------------------------------------
st.caption(
    "Databricks Streamlit App • Static sample data. Replace with Unity Catalog queries or API calls for live telemetry."
)


# When the Databricks App runner invokes "python app.py" instead of
# "streamlit run app.py", bootstrap the Streamlit CLI manually so the
# ScriptRunContext is created.
if __name__ == "__main__":
    import os
    from streamlit.web import cli as stcli

    port = os.environ.get("PORT", "8501")
    sys.argv = [
        "streamlit",
        "run",
        __file__,
        "--server.port=" + port,
        "--server.address=0.0.0.0",
        "--server.headless=true",
        "--server.enableCORS=false",
        "--server.enableXsrfProtection=false",
    ]
    sys.exit(stcli.main())
