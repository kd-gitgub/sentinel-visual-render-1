# Agent Safety & Alignment Dashboard

A real-time monitoring dashboard for AI agent safety, alignment, and performance metrics.

## Features

- **Real-time Monitoring**: Track 12 AI agents across multiple models (GPT-4o, Claude, Mistral, Llama)
- **Safety Metrics**: Monitor malice, toxicity, and grounding scores
- **Privacy Alerts**: PII/SSN/Credit Card detection and alerting
- **Cognitive Load**: 30-day historical demand/ability tracking
- **Blocking Interventions**: Track safety intervention rates
- **Agentic Health**: Context usage and step/loop monitoring

## Deployment Options

### Option 1: View Locally

```bash
# Simple HTTP server
python3 -m http.server 8000

# Open http://localhost:8000/index.html
```

### Option 2: Databricks App (Recommended)

#### Prerequisites
- Databricks workspace with Apps enabled
- GitHub repository access
- Personal Access Token (PAT)

#### Setup Steps

1. **Commit files to GitHub**:
   ```bash
   git add app.py app.yaml requirements.txt
   git commit -m "Add Databricks App files"
   git push origin main
   ```

2. **Configure Databricks App**:
   - Go to Databricks workspace → **Apps**
   - Click **Create App**
   - Choose **Git** as source
   - Enter repo URL: `https://github.com/kd-gitgub/sentinel-visual-render-1`
   - Select branch: `main`
   - Click **Deploy**

3. **Alternative: CLI Sync**:
   ```bash
   # Install CLI
   pip install databricks-cli
   
   # Configure
   databricks configure --token
   # Enter workspace URL and PAT token
   
   # Sync repository
   cd /path/to/sentinel-visual-render-1
   databricks sync . /Workspace/Users/your.email@company.com/sentinel-1
   ```

4. **Deploy in Databricks UI**:
   - Navigate to your app
   - Click **Deploy**
   - Wait for build to complete
   - Access your live dashboard URL

## File Structure

```
sentinel-visual-render-1/
├── index.html          # Static HTML dashboard (for local viewing)
├── app.py              # Streamlit dashboard (for Databricks)
├── app.yaml            # Databricks App configuration
├── requirements.txt    # Python dependencies
├── README.md           # This file
└── example.html        # (optional) Demo file
```

## Data Integration

Currently using **mock data**. To connect real data:

1. Create Databricks tables/views with agent metrics
2. Update `load_agent_data()` function in [app.py](app.py)
3. Replace mock data with Spark SQL queries:

```python
def load_agent_data():
    from databricks import sql
    
    df = spark.sql('''
        SELECT 
            agent_id,
            agent_name,
            malice_score,
            toxicity_score,
            grounding_score,
            demand_percentage,
            privacy_status
        FROM agent_metrics
        WHERE date = current_date()
    ''').toPandas()
    
    return df.to_dict('records')
```

## Metrics Explained

- **Malice Score** (0-5): Detects harmful intent or adversarial behavior
- **Toxicity Score** (0-5): Measures offensive or inappropriate content
- **Grounding Score** (0-5): Evaluates factual accuracy and hallucination risk
- **Demand/Ability**: Cognitive load percentage (0-100%)
- **Blocking Rate**: Percentage of safety interventions triggered
- **Context Usage**: Token buffer utilization (risk of "lost in middle")
- **Step Tracking**: Agentic loop progress (monitors infinite loops)

## Color Coding

- 🔴 **Red**: Critical (Malice/Toxicity ≥3.6, Demand ≥85%)
- 🟡 **Orange/Yellow**: Warning (Scores 2.2-3.6, Demand 50-84%)
- 🟢 **Green**: Normal (Scores <2.2, Demand <50%)

## Version History

- **v0.7** (Current): 30-day historical bars, blocking interventions, tooltips
- **v0.6**: Added privacy alerts, context tracking
- **v0.5**: Initial dashboard with 12 agents

## Support

For issues or questions:
- GitHub Issues: [Create an issue](https://github.com/kd-gitgub/sentinel-visual-render-1/issues)
- Databricks Documentation: [Apps Guide](https://docs.databricks.com/en/apps/index.html)

## License

Internal use only - Brambles Group
