import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="LLM Benchmarker",
    page_icon=":bar_chart:",
    layout="wide"
)

st.title("LLM Benchmarking")
st.caption("Evaluating Gemini 2.5 Flash x LLaMA 4 Scout x LLaMA 3.1 8B on Coding + Reasoning + Summarization + RAG tasks")

st.divider()

import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

# LOAD THE DATA
IS_CLOUD = os.getenv("K_SERVICE") is not None

def load_data():
    if IS_CLOUD:
        from google.cloud import bigquery
        project = os.getenv("GCP_PROJECT_ID")
        dataset = os.getenv("BQ_DATASET")
        client = bigquery.Client(project=project)

        leaderboard = client.query(f"""
            SELECT
                display_name, model_id,
                ROUND(AVG(aggregate_score), 2) as avg_score,
                ROUND(AVG(score_accuracy), 2) as avg_accuracy,
                ROUND(AVG(score_clarity), 2) as avg_clarity,
                ROUND(AVG(score_completeness), 2) as avg_completeness,
                ROUND(AVG(latency_seconds), 3) as avg_latency,
                COUNT(*) as total_evaluations
            FROM `{project}.{dataset}.results`
            WHERE aggregate_score IS NOT NULL
            GROUP BY model_id, display_name
            ORDER BY avg_score DESC
        """).to_dataframe()

        by_category = client.query(f"""
            SELECT
                display_name, category,
                ROUND(AVG(aggregate_score), 2) as avg_score,
                COUNT(*) as total
            FROM `{project}.{dataset}.results`
            WHERE aggregate_score IS NOT NULL
            GROUP BY model_id, display_name, category
            ORDER BY category, avg_score DESC
        """).to_dataframe()

        all_results = client.query(f"""
            SELECT * FROM `{project}.{dataset}.results`
            ORDER BY run_timestamp DESC
            LIMIT 500
        """).to_dataframe()

        return leaderboard, by_category, all_results
    else:
        from storage import fetch_leaderboard, fetch_results_by_category, fetch_all_results
        return (
            pd.DataFrame(fetch_leaderboard()),
            pd.DataFrame(fetch_results_by_category()),
            pd.DataFrame(fetch_all_results())
        )

df_leaderboard, df_category, df_all = load_data()

# SECTION 1: OVERALL LEADERBOARD
st.subheader("Overall Leaderboard")

cols = st.columns(len(df_leaderboard))
for i, row in df_leaderboard.iterrows():
    with cols[i]:
        rank = ["1st", "2nd", "3rd"][i] if i < 3 else f"{i+1}th"
        st.metric(
            label=f"{rank} — {row['display_name']}",
            value=f"{row['avg_score']} / 10",
            delta=f"{row['total_evaluations']} evaluations"
        )

st.divider()

# SECTION 2: SCORE BREAKDOWN TABLE
st.subheader("Score Breakdown by Dimension")

display_cols = {
    "display_name": "Model",
    "avg_score": "Overall",
    "avg_accuracy": "Accuracy",
    "avg_clarity": "Clarity",
    "avg_completeness": "Completeness",
    "avg_latency": "Avg Latency (s)",
    "total_evaluations": "Evaluations"
}

df_display = df_leaderboard[list(display_cols.keys())].rename(columns=display_cols)
st.dataframe(
    df_display,
    use_container_width=True,
    hide_index=True
)

st.divider()

# SECTION 3: PERFORMANCE BY CATEGORY
st.subheader("Performance by Task Category")

if not df_category.empty:
    categories = df_category["category"].unique()
    cat_cols = st.columns(len(categories))

    for i, cat in enumerate(sorted(categories)):
        with cat_cols[i]:
            st.markdown(f"**{cat.upper()}**")
            cat_df = df_category[df_category["category"] == cat][["display_name", "avg_score", "total"]].copy()
            cat_df = cat_df.sort_values("avg_score", ascending=False).reset_index(drop=True)
            cat_df.columns = ["Model", "Avg Score", "Prompts"]
            st.dataframe(cat_df, use_container_width=True, hide_index=True)

st.divider()

# SECTION 4: LATENCY vs QUALITY
st.subheader("Quality vs Latency")
if not df_leaderboard.empty:
    import altair as alt
    chart_data = df_leaderboard[["display_name", "avg_score", "avg_latency"]].copy()
    chart = alt.Chart(chart_data).mark_circle(size=200).encode(
        x=alt.X("avg_latency:Q", title="Avg Latency (seconds)"),
        y=alt.Y("avg_score:Q", title="Avg Score (0-10)", scale=alt.Scale(domain=[0, 10])),
        color=alt.Color("display_name:N", title="Model"),
        tooltip=["display_name", "avg_score", "avg_latency"]
    ).properties(height=350)
    st.altair_chart(chart, use_container_width=True)

st.divider()