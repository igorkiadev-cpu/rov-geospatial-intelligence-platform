import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

# Corrige import do src no Streamlit Cloud
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.geospatial_analysis import load_data

# -------------------------------
# CONFIG PAGE
# -------------------------------
st.set_page_config(page_title="ROV Mission Intelligence", layout="wide")

st.title("🌊 ROV Mission Intelligence Platform")
st.markdown("Transforming ROV telemetry into subsea insights")

# -------------------------------
# FILE UPLOAD
# -------------------------------
uploaded_file = st.file_uploader("Upload ROV CSV", type=["csv"])

if uploaded_file:
    df = load_data(uploaded_file)

    # -------------------------------
    # CLEAN DATA
    # -------------------------------
    df.columns = df.columns.str.strip().str.lower()

    required_columns = {"latitude", "longitude", "depth"}

    if not required_columns.issubset(df.columns):
        st.error("CSV must contain: latitude, longitude, depth")
        st.stop()

    # Convert + clean
    for col in ["latitude", "longitude", "depth"]:
        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].str.replace(",", ".", regex=False)
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["latitude", "longitude", "depth"])

    # -------------------------------
    # PERFORMANCE (BIG DATA SAFE)
    # -------------------------------
    if len(df) > 5000:
        df = df.sample(5000)

    # -------------------------------
    # SIDEBAR FILTERS
    # -------------------------------
    st.sidebar.header("Filters")

    min_depth, max_depth = float(df["depth"].min()), float(df["depth"].max())

    depth_range = st.sidebar.slider(
        "Depth Range",
        min_value=min_depth,
        max_value=max_depth,
        value=(min_depth, max_depth)
    )

    df = df[(df["depth"] >= depth_range[0]) & (df["depth"] <= depth_range[1])]

    # -------------------------------
    # KPIs
    # -------------------------------
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Points", len(df))
    col2.metric("Max Depth", f"{df['depth'].max():.2f}")
    col3.metric("Min Depth", f"{df['depth'].min():.2f}")

    st.markdown("---")

    # -------------------------------
    # VIEW SELECTOR
    # -------------------------------
    view = st.radio("Select Visualization", ["2D Map", "3D Subsea View"], horizontal=True)

    # -------------------------------
    # 2D MAP
    # -------------------------------
    if view == "2D Map":
        fig = px.scatter_mapbox(
            df,
            lat="latitude",
            lon="longitude",
            color="depth",
            color_continuous_scale="Viridis",
            zoom=5,
            height=600,
            hover_data=["depth"]
        )

        fig.update_layout(
            mapbox_style="open-street-map",
            margin=dict(l=0, r=0, t=0, b=0)
        )

    # -------------------------------
    # 3D VIEW
    # -------------------------------
    else:
        df["depth_visual"] = -df["depth"]

        fig = px.scatter_3d(
            df,
            x="longitude",
            y="latitude",
            z="depth_visual",
            color="depth",
            color_continuous_scale="Viridis",
            height=700
        )

        fig.update_traces(marker=dict(size=3))

        fig.update_layout(
            scene=dict(
                xaxis_title="Longitude",
                yaxis_title="Latitude",
                zaxis_title="Depth"
            ),
            margin=dict(l=0, r=0, t=0, b=0)
        )

    # -------------------------------
    # SHOW CHART
    # -------------------------------
    st.plotly_chart(fig, use_container_width=True)

    # -------------------------------
    # DATA PREVIEW
    # -------------------------------
    with st.expander("View Raw Data"):
        st.dataframe(df.head(100))
