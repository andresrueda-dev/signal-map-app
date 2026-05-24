import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import json
import os
import glob

from datetime import datetime

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Signal Map AI",
    layout="wide"
)

# ==================================================
# PREMIUM STYLE
# ==================================================

st.markdown("""
<style>

.stApp{
    background-color:#050816;
    color:white;
}

[data-testid="stSidebar"]{
    background-color:#0B1026;
}

h1,h2,h3,h4{
    color:#C8B6FF;
}

div.stButton > button{
    background:#7B61FF;
    color:white;
    border-radius:12px;
    border:none;
    padding:0.6rem 1rem;
    font-weight:bold;
}

div.stMetric{
    background-color:#11162A;
    padding:10px;
    border-radius:10px;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.title("SIGNAL MAP AI")

page = st.sidebar.radio(
    "Navigation",
    [
        "Live Signal",
        "Signal Journal",
        "Timeline",
        "Insights"
    ]
)

# ==================================================
# SAVE SIGNAL
# ==================================================

def save_signal(signal_data):

    os.makedirs("signals", exist_ok=True)

    filename = f"signals/{signal_data['date']}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(signal_data, f, indent=4)

# ==================================================
# LOAD SIGNAL
# ==================================================

def load_signal(date):

    filename = f"signals/{date}.json"

    if os.path.exists(filename):

        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)

    return None

# ==================================================
# PATTERN ANALYSIS ENGINE
# ==================================================

def analyze_pattern(nodes):

    x_values = [n[0] for n in nodes]
    y_values = [n[1] for n in nodes]

    symmetry_score = round(
        1 - abs(np.mean(x_values)),
        2
    )

    vertical_alignment = np.std(x_values) < 0.25

    lower_density = np.mean(y_values) < 0

    reading = []

    if symmetry_score > 0.75:
        reading.append(
            "High symmetry detected indicating alignment."
        )

    if vertical_alignment:
        reading.append(
            "Strong central axis formation detected."
        )

    if lower_density:
        reading.append(
            "Lower-node concentration suggests grounding and manifestation."
        )

    if len(reading) == 0:
        reading.append(
            "Distributed exploratory structure detected."
        )

    return {
        "pattern_type": "Humanoid Structure",
        "energy_type": "Convergent",
        "symmetry_score": symmetry_score,
        "reading": " ".join(reading)
    }

# ==================================================
# GENERATE SIGNAL NODES
# ==================================================

np.random.seed(7)

nodes = [

    (0.00, 0.60),
    (-0.15, 0.50),
    (0.15, 0.50),

    (-0.25, 0.30),
    (0.25, 0.30),

    (-0.10, 0.10),
    (0.10, 0.10),

    (0.00, -0.10),

    (-0.15, -0.30),
    (0.15, -0.30),

    (-0.05, -0.55),
    (0.05, -0.55)

]

# ==================================================
# LIVE SIGNAL
# ==================================================

if page == "Live Signal":

    st.title("SIGNAL MAP AI")

    st.markdown("""
    ### Interactive Pattern Intelligence System

    Track • Analyze • Interpret • Archive
    """)

    analysis = analyze_pattern(nodes)

    x = [n[0] for n in nodes]
    y = [n[1] for n in nodes]

    fig = go.Figure()

    # CONNECTION LINES

    for i in range(len(nodes)-1):

        fig.add_trace(
            go.Scatter(
                x=[nodes[i][0], nodes[i+1][0]],
                y=[nodes[i][1], nodes[i+1][1]],
                mode="lines",
                line=dict(
                    width=2,
                    color="#7B61FF"
                ),
                hoverinfo="none",
                showlegend=False
            )
        )

    # NODES

    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="markers+text",

            marker=dict(
                size=18,
                color="#B388FF",
                line=dict(
                    width=2,
                    color="white"
                )
            ),

            text=[
                str(i+1)
                for i in range(len(nodes))
            ],

            textposition="top center",

            hovertemplate=
            "<b>Node %{text}</b><extra></extra>"
        )
    )

    fig.update_layout(

        height=700,

        paper_bgcolor="#050816",
        plot_bgcolor="#050816",

        font=dict(
            color="white"
        ),

        xaxis=dict(
            visible=False
        ),

        yaxis=dict(
            visible=False
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # METRICS

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Symmetry",
            f"{analysis['symmetry_score'] * 100:.0f}%"
        )

    with col2:

        st.metric(
            "Pattern",
            analysis["pattern_type"]
        )

    with col3:

        st.metric(
            "Energy",
            analysis["energy_type"]
        )

    # AI READING

    st.subheader("Pattern Reading AI")

    st.info(
        analysis["reading"]
    )

    # SAVE BUTTON

    if st.button("Save Current Signal"):

        signal_entry = {

            "date": str(datetime.now().date()),

            "title": "Central Alignment Formation",

            "pattern_type": analysis["pattern_type"],

            "energy_type": analysis["energy_type"],

            "symmetry_score": analysis["symmetry_score"],

            "intensity": 92,

            "reading": analysis["reading"],

            "created_at": str(datetime.now())
        }

        save_signal(signal_entry)

        st.success(
            "Signal saved successfully."
        )

# ==================================================
# SIGNAL JOURNAL
# ==================================================

if page == "Signal Journal":

    st.title("Signal Journal")

    selected_date = st.date_input(
        "Select Signal Date"
    )

    signal = load_signal(
        str(selected_date)
    )

    if signal:

        st.subheader(
            signal["title"]
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Symmetry",
                f"{signal['symmetry_score'] * 100:.0f}%"
            )

        with col2:

            st.metric(
                "Intensity",
                signal["intensity"]
            )

        st.markdown(
            f"### Pattern Type: {signal['pattern_type']}"
        )

        st.markdown(
            f"### Energy Type: {signal['energy_type']}"
        )

        st.info(
            signal["reading"]
        )

    else:

        st.warning(
            "No saved signal for this date."
        )

# ==================================================
# TIMELINE
# ==================================================

if page == "Timeline":

    st.title("Signal Timeline")

    files = sorted(
        glob.glob("signals/*.json")
    )

    if len(files) == 0:

        st.warning(
            "No saved signals yet."
        )

    for file in files:

        with open(file, "r", encoding="utf-8") as f:

            signal = json.load(f)

            st.markdown(f"""
            ---
            ## {signal['date']}

            ### {signal['pattern_type']}

            **Energy Type**
            {signal['energy_type']}

            **Symmetry**
            {signal['symmetry_score'] * 100:.0f}%

            **Reading**
            {signal['reading']}
            """)

# ==================================================
# INSIGHTS
# ==================================================

if page == "Insights":

    st.title("Insights")

    files = sorted(
        glob.glob("signals/*.json")
    )

    if len(files) == 0:

        st.warning(
            "Not enough saved signals yet."
        )

    else:

        symmetry_scores = []

        for file in files:

            with open(file, "r", encoding="utf-8") as f:

                signal = json.load(f)

                symmetry_scores.append(
                    signal["symmetry_score"]
                )

        avg_symmetry = np.mean(
            symmetry_scores
        )

        st.metric(
            "Average Symmetry",
            f"{avg_symmetry * 100:.0f}%"
        )

        st.markdown("""
        ### AI Insight

        Recent formations reveal increasing structural consistency
        and progressive convergence patterns across saved signals.

        The system detects stabilization tendencies
        and stronger central-axis manifestations.
        """)
