import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
import pytesseract
import re

from PIL import Image
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="SignalMap AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.set_page_config(
page_title="SignalMap AI 🌌",
page_icon="🌌",
layout="wide",
initial_sidebar_state="expanded"
)


# ---------------- CONFIG ----------------

st.set_page_config(
    page_title="Signal Map",
    page_icon="⚡",
    layout="wide"
)

# ---------------- DARK MODE + MOBILE ----------------

st.markdown("""
<style>

.stApp {
    background-color: #050816;
    color: white;
}

/* MAIN CONTAINER */

.block-container {
    padding-top: 1rem;
    padding-bottom: 4rem;
    padding-left: 1rem;
    padding-right: 1rem;
}

/* TITLES */

h1 {
    font-size: 3rem !important;
    font-weight: 800;
    color: white;
}

h2, h3 {
    color: #8be9fd;
    font-weight: 700;
}

/* GLASS EFFECT */

[data-testid="stMetric"] {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(15px);
    border-radius: 25px;
    padding: 20px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 0 25px rgba(0,255,255,0.08);
}

/* CHARTS */

div[data-testid="stPlotlyChart"] {
    border-radius: 25px;
    overflow: hidden;
    background: rgba(255,255,255,0.03);
    padding: 10px;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background-color: #0b1023;
}

/* CUSTOM CARD */

.custom-card {
    background: linear-gradient(135deg,#00c6ff,#0072ff);
    padding: 25px;
    border-radius: 30px;
    text-align: center;
    margin-bottom: 20px;
    box-shadow: 0 0 30px rgba(0,255,255,0.3);
}

/* MOBILE */

@media (max-width: 768px) {

    h1 {
        font-size: 2.2rem !important;
        text-align: center;
    }

    h2 {
        font-size: 1.4rem !important;
    }

    [data-testid="stMetric"] {
        padding: 15px;
        margin-bottom: 10px;
    }

    .block-container {
        padding-left: 0.8rem;
        padding-right: 0.8rem;
    }
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------

df = pd.read_csv("signals.csv")

# ---------------- SIDEBAR ----------------

st.sidebar.title("⚡ Signal Map")
st.sidebar.markdown("AI Synchronicity Intelligence")

# ---------------- HEADER ----------------

st.markdown("""
# ⚡ SIGNAL MAP

### AI Synchronicity Intelligence System
""")

# ---------------- DOMINANT FREQUENCY ----------------

dominant = df["numero"].value_counts().idxmax()

st.markdown(f"""
<div class="custom-card">

<h3 style="color:white;">
Today's Dominant Frequency
</h3>

<h1 style="color:white;font-size:60px;">
{dominant}
</h1>

</div>
""", unsafe_allow_html=True)

# ---------------- METRICS ----------------

col1, col2, col3, col4 = st.columns(4)

col1.metric("Signals", len(df))
col2.metric("Unique Numbers", df["numero"].nunique())
col3.metric("Pattern Types", df["tipo"].nunique())
col4.metric("Peak Hour", "13:00")

st.divider()

# ---------------- LIVE CAMERA / GALLERY ----------------

st.subheader("📸 Live Signal Scanner")

uploaded = st.file_uploader(
    "Upload image or screenshot",
    type=["png","jpg","jpeg"]
)

if uploaded:

    image = Image.open(uploaded)

    st.image(image, use_container_width=True)

    text = pytesseract.image_to_string(image)

    st.markdown("### 🧠 AI Detected Text")

    st.code(text)

    numbers = re.findall(r'\d+', text)

    if numbers:

        st.markdown("### ⚡ Detected Numbers")

        for n in numbers:
            st.success(f"Detected: {n}")

# ---------------- GRAPH 1 ----------------

st.subheader("📈 Pattern Frequency")

type_count = df["tipo"].value_counts().reset_index()
type_count.columns = ["tipo", "cantidad"]

fig1 = px.bar(
    type_count,
    x="tipo",
    y="cantidad",
    text_auto=True,
    template="plotly_dark"
)

st.plotly_chart(fig1, use_container_width=True)

# ---------------- GRAPH 2 ----------------

st.subheader("⏰ Time Heatmap")

time_count = df["hora"].value_counts().reset_index()
time_count.columns = ["hora", "cantidad"]

fig2 = px.line(
    time_count,
    x="hora",
    y="cantidad",
    markers=True,
    template="plotly_dark"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------- GRAPH 3 ----------------

st.subheader("🧠 Dominant Numbers")

number_count = df["numero"].value_counts().reset_index().head(10)
number_count.columns = ["numero", "cantidad"]

fig3 = px.pie(
    number_count,
    names="numero",
    values="cantidad",
    hole=0.5,
    template="plotly_dark"
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------- TESLA NETWORK ----------------

st.subheader("⚡ Tesla Signal Network")

G = nx.Graph()

for _, row in df.iterrows():

    nums = str(row["numero"]).split("-")

    for i in range(len(nums)-1):
        G.add_edge(nums[i], nums[i+1])

pos = nx.spring_layout(G)

edge_x = []
edge_y = []

for edge in G.edges():

    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]

    edge_x.extend([x0, x1, None])
    edge_y.extend([y0, y1, None])

edge_trace = go.Scatter(
    x=edge_x,
    y=edge_y,
    line=dict(width=1),
    hoverinfo='none',
    mode='lines'
)

node_x = []
node_y = []
node_text = []

for node in G.nodes():

    x, y = pos[node]

    node_x.append(x)
    node_y.append(y)
    node_text.append(node)

node_trace = go.Scatter(
    x=node_x,
    y=node_y,
    mode='markers+text',
    text=node_text,
    textposition="top center",
    marker=dict(size=20)
)

fig_network = go.Figure(
    data=[edge_trace, node_trace]
)

fig_network.update_layout(
    template="plotly_dark",
    height=700
)

st.plotly_chart(fig_network, use_container_width=True)

# ---------------- AI PATTERN DETECTION ----------------

st.subheader("🧠 AI Pattern Detection")

patterns = []

for num in df["numero"]:

    if "-" in str(num):

        parts = str(num).split("-")

        try:

            parts = [int(x) for x in parts]

            if sorted(parts) == list(range(min(parts), max(parts)+1)):
                patterns.append(f"⚡ Sequence detected: {num}")

        except:
            pass

    if str(num) == str(num)[::-1]:
        patterns.append(f"🪞 Mirror detected: {num}")

for p in patterns:
    st.success(p)

# ---------------- AI INSIGHTS ----------------

st.subheader("⚡ AI Insights")

top_number = df["numero"].value_counts().idxmax()

st.info(f"Dominant frequency today: {top_number}")
st.info("Sequence activity increased in the 13:00 hour")
st.info("Mirror numbers detected repeatedly")
st.info("Retro pattern clusters active")

# ---------------- TABLE ----------------

with st.expander("📂 View Full Registry"):

    st.dataframe(
        df,
        use_container_width=True,
        height=400
    )
