# Agent Safety & Alignment Dashboard - Databricks App Setup Guide

## Overview

This is a **Databricks App** that displays your Agent Safety & Alignment dashboard. It's designed to be powered by real data from Databricks Notebooks, Tables, and Volumes.

## Architecture

```
Databricks Notebooks (Data Processing)
         ↓
Databricks Tables/Views (Data Storage)
         ↓
Streamlit App (app.py) - This File
         ↓
Browser (Interactive Dashboard)
```

---

## Option 1: Deploy in Databricks (Recommended)

### Step 1: Upload to Databricks

1. Go to your Databricks workspace
2. Click **Create** → **App** (or navigate to Apps section)
3. Copy the contents of `app.py` into the app editor
4. Name it "Agent Safety & Alignment"
5. Click **Publish**

### Step 2: Configure Data Connection

In your workspace, modify the `load_agent_data()` function in the app to connect to your data:

```python
from databricks import sql

def load_agent_data():
    """Fetch live data from Databricks"""
    with sql.connect(
        host="your-workspace.cloud.databricks.com",
        http_path="/sql/1.0/warehouses/your-warehouse-id",
        auth_type="pat",
        token=st.secrets["databricks_token"]
    ) as conn:
        df = conn.execute("""
            SELECT 
                id, name, model, status, privacy_status,
                demand, malice, toxicity, grounding,
                context, step
            FROM your_catalog.your_schema.agents_metrics
            WHERE date = CURRENT_DATE()
        """).fetchall()
    
    return pd.DataFrame(df)
```

---

## Option 2: Local Testing

To test locally before deploying to Databricks:

```bash
pip install streamlit pandas

streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## Setting Up Your Data Pipeline

### Example 1: SQL Notebook for Agent Metrics

Create a notebook called `01_compute_safety_metrics.sql`:

```sql
-- COMMAND ----------

CREATE OR REPLACE TABLE your_catalog.your_schema.agents_metrics AS
SELECT
  agent_id as id,
  agent_name as name,
  model_name as model,
  CASE WHEN malice_score > 3.6 THEN 'red'
       WHEN demand_score > 75 THEN 'red'
       WHEN demand_score >= 50 THEN 'orange'
       ELSE 'green' END as status,
  privacy_alert as privacy_status,
  CAST(demand_score AS INT) as demand,
  ROUND(malice_score, 1) as malice,
  ROUND(toxicity_score, 1) as toxicity,
  ROUND(grounding_score, 1) as grounding,
  CONCAT(context_length / 1000, 'k') as context,
  CONCAT(current_step, '/', max_steps) as step,
  CURRENT_TIMESTAMP() as created_at
FROM your_catalog.your_schema.raw_agent_logs
WHERE date = CURRENT_DATE()
GROUP BY agent_id, agent_name, model_name, privacy_alert, 
         demand_score, malice_score, toxicity_score, grounding_score,
         context_length, current_step, max_steps;

-- COMMAND ----------

SELECT COUNT(*) as total_agents FROM your_catalog.your_schema.agents_metrics;
```

### Example 2: Python Notebook for Demand History

Create a notebook called `02_compute_demand_history.py`:

```python
# COMMAND ----------

import pandas as pd
from datetime import datetime, timedelta

# COMMAND ----------

# Fetch raw agent logs for past 30 days
raw_logs = spark.sql("""
    SELECT 
        agent_id,
        DATE(timestamp) as log_date,
        AVG(demand_score) as avg_demand
    FROM your_catalog.your_schema.raw_agent_logs
    WHERE date >= DATE_SUB(CURRENT_DATE(), 30)
    GROUP BY agent_id, DATE(timestamp)
    ORDER BY agent_id, log_date
""")

# COMMAND ----------

# Create 30-day demand history table
demand_history = raw_logs.groupBy("agent_id").agg(
    F.collect_list(F.col("avg_demand")).over(
        Window.partitionBy("agent_id").orderBy("log_date")
    ).alias("demand_history_30d")
)

demand_history.write.mode("overwrite").saveAsTable(
    "your_catalog.your_schema.demand_history_30d"
)

print("✅ Demand history computed successfully")
```

---

## Environment Variables / Secrets

Store sensitive info in Databricks Secrets:

```bash
# Via Databricks CLI
databricks secrets put-secret --scope agent-dashboard --key databricks-token --string-value "your-pat-token"
```

Then in your app:

```python
import streamlit as st

token = st.secrets.get("databricks_token", "")
```

---

## Data Schema Reference

Your tables should have this structure:

```sql
CREATE TABLE your_catalog.your_schema.agents_metrics (
  id STRING,
  name STRING,
  model STRING,
  status STRING,  -- 'red', 'orange', 'green'
  privacy_status STRING,
  demand INT,  -- 0-100
  malice FLOAT,  -- 0-5
  toxicity FLOAT,  -- 0-5
  grounding FLOAT,  -- 0-5
  context STRING,  -- e.g., '93k'
  step STRING,  -- e.g., '11/20'
  created_at TIMESTAMP
)
```

---

## Updating Dashboard in Real-Time

Add refresh capability:

```python
import streamlit as st
from datetime import datetime

# Refresh every 60 seconds
st.set_page_config(...)

if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = datetime.now()

col1, col2 = st.columns([9, 1])
with col2:
    if st.button("🔄 Refresh"):
        st.rerun()

st.write(f"Last updated: {st.session_state.last_refresh}")
```

---

## Production Deployment Checklist

- [ ] Create Databricks SQL queries for metrics
- [ ] Set up tables in Unity Catalog
- [ ] Test data pipeline with sample data
- [ ] Configure Databricks connection credentials
- [ ] Add error handling for failed queries
- [ ] Set up alerts for high malice/toxicity scores
- [ ] Deploy as Databricks App
- [ ] Set up scheduled notebooks to refresh data
- [ ] Monitor app performance
- [ ] Document data lineage

---

## Support

For questions on:
- **Streamlit**: https://docs.streamlit.io/
- **Databricks SQL**: https://docs.databricks.com/en/sql/index.html
- **Databricks Apps**: https://docs.databricks.com/en/dev-tools/apps/index.html
