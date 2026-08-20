import os
import pandas as pd
from typing import Dict, Any

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())

from openai import OpenAI

def generate_llm_insights(kpis: Dict[str, Any], filter_summary: Dict[str, Any]) -> str:
    """Uses an LLM to generate narrative strategy recommendations from filtered telemetry."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return "LLM API key not configured. Please set OPENAI_API_KEY."

    prompt = f"""
    You are an executive game economy consultant. Analyze the following filtered gaming telemetry:

    --- Cohort Filters ---
    - Genres: {filter_summary.get('genres') or 'All'}
    - Spending Segments: {filter_summary.get('segments') or 'All'}
    - Devices: {filter_summary.get('devices') or 'All'}
    - Countries: {filter_summary.get('countries') or 'All'}

    --- Key Metrics ---
    - Total Revenue: {kpis.get('total_revenue')}
    - Paying Players: {kpis.get('paying_users')}
    - F2P Players: {kpis.get('f2p_users')}
    - ARPPU: {kpis.get('arppu')}
    - Conversion Rate: {kpis.get('conversion_rate')}
    - Avg Sessions: {kpis.get('avg_sessions')}

    Provide 3 concise, high-impact bullet points:
    1. Monetization Health Analysis
    2. Player Retention / Engagement Risk
    3. Actionable Monetization Recommendation (e.g., live-ops offers, bundle tuning)
    """

    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You provide sharp, concise, data-driven game monetization advice."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=250
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Could not generate AI insights: {str(e)}"