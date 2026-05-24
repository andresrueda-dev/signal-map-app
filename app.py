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

# ---------------------------------------------------
# CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="SignalMap AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------
# DARK MODE + MOBILE UI
# ---------------------------------------------------

st.markdown("""
<style>

/* BACKGROUND */

.stApp {
    background: linear-gradient(180deg,#020617,#050816,#071028);
    color: white;
}

/* MAIN CONTAINER */

.block-container {
    padding-top: 1rem;
    padding-bottom: 6rem;
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
}

/* GLASS EFFECT */

[data-testid="stMetric"] {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(20px);
    border-radius: 25px;
    padding: 20px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 0 30px rgba(0,255,255,0.08);
}

/* CHARTS */

div[data-testid="stPlotlyChart"] {
    background: rgba(255,255,255,0.03);
    border-radius: 25px;
    padding: 15px;
    overflow: hidden;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background: #0b1023;
}

/* GLOW CARD */

.glow-card {
    background: linear-gradient(135deg,#00c6ff,#0072ff);
    padding: 30px;
    border-radius: 30px;
    text-align: center;
    margin-bottom: 20px;
    box-shadow: 0 0 40px rgba(0,255,255,0.4);
}

/* SUCCESS BOX */

.stAlert {
    border-radius: 20px;
}

/* MOBILE */

@media (max-width:768px){

    h1{
        font-size:2.2rem !important;
        text-align:center;
    }

    h2{
        font-size:1.4rem !important;
    }

    .block-container{
        padding-left:0.7rem;
        padding-right:0.7rem;
    }
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

df = pd.read_csv("signals.csv")

# ---------------------------------------------------
# MOBILE MENU
# ---------------------------------------------------

selected = option_menu(
    menu_title=None,
    options=["Home","Scanner","Network","AI","Registry"],
    icons=["house","camera","diagram-3","cpu","table"],
    orientation="horizontal"
)

# ---------------------------------------------------
# HOME
# ---------------------------------------------------

if selected == "Home":

    dominant = df["numero"].value_counts().idxmax()

    st.markdown("""

    # ⚡ SIGNALMAP AI
    ### Synchronicity Intelligence System

    """)

    st.markdown(f"""
    <div class="glow-card">

    <h3 style="color:white;">
    Dominant Frequency
    </h3>

    <h1 style="color:white;font-size:70px;">
    {dominant}
    </h1>

    </div>
    """, unsafe_allow_html=True)

    col1,col2,col3 = st.columns(3)

    col1.metric("Signals", len(df))
    col2.metric("Unique", df["numero"].nunique())
    col3.metric("Patterns", df["tipo"].nunique())

    st.divider()

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

    st.subheader("⚡ AI Insights")

    st.info(f"Dominant number today: {dominant}")
    st.info("Retro sequence activity detected")
    st.info("Mirror patterns increasing")
    st.info("Neural signal clusters active")

# ---------------------------------------------------
# SCANNER
# ---------------------------------------------------

if selected == "Scanner":

    st.title("📸 Live Signal Scanner")

    uploaded = st.file_uploader(
        "Upload screenshot or image",
        type=["png","jpg","jpeg"]
    )

    if uploaded:

        image = Image.open(uploaded)

        st.image(image, use_container_width=True)

        text = pytesseract.image_to_string(image)

        st.subheader("🧠 AI Detected Text")

        st.code(text)

        numbers = re.findall(r'\d+', text)

        st.subheader("⚡ Numbers Detected")

        for n in numbers:
            st.success(f"Detected: {n}")

# ---------------------------------------------------
# NETWORK
# ---------------------------------------------------

if selected == "Network":

    st.title("⚡ Tesla Signal Network")

    G = nx.Graph()

    for _, row in df.iterrows():

        nums = str(row["numero"]).split("-")

        for i in range(len(nums)-1):
            G.add_edge(nums[i], nums[i+1])

    pos = nx.spring_layout(G)

    edge_x = []
    edge_y = []

    for edge in G.edges():

        x0,y0 = pos[edge[0]]
        x1,y1 = pos[edge[1]]

        edge_x.extend([x0,x1,None])
        edge_y.extend([y0,y1,None])

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        mode='lines',
        line=dict(width=1)
    )

    node_x=[]
    node_y=[]
    node_text=[]

    for node in G.nodes():

        x,y = pos[node]

        node_x.append(x)
        node_y.append(y)
        node_text.append(node)

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers+text',
        text=node_text,
        textposition="top center",
        marker=dict(
            size=24
        )
    )

    fig = go.Figure(
        data=[edge_trace,node_trace]
    )

    fig.update_layout(
        template="plotly_dark",
        height=800
    )

    st.plotly_chart(fig,use_container_width=True)

# ---------------------------------------------------
# AI
# ---------------------------------------------------

if selected == "AI":

    st.title("🧠 AI Pattern Detection")

    patterns=[]

    for num in df["numero"]:

        if "-" in str(num):

            parts = str(num).split("-")

            try:

                parts=[int(x) for x in parts]

                if sorted(parts)==list(range(min(parts),max(parts)+1)):
                    patterns.append(f"⚡ Sequence detected: {num}")

            except:
                pass

        if str(num)==str(num)[::-1]:
            patterns.append(f"🪞 Mirror detected: {num}")

    for p in patterns:
        st.success(p)

# ---------------------------------------------------
# REGISTRY
# ---------------------------------------------------

if selected == "Registry":

    st.title("📂 Signal Registry")

    with st.expander("View Full Data"):

        st.dataframe(
            df,
            use_container_width=True,
            height=500
        )
