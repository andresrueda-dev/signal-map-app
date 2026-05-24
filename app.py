import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
import pytesseract
import re
import random

from PIL import Image
from streamlit_option_menu import option_menu

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="SignalMap AI",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# =====================================================
# COSMIC UI
# =====================================================

st.markdown("""
<style>

/* =====================================================
BACKGROUND COSMOS
===================================================== */

.stApp {
    background:
    radial-gradient(circle at top,#081b3a 0%,#020617 45%,#000000 100%);
    color:white;
    overflow-x:hidden;
}

/* =====================================================
STARFIELD
===================================================== */

.stApp::before{
    content:"";
    position:fixed;
    width:100%;
    height:100%;
    top:0;
    left:0;
    background-image:
    radial-gradient(white 1px, transparent 1px),
    radial-gradient(#00c6ff 1px, transparent 1px),
    radial-gradient(#ffffff 2px, transparent 2px);

    background-size:
    120px 120px,
    180px 180px,
    250px 250px;

    background-position:
    0 0,
    40px 60px,
    130px 90px;

    opacity:0.12;
    z-index:-1;

    animation: starsMove 120s linear infinite;
}

@keyframes starsMove{
    from{
        transform:translateY(0px);
    }
    to{
        transform:translateY(-1000px);
    }
}

/* =====================================================
SMOOTH ANIMATION
===================================================== */

*{
    transition:all 0.4s ease;
}

/* =====================================================
MAIN CONTAINER
===================================================== */

.block-container{
    padding-top:1rem;
    padding-bottom:6rem;
    padding-left:0.8rem;
    padding-right:0.8rem;
    animation:fadeIn 1.2s ease;
}

@keyframes fadeIn{
    from{
        opacity:0;
        transform:translateY(25px);
    }
    to{
        opacity:1;
        transform:translateY(0px);
    }
}

/* =====================================================
TEXT
===================================================== */

h1{
    font-size:2.4rem !important;
    font-weight:800;
    color:white;
    text-align:center;
}

h2,h3{
    color:#8be9fd;
    font-weight:700;
}

/* =====================================================
GLASS CARDS
===================================================== */

[data-testid="stMetric"]{
    background:rgba(255,255,255,0.05);
    backdrop-filter:blur(18px);
    border-radius:25px;
    padding:18px;
    border:1px solid rgba(255,255,255,0.08);
    box-shadow:0 0 25px rgba(0,255,255,0.08);
}

/* =====================================================
CHARTS
===================================================== */

div[data-testid="stPlotlyChart"]{
    background:rgba(255,255,255,0.03);
    border-radius:25px;
    padding:12px;
    overflow:hidden;
    backdrop-filter:blur(12px);
}

/* =====================================================
GLOW CARD
===================================================== */

.glow-card{
    background:linear-gradient(135deg,#00c6ff,#0072ff);
    padding:30px;
    border-radius:30px;
    text-align:center;
    margin-bottom:20px;
    box-shadow:0 0 50px rgba(0,255,255,0.35);
}

/* =====================================================
MENU
===================================================== */

.nav-link{
    font-size:18px !important;
}

/* =====================================================
PLOT MOBILE
===================================================== */

@media (max-width:768px){

    h1{
        font-size:2rem !important;
    }

    iframe{
        height:350px !important;
    }

    .js-plotly-plot{
        height:350px !important;
    }

}

</style>
""", unsafe_allow_html=True)

# =====================================================
# SPLASH SCREEN
# =====================================================

with st.container():

    st.markdown("""

    <div style="
    text-align:center;
    padding:10px;
    margin-bottom:20px;
    animation:fadeIn 2s ease;
    ">

    <h1>⚡ SIGNALMAP AI</h1>

    <p style="
    color:#8be9fd;
    font-size:18px;
    ">
    Synchronicity Intelligence System
    </p>

    </div>

    """, unsafe_allow_html=True)

# =====================================================
# LOAD DATA
# =====================================================

df = pd.read_csv("signals.csv")

# =====================================================
# MOBILE MENU
# =====================================================

selected = option_menu(
    menu_title=None,
    options=["Home","Scanner","Constellation","AI","Registry"],
    icons=["house","camera","stars","cpu","table"],
    orientation="horizontal"
)

# =====================================================
# HOME
# =====================================================

if selected == "Home":

    dominant = df["numero"].value_counts().idxmax()

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

    col1 = st.columns(1)[0]

    col1.metric("Signals", len(df))

    st.subheader("⚡ AI Insights")

    st.info(f"Dominant number detected today: {dominant}")
    st.info("Retro sequence clusters active")
    st.info("Mirror frequencies increasing")
    st.info("Constellation mapping stabilized")

# =====================================================
# LIVE CAMERA / GALLERY
# =====================================================

if selected == "Scanner":

    st.title("📸 Live Signal Scanner")

    uploaded = st.file_uploader(
        "Upload image or screenshot",
        type=["png","jpg","jpeg"]
    )

    if uploaded:

        image = Image.open(uploaded)

        st.image(image,use_container_width=True)

        text = pytesseract.image_to_string(image)

        st.subheader("🧠 AI Detected Text")

        st.code(text)

        numbers = re.findall(r'\d+', text)

        st.subheader("⚡ Numbers Detected")

        for n in numbers:
            st.success(f"Detected frequency: {n}")

# =====================================================
# CONSTELLATION MAP
# =====================================================

if selected == "Constellation":

    st.title("🌌 Cosmic Constellation Map")

    G = nx.Graph()

    for _, row in df.iterrows():

        nums = str(row["numero"]).split("-")

        for i in range(len(nums)-1):
            G.add_edge(nums[i], nums[i+1])

    pos = nx.spring_layout(
        G,
        seed=42,
        k=1.5
    )

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
        line=dict(
            width=1.5,
            color="#4cc9f0"
        ),
        hoverinfo='none',
        mode='lines'
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
            size=38,
            color="#ffffff",
            line=dict(
                width=2,
                color="#00c6ff"
            )
        )
    )

    fig = go.Figure(
        data=[edge_trace,node_trace]
    )

    fig.update_layout(

        template="plotly_dark",

        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",

        xaxis=dict(
            showgrid=False,
            zeroline=False,
            visible=False
        ),

        yaxis=dict(
            showgrid=False,
            zeroline=False,
            visible=False
        ),

        height=500,

        margin=dict(
            l=0,
            r=0,
            t=0,
            b=0
        )
    )

    st.plotly_chart(fig,use_container_width=True)

# =====================================================
# AI DETECTION
# =====================================================

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

# =====================================================
# REGISTRY
# =====================================================

if selected == "Registry":

    st.title("📂 Signal Registry")

    with st.expander("View Full Registry"):

        st.dataframe(
            df,
            use_container_width=True,
            height=400
        )
