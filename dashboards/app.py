import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

# Import fix
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.geospatial_analysis import load_data

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="ROV Mission Intelligence", layout="wide")

st.title("🌊 ROV Mission Intelligence Platform")
st.markdown("Advanced subsea mission visualization & analytics")

# -------------------------------
# UPLOAD
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

    # Optional timestamp (pra replay)
    has_time = "timestamp" in df.columns

    # Convert data
    for col in ["latitude", "longitude", "depth"]:
        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].str.replace(",", ".", regex=False)
        df[col] = pd.to_numeric(df[col], errors="coerce")

    if has_time:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    df = df.dropna(subset=["latitude", "longitude", "depth"])

    # Ordena por tempo (importante pro replay)
    if has_time:
        df = df.sort_values("timestamp")

    # -------------------------------
    # PERFORMANCE
    # -------------------------------
    if len(df) > 8000:
        df = df.sample(8000)

    # -------------------------------
    # SIDEBAR
    # -------------------------------
    st.sidebar.header("Mission Controls")

    min_depth, max_depth = float(df["depth"].min()), float(df["depth"].max())

    depth_range = st.sidebar.slider(
        "Depth Filter",
        min_value=min_depth,
        max_value=max_depth,
        value=(min_depth, max_depth)
    )

    df = df[(df["depth"] >= depth_range[0]) & (df["depth"] <= depth_range[1])]

    # -------------------------------
    # KPIs
    # -------------------------------
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Data Points", len(df))
    col2.metric("Max Depth", f"{df['depth'].max():.1f}")
    col3.metric("Min Depth", f"{df['depth'].min():.1f}")

    if has_time:
        duration = (df["timestamp"].max() - df["timestamp"].min()).total_seconds() / 60
        col4.metric("Mission Duration (min)", f"{duration:.1f}")
    else:
        col4.metric("Mission Duration", "N/A")

    st.markdown("---")

    # -------------------------------
    # VIEW MODE
    # -------------------------------
    view = st.radio(
        "Select Mode",
        ["2D Map", "3D View", "Trajectory", "Mission Replay"],
        horizontal=True
    )

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

        fig.update_layout(mapbox_style="open-street-map")

    # -------------------------------
    # 3D VIEW
    # -------------------------------
    elif view == "3D View":
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

    # -------------------------------
    # TRAJECTORY (PATH)
    # -------------------------------
    elif view == "Trajectory":

        if has_time:
            fig = px.line_mapbox(
                df,
                lat="latitude",
                lon="longitude",
                color="depth",
                zoom=5,
                height=600
            )
        else:
            fig = px.line_mapbox(
                df.reset_index(),
                lat="latitude",
                lon="longitude",
                zoom=5,
                height=600
            )

        fig.update_layout(mapbox_style="open-street-map")

    # -------------------------------
    # REPLAY (ANIMATION)
    # -------------------------------
    else:
        if not has_time:
            st.warning("Replay requires a 'timestamp' column")
            st.stop()

        # Reduz granularidade (performance)
        df["time_group"] = df["timestamp"].dt.floor("10s")

        fig = px.scatter_mapbox(
            df,
            lat="latitude",
            lon="longitude",
            color="depth",
            animation_frame="time_group",
            zoom=5,
            height=600
        )

        fig.update_layout(mapbox_style="open-street-map")

    # -------------------------------
    # SHOW
    # -------------------------------
    st.plotly_chart(fig, use_container_width=True)

    # -------------------------------
    # DATA PREVIEW
    # -------------------------------
    with st.expander("Raw Data"):
        st.dataframe(df.head(200))
