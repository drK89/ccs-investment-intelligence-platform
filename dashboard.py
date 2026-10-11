"""Interactive Streamlit dashboard for the public portfolio project."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from ccs_platform.data_loader import DataValidationError, load_projects, validate_projects
from ccs_platform.scoring import DEFAULT_CRITERIA, DEFAULT_WEIGHTS, DecisionEngine
from ccs_platform.sensitivity import monte_carlo_rank_stability, one_way_sensitivity


st.set_page_config(page_title="CCS Investment Intelligence", page_icon="🌍", layout="wide")
st.title("CCS Investment Intelligence Platform")
st.caption("Transparent multi-criteria screening using public demonstration logic and synthetic data")

with st.sidebar:
    st.header("Scenario controls")
    uploaded = st.file_uploader("Upload a compatible CSV", type=["csv"])
    st.subheader("Criterion weights")
    raw_weights = {
        criterion: st.slider(
            criterion.replace("_", " ").title(),
            min_value=0,
            max_value=100,
            value=int(DEFAULT_WEIGHTS[criterion] * 100),
        )
        for criterion in DEFAULT_CRITERIA
    }
    iterations = st.select_slider("Monte Carlo iterations", [500, 1000, 2000, 5000], value=2000)

try:
    if uploaded is None:
        projects = load_projects(ROOT / "data" / "demo_projects.csv", DEFAULT_CRITERIA)
    else:
        projects = pd.read_csv(uploaded)
        validate_projects(projects, DEFAULT_CRITERIA)
except DataValidationError as exc:
    st.error(str(exc))
    st.stop()

if sum(raw_weights.values()) == 0:
    st.error("Set at least one criterion weight above zero.")
    st.stop()

engine = DecisionEngine(weights=raw_weights)
ranked = engine.score(projects)

top = ranked.iloc[0]
col1, col2, col3, col4 = st.columns(4)
col1.metric("Projects screened", len(ranked))
col2.metric("Top project", top["project_name"])
col3.metric("Top score", f"{top['screening_score']:.1f}/100")
col4.metric("Decision band", top["decision_band"])

st.subheader("Portfolio ranking")
chart = px.bar(
    ranked.sort_values("screening_score"),
    x="screening_score",
    y="project_name",
    color="decision_band",
    orientation="h",
    hover_data=["country", "region", "recommended_action"],
    labels={"screening_score": "Screening score", "project_name": "Project"},
)
chart.update_layout(height=max(450, 40 * len(ranked)), legend_title_text="Decision")
st.plotly_chart(chart, use_container_width=True)

display_columns = [
    "rank",
    "project_name",
    "country",
    "region",
    "screening_score",
    "decision_band",
    "recommended_action",
]
st.dataframe(ranked[display_columns], use_container_width=True, hide_index=True)

st.subheader("Explain one project")
selected_name = st.selectbox("Project", ranked["project_name"].tolist())
selected_id = ranked.loc[ranked["project_name"] == selected_name, "project_id"].iloc[0]
explanation = engine.explain(ranked, selected_id)
explanation["criterion_label"] = explanation["criterion"].str.replace("_", " ").str.title()

explain_col, radar_col = st.columns(2)
with explain_col:
    contribution_chart = px.bar(
        explanation.sort_values("weighted_contribution"),
        x="weighted_contribution",
        y="criterion_label",
        orientation="h",
        labels={"weighted_contribution": "Points contributed", "criterion_label": "Criterion"},
    )
    st.plotly_chart(contribution_chart, use_container_width=True)
with radar_col:
    radar = go.Figure(
        data=go.Scatterpolar(
            r=explanation["input_score"].tolist() + [explanation["input_score"].iloc[0]],
            theta=explanation["criterion_label"].tolist() + [explanation["criterion_label"].iloc[0]],
            fill="toself",
            name=selected_name,
        )
    )
    radar.update_layout(polar={"radialaxis": {"visible": True, "range": [0, 100]}}, showlegend=False)
    st.plotly_chart(radar, use_container_width=True)

with st.expander("Weight sensitivity"):
    varied = st.selectbox("Vary criterion", DEFAULT_CRITERIA)
    sensitivity = one_way_sensitivity(projects, engine.weights, varied, [0.10, 0.20, 0.30, 0.40, 0.50])
    sensitivity_chart = px.line(
        sensitivity,
        x="trial_weight",
        y="screening_score",
        color="project_name",
        markers=True,
        labels={"trial_weight": "Selected criterion weight", "screening_score": "Score"},
    )
    st.plotly_chart(sensitivity_chart, use_container_width=True)

with st.expander("Monte Carlo rank stability"):
    with st.spinner("Testing ranking stability..."):
        stability = monte_carlo_rank_stability(projects, DEFAULT_CRITERIA, iterations=iterations)
    st.dataframe(stability, use_container_width=True, hide_index=True)

st.download_button(
    "Download ranked results",
    ranked.to_csv(index=False).encode("utf-8"),
    file_name="ccs_project_rankings.csv",
    mime="text/csv",
)

st.info(
    "Demonstration only. Scores support structured discussion and do not replace technical, "
    "commercial, legal, environmental, or investment due diligence."
)

